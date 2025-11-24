#!/usr/bin/env python3
"""Systematically analyze SLD1 chunk structure."""

import struct
from pathlib import Path

test_file = '/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG'

with open(test_file, 'rb') as f:
    data = f.read()

# Find SLD1 chunk
sld1_offset = data.find(b'SLD1')
print(f"SLD1 chunk at: 0x{sld1_offset:08X}")

# The chunk size seems wrong, let's look at the actual structure
# SLD1 is inside SLS1, so let's find the real boundaries
sls1_offset = data.find(b'SLS1')
sls1_size = struct.unpack('<I', data[sls1_offset+4:sls1_offset+8])[0]
print(f"SLS1 chunk at: 0x{sls1_offset:08X}, size: 0x{sls1_size:08X}")

# SLD1 is at offset 0x60, which is 0x0C bytes after SLS1 (0x54)
# Let's look at what's between them
print(f"\nBytes between SLS1 and SLD1:")
for i in range(0, 32, 16):
    offset = sls1_offset + 8 + i
    hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
    print(f"  {offset:08X}: {hex_str:<48} {ascii_str}")

# Now let's find all the slot names we know about
known_slots = [
    b'SLEEPING INTRO',
    b'SLEEPING SUN RIT',
    b'NEMO',
    b'WISH I HAD AN ANGEL',
]

print(f"\n\nSearching for known slot names:")
for slot_name in known_slots:
    pos = data.find(slot_name)
    if pos >= 0:
        print(f"\n'{slot_name.decode()}' at 0x{pos:08X}")
        # Show what's before the name (might be slot metadata)
        print(f"  32 bytes before:")
        for i in range(-32, 0, 16):
            offset = pos + i
            hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
            print(f"    {offset:08X}: {hex_str}")
        
        # Show the name and what's after
        print(f"  Name and 32 bytes after:")
        for i in range(0, 48, 16):
            offset = pos + i
            hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
            print(f"    {offset:08X}: {hex_str:<48} {ascii_str}")

# Calculate distances between slot names
print(f"\n\nDistances between slot names:")
positions = []
for slot_name in known_slots:
    pos = data.find(slot_name)
    if pos >= 0:
        positions.append((slot_name.decode(), pos))

for i in range(len(positions) - 1):
    name1, pos1 = positions[i]
    name2, pos2 = positions[i + 1]
    distance = pos2 - pos1
    print(f"  {name1} -> {name2}: {distance} bytes (0x{distance:04X})")
