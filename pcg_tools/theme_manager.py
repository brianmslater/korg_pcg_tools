"""Theme manager for PCG Tools.

Based on C# MainViewModel.Theme and MdiContainer.ThemeType.

The C# version uses WPF themes (Generic, Luna, Aero) which are Windows-specific.
For Qt, we implement equivalent themes using Qt's styling system:
- Generic: System default style
- Luna: Fusion style with Windows XP-like colors
- Aero: Fusion style with Windows Vista/7-like colors (default)
"""

from enum import IntEnum
from typing import Optional

try:
    from PySide6.QtWidgets import QApplication, QStyleFactory
    from PySide6.QtGui import QPalette, QColor
    from PySide6.QtCore import Qt
    HAS_QT = True
except ImportError:
    HAS_QT = False


class ThemeType(IntEnum):
    """Theme types matching C# MainViewModel.Theme."""
    GENERIC = 0  # System default
    LUNA = 1     # Windows XP style
    AERO = 2     # Windows Vista/7 style (default)


# Luna theme colors (Windows XP blue theme)
LUNA_COLORS = {
    'window': '#ECE9D8',
    'window_text': '#000000',
    'base': '#FFFFFF',
    'alternate_base': '#F5F3EB',
    'text': '#000000',
    'button': '#ECE9D8',
    'button_text': '#000000',
    'highlight': '#316AC5',
    'highlighted_text': '#FFFFFF',
    'link': '#0000FF',
    'light': '#FFFFFF',
    'midlight': '#F5F3EB',
    'mid': '#ACA899',
    'dark': '#716F64',
    'shadow': '#000000',
}

# Aero theme colors (Windows Vista/7 glass theme)
AERO_COLORS = {
    'window': '#F0F0F0',
    'window_text': '#000000',
    'base': '#FFFFFF',
    'alternate_base': '#F5F5F5',
    'text': '#000000',
    'button': '#E1E1E1',
    'button_text': '#000000',
    'highlight': '#0078D7',
    'highlighted_text': '#FFFFFF',
    'link': '#0066CC',
    'light': '#FFFFFF',
    'midlight': '#E3E3E3',
    'mid': '#A0A0A0',
    'dark': '#696969',
    'shadow': '#000000',
}


def get_available_styles():
    """Get list of available Qt styles."""
    if not HAS_QT:
        return []
    return QStyleFactory.keys()


def apply_theme(theme: ThemeType, app: Optional['QApplication'] = None):
    """Apply a theme to the application.
    
    Based on C# MdiContainer.ThemeValueChanged().
    
    Args:
        theme: Theme type to apply
        app: QApplication instance (uses QApplication.instance() if None)
    """
    if not HAS_QT:
        return
    
    if app is None:
        app = QApplication.instance()
    
    if app is None:
        return
    
    if theme == ThemeType.GENERIC:
        _apply_generic_theme(app)
    elif theme == ThemeType.LUNA:
        _apply_luna_theme(app)
    elif theme == ThemeType.AERO:
        _apply_aero_theme(app)


def _apply_generic_theme(app: 'QApplication'):
    """Apply system default theme."""
    # Reset to system default
    app.setStyle(QStyleFactory.create(''))
    app.setPalette(app.style().standardPalette())
    app.setStyleSheet('')


def _apply_luna_theme(app: 'QApplication'):
    """Apply Luna (Windows XP) theme.
    
    Uses Fusion style with XP-like colors.
    """
    # Use Fusion style as base
    app.setStyle(QStyleFactory.create('Fusion'))
    
    # Create Luna palette
    palette = QPalette()
    
    palette.setColor(QPalette.Window, QColor(LUNA_COLORS['window']))
    palette.setColor(QPalette.WindowText, QColor(LUNA_COLORS['window_text']))
    palette.setColor(QPalette.Base, QColor(LUNA_COLORS['base']))
    palette.setColor(QPalette.AlternateBase, QColor(LUNA_COLORS['alternate_base']))
    palette.setColor(QPalette.Text, QColor(LUNA_COLORS['text']))
    palette.setColor(QPalette.Button, QColor(LUNA_COLORS['button']))
    palette.setColor(QPalette.ButtonText, QColor(LUNA_COLORS['button_text']))
    palette.setColor(QPalette.Highlight, QColor(LUNA_COLORS['highlight']))
    palette.setColor(QPalette.HighlightedText, QColor(LUNA_COLORS['highlighted_text']))
    palette.setColor(QPalette.Link, QColor(LUNA_COLORS['link']))
    palette.setColor(QPalette.Light, QColor(LUNA_COLORS['light']))
    palette.setColor(QPalette.Midlight, QColor(LUNA_COLORS['midlight']))
    palette.setColor(QPalette.Mid, QColor(LUNA_COLORS['mid']))
    palette.setColor(QPalette.Dark, QColor(LUNA_COLORS['dark']))
    palette.setColor(QPalette.Shadow, QColor(LUNA_COLORS['shadow']))
    
    app.setPalette(palette)
    app.setStyleSheet('')


def _apply_aero_theme(app: 'QApplication'):
    """Apply Aero (Windows Vista/7) theme.
    
    Uses Fusion style with Vista/7-like colors.
    This is the default theme per C# code.
    """
    # Use Fusion style as base
    app.setStyle(QStyleFactory.create('Fusion'))
    
    # Create Aero palette
    palette = QPalette()
    
    palette.setColor(QPalette.Window, QColor(AERO_COLORS['window']))
    palette.setColor(QPalette.WindowText, QColor(AERO_COLORS['window_text']))
    palette.setColor(QPalette.Base, QColor(AERO_COLORS['base']))
    palette.setColor(QPalette.AlternateBase, QColor(AERO_COLORS['alternate_base']))
    palette.setColor(QPalette.Text, QColor(AERO_COLORS['text']))
    palette.setColor(QPalette.Button, QColor(AERO_COLORS['button']))
    palette.setColor(QPalette.ButtonText, QColor(AERO_COLORS['button_text']))
    palette.setColor(QPalette.Highlight, QColor(AERO_COLORS['highlight']))
    palette.setColor(QPalette.HighlightedText, QColor(AERO_COLORS['highlighted_text']))
    palette.setColor(QPalette.Link, QColor(AERO_COLORS['link']))
    palette.setColor(QPalette.Light, QColor(AERO_COLORS['light']))
    palette.setColor(QPalette.Midlight, QColor(AERO_COLORS['midlight']))
    palette.setColor(QPalette.Mid, QColor(AERO_COLORS['mid']))
    palette.setColor(QPalette.Dark, QColor(AERO_COLORS['dark']))
    palette.setColor(QPalette.Shadow, QColor(AERO_COLORS['shadow']))
    
    app.setPalette(palette)
    app.setStyleSheet('')


def get_theme_name(theme: ThemeType) -> str:
    """Get display name for a theme."""
    names = {
        ThemeType.GENERIC: 'Generic',
        ThemeType.LUNA: 'Luna',
        ThemeType.AERO: 'Aero',
    }
    return names.get(theme, 'Unknown')


def get_theme_tooltip(theme: ThemeType) -> str:
    """Get tooltip description for a theme.
    
    Based on C# Generic_mainw_tt, Luna_mainw_tt, Aero_mainw_tt strings.
    """
    tooltips = {
        ThemeType.GENERIC: 'Generic Visual Studio designer theme',
        ThemeType.LUNA: 'Windows XP blue theme',
        ThemeType.AERO: 'Windows Vista and 7 theme',
    }
    return tooltips.get(theme, '')
