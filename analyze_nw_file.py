#!/usr/bin/env python3
"""Analyze the nw.PCG file to see what's happening with setlists."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file


def analyze():
    # Try to find the file
    possible_paths = [
        'nw.PCG',
        'NW.PCG',
        '/Volumes/KEYBOARD/nw.PCG',
        '/Volumes/KEYBOARD/NW.PCG',
    ]
    
    pcg_file = None
    for path in possible_paths:
        if Path(path).exists():
            pcg_file = path
            break
    
    if not pcg_file:
        print("Could not find nw.PCG file")
        print("Please provide the full path to the file")
        return
    
    print(f"Analyzing: {pcg_file}")
    print("="*70)
    
    pcg = read_pcg_file(pcg_file)
    
    print(f"\nSetlists found: {len(pcg.set_lists)}")
    
    for i, setlist in enumerate(pcg.set_lists):
        print(f"\nSetlist {i}: '{setlist.name}'")
        print(f"  Slots: {len(setlist.slots)}")
        
        # Show first 5 slots
        for slot in setlist.slots[:5]:
            print(f"    Slot {slot.slot_index}: '{slot.name}' -> {slot.patch_id} T:{slot.transpose:+d} V:{slot.volume}")
        
        if len(setlist.slots) > 5:
            print(f"    ... and {len(setlist.slots) - 5} more slots")


if __name__ == '__main__':
    analyze()
