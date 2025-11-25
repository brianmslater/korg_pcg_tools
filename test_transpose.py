"""Test transpose implementation in SetListSlot."""

import unittest
from pcg_tools.models import SetListSlot


class TestTranspose(unittest.TestCase):
    """Test transpose reading and writing."""
    
    def test_transpose_default(self):
        """Test default transpose without raw_data."""
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot"
        )
        self.assertEqual(slot.transpose, 0)
    
    def test_transpose_positive_values(self):
        """Test positive transpose values."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Test positive values
        for value in [0, 1, 5, 12, 24]:
            slot.transpose = value
            self.assertEqual(slot.transpose, value,
                           f"Transpose {value} not preserved")
    
    def test_transpose_negative_values(self):
        """Test negative transpose values."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Test negative values
        for value in [-1, -5, -12, -24]:
            slot.transpose = value
            self.assertEqual(slot.transpose, value,
                           f"Transpose {value} not preserved")
    
    def test_transpose_clamping(self):
        """Test that transpose values are clamped to valid range."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Test values beyond range
        slot.transpose = 30
        self.assertEqual(slot.transpose, 24)
        
        slot.transpose = -30
        self.assertEqual(slot.transpose, -24)
    
    def test_transpose_split_bits_encoding(self):
        """Test that transpose is correctly encoded in split bits."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Test 0 (0b000000)
        slot.transpose = 0
        msb = (raw_data[25] >> 5) & 0x07
        lsb = (raw_data[29] >> 5) & 0x07
        self.assertEqual((msb << 3) | lsb, 0)
        
        # Test +12 (0b001100)
        slot.transpose = 12
        msb = (raw_data[25] >> 5) & 0x07
        lsb = (raw_data[29] >> 5) & 0x07
        self.assertEqual((msb << 3) | lsb, 12)
        
        # Test -1 (0b111111 in 6-bit signed)
        slot.transpose = -1
        msb = (raw_data[25] >> 5) & 0x07
        lsb = (raw_data[29] >> 5) & 0x07
        self.assertEqual((msb << 3) | lsb, 63)  # -1 as unsigned 6-bit
        
        # Test -24 (0b101000 in 6-bit signed)
        slot.transpose = -24
        msb = (raw_data[25] >> 5) & 0x07
        lsb = (raw_data[29] >> 5) & 0x07
        self.assertEqual((msb << 3) | lsb, 40)  # -24 as unsigned 6-bit
    
    def test_transpose_preserves_other_bits(self):
        """Test that setting transpose doesn't affect other bits."""
        raw_data = bytearray(542)
        
        # Set some other bits in byte 25 and 29
        raw_data[25] = 0b00011111  # Bits 4-0 set
        raw_data[29] = 0b00011111  # Bits 4-0 set
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Set transpose (should only affect bits 7-5 of both bytes)
        slot.transpose = 12
        
        # Check that other bits are preserved
        self.assertEqual(raw_data[25] & 0x1F, 0x1F)  # Bits 4-0 should still be set
        self.assertEqual(raw_data[29] & 0x1F, 0x1F)  # Bits 4-0 should still be set
    
    def test_transpose_round_trip(self):
        """Test round-trip encoding/decoding of transpose values."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Test full range
        for value in range(-24, 25):
            slot.transpose = value
            
            # Create a new slot with the same raw data
            new_slot = SetListSlot(
                set_list_index=0,
                slot_index=0,
                name="Test Slot",
                raw_data=raw_data
            )
            
            # Verify it reads back correctly
            self.assertEqual(new_slot.transpose, value,
                           f"Round-trip failed for transpose {value}")
    
    def test_transpose_and_text_size_independent(self):
        """Test that transpose and text size don't interfere with each other."""
        from pcg_tools.models import SlotTextSize
        
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Set both transpose and text size
        slot.transpose = 12
        slot.text_size = SlotTextSize.XL
        
        # Verify both are preserved
        self.assertEqual(slot.transpose, 12)
        self.assertEqual(slot.text_size, SlotTextSize.XL)
        
        # Change transpose, verify text size unchanged
        slot.transpose = -5
        self.assertEqual(slot.transpose, -5)
        self.assertEqual(slot.text_size, SlotTextSize.XL)
        
        # Change text size, verify transpose unchanged
        slot.text_size = SlotTextSize.S
        self.assertEqual(slot.transpose, -5)
        self.assertEqual(slot.text_size, SlotTextSize.S)


if __name__ == '__main__':
    unittest.main()
