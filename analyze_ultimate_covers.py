#!/usr/bin/env python3
"""
Analyze the Ultimate Covers (narf) PCG file for text size and color values in setlist slots.
"""

import struct

def analyze_pcg_file(filename):
    """Analyze PCG file for setlist slot metadata including text size and color."""
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"File: {filename}")
    print(f"File size: {len(data):,} bytes\n")
    
    # Find SLD1 chunk
    sld1_pos = data.find(b'SLD1')
    if sld1_pos == -1:
        print("No SLD1 chunk found - no setlist data")
        return
    
    print(f"SLD1 chunk found at: 0x{sld1_pos:08X}")
    
    # Read SLD1 chunk size (4 bytes after 'SLD1')
    chunk_size = struct.unpack('>I', data[sld1_pos+4:sld1_pos+8])[0]
    print(f"SLD1 chunk size: {chunk_size} bytes\n")
    
    # Show hex dump of first 64 bytes after SLD1
    print("First 64 bytes after SLD1 header:")
    for i in range(0, 64, 16):
        offset = sld1_pos + 8 + i
        hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
        print(f"  {offset:08X}: {hex_str:<48} {ascii_str}")
    print()
    
    # Look for SDB1 (Set Data Bank) which contains the slot data
    sdb1_pos = data.find(b'SDB1', sld1_pos)
    if sdb1_pos == -1:
        print("No SDB1 found")
        return
    
    print(f"SDB1 found at: 0x{sdb1_pos:08X}")
    
    # The setlist name appears to be at SDB1 + 24
    # Let's find where the actual slot data starts
    # Looking at the hex dump, "Preload Set List" starts at offset 0x78
    # That's SDB1 + 16
    
    setlist_name_offset = sdb1_pos + 16
    setlist_name = data[setlist_name_offset:setlist_name_offset+24].rstrip(b'\x00').decode('ascii', errors='replace')
    print(f"Setlist name: '{setlist_name}'")
    
    # Now find where slots start - look for a pattern of readable text
    # Slots appear to start after the setlist name
    slot_start = setlist_name_offset + 24
    
    print(f"\nSlot data starts at: 0x{slot_start:08X}\n")
    
    # Each slot is 32 bytes
    slot_size = 32
    
    print("Analyzing first 20 slots for text size and color patterns:\n")
    print(f"{'Slot':<4} {'Name':<30} {'Bytes 24-31 (hex)':<40}")
    print("-" * 80)
    
    for i in range(20):
        slot_offset = slot_start + (i * slot_size)
        if slot_offset + slot_size > len(data):
            break
        
        slot_data = data[slot_offset:slot_offset + slot_size]
        
        # First 24 bytes are the name (null-padded)
        name_bytes = slot_data[:24]
        name = name_bytes.rstrip(b'\x00').decode('ascii', errors='replace')
        
        # Last 8 bytes are metadata
        metadata = slot_data[24:32]
        metadata_hex = ' '.join(f'{b:02X}' for b in metadata)
        
        print(f"{i:<4} {name:<30} {metadata_hex:<40}")
    
    print("\n" + "="*80)
    print("DETAILED ANALYSIS OF METADATA BYTES")
    print("="*80 + "\n")
    
    # Analyze patterns in the metadata bytes
    print("Looking for patterns in bytes 24-31 across all slots:\n")
    
    # Collect all metadata
    all_metadata = []
    slot_names = []
    for i in range(128):  # Max 128 slots
        slot_offset = slot_start + (i * slot_size)
        if slot_offset + slot_size > len(data):
            break
        
        slot_data = data[slot_offset:slot_offset + slot_size]
        name_bytes = slot_data[:24]
        name = name_bytes.rstrip(b'\x00').decode('ascii', errors='replace')
        
        if not name:  # Empty slot
            continue
            
        metadata = slot_data[24:32]
        all_metadata.append(metadata)
        slot_names.append(name)
    
    print(f"Found {len(all_metadata)} non-empty slots\n")
    
    # Analyze each byte position
    for byte_pos in range(8):
        values = [m[byte_pos] for m in all_metadata]
        unique_values = set(values)
        
        print(f"Byte {24 + byte_pos} (offset +{byte_pos} in metadata):")
        print(f"  Unique values: {sorted(unique_values)}")
        
        if len(unique_values) <= 10:
            # Show which slots have which values
            value_counts = {}
            for val in unique_values:
                count = values.count(val)
                value_counts[val] = count
            
            print(f"  Value distribution:")
            for val in sorted(value_counts.keys()):
                print(f"    {val:3d} (0x{val:02X}): {value_counts[val]:3d} slots")
                
                # Show a few example slot names for this value
                examples = [slot_names[i] for i, v in enumerate(values) if v == val][:3]
                if examples:
                    print(f"         Examples: {', '.join(examples)}")
        print()
    
    # Look for color patterns (typically RGB or indexed colors)
    print("\n" + "="*80)
    print("POTENTIAL COLOR/SIZE CANDIDATES")
    print("="*80 + "\n")
    
    # Check for bytes with small ranges (0-15 could be colors or sizes)
    for byte_pos in range(8):
        values = [m[byte_pos] for m in all_metadata]
        unique_values = set(values)
        max_val = max(values)
        min_val = min(values)
        
        if max_val <= 15 and len(unique_values) > 1:
            print(f"Byte {24 + byte_pos}: Range {min_val}-{max_val}, {len(unique_values)} unique values")
            print(f"  Could be: Color index or Text size")
            print(f"  Values: {sorted(unique_values)}")
            
            # Show examples
            for val in sorted(unique_values)[:5]:
                examples = [slot_names[i] for i, v in enumerate(values) if v == val][:2]
                print(f"    Value {val}: {', '.join(examples)}")
            print()

if __name__ == '__main__':
    # Analyze the narf (Ultimate Covers) file
    analyze_pcg_file('test_files/narf_modified.PCG')
