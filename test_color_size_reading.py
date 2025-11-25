#!/usr/bin/env python3
"""Test reading color and text size from PCG files."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file
from pcg_tools import pcg_parser

# Enable debug output
pcg_parser.DEBUG = True

def test_color_size():
    # Test with the modified Movie Themes file
    filename = 'SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    
    if not Path(filename).exists():
        print(f"File not found: {filename}")
        print("Looking in test_files...")
        filename = 'test_files/SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
        if not Path(filename).exists():
            print(f"File not found: {filename}")
            return
    
    print(f"Reading: {filename}\n")
    
    pcg = read_pcg_file(filename)
    
    print(f"Found {len(pcg.set_lists)} setlists\n")
    
    if len(pcg.set_lists) > 0:
        setlist = pcg.set_lists[0]
        print(f"Setlist 0: '{setlist.name}'")
        print(f"Slots: {len(setlist.slots)}\n")
        
        # Show first 5 non-empty slots with their color and text size
        shown = 0
        for slot in setlist.slots:
            if slot.name and shown < 5:
                print(f"Slot {slot.slot_index}: {slot.name}")
                print(f"  Color: {slot.color} ({slot.color_name})")
                print(f"  Text Size: {slot.text_size} ({slot.text_size_name})")
                print()
                shown += 1
    
    print("\nExpected values (from your test):")
    print("  Slot 0 'Ghostbusters': Indigo (32), XL (16)")
    print("  Slot 1 'Never Ending Story': Burgundy (140), L (?)")

if __name__ == '__main__':
    test_color_size()
