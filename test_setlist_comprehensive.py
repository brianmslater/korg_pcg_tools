#!/usr/bin/env python3
"""Comprehensive test of setlist parsing and writing."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file

def test_file(filepath, description):
    """Test a single PCG file."""
    print(f"\n{'='*70}")
    print(f"Testing: {description}")
    print(f"File: {filepath}")
    print('='*70)
    
    try:
        # Read
        pcg = read_pcg_file(filepath)
        print(f"\n✓ File loaded successfully")
        print(f"  Set lists: {len(pcg.set_lists)}")
        
        if not pcg.set_lists:
            print("  ✗ No setlists found")
            return False
        
        # Find first setlist with slots
        test_sl = None
        for sl in pcg.set_lists:
            if sl.slots:
                test_sl = sl
                break
        
        if not test_sl:
            print("  ✗ No setlists with slots found")
            return False
        
        print(f"  ✓ Found setlist: '{test_sl.name}' with {len(test_sl.slots)} slots")
        
        # Store originals
        original_sl_name = test_sl.name
        original_slot_name = test_sl.slots[0].name
        
        # Modify
        test_sl.name = "TEST MODIFIED"
        test_sl.slots[0].name = "TEST SLOT"
        
        # Write
        output_file = f'test_files/test_output_{Path(filepath).stem}.PCG'
        write_pcg_file(pcg, output_file)
        print(f"  ✓ File written to: {output_file}")
        
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
        
        # Verify
        if test_sl2.name != "TEST MODIFIED":
            print(f"  ✗ Setlist name mismatch: expected 'TEST MODIFIED', got '{test_sl2.name}'")
            return False
        
        if test_sl2.slots[0].name != "TEST SLOT":
            print(f"  ✗ Slot name mismatch: expected 'TEST SLOT', got '{test_sl2.slots[0].name}'")
            return False
        
        print(f"  ✓ Setlist name persisted: '{test_sl2.name}'")
        print(f"  ✓ Slot name persisted: '{test_sl2.slots[0].name}'")
        
        # Restore original values
        test_sl2.name = original_sl_name
        test_sl2.slots[0].name = original_slot_name
        write_pcg_file(pcg2, output_file)
        
        # Verify restoration
        pcg3 = read_pcg_file(output_file)
        test_sl3 = None
        for sl in pcg3.set_lists:
            if sl.slots:
                test_sl3 = sl
                break
        
        if test_sl3.name == original_sl_name and test_sl3.slots[0].name == original_slot_name:
            print(f"  ✓ Original values restored successfully")
        else:
            print(f"  ✗ Failed to restore original values")
            return False
        
        print(f"\n✓✓✓ ALL TESTS PASSED for {description} ✓✓✓")
        return True
        
    except Exception as e:
        print(f"\n✗✗✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "="*70)
    print("COMPREHENSIVE SETLIST PARSER TEST")
    print("="*70)
    
    test_files = [
        ('/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG', 'Nightwish Legacy'),
        ('/Volumes/KEYBOARD/KORGSOUNDS/ULTIMATE COVERS narfsounds/SETLIST Narf Ultimate Covers.PCG', 'NARF Ultimate Covers'),
        ('/Volumes/KEYBOARD/soundcheck9_25_25.PCG', 'Soundcheck 9/25/25'),
        ('/Volumes/KEYBOARD/soundcheck9_25_25_combined.PCG', 'Soundcheck Combined'),
        ('/Volumes/KEYBOARD/soundcheck9_25_25_combined2.PCG', 'Soundcheck Combined 2'),
    ]
    
    results = []
    for filepath, description in test_files:
        if Path(filepath).exists():
            result = test_file(filepath, description)
            results.append((description, result))
        else:
            print(f"\n✗ File not found: {filepath}")
            results.append((description, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for description, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {description}")
    
    all_passed = all(r for _, r in results)
    
    if all_passed:
        print("\n" + "="*70)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("="*70)
        print("\nSetlist parser is fully functional:")
        print("  ✓ Reads setlist names correctly")
        print("  ✓ Reads slot names correctly")
        print("  ✓ Writes setlist names correctly")
        print("  ✓ Writes slot names correctly")
        print("  ✓ Changes persist across save/load cycles")
        print("  ✓ Works with multiple PCG file formats")
        return 0
    else:
        print("\n✗ SOME TESTS FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(main())
