# Contributing to so-vits-svc-fork-osx

Thank you for your interest in contributing to the macOS port of so-vits-svc-fork! This guide will help you get started.

## Development Setup

### Prerequisites
- macOS 11.0 or later
- Python 3.11
- Git
- Xcode Command Line Tools
- Homebrew

### Clone and Setup

```bash
# Clone the repository
git clone https://github.com/audiohacking/so-vits-svc-fork-osx.git
cd so-vits-svc-fork-osx

# Install dependencies
pip install -r requirements_macos.txt

# Install in development mode
pip install -e .

# Test the installation
python build/macos/test_mps.py
```

## Making Changes

### Code Style
- Follow PEP 8 guidelines
- Use type hints where applicable
- Keep code compatible with Python 3.11+
- Test on both Intel and Apple Silicon if possible

### Testing Changes

#### Test GUI Changes
```bash
# Run the GUI
python -m so_vits_svc_fork.gui
# or
svcg
```

#### Test CLI Changes
```bash
# Test CLI commands
svc --help
svc pre-resample --help
```

#### Test MPS Functionality
```bash
python build/macos/test_mps.py
```

### Building the App

#### Local Build
```bash
# Generate icon (if needed)
./build/macos/generate_icon.sh

# Build with PyInstaller
python -m PyInstaller SoVitsSVC-OSX.spec --clean --noconfirm

# Sign the app (development)
./build/macos/codesign.sh dist/SoVitsSVC-OSX.app

# Test the app
open dist/SoVitsSVC-OSX.app
```

#### Full Build with DMG
```bash
# Build app
python -m PyInstaller SoVitsSVC-OSX.spec --clean --noconfirm
./build/macos/codesign.sh dist/SoVitsSVC-OSX.app

# Create DMG
mkdir -p dmg_temp
cp -R dist/SoVitsSVC-OSX.app dmg_temp/
ln -s /Applications dmg_temp/Applications
cp .github/DMG_README.txt dmg_temp/README.txt
hdiutil create -volname "so-vits-svc OSX" -srcfolder dmg_temp -ov -format UDZO SoVitsSVC-OSX-macOS.dmg
```

## Contribution Areas

### High Priority
- [ ] Performance optimizations for MPS
- [ ] UI/UX improvements
- [ ] Bug fixes
- [ ] Documentation improvements
- [ ] Testing on different macOS versions

### Nice to Have
- [ ] SwiftUI native interface
- [ ] Additional audio effects
- [ ] Model management features
- [ ] Preset sharing
- [ ] Advanced MPS optimizations

### Code Areas

#### PyInstaller Spec (`SoVitsSVC-OSX.spec`)
- App bundle configuration
- Hidden imports
- Data files inclusion
- Metadata updates

#### Build Scripts (`build/macos/`)
- Icon generation
- Code signing
- Version management
- Testing utilities

#### Workflow (`.github/workflows/build-macos-release.yml`)
- Build automation
- Release creation
- Asset uploading

#### Documentation (`docs/`)
- Build guides
- User guides
- Troubleshooting

## Pull Request Process

### Before Submitting
1. **Test your changes thoroughly**
   - Test on Apple Silicon if possible
   - Test on Intel Mac if possible
   - Verify GUI still works
   - Check for errors in Console.app

2. **Update documentation**
   - Update relevant .md files
   - Add comments to complex code
   - Update CHANGELOG_MACOS.md

3. **Check code quality**
   - Run linter (if configured)
   - Verify no unnecessary files included
   - Check .gitignore is correct

### Submitting PR
1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Commit with clear messages
   ```bash
   git commit -m "feat: add new feature"
   git commit -m "fix: resolve issue #123"
   git commit -m "docs: update build guide"
   ```
5. Push to your fork
6. Create Pull Request on GitHub

### PR Description
Include:
- **What**: What does this PR do?
- **Why**: Why is this change needed?
- **How**: How does it work?
- **Testing**: How did you test this?
- **Screenshots**: If UI changes, include screenshots

Example:
```markdown
## Description
Adds support for custom icon in PyInstaller build

## Changes
- Updated icon generation script to accept custom source
- Modified .spec file to use custom icon path
- Added documentation for custom icons

## Testing
- Tested on macOS 14.2 (M2 Mac)
- Built app with custom icon
- Verified icon displays correctly in Finder
- Tested both DMG and direct app launch

## Screenshots
[Include before/after screenshots]
```

## Reporting Bugs

Use the issue template at `.github/ISSUE_TEMPLATE/bug_report_macos.md`

Include:
- macOS version
- Mac model (Intel/Apple Silicon)
- App version
- Steps to reproduce
- Expected vs actual behavior
- Error messages
- Screenshots if relevant

## Requesting Features

Use the issue template at `.github/ISSUE_TEMPLATE/feature_request_macos.md`

Include:
- Clear description
- Problem it solves
- Proposed solution
- Benefits
- Examples if available

## Code Review Process

### What We Look For
1. **Functionality**: Does it work as intended?
2. **Quality**: Is the code clean and maintainable?
3. **Testing**: Is it well-tested?
4. **Documentation**: Is it documented?
5. **Compatibility**: Works on different macOS versions?

### Review Timeline
- Initial review: 1-3 days
- Follow-up: Based on complexity
- Merge: After approval and CI passes

## Release Process

### Version Numbering
We use semantic versioning: `MAJOR.MINOR.PATCH`
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes

### Creating a Release
1. Update version in relevant files
   ```bash
   python build/macos/update_version.py 1.1.0
   ```

2. Update CHANGELOG_MACOS.md

3. Create and push tag
   ```bash
   git tag -a v1.1.0 -m "Release version 1.1.0"
   git push origin v1.1.0
   ```

4. GitHub Actions automatically builds and creates release

5. Edit release notes on GitHub

## Resources

### Documentation
- [BUILD_MACOS.md](BUILD_MACOS.md) - Build instructions
- [QUICKSTART.md](QUICKSTART.md) - User guide
- [CHANGELOG_MACOS.md](../CHANGELOG_MACOS.md) - Change history

### External Resources
- [PyInstaller Documentation](https://pyinstaller.org/)
- [PyTorch MPS Backend](https://pytorch.org/docs/stable/notes/mps.html)
- [Apple Developer Documentation](https://developer.apple.com/documentation/)
- [macOS Code Signing](https://developer.apple.com/support/code-signing/)

### Original Project
- [so-vits-svc-fork](https://github.com/voicepaw/so-vits-svc-fork)
- [so-vits-svc](https://github.com/svc-develop-team/so-vits-svc)

## Community

### Communication
- **GitHub Issues**: Bug reports and feature requests
- **Pull Requests**: Code contributions
- **Discussions**: General questions and ideas

### Code of Conduct
Be respectful, inclusive, and constructive. We're all here to make great software.

## Questions?

If you have questions about contributing:
1. Check existing issues and PRs
2. Read the documentation
3. Create a discussion or issue
4. Reach out to maintainers

---

**Thank you for contributing to so-vits-svc-fork-osx!** 🙏

Your contributions help make voice conversion accessible and performant on macOS! 🍎🎵
