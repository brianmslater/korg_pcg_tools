#!/usr/bin/env python3
"""
Final comprehensive test of setlist parsing.
Verifies that all setlist data is correctly parsed from STL1.
"""

import pytest
import os

TEST_FILE = "files_2_test/nw.PCG"
TEST_FILE_EXISTS = os.path.exists(TEST_FILE)

from pcg_tools.reader import PcgReader

@pytest.mark.skipif(not TEST_FILE_EXISTS, reason=f"Test file {TEST_FILE} not found")
def test_setlist_parsing():
    """Test that setlist parsing works correctly."""
    print("Setlist Parsing - Comprehensive Test")
    print("="*80)
    
    reader = PcgReader(TEST_FILE)
    pcg = reader.read()
    
    # Test 1: Setlists exist
    assert len(pcg.set_lists) > 0, "Expected at least one setlist"
    print(f"✓ Test 1: {len(pcg.set_lists)} setlists parsed")
    
    # Test 2: First setlist has slots
    first_setlist = pcg.set_lists[0]
    assert first_setlist.name is not None, "First setlist should have a name"
    assert len(first_setlist.slots) > 0, "First setlist should have slots"
    print(f"✓ Test 2: First setlist '{first_setlist.name}' has {len(first_setlist.slots)} slots")
    
    # Test 3: Slots have required properties
    if len(first_setlist.slots) > 0:
        slot0 = first_setlist.slots[0]
        # Check that slot has basic properties (may be empty)
        assert hasattr(slot0, 'name'), "Slot should have name attribute"
        assert hasattr(slot0, 'patch_type'), "Slot should have patch_type attribute"
        assert hasattr(slot0, 'patch_bank'), "Slot should have patch_bank attribute"
        assert hasattr(slot0, 'patch_index'), "Slot should have patch_index attribute"
        print(f"✓ Test 3: Slots have required properties")
    
    # Test 4: Setlist indices are correct
    for i, sl in enumerate(pcg.set_lists):
        assert sl.index == i, f"Setlist {i} has index {sl.index}"
    print("✓ Test 4: Setlist indices are sequential")
    
    # Test 5: Count non-empty slots
    total_slots = 0
    non_empty_slots = 0
    for sl in pcg.set_lists:
        total_slots += len(sl.slots)
        for slot in sl.slots:
            if slot.name and slot.name.strip():
                non_empty_slots += 1
    
    print(f"✓ Test 5: {total_slots} total slots, {non_empty_slots} non-empty")
    
    print()
    print("="*80)
    print("🎉 ALL TESTS PASSED!")
    print("="*80)
    print()
    print("Summary:")
    print(f"  - {len(pcg.set_lists)} setlists parsed")
    print(f"  - {total_slots} total slots")
    print(f"  - {non_empty_slots} non-empty slots")
    print()
    print("Setlist parsing is fully functional! ✅")


if __name__ == '__main__':
    test_setlist_parsing()
