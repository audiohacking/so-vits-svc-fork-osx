#!/usr/bin/env python3
"""
Test script to validate PyInstaller spec file configuration.

This test ensures that the executable name in the EXE section matches
the CFBundleExecutable value in the BUNDLE section's Info.plist.

Issue: The macOS app failed to launch because of a mismatch where:
- EXE name was set to '{app_name}_bin'
- CFBundleExecutable was set to '{app_name}'

This caused macOS to be unable to find the executable when launching the app.

Fix: Changed CFBundleExecutable to '{app_name}_bin' to match the EXE name.
"""

from pathlib import Path
from unittest import TestCase


class TestPyInstallerSpec(TestCase):
    """Test that the PyInstaller spec file is correctly configured."""
    
    def test_spec_file_exists(self):
        """Test that the spec file exists."""
        project_root = Path(__file__).parent.parent
        spec_file = project_root / 'SoVitsSVC-OSX.spec'
        self.assertTrue(spec_file.exists(), f"Spec file not found: {spec_file}")
    
    def test_executable_name_configuration(self):
        """Test that EXE name and CFBundleExecutable match."""
        project_root = Path(__file__).parent.parent
        spec_file = project_root / 'SoVitsSVC-OSX.spec'
        
        # Read the spec file
        with open(spec_file, 'r') as f:
            spec_content = f.read()
        
        # Expected app name
        app_name = 'SoVitsSVC-OSX'
        
        # Test EXE name configuration
        exe_name_pattern = "name=f'{app_name}_bin'"
        self.assertIn(exe_name_pattern, spec_content,
                     f"EXE name pattern not found. Expected: {exe_name_pattern}")
        
        # Test CFBundleExecutable configuration
        bundle_exec_pattern = "'CFBundleExecutable': f'{app_name}_bin'"
        self.assertIn(bundle_exec_pattern, spec_content,
                     f"CFBundleExecutable pattern not found. Expected: {bundle_exec_pattern}")
        
        # Verify they evaluate to the same value
        expected_name = f'{app_name}_bin'
        self.assertEqual(expected_name, 'SoVitsSVC-OSX_bin',
                        "Executable name should be SoVitsSVC-OSX_bin")
    
    def test_source_file_exists(self):
        """Test that the source file exists."""
        project_root = Path(__file__).parent.parent
        gui_web_path = project_root / 'src' / 'so_vits_svc_fork' / 'gui_web.py'
        self.assertTrue(gui_web_path.exists(), f"Source file not found: {gui_web_path}")
    
    def test_console_disabled(self):
        """Test that console is disabled for GUI app."""
        project_root = Path(__file__).parent.parent
        spec_file = project_root / 'SoVitsSVC-OSX.spec'
        
        with open(spec_file, 'r') as f:
            spec_content = f.read()
        
        self.assertIn("console=False", spec_content,
                     "Console should be disabled for GUI app")
    
    def test_bundle_identifier(self):
        """Test that bundle identifier is set correctly."""
        project_root = Path(__file__).parent.parent
        spec_file = project_root / 'SoVitsSVC-OSX.spec'
        
        with open(spec_file, 'r') as f:
            spec_content = f.read()
        
        bundle_id = "bundle_identifier='com.audiohacking.sovitssvc-osx'"
        self.assertIn(bundle_id, spec_content,
                     f"Bundle identifier not found: {bundle_id}")

