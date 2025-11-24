#!/usr/bin/env python3
"""
Compare the original and modified Movie Themes files to find color/size data.

Original:
- Slot 0: Burgundy, M
- Slot 1: Olive, M

Modified:
- Slot 0: Indigo, XL
- Slot 1: Burgundy, L
"""

import struct

def compare_files():
    original = 'test_files/SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    modified = 'SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    
    with open(original, 'rb') as f:
        data1 = f.read()
    
    with open(modified, 'rb') as f:
        data2 = f.read()
    
    print(f"Original file: {len(data1):,} bytes")
    print(f"Modified file: {len(data2):,} bytes")
    print(f"Size difference: {len(data2) - len(data1):,} bytes\n")
    
    # Find SLD1 in both
    sld1_pos1 = data1.find(b'SLD1')
    sld1_pos2 = data2.find(b'SLD1')
    
    print(f"Original SLD1 at: 0x{sld1_pos1:08X}")
    print(f"Modified SLD1 at: 0x{sld1_pos2:08X}\n")
    
    # Get SLD1 sizes
    sld1_size1 = struct.unpack('>I', data1[sld1_pos1+4:sld1_pos1+8])[0]
    sld1_size2 = struct.unpack('>I', data2[sld1_pos2+4:sld1_pos2+8])[0]
    
    print(f"Original SLD1 size: {sld1_size1:,} bytes")
    print(f"Modified SLD1 size: {sld1_size2:,} bytes\n")
    
    # Compare byte by byte in the SLD1 region
    print("Finding differences in entire SLD1 chunk...\n")
    
    differences = []
    compare_len = min(len(data1), len(data2))
    
    print(f"Comparing {compare_len:,} bytes...\n")
    
    for i in range(0, compare_len):
        if data1[i] != data2[i]:
            differences.append((i, data1[i], data2[i]))
    
    print(f"Found {len(differences)} different bytes\n")
    
    if len(differences) > 0:
        print("First 50 differences:")
        print(f"{'Offset':<12} {'Original':<12} {'Modified':<12} {'Context'}")
        print("-" * 80)
        
        for i, (offset, byte1, byte2) in enumerate(differences[:50]):
            # Show context
            context_start = max(0, offset - 8)
            context1 = data1[context_start:offset+8]
            context2 = data2[context_start:offset+8]
            
            ctx1_hex = ' '.join(f'{b:02X}' for b in context1)
            ctx2_hex = ' '.join(f'{b:02X}' for b in context2)
            
            rel_offset = offset - sld1_pos1
            print(f"0x{offset:08X}  {byte1:3d} (0x{byte1:02X})  {byte2:3d} (0x{byte2:02X})  +{rel_offset} from SLD1")
            
            if i < 10:
                print(f"  Orig: {ctx1_hex}")
                print(f"  Mod:  {ctx2_hex}")
                print()
    
    # Look for patterns - check if differences cluster in specific regions
    print("\n" + "="*80)
    print("ANALYZING DIFFERENCE PATTERNS")
    print("="*80 + "\n")
    
    if len(differences) >= 2:
        # Check if there are clusters of differences
        clusters = []
        current_cluster = [differences[0]]
        
        for i in range(1, len(differences)):
            if differences[i][0] - differences[i-1][0] < 10:
                current_cluster.append(differences[i])
            else:
                if len(current_cluster) > 0:
                    clusters.append(current_cluster)
                current_cluster = [differences[i]]
        
        if len(current_cluster) > 0:
            clusters.append(current_cluster)
        
        print(f"Found {len(clusters)} clusters of differences:\n")
        
        for i, cluster in enumerate(clusters[:10]):
            start_offset = cluster[0][0]
            end_offset = cluster[-1][0]
            rel_start = start_offset - sld1_pos1
            
            print(f"Cluster {i+1}: 0x{start_offset:08X} to 0x{end_offset:08X} (+{rel_start} from SLD1)")
            print(f"  {len(cluster)} bytes changed")
            
            # Show the changed bytes
            orig_bytes = [b1 for _, b1, _ in cluster]
            mod_bytes = [b2 for _, _, b2 in cluster]
            
            print(f"  Original: {' '.join(f'{b:02X}' for b in orig_bytes[:16])}")
            print(f"  Modified: {' '.join(f'{b:02X}' for b in mod_bytes[:16])}")
            print()

if __name__ == '__main__':
    compare_files()
