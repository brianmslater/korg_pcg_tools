#!/usr/bin/env python3
"""Test parsing and writing NARF Ultimate Covers setlist."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file

test_file = '/Volumes/KEYBOARD/KORGSOUNDS/ULTIMATE COVERS narfsounds/SETLIST Narf Ultimate Covers.PCG'
output_file = 'test_files/narf_modified.PCG'

print(f"Reading: {test_file}\n")
pcg = read_pcg_file(test_file)

print(f"PCG loaded:")
print(f"  Program banks: {len(pcg.program_banks)}")
print(f"  Combi banks: {len(pcg.combi_banks)}")
print(f"  Set lists: {len(pcg.set_lists)}")
print(f"  has_set_lists: {pcg.has_set_lists}\n")

if pcg.set_lists:
    # Show first few setlists with slots
    print("Setlists with content:")
    for i, sl in enumerate(pcg.set_lists):
        if sl.slots:
            print(f"\nSetlist {i}: '{sl.name}' - {len(sl.slots)} slots")
            print(f"  First 5 slots:")
            for slot in sl.slots[:5]:
                print(f"    {slot.slot_index}: '{slot.name}'")
            
            if i >= 2:  # Show first 3 setlists with content
                break
    
    # Test modification
    print("\n" + "="*70)
    print("TESTING MODIFICATIONS")
    print("="*70)
    
    # Find first setlist with slots
    test_sl = None
    for sl in pcg.set_lists:
        if sl.slots:
            test_sl = sl
            break
    
    if test_sl:
        print(f"\nOriginal setlist: '{test_sl.name}'")
        original_sl_name = test_sl.name
        
        if test_sl.slots:
            original_slot_name = test_sl.slots[0].name
            print(f"Original slot 0: '{original_slot_name}'")
            
            # Modify
            test_sl.name = "MODIFIED NARF"
            test_sl.slots[0].name = "MODIFIED SLOT"
            
            print(f"\nModified setlist: '{test_sl.name}'")
            print(f"Modified slot 0: '{test_sl.slots[0].name}'")
            
            # Write
            print(f"\nWriting to: {output_file}")
            write_pcg_file(pcg, output_file)
            print("Done!")
            
            # Read back
            print("\nReading back...")
            pcg2 = read_pcg_file(output_file)
            
            # Find the same setlist
            test_sl2 = None
            for sl in pcg2.set_lists:
                if sl.slots:
                    test_sl2 = sl
                    break
            
            if test_sl2:
                print(f"Setlist name: '{test_sl2.name}'")
                if test_sl2.slots:
                    print(f"Slot 0: '{test_sl2.slots[0].name}'")
                
                # Verify
                if test_sl2.name == "MODIFIED NARF" and test_sl2.slots[0].name == "MODIFIED SLOT":
                    print("\n✓ SUCCESS! Changes persisted correctly.")
                else:
                    print(f"\n✗ FAILED!")
                    print(f"  Expected setlist: 'MODIFIED NARF', got: '{test_sl2.name}'")
                    print(f"  Expected slot: 'MODIFIED SLOT', got: '{test_sl2.slots[0].name}'")
else:
    print("No setlists found!")
