#!/usr/bin/env python3
"""Analyze SLD1 chunk structure."""

from pathlib import Path

test_file = '/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG'

with open(test_file, 'rb') as f:
    data = f.read()

# Find SLD1 chunk
sld1_offset = data.find(b'SLD1')
print(f"SLD1 chunk at: 0x{sld1_offset:08X}")

# Read chunk size
import struct
chunk_size = struct.unpack('<I', data[sld1_offset+4:sld1_offset+8])[0]
print(f"Chunk size: 0x{chunk_size:08X} ({chunk_size} bytes)")

# Data starts after 8-byte header
data_start = sld1_offset + 8
print(f"Data starts at: 0x{data_start:08X}\n")

# Show first 512 bytes of SLD1 data
print("First 512 bytes of SLD1 data:")
for i in range(0, 512, 16):
    offset = data_start + i
    hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
    print(f"  {offset:08X}: {hex_str:<48} {ascii_str}")

# Look for "SLEEPING SUN RIT" in the file
search_str = b'SLEEPING SUN RIT'
pos = data.find(search_str)
if pos >= 0:
    print(f"\n\nFound 'SLEEPING SUN RIT' at: 0x{pos:08X}")
    print(f"Relative to SLD1 start: +0x{pos - sld1_offset:04X}")
    print(f"Relative to SLD1 data: +0x{pos - data_start:04X}")
    
    # Show context around it
    print(f"\nContext (64 bytes before and after):")
    context_start = max(0, pos - 64)
    for i in range(0, 128, 16):
        offset = context_start + i
        hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
        marker = ">>>" if pos <= offset < pos + 16 else "   "
        print(f"{marker} {offset:08X}: {hex_str:<48} {ascii_str}")
else:
    print("\n\n'SLEEPING SUN RIT' not found in file")
