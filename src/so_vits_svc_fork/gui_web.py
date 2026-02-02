from __future__ import annotations

import multiprocessing
import threading
from logging import getLogger

import uvicorn
import webview

from . import __version__
from .webui.server import create_app

LOG = getLogger(__name__)


def start_server(app, host: str = "127.0.0.1", port: int = 5173):
    """Start the FastAPI server in a separate thread."""
    uvicorn.run(app, host=host, port=port, log_level="info")


def main():
    """Main entry point for the web UI."""
    LOG.info(f"Starting So-VITS-SVC Fork Web UI v{__version__}")

    # Create FastAPI app
    app = create_app()

    # Start server in a separate thread
    host = "127.0.0.1"
    port = 5173

    server_thread = threading.Thread(
        target=start_server,
        args=(app, host, port),
        daemon=True,
    )
    server_thread.start()

    # Wait a bit for server to start
    import time

    time.sleep(1)

    # Create and start webview window
    window = webview.create_window(
        title=f"So-VITS-SVC Fork v{__version__}",
        url=f"http://{host}:{port}",
        width=1400,
        height=900,
        resizable=True,
        text_select=True,
    )

    webview.start()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
