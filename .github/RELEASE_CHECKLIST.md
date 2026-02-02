# Release Checklist for so-vits-svc-fork-osx

Use this checklist when preparing a new release of the macOS application.

## Pre-Release Testing

### Local Build Testing

- [ ] Clean previous builds: `rm -rf build dist`
- [ ] Generate icon: `./build/macos/generate_icon.sh`
- [ ] Build with PyInstaller: `python -m PyInstaller SoVitsSVC-OSX.spec --clean`
- [ ] Code sign: `./build/macos/codesign.sh dist/SoVitsSVC-OSX.app`
- [ ] Verify signature: `codesign -dvvv dist/SoVitsSVC-OSX.app`
- [ ] Test app launches: `open dist/SoVitsSVC-OSX.app`

### Functionality Testing

- [ ] Test MPS detection: `python build/macos/test_mps.py`
- [ ] Test file inference (load model, convert audio)
- [ ] Test real-time conversion (microphone input)
- [ ] Test preset saving and loading
- [ ] Test "Use GPU" checkbox functionality
- [ ] Check Console.app for errors

### Platform Testing

- [ ] Test on Apple Silicon Mac (M1/M2/M3)
- [ ] Test on Intel Mac (if available)
- [ ] Test on macOS 11 (Big Sur) or latest available
- [ ] Test on macOS 12+ (Monterey, Ventura, Sonoma)

### DMG Testing

- [ ] Create DMG: `hdiutil create...`
- [ ] Mount DMG and test drag-to-install
- [ ] Verify README.txt displays correctly
- [ ] Test app from Applications folder
- [ ] Test the .command launcher file

## Version Management

### Update Version Numbers

- [ ] Update version in `SoVitsSVC-OSX.spec`
  - `CFBundleVersion`
  - `CFBundleShortVersionString`
- [ ] Update version in `src/so_vits_svc_fork/__init__.py`
- [ ] Or use: `python build/macos/update_version.py X.Y.Z`

### Update Documentation

- [ ] Update `CHANGELOG_MACOS.md` with new changes
- [ ] Review and update `README.md` if needed
- [ ] Check all documentation is current
- [ ] Update screenshots if UI changed

## Code Quality

### Run Checks

- [ ] Code review passed (automatic)
- [ ] Security scan passed: CodeQL (automatic)
- [ ] No console errors or warnings
- [ ] All scripts are executable (`chmod +x`)
- [ ] .gitignore is up to date

### Clean Up

- [ ] Remove any debug print statements
- [ ] Remove temporary files
- [ ] Check for sensitive data
- [ ] Verify no large files in repo

## GitHub Release Preparation

### Repository

- [ ] All changes committed and pushed
- [ ] Branch is up to date with main
- [ ] No merge conflicts
- [ ] CI/CD workflow file is correct

### Release Notes

- [ ] Prepare release notes (use `CHANGELOG_MACOS.md`)
- [ ] List new features
- [ ] List bug fixes
- [ ] List known issues
- [ ] Include upgrade instructions
- [ ] Add system requirements
- [ ] Include checksums for verification

## Create Release

### GitHub Release

1. [ ] Go to GitHub repository → Releases
2. [ ] Click "Draft a new release"
3. [ ] Choose a tag: `vX.Y.Z` (e.g., `v1.0.0`)
4. [ ] Set release title: "so-vits-svc-fork-osx vX.Y.Z"
5. [ ] Add release notes (from preparation)
6. [ ] Set as latest release (if stable)
7. [ ] Or mark as pre-release (if beta)
8. [ ] Publish release

### Automated Build

- [ ] GitHub Actions workflow triggered
- [ ] Build completes successfully
- [ ] DMG artifact created
- [ ] ZIP artifact created
- [ ] Checksums generated
- [ ] Assets attached to release

### Manual Build (if automated fails)

```bash
# Build locally
./build/macos/generate_icon.sh
python -m PyInstaller SoVitsSVC-OSX.spec --clean --noconfirm
./build/macos/codesign.sh dist/SoVitsSVC-OSX.app

# Create DMG
mkdir -p dmg_temp
cp -R dist/SoVitsSVC-OSX.app dmg_temp/
cp SoVitsSVC-OSX.command dmg_temp/
ln -s /Applications dmg_temp/Applications
cp .github/DMG_README.txt dmg_temp/README.txt
hdiutil create -volname "so-vits-svc OSX" -srcfolder dmg_temp -ov -format UDZO SoVitsSVC-OSX-macOS.dmg

# Create ZIP
cd dist && zip -r ../SoVitsSVC-OSX-macOS.zip SoVitsSVC-OSX.app && cd ..

# Generate checksums
shasum -a 256 SoVitsSVC-OSX-macOS.dmg > checksums.txt
shasum -a 256 SoVitsSVC-OSX-macOS.zip >> checksums.txt

# Upload to release manually
```

## Post-Release Validation

### Download Testing

- [ ] Download DMG from release page
- [ ] Download ZIP from release page
- [ ] Verify checksums match
- [ ] Test DMG installation
- [ ] Test ZIP extraction and installation

### Fresh Installation Testing

- [ ] Install on fresh Mac (or clean /Applications)
- [ ] Launch and grant permissions
- [ ] Test basic functionality
- [ ] Verify MPS works on Apple Silicon
- [ ] Check for any security warnings

### Documentation

- [ ] Update README.md download links (if needed)
- [ ] Announce release (if applicable)
- [ ] Update any external documentation

## Communication

### Internal

- [ ] Notify team of release
- [ ] Update project status
- [ ] Document any issues found

### External (Optional)

- [ ] Post release announcement
- [ ] Update social media
- [ ] Notify community
- [ ] Update project website

## Monitoring

### Post-Release

- [ ] Monitor GitHub Issues for bug reports
- [ ] Check for crash reports
- [ ] Respond to user feedback
- [ ] Track download numbers
- [ ] Note any patterns in issues

### Follow-Up

- [ ] Plan next release if needed
- [ ] Address critical bugs immediately
- [ ] Schedule bug-fix release if necessary
- [ ] Update roadmap based on feedback

## Version Numbering Guide

### Semantic Versioning (X.Y.Z)

- **X (Major)**: Breaking changes, major new features
- **Y (Minor)**: New features, backward compatible
- **Z (Patch)**: Bug fixes, small improvements

### Examples

- `1.0.0`: Initial stable release
- `1.0.1`: Bug fix release
- `1.1.0`: New feature added
- `2.0.0`: Major update with breaking changes

### Pre-Release Tags

- `v1.0.0-alpha.1`: Early alpha
- `v1.0.0-beta.1`: Feature complete, testing
- `v1.0.0-rc.1`: Release candidate

## Troubleshooting

### Build Fails

- Check Python version (3.11)
- Verify all dependencies installed
- Check PyInstaller logs
- Try clean build: `rm -rf build dist`

### GitHub Actions Fails

- Check workflow logs
- Verify secrets are set (if needed)
- Check for API rate limits
- Try manual workflow dispatch

### Code Signing Issues

- Verify certificate is valid
- Check entitlements are correct
- Try ad-hoc signing for testing
- Check Keychain Access

### DMG Creation Fails

- Check disk space
- Verify all files exist
- Check folder structure
- Try different DMG format

## Emergency Rollback

If critical issue found after release:

1. [ ] Mark release as pre-release or draft
2. [ ] Add warning to release notes
3. [ ] Prepare hotfix in new branch
4. [ ] Fast-track testing
5. [ ] Release patch version (X.Y.Z+1)
6. [ ] Notify users of issue and fix

## Archive

After successful release:

- [ ] Archive old builds (if keeping)
- [ ] Clean up temporary files
- [ ] Update project board/tracker
- [ ] Document lessons learned
- [ ] Plan next release cycle

---

## Quick Release Command Summary

```bash
# Version update
python build/macos/update_version.py X.Y.Z

# Build
./build/macos/generate_icon.sh
python -m PyInstaller SoVitsSVC-OSX.spec --clean --noconfirm
./build/macos/codesign.sh dist/SoVitsSVC-OSX.app

# Test
open dist/SoVitsSVC-OSX.app
python build/macos/test_mps.py

# Create tag and push
git tag -a vX.Y.Z -m "Release version X.Y.Z"
git push origin vX.Y.Z

# Create GitHub release (automated build)
# or build manually and upload
```

---

**Note**: Adapt this checklist based on your specific needs and workflow.
