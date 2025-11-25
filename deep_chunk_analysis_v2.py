#!/usr/bin/env python3
"""
Deep analysis using the actual PCG parser to understand chunk structures.
"""

from pathlib import Path
from pcg_tools.reader import read_pcg_file

def analyze_with_parser(pcg_file):
    """Use the actual parser to analyze chunk structure."""
    
    print(f"Analyzing: {pcg_file}")
    print("=" * 80)
    
    pcg = read_pcg_file(str(pcg_file))
    
    # Read raw file data
    with open(pcg_file, 'rb') as f:
        raw_data = f.read()
    
    print(f"File size: {len(raw_data):,} bytes")
    print(f"Parsed {len(pcg.set_lists)} setlists")
    print()
    
    # Find chunks manually
    chunks = {}
    pos = 16  # Skip PCG1 header
    while pos < len(raw_data) - 8:
        chunk_id = raw_data[pos:pos+4]
        if len(chunk_id) == 4:
            try:
                chunk_id_str = chunk_id.decode('ascii')
                size = int.from_bytes(raw_data[pos+4:pos+8], 'little')
                if 0 < size < len(raw_data) and chunk_id_str.isprintable():
                    chunks[chunk_id_str] = {'offset': pos, 'size': size}
                    pos += 8 + size
                    continue
            except:
                pass
        pos += 1
    
    # Show chunk information
    print("Chunks found:")
    for chunk_id, chunk_info in chunks.items():
        print(f"  {chunk_id}: offset={chunk_info['offset']}, size={chunk_info['size']}")
    
    print("\n" + "=" * 80)
    print("SEARCHING FOR SETLIST NAMES IN RAW DATA")
    print("=" * 80)
    
    # Search for each setlist name in the raw data
    for i, setlist in enumerate(pcg.set_lists):
        if not setlist.name or setlist.name == "INIT SETLIST":
            continue
        
        print(f"\n--- Setlist {i}: '{setlist.name}' ---")
        
        # Convert name to bytes (padded to 24 bytes)
        name_bytes = setlist.name.encode('ascii')
        
        # Find all occurrences
        occurrences = []
        pos = 0
        while pos < len(raw_data):
            idx = raw_data.find(name_bytes, pos)
            if idx == -1:
                break
            occurrences.append(idx)
            pos = idx + 1
        
        print(f"Found {len(occurrences)} occurrences:")
        
        for j, offset in enumerate(occurrences, 1):
            # Determine which chunk this is in
            chunk_name = "Unknown"
            chunk_offset = offset
            
            for cid, cinfo in chunks.items():
                chunk_start = cinfo['offset'] + 8  # +8 for chunk header
                chunk_end = chunk_start + cinfo['size']
                if chunk_start <= offset < chunk_end:
                    chunk_name = cid
                    chunk_offset = offset - chunk_start
                    break
            
            print(f"\n  Occurrence {j}:")
            print(f"    File offset: {offset} (0x{offset:08X})")
            print(f"    Chunk: {chunk_name}")
            print(f"    Chunk offset: {chunk_offset} (0x{chunk_offset:08X})")
            
            # Show context
            start = max(0, offset - 32)
            end = min(len(raw_data), offset + len(name_bytes) + 32)
            context = raw_data[start:end]
            
            print(f"    Context:")
            for k in range(0, len(context), 16):
                ctx_offset = start + k
                hex_str = ' '.join(f'{b:02X}' for b in context[k:k+16])
                ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in context[k:k+16])
                marker = " <--" if start + k <= offset < start + k + 16 else ""
                print(f"      {ctx_offset:08X}: {hex_str:<48} {ascii_str}{marker}")
    
    # Analyze SLS1 chunk structure in detail
    if 'SLS1' in chunks:
        print("\n\n" + "=" * 80)
        print("DETAILED SLS1 CHUNK ANALYSIS")
        print("=" * 80)
        
        chunk_info = chunks['SLS1']
        chunk_start = chunk_info['offset'] + 8
        chunk_end = chunk_start + chunk_info['size']
        chunk_data = raw_data[chunk_start:chunk_end]
        
        print(f"\nSLS1 chunk:")
        print(f"  File offset: {chunk_start} (0x{chunk_start:08X})")
        print(f"  Size: {len(chunk_data):,} bytes")
        
        # Look for the marker pattern (1E 02 00 00)
        marker = bytes([0x1E, 0x02, 0x00, 0x00])
        print(f"\nSearching for marker pattern: {' '.join(f'{b:02X}' for b in marker)}")
        
        pos = 0
        setlist_num = 0
        while pos < len(chunk_data):
            idx = chunk_data.find(marker, pos)
            if idx == -1:
                break
            
            setlist_num += 1
            print(f"\n  Setlist {setlist_num}:")
            print(f"    Marker at chunk offset: {idx} (0x{idx:08X})")
            print(f"    File offset: {chunk_start + idx} (0x{chunk_start + idx:08X})")
            
            # Try to extract name after marker
            name_start = idx + 4
            name_bytes = chunk_data[name_start:name_start+24]
            name = name_bytes.rstrip(b'\x00').decode('ascii', errors='ignore')
            print(f"    Name: '{name}'")
            
            # Show structure after name
            print(f"    Structure after name:")
            for k in range(24, min(128, len(chunk_data) - name_start), 16):
                offset = name_start + k
                if offset >= len(chunk_data):
                    break
                hex_str = ' '.join(f'{b:02X}' for b in chunk_data[offset:offset+16])
                ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk_data[offset:offset+16])
                print(f"      +{k:04X}: {hex_str:<48} {ascii_str}")
            
            pos = idx + 1
            if setlist_num >= 3:  # Limit output
                print(f"\n  ... (stopping after 3 setlists)")
                break
    
    # Analyze SDB1 chunk structure
    if 'SDB1' in chunks:
        print("\n\n" + "=" * 80)
        print("DETAILED SDB1 CHUNK ANALYSIS")
        print("=" * 80)
        
        chunk_info = chunks['SDB1']
        chunk_start = chunk_info['offset'] + 8
        chunk_end = chunk_start + chunk_info['size']
        chunk_data = raw_data[chunk_start:chunk_end]
        
        print(f"\nSDB1 chunk:")
        print(f"  File offset: {chunk_start} (0x{chunk_start:08X})")
        print(f"  Size: {len(chunk_data):,} bytes")
        
        # Show first 256 bytes
        print(f"\nFirst 256 bytes:")
        for k in range(0, min(256, len(chunk_data)), 16):
            hex_str = ' '.join(f'{b:02X}' for b in chunk_data[k:k+16])
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk_data[k:k+16])
            print(f"  {k:04X}: {hex_str:<48} {ascii_str}")
        
        # Look for patterns that might indicate setlist boundaries
        print(f"\nLooking for repeating patterns...")
        
        # Check if there's a regular structure (e.g., every N bytes)
        for stride in [128, 256, 512, 1024, 2048]:
            # Sample a few positions
            sample_size = 16
            matches = 0
            for i in range(0, min(len(chunk_data) - stride * 3, 10000), stride):
                if chunk_data[i:i+sample_size] == chunk_data[i+stride:i+stride+sample_size]:
                    matches += 1
            
            if matches > 2:
                print(f"  Possible stride of {stride} bytes (found {matches} matching patterns)")
    
    # Analyze SBK1 chunk structure
    if 'SBK1' in chunks:
        print("\n\n" + "=" * 80)
        print("DETAILED SBK1 CHUNK ANALYSIS")
        print("=" * 80)
        
        chunk_info = chunks['SBK1']
        chunk_start = chunk_info['offset'] + 8
        chunk_end = chunk_start + chunk_info['size']
        chunk_data = raw_data[chunk_start:chunk_end]
        
        print(f"\nSBK1 chunk:")
        print(f"  File offset: {chunk_start} (0x{chunk_start:08X})")
        print(f"  Size: {len(chunk_data):,} bytes")
        
        # Known structure: 16 setlists, 69,416 bytes each, after 69,432 byte header
        setlist_size = 69416
        header_size = 69432
        
        print(f"\nKnown structure:")
        print(f"  Header: {header_size} bytes")
        print(f"  Setlist size: {setlist_size} bytes")
        print(f"  Number of setlists: 16")
        
        print(f"\nSetlist names in SBK1:")
        for i in range(16):
            offset = header_size + (i * setlist_size)
            if offset + 24 > len(chunk_data):
                break
            
            name_bytes = chunk_data[offset:offset+24]
            name = name_bytes.rstrip(b'\x00').decode('ascii', errors='ignore')
            
            if name:
                print(f"  Setlist {i}: '{name}' at chunk offset {offset} (0x{offset:08X}), file offset {chunk_start + offset} (0x{chunk_start + offset:08X})")

if __name__ == '__main__':
    # Try to find a PCG file
    pcg_file = None
    
    # Check for test files
    test_dir = Path('test_files')
    if test_dir.exists():
        for f in test_dir.glob('*.PCG'):
            pcg_file = f
            break
    
    # Check current directory
    if not pcg_file:
        for f in Path('.').glob('*.PCG'):
            pcg_file = f
            break
    
    if pcg_file and pcg_file.exists():
        analyze_with_parser(pcg_file)
    else:
        print("No PCG files found!")
        print("Please provide a PCG file to analyze.")
