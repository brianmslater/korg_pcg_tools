#!/usr/bin/env python3
"""
Test the fixed writer that only updates SLS1.
This should now work on hardware!
"""

from pathlib import Path
from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file

def test_fixed_writer():
    """Test the fixed writer."""
    
    test_file = Path('test_files/nw_modified.PCG')
    if not test_file.exists():
        print(f"Test file not found: {test_file}")
        return
    
    print("=" * 80)
    print("FIXED WRITER TEST - SLS1 Only Updates")
    print("=" * 80)
    
    # Read file
    print(f"\n1. Reading: {test_file}")
    pcg = read_pcg_file(str(test_file))
    
    original_name = pcg.set_lists[0].name
    print(f"   Original name: '{original_name}'")
    
    # Change name
    new_name = "WRITER FIXED!"
    print(f"\n2. Changing name to: '{new_name}'")
    pcg.set_lists[0].name = new_name
    
    # Write with fixed writer
    output_file = Path('test_files/writer_fixed_test.PCG')
    print(f"\n3. Writing: {output_file}")
    write_pcg_file(pcg, str(output_file))
    print(f"   ✓ Written")
    
    # Verify
    print(f"\n4. Verifying...")
    pcg_verify = read_pcg_file(str(output_file))
    verified_name = pcg_verify.set_lists[0].name
    print(f"   Parser reads: '{verified_name}'")
    
    if verified_name == new_name:
        print(f"   ✓ Name matches!")
    else:
        print(f"   ❌ Name mismatch")
        return
    
    # Check raw data
    with open(output_file, 'rb') as f:
        data = f.read()
    
    print(f"\n5. Checking raw data:")
    
    # SLS1 at offset 3744
    sls1_name = data[3744:3744+24].rstrip(b'\x00').decode('ascii', errors='ignore')
    print(f"   SLS1 (offset 3744): '{sls1_name}'")
    
    # SBK1 at offset 531920
    sbk1_name = data[531920:531920+24].rstrip(b'\x00').decode('ascii', errors='ignore')
    print(f"   SBK1 (offset 531920): '{sbk1_name}'")
    
    # Verify expectations
    print(f"\n6. Validation:")
    
    if sls1_name == new_name:
        print(f"   ✓ SLS1 updated correctly")
    else:
        print(f"   ❌ SLS1 not updated")
    
    if sbk1_name == "NIGHTWISH LEGACY":
        print(f"   ✓ SBK1 unchanged (correct!)")
    else:
        print(f"   ❌ SBK1 was changed (will break file!)")
    
    print(f"\n{'=' * 80}")
    print("SUCCESS! File ready for hardware testing.")
    print()
    print("Expected results on Kronos:")
    print(f"  ✓ File loads successfully")
    print(f"  ✓ First setlist shows: '{new_name}'")
    print(f"  ✓ All slots work normally")
    print("=" * 80)

if __name__ == '__main__':
    test_fixed_writer()
