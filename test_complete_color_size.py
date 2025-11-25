#!/usr/bin/env python3
"""Complete test of color and text size functionality."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file

def test_complete():
    print("="*80)
    print("COMPLETE COLOR AND TEXT SIZE TEST")
    print("="*80)
    
    input_file = 'SETLIST Movie TV Themes LOAD SEPARATELY.PCG'
    
    if not Path(input_file).exists():
        print(f"\n✗ File not found: {input_file}")
        return False
    
    # Step 1: Read
    print("\n1. Reading PCG file...")
    pcg = read_pcg_file(input_file)
    
    if len(pcg.set_lists) == 0:
        print("✗ No setlists found!")
        return False
    
    setlist = pcg.set_lists[0]
    print(f"✓ Loaded setlist: '{setlist.name}' with {len(setlist.slots)} slots")
    
    # Step 2: Display current values
    print("\n2. Current values:")
    for i in range(min(3, len(setlist.slots))):
        slot = setlist.slots[i]
        if slot.name:
            print(f"   Slot {i}: {slot.name}")
            print(f"     Color: {slot.color} ({slot.color_name})")
            print(f"     Size: {slot.text_size} ({slot.text_size_name})")
    
    # Step 3: Modify values
    print("\n3. Modifying values...")
    changes = []
    
    if len(setlist.slots) > 0 and setlist.slots[0].name:
        old_color = setlist.slots[0].color
        old_size = setlist.slots[0].text_size
        setlist.slots[0].color = 140  # Burgundy
        setlist.slots[0].text_size = 0  # M
        changes.append((0, old_color, old_size, 140, 0))
        print(f"   Slot 0: {old_color}→140 (Burgundy), {old_size}→0 (M)")
    
    if len(setlist.slots) > 1 and setlist.slots[1].name:
        old_color = setlist.slots[1].color
        old_size = setlist.slots[1].text_size
        setlist.slots[1].color = 32  # Indigo
        setlist.slots[1].text_size = 16  # XL
        changes.append((1, old_color, old_size, 32, 16))
        print(f"   Slot 1: {old_color}→32 (Indigo), {old_size}→16 (XL)")
    
    # Step 4: Write
    output_file = 'test_complete_output.PCG'
    print(f"\n4. Writing to: {output_file}")
    write_pcg_file(pcg, output_file)
    print("✓ File written")
    
    # Step 5: Read back
    print(f"\n5. Reading back: {output_file}")
    pcg2 = read_pcg_file(output_file)
    
    if len(pcg2.set_lists) == 0:
        print("✗ No setlists in output file!")
        return False
    
    setlist2 = pcg2.set_lists[0]
    print(f"✓ Loaded setlist: '{setlist2.name}'")
    
    # Step 6: Verify
    print("\n6. Verification:")
    all_passed = True
    
    for slot_idx, old_color, old_size, new_color, new_size in changes:
        slot = setlist2.slots[slot_idx]
        
        color_match = slot.color == new_color
        size_match = slot.text_size == new_size
        
        status = "✓" if (color_match and size_match) else "✗"
        print(f"   {status} Slot {slot_idx}: {slot.name}")
        
        if not color_match:
            print(f"      Color mismatch: got {slot.color}, expected {new_color}")
            all_passed = False
        else:
            print(f"      Color: {slot.color} ({slot.color_name}) ✓")
        
        if not size_match:
            print(f"      Size mismatch: got {slot.text_size}, expected {new_size}")
            all_passed = False
        else:
            print(f"      Size: {slot.text_size} ({slot.text_size_name}) ✓")
    
    # Summary
    print("\n" + "="*80)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print("="*80)
        print("\nColor and text size implementation is working correctly!")
        print("- Reading from STL1/SBK1 chunk: ✓")
        print("- Writing to STL1/SBK1 chunk: ✓")
        print("- Round-trip persistence: ✓")
        return True
    else:
        print("✗ SOME TESTS FAILED")
        print("="*80)
        return False

if __name__ == '__main__':
    success = test_complete()
    sys.exit(0 if success else 1)
