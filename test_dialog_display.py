#!/usr/bin/env python3
"""Test that edit dialog displays correctly with visible buttons."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk
from pcg_tools.models import Program, Category
from pcg_tools.edit_dialog import EditPatchDialog

print("Testing Edit Dialog Display...")
print("="*70)

# Create a test window
root = tk.Tk()
root.title("Test Window")
root.geometry("600x400")

# Create a test program
test_program = Program(
    bank="I-A",
    index=0,
    name="Test Program",
    category=Category(0, 0, "Keyboard", "Acoustic Piano"),
    favorite=False,
    raw_data=b'\x00' * 4960
)

def test_dialog():
    """Open the edit dialog."""
    dialog = EditPatchDialog(root, test_program, "program")
    result = dialog.show()
    if result:
        print(f"\n✅ Dialog returned True")
        print(f"   New name: {test_program.name}")
        print(f"   Category: {test_program.category.name}")
        print(f"   Sub-category: {test_program.category.sub_name}")
        print(f"   Favorite: {test_program.favorite}")
    else:
        print(f"\n❌ Dialog was cancelled")

# Add a button to open the dialog
ttk.Label(root, text="Click the button to test the edit dialog", 
          font=('Arial', 14)).pack(pady=20)
ttk.Label(root, text="Check that OK and Cancel buttons are visible at the bottom", 
          font=('Arial', 12)).pack(pady=10)
ttk.Button(root, text="Open Edit Dialog", command=test_dialog, 
           width=20).pack(pady=20)

print("\n✅ Test window created")
print("   Click 'Open Edit Dialog' button to test")
print("   Verify that:")
print("   1. Dialog opens with correct size (450x300)")
print("   2. OK and Cancel buttons are visible at bottom")
print("   3. All fields are editable")
print("   4. Clicking OK saves changes")
print("   5. Clicking Cancel discards changes")

root.mainloop()
