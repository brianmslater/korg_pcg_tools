"""Integration tests for complete setlist slot functionality."""

import unittest
from pcg_tools.models import SetListSlot, SlotTextSize
from pcg_tools.operations import clear_setlist_slot, swap_setlist_slots


class TestSetlistIntegration(unittest.TestCase):
    """Integration tests for all setlist slot features."""
    
    def test_complete_slot_workflow(self):
        """Test a complete workflow of creating and editing a slot."""
        raw_data = bytearray(542)
        
        # Create a slot
        slot = SetListSlot(
            set_list_index=0,
            slot_index=10,
            name="My Song",
            raw_data=raw_data
        )
        
        # Set all properties
        slot.patch_type_value = 1  # Combi
        slot.patch_bank_id = 5     # I-F
        slot.patch_index_value = 75
        slot.transpose = 7
        slot.volume = 110
        slot.text_size = SlotTextSize.L
        slot.description = "Verse: soft\r\nChorus: loud\r\nBridge: build up"
        slot.color = 144  # Ivy
        
        # Verify all properties
        self.assertEqual(slot.name, "My Song")
        self.assertEqual(slot.patch_type_value, 1)
        self.assertEqual(slot.patch_type, "Combi")
        self.assertEqual(slot.patch_bank_id, 5)
        self.assertEqual(slot.patch_index_value, 75)
        self.assertEqual(slot.transpose, 7)
        self.assertEqual(slot.volume, 110)
        self.assertEqual(slot.text_size, SlotTextSize.L)
        self.assertEqual(slot.text_size_name, "L")
        self.assertIn("Verse: soft", slot.description)
        self.assertIn("Chorus: loud", slot.description)
        self.assertEqual(slot.color, 144)
        
        # Modify some properties
        slot.transpose = -3
        slot.text_size = SlotTextSize.XL
        
        # Verify modifications
        self.assertEqual(slot.transpose, -3)
        self.assertEqual(slot.text_size, SlotTextSize.XL)
        
        # Other properties should be unchanged
        self.assertEqual(slot.patch_type_value, 1)
        self.assertEqual(slot.patch_bank_id, 5)
        self.assertEqual(slot.volume, 110)
    
    def test_slot_round_trip(self):
        """Test that all slot data survives round-trip through raw_data."""
        raw_data = bytearray(542)
        
        # Create and configure slot
        slot1 = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test",
            raw_data=raw_data
        )
        
        slot1.patch_type_value = 0
        slot1.patch_bank_id = 3
        slot1.patch_index_value = 99
        slot1.transpose = -12
        slot1.volume = 85
        slot1.text_size = SlotTextSize.XS
        slot1.description = "Test description with\r\nmultiple lines"
        
        # Create new slot with same raw_data
        slot2 = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="",
            raw_data=raw_data
        )
        
        # Verify all data matches
        self.assertEqual(slot2.patch_type_value, 0)
        self.assertEqual(slot2.patch_bank_id, 3)
        self.assertEqual(slot2.patch_index_value, 99)
        self.assertEqual(slot2.transpose, -12)
        self.assertEqual(slot2.volume, 85)
        self.assertEqual(slot2.text_size, SlotTextSize.XS)
        self.assertEqual(slot2.description, "Test description with\r\nmultiple lines")
    
    def test_all_text_sizes(self):
        """Test all 5 text sizes work correctly."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test",
            raw_data=raw_data
        )
        
        sizes = [SlotTextSize.S, SlotTextSize.XS, SlotTextSize.M, 
                 SlotTextSize.L, SlotTextSize.XL]
        
        for size in sizes:
            slot.text_size = size
            self.assertEqual(slot.text_size, size)
            self.assertEqual(slot.text_size_name, size.name)
    
    def test_transpose_full_range(self):
        """Test transpose works across full range."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test",
            raw_data=raw_data
        )
        
        # Test full range
        for transpose in range(-24, 25):
            slot.transpose = transpose
            self.assertEqual(slot.transpose, transpose)
    
    def test_patch_references_all_types(self):
        """Test all patch reference types."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test",
            raw_data=raw_data
        )
        
        # Test Program
        slot.patch_type_value = 0
        slot.patch_bank_id = 0
        slot.patch_index_value = 50
        self.assertEqual(slot.patch_type, "Program")
        self.assertEqual(slot.patch_bank_id, 0)
        self.assertEqual(slot.patch_index_value, 50)
        
        # Test Combi
        slot.patch_type_value = 1
        slot.patch_bank_id = 6
        slot.patch_index_value = 100
        self.assertEqual(slot.patch_type, "Combi")
        self.assertEqual(slot.patch_bank_id, 6)
        self.assertEqual(slot.patch_index_value, 100)
        
        # Test Song
        slot.patch_type_value = 2
        self.assertEqual(slot.patch_type, "Song")
    
    def test_clear_and_reconfigure(self):
        """Test clearing a slot and reconfiguring it."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Original",
            raw_data=raw_data
        )
        
        # Configure slot
        slot.patch_type_value = 1
        slot.patch_bank_id = 5
        slot.patch_index_value = 75
        slot.transpose = 12
        slot.text_size = SlotTextSize.XL
        slot.description = "Original description"
        
        # Clear it
        clear_setlist_slot(slot)
        
        # Verify cleared
        self.assertEqual(slot.name, "Init Slot")
        self.assertEqual(slot.patch_type_value, 0)
        self.assertEqual(slot.transpose, 0)
        self.assertEqual(slot.text_size, SlotTextSize.M)
        self.assertEqual(slot.description, "")
        
        # Reconfigure with new values
        slot.name = "New Song"
        slot.patch_type_value = 0
        slot.patch_bank_id = 2
        slot.patch_index_value = 30
        slot.transpose = -5
        slot.text_size = SlotTextSize.S
        slot.description = "New description"
        
        # Verify new configuration
        self.assertEqual(slot.name, "New Song")
        self.assertEqual(slot.patch_type_value, 0)
        self.assertEqual(slot.patch_bank_id, 2)
        self.assertEqual(slot.patch_index_value, 30)
        self.assertEqual(slot.transpose, -5)
        self.assertEqual(slot.text_size, SlotTextSize.S)
        self.assertEqual(slot.description, "New description")
    
    def test_swap_configured_slots(self):
        """Test swapping two fully configured slots."""
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
        
        # Configure slot 1
        slot1.patch_type_value = 0
        slot1.patch_bank_id = 1
        slot1.patch_index_value = 25
        slot1.transpose = 5
        slot1.text_size = SlotTextSize.L
        slot1.description = "Description 1"
        
        # Configure slot 2
        slot2.patch_type_value = 1
        slot2.patch_bank_id = 4
        slot2.patch_index_value = 80
        slot2.transpose = -10
        slot2.text_size = SlotTextSize.XS
        slot2.description = "Description 2"
        
        # Swap
        swap_setlist_slots(slot1, slot2)
        
        # Verify swap
        self.assertEqual(slot1.patch_type_value, 1)
        self.assertEqual(slot1.patch_bank_id, 4)
        self.assertEqual(slot1.patch_index_value, 80)
        self.assertEqual(slot1.transpose, -10)
        self.assertEqual(slot1.text_size, SlotTextSize.XS)
        self.assertEqual(slot1.description, "Description 2")
        
        self.assertEqual(slot2.patch_type_value, 0)
        self.assertEqual(slot2.patch_bank_id, 1)
        self.assertEqual(slot2.patch_index_value, 25)
        self.assertEqual(slot2.transpose, 5)
        self.assertEqual(slot2.text_size, SlotTextSize.L)
        self.assertEqual(slot2.description, "Description 1")
    
    def test_maximum_description_length(self):
        """Test that 512-character descriptions work correctly."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test",
            raw_data=raw_data
        )
        
        # Create exactly 512 characters
        desc = "A" * 256 + "B" * 256
        slot.description = desc
        
        # Verify it's preserved
        self.assertEqual(len(slot.description), 512)
        self.assertEqual(slot.description, desc)
        
        # Verify it's in raw data
        desc_bytes = bytes(slot.raw_data[30:542])
        self.assertEqual(desc_bytes[:512], desc.encode('ascii'))


if __name__ == '__main__':
    unittest.main()
