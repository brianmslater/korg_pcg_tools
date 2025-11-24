#!/usr/bin/env python3
"""
Analyze setlist slot metadata for text size and color values.
Based on the actual slot structure: 7810 bytes (0x1E82) per slot.
"""

import struct

def analyze_slot_metadata(filename):
    """Analyze slot metadata in SLD1 chunk."""
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"File: {filename}")
    print(f"File size: {len(data):,} bytes\n")
    
    # Find SLD1 chunk
    sld1_pos = data.find(b'SLD1')
    if sld1_pos == -1:
        print("No SLD1 chunk found")
        return
    
    print(f"SLD1 chunk found at: 0x{sld1_pos:08X}")
    
    # Show hex dump after SLD1 to understand structure
    print("\nFirst 128 bytes after SLD1 header:")
    for i in range(0, 128, 16):
        offset = sld1_pos + 8 + i
        hex_str = ' '.join(f'{b:02X}' for b in data[offset:offset+16])
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[offset:offset+16])
        print(f"  {offset:08X}: {hex_str:<48} {ascii_str}")
    
    # Find SDB1 (Set Data Bank)
    sdb1_pos = data.find(b'SDB1', sld1_pos)
    if sdb1_pos == -1:
        print("\nNo SDB1 found")
        return
    
    print(f"\nSDB1 found at: 0x{sdb1_pos:08X}")
    
    # Look for the actual slot data structure
    # The SLD1 chunk contains full slot data (7810 bytes per slot)
    # Look for a pattern that indicates slot data
    
    # Try to find slot data by looking for CBK1 markers
    cbk1_pos = data.find(b'CBK1', sld1_pos)
    
    if cbk1_pos > 0:
        print(f"\nFound CBK1 at: 0x{cbk1_pos:08X}")
        print("This appears to be full SLD1 format with 7810-byte slots")
        SLOT_SIZE = 0x1E82  # 7810 bytes
        first_slot_start = cbk1_pos
    else:
        print("\nNo CBK1 found - this appears to be SLS1 format (names only)")
        print("SLS1 format doesn't contain color/text size metadata")
        print("Looking for SDB1 structure instead...")
        
        # Slots appear to start after the setlist name
        # Setlist name is at SDB1 + 16
        setlist_name_offset = sdb1_pos + 16
        setlist_name = data[setlist_name_offset:setlist_name_offset+24].rstrip(b'\x00').decode('ascii', errors='replace')
        print(f"Setlist name: '{setlist_name}'")
        print("\nNote: This file format doesn't store color/text size in the PCG file.")
        print("These are display-only settings on the Kronos itself.")
        return
    
    print(f"First slot data at: 0x{first_slot_start:08X}")
    
    print(f"Slot size: {SLOT_SIZE} bytes (0x{SLOT_SIZE:04X})\n")
    
    # Analyze first 10 slots
    print("First 10 slots:")
    print(f"{'#':<3} {'Name':<30} {'Offset':<12}")
    print("-" * 50)
    
    for i in range(10):
        slot_offset = first_slot_start + (i * SLOT_SIZE)
        name_offset = slot_offset + 24
        
        if name_offset + 24 > len(data):
            break
        
        name_bytes = data[name_offset:name_offset + 24]
        name = name_bytes.rstrip(b'\x00').decode('ascii', errors='replace')
        
        print(f"{i:<3} {name:<30} 0x{slot_offset:08X}")
    
    print("\n" + "="*80)
    print("SEARCHING FOR TEXT SIZE AND COLOR METADATA")
    print("="*80 + "\n")
    
    # Look for metadata near the beginning of each slot
    # Check first 200 bytes of each slot for patterns
    print("Analyzing first 200 bytes of each slot for metadata patterns:\n")
    
    # Collect data from first 20 slots
    slot_data_samples = []
    for i in range(20):
        slot_offset = first_slot_start + (i * SLOT_SIZE)
        name_offset = slot_offset + 24
        
        if name_offset + 200 > len(data):
            break
        
        name = data[name_offset:name_offset + 24].rstrip(b'\x00').decode('ascii', errors='replace')
        
        # Get bytes after the name (potential metadata area)
        metadata_start = name_offset + 24
        metadata = data[metadata_start:metadata_start + 32]
        
        slot_data_samples.append((i, name, metadata))
    
    # Show metadata for first 10 slots
    print("Bytes immediately after slot name (24 bytes after name start):")
    print(f"{'Slot':<4} {'Name':<30} {'Bytes +24 to +31 (hex)':<40}")
    print("-" * 80)
    
    for i, name, metadata in slot_data_samples[:10]:
        hex_str = ' '.join(f'{b:02X}' for b in metadata[:8])
        print(f"{i:<4} {name:<30} {hex_str:<40}")
    
    print("\n" + "-"*80)
    print("Extended metadata (bytes +24 to +55):")
    print("-" * 80)
    
    for i, name, metadata in slot_data_samples[:5]:
        print(f"\nSlot {i}: {name}")
        for j in range(0, 32, 16):
            hex_str = ' '.join(f'{b:02X}' for b in metadata[j:j+16])
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in metadata[j:j+16])
            print(f"  +{24+j:3d}: {hex_str:<48} {ascii_str}")
    
    # Look for bytes with small values (potential color/size indicators)
    print("\n" + "="*80)
    print("ANALYZING BYTE PATTERNS FOR COLOR/SIZE CANDIDATES")
    print("="*80 + "\n")
    
    for byte_pos in range(32):
        values = [m[byte_pos] for _, _, m in slot_data_samples if len(m) > byte_pos]
        unique_values = set(values)
        max_val = max(values) if values else 0
        min_val = min(values) if values else 0
        
        # Look for bytes with small ranges (0-15 could be colors or text sizes)
        if max_val <= 15 and len(unique_values) > 1:
            print(f"Byte +{24 + byte_pos}: Range {min_val}-{max_val}, {len(unique_values)} unique values")
            print(f"  Values: {sorted(unique_values)}")
            print(f"  Could be: Color index or Text size setting")
            
            # Show which slots have which values
            for val in sorted(unique_values):
                examples = [name for i, name, m in slot_data_samples if len(m) > byte_pos and m[byte_pos] == val][:3]
                print(f"    {val}: {', '.join(examples)}")
            print()

if __name__ == '__main__':
    import sys
    filename = sys.argv[1] if len(sys.argv) > 1 else 'test_files/files/GLAM V3/GLAMV3_modified.PCG'
    analyze_slot_metadata(filename)
