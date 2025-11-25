#!/usr/bin/env python3
"""Test setlist GUI functionality."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcg_tools.reader import read_pcg_file

TEST_FILE = "/Volumes/KEYBOARD/KORGSOUNDS/ULTIMATE COVERS narfsounds 3/SETLIST Narf Ultimate Covers.PCG"

print(f"\nTesting setlist GUI data: {os.path.basename(TEST_FILE)}\n")

try:
    pcg = read_pcg_file(TEST_FILE)
    
    print(f"Set Lists: {len(pcg.set_lists)}")
    print(f"Has Set Lists: {pcg.has_set_lists}")
    
    if pcg.set_lists:
        print("\n" + "="*70)
        print("SETLIST SUMMARY")
        print("="*70)
        
        for i, setlist in enumerate(pcg.set_lists):
            slot_count = len(setlist.slots)
            print(f"{i}: {setlist.name:<20} ({slot_count} slots)")
        
        # Show details of first setlist with slots
        for setlist in pcg.set_lists:
            if setlist.slots:
                print("\n" + "="*70)
                print(f"FIRST SETLIST WITH SLOTS: {setlist.name}")
                print("="*70)
                
                for i, slot in enumerate(setlist.slots[:10]):
                    trans_str = f"{slot.transpose:+3d}" if slot.transpose != 0 else "  0"
                    print(f"{slot.slot_index:3d}  {slot.name:<24} {slot.patch_id:<10} {trans_str} {slot.volume:3d}")
                
                if len(setlist.slots) > 10:
                    print(f"... and {len(setlist.slots) - 10} more slots")
                
                break
        
        print("\n✅ Setlist data is ready for GUI display!")
        print("   - Setlist names can be shown in dropdown")
        print("   - Slot data can be displayed in listbox")
        print("   - Notes field is available for editing")
        
    else:
        print("\n❌ No set lists found in file!")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
