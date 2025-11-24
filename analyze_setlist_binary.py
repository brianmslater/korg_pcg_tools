#!/usr/bin/env python3
"""Analyze setlist binary structure."""

import sys
import os
import struct

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TEST_FILE = "/Volumes/KEYBOARD/KORGSOUNDS/ULTIMATE COVERS narfsounds 3/SETLIST Narf Ultimate Covers.PCG"

print(f"\nAnalyzing: {os.path.basename(TEST_FILE)}\n")

with open(TEST_FILE, 'rb') as f:
    data = f.read()

# Find SLS1 chunk
sls1_offset = data.find(b'SLS1')
if sls1_offset < 0:
    print("SLS1 chunk not found!")
    sys.exit(1)

print(f"SLS1 chunk found at offset: 0x{sls1_offset:08X}")

# Read chunk size
chunk_size = struct.unpack('<I', data[sls1_offset+4:sls1_offset+8])[0]
print(f"Chunk size: 0x{chunk_size:08X} ({chunk_size} bytes)")

# Start of data
data_start = sls1_offset + 8
print(f"\nData starts at: 0x{data_start:08X}")

# Show first 512 bytes in hex
print("\nFirst 512 bytes of SLS1 data:")
print("="*70)
for i in range(0, min(512, len(data) - data_start), 16):
    offset = data_start + i
    hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
    print(f"{i:04X}: {hex_str:<48} {ascii_str}")

# Try to find set list names
print("\n" + "="*70)
print("Searching for readable strings (potential set list names):")
print("="*70)

# Look for strings in the first 2KB
search_area = data[data_start:data_start+2048]
current_string = []
string_offset = 0

for i, byte in enumerate(search_area):
    if 32 <= byte < 127:  # Printable ASCII
        if not current_string:
            string_offset = i
        current_string.append(chr(byte))
    else:
        if len(current_string) >= 4:  # String of 4+ chars
            string_text = ''.join(current_string)
            print(f"  Offset 0x{string_offset:04X}: '{string_text}'")
        current_string = []

# Look for specific patterns
print("\n" + "="*70)
print("Looking for slot structure patterns:")
print("="*70)

# Kronos setlist slot is typically 64-80 bytes
# Let's look for repeating patterns
slot_size_candidates = [64, 72, 80, 96]

for slot_size in slot_size_candidates:
    print(f"\nTrying slot size: {slot_size} bytes")
    # Check if we see similar patterns at regular intervals
    test_offset = data_start + 32  # Skip header
    for i in range(5):  # Check first 5 slots
        offset = test_offset + (i * slot_size)
        if offset + 32 < len(data):
            # Try to read as string
            slot_data = data[offset:offset+32]
            try:
                name = slot_data.split(b'\x00')[0].decode('ascii', errors='ignore')
                if name and len(name) > 2:
                    print(f"  Slot {i} at 0x{offset:04X}: '{name}'")
            except:
                pass
