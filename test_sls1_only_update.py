#!/usr/bin/env python3
"""
Test updating ONLY SLS1, leaving SBK1 unchanged.
This should work since the original file has mismatched names.
"""

from pathlib import Path
from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import PcgWriter

class SLS1OnlyWriter(PcgWriter):
    """Writer that only updates SLS1, not SBK1."""
    
    def _update_all_setlist_chunks(self, raw_data):
        """Update ONLY SLS1, leave SBK1 alone."""
        if not self.pcg.set_lists:
            return
        
        # Only update SLS1 (new format)
        self._update_sls1_names(raw_data)
        # DO NOT update SBK1!

def test_sls1_only():
    """Test updating only SLS1."""
    
    test_file = Path('test_files/nw_modified.PCG')
    if not test_file.exists():
        print(f"Test file not found: {test_file}")
        return
    
    print("=" * 80)
    print("TEST: Update ONLY SLS1 (Leave SBK1 Unchanged)")
    print("=" * 80)
    
    # Read file
    print(f"\n1. Reading: {test_file}")
    pcg = read_pcg_file(str(test_file))
    
    original_name = pcg.set_lists[0].name
    print(f"   Original name: '{original_name}'")
    
    # Change name
    new_name = "SLS1 ONLY TEST"
    print(f"\n2. Changing name to: '{new_name}'")
    pcg.set_lists[0].name = new_name
    
    # Write with SLS1-only writer
    output_file = Path('test_files/sls1_only_test.PCG')
    print(f"\n3. Writing (SLS1 only): {output_file}")
    
    writer = SLS1OnlyWriter(pcg)
    writer.write(str(output_file))
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
    
    # Check what's in the raw data
    with open(output_file, 'rb') as f:
        data = f.read()
    
    print(f"\n5. Checking raw data:")
    
    # SLS1 at offset 3744
    sls1_name = data[3744:3744+24].rstrip(b'\x00').decode('ascii', errors='ignore')
    print(f"   SLS1 (offset 3744): '{sls1_name}'")
    
    # SBK1 at offset 531920
    sbk1_name = data[531920:531920+24].rstrip(b'\x00').decode('ascii', errors='ignore')
    print(f"   SBK1 (offset 531920): '{sbk1_name}'")
    
    print(f"\n{'=' * 80}")
    print("EXPECTED RESULTS:")
    print(f"  SLS1: '{new_name}' (updated)")
    print(f"  SBK1: 'NIGHTWISH LEGACY' (unchanged)")
    print()
    print("If SBK1 is unchanged, this file should load on Kronos!")
    print("=" * 80)

if __name__ == '__main__':
    test_sls1_only()
