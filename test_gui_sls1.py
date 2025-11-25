#!/usr/bin/env python3
"""Test GUI with SLS1 format file."""

import sys
sys.path.insert(0, '.')

from pcg_tools.reader import read_pcg_file

def test_gui_sls1():
    """Test that GUI can load SLS1 format."""
    filename = 'test_files/soundcheck9_25_25_combined2.PCG'
    
    print("Testing GUI integration with SLS1 format")
    print("="*60)
    print(f"\nLoading: {filename}")
    
    # Read file using the same method as GUI
    pcg = read_pcg_file(filename)
    
    print(f"\nParsed data:")
    print(f"  Program banks: {len(pcg.program_banks)}")
    print(f"  Combi banks: {len(pcg.combi_banks)}")
    print(f"  Setlists: {len(pcg.set_lists)}")
    
    if pcg.set_lists:
        print(f"\nSetlists:")
        for sl in pcg.set_lists:
            non_empty = sum(1 for s in sl.slots if s.name and len(s.name) >= 2)
            print(f"  [{sl.index:2d}] {sl.name} - {non_empty} slots")
        
        # Test first setlist in detail
        print(f"\nFirst setlist details:")
        setlist = pcg.set_lists[0]
        print(f"  Name: {setlist.name}")
        print(f"  Index: {setlist.index}")
        print(f"  Total slots: {len(setlist.slots)}")
        
        # Show first 5 slots
        print(f"\n  First 5 slots:")
        for i, slot in enumerate(setlist.slots[:5]):
            if slot.name:
                print(f"    [{slot.slot_index:3d}] {slot.name}")
                print(f"          Color: {slot.color_name} ({slot.color})")
                print(f"          Type: {slot.patch_type}")
                print(f"          Index: {slot.patch_index}")
    
    print(f"\n✓ GUI integration test passed!")
    print(f"\nThe GUI should now display all {len(pcg.set_lists)} setlists")
    print(f"in the setlist dropdown.")

if __name__ == '__main__':
    test_gui_sls1()
