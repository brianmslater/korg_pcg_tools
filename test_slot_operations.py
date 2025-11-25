"""Test setlist slot operations."""

import unittest
from pcg_tools.models import SetListSlot, SlotTextSize
from pcg_tools.operations import (
    clear_setlist_slot, swap_setlist_slots,
    batch_set_volume, batch_set_transpose, batch_set_text_size
)


class TestSlotOperations(unittest.TestCase):
    """Test setlist slot operations."""
    
    def test_clear_slot_basic(self):
        """Test clearing a slot resets all fields."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=5,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Set various fields
        slot.patch_type_value = 1
        slot.patch_bank_id = 5
        slot.patch_index_value = 100
        slot.transpose = 12
        slot.volume = 64
        slot.text_size = SlotTextSize.XL
        slot.description = "Test description"
        slot.color = 136
        
        # Clear the slot
        clear_setlist_slot(slot)
        
        # Verify all fields are reset
        self.assertEqual(slot.name, "Init Slot")
        self.assertEqual(slot.patch_type_value, 0)
        self.assertEqual(slot.patch_type, "Program")
        self.assertEqual(slot.patch_bank_id, 0)
        self.assertEqual(slot.patch_index_value, 0)
        self.assertEqual(slot.transpose, 0)
        self.assertEqual(slot.volume, 127)
        self.assertEqual(slot.text_size, SlotTextSize.M)
        self.assertEqual(slot.description, "")
        self.assertEqual(slot.color, 0)
    
    def test_clear_slot_without_raw_data(self):
        """Test clearing a slot without raw_data doesn't crash."""
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot"
        )
        
        # Should not crash
        clear_setlist_slot(slot)
        
        # Basic fields should be set
        self.assertEqual(slot.name, "Init Slot")
        self.assertEqual(slot.patch_type, "Program")
    
    def test_clear_slot_multiple_times(self):
        """Test clearing a slot multiple times is idempotent."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Clear once
        clear_setlist_slot(slot)
        first_state = (
            slot.name, slot.patch_type_value, slot.transpose,
            slot.volume, slot.text_size, slot.description
        )
        
        # Clear again
        clear_setlist_slot(slot)
        second_state = (
            slot.name, slot.patch_type_value, slot.transpose,
            slot.volume, slot.text_size, slot.description
        )
        
        # Should be identical
        self.assertEqual(first_state, second_state)
    
    def test_swap_slots(self):
        """Test swapping two slots."""
        raw_data1 = bytearray(542)
        raw_data2 = bytearray(542)
        
        slot1 = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Slot 1",
            raw_data=raw_data1
        )
        
        slot2 = SetListSlot(
            set_list_index=0,
            slot_index=1,
            name="Slot 2",
            raw_data=raw_data2
        )
        
        # Set different values
        slot1.patch_type_value = 0
        slot1.patch_bank_id = 1
        slot1.patch_index_value = 50
        slot1.transpose = 5
        slot1.text_size = SlotTextSize.L
        
        slot2.patch_type_value = 1
        slot2.patch_bank_id = 3
        slot2.patch_index_value = 100
        slot2.transpose = -12
        slot2.text_size = SlotTextSize.XS
        
        # Swap
        swap_setlist_slots(slot1, slot2)
        
        # Verify swap (indices should be swapped)
        self.assertEqual(slot1.slot_index, 1)
        self.assertEqual(slot2.slot_index, 0)
        
        # Verify data was swapped
        self.assertEqual(slot1.patch_type_value, 1)
        self.assertEqual(slot1.patch_bank_id, 3)
        self.assertEqual(slot1.patch_index_value, 100)
        self.assertEqual(slot1.transpose, -12)
        self.assertEqual(slot1.text_size, SlotTextSize.XS)
        
        self.assertEqual(slot2.patch_type_value, 0)
        self.assertEqual(slot2.patch_bank_id, 1)
        self.assertEqual(slot2.patch_index_value, 50)
        self.assertEqual(slot2.transpose, 5)
        self.assertEqual(slot2.text_size, SlotTextSize.L)
    
    def test_swap_slots_without_raw_data(self):
        """Test swapping slots without raw_data doesn't crash."""
        slot1 = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Slot 1"
        )
        
        slot2 = SetListSlot(
            set_list_index=0,
            slot_index=1,
            name="Slot 2"
        )
        
        # Should not crash
        swap_setlist_slots(slot1, slot2)
    
    def test_batch_set_volume(self):
        """Test setting volume for multiple slots."""
        slots = []
        for i in range(5):
            raw_data = bytearray(542)
            slot = SetListSlot(
                set_list_index=0,
                slot_index=i,
                name=f"Slot {i}",
                raw_data=raw_data
            )
            slots.append(slot)
        
        # Set volume to 80 for all
        batch_set_volume(slots, 80)
        
        # Verify all have volume 80
        for slot in slots:
            self.assertEqual(slot.volume, 80)
    
    def test_batch_set_volume_clamping(self):
        """Test that batch volume is clamped to valid range."""
        raw_data = bytearray(542)
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Slot",
            raw_data=raw_data
        )
        
        # Test beyond range
        batch_set_volume([slot], 200)
        self.assertEqual(slot.volume, 127)
        
        batch_set_volume([slot], -10)
        self.assertEqual(slot.volume, 0)
    
    def test_batch_set_transpose(self):
        """Test setting transpose for multiple slots."""
        slots = []
        for i in range(5):
            raw_data = bytearray(542)
            slot = SetListSlot(
                set_list_index=0,
                slot_index=i,
                name=f"Slot {i}",
                raw_data=raw_data
            )
            slots.append(slot)
        
        # Set transpose to +12 for all
        batch_set_transpose(slots, 12)
        
        # Verify all have transpose +12
        for slot in slots:
            self.assertEqual(slot.transpose, 12)
        
        # Set transpose to -5 for all
        batch_set_transpose(slots, -5)
        
        # Verify all have transpose -5
        for slot in slots:
            self.assertEqual(slot.transpose, -5)
    
    def test_batch_set_text_size(self):
        """Test setting text size for multiple slots."""
        slots = []
        for i in range(5):
            raw_data = bytearray(542)
            slot = SetListSlot(
                set_list_index=0,
                slot_index=i,
                name=f"Slot {i}",
                raw_data=raw_data
            )
            slots.append(slot)
        
        # Set text size to XL for all
        batch_set_text_size(slots, SlotTextSize.XL)
        
        # Verify all have text size XL
        for slot in slots:
            self.assertEqual(slot.text_size, SlotTextSize.XL)
        
        # Set text size to S for all
        batch_set_text_size(slots, SlotTextSize.S)
        
        # Verify all have text size S
        for slot in slots:
            self.assertEqual(slot.text_size, SlotTextSize.S)
    
    def test_batch_operations_empty_list(self):
        """Test batch operations with empty list don't crash."""
        # Should not crash
        batch_set_volume([], 100)
        batch_set_transpose([], 5)
        batch_set_text_size([], SlotTextSize.M)
    
    def test_batch_operations_single_slot(self):
        """Test batch operations with single slot."""
        raw_data = bytearray(542)
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Slot",
            raw_data=raw_data
        )
        
        batch_set_volume([slot], 90)
        self.assertEqual(slot.volume, 90)
        
        batch_set_transpose([slot], -10)
        self.assertEqual(slot.transpose, -10)
        
        batch_set_text_size([slot], SlotTextSize.L)
        self.assertEqual(slot.text_size, SlotTextSize.L)


if __name__ == '__main__':
    unittest.main()
