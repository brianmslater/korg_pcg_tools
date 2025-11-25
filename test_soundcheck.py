#!/usr/bin/env python3
"""Test parsing soundcheck PCG files."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file

def test_soundcheck_file(filepath):
    """Test a soundcheck PCG file."""
    print(f"\n{'='*70}")
    print(f"Testing: {Path(filepath).name}")
    print('='*70)
    
    try:
        # Read
        pcg = read_pcg_file(filepath)
        print(f"\n✓ File loaded successfully")
        print(f"  Program banks: {len(pcg.program_banks)}")
        print(f"  Combi banks: {len(pcg.combi_banks)}")
        print(f"  Set lists: {len(pcg.set_lists)}")
        print(f"  has_set_lists: {pcg.has_set_lists}")
        
        if not pcg.set_lists:
            print("  ℹ No setlists in this file")
            return True
        
        # Show setlists
        print(f"\nSetlists found:")
        for i, sl in enumerate(pcg.set_lists):
            if sl.slots:
                print(f"  {i}: '{sl.name}' - {len(sl.slots)} slots")
                if i < 3:  # Show first 3 slots of first 3 setlists
                    for slot in sl.slots[:3]:
                        print(f"      Slot {slot.slot_index}: '{slot.name}'")
        
        # Find first setlist with slots for testing
        test_sl = None
        for sl in pcg.set_lists:
            if sl.slots:
                test_sl = sl
                break
        
        if not test_sl:
            print("  ℹ No setlists with slots found")
            return True
        
        # Test modification
        print(f"\n{'='*70}")
        print("Testing modifications...")
        print('='*70)
        
        original_sl_name = test_sl.name
        original_slot_name = test_sl.slots[0].name
        
        print(f"Original setlist: '{original_sl_name}'")
        print(f"Original slot 0: '{original_slot_name}'")
        
        # Modify
        test_sl.name = "SOUNDCHECK TEST"
        test_sl.slots[0].name = "TEST SLOT"
        
        # Write
        output_file = f'test_files/test_{Path(filepath).stem}.PCG'
        write_pcg_file(pcg, output_file)
        print(f"\n✓ Written to: {output_file}")
        
        # Read back
        pcg2 = read_pcg_file(output_file)
        
        # Find the same setlist
        test_sl2 = None
        for sl in pcg2.set_lists:
            if sl.slots:
                test_sl2 = sl
                break
        
        if not test_sl2:
            print("  ✗ Could not find setlist in reloaded file")
            return False
        
        print(f"Read back setlist: '{test_sl2.name}'")
        print(f"Read back slot 0: '{test_sl2.slots[0].name}'")
        
        # Verify
        if test_sl2.name != "SOUNDCHECK TEST":
            print(f"\n✗ Setlist name mismatch!")
            return False
        
        if test_sl2.slots[0].name != "TEST SLOT":
            print(f"\n✗ Slot name mismatch!")
            return False
        
        print(f"\n✓✓✓ ALL TESTS PASSED ✓✓✓")
        return True
        
    except Exception as e:
        print(f"\n✗✗✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "="*70)
    print("SOUNDCHECK PCG FILES TEST")
    print("="*70)
    
    test_files = [
        '/Volumes/KEYBOARD/soundcheck9_25_25.PCG',
        '/Volumes/KEYBOARD/soundcheck9_25_25_combined.PCG',
        '/Volumes/KEYBOARD/soundcheck9_25_25_combined2.PCG',
    ]
    
    results = []
    for filepath in test_files:
        if Path(filepath).exists():
            result = test_soundcheck_file(filepath)
            results.append((Path(filepath).name, result))
        else:
            print(f"\n✗ File not found: {filepath}")
            results.append((Path(filepath).name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for filename, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {filename}")
    
    all_passed = all(r for _, r in results)
    
    if all_passed:
        print("\n✓ All soundcheck files tested successfully!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
