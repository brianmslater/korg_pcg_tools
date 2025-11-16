"""Settings management for PCG Tools."""

import json
from pathlib import Path
from typing import List


class Settings:
    """Application settings."""
    
    def __init__(self):
        self.settings_file = Path.home() / '.pcg_tools' / 'settings.json'
        self.settings_file.parent.mkdir(exist_ok=True)
        
        self.recent_files: List[str] = []
        self.max_recent_files = 10
        self.auto_save = False
        self.confirm_clear = True
        self.confirm_delete = True
        
        self.load()
    
    def load(self):
        """Load settings from file."""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    data = json.load(f)
                    self.recent_files = data.get('recent_files', [])
                    self.max_recent_files = data.get('max_recent_files', 10)
                    self.auto_save = data.get('auto_save', False)
                    self.confirm_clear = data.get('confirm_clear', True)
                    self.confirm_delete = data.get('confirm_delete', True)
            except Exception:
                pass
    
    def save(self):
        """Save settings to file."""
        try:
            data = {
                'recent_files': self.recent_files,
                'max_recent_files': self.max_recent_files,
                'auto_save': self.auto_save,
                'confirm_clear': self.confirm_clear,
                'confirm_delete': self.confirm_delete
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
