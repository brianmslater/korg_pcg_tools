#!/usr/bin/env python3
"""Test visual color display and expanded color mappings."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file
from pcg_tools.models import SLOT_COLORS, SLOT_COLOR_VALUES

def test_color_mappings():
    print("="*80)
    print("COLOR MAPPING TEST")
    print("="*80)
    
    print("\nAvailable Colors:")
    print(f"  Total: {len(SLOT_COLOR_VALUES)} colors defined")
    
    for color_name, color_value in sorted(SLOT_COLOR_VALUES.items(), key=lambda x: x[1]):
        print(f"  {color_value:3d} (0x{color_value:02X}): {color_name}")
    
    print("\nReverse Mapping:")
    print(f"  Total: {len(SLOT_COLORS)} values mapped")
    
    for color_value, color_name in sorted(SLOT_COLORS.items()):
        print(f"  {color_value:3d} (0x{color_value:02X}): {color_name}")
    
    # Test with real file
    input_file = 'SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    
    if not Path(input_file).exists():
        print(f"\n✗ File not found: {input_file}")
        return
    
    print(f"\n\nTesting with: {input_file}")
    pcg = read_pcg_file(input_file)
    
    if len(pcg.set_lists) == 0:
        print("✗ No setlists found!")
        return
    
    setlist = pcg.set_lists[0]
    print(f"Setlist: '{setlist.name}'")
    
    print("\nSlot Colors Found:")
    color_counts = {}
    for slot in setlist.slots:
        if slot.name:
            color_counts[slot.color] = color_counts.get(slot.color, 0) + 1
    
    for color_value in sorted(color_counts.keys()):
        count = color_counts[color_value]
        color_name = SLOT_COLORS.get(color_value, f"Unknown({color_value})")
        print(f"  {color_value:3d} (0x{color_value:02X}): {color_name:<20} - {count} slots")
    
    # Test setting all colors
    print("\n\nTesting Color Assignment:")
    test_colors = [0, 16, 32, 140, 160, 204]
    
    for i, color_value in enumerate(test_colors):
        if i < len(setlist.slots) and setlist.slots[i].name:
            old_color = setlist.slots[i].color
            setlist.slots[i].color = color_value
            color_name = SLOT_COLORS.get(color_value, f"Unknown({color_value})")
            print(f"  Slot {i}: {old_color} → {color_value} ({color_name})")
    
    # Write and verify
    output_file = 'test_color_visual_output.PCG'
    print(f"\nWriting to: {output_file}")
    write_pcg_file(pcg, output_file)
    
    print("Reading back...")
    pcg2 = read_pcg_file(output_file)
    setlist2 = pcg2.set_lists[0]
    
    print("\nVerification:")
    all_match = True
    for i, color_value in enumerate(test_colors):
        if i < len(setlist2.slots):
            slot = setlist2.slots[i]
            if slot.color == color_value:
                print(f"  ✓ Slot {i}: {slot.color} ({slot.color_name})")
            else:
                print(f"  ✗ Slot {i}: Expected {color_value}, got {slot.color}")
                all_match = False
    
    if all_match:
        print("\n✓ All color assignments verified!")
    else:
        print("\n✗ Some color assignments failed")
    
    return all_match

if __name__ == '__main__':
    success = test_color_mappings()
    sys.exit(0 if success else 1)
