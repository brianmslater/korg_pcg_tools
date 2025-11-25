#!/usr/bin/env python3
"""Comprehensive test of complete setlist functionality."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file


def test():
    test_file = Path('test_files/files/GLAM V3/GLAMV3.PCG')
    
    print("COMPREHENSIVE SETLIST FUNCTIONALITY TEST")
    print("="*70)
    
    # Read
    print("\n1. Reading original file...")
    pcg = read_pcg_file(str(test_file))
    
    if not pcg.set_lists or not pcg.set_lists[0].slots:
        print("No slots found!")
        return 1
    
    # Show original
    print(f"\n2. Original data:")
    print(f"   Setlist 0: '{pcg.set_lists[0].name}'")
    slot0 = pcg.set_lists[0].slots[0]
    slot1 = pcg.set_lists[0].slots[1]
    print(f"   Slot 0: '{slot0.name}' -> {slot0.patch_id} T:{slot0.transpose:+d} V:{slot0.volume}")
    print(f"   Slot 1: '{slot1.name}' -> {slot1.patch_id} T:{slot1.transpose:+d} V:{slot1.volume}")
    
    # Modify everything
    print(f"\n3. Modifying all data types...")
    pcg.set_lists[0].name = "FULL TEST"
    slot0.name = "Modified Name"
    slot0.transpose = -5
    slot0.volume = 90
    slot1.transpose = 10
    slot1.volume = 120
    
    print(f"   Setlist name: '{pcg.set_lists[0].name}'")
    print(f"   Slot 0: '{slot0.name}' T:{slot0.transpose:+d} V:{slot0.volume}")
    print(f"   Slot 1: '{slot1.name}' T:{slot1.transpose:+d} V:{slot1.volume}")
    
    # Write
    output_file = test_file.parent / f"{test_file.stem}_complete_test.PCG"
    print(f"\n4. Writing to: {output_file.name}")
    write_pcg_file(pcg, str(output_file))
    print("   Done!")
    
    # Read back
    print("\n5. Reading back...")
    pcg2 = read_pcg_file(str(output_file))
    slot0_new = pcg2.set_lists[0].slots[0]
    slot1_new = pcg2.set_lists[0].slots[1]
    
    print(f"   Setlist 0: '{pcg2.set_lists[0].name}'")
    print(f"   Slot 0: '{slot0_new.name}' -> {slot0_new.patch_id} T:{slot0_new.transpose:+d} V:{slot0_new.volume}")
    print(f"   Slot 1: '{slot1_new.name}' -> {slot1_new.patch_id} T:{slot1_new.transpose:+d} V:{slot1_new.volume}")
    
    # Verify
    print("\n6. Verification:")
    all_pass = True
    
    if pcg2.set_lists[0].name == "FULL TEST":
        print("   ✓ Setlist name")
    else:
        print(f"   ✗ Setlist name (expected 'FULL TEST', got '{pcg2.set_lists[0].name}')")
        all_pass = False
    
    if slot0_new.name == "Modified Name":
        print("   ✓ Slot 0 name")
    else:
        print(f"   ✗ Slot 0 name (expected 'Modified Name', got '{slot0_new.name}')")
        all_pass = False
    
    if slot0_new.transpose == -5:
        print("   ✓ Slot 0 transpose")
    else:
        print(f"   ✗ Slot 0 transpose (expected -5, got {slot0_new.transpose})")
        all_pass = False
    
    if slot0_new.volume == 90:
        print("   ✓ Slot 0 volume")
    else:
        print(f"   ✗ Slot 0 volume (expected 90, got {slot0_new.volume})")
        all_pass = False
    
    if slot1_new.transpose == 10:
        print("   ✓ Slot 1 transpose")
    else:
        print(f"   ✗ Slot 1 transpose (expected 10, got {slot1_new.transpose})")
        all_pass = False
    
    if slot1_new.volume == 120:
        print("   ✓ Slot 1 volume")
    else:
        print(f"   ✗ Slot 1 volume (expected 120, got {slot1_new.volume})")
        all_pass = False
    
    print("\n" + "="*70)
    if all_pass:
        print("✓✓✓ ALL TESTS PASSED! ✓✓✓")
        print("\n🎉 SETLIST SUPPORT IS NOW FULLY FUNCTIONAL! 🎉")
        print("\nWhat works:")
        print("  ✓ Reading all setlist data")
        print("  ✓ Editing setlist names")
        print("  ✓ Editing slot names")
        print("  ✓ Editing slot transpose values")
        print("  ✓ Editing slot volume values")
        print("  ✓ Saving all changes to PCG files")
        print("  ✓ Changes persist across file save/load cycles")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(test())
