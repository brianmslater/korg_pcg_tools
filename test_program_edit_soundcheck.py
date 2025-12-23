#!/usr/bin/env python3
"""Test program editing with soundcheck file - verify hardware compatibility.

This is a standalone script, not a pytest test.
Run with: python test_program_edit_soundcheck.py <input_file> <output_file>
"""

import pytest
import sys
import os
from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file
from pcg_tools.models import Category


@pytest.mark.skip(reason="Standalone script - requires command line arguments")
def test_program_edit(input_file=None, output_file=None):
    """Test editing a program and verify file integrity."""
    print(f"Testing program edit with: {input_file}")
    print("=" * 80)
    
    # Read the file
    print("\n1. Reading PCG file...")
    pcg = read_pcg_file(input_file)
    print(f"   ✓ File loaded successfully")
    print(f"   - Program banks: {len(pcg.program_banks)}")
    print(f"   - Combi banks: {len(pcg.combi_banks)}")
    print(f"   - Set lists: {len(pcg.set_lists)}")
    
    # Get first non-empty program
    print("\n2. Finding first program...")
    programs = pcg.get_all_programs()
    test_program = None
    for prog in programs:
        if prog.name and not prog.name.startswith("[Empty"):
            test_program = prog
            break
    
    if not test_program:
        print("   ✗ No programs found!")
        return False
    
    print(f"   ✓ Found program: {test_program.id} - {test_program.name}")
    print(f"   - Category: {test_program.category.main_category if test_program.category else 'None'}")
    print(f"   - SubCategory: {test_program.category.sub_category if test_program.category else 'None'}")
    print(f"   - Favorite: {test_program.favorite}")
    print(f"   - Raw data length: {len(test_program.raw_data)}")
    print(f"   - Has offset: {hasattr(test_program, '_raw_offset')}")
    
    # Make a small change
    print("\n3. Making changes...")
    original_name = test_program.name
    original_cat = test_program.category.main_category if test_program.category else 0
    original_fav = test_program.favorite
    
    test_program.name = "TEST EDIT"
    if not test_program.category:
        test_program.category = Category(main_category=0, sub_category=0)
    test_program.category.main_category = 7  # Synth Lead
    test_program.favorite = True
    
    print(f"   ✓ Changed name: '{original_name}' -> '{test_program.name}'")
    print(f"   ✓ Changed category: {original_cat} -> {test_program.category.main_category}")
    print(f"   ✓ Changed favorite: {original_fav} -> {test_program.favorite}")
    
    # Update raw_data
    print("\n4. Updating raw_data...")
    _update_program_raw_data(test_program)
    print(f"   ✓ Raw data updated")
    print(f"   - Raw data length: {len(test_program.raw_data)} (should be 4960)")
    
    # Save the file
    print(f"\n5. Saving to: {output_file}")
    write_pcg_file(pcg, output_file)
    print(f"   ✓ File saved")
    
    # Verify by re-reading
    print("\n6. Verifying changes...")
    pcg2 = read_pcg_file(output_file)
    programs2 = pcg2.get_all_programs()
    test_program2 = programs2[test_program.index]
    
    print(f"   - Name: {test_program2.name}")
    print(f"   - Category: {test_program2.category.main_category if test_program2.category else 'None'}")
    print(f"   - Favorite: {test_program2.favorite}")
    
    # Check if changes persisted
    success = True
    if test_program2.name != "TEST EDIT":
        print("   ✗ Name did NOT persist!")
        success = False
    else:
        print("   ✓ Name persisted")
    
    if test_program2.category.main_category != 7:
        print("   ✗ Category did NOT persist!")
        success = False
    else:
        print("   ✓ Category persisted")
    
    if test_program2.favorite != True:
        print("   ✗ Favorite did NOT persist!")
        success = False
    else:
        print("   ✓ Favorite persisted")
    
    # Compare file sizes
    original_size = os.path.getsize(input_file)
    new_size = os.path.getsize(output_file)
    print(f"\n7. File size check:")
    print(f"   - Original: {original_size:,} bytes")
    print(f"   - New:      {new_size:,} bytes")
    print(f"   - Diff:     {new_size - original_size:+,} bytes")
    
    if original_size != new_size:
        print("   ⚠ File size changed! This might indicate corruption.")
    else:
        print("   ✓ File size unchanged")
    
    print("\n" + "=" * 80)
    if success:
        print("✅ TEST PASSED - Changes persisted correctly")
        print("\nNow test on hardware:")
        print(f"1. Copy {output_file} to USB drive")
        print("2. Load on Kronos")
        print("3. Check if file loads without 'File Unavailable' error")
    else:
        print("❌ TEST FAILED - Changes did not persist")
    print("=" * 80)
    
    return success


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
    input_file = "files_2_test/soundcheck9_25_25_combined2.PCG"
    output_file = "files_2_test/soundcheck_PROGRAM_EDIT_TEST.PCG"
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    
    test_program_edit(input_file, output_file)
