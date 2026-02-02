# macOS Build Testing Summary

## Overview
This document explains the testing infrastructure added to validate the macOS app build on real macOS systems using GitHub Actions.

## Problem Statement
The original issue was that the macOS app failed to launch with a traceback error. The root cause was a mismatch between:
- The executable name created by PyInstaller: `SoVitsSVC-OSX_bin`
- The executable referenced in Info.plist: `SoVitsSVC-OSX`

## Solution Implemented
Changed `SoVitsSVC-OSX.spec` line 130 to set `CFBundleExecutable` to `f'{app_name}_bin'` to match the actual executable name.

## Testing Infrastructure Added

### 1. GitHub Actions Workflow (test-macos-build.yml)
**Purpose**: Test the build process on real macOS hardware

**Trigger Conditions**:
- Pull requests that modify:
  - `SoVitsSVC-OSX.spec`
  - `src/so_vits_svc_fork/gui_web.py`
  - `.github/workflows/test-macos-build.yml`
  - `requirements_macos.txt`
- Manual workflow dispatch

**What it Tests**:
1. ✅ Builds the app using PyInstaller on macOS-latest
2. ✅ Verifies the executable `SoVitsSVC-OSX_bin` exists
3. ✅ Checks Info.plist `CFBundleExecutable` matches executable name
4. ✅ Validates app bundle structure
5. ✅ Performs adhoc code signing
6. ✅ Verifies executable permissions
7. ✅ Uploads test build as artifact (7-day retention)

**Key Validation Step**:
```bash
# Extract CFBundleExecutable from Info.plist
BUNDLE_EXEC=$(/usr/libexec/PlistBuddy -c "Print :CFBundleExecutable" \
  "dist/SoVitsSVC-OSX.app/Contents/Info.plist")

# Verify it matches the actual executable
if [ "$BUNDLE_EXEC" != "SoVitsSVC-OSX_bin" ]; then
  exit 1  # Mismatch detected
fi
```

### 2. Unit Tests (tests/test_pyinstaller_spec.py)
**Purpose**: Validate spec file configuration without building

**Tests**:
- `test_spec_file_exists`: Verify spec file exists
- `test_executable_name_configuration`: Verify EXE and CFBundleExecutable match
- `test_source_file_exists`: Verify gui_web.py exists
- `test_console_disabled`: Verify console=False for GUI app
- `test_bundle_identifier`: Verify bundle ID is correct

**Run Locally**:
```bash
python3 -m unittest tests.test_pyinstaller_spec -v
```

### 3. Build Simulation (tests/test_build_simulation.py)
**Purpose**: Document and demonstrate the fix

**What it Does**:
- Reads the spec file configuration
- Simulates PyInstaller build process
- Shows what happens when user launches the app
- Validates configuration matches

**Run Locally**:
```bash
python3 tests/test_build_simulation.py
```

## Changes to Build Scripts

### build-macos-release.yml
**Removed**: Obsolete workaround that copied `SoVitsSVC-OSX_bin` to `SoVitsSVC-OSX`

**Added**: Proper verification of executable existence and permissions

### local_build.sh
**Removed**: Same obsolete workaround as above

**Added**: Error checking if executable doesn't exist

## Why macOS Testing is Important

1. **Platform-Specific Issues**: macOS has unique requirements for app bundles
2. **Info.plist Validation**: Info.plist must correctly reference the executable
3. **Code Signing**: macOS requires valid code signatures (adhoc for testing)
4. **App Bundle Structure**: macOS expects specific directory structure
5. **Executable Permissions**: Unix-style permissions must be set correctly

## How to Test This PR

### Automatic Testing (Recommended)
1. The PR will automatically trigger the macOS build test workflow
2. Check the "Actions" tab for results
3. Download the test build artifact if needed

### Manual Testing on macOS
1. Checkout this branch
2. Run: `./local_build.sh`
3. Test: `open dist/SoVitsSVC-OSX.app`

### Validation Points
- [ ] Build completes without errors
- [ ] Executable `SoVitsSVC-OSX_bin` exists in `Contents/MacOS/`
- [ ] Info.plist has `CFBundleExecutable` = `SoVitsSVC-OSX_bin`
- [ ] App launches successfully (no traceback error)
- [ ] All unit tests pass

## Expected Results

### Before Fix
```
User launches app → macOS reads Info.plist → Looks for 'SoVitsSVC-OSX'
→ File not found (actual file is 'SoVitsSVC-OSX_bin') → ✗ Traceback error
```

### After Fix
```
User launches app → macOS reads Info.plist → Looks for 'SoVitsSVC-OSX_bin'
→ File found → ✓ App launches successfully
```

## Continuous Integration

The workflow integrates seamlessly with the existing CI/CD pipeline:
- Runs on pull requests (no merge required)
- Fails fast if configuration is broken
- Provides test artifacts for manual verification
- Does not block unrelated changes

## Future Improvements

1. Add actual app launch test (currently smoke test only)
2. Test with real code signing certificate in release workflow
3. Add DMG validation tests
4. Test app permissions and entitlements
5. Add automated UI testing with AppleScript or similar

## References

- PyInstaller macOS documentation
- Apple's App Bundle documentation
- Info.plist keys reference
- GitHub Actions macOS runner documentation
