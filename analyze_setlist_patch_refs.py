#!/usr/bin/env python3
"""Analyze setlist patch reference structure."""

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

print(f"NIGHTWISH LEGACY separator at: 0x{nw_sep:08X}")

# After separator + first slot name, look at the data
slots_start = nw_sep + 4
first_slot_name_end = slots_start + 24

print(f"\nFirst slot name area: 0x{slots_start:08X} to 0x{first_slot_name_end:08X}")
name_bytes = data[slots_start:first_slot_name_end].split(b'\x00')[0].decode('ascii', errors='ignore')
print(f"Name: {name_bytes}")

# After first slot name, we have marker + second slot
second_slot_start = first_slot_name_end
print(f"\nSecond slot marker at: 0x{second_slot_start:08X}")
print(f"Marker: {data[second_slot_start:second_slot_start+4].hex()}")

# Look for patch reference data
# It might be in a different chunk or after the names
print(f"\n\nLooking for patch reference data...")
print(f"Bytes after first slot name (next 64 bytes):")
for i in range(0, 64, 16):
    offset = first_slot_name_end + i
    hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
    print(f"  {offset:08X}: {hex_str:<48} {ascii_str}")

# Check if there's a separate data section after all slot names
# 128 slots * 28 bytes = 3584 bytes
all_slots_end = slots_start + 24 + (127 * 28)
print(f"\n\nAfter all slot names (0x{all_slots_end:08X}):")
for i in range(0, 128, 16):
    offset = all_slots_end + i
    hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
    print(f"  {offset:08X}: {hex_str:<48} {ascii_str}")
