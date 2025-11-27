#!/usr/bin/env python3
"""Test script for programmatic editing (no GUI)."""

from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file
from pcg_tools.models import Category
import sys


def test_programmatic_edit(pcg_file):
    """Test programmatic editing of patches."""
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
    
    print(f"\n{'='*60}")
    print("BEFORE EDITING")
    print(f"{'='*60}")
    print(f"ID: {test_program.id}")
    print(f"Name: {test_program.name}")
    print(f"Category: {test_program.category.main_category if test_program.category else 'None'}")
    print(f"SubCategory: {test_program.category.sub_category if test_program.category else 'None'}")
    print(f"Favorite: {test_program.favorite}")
    print(f"Engine: {test_program.engine}")
    print(f"OSC Mode: {test_program.osc_mode}")
    
    # Make changes
    print(f"\n{'='*60}")
    print("MAKING CHANGES")
    print(f"{'='*60}")
    
    # Change name
    old_name = test_program.name
    test_program.name = "TEST EDITED PROGRAM"
    print(f"Changed name: '{old_name}' -> '{test_program.name}'")
    
    # Change category
    old_cat = test_program.category.main_category if test_program.category else 0
    old_subcat = test_program.category.sub_category if test_program.category else 0
    
    if not test_program.category:
        test_program.category = Category(main_category=0, sub_category=0)
    
    test_program.category.main_category = 7  # Synth Lead
    test_program.category.sub_category = 1  # Digital Lead
    print(f"Changed category: {old_cat} -> {test_program.category.main_category}")
    print(f"Changed subcategory: {old_subcat} -> {test_program.category.sub_category}")
    
    # Toggle favorite
    test_program.favorite = not test_program.favorite
    print(f"Toggled favorite: {not test_program.favorite} -> {test_program.favorite}")
    
    # Update raw data
    print("\nUpdating raw data...")
    _update_program_raw_data(test_program)
    
    print(f"\n{'='*60}")
    print("AFTER EDITING")
    print(f"{'='*60}")
    print(f"ID: {test_program.id}")
    print(f"Name: {test_program.name}")
    print(f"Category: {test_program.category.main_category}")
    print(f"SubCategory: {test_program.category.sub_category}")
    print(f"Favorite: {test_program.favorite}")
    
    # Save to new file
    output_file = pcg_file.replace('.PCG', '_test_edited.PCG')
    print(f"\nSaving to: {output_file}")
    write_pcg_file(pcg, output_file)
    print("Saved successfully!")
    
    # Verify by re-reading
    print(f"\n{'='*60}")
    print("VERIFICATION (re-reading saved file)")
    print(f"{'='*60}")
    pcg2 = read_pcg_file(output_file)
    programs2 = pcg2.get_all_programs()
    test_program2 = programs2[test_program.index]
    
    print(f"ID: {test_program2.id}")
    print(f"Name: {test_program2.name}")
    print(f"Category: {test_program2.category.main_category if test_program2.category else 'None'}")
    print(f"SubCategory: {test_program2.category.sub_category if test_program2.category else 'None'}")
    print(f"Favorite: {test_program2.favorite}")
    
    # Check if changes persisted
    success = True
    if test_program2.name != "TEST EDITED PROGRAM":
        print("❌ Name change did NOT persist!")
        success = False
    else:
        print("✅ Name change persisted")
    
    if test_program2.category.main_category != 7:
        print("❌ Category change did NOT persist!")
        success = False
    else:
        print("✅ Category change persisted")
    
    if test_program2.category.sub_category != 1:
        print("❌ SubCategory change did NOT persist!")
        success = False
    else:
        print("✅ SubCategory change persisted")
    
    if test_program2.favorite != test_program.favorite:
        print("❌ Favorite change did NOT persist!")
        success = False
    else:
        print("✅ Favorite change persisted")
    
    if success:
        print(f"\n{'='*60}")
        print("✅ ALL TESTS PASSED!")
        print(f"{'='*60}")
    else:
        print(f"\n{'='*60}")
        print("❌ SOME TESTS FAILED!")
        print(f"{'='*60}")


def _update_program_raw_data(program):
    """Update program raw data with changes."""
    if not program.raw_data:
        return
    
    raw_data = bytearray(program.raw_data)
    
    # Update name (offset 0, 24 bytes)
    if len(raw_data) >= 24:
        name_bytes = program.name.encode('ascii', errors='replace')[:24]
        name_bytes = name_bytes.ljust(24, b'\x00')
        raw_data[0:24] = name_bytes
    
    # Update category/subcategory (offset 2568)
    if len(raw_data) >= 2569 and program.category:
        cat_byte = 0
        cat_byte |= (program.category.main_category & 0x1F)
        cat_byte |= ((program.category.sub_category & 0x07) << 5)
        raw_data[2568] = cat_byte
    
    # Update favorite (offset 2558, bit 5)
    if len(raw_data) >= 2559:
        if program.favorite:
            raw_data[2558] |= 0x20
        else:
            raw_data[2558] &= ~0x20
    
    program.raw_data = bytes(raw_data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_edit_programmatic.py <pcg_file>")
        sys.exit(1)
    
    test_programmatic_edit(sys.argv[1])
