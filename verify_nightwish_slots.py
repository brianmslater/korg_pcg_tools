#!/usr/bin/env python3
"""Verify NIGHTWISH LEGACY slot indices."""

from pathlib import Path

test_file = '/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG'

with open(test_file, 'rb') as f:
    data = f.read()

# Find NIGHTWISH LEGACY setlist
separator = b'\x28\x0F\x01\x00'
marker = b'\x1E\x02\x00\x00'

# Find all separators
sls1 = data.find(b'SLS1')
pos = sls1
separators = []

for i in range(20):
    pos = data.find(separator, pos + 1)
    if pos == -1:
        break
    name_start = pos - 24
    name = data[name_start:pos].split(b'\x00')[0].decode('ascii', errors='ignore')
    separators.append((pos, name))
    print(f"{i}: '{name}' at 0x{pos:08X}")

# Find NIGHTWISH LEGACY (should be index 1)
nw_sep = None
for pos, name in separators:
    if 'NIGHTWISH LEGACY' in name and '2' not in name:
        nw_sep = pos
        print(f"\nFound '{name}' at 0x{nw_sep:08X}")
        break

if nw_sep:
    # Read slots
    slots_start = nw_sep + 4
    print("\nReading all 128 slots:\n")
    
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
