#!/bin/bash
# Launcher script for so-vits-svc OSX application
# This provides a convenient way to launch the app from Finder

cd "$(dirname "$0")"

if [ -d "dist/SoVitsSVC-OSX.app" ]; then
    open dist/SoVitsSVC-OSX.app
elif [ -d "SoVitsSVC-OSX.app" ]; then
    open SoVitsSVC-OSX.app
else
    echo "Error: Application bundle not found!"
    echo "Please build the application first using:"
    echo "  python -m PyInstaller SoVitsSVC-OSX.spec"
    read -p "Press Enter to close..."
fi
