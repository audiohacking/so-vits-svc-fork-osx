# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for so-vits-svc-fork macOS Application
This creates a native macOS app bundle with MPS GPU support
"""

import sys
from pathlib import Path

# Get the project root directory
project_root = Path(os.getcwd())

# Define the application name
app_name = 'SoVitsSVC-OSX'

# Analysis configuration
a = Analysis(
    ['src/so_vits_svc_fork/gui_web.py'],
    pathex=[str(project_root / 'src')],
    binaries=[],
    datas=[
        # Include the default GUI presets
        ('src/so_vits_svc_fork/default_gui_presets.json', 'so_vits_svc_fork'),
        # Include config templates
        ('src/so_vits_svc_fork/preprocessing/config_templates', 'so_vits_svc_fork/preprocessing/config_templates'),
        # Include the web UI files
        ('src/so_vits_svc_fork/webui', 'so_vits_svc_fork/webui'),
    ],
    hiddenimports=[
        'so_vits_svc_fork',
        'so_vits_svc_fork.gui_web',
        'so_vits_svc_fork.webui',
        'so_vits_svc_fork.webui.server',
        'so_vits_svc_fork.__main__',
        'so_vits_svc_fork.inference.main',
        'so_vits_svc_fork.inference.core',
        'so_vits_svc_fork.train',
        'so_vits_svc_fork.utils',
        'so_vits_svc_fork.preprocessing',
        'so_vits_svc_fork.cluster',
        'so_vits_svc_fork.modules',
        'torch',
        'torchaudio',
        'torchcrepe',
        'transformers',
        'librosa',
        'sounddevice',
        'soundfile',
        'numpy',
        'scipy',
        'matplotlib',
        'tensorboard',
        'tensorboardx',
        'lightning',
        'pywebview',
        'uvicorn',
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'click',
        'fastapi',
        'parselmouth',
        'pyworld',
        'pebble',
        'psutil',
        'cm_time',
        'rich',
        'tqdm',
        'requests',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib.tests',
        'numpy.random._examples',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=f'{app_name}_bin',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='arm64',  # Target macOS Arm64 (Apple Silicon)
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=app_name,
)

app = BUNDLE(
    coll,
    name=f'{app_name}.app',
    icon='build/macos/SoVitsSVC-OSX.icns',
    bundle_identifier='com.audiohacking.sovitssvc-osx',
    info_plist={
        'CFBundleName': app_name,
        'CFBundleDisplayName': 'so-vits-svc OSX',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleExecutable': app_name,
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
        'LSMinimumSystemVersion': '11.0',
        'NSMicrophoneUsageDescription': 'This app requires microphone access for real-time voice conversion.',
        'NSAppleEventsUsageDescription': 'This app requires Apple Events for automation.',
        'LSApplicationCategoryType': 'public.app-category.music',
        # MPS/Metal GPU support
        'NSSupportsAutomaticGraphicsSwitching': True,
        'GPUEject': False,
    },
)
