#!/usr/bin/env python3
"""Analyze SLD1 structure for NIGHTWISH LEGACY setlist."""

from pathlib import Path

test_file = '/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG'

with open(test_file, 'rb') as f:
    data = f.read()

# Find "NIGHTWISH LEGACY" in SLD1
search = b'NIGHTWISH LEGACY'
positions = []
pos = 0
while True:
    pos = data.find(search, pos)
    if pos == -1:
        break
    positions.append(pos)
    pos += 1

print(f"Found 'NIGHTWISH LEGACY' at {len(positions)} locations:")
for i, pos in enumerate(positions):
    print(f"  {i}: 0x{pos:08X}")

# The second occurrence should be in SLD1 (first is in SLS1)
if len(positions) >= 2:
    sld1_pos = positions[1]
    print(f"\nAnalyzing SLD1 occurrence at 0x{sld1_pos:08X}:")
    
    # Show context before and after
    print("\nContext (128 bytes before and after):")
    for i in range(-128, 256, 16):
        offset = sld1_pos + i
        hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
        marker = ">>>" if sld1_pos <= offset < sld1_pos + 16 else "   "
        print(f"{marker} {offset:08X}: {hex_str:<48} {ascii_str}")
    
    # Look for slot data after the setlist name
    # Slot data should start shortly after the setlist name
    print(f"\n\nLooking for slot 0 data (SLEEPING INTRO):")
    slot0_search = b'SLEEPING INTRO'
    slot0_pos = data.find(slot0_search, sld1_pos)
    if slot0_pos > 0:
        print(f"Found at: 0x{slot0_pos:08X}")
        print(f"Distance from setlist name: {slot0_pos - sld1_pos} bytes (0x{slot0_pos - sld1_pos:04X})")
        
        # Show the structure
        print(f"\nSlot 0 structure:")
        for i in range(-32, 64, 16):
            offset = slot0_pos + i
            hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
            marker = ">>>" if slot0_pos <= offset < slot0_pos + 16 else "   "
            print(f"{marker} {offset:08X}: {hex_str:<48} {ascii_str}")
