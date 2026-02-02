from __future__ import annotations

import multiprocessing
import sys
import threading
import time
from logging import getLogger
from pathlib import Path

import requests
import uvicorn
import webview

# Handle both direct script execution and module execution
try:
    from . import __version__
    from .webui.server import create_app
except ImportError:
    # Running as a script directly - add parent directory to path
    src_path = Path(__file__).parent.parent
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    from so_vits_svc_fork import __version__
    from so_vits_svc_fork.webui.server import create_app

LOG = getLogger(__name__)


def start_server(app, host: str = "127.0.0.1", port: int = 5173):
    """Start the FastAPI server in a separate thread."""
    uvicorn.run(app, host=host, port=port, log_level="info")


def wait_for_server(url: str, timeout: int = 10) -> bool:
    """Wait for the server to become available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                LOG.info("Server is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.1)
    return False


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

    # Wait for server to be ready with health check
    url = f"http://{host}:{port}"
    if not wait_for_server(url):
        LOG.error("Server failed to start within timeout period")
        return

    # Create and start webview window
    window = webview.create_window(
        title=f"So-VITS-SVC Fork v{__version__}",
        url=url,
        width=1400,
        height=900,
        resizable=True,
        text_select=True,
    )

    webview.start()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
