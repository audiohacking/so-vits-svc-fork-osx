#!/bin/bash
# ---------------------------------------------------------------------------
#  so-vits-svc-fork-osx - Local Build Script
#  Replicates the GitHub Actions build process for local testing
# ---------------------------------------------------------------------------

set -e  # Exit on error

echo "=========================================="
echo "so-vits-svc-fork-osx - Local Build"
echo "=========================================="
echo ""

# This script mirrors .github/workflows/build-macos-release.yml
# for local testing without needing to push to GitHub

cd "$(dirname "$0")"

# Check Python 3.11 (same as GitHub Actions)
if ! command -v python3.11 &> /dev/null && ! python3 --version 2>&1 | grep -q "3.11"; then
    echo "ERROR: Python 3.11 not found"
    echo "GitHub Actions uses Python 3.11. Please install it for consistent builds."
    exit 1
fi

PYTHON="python3"
if command -v python3.11 &> /dev/null; then
    PYTHON="python3.11"
fi

echo "Using Python: $($PYTHON --version)"
echo ""

# Install system dependencies for icon generation
echo "Checking system dependencies..."
if ! command -v convert &> /dev/null; then
    echo "WARNING: ImageMagick not found"
    echo "Install with: brew install imagemagick"
    echo ""
fi

# Install Python dependencies
echo "Installing Python dependencies..."
$PYTHON -m pip install --upgrade pip
pip install -r requirements_macos.txt
# Install the package itself
pip install -e .

echo ""

# Generate app icon
echo "Generating app icon..."
chmod +x build/macos/generate_icon.sh
./build/macos/generate_icon.sh

echo ""

# Check build/macos assets (same checks as GitHub Actions)
echo "Checking build assets..."
if [ ! -f "build/macos/SoVitsSVC-OSX.icns" ]; then
    echo "ERROR: build/macos/SoVitsSVC-OSX.icns not found after generation."
    exit 1
fi
if [ ! -f "build/macos/codesign.sh" ]; then
    echo "ERROR: build/macos/codesign.sh not found."
    exit 1
fi
if [ ! -f ".github/DMG_README.txt" ]; then
    echo "ERROR: .github/DMG_README.txt not found."
    exit 1
fi

echo "✓ All build assets present"
echo ""

# Clean previous PyInstaller outputs
echo "Cleaning previous builds..."
rm -rf dist/SoVitsSVC-OSX.app build/SoVitsSVC-OSX

# Build with PyInstaller
echo "Building with PyInstaller..."
$PYTHON -m PyInstaller SoVitsSVC-OSX.spec --clean --noconfirm

echo ""

# Set up app bundle executable
echo "Setting up app bundle executable..."
if [ -f "dist/SoVitsSVC-OSX.app/Contents/MacOS/SoVitsSVC-OSX_bin" ]; then
    cp dist/SoVitsSVC-OSX.app/Contents/MacOS/SoVitsSVC-OSX_bin dist/SoVitsSVC-OSX.app/Contents/MacOS/SoVitsSVC-OSX
    chmod +x dist/SoVitsSVC-OSX.app/Contents/MacOS/SoVitsSVC-OSX
fi

# Code sign the app bundle
echo ""
echo "Code signing app bundle..."
chmod +x build/macos/codesign.sh
MACOS_SIGNING_IDENTITY="-" ./build/macos/codesign.sh dist/SoVitsSVC-OSX.app

echo ""
echo "=========================================="
echo "✓ Build Complete!"
echo "=========================================="
echo ""
echo "App: dist/SoVitsSVC-OSX.app"
echo ""
echo "To test:"
echo "  open dist/SoVitsSVC-OSX.app"
echo ""
echo "To test MPS GPU acceleration:"
echo "  python build/macos/test_mps.py"
echo ""
echo "If blocked by Gatekeeper:"
echo "  xattr -cr dist/SoVitsSVC-OSX.app"
echo "  (then right-click → Open)"
echo ""
echo "To create DMG (optional):"
echo "  mkdir -p dmg_temp"
echo "  cp -R dist/SoVitsSVC-OSX.app dmg_temp/"
echo "  ln -s /Applications dmg_temp/Applications"
echo "  cp .github/DMG_README.txt dmg_temp/README.txt"
echo "  hdiutil create -volname 'so-vits-svc OSX' -srcfolder dmg_temp -ov -format UDZO SoVitsSVC-OSX-macOS.dmg"
echo ""
