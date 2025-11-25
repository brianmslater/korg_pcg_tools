#!/usr/bin/env python3
"""Debug the nw.PCG setlist names."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def debug():
    nw_file = '/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG'
    
    with open(nw_file, 'rb') as f:
        data = f.read()
    
    # Find SLS1
    sls1_offset = data.find(b'SLS1')
    print(f"SLS1 at offset: {sls1_offset}")
    
    # Find markers
    marker = b'\x1E\x02\x00\x00'
    markers = []
    pos = sls1_offset + 8
    
    while pos < len(data) - 32 and len(markers) < 20:
        pos = data.find(marker, pos)
        if pos == -1:
            break
        markers.append(pos + 4)
        pos += 4
    
    print(f"Found {len(markers)} markers\n")
    
    # First 16 markers should be setlist names
    print("SETLIST NAMES (first 16 entries):")
    for i in range(min(16, len(markers))):
        name_offset = markers[i]
        name_bytes = data[name_offset:name_offset+24]
        name = name_bytes.decode('ascii', errors='ignore').rstrip('\x00')
        hex_bytes = ' '.join(f'{b:02X}' for b in name_bytes[:12])
        
        print(f"Setlist {i}:")
        print(f"  Offset: {name_offset}")
        print(f"  First 12 bytes: {hex_bytes}")
        print(f"  Name: '{name}'")
        print()


if __name__ == '__main__':
    debug()
