#!/usr/bin/env python3
"""
Map all 16 Kronos colors from the Movie TV Themes 2 file.
Based on the color chart image showing the official order.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file

# Official Kronos color order from the color chart
OFFICIAL_COLOR_ORDER = [
    "Azure", "Indigo", "Ivy", "Default",
    "Denim", "Navy", "Olive", "Charcoal", 
    "Silver", "Rose", "Gold", "Brick",
    "Slate", "Lavender", "Cacao", "Burgundy"
]

def map_colors(filename):
    """Map all 16 Kronos colors from the file."""
    
    print(f"Analyzing: {filename}\n")
    
    pcg = read_pcg_file(filename)
    
    if len(pcg.set_lists) == 0:
        print("No setlists found!")
        return False
    
    setlist = pcg.set_lists[0]
    print(f"Setlist: '{setlist.name}'")
    print(f"Slots: {len(setlist.slots)}\n")
    
    print("Color Mapping from File:")
    print("=" * 70)
    print(f"{'#':<3} {'Slot Name':<30} {'Color':<8} {'Hex':<6} {'Expected'}") 
    print("-" * 70)
    
    color_mapping = {}
    
    for i, slot in enumerate(setlist.slots[:16]):
        if slot.name:
            color_mapping[slot.name.strip()] = slot.color
            expected = OFFICIAL_COLOR_ORDER[i] if i < len(OFFICIAL_COLOR_ORDER) else "?"
            print(f"{i:2d}  {slot.name:<30} {slot.color:<8} 0x{slot.color:02X}   {expected}")
    
    # Now map by position to official color names
    print("\n" + "=" * 70)
    print("COMPLETE COLOR MAPPING")
    print("=" * 70)
    
    final_mapping = {}
    for i, slot in enumerate(setlist.slots[:16]):
        if i < len(OFFICIAL_COLOR_ORDER) and slot.name:
            color_name = OFFICIAL_COLOR_ORDER[i]
            final_mapping[color_name] = slot.color
    
    print("\n# Complete Kronos color mapping")
    print("SLOT_COLORS = {")
    for color_name, color_value in sorted(final_mapping.items(), key=lambda x: x[1]):
        print(f"    {color_value}: \"{color_name}\",")
    print("}")
    
    print("\n# Reverse mapping")
    print("SLOT_COLOR_VALUES = {")
    for color_name, color_value in sorted(final_mapping.items()):
        print(f"    \"{color_name}\": {color_value},")
    print("}")
    
    print("\n" + "=" * 70)
    print(f"✓ Mapped {len(final_mapping)}/16 colors")
    print("=" * 70)
    
    return True

if __name__ == '__main__':
    filename = "SETLIST Movie TV Themes LOAD SEPARATELY 2.PCG"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    map_colors(filename)
