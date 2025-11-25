#!/usr/bin/env python3
"""Debug slot 1 to see why it's not being read."""

from pathlib import Path

test_file = '/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG'

with open(test_file, 'rb') as f:
    data = f.read()

# Find NIGHTWISH LEGACY setlist
separator = b'\x28\x0F\x01\x00'
marker = b'\x1E\x02\x00\x00'

sls1 = data.find(b'SLS1')
pos = sls1

# Find second separator (NIGHTWISH LEGACY)
pos = data.find(separator, pos + 1)  # Skip Preload
nw_sep = data.find(separator, pos + 1)

print(f"NIGHTWISH LEGACY separator at: 0x{nw_sep:08X}\n")

# Slot 0 starts right after separator
slot_0_start = nw_sep + 4
print(f"Slot 0 (no marker):")
print(f"  Offset: 0x{slot_0_start:08X}")
slot_0_name = data[slot_0_start:slot_0_start+24].split(b'\x00')[0].decode('ascii', errors='ignore')
print(f"  Name: '{slot_0_name}'")

# Slot 1 starts after slot 0 name
slot_1_start = slot_0_start + 24
print(f"\nSlot 1 (with marker):")
print(f"  Offset: 0x{slot_1_start:08X}")
slot_1_marker = data[slot_1_start:slot_1_start+4]
print(f"  Marker: {slot_1_marker.hex()}")

if slot_1_marker == marker:
    slot_1_name_start = slot_1_start + 4
    slot_1_name = data[slot_1_name_start:slot_1_name_start+24].split(b'\x00')[0].decode('ascii', errors='ignore')
    print(f"  Name: '{slot_1_name}'")
    print(f"  Name bytes: {data[slot_1_name_start:slot_1_name_start+24].hex()}")
else:
    print(f"  ERROR: No marker found!")

# Check slots 2-5
for slot_idx in range(2, 6):
    slot_start = slot_0_start + 24 + ((slot_idx - 1) * 28)
    print(f"\nSlot {slot_idx}:")
    print(f"  Offset: 0x{slot_start:08X}")
    slot_marker = data[slot_start:slot_start+4]
    print(f"  Marker: {slot_marker.hex()}")
    
    if slot_marker == marker:
        slot_name_start = slot_start + 4
        slot_name = data[slot_name_start:slot_name_start+24].split(b'\x00')[0].decode('ascii', errors='ignore')
        print(f"  Name: '{slot_name}'")
    else:
        print(f"  ERROR: No marker found!")
