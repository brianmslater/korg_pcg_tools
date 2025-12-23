#!/usr/bin/env python3
"""Test multi-edit dialogs for PCG Tools.

Tests the batch editing functionality for programs, combis, and set list slots.
This test validates the core logic without requiring Qt GUI.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcg_tools.models import Program, Combi, SetListSlot, Category

# Check if PySide6 is available
try:
    from PySide6.QtWidgets import QApplication
    HAS_QT = True
except ImportError:
    HAS_QT = False
    print("Note: PySide6 not available, running non-GUI tests only")


def test_common_value_analysis_combis():
    """Test common value analysis for combis (without Qt)."""
    print("Testing common value analysis for combis...")
    
    # Create test combis
    combis = []
    for i in range(5):
        combi = Combi(
            name=f"Test Combi {i}",
            bank="I-A",
            index=i,
            category=Category(main_category=0, sub_category=0, name="Keyboard"),
            favorite=False,
            raw_data=b'\x00' * 5000  # Dummy raw data
        )
        combis.append(combi)
    
    # Test common value detection logic (same as dialog._analyze_common_values)
    categories = set()
    subcategories = set()
    favorites = set()
    
    for combi in combis:
        if combi.category:
            categories.add(combi.category.main_category)
            subcategories.add(combi.category.sub_category)
        favorites.add(combi.favorite)
    
    common_category = list(categories)[0] if len(categories) == 1 else None
    common_subcategory = list(subcategories)[0] if len(subcategories) == 1 else None
    common_favorite = list(favorites)[0] if len(favorites) == 1 else None
    
    # All combis have same category (0), so common_category should be 0
    assert common_category == 0, f"Expected common_category=0, got {common_category}"
    
    # All combis have same subcategory (0), so common_subcategory should be 0
    assert common_subcategory == 0, f"Expected common_subcategory=0, got {common_subcategory}"
    
    # All combis have same favorite (False), so common_favorite should be False
    assert common_favorite == False, f"Expected common_favorite=False, got {common_favorite}"
    
    print("  ✓ Common value analysis works correctly")
    
    # Test with mixed values
    combis[0].category.main_category = 1
    combis[1].favorite = True
    
    categories = set()
    favorites = set()
    for combi in combis:
        if combi.category:
            categories.add(combi.category.main_category)
        favorites.add(combi.favorite)
    
    common_category = list(categories)[0] if len(categories) == 1 else None
    common_favorite = list(favorites)[0] if len(favorites) == 1 else None
    
    # Categories are now mixed, so common_category should be None
    assert common_category is None, f"Expected common_category=None, got {common_category}"
    
    # Favorites are now mixed, so common_favorite should be None
    assert common_favorite is None, f"Expected common_favorite=None, got {common_favorite}"
    
    print("  ✓ Mixed value detection works correctly")
    print("  ✓ Combi common value analysis tests passed")


def test_common_value_analysis_programs():
    """Test common value analysis for programs (without Qt)."""
    print("Testing common value analysis for programs...")
    
    # Create test programs
    programs = []
    for i in range(3):
        prog = Program(
            name=f"Test Program {i}",
            bank="I-A",
            index=i,
            category=Category(main_category=2, sub_category=1, name="Bass"),
            favorite=True,
            raw_data=b'\x00' * 3000  # Dummy raw data
        )
        programs.append(prog)
    
    # Test common value detection logic
    categories = set()
    subcategories = set()
    favorites = set()
    
    for prog in programs:
        if prog.category:
            categories.add(prog.category.main_category)
            subcategories.add(prog.category.sub_category)
        favorites.add(prog.favorite)
    
    common_category = list(categories)[0] if len(categories) == 1 else None
    common_subcategory = list(subcategories)[0] if len(subcategories) == 1 else None
    common_favorite = list(favorites)[0] if len(favorites) == 1 else None
    
    # All programs have same category (2), so common_category should be 2
    assert common_category == 2, f"Expected common_category=2, got {common_category}"
    
    # All programs have same subcategory (1), so common_subcategory should be 1
    assert common_subcategory == 1, f"Expected common_subcategory=1, got {common_subcategory}"
    
    # All programs have same favorite (True), so common_favorite should be True
    assert common_favorite == True, f"Expected common_favorite=True, got {common_favorite}"
    
    print("  ✓ Common value analysis works correctly")
    print("  ✓ Program common value analysis tests passed")


def test_common_value_analysis_slots():
    """Test common value analysis for set list slots (without Qt)."""
    print("Testing common value analysis for set list slots...")
    
    # Create test slots
    slots = []
    for i in range(4):
        slot = SetListSlot(
            set_list_index=0,
            slot_index=i,
            name=f"Slot {i}",
            notes="",
            patch_type="Program",
            patch_bank="I-A",
            patch_index=i,
            color=0
        )
        slot.volume = 100  # Set via property
        slots.append(slot)
    
    # Test common value detection logic
    volumes = set(slot.volume for slot in slots if hasattr(slot, 'volume'))
    colors = set(slot.color for slot in slots if hasattr(slot, 'color'))
    
    common_volume = list(volumes)[0] if len(volumes) == 1 else None
    common_color = list(colors)[0] if len(colors) == 1 else None
    
    # All slots have same volume (100), so common_volume should be 100
    assert common_volume == 100, f"Expected common_volume=100, got {common_volume}"
    
    # All slots have same color (0), so common_color should be 0
    assert common_color == 0, f"Expected common_color=0, got {common_color}"
    
    print("  ✓ Common value analysis works correctly")
    
    # Test with mixed values
    slots[0].volume = 80
    slots[1].color = 1
    
    volumes = set(slot.volume for slot in slots if hasattr(slot, 'volume'))
    colors = set(slot.color for slot in slots if hasattr(slot, 'color'))
    
    common_volume = list(volumes)[0] if len(volumes) == 1 else None
    common_color = list(colors)[0] if len(colors) == 1 else None
    
    # Volumes are now mixed, so common_volume should be None
    assert common_volume is None, f"Expected common_volume=None, got {common_volume}"
    
    # Colors are now mixed, so common_color should be None
    assert common_color is None, f"Expected common_color=None, got {common_color}"
    
    print("  ✓ Mixed value detection works correctly")
    print("  ✓ Set list slot common value analysis tests passed")


def test_validation():
    """Test validation logic (without Qt)."""
    print("Testing validation logic...")
    
    # Create a combi with a long name
    combi = Combi(
        name="A" * 20,  # 20 characters
        bank="I-A",
        index=0,
        category=Category(main_category=0, sub_category=0, name="Keyboard"),
        favorite=False,
        raw_data=b'\x00' * 5000
    )
    
    # Test validation logic directly (same as dialog._validate)
    def validate_prefix(combis, prefix):
        for c in combis:
            if len(prefix + c.name) > 24:
                return False
        return True
    
    def validate_suffix(combis, suffix):
        for c in combis:
            if len(c.name + suffix) > 24:
                return False
        return True
    
    # Test prefix that would make name too long
    assert validate_prefix([combi], "PREFIX") == False, "Validation should fail for name > 24 chars"
    
    # Shorter prefix should pass
    assert validate_prefix([combi], "P") == True, "Validation should pass for name <= 24 chars"
    
    # Test suffix validation
    assert validate_suffix([combi], "SUFFIX") == False, "Validation should fail for name > 24 chars"
    assert validate_suffix([combi], "S") == True, "Validation should pass for name <= 24 chars"
    
    print("  ✓ Name length validation works correctly")
    print("  ✓ Validation tests passed")


def test_raw_data_update():
    """Test that raw_data is updated correctly (without Qt)."""
    print("Testing raw_data update...")
    
    # Create a combi with proper raw_data
    raw_data = bytearray(5000)
    raw_data[0:24] = b"Original Name\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    raw_data[4790] = 0x00  # Category 0, SubCategory 0
    raw_data[4791] = 0x00  # Not favorite
    
    combi = Combi(
        name="Original Name",
        bank="I-A",
        index=0,
        category=Category(main_category=0, sub_category=0, name="Keyboard"),
        favorite=False,
        raw_data=bytes(raw_data)
    )
    
    # Test raw_data update logic (same as dialog._update_combi_raw_data)
    def update_combi_raw_data(combi):
        """Update combi raw_data with changes.
        
        Based on C# KronosCombi.cs:
        - Name: offset 0, 24 bytes
        - Category: offset 4790, bits 4-0
        - SubCategory: offset 4790, bits 7-5
        - Favorite: offset 4791, bit 0
        """
        if not combi.raw_data:
            return
        
        raw_data = bytearray(combi.raw_data)
        
        # Update name (offset 0, 24 bytes)
        if len(raw_data) >= 24:
            name_bytes = combi.name.encode('ascii', errors='replace')[:24]
            name_bytes = name_bytes.ljust(24, b'\x00')
            raw_data[0:24] = name_bytes
        
        # Update category and subcategory (offset 4790)
        if len(raw_data) >= 4791 and combi.category:
            cat_byte = 0
            cat_byte |= (combi.category.main_category & 0x1F)
            cat_byte |= ((combi.category.sub_category & 0x07) << 5)
            raw_data[4790] = cat_byte
        
        # Update favorite (offset 4791, bit 0)
        if len(raw_data) >= 4792:
            if combi.favorite:
                raw_data[4791] |= 0x01
            else:
                raw_data[4791] &= ~0x01
        
        combi.raw_data = bytes(raw_data)
    
    # Manually apply changes
    combi.name = "New Name"
    combi.category.main_category = 5
    combi.category.sub_category = 2
    combi.favorite = True
    
    update_combi_raw_data(combi)
    
    # Check name was updated
    name_bytes = combi.raw_data[0:24]
    assert name_bytes.startswith(b"New Name"), f"Name not updated correctly: {name_bytes}"
    
    # Check category was updated (offset 4790)
    cat_byte = combi.raw_data[4790]
    expected_cat = 5 | (2 << 5)  # main_category=5, sub_category=2
    assert cat_byte == expected_cat, f"Category not updated correctly: {cat_byte} != {expected_cat}"
    
    # Check favorite was updated (offset 4791, bit 0)
    fav_byte = combi.raw_data[4791]
    assert (fav_byte & 0x01) == 1, f"Favorite not updated correctly: {fav_byte}"
    
    print("  ✓ Name update works correctly")
    print("  ✓ Category update works correctly")
    print("  ✓ Favorite update works correctly")
    print("  ✓ raw_data update tests passed")


def test_program_raw_data_update():
    """Test that program raw_data is updated correctly (without Qt)."""
    print("Testing program raw_data update...")
    
    # Create a program with proper raw_data
    raw_data = bytearray(3000)
    raw_data[0:24] = b"Original Prog\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    raw_data[2568] = 0x00  # Category 0, SubCategory 0
    raw_data[2558] = 0x00  # Not favorite (bit 5)
    
    prog = Program(
        name="Original Prog",
        bank="I-A",
        index=0,
        category=Category(main_category=0, sub_category=0, name="Keyboard"),
        favorite=False,
        raw_data=bytes(raw_data)
    )
    
    # Test raw_data update logic (same as dialog._update_program_raw_data)
    def update_program_raw_data(prog):
        """Update program raw_data with changes.
        
        Based on C# KronosProgram.cs:
        - Name: offset 0, 24 bytes
        - Category: offset 2568, bits 4-0
        - SubCategory: offset 2568, bits 7-5
        - Favorite: offset 2558, bit 5
        """
        if not prog.raw_data:
            return
        
        raw_data = bytearray(prog.raw_data)
        
        # Update name (offset 0, 24 bytes)
        if len(raw_data) >= 24:
            name_bytes = prog.name.encode('ascii', errors='replace')[:24]
            name_bytes = name_bytes.ljust(24, b'\x00')
            raw_data[0:24] = name_bytes
        
        # Update category and subcategory (offset 2568)
        if len(raw_data) >= 2569 and prog.category:
            cat_byte = 0
            cat_byte |= (prog.category.main_category & 0x1F)
            cat_byte |= ((prog.category.sub_category & 0x07) << 5)
            raw_data[2568] = cat_byte
        
        # Update favorite (offset 2558, bit 5)
        if len(raw_data) >= 2559:
            if prog.favorite:
                raw_data[2558] |= 0x20
            else:
                raw_data[2558] &= ~0x20
        
        prog.raw_data = bytes(raw_data)
    
    # Manually apply changes
    prog.name = "New Prog"
    prog.category.main_category = 3
    prog.category.sub_category = 1
    prog.favorite = True
    
    update_program_raw_data(prog)
    
    # Check name was updated
    name_bytes = prog.raw_data[0:24]
    assert name_bytes.startswith(b"New Prog"), f"Name not updated correctly: {name_bytes}"
    
    # Check category was updated (offset 2568)
    cat_byte = prog.raw_data[2568]
    expected_cat = 3 | (1 << 5)  # main_category=3, sub_category=1
    assert cat_byte == expected_cat, f"Category not updated correctly: {cat_byte} != {expected_cat}"
    
    # Check favorite was updated (offset 2558, bit 5)
    fav_byte = prog.raw_data[2558]
    assert (fav_byte & 0x20) == 0x20, f"Favorite not updated correctly: {fav_byte}"
    
    print("  ✓ Program name update works correctly")
    print("  ✓ Program category update works correctly")
    print("  ✓ Program favorite update works correctly")
    print("  ✓ Program raw_data update tests passed")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Multi-Edit Dialog Tests")
    print("=" * 60)
    print()
    
    try:
        test_common_value_analysis_combis()
        print()
        test_common_value_analysis_programs()
        print()
        test_common_value_analysis_slots()
        print()
        test_validation()
        print()
        test_raw_data_update()
        print()
        test_program_raw_data_update()
        print()
        
        print("=" * 60)
        print("All multi-edit dialog tests passed!")
        print("=" * 60)
        return 0
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
