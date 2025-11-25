#!/usr/bin/env python3
"""Verify slot indices match the binary data."""

from pathlib import Path

test_file = '/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG'

with open(test_file, 'rb') as f:
    data = f.read()

# Find first setlist (NIGHTWISH LEGACY)
separator = b'\x28\x0F\x01\x00'
marker = b'\x1E\x02\x00\x00'

# Find first separator after SLS1
sls1 = data.find(b'SLS1')
first_sep = data.find(separator, sls1)

print(f"First separator at: 0x{first_sep:08X}")

# Name is 24 bytes before separator
name_start = first_sep - 24
name = data[name_start:first_sep].split(b'\x00')[0].decode('ascii', errors='ignore')
print(f"Setlist name: '{name}'\n")

# First slot is right after separator (no marker)
slots_start = first_sep + 4
print("Reading all 128 slots:\n")

# Slot 0 (no marker)
slot_name = data[slots_start:slots_start+24].split(b'\x00')[0].decode('ascii', errors='ignore')
print(f"Slot 0: '{slot_name}'")

# Slots 1-127 (with markers)
current_pos = slots_start + 24
for i in range(1, 128):
    check_marker = data[current_pos:current_pos+4]
    if check_marker != marker:
        print(f"Slot {i}: NO MARKER FOUND - stopping")
        break
    
    slot_name = data[current_pos+4:current_pos+28].split(b'\x00')[0].decode('ascii', errors='ignore')
    if slot_name:  # Only print non-empty
        print(f"Slot {i}: '{slot_name}'")
    
    current_pos += 28
    
    if i >= 20:  # Just show first 20
        print("...")
        break
