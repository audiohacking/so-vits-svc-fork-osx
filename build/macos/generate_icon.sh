#!/bin/bash
# Generate application icon for macOS from SVG or PNG source
# Creates .icns file with multiple resolutions

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ICON_SOURCE="${SCRIPT_DIR}/icon.png"
ICON_OUTPUT="${SCRIPT_DIR}/SoVitsSVC-OSX.icns"

echo "🎨 Generating macOS application icon..."

# Create a temporary directory for icon generation
ICONSET_DIR=$(mktemp -d)/SoVitsSVC-OSX.iconset
mkdir -p "$ICONSET_DIR"

# Check if we have a source icon, if not create a simple placeholder
if [ ! -f "$ICON_SOURCE" ]; then
    echo "  Creating placeholder icon..."
    # Create a simple gradient icon using ImageMagick
    convert -size 1024x1024 \
        -define gradient:angle=135 \
        gradient:'#4A90E2-#50C878' \
        -gravity center \
        -pointsize 240 \
        -font Helvetica-Bold \
        -fill white \
        -annotate +0+0 'SVC' \
        -pointsize 80 \
        -annotate +0+200 'OSX' \
        "$ICON_SOURCE"
fi

echo "  Generating icon set at multiple resolutions..."

# Generate all required icon sizes for macOS
sips -z 16 16     "$ICON_SOURCE" --out "$ICONSET_DIR/icon_16x16.png" >/dev/null
sips -z 32 32     "$ICON_SOURCE" --out "$ICONSET_DIR/icon_16x16@2x.png" >/dev/null
sips -z 32 32     "$ICON_SOURCE" --out "$ICONSET_DIR/icon_32x32.png" >/dev/null
sips -z 64 64     "$ICON_SOURCE" --out "$ICONSET_DIR/icon_32x32@2x.png" >/dev/null
sips -z 128 128   "$ICON_SOURCE" --out "$ICONSET_DIR/icon_128x128.png" >/dev/null
sips -z 256 256   "$ICON_SOURCE" --out "$ICONSET_DIR/icon_128x128@2x.png" >/dev/null
sips -z 256 256   "$ICON_SOURCE" --out "$ICONSET_DIR/icon_256x256.png" >/dev/null
sips -z 512 512   "$ICON_SOURCE" --out "$ICONSET_DIR/icon_256x256@2x.png" >/dev/null
sips -z 512 512   "$ICON_SOURCE" --out "$ICONSET_DIR/icon_512x512.png" >/dev/null
sips -z 1024 1024 "$ICON_SOURCE" --out "$ICONSET_DIR/icon_512x512@2x.png" >/dev/null

# Create the .icns file
echo "  Creating .icns file..."
iconutil -c icns "$ICONSET_DIR" -o "$ICON_OUTPUT"

# Clean up
rm -rf "$(dirname "$ICONSET_DIR")"

echo "✅ Icon generated successfully: $ICON_OUTPUT"
ls -lh "$ICON_OUTPUT"
