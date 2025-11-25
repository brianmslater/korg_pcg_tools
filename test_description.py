"""Test description implementation in SetListSlot."""

import unittest
from pcg_tools.models import SetListSlot


class TestDescription(unittest.TestCase):
    """Test description reading and writing."""
    
    def test_description_default(self):
        """Test default description without raw_data."""
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot"
        )
        self.assertEqual(slot.description, "")
    
    def test_description_short(self):
        """Test short description."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Set short description
        slot.description = "This is a test"
        self.assertEqual(slot.description, "This is a test")
    
    def test_description_long(self):
        """Test long description (up to 512 chars)."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Create a 512-character description
        long_desc = "A" * 512
        slot.description = long_desc
        self.assertEqual(slot.description, long_desc)
        self.assertEqual(len(slot.description), 512)
    
    def test_description_truncation(self):
        """Test that descriptions longer than 512 chars are truncated."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Try to set a 600-character description
        long_desc = "B" * 600
        slot.description = long_desc
        
        # Should be truncated to 512
        self.assertEqual(len(slot.description), 512)
        self.assertEqual(slot.description, "B" * 512)
    
    def test_description_multiline(self):
        """Test multi-line description with \\r\\n."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Set multi-line description
        multiline = "Line 1\r\nLine 2\r\nLine 3"
        slot.description = multiline
        self.assertEqual(slot.description, multiline)
    
    def test_description_special_chars(self):
        """Test description with special characters."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Set description with special chars
        special = "Test: 123, ABC! @#$%"
        slot.description = special
        self.assertEqual(slot.description, special)
    
    def test_description_empty(self):
        """Test setting empty description."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Set non-empty then clear
        slot.description = "Something"
        self.assertEqual(slot.description, "Something")
        
        slot.description = ""
        self.assertEqual(slot.description, "")
    
    def test_description_round_trip(self):
        """Test round-trip encoding/decoding of descriptions."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        test_descriptions = [
            "",
            "Short",
            "Medium length description with some text",
            "A" * 100,
            "A" * 512,
            "Multi\r\nLine\r\nText",
            "Special: !@#$%^&*()",
        ]
        
        for desc in test_descriptions:
            # Set the description
            slot.description = desc
            
            # Create a new slot with the same raw data
            new_slot = SetListSlot(
                set_list_index=0,
                slot_index=0,
                name="Test Slot",
                raw_data=raw_data
            )
            
            # Verify it reads back correctly
            self.assertEqual(new_slot.description, desc,
                           f"Round-trip failed for description: {desc[:50]}...")
    
    def test_description_null_termination(self):
        """Test that description is properly null-terminated."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Set a short description
        slot.description = "Test"
        
        # Check that it's null-terminated in raw data
        # Description starts at byte 30
        self.assertEqual(raw_data[30:34], b'Test')
        self.assertEqual(raw_data[34], 0)  # Null terminator
    
    def test_description_independent_of_other_fields(self):
        """Test that description doesn't interfere with other fields."""
        from pcg_tools.models import SlotTextSize
        
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Set all fields
        slot.patch_type_value = 1
        slot.patch_bank_id = 5
        slot.patch_index_value = 100
        slot.transpose = 12
        slot.text_size = SlotTextSize.XL
        slot.description = "This is a test description"
        
        # Verify all are preserved
        self.assertEqual(slot.patch_type_value, 1)
        self.assertEqual(slot.patch_bank_id, 5)
        self.assertEqual(slot.patch_index_value, 100)
        self.assertEqual(slot.transpose, 12)
        self.assertEqual(slot.text_size, SlotTextSize.XL)
        self.assertEqual(slot.description, "This is a test description")
        
        # Change description, verify others unchanged
        slot.description = "New description"
        
        self.assertEqual(slot.patch_type_value, 1)
        self.assertEqual(slot.patch_bank_id, 5)
        self.assertEqual(slot.patch_index_value, 100)
        self.assertEqual(slot.transpose, 12)
        self.assertEqual(slot.text_size, SlotTextSize.XL)


if __name__ == '__main__':
    unittest.main()
