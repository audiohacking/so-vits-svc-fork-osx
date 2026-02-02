#!/bin/bash
# Script to check the status of macOS build tests
# Run this to see if the macOS build is working

set -e

echo "======================================================================"
echo "macOS Build Test Status Checker"
echo "======================================================================"
echo ""

echo "Checking local validation tests..."
echo ""

# Run unit tests
echo "1. Running PyInstaller spec unit tests..."
if python3 -m unittest tests.test_pyinstaller_spec -v 2>&1 | grep -q "OK"; then
    echo "   ✓ Unit tests: PASS"
else
    echo "   ✗ Unit tests: FAIL"
    exit 1
fi
echo ""

# Run simulation
echo "2. Running build simulation..."
if python3 tests/test_build_simulation.py 2>&1 | grep -q "SIMULATION SUCCESSFUL"; then
    echo "   ✓ Build simulation: PASS"
else
    echo "   ✗ Build simulation: FAIL"
    exit 1
fi
echo ""

echo "3. Checking spec file configuration..."
python3 << 'PYTHON_CHECK'
from pathlib import Path
spec_file = Path('SoVitsSVC-OSX.spec')
content = spec_file.read_text()
if "name=f'{app_name}_bin'" in content and "'CFBundleExecutable': f'{app_name}_bin'" in content:
    print("   ✓ Spec file: CORRECT")
else:
    print("   ✗ Spec file: INCORRECT")
    exit(1)
PYTHON_CHECK
echo ""

echo "======================================================================"
echo "✓ All local validation tests PASSED"
echo "======================================================================"
echo ""
echo "To test on real macOS:"
echo "  1. Go to: https://github.com/audiohacking/so-vits-svc-fork-osx/actions"
echo "  2. Approve the 'Test macOS Build' workflow run"
echo "  3. Wait for completion (~5-10 minutes)"
echo "  4. Download the artifact 'SoVitsSVC-OSX-test-build'"
echo "  5. Test the app on macOS"
echo ""
echo "Expected result: App launches without traceback errors"
echo "======================================================================"
