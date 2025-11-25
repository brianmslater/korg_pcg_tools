#!/usr/bin/env python3
"""
Compare two PCG files byte-by-byte to find differences.
"""

import sys
from pathlib import Path

def compare_files(file1_path, file2_path, context=32):
    """Compare two files byte-by-byte and show differences."""
    
    with open(file1_path, 'rb') as f1:
        data1 = f1.read()
    
    with open(file2_path, 'rb') as f2:
        data2 = f2.read()
    
    print(f"File 1: {file1_path}")
    print(f"  Size: {len(data1):,} bytes")
    print(f"\nFile 2: {file2_path}")
    print(f"  Size: {len(data2):,} bytes")
    print()
    
    if len(data1) != len(data2):
        print(f"❌ SIZE MISMATCH: {len(data2) - len(data1):+,} bytes")
        print()
    
    # Find all differences
    differences = []
    min_len = min(len(data1), len(data2))
    
    for i in range(min_len):
        if data1[i] != data2[i]:
            differences.append(i)
    
    if not differences:
        print("✓ Files are IDENTICAL")
        return True
    
    print(f"❌ Found {len(differences):,} byte differences")
    print()
    
    # Show first 20 differences with context
    for idx, offset in enumerate(differences[:20]):
        print(f"Difference {idx+1} at offset {offset} (0x{offset:08X}):")
        
        # Show context
        start = max(0, offset - context)
        end = min(min_len, offset + context + 1)
        
        print(f"  File 1:")
        for i in range(start, end, 16):
            hex_str = ' '.join(f'{data1[j]:02X}' if j < len(data1) else '  ' for j in range(i, min(i+16, end)))
            marker = ' <--' if i <= offset < i+16 else ''
            print(f"    {i:08X}: {hex_str}{marker}")
        
        print(f"  File 2:")
        for i in range(start, end, 16):
            hex_str = ' '.join(f'{data2[j]:02X}' if j < len(data2) else '  ' for j in range(i, min(i+16, end)))
            marker = ' <--' if i <= offset < i+16 else ''
            print(f"    {i:08X}: {hex_str}{marker}")
        
        print()
    
    if len(differences) > 20:
        print(f"... and {len(differences) - 20:,} more differences")
    
    return False

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 compare_binary_files.py <file1> <file2>")
        print()
        print("Example:")
        print("  python3 compare_binary_files.py test_files/nw_modified.PCG test_files/unmodified_roundtrip.PCG")
        sys.exit(1)
    
    file1 = Path(sys.argv[1])
    file2 = Path(sys.argv[2])
    
    if not file1.exists():
        print(f"Error: {file1} not found")
        sys.exit(1)
    
    if not file2.exists():
        print(f"Error: {file2} not found")
        sys.exit(1)
    
    compare_files(file1, file2)
