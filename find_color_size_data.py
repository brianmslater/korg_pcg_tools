#!/usr/bin/env python3
"""
Search for color and text size data in the Movie Themes file.
Looking beyond just the slot names - checking for separate metadata sections.
"""

import struct

def find_metadata(filename):
    """Search for color/size metadata."""
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"File: {filename}")
    print(f"File size: {len(data):,} bytes\n")
    
    # Find SLD1
    sld1_pos = data.find(b'SLD1')
    sld1_size = struct.unpack('>I', data[sld1_pos+4:sld1_pos+8])[0]
    sld1_end = sld1_pos + 8 + sld1_size
    
    print(f"SLD1: 0x{sld1_pos:08X} to 0x{sld1_end:08X} (size: {sld1_size:,} bytes)\n")
    
    # Find all chunks within SLD1
    print("Chunks within SLD1:")
    pos = sld1_pos + 8
    while pos < sld1_end - 8:
        # Look for 4-letter chunk IDs
        chunk_id = data[pos:pos+4]
        if chunk_id.isalpha() or (chunk_id[0:3].isalpha() and chunk_id[3:4].isdigit()):
            chunk_size = struct.unpack('>I', data[pos+4:pos+8])[0]
            print(f"  {chunk_id.decode('ascii', errors='replace')} at 0x{pos:08X}, size: {chunk_size:,} bytes")
            
            # Show first 64 bytes of this chunk
            print(f"    First 64 bytes:")
            for i in range(0, min(64, chunk_size), 16):
                offset = pos + 8 + i
                hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
                ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
                print(f"      +{i:3d}: {hex_str:<48} {ascii_str}")
            
            pos += 8 + chunk_size
        else:
            pos += 1
    
    # Look for patterns that might be color/size arrays
    print("\n" + "="*80)
    print("SEARCHING FOR METADATA ARRAYS")
    print("="*80 + "\n")
    
    # Look for arrays of small values (0-15) that could be colors or sizes
    # Search in the SLD1 chunk
    print("Looking for sequences of bytes in range 0-15...")
    
    pos = sld1_pos
    sequences = []
    
    while pos < sld1_end - 128:
        # Check if we have a sequence of at least 16 bytes where most are 0-15
        window = data[pos:pos+128]
        small_count = sum(1 for b in window if 0 <= b <= 15)
        
        if small_count >= 100:  # At least 100 out of 128 are small values
            # This might be a metadata array
            sequences.append(pos)
            pos += 128
        else:
            pos += 1
    
    if sequences:
        print(f"\nFound {len(sequences)} potential metadata sequences:")
        for seq_pos in sequences[:5]:
            print(f"\n  At 0x{seq_pos:08X}:")
            # Show first 128 bytes
            for i in range(0, 128, 16):
                offset = seq_pos + i
                hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
                vals = [b for b in data[offset:offset+16]]
                print(f"    +{i:3d}: {hex_str:<48} values: {vals}")
    
    # Look specifically after all the slot names
    print("\n" + "="*80)
    print("CHECKING DATA AFTER ALL SLOT NAMES")
    print("="*80 + "\n")
    
    # Find where slot names end (128 slots)
    sdb1_pos = data.find(b'SDB1', sld1_pos)
    first_slot = sdb1_pos + 16 + 24 + 4  # SDB1 + setlist name + separator
    
    # Each slot: 4-byte marker + 24-byte name = 28 bytes (except first has no marker)
    # First slot: 24 bytes
    # Next 127 slots: 127 * 28 = 3556 bytes
    # Total: 24 + 3556 = 3580 bytes
    
    slots_end = first_slot + 24 + (127 * 28)
    print(f"Slots should end around: 0x{slots_end:08X}")
    print(f"Checking next 512 bytes after slots:\n")
    
    for i in range(0, 512, 16):
        offset = slots_end + i
        if offset + 16 > len(data):
            break
        hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
        
        # Highlight if we see small values
        vals = [b for b in data[offset:offset+16]]
        small_vals = [b for b in vals if 0 <= b <= 15]
        marker = " <-- SMALL VALUES" if len(small_vals) >= 8 else ""
        
        print(f"  +{i:4d}: {hex_str:<48} {ascii_str}{marker}")

if __name__ == '__main__':
    find_metadata('test_files/SETLIST Movie TV Themes LOAD SEPARATELY.PCG')
