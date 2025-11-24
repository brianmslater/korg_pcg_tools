#!/usr/bin/env python3
"""Analyze the structure of a single slot entry in SLD1."""

import struct
from pathlib import Path

test_file = '/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG'

with open(test_file, 'rb') as f:
    data = f.read()

# Focus on SLEEPING INTRO slot
slot_name_pos = data.find(b'SLEEPING INTRO')
print(f"SLEEPING INTRO at: 0x{slot_name_pos:08X}\n")

# The name is 24 bytes
name_bytes = data[slot_name_pos:slot_name_pos+24]
print(f"Name (24 bytes): {name_bytes.hex()}")
name_str = name_bytes.split(b'\x00')[0].decode()
print(f"Name string: '{name_str}'")

# After the name, there should be slot parameters
params_start = slot_name_pos + 24
print(f"\nParameters after name (64 bytes):")
for i in range(0, 64, 16):
    offset = params_start + i
    hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
    print(f"  +{i:02d}: {hex_str:<48} {ascii_str}")

# Try to decode some parameters
print(f"\nDecoding parameters:")
params = data[params_start:params_start+32]

# Common slot parameters might include:
# - Transpose (signed byte, -24 to +24)
# - Volume (0-127)
# - Patch bank/index
# - Patch type (Program/Combi)

print(f"  Byte 0: 0x{params[0]:02X} ({params[0]}) - might be transpose+offset")
print(f"  Byte 1: 0x{params[1]:02X} ({params[1]})")
print(f"  Byte 2: 0x{params[2]:02X} ({params[2]})")
print(f"  Byte 3: 0x{params[3]:02X} ({params[3]})")
print(f"  Byte 4: 0x{params[4]:02X} ({params[4]})")
print(f"  Byte 5: 0x{params[5]:02X} ({params[5]})")
print(f"  Byte 6: 0x{params[6]:02X} ({params[6]})")
print(f"  Byte 7: 0x{params[7]:02X} ({params[7]})")

# Look for CBK1 marker (Combi Bank) before the slot
print(f"\n\nSearching backwards for chunk markers:")
for search_back in [100, 200, 500, 1000, 2000]:
    search_start = max(0, slot_name_pos - search_back)
    chunk_markers = [b'CBK1', b'PBK1', b'SLD1', b'SLDT']
    for marker in chunk_markers:
        pos = data.rfind(marker, search_start, slot_name_pos)
        if pos >= 0:
            distance = slot_name_pos - pos
            print(f"  {marker.decode()} at 0x{pos:08X} (distance: {distance} bytes, 0x{distance:04X})")
            break
    else:
        continue
    break

# Check if there's a pattern before each slot name
print(f"\n\nLooking for slot entry header:")
# Go back 32 bytes and look for patterns
header_start = slot_name_pos - 32
print(f"32 bytes before name:")
for i in range(0, 32, 16):
    offset = header_start + i
    hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
    print(f"  {offset:08X}: {hex_str}")
