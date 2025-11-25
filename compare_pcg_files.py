#!/usr/bin/env python3
"""
Binary comparison tool for discovering SDB1 color data structure.

USAGE:
1. Load soundcheck9_25_25_combined2.PCG into Kronos
2. Note the current colors for a setlist (e.g., SC 10/4)
3. Change ONE slot color (e.g., Slot 0 from Navy to Brick)
4. Save as a new file (e.g., soundcheck_modified.PCG)
5. Run: python3 compare_pcg_files.py original.PCG modified.PCG

This will show you exactly which bytes changed, helping identify
where color data is stored in the SDB1 chunk.
"""

import sys
from pathlib import Path

def compare_files(file1_path, file2_path, context_bytes=32):
    """Compare two PCG files and show differences."""
    
    print("="*80)
    print("PCG FILE BINARY COMPARISON TOOL")
    print("="*80)
    print()
    
    # Read both files
    with open(file1_path, 'rb') as f:
        data1 = f.read()
    
    with open(file2_path, 'rb') as f:
        data2 = f.read()
    
    print(f"File 1: {file1_path}")
    print(f"  Size: {len(data1):,} bytes")
    print()
    print(f"File 2: {file2_path}")
    print(f"  Size: {len(data2):,} bytes")
    print()
    
    # Check size difference
    if len(data1) != len(data2):
        print(f"⚠️  WARNING: Files are different sizes!")
        print(f"  Difference: {abs(len(data1) - len(data2)):,} bytes")
        print()
        min_len = min(len(data1), len(data2))
    else:
        print("✓ Files are the same size")
        print()
        min_len = len(data1)
    
    # Find all differences
    differences = []
    for i in range(min_len):
        if data1[i] != data2[i]:
            differences.append(i)
    
    print(f"Found {len(differences)} byte differences")
    print()
    
    if len(differences) == 0:
        print("✓ Files are identical!")
        return
    
    # Locate chunks
    sdb1_pos = data1.find(b'SDB1')
    sld1_pos = data1.find(b'SLD1')
    stl1_pos = data1.find(b'STL1')
    
    print("Chunk locations:")
    if sdb1_pos >= 0:
        print(f"  SDB1: 0x{sdb1_pos:08X}")
    if sld1_pos >= 0:
        print(f"  SLD1: 0x{sld1_pos:08X}")
    if stl1_pos >= 0:
        print(f"  STL1: 0x{stl1_pos:08X}")
    print()
    
    # Categorize differences by chunk
    sdb1_diffs = []
    sld1_diffs = []
    stl1_diffs = []
    other_diffs = []
    
    for diff_pos in differences:
        if sdb1_pos >= 0 and diff_pos >= sdb1_pos:
            sdb1_diffs.append(diff_pos)
        elif sld1_pos >= 0 and diff_pos >= sld1_pos:
            sld1_diffs.append(diff_pos)
        elif stl1_pos >= 0 and diff_pos >= stl1_pos:
            stl1_diffs.append(diff_pos)
        else:
            other_diffs.append(diff_pos)
    
    print("Differences by chunk:")
    print(f"  SDB1: {len(sdb1_diffs)} differences")
    print(f"  SLD1: {len(sld1_diffs)} differences")
    print(f"  STL1: {len(stl1_diffs)} differences")
    print(f"  Other: {len(other_diffs)} differences")
    print()
    
    # Show detailed differences
    print("="*80)
    print("DETAILED DIFFERENCES")
    print("="*80)
    print()
    
    # Group consecutive differences
    groups = []
    if differences:
        current_group = [differences[0]]
        for i in range(1, len(differences)):
            if differences[i] - differences[i-1] <= 16:  # Within 16 bytes
                current_group.append(differences[i])
            else:
                groups.append(current_group)
                current_group = [differences[i]]
        groups.append(current_group)
    
    print(f"Found {len(groups)} groups of differences:")
    print()
    
    for group_idx, group in enumerate(groups[:20]):  # Show first 20 groups
        start_pos = group[0]
        end_pos = group[-1]
        
        # Determine which chunk this is in
        chunk_name = "Unknown"
        chunk_offset = 0
        if sdb1_pos >= 0 and start_pos >= sdb1_pos:
            chunk_name = "SDB1"
            chunk_offset = start_pos - sdb1_pos
        elif sld1_pos >= 0 and start_pos >= sld1_pos:
            chunk_name = "SLD1"
            chunk_offset = start_pos - sld1_pos
        elif stl1_pos >= 0 and start_pos >= stl1_pos:
            chunk_name = "STL1"
            chunk_offset = start_pos - stl1_pos
        
        print(f"Group {group_idx + 1}: {len(group)} bytes changed")
        print(f"  Location: 0x{start_pos:08X} to 0x{end_pos:08X}")
        print(f"  Chunk: {chunk_name} (offset +{chunk_offset})")
        print()
        
        # Show context
        context_start = max(0, start_pos - context_bytes)
        context_end = min(min_len, end_pos + context_bytes + 1)
        
        print(f"  File 1 context:")
        for i in range(context_start, context_end, 16):
            hex_str = ' '.join(f'{data1[i+j]:02X}' for j in range(min(16, context_end-i)))
            ascii_str = ''.join(chr(data1[i+j]) if 32 <= data1[i+j] < 127 else '.' 
                               for j in range(min(16, context_end-i)))
            marker = ' <<<' if any(i <= d < i+16 for d in group) else ''
            print(f"    {i:08X}: {hex_str:<48} {ascii_str}{marker}")
        
        print()
        print(f"  File 2 context:")
        for i in range(context_start, context_end, 16):
            hex_str = ' '.join(f'{data2[i+j]:02X}' for j in range(min(16, context_end-i)))
            ascii_str = ''.join(chr(data2[i+j]) if 32 <= data2[i+j] < 127 else '.' 
                               for j in range(min(16, context_end-i)))
            marker = ' <<<' if any(i <= d < i+16 for d in group) else ''
            print(f"    {i:08X}: {hex_str:<48} {ascii_str}{marker}")
        
        print()
        print(f"  Byte changes:")
        for diff_pos in group[:10]:  # Show first 10 in group
            old_val = data1[diff_pos]
            new_val = data2[diff_pos]
            print(f"    0x{diff_pos:08X}: 0x{old_val:02X} ({old_val:3d}) → 0x{new_val:02X} ({new_val:3d})")
        if len(group) > 10:
            print(f"    ... and {len(group) - 10} more")
        
        print()
        print("-"*80)
        print()
    
    if len(groups) > 20:
        print(f"... and {len(groups) - 20} more groups")
        print()
    
    # Summary
    print("="*80)
    print("ANALYSIS SUMMARY")
    print("="*80)
    print()
    
    print("To find color data:")
    print("1. Look for changes in SDB1 chunk")
    print("2. Check if changed bytes match color values:")
    print("   - Navy: 164 (0xA4) or 165 (0xA5)")
    print("   - Indigo: 160 (0xA0)")
    print("   - Gold: 152 (0x98) or 153 (0x99)")
    print("   - Brick: 136 (0x88) or 137 (0x89)")
    print("   - etc.")
    print()
    print("3. Note the offset from SDB1 start")
    print("4. Calculate pattern: (setlist_index * X) + (slot_index * Y) + base_offset")
    print()
    
    # Check if any differences match known color values
    color_values = {
        136: "Brick", 137: "Brick",
        140: "Burgundy",
        144: "Ivy",
        148: "Olive",
        152: "Gold", 153: "Gold",
        156: "Cacao", 157: "Cacao",
        160: "Indigo",
        164: "Navy", 165: "Navy",
        168: "Rose",
        172: "Lavender", 174: "Lavender",
        176: "Azure",
        180: "Denim", 181: "Denim",
        184: "Silver",
        188: "Slate",
        196: "Charcoal",
    }
    
    print("Potential color changes found:")
    found_colors = False
    for diff_pos in differences[:100]:  # Check first 100
        old_val = data1[diff_pos]
        new_val = data2[diff_pos]
        
        if old_val in color_values or new_val in color_values:
            old_color = color_values.get(old_val, f"Unknown({old_val})")
            new_color = color_values.get(new_val, f"Unknown({new_val})")
            
            chunk_info = ""
            if sdb1_pos >= 0 and diff_pos >= sdb1_pos:
                chunk_info = f" [SDB1 +{diff_pos - sdb1_pos}]"
            
            print(f"  0x{diff_pos:08X}: {old_color} → {new_color}{chunk_info}")
            found_colors = True
    
    if not found_colors:
        print("  None found in first 100 differences")
    
    print()
    print("Next steps:")
    print("1. Review the differences above")
    print("2. Identify which bytes correspond to the color you changed")
    print("3. Calculate the offset pattern")
    print("4. Test with more color changes to confirm the pattern")


def main():
    """Main entry point."""
    if len(sys.argv) != 3:
        print("Usage: python3 compare_pcg_files.py <original.PCG> <modified.PCG>")
        print()
        print("Example workflow:")
        print("1. Load soundcheck9_25_25_combined2.PCG into Kronos")
        print("2. Go to SC 10/4 setlist, Slot 0")
        print("3. Change color from Navy to Brick")
        print("4. Save as soundcheck_modified.PCG")
        print("5. Run:")
        print("   python3 compare_pcg_files.py \\")
        print("     test_files/soundcheck9_25_25_combined2.PCG \\")
        print("     test_files/soundcheck_modified.PCG")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    
    if not Path(file1).exists():
        print(f"Error: File not found: {file1}")
        sys.exit(1)
    
    if not Path(file2).exists():
        print(f"Error: File not found: {file2}")
        sys.exit(1)
    
    compare_files(file1, file2)


if __name__ == '__main__':
    main()
