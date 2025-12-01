#!/usr/bin/env python3
"""Analyze PCG file chunk structure to understand corruption issues."""

import sys
import struct

def read_chunk_header(data, offset):
    """Read a chunk header (ID + size)."""
    if offset + 8 > len(data):
        return None, None, None
    
    chunk_id = data[offset:offset+4].decode('ascii', errors='ignore')
    chunk_size = struct.unpack('>I', data[offset+4:offset+8])[0]
    
    return chunk_id, chunk_size, offset

def analyze_chunks(filename):
    """Analyze all chunks in a PCG file."""
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"File: {filename}")
    print(f"Size: {len(data)} bytes")
    print("="*80)
    print()
    
    # Check header
    if data[:4] != b'KORG':
        print("ERROR: Not a valid PCG file (missing KORG header)")
        return
    
    print("Header: KORG")
    print()
    
    # Read PCG1 chunk (main container)
    offset = 16
    chunk_id, chunk_size, chunk_offset = read_chunk_header(data, offset)
    
    if chunk_id != 'PCG1':
        print(f"ERROR: Expected PCG1 chunk, got {chunk_id}")
        return
    
    print(f"Main Container: PCG1")
    print(f"  Offset: 0x{chunk_offset:08x}")
    print(f"  Size: {chunk_size} bytes")
    print()
    
    # Parse sub-chunks within PCG1
    offset = 28  # Skip PCG1 header (4 + 4 + 4)
    pcg1_end = 28 + chunk_size
    chunks = []
    
    print("Top-Level Chunks:")
    print("-" * 80)
    
    while offset < pcg1_end - 8:
        chunk_id, chunk_size, chunk_offset = read_chunk_header(data, offset)
        
        if not chunk_id or not chunk_id.replace('_', '').isalnum():
            offset += 1
            continue
        
        chunks.append({
            'id': chunk_id,
            'offset': chunk_offset,
            'size': chunk_size,
            'total_size': chunk_size + 12
        })
        
        print(f"{chunk_id:4s}: offset=0x{chunk_offset:08x}, size={chunk_size:10d} bytes")
        
        # Check for sub-chunks in specific chunks
        if chunk_id in ['PRG1', 'PRG2', 'CMB1', 'CMB2', 'SLS1', 'SLS2']:
            sub_offset = chunk_offset + 12  # Skip header + 4 bytes padding
            sub_end = chunk_offset + 12 + chunk_size
            sub_chunks = []
            
            while sub_offset < sub_end - 8:
                sub_id, sub_size, sub_off = read_chunk_header(data, sub_offset)
                if sub_id and sub_id.replace('_', '').isalnum() and len(sub_id) == 4:
                    sub_chunks.append((sub_id, sub_off, sub_size))
                    sub_offset += sub_size + 12
                else:
                    break
            
            if sub_chunks:
                for sub_id, sub_off, sub_size in sub_chunks:
                    print(f"  └─ {sub_id}: offset=0x{sub_off:08x}, size={sub_size:10d} bytes")
        
        offset += chunk_size + 12
    
    print()
    print("="*80)
    print(f"Total top-level chunks: {len(chunks)}")
    
    return chunks

def compare_files(file1, file2):
    """Compare two PCG files byte-by-byte."""
    with open(file1, 'rb') as f:
        data1 = f.read()
    with open(file2, 'rb') as f:
        data2 = f.read()
    
    print(f"\nComparing:")
    print(f"  File 1: {file1} ({len(data1)} bytes)")
    print(f"  File 2: {file2} ({len(data2)} bytes)")
    print("="*80)
    
    if len(data1) != len(data2):
        print(f"ERROR: Files have different sizes!")
        print(f"  Difference: {abs(len(data1) - len(data2))} bytes")
        return
    
    # Find differences
    diffs = []
    for i in range(len(data1)):
        if data1[i] != data2[i]:
            diffs.append(i)
    
    print(f"\nTotal differences: {len(diffs)} bytes ({len(diffs)*100//len(data1)}%)")
    
    if diffs:
        print(f"\nFirst 20 differences:")
        for i, offset in enumerate(diffs[:20]):
            print(f"  0x{offset:08x}: {data1[offset]:02x} -> {data2[offset]:02x}")
        
        # Group differences by region
        print(f"\nDifference regions:")
        if diffs:
            region_start = diffs[0]
            region_end = diffs[0]
            
            for offset in diffs[1:]:
                if offset == region_end + 1:
                    region_end = offset
                else:
                    print(f"  0x{region_start:08x} - 0x{region_end:08x} ({region_end - region_start + 1} bytes)")
                    region_start = offset
                    region_end = offset
            
            print(f"  0x{region_start:08x} - 0x{region_end:08x} ({region_end - region_start + 1} bytes)")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python test_chunk_analysis.py <file.PCG>")
        print("  python test_chunk_analysis.py <file1.PCG> <file2.PCG>")
        sys.exit(1)
    
    if len(sys.argv) == 2:
        analyze_chunks(sys.argv[1])
    else:
        analyze_chunks(sys.argv[1])
        print("\n" + "="*80 + "\n")
        analyze_chunks(sys.argv[2])
        compare_files(sys.argv[1], sys.argv[2])
