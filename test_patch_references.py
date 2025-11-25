"""Test patch reference implementation in SetListSlot."""

import unittest
from pcg_tools.models import SetListSlot


class TestPatchReferences(unittest.TestCase):
    """Test patch reference reading and writing."""
    
    def test_patch_type_default(self):
        """Test default patch type without raw_data."""
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            patch_type="Program"
        )
        self.assertEqual(slot.patch_type_value, 0)
    
    def test_patch_type_values(self):
        """Test all patch type values."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Test Program (0)
        slot.patch_type_value = 0
        self.assertEqual(slot.patch_type_value, 0)
        self.assertEqual(slot.patch_type, 'Program')
        
        # Test Combi (1)
        slot.patch_type_value = 1
        self.assertEqual(slot.patch_type_value, 1)
        self.assertEqual(slot.patch_type, 'Combi')
        
        # Test Song (2)
        slot.patch_type_value = 2
        self.assertEqual(slot.patch_type_value, 2)
        self.assertEqual(slot.patch_type, 'Song')
    
    def test_patch_type_encoding(self):
        """Test that patch type is correctly encoded in bits 1-0 of byte 24."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Test Program (0 = 0b00)
        slot.patch_type_value = 0
        self.assertEqual(raw_data[24] & 0x03, 0)
        
        # Test Combi (1 = 0b01)
        slot.patch_type_value = 1
        self.assertEqual(raw_data[24] & 0x03, 1)
        
        # Test Song (2 = 0b10)
        slot.patch_type_value = 2
        self.assertEqual(raw_data[24] & 0x03, 2)
    
    def test_patch_type_preserves_other_bits(self):
        """Test that setting patch type doesn't affect other bits in byte 24."""
        raw_data = bytearray(542)
        raw_data[24] = 0b11111100  # Set bits 7-2
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Set patch type (should only affect bits 1-0)
        slot.patch_type_value = 1
        
        # Check that other bits are preserved
        self.assertEqual(raw_data[24] & 0xFC, 0xFC)
    
    def test_bank_id_read_write(self):
        """Test reading and writing bank ID."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Test various bank IDs (0-31, since it's 5 bits)
        for bank_id in [0, 1, 5, 15, 23, 31]:
            slot.patch_bank_id = bank_id
            self.assertEqual(slot.patch_bank_id, bank_id,
                           f"Bank ID {bank_id} not preserved")
            # Bank ID is in bits 4-0 of byte 25
            self.assertEqual(raw_data[25] & 0x1F, bank_id)
    
    def test_patch_index_read_write(self):
        """Test reading and writing patch index."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Test various patch indices
        for index in [0, 1, 63, 127]:
            slot.patch_index_value = index
            self.assertEqual(slot.patch_index_value, index,
                           f"Patch index {index} not preserved")
            self.assertEqual(raw_data[26], index)
            self.assertEqual(slot.patch_index, index)
    
    def test_patch_index_clamping(self):
        """Test that patch index is clamped to 0-127."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Test value beyond range
        slot.patch_index_value = 200
        self.assertEqual(slot.patch_index_value, 200 & 0x7F)  # Should be masked
    
    def test_complete_patch_reference(self):
        """Test setting a complete patch reference."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Set a program reference: I-A (bank 0), patch 50
        slot.patch_type_value = 0  # Program
        slot.patch_bank_id = 0     # I-A
        slot.patch_index_value = 50
        
        # Verify all fields
        self.assertEqual(slot.patch_type_value, 0)
        self.assertEqual(slot.patch_type, 'Program')
        self.assertEqual(slot.patch_bank_id, 0)
        self.assertEqual(slot.patch_index_value, 50)
        
        # Change to a combi reference: I-C (bank 2), patch 100
        slot.patch_type_value = 1  # Combi
        slot.patch_bank_id = 2     # I-C
        slot.patch_index_value = 100
        
        # Verify all fields
        self.assertEqual(slot.patch_type_value, 1)
        self.assertEqual(slot.patch_type, 'Combi')
        self.assertEqual(slot.patch_bank_id, 2)
        self.assertEqual(slot.patch_index_value, 100)
    
    def test_patch_reference_round_trip(self):
        """Test round-trip encoding/decoding of patch references."""
        raw_data = bytearray(542)
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=raw_data
        )
        
        # Test various combinations
        test_cases = [
            (0, 0, 0),      # Program, I-A, patch 0
            (0, 5, 63),     # Program, I-F, patch 63
            (1, 2, 100),    # Combi, I-C, patch 100
            (1, 6, 127),    # Combi, I-G, patch 127
            (2, 0, 0),      # Song, bank 0, patch 0
        ]
        
        for patch_type, bank_id, patch_index in test_cases:
            # Set the reference
            slot.patch_type_value = patch_type
            slot.patch_bank_id = bank_id
            slot.patch_index_value = patch_index
            
            # Create a new slot with the same raw data
            new_slot = SetListSlot(
                set_list_index=0,
                slot_index=0,
                name="Test Slot",
                raw_data=raw_data
            )
            
            # Verify it reads back correctly
            self.assertEqual(new_slot.patch_type_value, patch_type,
                           f"Round-trip failed for type {patch_type}")
            self.assertEqual(new_slot.patch_bank_id, bank_id,
                           f"Round-trip failed for bank {bank_id}")
            self.assertEqual(new_slot.patch_index_value, patch_index,
                           f"Round-trip failed for index {patch_index}")
    
    def test_patch_reference_independent_of_other_fields(self):
        """Test that patch references don't interfere with other fields."""
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
        
        # Verify all are preserved
        self.assertEqual(slot.patch_type_value, 1)
        self.assertEqual(slot.patch_bank_id, 5)
        self.assertEqual(slot.patch_index_value, 100)
        self.assertEqual(slot.transpose, 12)
        self.assertEqual(slot.text_size, SlotTextSize.XL)
        
        # Change patch reference, verify others unchanged
        slot.patch_type_value = 0
        slot.patch_bank_id = 2
        slot.patch_index_value = 50
        
        self.assertEqual(slot.transpose, 12)
        self.assertEqual(slot.text_size, SlotTextSize.XL)
        
        # Change transpose and text size, verify patch reference unchanged
        slot.transpose = -5
        slot.text_size = SlotTextSize.S
        
        self.assertEqual(slot.patch_type_value, 0)
        self.assertEqual(slot.patch_bank_id, 2)
        self.assertEqual(slot.patch_index_value, 50)


if __name__ == '__main__':
    unittest.main()
