#!/usr/bin/env python3
"""Test minimal edit - only change program name, nothing else."""

import sys
import os
from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file


def test_minimal_edit(input_file, output_file):
    """Test editing only the program name."""
    print(f"Testing MINIMAL edit (name only) with: {input_file}")
    print("=" * 80)
    
    # Read the file
    print("\n1. Reading PCG file...")
    pcg = read_pcg_file(input_file)
    print(f"   ✓ File loaded")
    
    # Get first program
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
    
    print(f"   ✓ Found: {test_program.id} - {test_program.name}")
    
    # Make ONLY name change
    print("\n3. Changing ONLY the name...")
    original_name = test_program.name
    test_program.name = "NAME TEST"
    print(f"   ✓ Changed: '{original_name}' -> '{test_program.name}'")
    print(f"   - NOT changing category")
    print(f"   - NOT changing favorite")
    print(f"   - NOT changing anything else")
    
    # Update ONLY the name in raw_data
    print("\n4. Updating raw_data (name only)...")
    if test_program.raw_data and len(test_program.raw_data) >= 24:
        raw_data = bytearray(test_program.raw_data)
        name_bytes = test_program.name.encode('ascii', errors='replace')[:24]
        name_bytes = name_bytes.ljust(24, b'\x00')
        raw_data[0:24] = name_bytes
        test_program.raw_data = bytes(raw_data)
        print(f"   ✓ Name updated in raw_data")
    
    # Save
    print(f"\n5. Saving to: {output_file}")
    write_pcg_file(pcg, output_file)
    print(f"   ✓ File saved")
    
    # Compare
    original_size = os.path.getsize(input_file)
    new_size = os.path.getsize(output_file)
    print(f"\n6. File size check:")
    print(f"   - Original: {original_size:,} bytes")
    print(f"   - New:      {new_size:,} bytes")
    print(f"   - Diff:     {new_size - original_size:+,} bytes")
    
    if original_size == new_size:
        print("   ✓ File size unchanged")
    
    # Count differences
    with open(input_file, 'rb') as f1, open(output_file, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()
    
    diffs = sum(1 for b1, b2 in zip(data1, data2) if b1 != b2)
    print(f"\n7. Binary differences: {diffs} bytes changed")
    print(f"   - Expected: ~24 bytes (just the name)")
    
    if diffs <= 24:
        print("   ✓ Only name changed (as expected)")
    else:
        print(f"   ⚠ More than name changed! ({diffs} bytes)")
    
    print("\n" + "=" * 80)
    print("✅ TEST COMPLETE")
    print("\nCopy to USB and test on hardware:")
    print(f"   File: {output_file}")
    print("=" * 80)


if __name__ == "__main__":
    input_file = "test_files/soundcheck9_25_25_combined2.PCG"
    output_file = "test_files/soundcheck_NAME_ONLY_TEST.PCG"
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    
    test_minimal_edit(input_file, output_file)
