#!/usr/bin/env python3
"""Test setlist parsing."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcg_tools.reader import read_pcg_file

TEST_FILE = "/Volumes/KEYBOARD/KORGSOUNDS/ULTIMATE COVERS narfsounds 3/SETLIST Narf Ultimate Covers.PCG"

print(f"\nTesting setlist parsing: {os.path.basename(TEST_FILE)}\n")

try:
    pcg = read_pcg_file(TEST_FILE)
    
    print(f"Program Banks: {len(pcg.program_banks)}")
    print(f"Combi Banks: {len(pcg.combi_banks)}")
    print(f"Set Lists: {len(pcg.set_lists)}")
    print(f"Has Set Lists: {pcg.has_set_lists}")
    
    if pcg.set_lists:
        print("\n" + "="*70)
        print("SET LISTS FOUND")
        print("="*70)
        
        for i, setlist in enumerate(pcg.set_lists[:3]):  # Show first 3
            print(f"\nSet List {i}: {setlist.name} (ID: {setlist.id})")
            print(f"  Description: {setlist.description}")
            print(f"  Slots: {len(setlist.slots)}")
            
            # Show first 5 slots
            for j, slot in enumerate(setlist.slots[:5]):
                print(f"\n  Slot {j}:")
                print(f"    Name: {slot.name}")
                print(f"    Description: {slot.description}")
                print(f"    Patch Type: {slot.patch_type}")
                print(f"    Patch Bank: {slot.patch_bank}")
                print(f"    Patch Index: {slot.patch_index}")
                print(f"    Patch ID: {slot.patch_id}")
                print(f"    Transpose: {slot.transpose}")
                print(f"    Volume: {slot.volume}")
                print(f"    Notes: {slot.notes[:50] if slot.notes else 'None'}")
    else:
        print("\n❌ No set lists found in file!")
        print("This indicates a parsing issue.")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
