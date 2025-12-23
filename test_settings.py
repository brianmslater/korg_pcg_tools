#!/usr/bin/env python3
"""Test settings module for PCG Tools.

Tests the enhanced settings module with all C# parity settings.
"""

import os
import json
import tempfile
from pathlib import Path

# Test settings module
from pcg_tools.settings import (
    Settings, get_settings,
    ClearPatchesAlgorithm, AutoLoadMasterFiles,
    PatchDuplication, SortOrder, Theme
)


def test_settings_enums():
    """Test that all enum values match C# values."""
    # ClearPatchesAlgorithm
    assert ClearPatchesAlgorithm.NONE == 0
    assert ClearPatchesAlgorithm.UNUSED_ONLY == 1
    assert ClearPatchesAlgorithm.ASK == 2
    assert ClearPatchesAlgorithm.UNUSED_AND_USED == 3
    
    # AutoLoadMasterFiles
    assert AutoLoadMasterFiles.ALWAYS == 0
    assert AutoLoadMasterFiles.ASK == 1
    assert AutoLoadMasterFiles.NEVER == 2
    
    # PatchDuplication
    assert PatchDuplication.DO_NOT_USE_PATCH_NAMES == 0
    assert PatchDuplication.EQUAL_NAMES == 1
    assert PatchDuplication.LIKE_NAMED_NAMES == 2
    
    # SortOrder
    assert SortOrder.NAME_CATEGORY == 0
    assert SortOrder.TITLE_ARTIST_CATEGORY == 1
    assert SortOrder.ARTIST_TITLE_CATEGORY == 2
    assert SortOrder.CATEGORY_NAME == 3
    assert SortOrder.CATEGORY_TITLE_ARTIST == 4
    assert SortOrder.CATEGORY_ARTIST_TITLE == 5
    
    # Theme (from C# MainViewModel.Theme)
    assert Theme.GENERIC == 0
    assert Theme.LUNA == 1
    assert Theme.AERO == 2
    
    print("✓ All enum values match C# values")


def test_settings_defaults():
    """Test that default settings match C# defaults.
    
    All defaults verified against C# Settings.Designer.cs
    """
    # Create a fresh settings instance with temp file
    with tempfile.TemporaryDirectory() as tmpdir:
        settings_file = Path(tmpdir) / 'settings.json'
        
        s = Settings()
        s.settings_file = settings_file
        
        # PCG Window defaults (from C# UI_* settings)
        assert s.show_number_of_references_column == False  # C# UI_ShowNumberOfReferencesColumn = False
        assert s.single_lined_setlist_slot_descriptions == False  # C# SingleLinedSetListSlotDescriptions = False
        assert s.clear_patches_algorithm == ClearPatchesAlgorithm.ASK  # C# UI_ClearPatches = 2
        assert s.clear_patches_fix_references == True  # C# UI_ClearPatchesFixReferences = True
        
        # Files defaults (from C# Settings_* settings)
        assert s.auto_backup_enabled == True  # C# Settings_AutoBackupFilesEnabled = True
        assert s.auto_backup_interval_minutes == 5  # C# Settings_AutoBackupFilesIntervalTime = 5
        assert s.auto_backup_max_storage_mb == 500  # C# Settings_AutoBackupFilesMaxStorage = 500
        assert s.master_files_auto_load == AutoLoadMasterFiles.ASK  # C# MasterFiles_AutoLoad = 1
        
        # Edit defaults
        assert s.rename_file_when_patch_name_changes == True  # C# Edit_RenameFileWhenPatchNameChanges = True
        
        # Copy/Paste defaults (from C# CopyPaste_* settings)
        assert s.copy_incomplete_combis == True  # C# CopyPaste_CopyIncompleteCombis = True
        assert s.copy_incomplete_setlist_slots == True  # C# CopyPaste_CopyIncompleteSetListSlots = True
        assert s.copy_patches_from_master_file == False  # C# CopyPaste_CopyPatchesFromMasterFile = False
        assert s.paste_duplicate_programs == False  # C# CopyPaste_PasteDuplicatePrograms = False
        assert s.paste_duplicate_combis == False  # C# CopyPaste_PasteDuplicateCombis = False
        assert s.paste_duplicate_setlist_slots == True  # C# CopyPaste_PasteDuplicateSetListSlots = True
        assert s.paste_duplicate_drum_kits == False  # C# CopyPaste_PasteDuplicateDrumKits = False
        assert s.paste_duplicate_drum_patterns == False  # C# CopyPaste_PasteDuplicateDrumPatterns = False
        assert s.paste_duplicate_wave_sequences == False  # C# CopyPaste_PasteDuplicateWaveSequences = False
        assert s.auto_extend_paste == True  # C# CopyPaste_AutoExtendedSinglePatchSelectionPaste = True
        assert s.patch_duplication_checking == PatchDuplication.DO_NOT_USE_PATCH_NAMES  # C# CopyPaste_PatchDuplicationName = 0
        assert s.overwrite_filled_programs == False  # C# CopyPaste_OverwriteFilledPrograms = False
        assert s.overwrite_filled_combis == False  # C# CopyPaste_OverwriteFilledCombis = False
        assert s.overwrite_filled_setlist_slots == True  # C# CopyPaste_OverwriteFilledSetListSlots = True
        
        # Sort defaults (from C# Sort_* settings)
        assert s.sort_split_character == "-"  # C# Sort_SplitCharacter = "-"
        assert s.sort_artist_title_order == True  # C# Sort_ArtistTitleSortOrder = True
        assert s.sort_order == SortOrder.NAME_CATEGORY  # C# Sort_Order = 0
        
        # Categories defaults
        assert s.trinity_category_set_a == True  # C# TrinityCategorySetA = True
        
        # Theme defaults (from C# MainViewModel.Theme - default is Aero)
        assert s.selected_theme == Theme.AERO  # C# default: Aero (Windows Vista/7 theme)
        
        print("✓ All default settings match C# defaults")


def test_settings_save_load():
    """Test that settings can be saved and loaded correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        settings_file = Path(tmpdir) / 'settings.json'
        
        # Create settings and modify values
        s1 = Settings()
        s1.settings_file = settings_file
        
        s1.show_number_of_references_column = False
        s1.clear_patches_algorithm = ClearPatchesAlgorithm.UNUSED_ONLY
        s1.auto_backup_enabled = True
        s1.auto_backup_interval_minutes = 10
        s1.master_files_auto_load = AutoLoadMasterFiles.NEVER
        s1.paste_duplicate_programs = True
        s1.sort_split_character = "/"
        s1.sort_order = SortOrder.CATEGORY_NAME
        s1.trinity_category_set_a = False
        s1.selected_theme = Theme.LUNA
        
        s1.save()
        
        # Load into new instance
        s2 = Settings()
        s2.settings_file = settings_file
        s2.load()
        
        # Verify values
        assert s2.show_number_of_references_column == False
        assert s2.clear_patches_algorithm == ClearPatchesAlgorithm.UNUSED_ONLY
        assert s2.auto_backup_enabled == True
        assert s2.auto_backup_interval_minutes == 10
        assert s2.master_files_auto_load == AutoLoadMasterFiles.NEVER
        assert s2.paste_duplicate_programs == True
        assert s2.sort_split_character == "/"
        assert s2.sort_order == SortOrder.CATEGORY_NAME
        assert s2.trinity_category_set_a == False
        assert s2.selected_theme == Theme.LUNA
        
        print("✓ Settings save/load works correctly")


def test_settings_json_structure():
    """Test that saved JSON has correct structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        settings_file = Path(tmpdir) / 'settings.json'
        
        s = Settings()
        s.settings_file = settings_file
        s.save()
        
        # Load JSON directly
        with open(settings_file, 'r') as f:
            data = json.load(f)
        
        # Check all expected keys exist
        expected_keys = [
            'recent_files', 'max_recent_files', 'auto_save',
            'show_number_of_references_column', 'single_lined_setlist_slot_descriptions',
            'clear_patches_algorithm', 'clear_patches_fix_references',
            'auto_backup_enabled', 'auto_backup_interval_minutes', 'auto_backup_max_storage_mb',
            'master_files_auto_load', 'default_output_directory',
            'rename_file_when_patch_name_changes',
            'copy_incomplete_combis', 'copy_incomplete_setlist_slots',
            'paste_duplicate_programs', 'paste_duplicate_combis', 'paste_duplicate_setlist_slots',
            'auto_extend_paste', 'patch_duplication_checking', 'ignore_characters_for_duplication',
            'overwrite_filled_programs', 'overwrite_filled_combis', 'overwrite_filled_setlist_slots',
            'sort_split_character', 'sort_artist_title_order', 'sort_order',
            'trinity_category_set_a', 'settings_tab_index', 'selected_theme'
        ]
        
        for key in expected_keys:
            assert key in data, f"Missing key: {key}"
        
        print("✓ JSON structure is correct")


def test_recent_files():
    """Test recent files functionality."""
    with tempfile.TemporaryDirectory() as tmpdir:
        settings_file = Path(tmpdir) / 'settings.json'
        test_file = Path(tmpdir) / 'test.pcg'
        test_file.touch()
        
        s = Settings()
        s.settings_file = settings_file
        s.recent_files = []
        
        # Add a file
        s.add_recent_file(str(test_file))
        assert len(s.recent_files) == 1
        assert str(test_file.absolute()) in s.recent_files
        
        # Add same file again - should move to front, not duplicate
        s.add_recent_file(str(test_file))
        assert len(s.recent_files) == 1
        
        # Get recent files - should only return existing files
        existing = s.get_recent_files()
        assert len(existing) == 1
        
        # Add non-existent file
        s.recent_files.append('/nonexistent/file.pcg')
        existing = s.get_recent_files()
        assert len(existing) == 1  # Non-existent file filtered out
        
        print("✓ Recent files functionality works correctly")


def test_theme_settings():
    """Test theme settings matching C# MainViewModel.Theme.
    
    Based on C# MainWindow.xaml Theme menu and MdiContainer.ThemeType.
    """
    # Test Theme enum values match C# MainViewModel.Theme
    assert Theme.GENERIC == 0  # C# Theme.Generic
    assert Theme.LUNA == 1     # C# Theme.Luna (Windows XP)
    assert Theme.AERO == 2     # C# Theme.Aero (Windows Vista/7)
    
    # Test theme save/load
    with tempfile.TemporaryDirectory() as tmpdir:
        settings_file = Path(tmpdir) / 'settings.json'
        
        # Test each theme value
        for theme in [Theme.GENERIC, Theme.LUNA, Theme.AERO]:
            s1 = Settings()
            s1.settings_file = settings_file
            s1.selected_theme = theme
            s1.save()
            
            s2 = Settings()
            s2.settings_file = settings_file
            s2.load()
            
            assert s2.selected_theme == theme, f"Theme {theme} not saved/loaded correctly"
    
    print("✓ Theme settings work correctly")


if __name__ == '__main__':
    print("Testing PCG Tools Settings Module")
    print("=" * 50)
    
    test_settings_enums()
    test_settings_defaults()
    test_settings_save_load()
    test_settings_json_structure()
    test_recent_files()
    test_theme_settings()
    
    print("=" * 50)
    print("All settings tests passed!")
