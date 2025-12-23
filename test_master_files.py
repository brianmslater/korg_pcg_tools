"""Tests for the Master Files module.

Tests the master files functionality ported from C# PCG Tools.
"""

import pytest
import os
import tempfile
import json

from pcg_tools.master_files import (
    MasterFiles, MasterFileEntry, FileState, AutoLoadOption,
    get_master_files, set_master_file, get_master_pcg
)


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def temp_settings_file():
    """Create a temporary settings file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{}')
        temp_path = f.name
    yield temp_path
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def master_files(temp_settings_file):
    """Create a MasterFiles instance with temp settings."""
    return MasterFiles(settings_path=temp_settings_file)


# =============================================================================
# MasterFileEntry Tests
# =============================================================================

class TestMasterFileEntry:
    """Test the MasterFileEntry class."""
    
    def test_unassigned_state(self):
        """Entry with no file path is unassigned."""
        entry = MasterFileEntry(model="Kronos", os_version="3.x", file_path="")
        assert entry.file_state == FileState.UNASSIGNED
    
    def test_not_present_state(self):
        """Entry with non-existent file path is not present."""
        entry = MasterFileEntry(
            model="Kronos", 
            os_version="3.x", 
            file_path="/nonexistent/path/file.pcg"
        )
        assert entry.file_state == FileState.NOT_PRESENT
    
    def test_unloaded_state(self, temp_settings_file):
        """Entry with existing file path is unloaded."""
        entry = MasterFileEntry(
            model="Kronos",
            os_version="3.x",
            file_path=temp_settings_file  # Use the temp file as it exists
        )
        assert entry.file_state == FileState.UNLOADED
    
    def test_display_name(self):
        """Display name combines model and OS version."""
        entry = MasterFileEntry(model="Kronos", os_version="3.x", file_path="")
        assert entry.display_name == "Kronos 3.x"
        
        entry2 = MasterFileEntry(model="Oasys", os_version="", file_path="")
        assert entry2.display_name == "Oasys "


# =============================================================================
# MasterFiles Tests
# =============================================================================

class TestMasterFiles:
    """Test the MasterFiles class."""
    
    def test_init_creates_entries(self, master_files):
        """Initialization creates entries for all supported models."""
        entries = master_files.get_entries()
        assert len(entries) > 0
        
        # Check some expected models exist
        kronos_entry = master_files.get_entry("Kronos", "3.x")
        assert kronos_entry is not None
        assert kronos_entry.model == "Kronos"
        assert kronos_entry.os_version == "3.x"
    
    def test_set_master_file(self, master_files, temp_settings_file):
        """Setting a master file updates the entry."""
        master_files.set_master_file("Kronos", "3.x", "/path/to/file.pcg")
        
        entry = master_files.get_entry("Kronos", "3.x")
        assert entry.file_path == "/path/to/file.pcg"
    
    def test_set_master_file_saves_settings(self, master_files, temp_settings_file):
        """Setting a master file saves to settings file."""
        master_files.set_master_file("Kronos", "3.x", "/path/to/file.pcg")
        
        # Read settings file
        with open(temp_settings_file, 'r') as f:
            data = json.load(f)
        
        assert 'files' in data
        assert 'Kronos|3.x' in data['files']
        assert data['files']['Kronos|3.x'] == "/path/to/file.pcg"
    
    def test_clear_master_file(self, master_files):
        """Clearing a master file sets empty path."""
        master_files.set_master_file("Kronos", "3.x", "/path/to/file.pcg")
        master_files.set_master_file("Kronos", "3.x", "")
        
        entry = master_files.get_entry("Kronos", "3.x")
        assert entry.file_path == ""
        assert entry.file_state == FileState.UNASSIGNED
    
    def test_load_settings(self, temp_settings_file):
        """Loading settings restores file paths."""
        # Write settings
        with open(temp_settings_file, 'w') as f:
            json.dump({
                'auto_load': 'always',
                'files': {
                    'Kronos|3.x': '/path/to/kronos.pcg',
                    'Oasys|': '/path/to/oasys.pcg'
                }
            }, f)
        
        # Create new instance that loads settings
        master_files = MasterFiles(settings_path=temp_settings_file)
        
        kronos_entry = master_files.get_entry("Kronos", "3.x")
        assert kronos_entry.file_path == '/path/to/kronos.pcg'
        
        oasys_entry = master_files.get_entry("Oasys", "")
        assert oasys_entry.file_path == '/path/to/oasys.pcg'
        
        assert master_files.auto_load == AutoLoadOption.ALWAYS
    
    def test_auto_load_setting(self, master_files, temp_settings_file):
        """Auto-load setting is saved and loaded."""
        master_files.auto_load = AutoLoadOption.NEVER
        master_files.save_settings()
        
        # Read settings file
        with open(temp_settings_file, 'r') as f:
            data = json.load(f)
        
        assert data['auto_load'] == 'never'
    
    def test_get_master_pcg_unassigned(self, master_files):
        """Getting master PCG for unassigned entry returns None."""
        pcg = master_files.get_master_pcg("Kronos", "3.x")
        assert pcg is None
    
    def test_get_master_pcg_not_present(self, master_files):
        """Getting master PCG for non-existent file returns None."""
        master_files.set_master_file("Kronos", "3.x", "/nonexistent/file.pcg")
        pcg = master_files.get_master_pcg("Kronos", "3.x")
        assert pcg is None
    
    def test_clear_cache(self, master_files):
        """Clearing cache removes loaded files."""
        # Just verify it doesn't error
        master_files.clear_cache()


# =============================================================================
# AutoLoadOption Tests
# =============================================================================

class TestAutoLoadOption:
    """Test the AutoLoadOption enum."""
    
    def test_values(self):
        """Auto-load options have expected values."""
        assert AutoLoadOption.ALWAYS.value == "always"
        assert AutoLoadOption.ASK.value == "ask"
        assert AutoLoadOption.NEVER.value == "never"


# =============================================================================
# Integration Tests
# =============================================================================

class TestMasterFilesIntegration:
    """Integration tests with real PCG files."""
    
    def test_load_real_master_file(self, master_files):
        """Test loading a real PCG file as master."""
        test_file = 'files_2_test/nw.PCG'
        if not os.path.exists(test_file):
            pytest.skip(f"Test file not found: {test_file}")
        
        # Set as master file
        master_files.set_master_file("Kronos", "3.x", test_file)
        
        # Load it
        pcg = master_files.get_master_pcg("Kronos", "3.x")
        assert pcg is not None
        
        # Verify it's cached
        pcg2 = master_files.get_master_pcg("Kronos", "3.x")
        assert pcg2 is pcg  # Same object


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
