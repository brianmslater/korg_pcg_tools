"""Unit tests for bit_utils module."""

import unittest
from pcg_tools.bit_utils import (
    get_bits, set_bits, to_signed_bit, from_signed_bit,
    get_bit, set_bit, clear_bit
)


class TestBitUtils(unittest.TestCase):
    """Test bit manipulation utilities."""
    
    def test_get_bits_full_byte(self):
        """Test getting all bits from a byte."""
        data = bytes([0b11010110])
        result = get_bits(data, 0, 7, 0)
        self.assertEqual(result, 0b11010110)
    
    def test_get_bits_high_nibble(self):
        """Test getting high nibble (bits 7-4)."""
        data = bytes([0b11010110])
        result = get_bits(data, 0, 7, 4)
        self.assertEqual(result, 0b1101)
    
    def test_get_bits_low_nibble(self):
        """Test getting low nibble (bits 3-0)."""
        data = bytes([0b11010110])
        result = get_bits(data, 0, 3, 0)
        self.assertEqual(result, 0b0110)
    
    def test_get_bits_middle_bits(self):
        """Test getting middle bits (bits 5-2)."""
        data = bytes([0b11010110])
        result = get_bits(data, 0, 5, 2)
        self.assertEqual(result, 0b0101)
    
    def test_set_bits_full_byte(self):
        """Test setting all bits in a byte."""
        data = bytearray([0b00000000])
        set_bits(data, 0, 7, 0, 0b11010110)
        self.assertEqual(data[0], 0b11010110)
    
    def test_set_bits_high_nibble(self):
        """Test setting high nibble (bits 7-4)."""
        data = bytearray([0b00001111])
        set_bits(data, 0, 7, 4, 0b1101)
        self.assertEqual(data[0], 0b11011111)
    
    def test_set_bits_low_nibble(self):
        """Test setting low nibble (bits 3-0)."""
        data = bytearray([0b11110000])
        set_bits(data, 0, 3, 0, 0b0110)
        self.assertEqual(data[0], 0b11110110)
    
    def test_set_bits_preserves_other_bits(self):
        """Test that setting bits preserves other bits."""
        data = bytearray([0b11110000])
        set_bits(data, 0, 5, 2, 0b1010)
        # Bits 7-6 should be 11, bits 5-2 should be 1010, bits 1-0 should be 00
        self.assertEqual(data[0], 0b11101000)
    
    def test_to_signed_bit_positive(self):
        """Test converting positive unsigned to signed."""
        # 6-bit: 0b011111 (31) -> 31
        result = to_signed_bit(6, 0b011111)
        self.assertEqual(result, 31)
    
    def test_to_signed_bit_negative(self):
        """Test converting negative unsigned to signed."""
        # 6-bit: 0b111111 (63) -> -1
        result = to_signed_bit(6, 0b111111)
        self.assertEqual(result, -1)
        
        # 6-bit: 0b100000 (32) -> -32
        result = to_signed_bit(6, 0b100000)
        self.assertEqual(result, -32)
    
    def test_from_signed_bit_positive(self):
        """Test converting positive signed to unsigned."""
        # 31 -> 0b011111 (31)
        result = from_signed_bit(6, 31)
        self.assertEqual(result, 0b011111)
    
    def test_from_signed_bit_negative(self):
        """Test converting negative signed to unsigned."""
        # -1 -> 0b111111 (63)
        result = from_signed_bit(6, -1)
        self.assertEqual(result, 0b111111)
        
        # -32 -> 0b100000 (32)
        result = from_signed_bit(6, -32)
        self.assertEqual(result, 0b100000)
    
    def test_signed_bit_round_trip(self):
        """Test round-trip conversion signed -> unsigned -> signed."""
        for value in range(-32, 32):
            unsigned = from_signed_bit(6, value)
            signed = to_signed_bit(6, unsigned)
            self.assertEqual(signed, value, f"Round-trip failed for {value}")
    
    def test_get_bit(self):
        """Test getting single bit."""
        data = bytes([0b10101010])
        self.assertTrue(get_bit(data, 0, 7))
        self.assertFalse(get_bit(data, 0, 6))
        self.assertTrue(get_bit(data, 0, 5))
        self.assertFalse(get_bit(data, 0, 4))
    
    def test_set_bit(self):
        """Test setting single bit."""
        data = bytearray([0b00000000])
        set_bit(data, 0, 7)
        self.assertEqual(data[0], 0b10000000)
        
        set_bit(data, 0, 0)
        self.assertEqual(data[0], 0b10000001)
    
    def test_clear_bit(self):
        """Test clearing single bit."""
        data = bytearray([0b11111111])
        clear_bit(data, 0, 7)
        self.assertEqual(data[0], 0b01111111)
        
        clear_bit(data, 0, 0)
        self.assertEqual(data[0], 0b01111110)
    
    def test_text_size_split_bits(self):
        """Test text size encoding (split across 2 bytes like in Kronos)."""
        # Text size is 3 bits: MSB (1 bit) in byte +29 bit 4, LSB (2 bits) in byte +24 bits 7-6
        data = bytearray([0] * 30)
        
        # Test all 5 text sizes
        for size in range(5):
            # Clear previous values
            data[24] = 0
            data[29] = 0
            
            # Set MSB (1 bit) in byte 29, bit 4
            msb = (size >> 2) & 0x01
            set_bits(data, 29, 4, 4, msb)
            
            # Set LSB (2 bits) in byte 24, bits 7-6
            lsb = size & 0x03
            set_bits(data, 24, 7, 6, lsb)
            
            # Read back
            read_msb = get_bits(data, 29, 4, 4)
            read_lsb = get_bits(data, 24, 7, 6)
            read_size = (read_msb << 2) | read_lsb
            
            self.assertEqual(read_size, size, f"Text size {size} encoding/decoding failed")
    
    def test_transpose_split_bits(self):
        """Test transpose encoding (split across 2 bytes, signed)."""
        # Transpose is 6 bits: MSB (3 bits) in byte +25 bits 7-5, LSB (3 bits) in byte +29 bits 7-5
        data = bytearray([0] * 30)
        
        # Test various transpose values
        test_values = [-24, -12, -1, 0, 1, 12, 24]
        
        for transpose in test_values:
            # Clear previous values
            data[25] = 0
            data[29] = 0
            
            # Convert to unsigned
            unsigned = from_signed_bit(6, transpose)
            
            # Set MSB (3 bits) in byte 25, bits 7-5
            msb = (unsigned >> 3) & 0x07
            set_bits(data, 25, 7, 5, msb)
            
            # Set LSB (3 bits) in byte 29, bits 7-5
            lsb = unsigned & 0x07
            set_bits(data, 29, 7, 5, lsb)
            
            # Read back
            read_msb = get_bits(data, 25, 7, 5)
            read_lsb = get_bits(data, 29, 7, 5)
            read_unsigned = (read_msb << 3) | read_lsb
            read_transpose = to_signed_bit(6, read_unsigned)
            
            self.assertEqual(read_transpose, transpose, 
                           f"Transpose {transpose} encoding/decoding failed")


if __name__ == '__main__':
    unittest.main()
