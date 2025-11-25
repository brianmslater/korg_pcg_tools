#!/usr/bin/env python3
"""
Automated Hardware Test - Make Sample Edits
============================================
This script loads a PCG file, makes test edits, and saves for hardware testing.
"""

import sys
sys.path.insert(0, '.')

from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file
from pcg_tools.models import SlotTextSize

def main():
    # Use STL1 format file which has raw_data attached
    input_file = 'SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    output_file = 'SETLIST_Movie_TV_HARDWARE_TEST.PCG'
    
    print("🎯 Automated Hardware Test")
    print("=" * 60)
    print(f"\n📂 Loading: {input_file}")
    
    # Load PCG
    pcg = read_pcg_file(input_file)
    print(f"✓ Loaded {len(pcg.set_lists)} setlists")
    
    # Make test edits to first setlist
    if pcg.set_lists:
        setlist = pcg.set_lists[0]
        print(f"\n📝 Making test edits to: {setlist.name}")
        print(f"   Original slots: {len(setlist.slots)}")
        
        changes = []
        
        # Edit first 5 slots with different changes
        for i in range(min(5, len(setlist.slots))):
            slot = setlist.slots[i]
            if slot.name:
                # Debug: check if raw_data exists
                if not slot.raw_data:
                    print(f"   ⚠️  Slot {i} has no raw_data - changes may not persist")
                
                original_name = slot.name
                original_transpose = slot.transpose
                original_size = slot.text_size_name
                
                # Make different edits to each slot
                # Use property setters to update raw_data
                if i == 0:
                    # Slot 0: Change text size to Large
                    slot.text_size = SlotTextSize.L
                    changes.append(f"Slot {i}: Text size {original_size} → Large")
                    
                elif i == 1:
                    # Slot 1: Transpose up 12 semitones
                    slot.transpose = 12
                    changes.append(f"Slot {i}: Transpose {original_transpose} → +12")
                    
                elif i == 2:
                    # Slot 2: Transpose down 12 semitones
                    slot.transpose = -12
                    changes.append(f"Slot {i}: Transpose {original_transpose} → -12")
                    
                elif i == 3:
                    # Slot 3: Change text size to Small
                    slot.text_size = SlotTextSize.S
                    changes.append(f"Slot {i}: Text size {original_size} → Small")
                    
                elif i == 4:
                    # Slot 4: Transpose +5
                    slot.transpose = 5
                    changes.append(f"Slot {i}: Transpose {original_transpose} → +5")
        
        print("\n✏️  Changes made:")
        for change in changes:
            print(f"   • {change}")
    
    # Save modified PCG
    print(f"\n💾 Saving to: {output_file}")
    write_pcg_file(pcg, output_file)
    print("✓ File saved successfully")
    
    # Verify changes by re-reading
    print("\n🔍 Verifying changes...")
    pcg_verify = read_pcg_file(output_file)
    setlist_verify = pcg_verify.set_lists[0]
    
    print("\n✅ Verification:")
    for i in range(min(5, len(setlist_verify.slots))):
        slot = setlist_verify.slots[i]
        if slot.name:
            print(f"   Slot {i}: {slot.name}")
            print(f"      Text Size: {slot.text_size_name}, Transpose: {slot.transpose:+d}")
    
    print("\n" + "=" * 60)
    print("🎯 HARDWARE TESTING INSTRUCTIONS")
    print("=" * 60)
    print(f"\n1. Copy this file to USB: {output_file}")
    print("2. Load on your Kronos")
    print("3. Go to the first setlist")
    print("4. Check these slots:")
    print()
    print("   Slot 0: Should have LARGE text")
    print("   Slot 1: Should play 1 octave UP (+12)")
    print("   Slot 2: Should play 1 octave DOWN (-12)")
    print("   Slot 3: Should have SMALL text")
    print("   Slot 4: Should play +5 semitones up")
    print()
    print("5. Report back if everything works correctly!")
    print("=" * 60)

if __name__ == '__main__':
    main()
