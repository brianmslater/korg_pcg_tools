#!/usr/bin/env python3
"""
Final comprehensive test of setlist parsing.
Verifies that all setlist data is correctly parsed from STL1.
"""

from pcg_tools.reader import PcgReader

def test_setlist_parsing():
    """Test that setlist parsing works correctly."""
    print("Setlist Parsing - Comprehensive Test")
    print("="*80)
    
    reader = PcgReader('test_files/soundcheck12012025.PCG')
    pcg = reader.read()
    
    # Test 1: Correct number of setlists
    assert len(pcg.set_lists) == 128, f"Expected 128 setlists, got {len(pcg.set_lists)}"
    print("✓ Test 1: 128 setlists parsed")
    
    # Test 2: Preload setlist exists and has correct data
    preload = pcg.set_lists[0]
    assert preload.name == "Preload Set List", f"Expected 'Preload Set List', got '{preload.name}'"
    assert len(preload.slots) == 128, f"Expected 128 slots, got {len(preload.slots)}"
    
    # Check first slot
    slot0 = preload.slots[0]
    assert slot0.name == "SGX-2", f"Expected 'SGX-2', got '{slot0.name}'"
    assert slot0.patch_type == "Combi", f"Expected 'Combi', got '{slot0.patch_type}'"
    assert slot0.patch_bank == "I-A", f"Expected 'I-A', got '{slot0.patch_bank}'"
    assert slot0.patch_index == 0, f"Expected 0, got {slot0.patch_index}"
    print("✓ Test 2: Preload setlist correct")
    
    # Test 3: Narf setlist has correct bank assignments (USER-D, not INT-A)
    narf = None
    for sl in pcg.set_lists:
        if sl.name == "Narf":
            narf = sl
            break
    
    assert narf is not None, "Narf setlist not found"
    
    # Check multiple slots to ensure bank is correct
    test_slots = [
        (0, "Beat It", "Program", "U-D", 0),
        (1, "Call Me", "Program", "U-D", 1),
        (5, "In The Air Tonight (Mic)", "Program", "U-D", 5),
        (10, "Shine On U Crazy Diamond", "Program", "U-D", 10),
    ]
    
    for slot_idx, expected_name, expected_type, expected_bank, expected_index in test_slots:
        slot = narf.slots[slot_idx]
        assert slot.name == expected_name, f"Slot {slot_idx}: Expected '{expected_name}', got '{slot.name}'"
        assert slot.patch_type == expected_type, f"Slot {slot_idx}: Expected '{expected_type}', got '{slot.patch_type}'"
        assert slot.patch_bank == expected_bank, f"Slot {slot_idx}: Expected '{expected_bank}', got '{slot.patch_bank}'"
        assert slot.patch_index == expected_index, f"Slot {slot_idx}: Expected {expected_index}, got {slot.patch_index}"
    
    print("✓ Test 3: Narf setlist has correct USER-D bank assignments")
    
    # Test 4: All setlists have 128 slots
    for sl in pcg.set_lists:
        assert len(sl.slots) == 128, f"Setlist '{sl.name}' has {len(sl.slots)} slots, expected 128"
    print("✓ Test 4: All setlists have 128 slots")
    
    # Test 5: Setlist indices are correct
    for i, sl in enumerate(pcg.set_lists):
        assert sl.index == i, f"Setlist {i} has index {sl.index}"
    print("✓ Test 5: Setlist indices are sequential")
    
    print()
    print("="*80)
    print("🎉 ALL TESTS PASSED!")
    print("="*80)
    print()
    print("Summary:")
    print(f"  - {len(pcg.set_lists)} setlists parsed")
    print(f"  - {sum(len(sl.slots) for sl in pcg.set_lists)} total slots")
    print(f"  - Bank ID decoding: CORRECT")
    print(f"  - STL1 parsing: COMPLETE")
    print()
    print("Setlist parsing is fully functional! ✅")


if __name__ == '__main__':
    test_setlist_parsing()
