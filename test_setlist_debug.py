#!/usr/bin/env python3
"""Debug setlist parsing."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file

test_file = Path('test_files/files/GLAM V3/GLAMV3.PCG')

print(f"Reading: {test_file}")
pcg = read_pcg_file(str(test_file))

print(f"\nPCG loaded:")
print(f"  Program banks: {len(pcg.program_banks)}")
print(f"  Combi banks: {len(pcg.combi_banks)}")
print(f"  Set lists: {len(pcg.set_lists)}")
print(f"  has_set_lists: {pcg.has_set_lists}")

if pcg.set_lists:
    print(f"\nFirst setlist:")
    sl = pcg.set_lists[0]
    print(f"  Name: '{sl.name}'")
    print(f"  Index: {sl.index}")
    print(f"  Slots: {len(sl.slots)}")
    
    if sl.slots:
        print(f"\nFirst 3 slots:")
        for i, slot in enumerate(sl.slots[:3]):
            print(f"    {i}: '{slot.name}' -> {slot.patch_id} T:{slot.transpose:+d} V:{slot.volume}")
else:
    print("\nNo setlists found!")
    
    # Check if SLS1 chunk exists
    data = pcg.raw_data
    sls1_pos = data.find(b'SLS1')
    if sls1_pos >= 0:
        print(f"\nSLS1 chunk found at offset 0x{sls1_pos:08X}")
        
        # Look for marker pattern
        marker = b'\x1E\x02\x00\x00'
        marker_pos = data.find(marker, sls1_pos)
        if marker_pos >= 0:
            print(f"Marker found at offset 0x{marker_pos:08X}")
            # Try to read a name
            name = data[marker_pos+4:marker_pos+28].split(b'\x00')[0].decode('ascii', errors='ignore')
            print(f"Name at marker: '{name}'")
        else:
            print("No marker pattern found")
    else:
        print("\nNo SLS1 chunk in file!")
