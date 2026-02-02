# Dependency Reduction Summary

As part of replacing PySimpleGUI with a modern web-based UI, we also removed several large system dependencies that were only used for icon generation.

## Dependencies Removed

### System Dependencies
1. **ImageMagick** (~100MB)
   - Previously used to generate placeholder icon at build time
   - Required Ghostscript as a delegate
   
2. **Ghostscript** (~100MB)
   - Required by ImageMagick for gradient generation
   - Large PostScript/PDF rendering engine

3. **Tesseract** (was never actually used)
   - Not found in the codebase

### Python Dependencies
1. **pysimplegui-4-foss** (~500KB + framework overhead)
   - Old GUI framework
   - Replaced with pywebview + React

## Dependencies Added

### Python Dependencies
1. **pywebview** (~50KB)
   - Lightweight wrapper for native window
   - Much smaller than PySimpleGUI

2. **uvicorn** (already a dependency via FastAPI)
   - ASGI server for FastAPI
   - No additional size impact

## Icon Generation Solution

### Before
```bash
# Required ImageMagick + Ghostscript
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
    icon.png
```

### After
- Pre-built `icon.png` (5KB) included in repository
- Generated once using Python standard library
- No runtime dependencies needed
- Icon uses matching purple gradient from web UI

## Build Time Impact

### GitHub Actions
```yaml
# BEFORE
- name: Install system dependencies for icon generation
  run: |
    brew install imagemagick  # ~2 minutes
    brew install ghostscript  # ~1 minute

# AFTER  
# (removed - not needed)
```

**Build time savings: ~3 minutes per build**

### Local Builds
```bash
# BEFORE
if ! command -v convert &> /dev/null; then
    echo "WARNING: ImageMagick not found"
    echo "Install with: brew install imagemagick"
fi

# AFTER
# (removed - not needed)
```

**No manual dependency installation required**

## Storage Impact

| Dependency | Size | Status |
|------------|------|--------|
| ImageMagick | ~100MB | ❌ Removed |
| Ghostscript | ~100MB | ❌ Removed |
| PySimpleGUI | ~500KB | ❌ Removed |
| pywebview | ~50KB | ✅ Added |
| Pre-built icon | 5KB | ✅ Added |
| **Net Change** | **~200MB saved** | ✅ |

## Verification

To verify the icon works without ImageMagick:

```bash
# Generate .icns from icon.png (uses only macOS built-in tools)
./build/macos/generate_icon.sh

# This will succeed as long as:
# 1. icon.png exists (checked into repository)
# 2. sips is available (built into macOS)
# 3. iconutil is available (built into macOS)
```

## Benefits

1. **Faster CI/CD**: No need to install ImageMagick/Ghostscript
2. **Smaller downloads**: ~200MB less for users who build from source
3. **Fewer failure points**: Less dependencies = fewer things that can break
4. **Consistent icons**: Pre-built icon ensures everyone gets the same result
5. **Matching design**: Icon now matches the new web UI's purple gradient

## Migration Notes

For maintainers who want to update the icon:

1. Edit `build/macos/icon.png` directly
2. Can use any image editor (Preview.app, GIMP, Photoshop, etc.)
3. Should be 1024x1024 PNG format
4. Commit the updated icon.png to the repository
5. No need to install ImageMagick

## Related Changes

- PR: Implement Web-based UI
- Commit: "refactor: remove imagemagick and ghostscript dependencies"
- Files modified:
  - `.github/workflows/build-macos-release.yml`
  - `local_build.sh`
  - `build/macos/generate_icon.sh`
  - `.gitignore`
- Files added:
  - `build/macos/icon.png`
