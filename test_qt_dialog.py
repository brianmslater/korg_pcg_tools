#!/usr/bin/env python3
"""Test the Qt edit dialog."""

import sys
from PySide6.QtWidgets import QApplication
from pcg_tools.reader import read_pcg_file
from pcg_tools.qt_edit_dialog import QtEditPatchDialog


def test_qt_dialog(pcg_file):
    """Test the Qt edit dialog with a real PCG file."""
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
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Show edit dialog
    print("\nOpening Qt edit dialog...")
    dialog = QtEditPatchDialog(None, test_program, "program")
    dialog.exec()
    
    if dialog.get_result():
        print("\nUser clicked OK")
        print(f"Modified Program:")
        print(f"  ID: {test_program.id}")
        print(f"  Name: {test_program.name}")
        print(f"  Category: {test_program.category.main_category if test_program.category else 'None'}")
        print(f"  SubCategory: {test_program.category.sub_category if test_program.category else 'None'}")
        print(f"  Favorite: {test_program.favorite}")
        print("\n✅ Qt dialog works!")
    else:
        print("\nUser clicked Cancel")
        print("✅ Qt dialog works (cancel tested)!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_qt_dialog.py <pcg_file>")
        sys.exit(1)
    
    test_qt_dialog(sys.argv[1])
