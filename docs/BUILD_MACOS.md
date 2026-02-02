# Building for macOS

This guide explains how to build the so-vits-svc-fork OSX application locally or via GitHub Actions.

## Prerequisites

### System Requirements

- macOS 11.0 (Big Sur) or later
- Python 3.11
- Xcode Command Line Tools
- Homebrew (for dependencies)

### Install Dependencies

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install system dependencies
brew install imagemagick

# Install Python dependencies (includes PyObjC for pywebview on macOS)
pip install -r requirements_macos.txt

# Install the package in development mode
pip install -e .
```

**Important for macOS**: The `requirements_macos.txt` file includes PyObjC dependencies (`pyobjc-core`, `pyobjc-framework-Cocoa`, `pyobjc-framework-WebKit`) which are required for pywebview to work with the native macOS Cocoa framework. These dependencies are automatically installed when you use `requirements_macos.txt`.

## Local Build Process

### Quick Build (Recommended)

For the fastest local build experience, use the automated build script:

```bash
./local_build.sh
```

This script mirrors the GitHub Actions workflow and handles all build steps automatically, including:

- Checking Python version
- Installing dependencies
- Generating icons
- Building with PyInstaller
- Code signing
- Providing test instructions

### Manual Build Process

If you prefer to run each step manually:

#### 1. Generate Application Icon

```bash
chmod +x build/macos/generate_icon.sh
./build/macos/generate_icon.sh
```

This creates `build/macos/SoVitsSVC-OSX.icns` from a source icon or generates a placeholder.

#### 2. Build with PyInstaller

```bash
python -m PyInstaller SoVitsSVC-OSX.spec --clean --noconfirm
```

This creates the application bundle at `dist/SoVitsSVC-OSX.app`.

#### 3. Set Up Executable

```bash
# Copy the binary to the expected location
cp dist/SoVitsSVC-OSX.app/Contents/MacOS/SoVitsSVC-OSX_bin \
   dist/SoVitsSVC-OSX.app/Contents/MacOS/SoVitsSVC-OSX
chmod +x dist/SoVitsSVC-OSX.app/Contents/MacOS/SoVitsSVC-OSX
```

#### 4. Code Sign (Optional but Recommended)

```bash
chmod +x build/macos/codesign.sh
./build/macos/codesign.sh dist/SoVitsSVC-OSX.app
```

For development builds, this uses ad-hoc signing. For distribution, set the `MACOS_SIGNING_IDENTITY` environment variable:

```bash
export MACOS_SIGNING_IDENTITY="Developer ID Application: Your Name (TEAM_ID)"
./build/macos/codesign.sh dist/SoVitsSVC-OSX.app
```

#### 5. Create DMG (Optional)

```bash
# Create temporary directory
mkdir -p dmg_temp
cp -R dist/SoVitsSVC-OSX.app dmg_temp/
cp SoVitsSVC-OSX.command dmg_temp/
chmod +x dmg_temp/SoVitsSVC-OSX.command
ln -s /Applications dmg_temp/Applications
cp .github/DMG_README.txt dmg_temp/README.txt

# Create DMG
hdiutil create -volname "so-vits-svc OSX" \
  -srcfolder dmg_temp \
  -ov -format UDZO \
  SoVitsSVC-OSX-macOS.dmg
```

## GitHub Actions Build

The repository includes a GitHub Actions workflow that automatically builds and releases the macOS application.

### Triggering a Build

#### Option 1: Create a Release

1. Go to the repository on GitHub
2. Click "Releases" → "Create a new release"
3. Tag version (e.g., `v1.0.0`)
4. Publish release
5. The workflow automatically builds and attaches the DMG and ZIP files

#### Option 2: Manual Workflow Dispatch

1. Go to Actions → "Build macOS Release"
2. Click "Run workflow"
3. Enter a version tag (e.g., `v1.0.0-beta`)
4. Run the workflow
5. Download artifacts from the completed workflow run

### Secrets Configuration

For production releases with proper code signing, add the following secret to your repository:

- `MACOS_SIGNING_IDENTITY`: Your Developer ID Application certificate name
  - Example: `"Developer ID Application: Your Name (TEAM_ID)"`
  - Get this from Keychain Access or `security find-identity -v -p codesigning`

Without this secret, the build uses ad-hoc signing (suitable for development).

## Testing the Build

### Test Locally

```bash
# Launch the app
open dist/SoVitsSVC-OSX.app

# Or use the launcher script
./SoVitsSVC-OSX.command
```

### Test MPS GPU Acceleration

```python
import torch
print(f"MPS Available: {torch.backends.mps.is_available()}")
print(f"Optimal Device: {torch.device('mps' if torch.backends.mps.is_available() else 'cpu')}")
```

In the GUI, ensure "Use GPU" checkbox is enabled (it should be by default on Apple Silicon Macs).

## Troubleshooting

### "App is damaged and can't be opened"

This happens with ad-hoc signed apps. Run:

```bash
sudo xattr -cr dist/SoVitsSVC-OSX.app
```

### PyInstaller Build Fails

- Ensure all dependencies are installed: `pip install -r requirements_macos.txt`
- Check Python version: `python --version` (should be 3.11)
- Clean previous builds: `rm -rf build dist`

### Icon Generation Fails

If `generate_icon.sh` fails:

- Ensure ImageMagick is installed: `brew install imagemagick`
- Check for `build/macos/icon.png` or the script will create a placeholder

### Code Signing Issues

For development:

- Use ad-hoc signing: `MACOS_SIGNING_IDENTITY="-" ./build/macos/codesign.sh dist/SoVitsSVC-OSX.app`

For distribution:

- Ensure you have a valid Developer ID certificate
- Check certificate: `security find-identity -v -p codesigning`

### App Won't Launch

- Check Console.app for error messages
- Verify the executable is properly set: `ls -l dist/SoVitsSVC-OSX.app/Contents/MacOS/`
- Test from terminal: `dist/SoVitsSVC-OSX.app/Contents/MacOS/SoVitsSVC-OSX`

### Import Error at Startup (Line 12 or 19 in gui_web.py)

If you see an error like `ModuleNotFoundError: No module named 'webview'` or similar at line 12/19:

- This typically means PyObjC dependencies are missing
- Solution: Reinstall from requirements: `pip install -r requirements_macos.txt`
- Or install PyObjC manually: `pip install "pyobjc-core>=10.0" "pyobjc-framework-Cocoa>=10.0" "pyobjc-framework-WebKit>=10.0"`
- When building with PyInstaller, ensure hidden imports in `SoVitsSVC-OSX.spec` include the PyObjC modules

The pywebview library requires PyObjC on macOS to access the native Cocoa framework for window creation.

## Advanced Configuration

### Universal Binary (Intel + Apple Silicon)

The default build creates a Universal 2 binary. To target only Apple Silicon:

Edit `SoVitsSVC-OSX.spec`:

```python
target_arch='arm64',  # Apple Silicon only
```

Or for Intel only:

```python
target_arch='x86_64',  # Intel only
```

### Custom Icon

Replace `build/macos/icon.png` with your custom 1024x1024 PNG icon before running `generate_icon.sh`.

### PyInstaller Customization

Edit `SoVitsSVC-OSX.spec` to:

- Add more hidden imports
- Include additional data files
- Customize app metadata
- Adjust optimization settings

## CI/CD Integration

The workflow is configured to:

1. Build on every release
2. Create DMG and ZIP distributions
3. Generate SHA-256 checksums
4. Upload artifacts
5. Attach to releases automatically

Modify `.github/workflows/build-macos-release.yml` to customize the CI/CD pipeline.

## Distribution Checklist

Before distributing the app:

- [ ] Test on both Intel and Apple Silicon Macs
- [ ] Verify MPS GPU acceleration works
- [ ] Test all GUI features (file inference, real-time)
- [ ] Check microphone permissions prompt
- [ ] Verify app signature: `codesign -dvvv dist/SoVitsSVC-OSX.app`
- [ ] Test DMG installation flow
- [ ] Update version in `SoVitsSVC-OSX.spec`
- [ ] Update CHANGELOG
- [ ] Create release notes

## Support

For build issues or questions:

- Open an issue on GitHub
- Check existing issues for solutions
- Review PyInstaller documentation for advanced topics

---

**Note**: This build process creates a fully native macOS application optimized for Apple Silicon with Metal Performance Shaders (MPS) GPU acceleration.
