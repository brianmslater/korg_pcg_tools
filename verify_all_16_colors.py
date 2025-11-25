#!/usr/bin/env python3
"""
Verify all 16 Kronos colors are correctly mapped.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file
from pcg_tools.models import SLOT_COLORS

def verify_colors(filename):
    """Verify all 16 colors display correctly."""
    
    print("=" * 70)
    print("VERIFYING ALL 16 KRONOS COLORS")
    print("=" * 70)
    
    pcg = read_pcg_file(filename)
    
    if len(pcg.set_lists) == 0:
        print("✗ No setlists found!")
        return False
    
    setlist = pcg.set_lists[0]
    print(f"\nSetlist: '{setlist.name}'")
    print(f"Slots: {len(setlist.slots)}\n")
    
    print(f"{'#':<3} {'Song Name':<30} {'Color Value':<12} {'Color Name':<15} {'Status'}")
    print("-" * 70)
    
    all_correct = True
    colors_found = set()
    
    for i, slot in enumerate(setlist.slots[:16]):
        if slot.name:
            color_name = slot.color_name
            is_known = "Unknown" not in color_name
            status = "✓" if is_known else "✗"
            
            if not is_known:
                all_correct = False
            else:
                colors_found.add(color_name)
            
            print(f"{i:2d}  {slot.name:<30} {slot.color:<12} {color_name:<15} {status}")
    
    print("\n" + "=" * 70)
    print(f"Colors correctly mapped: {len(colors_found)}/16")
    print("=" * 70)
    
    if len(colors_found) == 16:
        print("\n✓ SUCCESS: All 16 Kronos colors are correctly mapped!")
        print("\nColors found:")
        for color in sorted(colors_found):
            print(f"  • {color}")
        return True
    else:
        print(f"\n✗ INCOMPLETE: Only {len(colors_found)} colors mapped")
        return False

if __name__ == '__main__':
    filename = "SETLIST Movie TV Themes LOAD SEPARATELY 2.PCG"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    success = verify_colors(filename)
    sys.exit(0 if success else 1)
