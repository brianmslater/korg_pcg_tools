#!/usr/bin/env python3
"""Parse SLD1 slot data for NIGHTWISH LEGACY setlist."""

import struct
from pathlib import Path

test_file = '/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG'

with open(test_file, 'rb') as f:
    data = f.read()

# Find the start of slot data for NIGHTWISH LEGACY
# We know SLEEPING INTRO is the first slot
first_slot_pos = data.find(b'SLEEPING INTRO')
print(f"First slot (SLEEPING INTRO) at: 0x{first_slot_pos:08X}\n")

# Go back to find the CBK1 marker
cbk1_pos = data.rfind(b'CBK1', first_slot_pos - 100, first_slot_pos)
print(f"CBK1 marker at: 0x{cbk1_pos:08X}")
print(f"Distance to name: {first_slot_pos - cbk1_pos} bytes\n")

# Parse the header between CBK1 and the name
header_start = cbk1_pos + 4
header = data[header_start:first_slot_pos]
print(f"Header ({len(header)} bytes): {header.hex()}")

# Try to parse the header
print(f"\nHeader breakdown:")
print(f"  Bytes 0-3:   {header[0:4].hex()} - might be size/offset")
print(f"  Bytes 4-7:   {header[4:8].hex()}")
print(f"  Bytes 8-11:  {header[8:12].hex()}")
print(f"  Bytes 12-15: {header[12:16].hex()} - contains 1E 82 (7810 = combi size)")
print(f"  Bytes 16-19: {header[16:20].hex()}")

# The pattern seems to be:
# CBK1 + 20 bytes header + 24 bytes name
# Let's try to find all slots by looking for this pattern

print(f"\n\nSearching for all slots in NIGHTWISH LEGACY:")
print(f"Looking for CBK1 markers followed by names...\n")

# Start from the first slot and look for more
current_pos = cbk1_pos
slot_count = 0
max_slots = 20  # Just check first 20

while slot_count < max_slots:
    # Look for next CBK1
    next_cbk1 = data.find(b'CBK1', current_pos + 1)
    if next_cbk1 < 0 or next_cbk1 > first_slot_pos + 200000:  # Don't go too far
        break
    
    # Name should be 24 bytes after CBK1 (4 byte marker + 20 byte header)
    name_pos = next_cbk1 + 4 + 20
    name_bytes = data[name_pos:name_pos+24]
    name = name_bytes.split(b'\x00')[0].decode('ascii', errors='ignore')
    
    if name and len(name) >= 3 and name.isprintable():
        print(f"Slot {slot_count}: '{name}' at 0x{name_pos:08X}")
        slot_count += 1
        current_pos = name_pos
    else:
        current_pos = next_cbk1 + 4

print(f"\nFound {slot_count} slots")
