#!/usr/bin/env python3
"""Test setlist view directly."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk
from pcg_tools.reader import read_pcg_file

TEST_FILE = "/Volumes/KEYBOARD/KORGSOUNDS/ULTIMATE COVERS narfsounds 3/SETLIST Narf Ultimate Covers.PCG"

print("Testing Setlist View...")
print("="*70)

# Load PCG
pcg = read_pcg_file(TEST_FILE)
print(f"Loaded PCG with {len(pcg.set_lists)} setlists")

# Create window
root = tk.Tk()
root.title("Setlist View Test")
root.geometry("800x600")

# Import and create a minimal setlist view
from pcg_tools.gui_macos import PcgWindow

# Create a mock parent
class MockParent:
    def __init__(self):
        self.root = root
        self.status_bar = tk.Label(root, text="Status", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.windows = []

parent = MockParent()

# Create window
window = PcgWindow(parent, TEST_FILE)

print("\n✅ Window created")
print("   Click 'Set Lists' radio button")
print("   You should see:")
print("   - Dropdown with setlist names")
print("   - 'Edit Name' button")
print("   - 'New Setlist' button")

root.mainloop()
