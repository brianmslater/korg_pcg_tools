#!/usr/bin/env python3
"""Directly read color/size from STL1/SBK1 chunk."""

import struct

def test_direct():
    filename = 'SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"File size: {len(data):,} bytes\n")
    
    # Find STL1
    stl1_pos = data.find(b'STL1')
    print(f"STL1 at: 0x{stl1_pos:08X}")
    
    # Find SBK1
    sbk1_pos = data.find(b'SBK1', stl1_pos)
    print(f"SBK1 at: 0x{sbk1_pos:08X}")
    
    # SBK1 data starts at +8
    sbk1_data = sbk1_pos + 8
    
    # Setlist name at +16
    setlist_name_pos = sbk1_data + 16
    setlist_name = data[setlist_name_pos:setlist_name_pos+24].rstrip(b'\x00').decode('ascii')
    print(f"Setlist name: '{setlist_name}'")
    
    # First slot at +40
    slot0_pos = sbk1_data + 40
    slot0_name = data[slot0_pos:slot0_pos+24].rstrip(b'\x00').decode('ascii')
    print(f"\nSlot 0 name: '{slot0_name}'")
    
    # Color at +24 from slot name
    color_pos = slot0_pos + 24
    color = data[color_pos]
    print(f"  Color byte (+24): {color} (0x{color:02X})")
    
    # Text size at +29 from slot name
    size_pos = slot0_pos + 29
    text_size = data[size_pos]
    print(f"  Text size byte (+29): {text_size} (0x{text_size:02X})")
    
    print(f"\nExpected: Indigo (32), XL (16)")
    print(f"Match: Color={'YES' if color == 32 else 'NO'}, Size={'YES' if text_size == 16 else 'NO'}")

if __name__ == '__main__':
    test_direct()
