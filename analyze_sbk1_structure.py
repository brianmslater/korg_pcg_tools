#!/usr/bin/env python3
"""Analyze SBK1 chunk structure to understand setlist layout."""

import struct

def analyze_sbk1():
    data = open('test_files/soundcheck9_25_25_combined2.PCG', 'rb').read()
    
    # Find SBK1
    sbk1_offset = data.find(b'SBK1')
    print(f'SBK1 at offset: {sbk1_offset} (0x{sbk1_offset:X})')
    
    # Get size
    size = struct.unpack('<I', data[sbk1_offset+4:sbk1_offset+8])[0]
    print(f'SBK1 size: {size:,} bytes')
    
    sbk1_data_start = sbk1_offset + 8
    sbk1_end = sbk1_data_start + size
    
    print(f'SBK1 data: {sbk1_data_start} to {sbk1_end}')
    print()
    
    # Search for setlist names in SBK1
    setlist_names = [
        b'NIGHTWISH LEGACY',
        b'NIGHTWISH LEGACY 2',
        b'Narf',
        b'Set List 004',
        b'SC 10/4',
        b'Set List 006',
        b'Set List 007',
        b'Set List 008'
    ]
    
    print('Setlist name positions in SBK1:')
    for name in setlist_names:
        pos = data.find(name, sbk1_data_start, sbk1_end)
        if pos >= 0:
            offset_in_sbk1 = pos - sbk1_data_start
            print(f'  {name.decode():24s} at SBK1+{offset_in_sbk1:6d} (absolute {pos})')
            
            # Check what's before it
            before = data[pos-20:pos]
            print(f'    Before: {before.hex()}')
    
    print()
    print('Looking for pattern...')
    
    # Calculate spacing between setlists
    positions = []
    for name in setlist_names:
        pos = data.find(name, sbk1_data_start, sbk1_end)
        if pos >= 0:
            positions.append(pos - sbk1_data_start)
    
    if len(positions) > 1:
        spacings = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
        print(f'Spacings between setlists: {spacings}')
        if len(set(spacings)) == 1:
            print(f'✓ Regular spacing: {spacings[0]} bytes per setlist')
        else:
            print(f'✗ Irregular spacing')

if __name__ == '__main__':
    analyze_sbk1()
