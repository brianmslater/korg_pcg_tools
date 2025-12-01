#!/usr/bin/env python3
"""Check STL1/SBK1 structure."""

# Check if the STL1 update is working correctly
with open('test_files/soundcheck_BASE_FOR_TESTING.PCG', 'rb') as f:
    data = f.read()

# Find STL1
stl1_offset = data.find(b'STL1')
print(f'STL1 chunk at: 0x{stl1_offset:08x}')

# Find SBK1 within STL1
sbk1_offset = data.find(b'SBK1', stl1_offset)
print(f'SBK1 chunk at: 0x{sbk1_offset:08x}')

if sbk1_offset > 0:
    sbk1_data_start = sbk1_offset + 8
    
    # Calculate first setlist name position
    FIRST_SETLIST_OFFSET = 69432
    name_pos = sbk1_data_start + FIRST_SETLIST_OFFSET
    
    print(f'SBK1 data starts at: 0x{sbk1_data_start:08x}')
    print(f'First setlist name should be at: 0x{name_pos:08x}')
    print(f'Name at that position: {data[name_pos:name_pos+24].decode("ascii", errors="ignore").strip()!r}')
    
    # Check where NIGHTWISH actually is in STL1
    nightwish_in_stl1 = data.find(b'NIGHTWISH LEGACY', stl1_offset)
    if nightwish_in_stl1 > 0:
        print(f'\nNIGHTWISH LEGACY found at: 0x{nightwish_in_stl1:08x}')
        print(f'Offset from SBK1 data start: {nightwish_in_stl1 - sbk1_data_start}')
        print(f'Expected offset: {FIRST_SETLIST_OFFSET}')
        print(f'Difference: {(nightwish_in_stl1 - sbk1_data_start) - FIRST_SETLIST_OFFSET}')
