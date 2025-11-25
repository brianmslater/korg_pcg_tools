#!/usr/bin/env python3
"""Test parsing nw.PCG file."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file

test_file = '/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG'

print(f"Reading: {test_file}\n")
pcg = read_pcg_file(test_file)

print(f"PCG loaded:")
print(f"  Program banks: {len(pcg.program_banks)}")
print(f"  Combi banks: {len(pcg.combi_banks)}")
print(f"  Set lists: {len(pcg.set_lists)}")
print(f"  has_set_lists: {pcg.has_set_lists}\n")

if pcg.set_lists:
    # Show first few setlists
    for i, sl in enumerate(pcg.set_lists[:5]):
        print(f"Setlist {i}: '{sl.name}' - {len(sl.slots)} slots")
        if sl.slots:
            print(f"  First 3 slots:")
            for slot in sl.slots[:3]:
                print(f"    {slot.slot_index}: '{slot.name}'")
        print()
else:
    print("No setlists found!")
