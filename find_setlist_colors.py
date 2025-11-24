#!/usr/bin/env python3
"""Find where setlist colors are stored."""

from pathlib import Path

test_file = '/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG'

with open(test_file, 'rb') as f:
    data = f.read()

# Find the NIGHTWISH LEGACY setlist name in SLS1
sls1_offset = data.find(b'SLS1')
print(f"SLS1 at: 0x{sls1_offset:08X}")

# Find NIGHTWISH LEGACY in SLS1 (should be second occurrence after Preload)
separator = b'\x28\x0F\x01\x00'
pos = sls1_offset
pos = data.find(separator, pos + 1)  # Skip Preload
nw_pos = data.find(separator, pos + 1)  # NIGHTWISH LEGACY

print(f"NIGHTWISH LEGACY separator at: 0x{nw_pos:08X}")

# The setlist name is 24 bytes before the separator
name_start = nw_pos - 24
name = data[name_start:nw_pos].split(b'\x00')[0].decode('ascii', errors='ignore')
print(f"Setlist name: '{name}'")

# Look at data before the marker (might contain color/metadata)
marker_pos = name_start - 4
print(f"\nMarker at: 0x{marker_pos:08X}")
print(f"Marker: {data[marker_pos:marker_pos+4].hex()}")

# Show 64 bytes before the marker
print(f"\n64 bytes before marker (might contain color/metadata):")
for i in range(-64, 0, 16):
    offset = marker_pos + i
    hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
    print(f"  {offset:08X}: {hex_str:<48} {ascii_str}")

# Colors might be stored in a separate section
# Let's look for patterns - colors are 0-11
print(f"\n\nLooking for potential color bytes (0-11) near setlist names...")
# Check bytes around the setlist name
for offset in range(marker_pos - 32, marker_pos):
    byte_val = data[offset]
    if byte_val <= 11:
        print(f"  Offset {offset:08X} (marker-{marker_pos-offset}): {byte_val} - could be color")
