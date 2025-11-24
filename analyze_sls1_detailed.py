#!/usr/bin/env python3
"""Detailed analysis of SLS1 structure."""

from pathlib import Path

test_file = Path('test_files/files/GLAM V3/GLAMV3.PCG')

with open(test_file, 'rb') as f:
    data = f.read()

# Find SLS1
sls1 = data.find(b'SLS1')
print(f"SLS1 at: 0x{sls1:08X}\n")

# Find marker pattern
marker = b'\x1E\x02\x00\x00'
separator = b'\x28\x0F\x01\x00'

# Find first few markers
print("First 10 markers:")
pos = sls1
for i in range(10):
    pos = data.find(marker, pos + 1)
    if pos == -1:
        break
    name = data[pos+4:pos+28].split(b'\x00')[0].decode('ascii', errors='ignore')
    print(f"  {i}: 0x{pos:08X} (+0x{pos-sls1:06X}) -> '{name}'")

# Find separators
print("\nFirst 5 separators:")
pos = sls1
for i in range(5):
    pos = data.find(separator, pos + 1)
    if pos == -1:
        break
    # Check what's before the separator
    before = data[pos-24:pos].split(b'\x00')[0].decode('ascii', errors='ignore')
    print(f"  {i}: 0x{pos:08X} (+0x{pos-sls1:06X}), before: '{before}'")

# Check the structure around first separator
first_sep = data.find(separator, sls1)
if first_sep > 0:
    print(f"\nStructure around first separator (0x{first_sep:08X}):")
    start = first_sep - 32
    for i in range(0, 128, 16):
        offset = start + i
        hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
        marker_text = ""
        if offset <= first_sep < offset + 16:
            marker_text = " <-- SEPARATOR"
        print(f"  {offset:08X}: {hex_str:<48} {ascii_str}{marker_text}")
