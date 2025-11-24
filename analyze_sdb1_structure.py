#!/usr/bin/env python3
"""
Analyze the SDB1 chunk structure in detail.
Looking for color/size metadata arrays.
"""

import struct

def analyze_sdb1(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"Analyzing: {filename}\n")
    
    # Find SDB1
    sdb1_pos = data.find(b'SDB1')
    sdb1_size = struct.unpack('>I', data[sdb1_pos+4:sdb1_pos+8])[0]
    
    print(f"SDB1 at: 0x{sdb1_pos:08X}")
    print(f"SDB1 size: {sdb1_size:,} bytes\n")
    
    # Show first 512 bytes of SDB1 data
    print("First 512 bytes of SDB1 data:")
    print("="*80)
    for i in range(0, 512, 16):
        offset = sdb1_pos + 8 + i
        hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
        print(f"  +{i:4d} (0x{offset:08X}): {hex_str:<48} {ascii_str}")
    
    # The setlist name starts at +16
    setlist_name_offset = sdb1_pos + 8 + 16
    setlist_name = data[setlist_name_offset:setlist_name_offset+24].rstrip(b'\x00').decode('ascii', errors='replace')
    print(f"\nSetlist name at +16: '{setlist_name}'")
    
    # Check the first 16 bytes - might be metadata
    print("\nFirst 16 bytes of SDB1 (before setlist name):")
    first_16 = data[sdb1_pos+8:sdb1_pos+24]
    hex_str = ' '.join(f'{b:02X}' for b in first_16)
    print(f"  {hex_str}")
    print(f"  As integers: {list(first_16)}")
    
    # Parse as potential structure
    print("\nParsing first 16 bytes:")
    print(f"  Bytes 0-3:   {struct.unpack('>I', first_16[0:4])[0]:10d} (0x{struct.unpack('>I', first_16[0:4])[0]:08X})")
    print(f"  Bytes 4-7:   {struct.unpack('>I', first_16[4:8])[0]:10d} (0x{struct.unpack('>I', first_16[4:8])[0]:08X})")
    print(f"  Bytes 8-11:  {struct.unpack('>I', first_16[8:12])[0]:10d} (0x{struct.unpack('>I', first_16[8:12])[0]:08X})")
    print(f"  Bytes 12-15: {struct.unpack('>I', first_16[12:16])[0]:10d} (0x{struct.unpack('>I', first_16[12:16])[0]:08X})")
    
    # 0x0E1C = 3612 bytes - size of ONE setlist's slot names
    # With 16 setlists, that's 16 × 3612 = 57,792 bytes (0xE1C0)
    # Metadata should be AFTER all 16 setlists
    
    one_setlist_size = 0x0E1C
    all_setlists_size = 16 * one_setlist_size
    
    print(f"\nOne setlist size: {one_setlist_size} bytes (0x{one_setlist_size:04X})")
    print(f"All 16 setlists: {all_setlists_size} bytes (0x{all_setlists_size:04X})")
    
    potential_metadata_offset = sdb1_pos + 8 + all_setlists_size
    print(f"\nChecking after all 16 setlists:")
    print(f"  Absolute position: 0x{potential_metadata_offset:08X}")
    print(f"  First 256 bytes at this location:")
    
    for i in range(0, 256, 16):
        offset = potential_metadata_offset + i
        hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
        
        # Check if this looks like metadata (small values)
        vals = [b for b in data[offset:offset+16]]
        small_count = sum(1 for v in vals if 0 <= v <= 15)
        marker = f" <-- {small_count}/16 small" if small_count >= 12 else ""
        
        print(f"  +{i:4d}: {hex_str:<48} {ascii_str}{marker}")
    
    # Check specific slot positions in this potential metadata array
    print("\n" + "="*80)
    print("CHECKING POTENTIAL COLOR ARRAY")
    print("="*80)
    print(f"\nIf this is a color array at 0x{potential_metadata_offset:08X}:")
    print(f"  Slot 0 (Burgundy): {data[potential_metadata_offset + 0]:3d} (0x{data[potential_metadata_offset + 0]:02X})")
    print(f"  Slot 1 (Olive):    {data[potential_metadata_offset + 1]:3d} (0x{data[potential_metadata_offset + 1]:02X})")
    print(f"  Slot 3 (Navy):     {data[potential_metadata_offset + 3]:3d} (0x{data[potential_metadata_offset + 3]:02X})")
    print(f"  Slot 12 (Indigo):  {data[potential_metadata_offset + 12]:3d} (0x{data[potential_metadata_offset + 12]:02X})")
    
    test_vals = [
        data[potential_metadata_offset + 0],
        data[potential_metadata_offset + 1],
        data[potential_metadata_offset + 3],
        data[potential_metadata_offset + 12]
    ]
    
    if len(set(test_vals)) > 1:
        print("\n  *** DIFFERENT VALUES - This could be the color array! ***")
        print(f"\n  Unique values: {sorted(set(test_vals))}")
    else:
        print("\n  All same values - not the color array")

if __name__ == '__main__':
    analyze_sdb1('test_files/SETLIST Movie TV Themes LOAD SEPARATELY.PCG')
