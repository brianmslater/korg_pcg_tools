#!/usr/bin/env python3
"""Analyze SLD1 slot structure in detail."""

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
        if offset+i >= len(data):
            break
        hex_str = ' '.join(f'{b:02X}' for b in data[offset+i:offset+i+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset+i:offset+i+16])
        print(f"  {offset+i:08X}: {hex_str:<48} {ascii_str}")

def analyze_sld1_slots(filename):
    """Analyze SLD1 slot structure."""
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Find first CBK1
    cbk1_pos = data.find(b'CBK1')
    if cbk1_pos < 0:
        print("No CBK1 found")
        return
    
    print(f"First CBK1 at 0x{cbk1_pos:08X}\n")
    
    SLOT_SIZE = 7810  # 0x1E82
    
    # Analyze first 5 slots
    for slot_idx in range(5):
        slot_offset = cbk1_pos + (slot_idx * SLOT_SIZE)
        
        print(f"=== SLOT {slot_idx} at 0x{slot_offset:08X} ===")
        
        # Check for CBK1 marker (only slot 0 has it)
        if slot_idx == 0:
            marker = data[slot_offset:slot_offset+4]
            print(f"Marker: {marker}")
            size = struct.unpack('<I', data[slot_offset+4:slot_offset+8])[0]
            print(f"Size: 0x{size:08X}")
            name_offset = 24
        else:
            # No marker, name is at different offset
            # Let's search for readable text
            name_offset = None
            for test_offset in [0, 4, 8, 12, 16, 20, 24, 28, 32]:
                test_name = get_string(data, slot_offset + test_offset, 24)
                if test_name and len(test_name) >= 5 and test_name.isprintable():
                    name_offset = test_offset
                    break
        
        if name_offset is not None:
            slot_name = get_string(data, slot_offset + name_offset, 24)
            print(f"Name at +{name_offset}: '{slot_name}'")
            
            # Show hex dump around the name
            hex_dump(data, slot_offset + name_offset, 48, "Name area")
            
            # Try to find patch reference data
            # In STL1 it's at name+24, name+25, name+26
            # Let's check the same in SLD1
            patch_area_offset = slot_offset + name_offset + 24
            print(f"\nBytes after name (+{name_offset+24} to +{name_offset+35}):")
            for i in range(12):
                byte_val = data[patch_area_offset + i]
                print(f"  +{name_offset+24+i}: 0x{byte_val:02X} ({byte_val:3d})")
        
        print()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    
    analyze_sld1_slots(filename)
