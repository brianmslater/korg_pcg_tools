#!/usr/bin/env python3
"""Test writing color and text size to PCG files."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file

def test_write():
    # Read the file
    input_file = 'SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    
    if not Path(input_file).exists():
        print(f"File not found: {input_file}")
        return
    
    print(f"Reading: {input_file}\n")
    pcg = read_pcg_file(input_file)
    
    if len(pcg.set_lists) == 0:
        print("No setlists found!")
        return
    
    setlist = pcg.set_lists[0]
    print(f"Setlist: '{setlist.name}'")
    print(f"Slots: {len(setlist.slots)}\n")
    
    # Show original values
    print("Original values:")
    for i, slot in enumerate(setlist.slots[:3]):
        if slot.name:
            print(f"  Slot {i}: {slot.name}")
            print(f"    Color: {slot.color} ({slot.color_name})")
            print(f"    Size: {slot.text_size} ({slot.text_size_name})")
    
    # Modify some values
    print("\nModifying values...")
    if len(setlist.slots) > 0 and setlist.slots[0].name:
        setlist.slots[0].color = 140  # Burgundy
        setlist.slots[0].text_size = 0  # M
        print(f"  Slot 0: color={setlist.slots[0].color}, size={setlist.slots[0].text_size}")
    
    if len(setlist.slots) > 1 and setlist.slots[1].name:
        setlist.slots[1].color = 32  # Indigo
        setlist.slots[1].text_size = 16  # XL
        print(f"  Slot 1: color={setlist.slots[1].color}, size={setlist.slots[1].text_size}")
    
    # Write to new file
    output_file = 'test_output_color_size.PCG'
    print(f"\nWriting to: {output_file}")
    write_pcg_file(pcg, output_file)
    print("Done!")
    
    # Read back and verify
    print(f"\nReading back: {output_file}")
    pcg2 = read_pcg_file(output_file)
    
    if len(pcg2.set_lists) > 0:
        setlist2 = pcg2.set_lists[0]
        print(f"Setlist: '{setlist2.name}'")
        print("\nVerifying changes:")
        
        for i, slot in enumerate(setlist2.slots[:3]):
            if slot.name:
                print(f"  Slot {i}: {slot.name}")
                print(f"    Color: {slot.color} ({slot.color_name})")
                print(f"    Size: {slot.text_size} ({slot.text_size_name})")
        
        # Check if changes persisted
        print("\nVerification:")
        if len(setlist2.slots) > 0:
            slot0 = setlist2.slots[0]
            if slot0.color == 140 and slot0.text_size == 0:
                print("  ✓ Slot 0 changes persisted")
            else:
                print(f"  ✗ Slot 0 mismatch: color={slot0.color} (expected 140), size={slot0.text_size} (expected 0)")
        
        if len(setlist2.slots) > 1:
            slot1 = setlist2.slots[1]
            if slot1.color == 32 and slot1.text_size == 16:
                print("  ✓ Slot 1 changes persisted")
            else:
                print(f"  ✗ Slot 1 mismatch: color={slot1.color} (expected 32), size={slot1.text_size} (expected 16)")

if __name__ == '__main__':
    test_write()
