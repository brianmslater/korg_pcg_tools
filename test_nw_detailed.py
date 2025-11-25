#!/usr/bin/env python3
"""Detailed test of nw.PCG parsing."""

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
    
    print("All slots:")
    for slot in sl.slots:
        print(f"  Slot {slot.slot_index}: '{slot.name}'")
else:
    print("No setlists found!")
