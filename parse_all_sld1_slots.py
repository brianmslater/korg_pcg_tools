#!/usr/bin/env python3
"""Parse all SLD1 slots using fixed spacing."""

from pathlib import Path

test_file = '/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG'

with open(test_file, 'rb') as f:
    data = f.read()

# Find the first slot
first_slot_name_pos = data.find(b'SLEEPING INTRO')
print(f"First slot name at: 0x{first_slot_name_pos:08X}\n")

# Each slot is 7810 bytes (0x1E82)
SLOT_SIZE = 0x1E82

# The name appears to be at offset +24 from the start of each slot entry
# So the slot entry starts 24 bytes before the name
first_slot_start = first_slot_name_pos - 24

print(f"Slot entry structure:")
print(f"  Slot start: 0x{first_slot_start:08X}")
print(f"  Name at:    0x{first_slot_name_pos:08X} (+24 bytes)")
print(f"  Slot size:  {SLOT_SIZE} bytes (0x{SLOT_SIZE:04X})\n")

# Parse all 128 slots
print(f"Parsing all 128 slots:\n")
for slot_idx in range(128):
    slot_start = first_slot_start + (slot_idx * SLOT_SIZE)
    name_pos = slot_start + 24
    
    # Read name (24 bytes)
    name_bytes = data[name_pos:name_pos+24]
    name = name_bytes.split(b'\x00')[0].decode('ascii', errors='ignore')
    
    # Only show slots with names
    if name and len(name) >= 2:
        print(f"Slot {slot_idx:3d}: '{name}'")
    
    # Stop after showing first 20 with names
    if slot_idx >= 20:
        break

print(f"\n... (continuing to slot 127)")

# Check a few specific slots we know about
print(f"\n\nVerifying known slots:")
known_slots = {
    0: 'SLEEPING INTRO',
    1: 'SLEEPING SUN RIT',
}

for slot_idx, expected_name in known_slots.items():
    slot_start = first_slot_start + (slot_idx * SLOT_SIZE)
    name_pos = slot_start + 24
    name_bytes = data[name_pos:name_pos+24]
    name = name_bytes.split(b'\x00')[0].decode('ascii', errors='ignore')
    
    match = "✓" if name == expected_name else "✗"
    print(f"  {match} Slot {slot_idx}: expected '{expected_name}', got '{name}'")
