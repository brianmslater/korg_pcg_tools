#!/usr/bin/env python3
"""Search for font size metadata in slot data."""

from pathlib import Path

test_file = '/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG'

with open(test_file, 'rb') as f:
    data = f.read()

# Find the first slot in SLD1
slot0_name_pos = data.find(b'SLEEPING INTRO')
print(f"Slot 0 name at: 0x{slot0_name_pos:08X}")

# The slot entry is 7810 bytes (0x1E82)
# Name is at offset +24 from slot start
slot0_start = slot0_name_pos - 24
print(f"Slot 0 start at: 0x{slot0_start:08X}")

# Look at the entire slot structure
print(f"\nSlot 0 structure (first 128 bytes):")
for i in range(0, 128, 16):
    offset = slot0_start + i
    hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
    
    # Mark important sections
    marker = ""
    if i == 0:
        marker = " <-- Slot header"
    elif i == 24:
        marker = " <-- Name starts here"
    elif i == 48:
        marker = " <-- After name (params?)"
    
    print(f"  +{i:03d}: {hex_str:<48} {ascii_str}{marker}")

# Font size would likely be a single byte with value 0-4
# Let's look for bytes with values 0-4 in the parameter area
print(f"\n\nSearching for potential font size bytes (0-4) in parameter area:")
params_start = slot0_name_pos + 24
params = data[params_start:params_start+64]

for i, byte_val in enumerate(params):
    if byte_val <= 4:
        print(f"  Offset +{i} (0x{params_start+i:08X}): {byte_val} - could be font size")

# Check if there's a pattern across multiple slots
print(f"\n\nComparing parameter areas across first 3 slots:")
SLOT_SIZE = 0x1E82

for slot_idx in range(3):
    slot_start = slot0_start + (slot_idx * SLOT_SIZE)
    name_pos = slot_start + 24
    params_pos = name_pos + 24
    
    name = data[name_pos:name_pos+24].split(b'\x00')[0].decode('ascii', errors='ignore')
    
    # Show first 16 bytes of parameters
    params = data[params_pos:params_pos+16]
    hex_str = ' '.join(f'{b:02X}' for b in params)
    
    print(f"\nSlot {slot_idx}: '{name}'")
    print(f"  Params: {hex_str}")
    
    # Look for low values that might be font size
    for i, byte_val in enumerate(params):
        if byte_val <= 4:
            print(f"    Byte {i}: {byte_val}")
