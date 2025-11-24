#!/usr/bin/env python3
"""Test reading the Movie Themes file."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file

def test():
    filename = 'test_files/SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    
    print(f"Reading: {filename}\n")
    
    pcg = read_pcg_file(filename)
    
    print(f"Found {len(pcg.set_lists)} setlists\n")
    
    for sl_idx, setlist in enumerate(pcg.set_lists[:3]):  # First 3 setlists
        print(f"Setlist {sl_idx}: '{setlist.name}'")
        print(f"  Slots: {len(setlist.slots)}")
        
        # Show first 20 non-empty slots
        shown = 0
        for slot in setlist.slots:
            if slot.name and shown < 20:
                print(f"    [{slot.slot_index:3d}] {slot.name}")
                if hasattr(slot, 'text_size'):
                    print(f"         Text size: {slot.text_size}")
                if hasattr(slot, 'color'):
                    print(f"         Color: {slot.color}")
                shown += 1
        print()

if __name__ == '__main__':
    test()
