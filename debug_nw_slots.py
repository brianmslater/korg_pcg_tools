#!/usr/bin/env python3
"""Debug the nw.PCG slot names to see what's actually stored."""

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
    
    while pos < len(data) - 32 and len(markers) < 25:
        pos = data.find(marker, pos)
        if pos == -1:
            break
        markers.append(pos + 4)
        pos += 4
    
    print(f"Found {len(markers)} markers\n")
    
    # Check first few slot entries (starting at marker 16)
    for i in range(16, min(20, len(markers))):
        slot_idx = i - 16
        name_offset = markers[i]
        
        # Read full 24-byte name area
        name_bytes = data[name_offset:name_offset+24]
        
        # First 2 bytes are previous slot's patch data
        prev_transpose = name_bytes[0]
        prev_volume = name_bytes[1]
        
        # Full name (including those first 2 bytes)
        full_name = name_bytes.decode('ascii', errors='ignore').rstrip('\x00')
        
        # Name without first 2 bytes
        actual_name = name_bytes[2:].decode('ascii', errors='ignore').rstrip('\x00')
        
        # Show all bytes
        hex_bytes = ' '.join(f'{b:02X}' for b in name_bytes)
        
        print(f"Slot {slot_idx}:")
        print(f"  Offset: {name_offset}")
        print(f"  All bytes: {hex_bytes}")
        print(f"  First 2 bytes: 0x{prev_transpose:02X} 0x{prev_volume:02X} ('{chr(prev_transpose) if 32 <= prev_transpose < 127 else '?'}' '{chr(prev_volume) if 32 <= prev_volume < 127 else '?'}')")
        print(f"  Full name (24 bytes): '{full_name}'")
        print(f"  Actual name (bytes 2-23): '{actual_name}'")
        
        # Decode as transpose/volume
        if slot_idx > 0:
            trans_val = prev_transpose - 0x40
            print(f"  Prev slot patch data: transpose={trans_val:+d}, volume={prev_volume}")
        print()


if __name__ == '__main__':
    debug()
