#!/usr/bin/env python3
"""
Analyze the region where differences were found (after SLD1 chunk).
This should contain the color/size metadata.
"""

import struct

def analyze_region():
    original = 'test_files/SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    modified = 'SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    
    with open(original, 'rb') as f:
        data1 = f.read()
    
    with open(modified, 'rb') as f:
        data2 = f.read()
    
    # Find SLD1
    sld1_pos = data1.find(b'SLD1')
    sld1_size = struct.unpack('>I', data1[sld1_pos+4:sld1_pos+8])[0]
    sld1_end = sld1_pos + 8 + sld1_size
    
    print(f"SLD1 ends at: 0x{sld1_end:08X}\n")
    
    # The difference at +462456 from SLD1 start
    # That's 96 bytes after SLD1 ends
    diff_offset = 0x00070ED8
    rel_to_sld1_end = diff_offset - sld1_end
    
    print(f"Difference found at: 0x{diff_offset:08X}")
    print(f"That's {rel_to_sld1_end} bytes after SLD1 ends\n")
    
    # Show 512 bytes starting from SLD1 end
    print("512 bytes after SLD1 chunk ends:")
    print("="*80)
    print(f"{'Offset':<12} {'Original':<50} {'Modified':<50}")
    print("-"*80)
    
    for i in range(0, 512, 16):
        offset = sld1_end + i
        
        orig_bytes = data1[offset:offset+16]
        mod_bytes = data2[offset:offset+16]
        
        orig_hex = ' '.join(f'{b:02X}' for b in orig_bytes)
        mod_hex = ' '.join(f'{b:02X}' for b in mod_bytes)
        
        # Mark if different
        marker = " <--" if orig_bytes != mod_bytes else ""
        
        print(f"+{i:4d}       {orig_hex:<50} {mod_hex:<50}{marker}")
    
    # Focus on the specific difference location
    print("\n" + "="*80)
    print("ANALYZING THE DIFFERENCE AT OFFSET +96")
    print("="*80 + "\n")
    
    # Offset +96 from SLD1 end
    meta_offset = sld1_end + 96
    
    print(f"At offset 0x{meta_offset:08X} (+96 from SLD1 end):\n")
    
    # Read 256 bytes from this location in both files
    orig_meta = data1[meta_offset:meta_offset+256]
    mod_meta = data2[meta_offset:meta_offset+256]
    
    print("Original file (first 128 bytes):")
    for i in range(0, 128, 16):
        hex_str = ' '.join(f'{b:02X}' for b in orig_meta[i:i+16])
        print(f"  +{i:3d}: {hex_str}")
    
    print("\nModified file (first 128 bytes):")
    for i in range(0, 128, 16):
        hex_str = ' '.join(f'{b:02X}' for b in mod_meta[i:i+16])
        print(f"  +{i:3d}: {hex_str}")
    
    # Check specific slot positions
    print("\n" + "="*80)
    print("CHECKING SLOT-SPECIFIC VALUES")
    print("="*80 + "\n")
    
    print("If this is a metadata array (one byte per slot):")
    print(f"\n  Slot 0 (Ghostbusters):")
    print(f"    Original (Burgundy, M):  {orig_meta[0]:3d} (0x{orig_meta[0]:02X})")
    print(f"    Modified (Indigo, XL):   {mod_meta[0]:3d} (0x{mod_meta[0]:02X})")
    
    print(f"\n  Slot 1 (Never Ending Story):")
    print(f"    Original (Olive, M):     {orig_meta[1]:3d} (0x{orig_meta[1]:02X})")
    print(f"    Modified (Burgundy, L):  {mod_meta[1]:3d} (0x{mod_meta[1]:02X})")
    
    if orig_meta[0] != mod_meta[0] or orig_meta[1] != mod_meta[1]:
        print("\n  *** VALUES CHANGED - This is likely the metadata array! ***")
    
    # Show all differences in first 128 bytes
    print("\n  All differences in first 128 bytes:")
    for i in range(128):
        if orig_meta[i] != mod_meta[i]:
            print(f"    Byte {i:3d}: {orig_meta[i]:3d} (0x{orig_meta[i]:02X}) -> {mod_meta[i]:3d} (0x{mod_meta[i]:02X})")

if __name__ == '__main__':
    analyze_region()
