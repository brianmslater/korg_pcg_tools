#!/usr/bin/env python3
"""Analyze all 4 locations where setlist names appear."""

import struct

def analyze():
    data = open('test_files/soundcheck9_25_25_combined2.PCG', 'rb').read()
    
    # Find chunk offsets
    sls1_off = data.find(b'SLS1')
    sld1_off = data.find(b'SLD1')
    sdb1_off = data.find(b'SDB1')
    sbk1_off = data.find(b'SBK1')
    
    print('Chunk offsets:')
    print(f'  SLS1: {sls1_off}')
    print(f'  SLD1: {sld1_off}')
    print(f'  SDB1: {sdb1_off}')
    print(f'  SBK1: {sbk1_off}')
    print()
    
    # Find all "NIGHTWISH LEGACY" positions
    positions = []
    pos = 0
    while True:
        pos = data.find(b'NIGHTWISH LEGACY', pos)
        if pos == -1:
            break
        positions.append(pos)
        pos += 1
    
    print(f'Found {len(positions)} occurrences of "NIGHTWISH LEGACY":')
    print()
    
    for i, pos in enumerate(positions, 1):
        # Determine which chunk it's in
        chunk = None
        chunk_offset = 0
        if pos > sbk1_off:
            chunk = 'SBK1'
            chunk_offset = sbk1_off
        elif pos > sdb1_off:
            chunk = 'SDB1'
            chunk_offset = sdb1_off
        elif pos > sld1_off:
            chunk = 'SLD1'
            chunk_offset = sld1_off
        elif pos > sls1_off:
            chunk = 'SLS1'
            chunk_offset = sls1_off
        
        offset_in_chunk = pos - chunk_offset
        
        print(f'Position {i}: {pos} (0x{pos:X})')
        print(f'  In chunk: {chunk} + {offset_in_chunk}')
        
        # Show context
        before = data[pos-30:pos]
        after = data[pos+16:pos+40]
        print(f'  Before: {before[-20:].hex()}')
        print(f'  After:  {after[:20].hex()}')
        
        # Check for marker before name
        marker_pos = pos - 4
        marker = data[marker_pos:marker_pos+4]
        print(f'  Marker at -4: {marker.hex()} ({marker})')
        
        # Check for separator after name
        sep_pos = pos + 24
        separator = data[sep_pos:sep_pos+4]
        print(f'  Separator at +24: {separator.hex()}')
        print()

if __name__ == '__main__':
    analyze()
