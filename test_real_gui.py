#!/usr/bin/env python3
"""Test the actual GUI with real PCG files from KEYBOARD device."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcg_tools.gui import launch_gui

# Set environment variable to suppress Tk deprecation warning
os.environ['TK_SILENCE_DEPRECATION'] = '1'

print("Launching PCG Tools GUI...")
print("Test files available on KEYBOARD device:")
print("  - /Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG")
print("  - /Volumes/KEYBOARD/Narf Sounds Movie TV Themes/Narf Sounds Movie TV Themes.PCG")
print("\nUse File > Open PCG to load a file and verify patches display correctly.\n")

launch_gui()
