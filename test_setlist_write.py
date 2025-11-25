#!/usr/bin/env python3
"""Test setlist writing."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file

test_file = '/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG'
output_file = 'test_files/nw_modified.PCG'

print(f"Reading: {test_file}\n")
pcg = read_pcg_file(test_file)

if pcg.set_lists:
    sl = pcg.set_lists[0]
    print(f"Original setlist: '{sl.name}'")
    print(f"Slots: {len(sl.slots)}\n")
    
    # Modify setlist name
    sl.name = "MODIFIED SETLIST"
    
    # Modify first slot name
    if sl.slots:
        original_name = sl.slots[0].name
        sl.slots[0].name = "MODIFIED SLOT"
        print(f"Changed slot 0: '{original_name}' -> '{sl.slots[0].name}'\n")
    
    # Write
    print(f"Writing to: {output_file}")
    write_pcg_file(pcg, output_file)
    print("Done!\n")
    
    # Read back
    print("Reading back...")
    pcg2 = read_pcg_file(output_file)
    
    sl2 = pcg2.set_lists[0]
    print(f"Setlist name: '{sl2.name}'")
    if sl2.slots:
        print(f"Slot 0: '{sl2.slots[0].name}'")
    
    # Verify
    if sl2.name == "MODIFIED SETLIST" and sl2.slots[0].name == "MODIFIED SLOT":
        print("\n✓ SUCCESS! Changes persisted correctly.")
    else:
        print("\n✗ FAILED! Changes did not persist.")
else:
    print("No setlists found!")
