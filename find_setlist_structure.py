#!/usr/bin/env python3
"""Find setlist structure by locating known strings."""

import sys
import os

TEST_FILE = "/Volumes/KEYBOARD/KORGSOUNDS/ULTIMATE COVERS narfsounds 3/SETLIST Narf Ultimate Covers.PCG"

with open(TEST_FILE, 'rb') as f:
    data = f.read()

# Find known setlist name
search_string = b"Here I Go Again"
offsets = []
pos = 0
while True:
    pos = data.find(search_string, pos)
    if pos == -1:
        break
    offsets.append(pos)
    pos += 1

print(f"Found '{search_string.decode()}' at {len(offsets)} locations:")
for offset in offsets:
    print(f"\n  Offset: 0x{offset:08X} ({offset})")
    # Show context around this offset
    start = max(0, offset - 32)
    end = min(len(data), offset + 64)
    
    print(f"  Context (32 bytes before, string, 32 bytes after):")
    for i in range(start, end, 16):
        hex_str = ' '.join(f'{b:02X}' for b in data[i:i+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:i+16])
        marker = ">>>" if i <= offset < i+16 else "   "
        print(f"  {marker} {i:08X}: {hex_str:<48} {ascii_str}")

# Also search for slot names
print("\n" + "="*70)
search_string2 = b"Hey Ya!"
pos = data.find(search_string2)
if pos >= 0:
    print(f"\nFound '{search_string2.decode()}' at offset: 0x{pos:08X}")
    start = max(0, pos - 64)
    end = min(len(data), pos + 96)
    
    print(f"Context:")
    for i in range(start, end, 16):
        hex_str = ' '.join(f'{b:02X}' for b in data[i:i+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:i+16])
        marker = ">>>" if i <= pos < i+16 else "   "
        print(f"{marker} {i:08X}: {hex_str:<48} {ascii_str}")
