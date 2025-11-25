#!/usr/bin/env python3
"""
Check what names are in SLS1 vs SBK1 in the original file.
"""

import struct
from pathlib import Path

def check_names(pcg_file):
    """Check setlist names in both SLS1 and SBK1."""
    
    with open(pcg_file, 'rb') as f:
        data = f.read()
    
    print(f"Analyzing: {pcg_file}")
    print("=" * 80)
    
    # Find SLS1
    sls1_offset = data.find(b'SLS1')
    if sls1_offset >= 0:
        print(f"\nSLS1 chunk at offset {sls1_offset} (0x{sls1_offset:08X})")
        
        sls1_data_start = sls1_offset + 8
        marker = b'\x1e\x02\x00\x00'
        
        # Find first setlist
        pos = data.find(marker, sls1_data_start)
        if pos > 0:
            name_pos = pos + 4
            name = data[name_pos:name_pos+24].rstrip(b'\x00').decode('ascii', errors='ignore')
            print(f"  First setlist name: '{name}'")
            print(f"  At offset: {name_pos} (0x{name_pos:08X})")
    
    # Find SBK1
    sbk1_offset = data.find(b'SBK1')
    if sbk1_offset >= 0:
        print(f"\nSBK1 chunk at offset {sbk1_offset} (0x{sbk1_offset:08X})")
        
        sbk1_data_start = sbk1_offset + 8
        name_pos = sbk1_data_start + 69432
        
        name = data[name_pos:name_pos+24].rstrip(b'\x00').decode('ascii', errors='ignore')
        print(f"  First setlist name: '{name}'")
        print(f"  At offset: {name_pos} (0x{name_pos:08X})")
    
    print("\n" + "=" * 80)
    print("CONCLUSION:")
    print("If the names are DIFFERENT, that explains the problem!")
    print("The parser reads from SLS1, but writer updates SBK1 with SLS1's name.")
    print("This creates a mismatch that didn't exist before.")
    print("=" * 80)

if __name__ == '__main__':
    test_file = Path('test_files/nw_modified.PCG')
    if test_file.exists():
        check_names(test_file)
    else:
        print(f"File not found: {test_file}")
