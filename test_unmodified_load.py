#!/usr/bin/env python3
"""
Test if an unmodified file (just read and write back) loads on hardware.
This will tell us if the issue is with our modifications or the write process itself.
"""

from pathlib import Path
from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file

def test_unmodified_roundtrip():
    """Read a file and write it back WITHOUT modifications."""
    
    test_file = Path('test_files/nw_modified.PCG')
    if not test_file.exists():
        print(f"Test file not found: {test_file}")
        return
    
    print("=" * 80)
    print("UNMODIFIED ROUNDTRIP TEST")
    print("=" * 80)
    
    # Read file
    print(f"\n1. Reading: {test_file}")
    pcg = read_pcg_file(str(test_file))
    print(f"   ✓ Loaded {len(pcg.set_lists)} setlists")
    
    if pcg.set_lists:
        print(f"   First setlist: '{pcg.set_lists[0].name}'")
    
    # Write back WITHOUT any modifications
    output_file = Path('test_files/unmodified_roundtrip.PCG')
    print(f"\n2. Writing back (NO CHANGES): {output_file}")
    write_pcg_file(pcg, str(output_file))
    print(f"   ✓ File written")
    
    # Verify
    print(f"\n3. Verifying...")
    pcg_verify = read_pcg_file(str(output_file))
    
    if pcg_verify.set_lists:
        verified_name = pcg_verify.set_lists[0].name
        print(f"   First setlist: '{verified_name}'")
        
        if verified_name == pcg.set_lists[0].name:
            print(f"   ✓ Name matches")
        else:
            print(f"   ❌ Name changed!")
    
    # Compare file sizes
    original_size = test_file.stat().st_size
    output_size = output_file.stat().st_size
    
    print(f"\n4. File size comparison:")
    print(f"   Original: {original_size:,} bytes")
    print(f"   Output:   {output_size:,} bytes")
    
    if original_size == output_size:
        print(f"   ✓ Sizes match")
    else:
        diff = output_size - original_size
        print(f"   ❌ Size difference: {diff:+,} bytes")
    
    print(f"\n{'=' * 80}")
    print("CRITICAL TEST:")
    print("Copy test_files/unmodified_roundtrip.PCG to USB drive")
    print("Try loading it on Kronos")
    print()
    print("If this FAILS to load:")
    print("  → The write process itself is corrupting the file")
    print("  → Need to investigate what writer.write() is doing wrong")
    print()
    print("If this LOADS successfully:")
    print("  → The write process is OK")
    print("  → Our modifications are causing the problem")
    print("  → Need to investigate what we're changing incorrectly")
    print("=" * 80)

if __name__ == '__main__':
    test_unmodified_roundtrip()
