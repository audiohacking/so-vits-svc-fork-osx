#!/bin/bash
# Code signing script for macOS application bundle
# This script signs the application with either a Developer ID or ad-hoc signing

set -e

APP_PATH="${1:-dist/SoVitsSVC-OSX.app}"
SIGNING_IDENTITY="${MACOS_SIGNING_IDENTITY:--}"

echo "🔐 Code signing macOS application..."
echo "  App Path: $APP_PATH"
echo "  Signing Identity: $SIGNING_IDENTITY"

if [ ! -d "$APP_PATH" ]; then
    echo "❌ Error: App bundle not found at $APP_PATH"
    exit 1
fi

# Sign all dylib and framework files first
echo "  Signing frameworks and libraries..."
find "$APP_PATH/Contents" -type f \( -name "*.dylib" -o -name "*.so" \) -exec codesign --force --sign "$SIGNING_IDENTITY" --timestamp --options runtime {} \; 2>/dev/null || true

# Sign all executables
echo "  Signing executables..."
find "$APP_PATH/Contents/MacOS" -type f -perm +111 -exec codesign --force --sign "$SIGNING_IDENTITY" --timestamp --options runtime {} \;

# Sign the main app bundle
echo "  Signing app bundle..."
codesign --force --sign "$SIGNING_IDENTITY" --timestamp --options runtime --deep --entitlements <(echo '<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
    <key>com.apple.security.device.audio-input</key>
    <true/>
    <key>com.apple.security.automation.apple-events</key>
    <true/>
</dict>
</plist>') "$APP_PATH"

# Verify the signature
echo "  Verifying signature..."
codesign --verify --deep --strict --verbose=2 "$APP_PATH"

if [ "$SIGNING_IDENTITY" = "-" ]; then
    echo "✅ Ad-hoc signing completed successfully"
    echo "   Note: This is for development only. Users will need to run:"
    echo "   sudo xattr -cr '$APP_PATH'"
else
    echo "✅ Code signing completed with identity: $SIGNING_IDENTITY"
fi

# Display signature information
echo "  Signature details:"
codesign -dvvv "$APP_PATH" 2>&1 | head -20
