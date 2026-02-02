# Web UI Implementation

This document describes the new web-based UI that replaces the PySimpleGUI interface.

## Overview

The new UI is a modern, browser-based interface served through pywebview, providing a native-like experience while using web technologies.

## Architecture

### Frontend (React + HTML)
- **File**: `src/so_vits_svc_fork/webui/index.html`
- **Technology**: Single-page React application (via CDN - no build step required)
- **Styling**: Custom CSS with macOS-inspired design
- **Features**:
  - Gradient purple theme matching modern macOS applications
  - All original PySimpleGUI features preserved:
    - Path configuration (model, config, cluster model)
    - Common inference settings (speaker, thresholds, F0 prediction, etc.)
    - File inference settings
    - Real-time voice changer settings
    - Preset management (load, save, delete)
    - GPU toggle

### Backend (FastAPI)
- **File**: `src/so_vits_svc_fork/webui/server.py`
- **Technology**: FastAPI REST API
- **Endpoints**:
  - `GET /` - Serve the main HTML page
  - `GET /api/presets` - Get all presets
  - `POST /api/presets` - Add a new preset
  - `DELETE /api/presets/{name}` - Delete a preset
  - `GET /api/devices` - Get audio input/output devices
  - `GET /api/default-paths` - Get default model/config paths
  - `GET /api/speakers` - Get available speakers from config
  - `POST /api/infer` - Run file inference
  - `POST /api/realtime/start` - Start real-time voice conversion
  - `POST /api/realtime/stop` - Stop real-time voice conversion

### Native Window (pywebview)
- **File**: `src/so_vits_svc_fork/gui_web.py`
- **Technology**: pywebview creates a native window with embedded browser
- **Configuration**:
  - Window size: 1400x900
  - Resizable: Yes
  - Runs FastAPI server in background thread
  - Opens at `http://127.0.0.1:5173`

## Key Features

### 1. No Build Step Required
- React is loaded via CDN (unpkg.com)
- Babel transpiles JSX in the browser
- Single HTML file contains all frontend code
- Makes deployment and maintenance simpler

### 2. 100% Feature Parity
All features from the original PySimpleGUI interface are preserved:
- Model and configuration path selection
- All inference parameters and sliders
- File and real-time inference modes
- Audio device selection
- Preset management
- Auto-play functionality

### 3. Modern UI/UX
- Responsive design
- Smooth animations and transitions
- macOS-inspired visual style
- Better visual hierarchy with sections
- Status messages for user feedback
- Tooltips and help text

### 4. Reduced Dependencies
**Removed:**
- pysimplegui-4-foss

**Added:**
- pywebview (native window)
- uvicorn (ASGI server)

Net result: Fewer dependencies, smaller package size

## Build Configuration

### PyInstaller (macOS App)
Updated `SoVitsSVC-OSX.spec`:
- Entry point changed to `gui_web.py`
- Includes `webui/` directory in data files
- Added pywebview and uvicorn to hidden imports
- Removed PySimpleGUI references

### GitHub Actions
No changes needed - workflow uses `requirements_macos.txt` which has been updated.

### Local Build
No changes needed - `local_build.sh` uses `requirements_macos.txt`.

## Usage

### Running the Web UI

From command line:
```bash
svc gui
```

Or:
```bash
svcg
```

Or directly:
```bash
python -m so_vits_svc_fork.gui_web
```

### Development

To modify the UI:
1. Edit `src/so_vits_svc_fork/webui/index.html`
2. Changes take effect immediately (no build step)
3. Refresh the window to see updates

To modify the backend:
1. Edit `src/so_vits_svc_fork/webui/server.py`
2. Restart the application

## Testing

Run the existing test suite:
```bash
pytest tests/test_main.py
```

All tests pass with the new web UI.

## Migration Notes

### For Users
- The UI looks different but all features work the same way
- Presets are preserved (uses same `default_gui_presets.json`)
- User presets in `user_gui_presets.json` are still supported

### For Developers
- Old `gui.py` has been removed
- Entry points now point to `gui_web.py`
- FastAPI provides better API structure for future enhancements
- Easier to add new features (e.g., WebSocket for real-time status updates)

## Future Enhancements (Optional)

Potential improvements that could be made:
1. WebSocket support for real-time progress updates
2. File drag-and-drop support
3. Audio waveform visualization
4. Built-in audio player with waveform
5. Dark/light theme toggle
6. Mobile-responsive design
7. Multi-language support

## Screenshots

The UI features:
- Purple gradient header
- Two-column layout
- Clean, modern card-based sections
- Smooth sliders with value displays
- Status messages with color coding
- macOS-style buttons and inputs
