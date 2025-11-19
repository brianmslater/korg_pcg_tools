"""Window position and size persistence."""

import json
from pathlib import Path


class WindowSettings:
    """Manage window position and size settings."""
    
    def __init__(self):
        self.settings_file = Path.home() / '.pcg_tools' / 'window_settings.json'
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        self.settings = self._load()
    
    def _load(self):
        """Load settings from file."""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save(self):
        """Save settings to file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except:
            pass
    
    def get_window_geometry(self, window_name='main'):
        """Get saved window geometry."""
        return self.settings.get(window_name, {})
    
    def save_window_geometry(self, window_name, geometry):
        """Save window geometry."""
        self.settings[window_name] = geometry
        self.save()
    
    def get_position(self, window_name='main'):
        """Get window position."""
        geom = self.get_window_geometry(window_name)
        return geom.get('x'), geom.get('y')
    
    def get_size(self, window_name='main'):
        """Get window size."""
        geom = self.get_window_geometry(window_name)
        return geom.get('width', 800), geom.get('height', 600)
    
    def save_position_and_size(self, window_name, x, y, width, height):
        """Save window position and size."""
        self.save_window_geometry(window_name, {
            'x': x,
            'y': y,
            'width': width,
            'height': height
        })


_window_settings = None


def get_window_settings():
    """Get the global window settings instance."""
    global _window_settings
    if _window_settings is None:
        _window_settings = WindowSettings()
    return _window_settings
