#!/usr/bin/env python3
"""
Deep analysis of ALL chunk structures to understand where setlist data is stored.
This will help us identify ALL locations that need to be updated when writing.
"""

import struct
from pathlib import Path

def analyze_chunk_structure(pcg_file):
    """Analyze all chunks in a PCG file to find setlist data locations."""
    
    with open(pcg_file, 'rb') as f:
        data = f.read()
    
    print(f"Analyzing: {pcg_file}")
    print(f"File size: {len(data):,} bytes")
    print("=" * 80)
    
    # Find all chunks
    chunks = []
    pos = 0
    while pos < len(data) - 8:
        # Look for 4-byte chunk IDs followed by size
        chunk_id = data[pos:pos+4]
        if len(chunk_id) == 4 and all(32 <= b <= 126 for b in chunk_id):
            try:
                size = struct.unpack('<I', data[pos+4:pos+8])[0]
                if 0 < size < len(data):
                    chunks.append({
                        'id': chunk_id.decode('ascii'),
                        'offset': pos,
                        'size': size,
                        'data_start': pos + 8,
                        'data_end': pos + 8 + size
                    })
                    print(f"\nChunk: {chunk_id.decode('ascii')}")
                    print(f"  Offset: {pos} (0x{pos:08X})")
                    print(f"  Size: {size:,} bytes")
                    pos += 8 + size
                    continue
            except:
                pass
        pos += 1
    
    print(f"\n\nFound {len(chunks)} chunks")
    print("=" * 80)
    
    # Search for "NIGHTWISH LEGACY" in each chunk
    search_name = b"NIGHTWISH LEGACY"
    
    print(f"\n\nSearching for '{search_name.decode()}' in each chunk:")
    print("=" * 80)
    
    for chunk in chunks:
        chunk_data = data[chunk['data_start']:chunk['data_end']]
        occurrences = []
        
        pos = 0
        while pos < len(chunk_data):
            idx = chunk_data.find(search_name, pos)
            if idx == -1:
                break
            
            # Calculate absolute file position
            abs_pos = chunk['data_start'] + idx
            occurrences.append({
                'chunk_offset': idx,
                'file_offset': abs_pos
            })
            pos = idx + 1
        
        if occurrences:
            print(f"\n{chunk['id']} chunk:")
            for i, occ in enumerate(occurrences, 1):
                print(f"  Occurrence {i}:")
                print(f"    Chunk offset: {occ['chunk_offset']} (0x{occ['chunk_offset']:08X})")
                print(f"    File offset: {occ['file_offset']} (0x{occ['file_offset']:08X})")
                
                # Show context around the name
                start = max(0, occ['chunk_offset'] - 32)
                end = min(len(chunk_data), occ['chunk_offset'] + len(search_name) + 32)
                context = chunk_data[start:end]
                
                print(f"    Context (hex):")
                for j in range(0, len(context), 16):
                    hex_str = ' '.join(f'{b:02X}' for b in context[j:j+16])
                    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in context[j:j+16])
                    print(f"      {hex_str:<48} {ascii_str}")
    
    # Analyze SLS1 structure specifically
    print("\n\n" + "=" * 80)
    print("DETAILED SLS1 STRUCTURE ANALYSIS")
    print("=" * 80)
    
    sls1_chunk = next((c for c in chunks if c['id'] == 'SLS1'), None)
    if sls1_chunk:
        chunk_data = data[sls1_chunk['data_start']:sls1_chunk['data_end']]
        
        print(f"\nSLS1 chunk size: {len(chunk_data):,} bytes")
        
        # Look for the marker pattern
        marker = bytes([0x1E, 0x02, 0x00, 0x00])
        pos = 0
        setlist_count = 0
        
        while pos < len(chunk_data):
            idx = chunk_data.find(marker, pos)
            if idx == -1:
                break
            
            setlist_count += 1
            print(f"\n--- Setlist {setlist_count} ---")
            print(f"Marker at chunk offset: {idx} (0x{idx:08X})")
            print(f"File offset: {sls1_chunk['data_start'] + idx} (0x{sls1_chunk['data_start'] + idx:08X})")
            
            # Extract setlist name (should be right after marker)
            name_start = idx + 4
            name_end = name_start + 24  # Setlist names are 24 bytes
            name_bytes = chunk_data[name_start:name_end]
            name = name_bytes.rstrip(b'\x00').decode('ascii', errors='ignore')
            print(f"Setlist name: '{name}'")
            
            # Look for separator after name
            sep_pos = name_end
            separator = chunk_data[sep_pos:sep_pos+4]
            print(f"Separator: {' '.join(f'{b:02X}' for b in separator)}")
            
            # Count slots (look for next marker or end)
            slot_start = sep_pos + 4
            next_marker = chunk_data.find(marker, idx + 1)
            if next_marker == -1:
                next_marker = len(chunk_data)
            
            slot_section_size = next_marker - slot_start
            estimated_slots = slot_section_size // 24  # Each slot name is 24 bytes
            print(f"Slot section size: {slot_section_size} bytes")
            print(f"Estimated slots: {estimated_slots}")
            
            # Show first few slot names
            print(f"\nFirst 5 slot names:")
            for i in range(min(5, estimated_slots)):
                slot_offset = slot_start + (i * 24)
                slot_name_bytes = chunk_data[slot_offset:slot_offset+24]
                slot_name = slot_name_bytes.rstrip(b'\x00').decode('ascii', errors='ignore')
                print(f"  Slot {i}: '{slot_name}'")
            
            pos = idx + 1
    
    # Analyze SDB1 structure
    print("\n\n" + "=" * 80)
    print("DETAILED SDB1 STRUCTURE ANALYSIS")
    print("=" * 80)
    
    sdb1_chunk = next((c for c in chunks if c['id'] == 'SDB1'), None)
    if sdb1_chunk:
        chunk_data = data[sdb1_chunk['data_start']:sdb1_chunk['data_end']]
        
        print(f"\nSDB1 chunk size: {len(chunk_data):,} bytes")
        
        # Look for setlist names
        search_names = [b"NIGHTWISH LEGACY", b"ULTIMATE COVERS", b"MOVIE & TV THEMES"]
        
        for search_name in search_names:
            idx = chunk_data.find(search_name)
            if idx != -1:
                print(f"\nFound '{search_name.decode()}' at offset {idx} (0x{idx:08X})")
                
                # Show surrounding data
                start = max(0, idx - 64)
                end = min(len(chunk_data), idx + len(search_name) + 64)
                context = chunk_data[start:end]
                
                print("Context:")
                for j in range(0, len(context), 16):
                    offset = start + j
                    hex_str = ' '.join(f'{b:02X}' for b in context[j:j+16])
                    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in context[j:j+16])
                    marker = " <--" if start + j <= idx < start + j + 16 else ""
                    print(f"  {offset:06X}: {hex_str:<48} {ascii_str}{marker}")
    
    # Analyze SBK1 structure
    print("\n\n" + "=" * 80)
    print("DETAILED SBK1 STRUCTURE ANALYSIS")
    print("=" * 80)
    
    sbk1_chunk = next((c for c in chunks if c['id'] == 'SBK1'), None)
    if sbk1_chunk:
        chunk_data = data[sbk1_chunk['data_start']:sbk1_chunk['data_end']]
        
        print(f"\nSBK1 chunk size: {len(chunk_data):,} bytes")
        
        # Calculate setlist positions (16 setlists, 69,416 bytes each)
        setlist_size = 69416
        header_size = 69432  # Before first setlist
        
        print(f"\nSetlist structure:")
        print(f"  Header size: {header_size} bytes")
        print(f"  Setlist size: {setlist_size} bytes")
        print(f"  Number of setlists: 16")
        
        for i in range(16):
            setlist_offset = header_size + (i * setlist_size)
            if setlist_offset + 24 > len(chunk_data):
                break
            
            name_bytes = chunk_data[setlist_offset:setlist_offset+24]
            name = name_bytes.rstrip(b'\x00').decode('ascii', errors='ignore')
            
            if name:  # Only show non-empty setlists
                print(f"\nSetlist {i}:")
                print(f"  Offset in chunk: {setlist_offset} (0x{setlist_offset:08X})")
                print(f"  File offset: {sbk1_chunk['data_start'] + setlist_offset} (0x{sbk1_chunk['data_start'] + setlist_offset:08X})")
                print(f"  Name: '{name}'")
                
                # Show first few bytes after name
                print(f"  Bytes after name:")
                for j in range(24, min(64, setlist_size), 16):
                    offset = setlist_offset + j
                    hex_str = ' '.join(f'{b:02X}' for b in chunk_data[offset:offset+16])
                    print(f"    +{j:04X}: {hex_str}")

if __name__ == '__main__':
    # Analyze the Nightwish file
    pcg_file = Path('test_files/NIGHTWISH LEGACY.PCG')
    
    if not pcg_file.exists():
        print(f"Error: {pcg_file} not found")
        print("\nLooking for other PCG files...")
        for f in Path('.').glob('*.PCG'):
            print(f"  Found: {f}")
            pcg_file = f
            break
    
    if pcg_file.exists():
        analyze_chunk_structure(pcg_file)
    else:
        print("No PCG files found!")
