#!/usr/bin/env python3
"""Test SLD1 parsing."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file

test_file = '/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG'

print(f"Reading: {test_file}\n")
pcg = read_pcg_file(test_file)

if pcg.set_lists:
    sl = pcg.set_lists[0]
    print(f"Setlist 0: '{sl.name}'")
    print(f"Total slots: {len(sl.slots)}\n")
    
    print("First 10 slots:")
    for i, slot in enumerate(sl.slots[:10]):
        print(f"  Slot {slot.slot_index}: '{slot.name}'")
    
    print("\n✓ SLD1 parsing working!" if sl.slots[0].name == "SLEEPING INTRO" else "\n✗ SLD1 parsing failed")
else:
    print("No setlists found!")
