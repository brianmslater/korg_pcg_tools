#!/usr/bin/env python3
"""Analyze pattern of color data in SLD1 slots."""

def get_string(data, offset, length):
    """Read null-terminated ASCII string."""
    string_data = data[offset:offset+length]
    null_pos = string_data.find(b'\x00')
    if null_pos >= 0:
        string_data = string_data[:null_pos]
    return string_data.decode('ascii', errors='ignore').strip()

def analyze_color_pattern(filename):
    """Analyze color pattern in SLD1 slots."""
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Known color values from our color map
    KNOWN_COLORS = {
        0: "Default",
        136: "Brick", 137: "Brick",
        140: "Burgundy",
        144: "Ivy",
        148: "Olive",
        152: "Gold", 153: "Gold",
        156: "Cacao", 157: "Cacao",
        160: "Indigo",
        164: "Navy", 165: "Navy",
        168: "Rose",
        172: "Lavender", 174: "Lavender",
        176: "Azure",
        180: "Denim", 181: "Denim",
        184: "Silver",
        188: "Slate",
        196: "Charcoal",
    }
    
    # Find SLD1
    sld1_pos = data.find(b'SLD1')
    
    # Find CBK1 markers
    cbk1_positions = []
    search_pos = sld1_pos
    for i in range(16):
        cbk1_pos = data.find(b'CBK1', search_pos)
        if cbk1_pos < 0:
            break
        cbk1_positions.append(cbk1_pos)
        search_pos = cbk1_pos + 4
    
    # SC 10/4 is index 4
    if len(cbk1_positions) <= 4:
        print("SC 10/4 not found")
        return
    
    sc_start = cbk1_positions[4]
    SLOT_SIZE = 7810
    
    print("Analyzing SC 10/4 setlist for color patterns")
    print("="*80)
    
    # Check first 20 non-empty slots
    print("\nChecking offsets +48 to +60 for each slot:")
    print("(These are the bytes after the 24-byte name)")
    print()
    
    slot_count = 0
    for slot_idx in range(128):
        slot_offset = sc_start + (slot_idx * SLOT_SIZE)
        name_offset = slot_offset + 24
        
        slot_name = get_string(data, name_offset, 24)
        if not slot_name or len(slot_name) < 3:
            continue
        
        # Check bytes after name
        found_colors = []
        for i in range(48, 80):  # Extended range
            byte_val = data[slot_offset + i]
            if byte_val in KNOWN_COLORS:
                found_colors.append((i, byte_val, KNOWN_COLORS[byte_val]))
        
        if found_colors:
            print(f"Slot {slot_idx:3d}: '{slot_name}'")
            for offset, val, color_name in found_colors:
                print(f"         +{offset}: 0x{val:02X} ({val:3d}) = {color_name}")
        
        slot_count += 1
        if slot_count >= 20:
            break
    
    # Also check a different setlist for comparison
    print("\n" + "="*80)
    print("Comparing with NIGHTWISH LEGACY setlist (index 0)")
    print("="*80)
    
    nw_start = cbk1_positions[0]
    
    print("\nFirst 10 slots:")
    for slot_idx in range(10):
        slot_offset = nw_start + (slot_idx * SLOT_SIZE)
        name_offset = slot_offset + 24
        
        slot_name = get_string(data, name_offset, 24)
        if not slot_name:
            continue
        
        # Check bytes after name
        found_colors = []
        for i in range(48, 80):
            byte_val = data[slot_offset + i]
            if byte_val in KNOWN_COLORS:
                found_colors.append((i, byte_val, KNOWN_COLORS[byte_val]))
        
        if found_colors:
            print(f"Slot {slot_idx:3d}: '{slot_name}'")
            for offset, val, color_name in found_colors:
                print(f"         +{offset}: 0x{val:02X} ({val:3d}) = {color_name}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'test_files/soundcheck9_25_25_combined2.PCG'
    
    analyze_color_pattern(filename)
