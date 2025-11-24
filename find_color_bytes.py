#!/usr/bin/env python3
"""
Find color bytes by comparing specific slots with known colors.
Slot 0: Burgundy
Slot 1: Olive
Slot 3: Navy
Slot 12: Indigo
"""

import struct

def find_color_bytes(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"Analyzing: {filename}\n")
    
    # Find SLD1
    sld1_pos = data.find(b'SLD1')
    sdb1_pos = data.find(b'SDB1', sld1_pos)
    
    # Find setlist name
    setlist_name_pos = sdb1_pos + 16
    setlist_name = data[setlist_name_pos:setlist_name_pos+24].rstrip(b'\x00').decode('ascii', errors='replace')
    print(f"Setlist: '{setlist_name}'")
    
    # First slot position (after setlist name + separator)
    separator_pos = setlist_name_pos + 24
    first_slot_pos = separator_pos + 4
    
    # Define slots to analyze with their known colors
    slots_to_check = [
        (0, "Ghostbusters", "Burgundy"),
        (1, "Never Ending Story", "Olive"),
        (3, "Top Gun Anthem", "Navy"),
        (12, "A View To A Kill", "Indigo"),
    ]
    
    print("\nExtracting slot data:\n")
    
    slot_data_map = {}
    
    for slot_idx, expected_name, color in slots_to_check:
        # Calculate position
        if slot_idx == 0:
            # First slot has no marker
            pos = first_slot_pos
        else:
            # Subsequent slots have 4-byte marker + 24-byte name
            pos = first_slot_pos + 24 + ((slot_idx - 1) * 28) + 4
        
        # Read name
        name = data[pos:pos+24].rstrip(b'\x00').decode('ascii', errors='replace')
        
        # Read next 128 bytes after name (potential metadata area)
        metadata_start = pos + 24
        metadata = data[metadata_start:metadata_start+128]
        
        slot_data_map[slot_idx] = {
            'name': name,
            'expected_name': expected_name,
            'color': color,
            'position': pos,
            'metadata': metadata
        }
        
        print(f"Slot {slot_idx}: '{name}' (expected: '{expected_name}')")
        print(f"  Position: 0x{pos:08X}")
        print(f"  Color: {color}")
        print(f"  First 64 bytes after name:")
        for i in range(0, 64, 16):
            hex_str = ' '.join(f'{b:02X}' for b in metadata[i:i+16])
            print(f"    +{24+i:3d}: {hex_str}")
        print()
    
    # Compare bytes to find differences
    print("="*80)
    print("COMPARING BYTES TO FIND COLOR INDICATORS")
    print("="*80 + "\n")
    
    # Compare each byte position across all slots
    print("Byte positions that DIFFER between slots (potential color bytes):\n")
    
    for byte_pos in range(64):
        values = {}
        for slot_idx in [0, 1, 3, 12]:
            if byte_pos < len(slot_data_map[slot_idx]['metadata']):
                val = slot_data_map[slot_idx]['metadata'][byte_pos]
                color = slot_data_map[slot_idx]['color']
                if color not in values:
                    values[color] = []
                values[color].append(val)
        
        # Check if values differ
        unique_vals = set()
        for color_vals in values.values():
            unique_vals.update(color_vals)
        
        if len(unique_vals) > 1:
            print(f"Byte +{24 + byte_pos}:")
            for color in ["Burgundy", "Olive", "Navy", "Indigo"]:
                if color in values:
                    val = values[color][0]
                    print(f"  {color:12s}: {val:3d} (0x{val:02X})")
            print()
    
    # Also check if there's a pattern in the gaps between slots
    print("="*80)
    print("CHECKING FOR METADATA AFTER SLOT NAMES SECTION")
    print("="*80 + "\n")
    
    # After all 128 slots, there might be a metadata section
    # Calculate where slots end
    slots_end = first_slot_pos + 24 + (127 * 28)
    
    print(f"All slot names end at: 0x{slots_end:08X}")
    print(f"Checking for metadata arrays after this point...\n")
    
    # Look for 128-byte or 256-byte arrays (one byte per slot for color/size)
    for offset in [0, 128, 256, 512, 1024]:
        check_pos = slots_end + offset
        print(f"At offset +{offset} (0x{check_pos:08X}):")
        
        # Read 128 bytes (one per slot potentially)
        array_data = data[check_pos:check_pos+128]
        
        # Check slots 0, 1, 3, 12
        print(f"  Slot 0 (Burgundy): byte value = {array_data[0]:3d} (0x{array_data[0]:02X})")
        print(f"  Slot 1 (Olive):    byte value = {array_data[1]:3d} (0x{array_data[1]:02X})")
        print(f"  Slot 3 (Navy):     byte value = {array_data[3]:3d} (0x{array_data[3]:02X})")
        print(f"  Slot 12 (Indigo):  byte value = {array_data[12]:3d} (0x{array_data[12]:02X})")
        
        # Check if these values are different
        test_vals = [array_data[0], array_data[1], array_data[3], array_data[12]]
        if len(set(test_vals)) > 1:
            print(f"  *** DIFFERENT VALUES FOUND - This might be the color array! ***")
        print()

if __name__ == '__main__':
    find_color_bytes('test_files/SETLIST Movie TV Themes LOAD SEPARATELY.PCG')
