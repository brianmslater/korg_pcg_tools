#!/usr/bin/env python3
"""
Detailed analysis of Movie Themes file to find text size and color metadata.
Looking at the complete SLD1 structure, not just slot names.
"""

import struct

def analyze_detailed(filename):
    """Deep analysis of SLD1 structure."""
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"File: {filename}")
    print(f"File size: {len(data):,} bytes\n")
    
    # Find SLD1
    sld1_pos = data.find(b'SLD1')
    if sld1_pos == -1:
        print("No SLD1 found")
        return
    
    print(f"SLD1 at: 0x{sld1_pos:08X}")
    
    # Get SLD1 size
    sld1_size = struct.unpack('>I', data[sld1_pos+4:sld1_pos+8])[0]
    print(f"SLD1 size: {sld1_size:,} bytes (0x{sld1_size:08X})")
    print(f"SLD1 ends at: 0x{sld1_pos + 8 + sld1_size:08X}\n")
    
    # Find SDB1
    sdb1_pos = data.find(b'SDB1', sld1_pos)
    print(f"SDB1 at: 0x{sdb1_pos:08X}")
    
    # Setlist name
    setlist_name_pos = sdb1_pos + 16
    setlist_name = data[setlist_name_pos:setlist_name_pos+24].rstrip(b'\x00').decode('ascii', errors='replace')
    print(f"Setlist name: '{setlist_name}'")
    
    # After setlist name, there's a separator then slot names
    separator_pos = setlist_name_pos + 24
    separator = data[separator_pos:separator_pos+4]
    print(f"Separator: {' '.join(f'{b:02X}' for b in separator)}")
    
    # First slot starts after separator
    first_slot_pos = separator_pos + 4
    print(f"\nFirst slot at: 0x{first_slot_pos:08X}")
    
    # Read first 20 slots with extended data
    print("\nFirst 20 slots with ALL data after name:")
    print("="*100)
    
    current_pos = first_slot_pos
    slot_num = 0
    
    # First slot has NO marker
    name = data[current_pos:current_pos+24].rstrip(b'\x00').decode('ascii', errors='replace')
    print(f"\nSlot {slot_num}: '{name}'")
    print(f"  Position: 0x{current_pos:08X}")
    
    # Show next 64 bytes after the name
    metadata_pos = current_pos + 24
    print(f"  Next 64 bytes after name:")
    for i in range(0, 64, 16):
        offset = metadata_pos + i
        hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
        print(f"    +{24+i:3d}: {hex_str:<48} {ascii_str}")
    
    current_pos += 24  # Move past first slot name
    
    # Read next 19 slots (with markers)
    marker = b'\x1E\x02\x00\x00'
    
    for slot_num in range(1, 20):
        # Check for marker
        check_marker = data[current_pos:current_pos+4]
        
        if check_marker != marker:
            print(f"\nSlot {slot_num}: No marker found at 0x{current_pos:08X}")
            print(f"  Found: {' '.join(f'{b:02X}' for b in check_marker)}")
            # Try to find next marker
            next_marker = data.find(marker, current_pos, current_pos + 100)
            if next_marker > 0:
                print(f"  Next marker at: 0x{next_marker:08X} (skip {next_marker - current_pos} bytes)")
                current_pos = next_marker
            else:
                break
        
        current_pos += 4  # Skip marker
        
        # Read name
        name = data[current_pos:current_pos+24].rstrip(b'\x00').decode('ascii', errors='replace')
        print(f"\nSlot {slot_num}: '{name}'")
        print(f"  Position: 0x{current_pos:08X}")
        
        # Show next 64 bytes after the name
        metadata_pos = current_pos + 24
        print(f"  Next 64 bytes after name:")
        for i in range(0, 64, 16):
            offset = metadata_pos + i
            if offset + 16 > len(data):
                break
            hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
            print(f"    +{24+i:3d}: {hex_str:<48} {ascii_str}")
        
        current_pos += 24  # Move past slot name
    
    print("\n" + "="*100)
    print("LOOKING FOR PATTERNS IN THE DATA BETWEEN SLOTS")
    print("="*100)
    
    # Go back and collect the bytes BETWEEN slot names
    current_pos = first_slot_pos + 24  # After first slot name
    
    between_data = []
    
    for slot_num in range(1, 20):
        # Find next marker
        next_marker = data.find(marker, current_pos, current_pos + 100)
        if next_marker < 0:
            break
        
        # Data between this slot and next marker
        gap_data = data[current_pos:next_marker]
        if len(gap_data) > 0:
            between_data.append((slot_num - 1, gap_data))
        
        current_pos = next_marker + 4 + 24  # Skip marker and next name
    
    if between_data:
        print(f"\nFound {len(between_data)} gaps between slots:")
        for slot_num, gap in between_data[:10]:
            print(f"\nAfter slot {slot_num}: {len(gap)} bytes")
            if len(gap) <= 32:
                hex_str = ' '.join(f'{b:02X}' for b in gap)
                print(f"  Data: {hex_str}")
                
                # Look for small values that could be color/size
                small_vals = [b for b in gap if 0 <= b <= 15]
                if small_vals:
                    print(f"  Small values (0-15): {small_vals}")

if __name__ == '__main__':
    analyze_detailed('test_files/SETLIST Movie TV Themes LOAD SEPARATELY.PCG')
