#!/usr/bin/env python3
"""Test roundtrip without any edits - just read and write."""

import sys
import os
from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file


def test_roundtrip(input_file, output_file):
    """Test reading and writing without any edits."""
    print(f"Testing roundtrip (no edits) with: {input_file}")
    print("=" * 80)
    
    # Read the file
    print("\n1. Reading PCG file...")
    pcg = read_pcg_file(input_file)
    print(f"   ✓ File loaded")
    
    # DON'T make any changes - just write it back
    print("\n2. Writing file (NO EDITS)...")
    write_pcg_file(pcg, output_file)
    print(f"   ✓ File saved to: {output_file}")
    
    # Compare file sizes
    original_size = os.path.getsize(input_file)
    new_size = os.path.getsize(output_file)
    print(f"\n3. File size check:")
    print(f"   - Original: {original_size:,} bytes")
    print(f"   - New:      {new_size:,} bytes")
    print(f"   - Diff:     {new_size - original_size:+,} bytes")
    
    if original_size != new_size:
        print("   ⚠ File size changed!")
    else:
        print("   ✓ File size unchanged")
    
    # Binary compare
    print(f"\n4. Binary comparison...")
    with open(input_file, 'rb') as f1, open(output_file, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()
    
    if data1 == data2:
        print("   ✓ Files are IDENTICAL (byte-for-byte)")
    else:
        print("   ⚠ Files are DIFFERENT")
        # Find first difference
        for i, (b1, b2) in enumerate(zip(data1, data2)):
            if b1 != b2:
                print(f"   - First diff at byte {i:,} (0x{i:08X})")
                print(f"   - Original: 0x{b1:02X}, New: 0x{b2:02X}")
                break
    
    print("\n" + "=" * 80)
    print("Test on hardware:")
    print(f"1. Copy {output_file} to USB")
    print("2. Load on Kronos")
    print("3. If it loads, the writer is OK")
    print("4. If it fails, the writer itself is corrupting files")
    print("=" * 80)


if __name__ == "__main__":
    input_file = "test_files/soundcheck9_25_25_combined2.PCG"
    output_file = "test_files/soundcheck_ROUNDTRIP_NO_EDIT.PCG"
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    
    test_roundtrip(input_file, output_file)
