#!/usr/bin/env python3
"""Analyze STL1/SBK1 structure in detail."""

with open('test_files/soundcheck_BASE_FOR_TESTING.PCG', 'rb') as f:
    data = f.read()

# Find STL1
stl1_offset = data.find(b'STL1')
stl1_size = int.from_bytes(data[stl1_offset+4:stl1_offset+8], 'little')
stl1_data_start = stl1_offset + 12  # Skip STL1 header (4 + 4 + 4)

print("STL1 Structure Analysis")
print("="*80)
print(f"STL1 chunk at: 0x{stl1_offset:08x}")
print(f"STL1 size: {stl1_size} bytes")
print(f"STL1 data starts at: 0x{stl1_data_start:08x}")
print()

# Find SBK1 within STL1
sbk1_offset = data.find(b'SBK1', stl1_offset)
if sbk1_offset > 0:
    sbk1_size = int.from_bytes(data[sbk1_offset+4:sbk1_offset+8], 'little')
    sbk1_data_start = sbk1_offset + 12  # Skip SBK1 header
    
    print(f"SBK1 chunk at: 0x{sbk1_offset:08x}")
    print(f"SBK1 size: {sbk1_size} bytes")
    print(f"SBK1 data starts at: 0x{sbk1_data_start:08x}")
    print()
    
    # Find all setlist names in SBK1
    print("Searching for setlist names in SBK1...")
    print("-"*80)
    
    # Known setlist names to search for
    setlist_names = [
        b'NIGHTWISH LEGACY',
        b'Set List 2',
        b'Set List 3',
    ]
    
    for name in setlist_names:
        pos = data.find(name, sbk1_offset, sbk1_offset + sbk1_size)
        if pos > 0:
            offset_from_sbk1_data = pos - sbk1_data_start
            print(f"'{name.decode()}' at 0x{pos:08x}")
            print(f"  Offset from SBK1 data start: {offset_from_sbk1_data} (0x{offset_from_sbk1_data:x})")
            
            # Check what's around it
            before = data[pos-16:pos]
            after = data[pos+24:pos+40]
            print(f"  16 bytes before: {before.hex()}")
            print(f"  16 bytes after:  {after.hex()}")
            print()

# Find the second occurrence of NIGHTWISH in STL1
print("\nAll occurrences of 'NIGHTWISH LEGACY' in STL1:")
print("-"*80)
pos = stl1_offset
count = 0
while pos < stl1_offset + stl1_size:
    pos = data.find(b'NIGHTWISH LEGACY', pos, stl1_offset + stl1_size)
    if pos == -1:
        break
    count += 1
    offset_from_stl1 = pos - stl1_data_start
    offset_from_sbk1 = pos - sbk1_data_start if sbk1_offset > 0 else -1
    print(f"Occurrence {count}: 0x{pos:08x}")
    print(f"  From STL1 data: {offset_from_stl1} (0x{offset_from_stl1:x})")
    if sbk1_offset > 0:
        print(f"  From SBK1 data: {offset_from_sbk1} (0x{offset_from_sbk1:x})")
    print()
    pos += 1
