#!/usr/bin/env python3
"""Analyze setlist name structure."""

TEST_FILE = "/Volumes/KEYBOARD/KORGSOUNDS/ULTIMATE COVERS narfsounds 3/SETLIST Narf Ultimate Covers.PCG"

with open(TEST_FILE, 'rb') as f:
    data = f.read()

# Find SLS1
sls1 = data.find(b'SLS1')
print(f"SLS1 at: 0x{sls1:08X}\n")

# Find Preload Set List
preload = data.find(b'Preload Set List')
print(f"'Preload Set List' at: 0x{preload:08X}")
print(f"Relative to SLS1: +0x{preload - sls1:04X}\n")

# Show hex around Preload
print("Hex around 'Preload Set List':")
start = preload - 8
for i in range(0, 128, 16):
    offset = start + i
    hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
    marker = ">>>" if preload <= offset < preload + 16 else "   "
    print(f"{marker} {offset:08X}: {hex_str:<48} {ascii_str}")

# Find first marker
marker = b'\x1E\x02\x00\x00'
first_marker = data.find(marker, sls1)
print(f"\nFirst marker at: 0x{first_marker:08X}")
print(f"Relative to SLS1: +0x{first_marker - sls1:04X}")
print(f"Relative to Preload: +0x{first_marker - preload:04X}\n")

# The real setlist names appear to be in SDB1 chunk
# Let's find SDB1
sdb1 = data.find(b'SDB1', sls1)
if sdb1 > 0:
    print(f"\nSDB1 at: 0x{sdb1:08X}")
    print(f"Relative to SLS1: +0x{sdb1 - sls1:04X}\n")
    
    # SDB1 structure: chunk header (8 bytes) + data
    # Data starts at SDB1 + 8
    offset = sdb1 + 8
    print("Reading 16 setlist names from SDB1:")
    for i in range(16):
        # Each entry: 4-byte header + 24-byte name
        header = data[offset:offset+4]
        name = data[offset+4:offset+28].split(b'\x00')[0].decode('ascii', errors='ignore')
        print(f"  {i}: 0x{offset:08X} header={header.hex()} name=\"{name}\"")
        offset += 28

# Now check slot names with markers
print("\nSlot names (with markers):")
pos = first_marker
for i in range(20):
    if pos >= len(data) - 28:
        break
    marker_bytes = data[pos:pos+4]
    if marker_bytes != marker:
        break
    name = data[pos+4:pos+28].split(b'\x00')[0].decode('ascii', errors='ignore')
    print(f"  {i}: 0x{pos:08X} -> \"{name}\"")
    pos = data.find(marker, pos + 4)
    if pos == -1:
        break
