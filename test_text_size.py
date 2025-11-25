"""Test text size implementation in SetListSlot."""

import unittest
from pcg_tools.models import SetListSlot, SlotTextSize


class TestTextSize(unittest.TestCase):
    """Test text size reading and writing."""
    
    def test_text_size_enum_values(self):
        """Test that text size enum has correct values."""
        self.assertEqual(SlotTextSize.S.value, 0)
        self.assertEqual(SlotTextSize.XS.value, 1)
        self.assertEqual(SlotTextSize.M.value, 2)
        self.assertEqual(SlotTextSize.L.value, 3)
        self.assertEqual(SlotTextSize.XL.value, 4)
    
    def test_text_size_default(self):
        """Test default text size without raw_data."""
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot"
        )
        self.assertEqual(slot.text_size, SlotTextSize.M)
        self.assertEqual(slot.text_size_name, "M")
    
    def test_text_size_read_from_raw_data(self):
        """Test reading text size from raw data."""
        # Create slot with raw data
        raw_data = bytearray(542)  # Full slot size
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Test all 5 text sizes
        for size in SlotTextSize:
            # Set the size
            slot.text_size = size
            
            # Read it back
            read_size = slot.text_size
            self.assertEqual(read_size, size, 
                           f"Text size {size.name} not preserved")
            self.assertEqual(slot.text_size_name, size.name)
    
    def test_text_size_split_bits_encoding(self):
        """Test that text size is correctly encoded in split bits."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Test S (0 = 0b000)
        slot.text_size = SlotTextSize.S
        self.assertEqual((raw_data[29] >> 4) & 0x01, 0)  # MSB = 0
        self.assertEqual((raw_data[24] >> 6) & 0x03, 0)  # LSB = 00
        
        # Test XS (1 = 0b001)
        slot.text_size = SlotTextSize.XS
        self.assertEqual((raw_data[29] >> 4) & 0x01, 0)  # MSB = 0
        self.assertEqual((raw_data[24] >> 6) & 0x03, 1)  # LSB = 01
        
        # Test M (2 = 0b010)
        slot.text_size = SlotTextSize.M
        self.assertEqual((raw_data[29] >> 4) & 0x01, 0)  # MSB = 0
        self.assertEqual((raw_data[24] >> 6) & 0x03, 2)  # LSB = 10
        
        # Test L (3 = 0b011)
        slot.text_size = SlotTextSize.L
        self.assertEqual((raw_data[29] >> 4) & 0x01, 0)  # MSB = 0
        self.assertEqual((raw_data[24] >> 6) & 0x03, 3)  # LSB = 11
        
        # Test XL (4 = 0b100)
        slot.text_size = SlotTextSize.XL
        self.assertEqual((raw_data[29] >> 4) & 0x01, 1)  # MSB = 1
        self.assertEqual((raw_data[24] >> 6) & 0x03, 0)  # LSB = 00
    
    def test_text_size_preserves_other_bits(self):
        """Test that setting text size doesn't affect other bits."""
        raw_data = bytearray(542)
        
        # Set some other bits in byte 24 and 29
        raw_data[24] = 0b00111111  # Bits 5-0 set
        raw_data[29] = 0b11101111  # Bits 7-5 and 3-0 set
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Set text size to XL (should only affect bit 4 of byte 29 and bits 7-6 of byte 24)
        slot.text_size = SlotTextSize.XL
        
        # Check that other bits are preserved
        self.assertEqual(raw_data[24] & 0x3F, 0x3F)  # Bits 5-0 should still be set
        self.assertEqual(raw_data[29] & 0xEF, 0xEF)  # Bits 7-5 and 3-0 should still be set
    
    def test_text_size_round_trip(self):
        """Test round-trip encoding/decoding of all text sizes."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        for size in SlotTextSize:
            # Set the size
            slot.text_size = size
            
            # Create a new slot with the same raw data
            new_slot = SetListSlot(
                set_list_index=0,
                slot_index=0,
                name="Test Slot",
                raw_data=raw_data
            )
            
            # Verify it reads back correctly
            self.assertEqual(new_slot.text_size, size,
                           f"Round-trip failed for {size.name}")


if __name__ == '__main__':
    unittest.main()
