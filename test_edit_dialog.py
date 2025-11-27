#!/usr/bin/env python3
"""Test script for edit dialog functionality."""

import tkinter as tk
from pcg_tools.reader import read_pcg_file
from pcg_tools.edit_dialog import EditPatchDialog
from pcg_tools.writer import write_pcg_file
import sys


def test_edit_dialog(pcg_file):
    """Test the edit dialog with a real PCG file."""
    print(f"Loading PCG file: {pcg_file}")
    
    # Load PCG file
    pcg = read_pcg_file(pcg_file)
    
    # Get first non-empty program
    programs = pcg.get_all_programs()
    test_program = None
    for prog in programs:
        if prog.name and not prog.name.startswith("[Empty"):
            test_program = prog
            break
    
    if not test_program:
        print("No programs found in file")
        return
    
    print(f"\nOriginal Program:")
    print(f"  ID: {test_program.id}")
    print(f"  Name: {test_program.name}")
    print(f"  Category: {test_program.category.main_category if test_program.category else 'None'}")
    print(f"  SubCategory: {test_program.category.sub_category if test_program.category else 'None'}")
    print(f"  Favorite: {test_program.favorite}")
    
    # Create root window (hidden)
    root = tk.Tk()
    root.withdraw()
    
    # Show edit dialog
    print("\nOpening edit dialog...")
    dialog = EditPatchDialog(root, test_program, "program")
    result = dialog.show()
    
    if result:
        print("\nUser clicked OK")
        print(f"Modified Program:")
        print(f"  ID: {test_program.id}")
        print(f"  Name: {test_program.name}")
        print(f"  Category: {test_program.category.main_category if test_program.category else 'None'}")
        print(f"  SubCategory: {test_program.category.sub_category if test_program.category else 'None'}")
        print(f"  Favorite: {test_program.favorite}")
        
        # Ask if user wants to save
        save_dialog = tk.messagebox.askyesno(
            "Save Changes",
            "Do you want to save the changes to a new file?",
            parent=root
        )
        
        if save_dialog:
            output_file = pcg_file.replace('.PCG', '_edited.PCG')
            print(f"\nSaving to: {output_file}")
            write_pcg_file(pcg, output_file)
            print("Saved successfully!")
    else:
        print("\nUser clicked Cancel")
    
    root.destroy()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_edit_dialog.py <pcg_file>")
        sys.exit(1)
    
    test_edit_dialog(sys.argv[1])
