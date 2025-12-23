"""Settings management for PCG Tools.

Ported from C# SettingsWindow.xaml.cs - provides complete settings parity.
"""

import json
from pathlib import Path
from typing import List, Optional
from enum import IntEnum


class ClearPatchesAlgorithm(IntEnum):
    """Clear patches algorithm options (from C# ClearCommands.ClearPatchesAlgorithm)."""
    NONE = 0
    UNUSED_ONLY = 1
    ASK = 2
    UNUSED_AND_USED = 3


class AutoLoadMasterFiles(IntEnum):
    """Auto-load master file options (from C# MasterFiles.AutoLoadMasterFiles)."""
    ALWAYS = 0
    ASK = 1
    NEVER = 2


class PatchDuplication(IntEnum):
    """Patch duplication checking options (from C# CopyPaste.PatchDuplication)."""
    DO_NOT_USE_PATCH_NAMES = 0
    EQUAL_NAMES = 1
    LIKE_NAMED_NAMES = 2


class SortOrder(IntEnum):
    """Sort order options (from C# PatchSorter.SortOrder)."""
    NAME_CATEGORY = 0
    TITLE_ARTIST_CATEGORY = 1
    ARTIST_TITLE_CATEGORY = 2
    CATEGORY_NAME = 3
    CATEGORY_TITLE_ARTIST = 4
    CATEGORY_ARTIST_TITLE = 5


class Theme(IntEnum):
    """Theme options (from C# MainViewModel.Theme).
    
    Maps to Qt styles:
    - Generic: System default style
    - Luna: Windows XP style (Fusion on Qt)
    - Aero: Windows Vista/7 style (Fusion with light colors on Qt)
    """
    GENERIC = 0
    LUNA = 1
    AERO = 2


class Settings:
    """Application settings - matches C# Settings.Default structure."""
    
    def __init__(self):
        self.settings_file = Path.home() / '.pcg_tools' / 'settings.json'
        self.settings_file.parent.mkdir(exist_ok=True)
        
        # Basic settings
        self.recent_files: List[str] = []
        self.max_recent_files = 10
        self.auto_save = False
        self.confirm_clear = True
        self.confirm_delete = True
        
        # PCG Window settings (from C# UI_* settings)
        self.show_number_of_references_column = False  # C# default: False
        self.single_lined_setlist_slot_descriptions = False  # C# default: False
        self.clear_patches_algorithm = ClearPatchesAlgorithm.ASK
        self.clear_patches_fix_references = True
        
        # Files settings (from C# Settings_* and Slg_* settings)
        self.auto_backup_enabled = True  # C# default: True
        self.auto_backup_interval_minutes = 5
        self.auto_backup_max_storage_mb = 500
        self.master_files_auto_load = AutoLoadMasterFiles.ASK
        self.default_output_directory: str = ""
        self.default_output_directory_sequencer: str = ""
        self.default_manual_path: str = ""
        
        # Edit settings
        self.rename_file_when_patch_name_changes = True  # C# default: True
        
        # Cut/Copy/Paste settings (from C# CopyPaste_* settings)
        self.copy_incomplete_combis = True  # C# default: True
        self.copy_incomplete_setlist_slots = True  # C# default: True
        self.copy_patches_from_master_file = False
        
        self.paste_duplicate_programs = False
        self.paste_duplicate_combis = False
        self.paste_duplicate_setlist_slots = True
        self.paste_duplicate_drum_kits = False  # C# default: False
        self.paste_duplicate_drum_patterns = False  # C# default: False
        self.paste_duplicate_wave_sequences = False  # C# default: False
        
        self.auto_extend_paste = True
        
        self.patch_duplication_checking = PatchDuplication.DO_NOT_USE_PATCH_NAMES
        self.ignore_characters_for_duplication: str = ""
        
        self.overwrite_filled_programs = False
        self.overwrite_filled_combis = False
        self.overwrite_filled_setlist_slots = True  # C# default: True
        self.overwrite_filled_drum_kits = False
        self.overwrite_filled_drum_patterns = False
        self.overwrite_filled_wave_sequences = False
        
        # Sort settings (from C# Sort_* settings)
        self.sort_split_character: str = "-"
        self.sort_artist_title_order = True  # C# default: True (Artist-Title order)
        self.sort_order = SortOrder.NAME_CATEGORY
        
        # Categories settings (Trinity-specific)
        self.trinity_category_set_a = True  # True = Set A, False = Set B
        
        # Theme setting (from C# MainViewModel.SelectedTheme)
        self.selected_theme = Theme.AERO  # C# default: Aero
        
        # Settings tab index (remember last tab)
        self.settings_tab_index = 0
        
        self.load()
    
    def load(self):
        """Load settings from file."""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    data = json.load(f)
                    
                    # Basic settings
                    self.recent_files = data.get('recent_files', [])
                    self.max_recent_files = data.get('max_recent_files', 10)
                    self.auto_save = data.get('auto_save', False)
                    self.confirm_clear = data.get('confirm_clear', True)
                    self.confirm_delete = data.get('confirm_delete', True)
                    
                    # PCG Window settings
                    self.show_number_of_references_column = data.get('show_number_of_references_column', False)
                    self.single_lined_setlist_slot_descriptions = data.get('single_lined_setlist_slot_descriptions', False)
                    self.clear_patches_algorithm = ClearPatchesAlgorithm(data.get('clear_patches_algorithm', 2))
                    self.clear_patches_fix_references = data.get('clear_patches_fix_references', True)
                    
                    # Files settings
                    self.auto_backup_enabled = data.get('auto_backup_enabled', True)
                    self.auto_backup_interval_minutes = data.get('auto_backup_interval_minutes', 5)
                    self.auto_backup_max_storage_mb = data.get('auto_backup_max_storage_mb', 500)
                    self.master_files_auto_load = AutoLoadMasterFiles(data.get('master_files_auto_load', 1))
                    self.default_output_directory = data.get('default_output_directory', "")
                    self.default_output_directory_sequencer = data.get('default_output_directory_sequencer', "")
                    self.default_manual_path = data.get('default_manual_path', "")
                    
                    # Edit settings
                    self.rename_file_when_patch_name_changes = data.get('rename_file_when_patch_name_changes', True)
                    
                    # Cut/Copy/Paste settings
                    self.copy_incomplete_combis = data.get('copy_incomplete_combis', True)
                    self.copy_incomplete_setlist_slots = data.get('copy_incomplete_setlist_slots', True)
                    self.copy_patches_from_master_file = data.get('copy_patches_from_master_file', False)
                    
                    self.paste_duplicate_programs = data.get('paste_duplicate_programs', False)
                    self.paste_duplicate_combis = data.get('paste_duplicate_combis', False)
                    self.paste_duplicate_setlist_slots = data.get('paste_duplicate_setlist_slots', True)
                    self.paste_duplicate_drum_kits = data.get('paste_duplicate_drum_kits', False)
                    self.paste_duplicate_drum_patterns = data.get('paste_duplicate_drum_patterns', False)
                    self.paste_duplicate_wave_sequences = data.get('paste_duplicate_wave_sequences', False)
                    
                    self.auto_extend_paste = data.get('auto_extend_paste', True)
                    
                    self.patch_duplication_checking = PatchDuplication(data.get('patch_duplication_checking', 0))
                    self.ignore_characters_for_duplication = data.get('ignore_characters_for_duplication', "")
                    
                    self.overwrite_filled_programs = data.get('overwrite_filled_programs', False)
                    self.overwrite_filled_combis = data.get('overwrite_filled_combis', False)
                    self.overwrite_filled_setlist_slots = data.get('overwrite_filled_setlist_slots', True)
                    self.overwrite_filled_drum_kits = data.get('overwrite_filled_drum_kits', False)
                    self.overwrite_filled_drum_patterns = data.get('overwrite_filled_drum_patterns', False)
                    self.overwrite_filled_wave_sequences = data.get('overwrite_filled_wave_sequences', False)
                    
                    # Sort settings
                    self.sort_split_character = data.get('sort_split_character', "-")
                    self.sort_artist_title_order = data.get('sort_artist_title_order', True)
                    self.sort_order = SortOrder(data.get('sort_order', 0))
                    
                    # Categories settings
                    self.trinity_category_set_a = data.get('trinity_category_set_a', True)
                    
                    # Theme setting
                    self.selected_theme = Theme(data.get('selected_theme', 2))  # Default: Aero
                    
                    # Settings tab index
                    self.settings_tab_index = data.get('settings_tab_index', 0)
                    
            except Exception:
                pass
    
    def save(self):
        """Save settings to file."""
        try:
            data = {
                # Basic settings
                'recent_files': self.recent_files,
                'max_recent_files': self.max_recent_files,
                'auto_save': self.auto_save,
                'confirm_clear': self.confirm_clear,
                'confirm_delete': self.confirm_delete,
                
                # PCG Window settings
                'show_number_of_references_column': self.show_number_of_references_column,
                'single_lined_setlist_slot_descriptions': self.single_lined_setlist_slot_descriptions,
                'clear_patches_algorithm': int(self.clear_patches_algorithm),
                'clear_patches_fix_references': self.clear_patches_fix_references,
                
                # Files settings
                'auto_backup_enabled': self.auto_backup_enabled,
                'auto_backup_interval_minutes': self.auto_backup_interval_minutes,
                'auto_backup_max_storage_mb': self.auto_backup_max_storage_mb,
                'master_files_auto_load': int(self.master_files_auto_load),
                'default_output_directory': self.default_output_directory,
                'default_output_directory_sequencer': self.default_output_directory_sequencer,
                'default_manual_path': self.default_manual_path,
                
                # Edit settings
                'rename_file_when_patch_name_changes': self.rename_file_when_patch_name_changes,
                
                # Cut/Copy/Paste settings
                'copy_incomplete_combis': self.copy_incomplete_combis,
                'copy_incomplete_setlist_slots': self.copy_incomplete_setlist_slots,
                'copy_patches_from_master_file': self.copy_patches_from_master_file,
                
                'paste_duplicate_programs': self.paste_duplicate_programs,
                'paste_duplicate_combis': self.paste_duplicate_combis,
                'paste_duplicate_setlist_slots': self.paste_duplicate_setlist_slots,
                'paste_duplicate_drum_kits': self.paste_duplicate_drum_kits,
                'paste_duplicate_drum_patterns': self.paste_duplicate_drum_patterns,
                'paste_duplicate_wave_sequences': self.paste_duplicate_wave_sequences,
                
                'auto_extend_paste': self.auto_extend_paste,
                
                'patch_duplication_checking': int(self.patch_duplication_checking),
                'ignore_characters_for_duplication': self.ignore_characters_for_duplication,
                
                'overwrite_filled_programs': self.overwrite_filled_programs,
                'overwrite_filled_combis': self.overwrite_filled_combis,
                'overwrite_filled_setlist_slots': self.overwrite_filled_setlist_slots,
                'overwrite_filled_drum_kits': self.overwrite_filled_drum_kits,
                'overwrite_filled_drum_patterns': self.overwrite_filled_drum_patterns,
                'overwrite_filled_wave_sequences': self.overwrite_filled_wave_sequences,
                
                # Sort settings
                'sort_split_character': self.sort_split_character,
                'sort_artist_title_order': self.sort_artist_title_order,
                'sort_order': int(self.sort_order),
                
                # Categories settings
                'trinity_category_set_a': self.trinity_category_set_a,
                
                # Theme setting
                'selected_theme': int(self.selected_theme),
                
                # Settings tab index
                'settings_tab_index': self.settings_tab_index,
            }
            with open(self.settings_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
    
    def add_recent_file(self, filepath: str):
        """Add file to recent files list."""
        filepath = str(Path(filepath).absolute())
        
        # Remove if already in list
        if filepath in self.recent_files:
            self.recent_files.remove(filepath)
        
        # Add to front
        self.recent_files.insert(0, filepath)
        
        # Trim to max
        self.recent_files = self.recent_files[:self.max_recent_files]
        
        self.save()
    
    def get_recent_files(self) -> List[str]:
        """Get list of recent files that still exist."""
        return [f for f in self.recent_files if Path(f).exists()]


# Global settings instance
_settings = None

def get_settings() -> Settings:
    """Get global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
