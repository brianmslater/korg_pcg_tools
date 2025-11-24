#!/usr/bin/env python3
"""Analyze nw.PCG setlist structure."""

from pathlib import Path

test_file = '/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG'

with open(test_file, 'rb') as f:
    data = f.read()

print(f"File size: {len(data):,} bytes\n")

# Find SLS1
sls1 = data.find(b'SLS1')
print(f"SLS1 at: 0x{sls1:08X}\n")

marker = b'\x1E\x02\x00\x00'
separator = b'\x28\x0F\x01\x00'

# Find separators
print("Looking for separators:")
pos = sls1
sep_positions = []
for i in range(20):
    pos = data.find(separator, pos + 1)
    if pos == -1:
        break
    # Name is 24 bytes before separator
    name_start = pos - 24
    name = data[name_start:pos].split(b'\x00')[0].decode('ascii', errors='ignore')
    sep_positions.append((pos, name))
    print(f"  {i}: 0x{pos:08X} -> '{name}'")

if len(sep_positions) >= 2:
    print(f"\n\nAnalyzing first setlist: '{sep_positions[0][1]}'")
    start = sep_positions[0][0]
    end = sep_positions[1][0]
    
    print(f"Start: 0x{start:08X}")
    print(f"End:   0x{end:08X}")
    print(f"Size:  0x{end-start:04X} ({end-start} bytes)")
    
    # Show bytes after separator
    print(f"\nBytes after separator:")
    for i in range(0, 128, 16):
        pos = start + i
        hex_str = ' '.join(f'{b:02X}' for b in data[pos:pos+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[pos:pos+16])
        marker_text = ""
        if i == 0:
            marker_text = " <-- SEPARATOR"
        print(f"  {pos:08X}: {hex_str:<48} {ascii_str}{marker_text}")
    
    # Find markers in this range
    print(f"\n\nSlots in first setlist:")
    pos = start
    slot_count = 0
    while pos < end:
        pos = data.find(marker, pos + 1)
        if pos == -1 or pos >= end:
            break
        name = data[pos+4:pos+28].split(b'\x00')[0].decode('ascii', errors='ignore')
        if slot_count < 10:  # Show first 10
            print(f"  Slot {slot_count}: 0x{pos:08X} -> '{name}'")
        slot_count += 1
    
    print(f"\nTotal slots found: {slot_count}")
