#!/usr/bin/env python3
"""Analyze the Preload Set List which should have data."""

from pathlib import Path

test_file = Path('test_files/files/GLAM V3/GLAMV3.PCG')

with open(test_file, 'rb') as f:
    data = f.read()

# Find SLS1
sls1 = data.find(b'SLS1')
print(f"SLS1 at: 0x{sls1:08X}\n")

marker = b'\x1E\x02\x00\x00'
separator = b'\x28\x0F\x01\x00'

# Find Preload Set List separator
preload_sep = data.find(separator, sls1)
print(f"Preload Set List separator at: 0x{preload_sep:08X}")

# Find next separator (Set List 001)
next_sep = data.find(separator, preload_sep + 1)
print(f"Set List 001 separator at: 0x{next_sep:08X}")
print(f"Size: 0x{next_sep - preload_sep:04X} ({next_sep - preload_sep} bytes)\n")

# Show structure after Preload separator
print("Bytes after Preload separator:")
offset = preload_sep
for i in range(0, 256, 16):
    pos = offset + i
    hex_str = ' '.join(f'{b:02X}' for b in data[pos:pos+16])
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[pos:pos+16])
    marker_text = ""
    if i == 0:
        marker_text = " <-- SEPARATOR"
    elif i == 4:
        marker_text = " <-- After separator"
    print(f"  {pos:08X}: {hex_str:<48} {ascii_str}{marker_text}")

# Find markers in Preload range
print(f"\n\nMarkers in Preload Set List:")
pos = preload_sep
slot_count = 0
first_slots = []
while pos < next_sep:
    pos = data.find(marker, pos + 1)
    if pos == -1 or pos >= next_sep:
        break
    name = data[pos+4:pos+28].split(b'\x00')[0].decode('ascii', errors='ignore')
    if slot_count < 20:  # Show first 20
        print(f"  Slot {slot_count}: 0x{pos:08X} (+0x{pos-preload_sep:04X}) -> '{name}'")
        first_slots.append((slot_count, pos, name))
    slot_count += 1

print(f"\nTotal slots found: {slot_count}")

# Analyze spacing between slots
if len(first_slots) >= 2:
    print(f"\n\nSpacing between slots:")
    for i in range(min(5, len(first_slots) - 1)):
        spacing = first_slots[i+1][1] - first_slots[i][1]
        print(f"  Slot {i} to {i+1}: {spacing} bytes (0x{spacing:02X})")
