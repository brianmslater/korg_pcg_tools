"""Master Files - Reference PCG files for each synthesizer model.

Ported from C# PCG Tools:
- MasterFiles/IMasterFile.cs - Interface definition
- MasterFiles/MasterFile.cs - Master file class
- MasterFiles/MasterFiles.cs - Master files collection

Master files are used to:
1. Provide global data (categories, etc.) for PCG files without GLB1 chunk
2. Allow copying patches from a reference file
3. Store per-model reference files in settings
"""

from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import json
import os

from .models import PcgFile


class FileState(Enum):
    """State of a master file."""
    UNASSIGNED = "Unassigned"
    NOT_PRESENT = "Not Present"
    UNLOADED = "Unloaded"
    LOADED = "Loaded"


class AutoLoadOption(Enum):
    """Auto-load master file options."""
    ALWAYS = "always"
    ASK = "ask"
    NEVER = "never"


@dataclass
class MasterFileEntry:
    """A master file entry for a specific model/OS version."""
    model: str  # e.g., "Kronos", "Oasys", "M3"
    os_version: str  # e.g., "3.x", "2.x", "1.5/1.6", "1.0/1.1"
    file_path: str  # Path to the master PCG file
    
    @property
    def file_state(self) -> FileState:
        """Get the current state of the master file."""
        if not self.file_path:
            return FileState.UNASSIGNED
        if not os.path.exists(self.file_path):
            return FileState.NOT_PRESENT
        # Note: LOADED state would require tracking open files
        return FileState.UNLOADED
    
    @property
    def display_name(self) -> str:
        """Get display name for this entry."""
        return f"{self.model} {self.os_version}"


class MasterFiles:
    """Collection of master files for all supported models.
    
    Master files are stored in a JSON settings file and provide
    reference data for PCG files that don't have global chunks.
    """
    
    # Supported models and OS versions
    SUPPORTED_MODELS = [
        ("Kronos", "3.x"),
        ("Kronos", "2.x"),
        ("Kronos", "1.5/1.6"),
        ("Kronos", "1.0/1.1"),
        ("Oasys", ""),
        ("Krome", ""),
        ("Krome EX", ""),
        ("Kross", ""),
        ("Kross 2", ""),
        ("M3", "2.0"),
        ("M3", "1.x"),
        ("M50", ""),
        ("microStation", ""),
        ("Triton Extreme", ""),
        ("Triton", ""),
        ("Triton LE", ""),
        ("Triton Karma", ""),
        ("Trinity", "V2"),
        ("Trinity", "V3"),
    ]
    
    def __init__(self, settings_path: Optional[str] = None):
        """Initialize master files collection.
        
        Args:
            settings_path: Path to settings file. If None, uses default location.
        """
        if settings_path is None:
            # Default to user's config directory
            config_dir = Path.home() / ".pcg_tools"
            config_dir.mkdir(exist_ok=True)
            settings_path = str(config_dir / "master_files.json")
        
        self.settings_path = settings_path
        self._entries: Dict[str, MasterFileEntry] = {}
        self._loaded_files: Dict[str, PcgFile] = {}  # Cache of loaded master files
        self.auto_load = AutoLoadOption.ASK
        
        self._init_entries()
        self.load_settings()
    
    def _init_entries(self):
        """Initialize entries for all supported models."""
        for model, os_version in self.SUPPORTED_MODELS:
            key = self._make_key(model, os_version)
            self._entries[key] = MasterFileEntry(
                model=model,
                os_version=os_version,
                file_path=""
            )
    
    def _make_key(self, model: str, os_version: str) -> str:
        """Create a unique key for a model/OS version combination."""
        return f"{model}|{os_version}"
    
    def load_settings(self):
        """Load master file settings from disk."""
        if not os.path.exists(self.settings_path):
            return
        
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load auto-load setting
            if 'auto_load' in data:
                try:
                    self.auto_load = AutoLoadOption(data['auto_load'])
                except ValueError:
                    pass
            
            # Load file paths
            if 'files' in data:
                for key, path in data['files'].items():
                    if key in self._entries:
                        self._entries[key].file_path = path
        except Exception as e:
            print(f"Warning: Failed to load master files settings: {e}")
    
    def save_settings(self):
        """Save master file settings to disk."""
        data = {
            'auto_load': self.auto_load.value,
            'files': {
                key: entry.file_path
                for key, entry in self._entries.items()
                if entry.file_path
            }
        }
        
        try:
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save master files settings: {e}")
    
    def get_entries(self) -> List[MasterFileEntry]:
        """Get all master file entries."""
        return list(self._entries.values())
    
    def get_entry(self, model: str, os_version: str = "") -> Optional[MasterFileEntry]:
        """Get a specific master file entry."""
        key = self._make_key(model, os_version)
        return self._entries.get(key)
    
    def set_master_file(self, model: str, os_version: str, file_path: str):
        """Set the master file for a model/OS version.
        
        Args:
            model: Model name (e.g., "Kronos")
            os_version: OS version (e.g., "3.x")
            file_path: Path to the PCG file, or empty string to clear
        """
        key = self._make_key(model, os_version)
        if key in self._entries:
            self._entries[key].file_path = file_path
            # Clear cached file if path changed
            if key in self._loaded_files:
                del self._loaded_files[key]
            self.save_settings()
    
    def get_master_pcg(self, model: str, os_version: str = "") -> Optional[PcgFile]:
        """Get the loaded master PCG file for a model.
        
        Args:
            model: Model name
            os_version: OS version
            
        Returns:
            Loaded PcgFile or None if not available
        """
        key = self._make_key(model, os_version)
        
        # Check cache first
        if key in self._loaded_files:
            return self._loaded_files[key]
        
        # Try to load
        entry = self._entries.get(key)
        if entry is None or not entry.file_path:
            return None
        
        if not os.path.exists(entry.file_path):
            return None
        
        try:
            from .reader import read_pcg_file
            pcg = read_pcg_file(entry.file_path)
            self._loaded_files[key] = pcg
            return pcg
        except Exception as e:
            print(f"Warning: Failed to load master file {entry.file_path}: {e}")
            return None
    
    def find_master_for_pcg(self, pcg: PcgFile) -> Optional[PcgFile]:
        """Find the appropriate master file for a PCG file.
        
        Args:
            pcg: The PCG file to find a master for
            
        Returns:
            The master PcgFile or None if not found
        """
        # Determine model and OS version from the PCG file
        model = pcg.model if hasattr(pcg, 'model') else None
        os_version = pcg.os_version if hasattr(pcg, 'os_version') else ""
        
        if model is None:
            return None
        
        return self.get_master_pcg(model, os_version)
    
    def clear_cache(self):
        """Clear the cache of loaded master files."""
        self._loaded_files.clear()


# Global instance
_master_files: Optional[MasterFiles] = None


def get_master_files() -> MasterFiles:
    """Get the global MasterFiles instance."""
    global _master_files
    if _master_files is None:
        _master_files = MasterFiles()
    return _master_files


def set_master_file(model: str, os_version: str, file_path: str):
    """Convenience function to set a master file."""
    get_master_files().set_master_file(model, os_version, file_path)


def get_master_pcg(model: str, os_version: str = "") -> Optional[PcgFile]:
    """Convenience function to get a master PCG file."""
    return get_master_files().get_master_pcg(model, os_version)
