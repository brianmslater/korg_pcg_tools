#!/usr/bin/env python3
"""
Search for 128-byte arrays that could be color/size metadata.
We know:
- Slot 0: Burgundy
- Slot 1: Olive
- Slot 3: Navy
- Slot 12: Indigo

These should have different byte values in a metadata array.
"""

import struct

def search_metadata(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"Searching: {filename}\n")
    
    sld1_pos = data.find(b'SLD1')
    sld1_size = struct.unpack('>I', data[sld1_pos+4:sld1_pos+8])[0]
    sld1_end = sld1_pos + 8 + sld1_size
    
    print(f"SLD1: 0x{sld1_pos:08X} to 0x{sld1_end:08X}")
    print(f"Searching for 128-byte arrays with different values at positions 0, 1, 3, 12...\n")
    
    candidates = []
    
    # Search through SLD1 chunk
    pos = sld1_pos
    while pos < sld1_end - 128:
        # Read 128 bytes
        array = data[pos:pos+128]
        
        # Check that ALL values are in range 0-15 (color/size indices)
        if all(b <= 15 for b in array):
            # Check if values at positions 0, 1, 3, 12 are different
            vals = [array[0], array[1], array[3], array[12]]
            
            # Need at least 2 different values
            if len(set(vals)) >= 2:
                candidates.append((pos, array, vals))
        
        pos += 1
    
    print(f"Found {len(candidates)} candidate arrays\n")
    
    # Show top candidates
    for i, (pos, array, vals) in enumerate(candidates[:10]):
        print(f"Candidate {i+1} at 0x{pos:08X}:")
        print(f"  Slot 0 (Burgundy): {vals[0]:3d} (0x{vals[0]:02X})")
        print(f"  Slot 1 (Olive):    {vals[1]:3d} (0x{vals[1]:02X})")
        print(f"  Slot 3 (Navy):     {vals[2]:3d} (0x{vals[2]:02X})")
        print(f"  Slot 12 (Indigo):  {vals[3]:3d} (0x{vals[3]:02X})")
        print(f"  Unique values in array: {sorted(set(array))}")
        
        # Show first 32 bytes
        hex_str = ' '.join(f'{b:02X}' for b in array[:32])
        print(f"  First 32 bytes: {hex_str}")
        print()

if __name__ == '__main__':
    search_metadata('test_files/SETLIST Movie TV Themes LOAD SEPARATELY.PCG')
