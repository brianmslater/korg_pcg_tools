#!/usr/bin/env python3
"""Analyze Ultimate Covers setlist for font size metadata."""

from pathlib import Path

test_file = '/Volumes/KEYBOARD/KORGSOUNDS/ULTIMATE COVERS narfsounds/SETLIST Narf Ultimate Covers.PCG'

with open(test_file, 'rb') as f:
    data = f.read()

print(f"File size: {len(data):,} bytes\n")

# Find SLD1 chunk
sld1_offset = data.find(b'SLD1')
print(f"SLD1 at: 0x{sld1_offset:08X}")

# Find first CBK1 (marks start of slot data)
cbk1_offset = data.find(b'CBK1', sld1_offset)
print(f"First CBK1 at: 0x{cbk1_offset:08X}")

# First slot name is 24 bytes after CBK1
first_slot_name_pos = cbk1_offset + 24
first_slot_name = data[first_slot_name_pos:first_slot_name_pos+24].split(b'\x00')[0].decode('ascii', errors='ignore')
print(f"First slot name: '{first_slot_name}'")

# Slot size is 7810 bytes (0x1E82)
SLOT_SIZE = 0x1E82

print(f"\n\nAnalyzing first 10 slots for font size patterns:")
print(f"{'Slot':<4} {'Name':<30} {'Byte+24':<8} {'Byte+25':<8} {'Byte+26':<8} {'Byte+27':<8}")
print("-" * 80)

for slot_idx in range(10):
    slot_start = cbk1_offset + (slot_idx * SLOT_SIZE)
    name_pos = slot_start + 24
    params_pos = name_pos + 24
    
    name = data[name_pos:name_pos+24].split(b'\x00')[0].decode('ascii', errors='ignore')
    
    # Check bytes after name that might be font size
    b24 = data[params_pos] if params_pos < len(data) else 0
    b25 = data[params_pos+1] if params_pos+1 < len(data) else 0
    b26 = data[params_pos+2] if params_pos+2 < len(data) else 0
    b27 = data[params_pos+3] if params_pos+3 < len(data) else 0
    
    print(f"{slot_idx:<4} {name[:28]:<30} {b24:<8} {b25:<8} {b26:<8} {b27:<8}")

# Look for any bytes with values 0-4 in the first few slots
print(f"\n\nSearching for bytes with values 0-4 in first 3 slots:")
for slot_idx in range(3):
    slot_start = cbk1_offset + (slot_idx * SLOT_SIZE)
    name_pos = slot_start + 24
    params_pos = name_pos + 24
    
    name = data[name_pos:name_pos+24].split(b'\x00')[0].decode('ascii', errors='ignore')
    params = data[params_pos:params_pos+32]
    
    print(f"\nSlot {slot_idx}: '{name}'")
    for i, byte_val in enumerate(params):
        if byte_val <= 4:
            print(f"  Byte +{i}: {byte_val}")
