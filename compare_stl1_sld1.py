#!/usr/bin/env python3
"""Compare STL1 and SLD1 formats to understand the differences."""

import struct

def get_string(data, offset, length):
    """Read null-terminated ASCII string."""
    string_data = data[offset:offset+length]
    null_pos = string_data.find(b'\x00')
    if null_pos >= 0:
        string_data = string_data[:null_pos]
    return string_data.decode('ascii', errors='ignore').strip()

def hex_dump(data, offset, length, label=""):
    """Print hex dump of data."""
    if label:
        print(f"{label}:")
    for i in range(0, length, 16):
        hex_str = ' '.join(f'{b:02X}' for b in data[offset+i:offset+i+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset+i:offset+i+16])
        print(f"  {offset+i:08X}: {hex_str:<48} {ascii_str}")

def compare_formats(filename):
    """Compare STL1 and SLD1 slot structures."""
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Find STL1
    stl1_pos = data.find(b'STL1')
    if stl1_pos >= 0:
        print(f"STL1 found at 0x{stl1_pos:08X}")
        sbk1_pos = data.find(b'SBK1', stl1_pos)
        if sbk1_pos >= 0:
            print(f"SBK1 found at 0x{sbk1_pos:08X}")
            
            # First slot in STL1 is at SBK1 + 8 + 40
            stl1_slot0 = sbk1_pos + 8 + 40
            slot_name = get_string(data, stl1_slot0, 24)
            print(f"\nSTL1 Slot 0: '{slot_name}'")
            hex_dump(data, stl1_slot0, 64, "First 64 bytes")
            
            # Show bytes at known offsets
            print(f"\nSTL1 Slot 0 structure:")
            print(f"  +0-23: Name = '{slot_name}'")
            print(f"  +24: Color = {data[stl1_slot0+24]}")
            print(f"  +25: Bank = 0x{data[stl1_slot0+25]:02X}")
            print(f"  +26: Index = {data[stl1_slot0+26]}")
            print(f"  +27: ? = 0x{data[stl1_slot0+27]:02X}")
            print(f"  +28: Volume = {data[stl1_slot0+28]}")
            print(f"  +29: Text Size = {data[stl1_slot0+29]}")
    
    print("\n" + "="*80 + "\n")
    
    # Find SLD1
    sld1_pos = data.find(b'SLD1')
    if sld1_pos >= 0:
        print(f"SLD1 found at 0x{sld1_pos:08X}")
        
        # Find first CBK1
        cbk1_pos = data.find(b'CBK1', sld1_pos)
        if cbk1_pos >= 0:
            print(f"First CBK1 found at 0x{cbk1_pos:08X}")
            
            # First slot in SLD1 is at CBK1 + 0 (CBK1 IS the slot)
            sld1_slot0 = cbk1_pos
            slot_name = get_string(data, sld1_slot0 + 24, 24)
            print(f"\nSLD1 Slot 0: '{slot_name}'")
            hex_dump(data, sld1_slot0, 64, "First 64 bytes")
            
            # Show bytes at various offsets
            print(f"\nSLD1 Slot 0 structure:")
            print(f"  +0-3: 'CBK1' marker")
            print(f"  +4-7: Size")
            print(f"  +8-23: Header?")
            print(f"  +24-47: Name = '{slot_name}'")
            print(f"  +48: 0x{data[sld1_slot0+48]:02X}")
            print(f"  +49: 0x{data[sld1_slot0+49]:02X}")
            print(f"  +50: 0x{data[sld1_slot0+50]:02X}")
            print(f"  +51: 0x{data[sld1_slot0+51]:02X}")
            print(f"  +52: 0x{data[sld1_slot0+52]:02X}")
            print(f"  +53: 0x{data[sld1_slot0+53]:02X}")
            
            # Try second slot
            SLOT_SIZE = 7810
            sld1_slot1 = sld1_slot0 + SLOT_SIZE
            slot_name = get_string(data, sld1_slot1 + 24, 24)
            print(f"\nSLD1 Slot 1: '{slot_name}'")
            hex_dump(data, sld1_slot1, 64, "First 64 bytes")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    
    compare_formats(filename)
