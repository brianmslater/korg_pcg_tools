#!/usr/bin/env python3
"""Analyze SLS1 chunk for color and text size metadata."""

import struct

def get_string(data, offset, length):
    """Read null-terminated ASCII string."""
    string_data = data[offset:offset+length]
    null_pos = string_data.find(b'\x00')
    if null_pos >= 0:
        string_data = string_data[:null_pos]
    return string_data.decode('ascii', errors='ignore').strip()

def hex_dump(data, offset, length):
    """Print hex dump."""
    for i in range(0, length, 16):
        if offset+i >= len(data):
            break
        hex_str = ' '.join(f'{b:02X}' for b in data[offset+i:offset+i+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset+i:offset+i+16])
        print(f"  {offset+i:08X}: {hex_str:<48} {ascii_str}")

def analyze_sls1_metadata(filename):
    """Analyze SLS1 for metadata."""
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Find SLS1
    sls1_pos = data.find(b'SLS1')
    if sls1_pos < 0:
        print("No SLS1 found")
        return
    
    print(f"SLS1 at 0x{sls1_pos:08X}\n")
    
    # Look for the NEW format separator
    separator = b'\x28\x0F\x01\x00'
    marker = b'\x1E\x02\x00\x00'
    
    # Find first setlist in NEW format
    sep_pos = data.find(separator, sls1_pos)
    if sep_pos < 0:
        print("No NEW format separator found")
        return
    
    print(f"Found separator at 0x{sep_pos:08X}")
    
    # Setlist name should be 24 bytes before separator
    setlist_name_pos = sep_pos - 24
    setlist_name = get_string(data, setlist_name_pos, 24)
    print(f"Setlist name: '{setlist_name}'")
    
    # After separator, first slot name (no marker)
    first_slot_pos = sep_pos + 4
    first_slot_name = get_string(data, first_slot_pos, 24)
    print(f"\nFirst slot name: '{first_slot_name}'")
    
    # Show bytes after first slot name
    print(f"\nBytes after first slot name:")
    hex_dump(data, first_slot_pos, 64)
    
    # Check for metadata after the name
    print(f"\nBytes at various offsets from first slot name:")
    for offset in [24, 25, 26, 27, 28, 29, 30]:
        byte_val = data[first_slot_pos + offset]
        print(f"  +{offset}: 0x{byte_val:02X} ({byte_val})")
    
    # Second slot (with marker)
    second_slot_pos = first_slot_pos + 24  # After first slot name
    print(f"\nSecond slot area:")
    hex_dump(data, second_slot_pos, 64)
    
    # Check if there's a marker
    if data[second_slot_pos:second_slot_pos+4] == marker:
        print(f"\nFound marker at second slot")
        second_slot_name = get_string(data, second_slot_pos + 4, 24)
        print(f"Second slot name: '{second_slot_name}'")
        
        # Bytes after second slot name
        print(f"\nBytes after second slot name:")
        for offset in [24, 25, 26, 27, 28, 29, 30]:
            byte_val = data[second_slot_pos + 4 + offset]
            print(f"  +{offset}: 0x{byte_val:02X} ({byte_val})")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    
    analyze_sls1_metadata(filename)
