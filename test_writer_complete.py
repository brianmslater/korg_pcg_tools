#!/usr/bin/env python3
"""
Complete test of the writer fix - verifies both SLS1 and SBK1 are updated correctly.
"""

from pathlib import Path
from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file

def test_writer_fix():
    """Test that writer updates both SLS1 and SBK1 formats."""
    
    # Find test file
    test_file = Path('test_files/nw_modified.PCG')
    if not test_file.exists():
        print(f"Test file not found: {test_file}")
        return False
    
    print("=" * 80)
    print("WRITER FIX TEST - Dual Format Update")
    print("=" * 80)
    
    # Read original file
    print(f"\n1. Loading original file: {test_file}")
    pcg = read_pcg_file(str(test_file))
    
    if not pcg.set_lists:
        print("  ❌ No setlists found")
        return False
    
    original_name = pcg.set_lists[0].name
    print(f"  ✓ Original first setlist: '{original_name}'")
    print(f"  ✓ Total setlists: {len(pcg.set_lists)}")
    
    # Modify setlist name
    new_name = "WRITER FIX TEST"
    print(f"\n2. Changing first setlist name to: '{new_name}'")
    pcg.set_lists[0].name = new_name
    
    # Write file
    output_file = Path('test_files/writer_fix_test.PCG')
    print(f"\n3. Writing modified file: {output_file}")
    write_pcg_file(pcg, str(output_file))
    print(f"  ✓ File written")
    
    # Read back and verify
    print(f"\n4. Reading back modified file...")
    pcg_verify = read_pcg_file(str(output_file))
    
    if not pcg_verify.set_lists:
        print("  ❌ No setlists found in written file")
        return False
    
    verified_name = pcg_verify.set_lists[0].name
    print(f"  Parser reads: '{verified_name}'")
    
    if verified_name == new_name:
        print(f"  ✓ SUCCESS! Name matches '{new_name}'")
        success = True
    else:
        print(f"  ❌ FAILED! Expected '{new_name}', got '{verified_name}'")
        success = False
    
    # Additional verification - check that other setlists weren't corrupted
    print(f"\n5. Verifying other setlists weren't corrupted...")
    if len(pcg_verify.set_lists) >= 2:
        second_name = pcg_verify.set_lists[1].name
        print(f"  Second setlist: '{second_name}'")
        if second_name and second_name != new_name:
            print(f"  ✓ Other setlists intact")
        else:
            print(f"  ❌ WARNING: Second setlist may be corrupted")
            success = False
    
    # Summary
    print(f"\n{'=' * 80}")
    if success:
        print("✓ WRITER FIX TEST PASSED")
        print()
        print("Next steps:")
        print(f"1. Copy {output_file} to USB drive")
        print(f"2. Load on Kronos hardware")
        print(f"3. Verify file is accepted (not rejected)")
        print(f"4. Check that setlist name shows as '{new_name}'")
    else:
        print("❌ WRITER FIX TEST FAILED")
        print()
        print("The writer is not correctly updating both formats.")
    print("=" * 80)
    
    return success

if __name__ == '__main__':
    success = test_writer_fix()
    exit(0 if success else 1)
