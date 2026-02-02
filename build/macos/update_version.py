#!/usr/bin/env python3
"""
Version information updater for macOS builds
This script updates version strings in the PyInstaller spec and other files
"""

import sys
from pathlib import Path


def update_version(version: str) -> None:
    """Update version strings in project files."""
    project_root = Path(__file__).parent.parent

    # Update spec file
    spec_file = project_root / "SoVitsSVC-OSX.spec"
    if spec_file.exists():
        content = spec_file.read_text()
        # Update CFBundleVersion and CFBundleShortVersionString
        content = content.replace("'CFBundleVersion': '1.0.0'", f"'CFBundleVersion': '{version}'")
        content = content.replace("'CFBundleShortVersionString': '1.0.0'", f"'CFBundleShortVersionString': '{version}'")
        spec_file.write_text(content)
        print(f"✓ Updated {spec_file.name}")

    # Update __init__.py
    init_file = project_root / "src" / "so_vits_svc_fork" / "__init__.py"
    if init_file.exists():
        content = init_file.read_text()
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("__version__"):
                lines[i] = f'__version__ = "{version}"'
                break
        init_file.write_text("\n".join(lines))
        print(f"✓ Updated {init_file.name}")


def main() -> None:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python update_version.py <version>")
        print("Example: python update_version.py 1.0.1")
        sys.exit(1)

    version = sys.argv[1].lstrip("v")  # Remove 'v' prefix if present
    print(f"Updating version to {version}")
    update_version(version)
    print("✓ Version update complete")


if __name__ == "__main__":
    main()
