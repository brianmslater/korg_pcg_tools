#!/usr/bin/env python3
"""
Test a hypothesized SDB1 color offset pattern.

Once you've discovered potential color byte locations through binary comparison,
use this script to test if your offset calculation pattern is correct.

USAGE:
python3 test_color_pattern.py <pcg_file> <base_offset> <setlist_multiplier> <slot_multiplier>

EXAMPLE:
python3 test_color_pattern.py test_files/soundcheck9_25_25_combined2.PCG 0x5000 0x1000 0x10
"""

import sys

def test_pattern(filename, base_offset, setlist_mult, slot_mult):
    """Test if the offset pattern correctly predicts color locations."""
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Find SDB1
    sdb1_pos = data.find(b'SDB1')
    if sdb1_pos < 0:
        print("Error: SDB1 chunk not found")
        return
    
    print("="*80)
    print("SDB1 COLOR PATTERN TESTER")
    print("="*80)
    print()
    print(f"File: {filename}")
    print(f"SDB1 at: 0x{sdb1_pos:08X}")
    print()
    print("Pattern:")
    print(f"  Base offset: 0x{base_offset:X}")
    print(f"  Setlist multiplier: 0x{setlist_mult:X}")
    print(f"  Slot multiplier: 0x{slot_mult:X}")
    print()
    print("Formula: offset = base + (setlist_idx * setlist_mult) + (slot_idx * slot_mult)")
    print()
    
    # Known colors from user report
    known_colors = {
        (4, 0): [164, 165],  # SC 10/4, Slot 0: Navy
        (4, 1): [160],       # SC 10/4, Slot 1: Indigo
        (4, 2): [152, 153],  # SC 10/4, Slot 2: Gold
        (4, 3): [152, 153],  # SC 10/4, Slot 3: Gold
        (4, 4): [152, 153],  # SC 10/4, Slot 4: Gold
    }
    
    color_names = {
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
    
    print("="*80)
    print("TESTING KNOWN COLORS (SC 10/4 setlist)")
    print("="*80)
    print()
    
    matches = 0
    total = 0
    
    for (setlist_idx, slot_idx), expected_values in known_colors.items():
        # Calculate offset
        offset = base_offset + (setlist_idx * setlist_mult) + (slot_idx * slot_mult)
        absolute_offset = sdb1_pos + offset
        
        # Check if offset is valid
        if absolute_offset >= len(data):
            print(f"Setlist {setlist_idx}, Slot {slot_idx}:")
            print(f"  Calculated offset: 0x{absolute_offset:08X} (OUT OF BOUNDS)")
            print(f"  Expected: {expected_values}")
            print()
            total += 1
            continue
        
        # Read byte at offset
        actual_value = data[absolute_offset]
        actual_color = color_names.get(actual_value, f"Unknown({actual_value})")
        expected_color = color_names.get(expected_values[0], f"Unknown({expected_values[0]})")
        
        # Check if it matches
        match = actual_value in expected_values
        match_str = "✓ MATCH" if match else "✗ NO MATCH"
        
        print(f"Setlist {setlist_idx}, Slot {slot_idx}:")
        print(f"  Calculated offset: 0x{absolute_offset:08X} (SDB1 +0x{offset:X})")
        print(f"  Expected: {expected_color} ({expected_values})")
        print(f"  Actual: {actual_color} ({actual_value})")
        print(f"  {match_str}")
        print()
        
        if match:
            matches += 1
        total += 1
    
    # Summary
    print("="*80)
    print("RESULTS")
    print("="*80)
    print()
    print(f"Matches: {matches}/{total}")
    print(f"Success rate: {matches*100//total if total > 0 else 0}%")
    print()
    
    if matches == total:
        print("✓ PATTERN CONFIRMED!")
        print()
        print("Next steps:")
        print("1. Test with more setlists and slots")
        print("2. Implement in pcg_parser.py")
        print("3. Add to models.py")
    elif matches > 0:
        print("⚠️  PARTIAL MATCH")
        print()
        print("The pattern works for some slots but not all.")
        print("Try adjusting the multipliers or base offset.")
    else:
        print("✗ PATTERN DOES NOT MATCH")
        print()
        print("Try different values for:")
        print("- Base offset")
        print("- Setlist multiplier")
        print("- Slot multiplier")
    
    # Test a few more slots to help refine
    print()
    print("="*80)
    print("ADDITIONAL SLOT SAMPLES")
    print("="*80)
    print()
    print("Testing pattern on other slots:")
    print()
    
    test_slots = [
        (0, 0),  # NIGHTWISH LEGACY, Slot 0
        (0, 1),  # NIGHTWISH LEGACY, Slot 1
        (1, 0),  # NIGHTWISH LEGACY 2, Slot 0
        (2, 0),  # Narf, Slot 0
    ]
    
    for setlist_idx, slot_idx in test_slots:
        offset = base_offset + (setlist_idx * setlist_mult) + (slot_idx * slot_mult)
        absolute_offset = sdb1_pos + offset
        
        if absolute_offset >= len(data):
            continue
        
        actual_value = data[absolute_offset]
        actual_color = color_names.get(actual_value, f"Unknown({actual_value})")
        
        print(f"Setlist {setlist_idx}, Slot {slot_idx}:")
        print(f"  Offset: 0x{absolute_offset:08X}")
        print(f"  Value: {actual_color} ({actual_value})")
        print()


def main():
    """Main entry point."""
    if len(sys.argv) != 5:
        print("Usage: python3 test_color_pattern.py <pcg_file> <base_offset> <setlist_mult> <slot_mult>")
        print()
        print("Arguments:")
        print("  pcg_file       - Path to PCG file")
        print("  base_offset    - Base offset from SDB1 start (hex, e.g., 0x5000)")
        print("  setlist_mult   - Multiplier for setlist index (hex, e.g., 0x1000)")
        print("  slot_mult      - Multiplier for slot index (hex, e.g., 0x10)")
        print()
        print("Example:")
        print("  python3 test_color_pattern.py \\")
        print("    test_files/soundcheck9_25_25_combined2.PCG \\")
        print("    0x5000 0x1000 0x10")
        print()
        print("This will test if colors are at:")
        print("  SDB1 + 0x5000 + (setlist_idx * 0x1000) + (slot_idx * 0x10)")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        base_offset = int(sys.argv[2], 16) if sys.argv[2].startswith('0x') else int(sys.argv[2])
        setlist_mult = int(sys.argv[3], 16) if sys.argv[3].startswith('0x') else int(sys.argv[3])
        slot_mult = int(sys.argv[4], 16) if sys.argv[4].startswith('0x') else int(sys.argv[4])
    except ValueError as e:
        print(f"Error parsing offsets: {e}")
        print("Make sure to use hex format (0x1234) or decimal")
        sys.exit(1)
    
    test_pattern(filename, base_offset, setlist_mult, slot_mult)


if __name__ == '__main__':
    main()
