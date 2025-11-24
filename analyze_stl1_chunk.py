#!/usr/bin/env python3
"""
Analyze the STL1 chunk which appears after SLD1.
This might contain the color/size metadata.
"""

import struct

def analyze_stl1():
    original = 'test_files/SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    modified = 'SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    
    with open(original, 'rb') as f:
        data1 = f.read()
    
    with open(modified, 'rb') as f:
        data2 = f.read()
    
    # Find STL1 chunk
    stl1_pos = data1.find(b'STL1')
    
    if stl1_pos < 0:
        print("No STL1 chunk found")
        return
    
    print(f"STL1 chunk at: 0x{stl1_pos:08X}\n")
    
    # STL1 structure
    stl1_size1 = struct.unpack('>I', data1[stl1_pos+4:stl1_pos+8])[0]
    stl1_size2 = struct.unpack('>I', data2[stl1_pos+4:stl1_pos+8])[0]
    
    print(f"Original STL1 size: {stl1_size1:,} bytes")
    print(f"Modified STL1 size: {stl1_size2:,} bytes\n")
    
    # Show first 512 bytes of STL1 data
    print("First 512 bytes of STL1 chunk:")
    print("="*80)
    
    for i in range(0, 512, 16):
        offset = stl1_pos + 8 + i
        
        orig_bytes = data1[offset:offset+16]
        mod_bytes = data2[offset:offset+16]
        
        orig_hex = ' '.join(f'{b:02X}' for b in orig_bytes)
        mod_hex = ' '.join(f'{b:02X}' for b in mod_bytes)
        
        marker = " <-- DIFF" if orig_bytes != mod_bytes else ""
        
        print(f"+{i:4d}: Orig: {orig_hex}")
        print(f"       Mod:  {mod_hex}{marker}")
        if marker:
            # Show which bytes differ
            diffs = [j for j in range(16) if orig_bytes[j] != mod_bytes[j]]
            print(f"       Diff at positions: {diffs}")
            for j in diffs:
                print(f"         [{j}]: {orig_bytes[j]:3d} (0x{orig_bytes[j]:02X}) -> {mod_bytes[j]:3d} (0x{mod_bytes[j]:02X})")
        print()
    
    # Look for SBK1 (Set Bank) within STL1
    sbk1_pos = data1.find(b'SBK1', stl1_pos)
    if sbk1_pos > 0:
        print(f"\nSBK1 found at: 0x{sbk1_pos:08X}")
        sbk1_size = struct.unpack('>I', data1[sbk1_pos+4:sbk1_pos+8])[0]
        print(f"SBK1 size: {sbk1_size:,} bytes\n")
        
        # Show first 256 bytes of SBK1
        print("First 256 bytes of SBK1:")
        for i in range(0, 256, 16):
            offset = sbk1_pos + 8 + i
            
            orig_bytes = data1[offset:offset+16]
            mod_bytes = data2[offset:offset+16]
            
            orig_hex = ' '.join(f'{b:02X}' for b in orig_bytes)
            mod_hex = ' '.join(f'{b:02X}' for b in mod_bytes)
            
            marker = " <-- DIFF" if orig_bytes != mod_bytes else ""
            
            print(f"+{i:4d}: Orig: {orig_hex}")
            print(f"       Mod:  {mod_hex}{marker}")
            if marker:
                diffs = [j for j in range(16) if orig_bytes[j] != mod_bytes[j]]
                for j in diffs:
                    print(f"         [{j}]: {orig_bytes[j]:3d} -> {mod_bytes[j]:3d}")
            print()

if __name__ == '__main__':
    analyze_stl1()
