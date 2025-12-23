#!/usr/bin/env python3
"""Test setlist slot copy/paste functionality."""

import pytest
import os

TEST_FILE = "files_2_test/nw.PCG"
TEST_FILE_EXISTS = os.path.exists(TEST_FILE)

from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file
from pcg_tools.clipboard import get_clipboard
from pcg_tools.models import SetListSlot

@pytest.mark.skipif(not TEST_FILE_EXISTS, reason=f"Test file {TEST_FILE} not found")
def test_slot_copy_paste():
    """Test copying and pasting setlist slots."""
    
    # Read test file
    print("Reading test file...")
    pcg = read_pcg_file(TEST_FILE)
    
    # Get first setlist
    setlist = pcg.set_lists[0]
    print(f"\nSetlist: {setlist.name}")
    print(f"Slots: {len(setlist.slots)}")
    
    if len(setlist.slots) < 2:
        print("Not enough slots to test copy/paste")
        return
    
    # Get source and destination slots
    source_slot = setlist.slots[0]
    print(f"\nSource slot (index {source_slot.slot_index}):")
    print(f"  Name: {source_slot.name}")
    print(f"  Patch: {source_slot.patch_id}")
    print(f"  Transpose: {source_slot.transpose}")
    print(f"  Volume: {source_slot.volume}")
    print(f"  Color: {source_slot.color_name}")
    print(f"  Text Size: {source_slot.text_size_name}")
    
    # Copy the slot
    clipboard = get_clipboard()
    clipboard.copy_slot(source_slot)
    print("\n✓ Copied slot to clipboard")
    
    # Check clipboard
    assert clipboard.has_slot(), "Clipboard should have a slot"
    print("✓ Clipboard has slot")
    
    # Find or create destination slot
    dest_index = 10  # Paste to slot 10
    dest_slot = None
    for slot in setlist.slots:
        if slot.slot_index == dest_index:
            dest_slot = slot
            break
    
    if not dest_slot:
        # Create new slot
        dest_slot = SetListSlot(
            set_list_index=setlist.index,
            slot_index=dest_index,
            name="",
            notes="",
            patch_type="",
            patch_bank="",
            patch_index=0,
            transpose=0,
            volume=127
        )
        setlist.slots.append(dest_slot)
        print(f"\n✓ Created new slot at index {dest_index}")
    
    print(f"\nDestination slot (index {dest_slot.slot_index}) BEFORE paste:")
    print(f"  Name: {dest_slot.name}")
    print(f"  Patch: {dest_slot.patch_id}")
    
    # Paste the slot
    clipboard.paste_slot(dest_slot)
    print("\n✓ Pasted slot from clipboard")
    
    # Verify the paste
    print(f"\nDestination slot (index {dest_slot.slot_index}) AFTER paste:")
    print(f"  Name: {dest_slot.name}")
    print(f"  Patch: {dest_slot.patch_id}")
    print(f"  Transpose: {dest_slot.transpose}")
    print(f"  Volume: {dest_slot.volume}")
    print(f"  Color: {dest_slot.color_name}")
    print(f"  Text Size: {dest_slot.text_size_name}")
    
    # Verify properties match
    assert dest_slot.name == source_slot.name, "Names should match"
    assert dest_slot.patch_type == source_slot.patch_type, "Patch types should match"
    assert dest_slot.patch_bank == source_slot.patch_bank, "Patch banks should match"
    assert dest_slot.patch_index == source_slot.patch_index, "Patch indices should match"
    assert dest_slot.transpose == source_slot.transpose, "Transpose should match"
    assert dest_slot.volume == source_slot.volume, "Volume should match"
    assert dest_slot.color == source_slot.color, "Color should match"
    
    print("\n✓ All properties match!")
    print("\n✅ Copy/paste functionality works!")

if __name__ == "__main__":
    test_slot_copy_paste()
