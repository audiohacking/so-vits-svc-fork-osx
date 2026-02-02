from __future__ import annotations

import json
import multiprocessing
import os
from logging import getLogger
from pathlib import Path
from typing import Any

import sounddevice as sd
import soundfile as sf
import torch
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pebble import ProcessFuture, ProcessPool

from .. import __version__
from ..utils import get_optimal_device

GUI_DEFAULT_PRESETS_PATH = Path(__file__).parent.parent / "default_gui_presets.json"
GUI_PRESETS_PATH = Path("./user_gui_presets.json").absolute()

LOG = getLogger(__name__)


def load_presets() -> dict:
    """Load presets from default and user files."""
    defaults = json.loads(GUI_DEFAULT_PRESETS_PATH.read_text("utf-8"))
    users = json.loads(GUI_PRESETS_PATH.read_text("utf-8")) if GUI_PRESETS_PATH.exists() else {}
    # priority: users > defaults (users override defaults)
    # order: defaults -> users (defaults listed first, then user presets)
    return {**defaults, **users}


def save_presets(presets: dict) -> None:
    """Save presets to user file."""
    with GUI_PRESETS_PATH.open("w") as f:
        json.dump(presets, f, indent=2)


def get_devices(update: bool = True) -> tuple[list[str], list[str], list[int], list[int]]:
    """Get available audio devices."""
    if update:
        sd._terminate()
        sd._initialize()
    devices = sd.query_devices()
    hostapis = sd.query_hostapis()
    for hostapi in hostapis:
        for device_idx in hostapi["devices"]:
            devices[device_idx]["hostapi_name"] = hostapi["name"]
    input_devices = [f"{d['name']} ({d['hostapi_name']})" for d in devices if d["max_input_channels"] > 0]
    output_devices = [f"{d['name']} ({d['hostapi_name']})" for d in devices if d["max_output_channels"] > 0]
    input_devices_indices = [d["index"] for d in devices if d["max_input_channels"] > 0]
    output_devices_indices = [d["index"] for d in devices if d["max_output_channels"] > 0]
    return input_devices, output_devices, input_devices_indices, output_devices_indices


def create_app() -> FastAPI:
    """Create FastAPI application for the web UI."""
    app = FastAPI(title="So-VITS-SVC Fork", version=__version__)

    # Global state for process pool and futures
    app.state.pool = None
    app.state.realtime_future = None
    app.state.infer_futures = set()

    @app.on_event("startup")
    async def startup_event():
        """Initialize process pool on startup."""
        app.state.pool = ProcessPool(
            max_workers=min(2, multiprocessing.cpu_count()),
            context=multiprocessing.get_context("spawn"),
        )

    @app.on_event("shutdown")
    async def shutdown_event():
        """Clean up process pool on shutdown."""
        if app.state.realtime_future:
            app.state.realtime_future.cancel()
        if app.state.pool:
            app.state.pool.close()
            app.state.pool.join()

    @app.get("/")
    async def read_root():
        """Serve the main HTML page."""
        html_path = Path(__file__).parent / "index.html"
        return FileResponse(html_path)

    @app.get("/api/presets")
    async def get_presets():
        """Get all presets."""
        try:
            presets = load_presets()
            return JSONResponse(content=presets)
        except Exception as e:
            LOG.exception(e)
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/presets")
    async def add_preset(data: dict):
        """Add a new preset."""
        try:
            name = data.get("name")
            preset = data.get("preset")
            if not name or not preset:
                raise HTTPException(status_code=400, detail="Name and preset are required")

            presets = load_presets()
            presets[name] = preset
            save_presets(presets)
            return JSONResponse(content={"status": "success"})
        except Exception as e:
            LOG.exception(e)
            raise HTTPException(status_code=500, detail=str(e))

    @app.delete("/api/presets/{name}")
    async def delete_preset(name: str):
        """Delete a preset."""
        try:
            presets = load_presets()
            if name in presets:
                del presets[name]
                save_presets(presets)
            return JSONResponse(content={"status": "success"})
        except Exception as e:
            LOG.exception(e)
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/devices")
    async def get_audio_devices():
        """Get available audio devices."""
        try:
            input_devices, output_devices, _, _ = get_devices()
            return JSONResponse(
                content={
                    "input_devices": input_devices,
                    "output_devices": output_devices,
                }
            )
        except Exception as e:
            LOG.exception(e)
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/default-paths")
    async def get_default_paths():
        """Get default paths for model, config, and cluster model."""
        try:
            model_candidates = sorted(Path("./logs/44k/").glob("G_*.pth"))
            model_path = model_candidates[-1].absolute().as_posix() if model_candidates else ""

            config_path = ""
            if Path("./configs/44k/config.json").exists():
                config_path = Path("./configs/44k/config.json").absolute().as_posix()

            cluster_model_path = ""
            if Path("./logs/44k/kmeans.pt").exists():
                cluster_model_path = Path("./logs/44k/kmeans.pt").absolute().as_posix()

            return JSONResponse(
                content={
                    "model_path": model_path,
                    "config_path": config_path,
                    "cluster_model_path": cluster_model_path,
                }
            )
        except Exception as e:
            LOG.exception(e)
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/speakers")
    async def get_speakers(config_path: str):
        """Get available speakers from config."""
        try:
            from .. import utils

            config_path_obj = Path(config_path)
            if not config_path_obj.exists() or not config_path_obj.is_file():
                raise HTTPException(status_code=404, detail="Config file not found")

            hp = utils.get_hparams(config_path)
            speakers = list(hp.__dict__["spk"].keys())
            return JSONResponse(content={"speakers": speakers})
        except Exception as e:
            LOG.exception(e)
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/infer")
    async def infer(data: dict):
        """Run inference on an audio file."""
        try:
            from ..inference.main import infer as infer_func

            # Extract parameters
            model_path = Path(data.get("model_path", ""))
            config_path = Path(data.get("config_path", ""))
            input_path = Path(data.get("input_path", ""))
            output_path = data.get("output_path", "")

            if not input_path.exists():
                raise HTTPException(status_code=404, detail="Input file not found")

            # Generate output path if not provided
            if not output_path:
                output_path = input_path.parent / f"{input_path.stem}.out{input_path.suffix}"
                file_num = 1
                while Path(output_path).exists():
                    output_path = input_path.parent / f"{input_path.stem}.out_{file_num}{input_path.suffix}"
                    file_num += 1
            output_path = Path(output_path)

            cluster_model_path = data.get("cluster_model_path")
            if cluster_model_path:
                cluster_model_path = Path(cluster_model_path)
            else:
                cluster_model_path = None

            # Run inference
            infer_future = app.state.pool.schedule(
                infer_func,
                kwargs=dict(
                    model_path=model_path,
                    output_path=output_path,
                    input_path=input_path,
                    config_path=config_path,
                    recursive=True,
                    speaker=data.get("speaker", ""),
                    cluster_model_path=cluster_model_path,
                    transpose=data.get("transpose", 0),
                    auto_predict_f0=data.get("auto_predict_f0", True),
                    cluster_infer_ratio=data.get("cluster_infer_ratio", 0.0),
                    noise_scale=data.get("noise_scale", 0.4),
                    f0_method=data.get("f0_method", "dio"),
                    db_thresh=data.get("db_thresh", -35),
                    pad_seconds=data.get("pad_seconds", 0.1),
                    chunk_seconds=data.get("chunk_seconds", 0.5),
                    absolute_thresh=data.get("absolute_thresh", True),
                    max_chunk_seconds=data.get("max_chunk_seconds", 40),
                    device=("cpu" if not data.get("use_gpu", True) else get_optimal_device()),
                ),
            )

            app.state.infer_futures.add(infer_future)

            # Wait for result
            result = infer_future.result()

            # Auto-play if requested
            if data.get("auto_play", False) and output_path.exists():
                audio_data, sr = sf.read(output_path.as_posix())
                sd.play(audio_data, sr)

            app.state.infer_futures.discard(infer_future)

            return JSONResponse(
                content={
                    "status": "success",
                    "output_path": str(output_path),
                }
            )
        except Exception as e:
            LOG.exception(e)
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/realtime/start")
    async def start_realtime(data: dict):
        """Start real-time voice conversion."""
        try:
            from ..inference.main import realtime

            # Cancel existing realtime if running
            if app.state.realtime_future:
                app.state.realtime_future.cancel()

            _, _, input_device_indices, output_device_indices = get_devices(update=False)

            # Find device indices
            input_device_name = data.get("input_device", "")
            output_device_name = data.get("output_device", "")

            input_devices, output_devices, _, _ = get_devices(update=False)
            input_device_idx = input_devices.index(input_device_name) if input_device_name in input_devices else 0
            output_device_idx = output_devices.index(output_device_name) if output_device_name in output_devices else 0

            cluster_model_path = data.get("cluster_model_path")
            if cluster_model_path:
                cluster_model_path = Path(cluster_model_path)
            else:
                cluster_model_path = None

            app.state.realtime_future = app.state.pool.schedule(
                realtime,
                kwargs=dict(
                    model_path=Path(data.get("model_path", "")),
                    config_path=Path(data.get("config_path", "")),
                    speaker=data.get("speaker", ""),
                    cluster_model_path=cluster_model_path,
                    transpose=data.get("transpose", 0),
                    auto_predict_f0=data.get("auto_predict_f0", False),
                    cluster_infer_ratio=data.get("cluster_infer_ratio", 0.0),
                    noise_scale=data.get("noise_scale", 0.4),
                    f0_method=data.get("f0_method", "dio"),
                    db_thresh=data.get("db_thresh", -35),
                    pad_seconds=data.get("pad_seconds", 0.1),
                    chunk_seconds=data.get("chunk_seconds", 0.5),
                    crossfade_seconds=data.get("crossfade_seconds", 0.05),
                    additional_infer_before_seconds=data.get("additional_infer_before_seconds", 0.15),
                    additional_infer_after_seconds=data.get("additional_infer_after_seconds", 0.1),
                    block_seconds=data.get("block_seconds", 0.35),
                    version=data.get("version", 1),
                    input_device=input_device_indices[input_device_idx],
                    output_device=output_device_indices[output_device_idx],
                    device=get_optimal_device() if data.get("use_gpu", True) else "cpu",
                    passthrough_original=data.get("passthrough_original", False),
                ),
            )

            return JSONResponse(content={"status": "started"})
        except Exception as e:
            LOG.exception(e)
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/realtime/stop")
    async def stop_realtime():
        """Stop real-time voice conversion."""
        try:
            if app.state.realtime_future:
                app.state.realtime_future.cancel()
                app.state.realtime_future = None
            return JSONResponse(content={"status": "stopped"})
        except Exception as e:
            LOG.exception(e)
            raise HTTPException(status_code=500, detail=str(e))

    return app
