#!/usr/bin/env python3
"""Search for color data in SLD1 combi structures."""

import struct

def hex_dump(data, offset, length, label=""):
    """Print hex dump."""
    if label:
        print(f"{label}:")
    for i in range(0, length, 16):
        if offset+i >= len(data):
            break
        hex_str = ' '.join(f'{b:02X}' for b in data[offset+i:offset+i+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset+i:offset+i+16])
        print(f"  {offset+i:08X}: {hex_str:<48} {ascii_str}")

def get_string(data, offset, length):
    """Read null-terminated ASCII string."""
    string_data = data[offset:offset+length]
    null_pos = string_data.find(b'\x00')
    if null_pos >= 0:
        string_data = string_data[:null_pos]
    return string_data.decode('ascii', errors='ignore').strip()

def find_sld1_colors(filename):
    """Search for color data in SLD1."""
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"Analyzing: {filename}\n")
    
    # Find SLD1
    sld1_pos = data.find(b'SLD1')
    if sld1_pos < 0:
        print("No SLD1 found")
        return
    
    print(f"SLD1 at 0x{sld1_pos:08X}\n")
    
    # Find all CBK1 markers
    cbk1_positions = []
    search_pos = sld1_pos
    for i in range(16):
        cbk1_pos = data.find(b'CBK1', search_pos)
        if cbk1_pos < 0:
            break
        cbk1_positions.append(cbk1_pos)
        search_pos = cbk1_pos + 4
    
    print(f"Found {len(cbk1_positions)} CBK1 markers (setlists)\n")
    
    # Analyze SC 10/4 setlist (index 4)
    if len(cbk1_positions) <= 4:
        print("SC 10/4 setlist not found")
        return
    
    sc_start = cbk1_positions[4]
    print(f"SC 10/4 setlist at 0x{sc_start:08X}\n")
    
    SLOT_SIZE = 7810  # 0x1E82
    
    # Analyze first few slots in detail
    print("="*80)
    print("ANALYZING FIRST 3 SLOTS FOR COLOR DATA")
    print("="*80)
    
    for slot_idx in range(3):
        slot_offset = sc_start + (slot_idx * SLOT_SIZE)
        name_offset = slot_offset + 24
        
        slot_name = get_string(data, name_offset, 24)
        print(f"\nSlot {slot_idx}: '{slot_name}'")
        print(f"Offset: 0x{slot_offset:08X}")
        
        # Show first 128 bytes of slot data
        print(f"\nFirst 128 bytes:")
        hex_dump(data, slot_offset, 128)
        
        # Look for non-zero bytes that might be color
        print(f"\nSearching for potential color bytes (non-zero, < 256):")
        for i in range(0, 200):
            byte_val = data[slot_offset + i]
            if byte_val > 0 and byte_val < 256:
                # Check if it's in a reasonable range for color values
                if byte_val in [136, 137, 140, 144, 148, 152, 153, 156, 157, 160, 164, 165, 168, 172, 174, 176, 180, 181, 184, 188, 196]:
                    print(f"  +{i:3d}: 0x{byte_val:02X} ({byte_val:3d}) *** POSSIBLE COLOR ***")
    
    # Compare with a known colored slot from STL1 if available
    print("\n" + "="*80)
    print("COMPARING WITH STL1 FORMAT (if available)")
    print("="*80)
    
    stl1_pos = data.find(b'STL1')
    if stl1_pos >= 0:
        sbk1_pos = data.find(b'SBK1', stl1_pos)
        if sbk1_pos >= 0:
            stl1_slot0 = sbk1_pos + 8 + 40
            stl1_name = get_string(data, stl1_slot0, 24)
            stl1_color = data[stl1_slot0 + 24]
            stl1_size = data[stl1_slot0 + 29]
            
            print(f"\nSTL1 First slot: '{stl1_name}'")
            print(f"  Color at +24: {stl1_color}")
            print(f"  Size at +29: {stl1_size}")
            print(f"\nSTL1 slot structure:")
            hex_dump(data, stl1_slot0, 64)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'test_files/soundcheck9_25_25_combined2.PCG'
    
    find_sld1_colors(filename)
