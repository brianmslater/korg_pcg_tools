"""Tests for CRC calculation functionality.

Tests the CRC calculation based on C# Patch.CalcCrc().
"""

import pytest
from pcg_tools.models import Program, Combi, Category, Timbre


class TestProgramCrc:
    """Test CRC calculation for programs."""
    
    def test_calc_crc_empty_data(self):
        """Empty raw_data should return 0."""
        program = Program(bank="INT-A", index=0, name="Test")
        assert program.calc_crc(True) == 0
        assert program.calc_crc(False) == 0
    
    def test_calc_crc_including_name(self):
        """CRC including name should sum all bytes."""
        # Create program with known raw data
        raw_data = bytes([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])  # Sum = 55
        program = Program(bank="INT-A", index=0, name="Test", raw_data=raw_data)
        
        assert program.calc_crc(True) == 55
    
    def test_calc_crc_excluding_name(self):
        """CRC excluding name should skip first 24 bytes."""
        # Create program with 30 bytes of data
        # First 24 bytes (name) = 1 each = 24
        # Last 6 bytes = 10 each = 60
        raw_data = bytes([1] * 24 + [10] * 6)
        program = Program(bank="INT-A", index=0, name="Test", raw_data=raw_data)
        
        # Including name: 24 + 60 = 84
        assert program.calc_crc(True) == 84
        
        # Excluding name: 60
        assert program.calc_crc(False) == 60
    
    def test_calc_crc_modulo(self):
        """CRC should be modulo 65536."""
        # Create data that sums to more than 65536
        raw_data = bytes([255] * 300)  # Sum = 76500
        program = Program(bank="INT-A", index=0, name="Test", raw_data=raw_data)
        
        expected = 76500 % 65536  # = 10964
        assert program.calc_crc(True) == expected
    
    def test_calc_crc_short_data(self):
        """CRC excluding name with data shorter than 24 bytes."""
        raw_data = bytes([1, 2, 3, 4, 5])  # Only 5 bytes
        program = Program(bank="INT-A", index=0, name="Test", raw_data=raw_data)
        
        # Including name: 15
        assert program.calc_crc(True) == 15
        
        # Excluding name: starts at byte 24, but data is only 5 bytes
        # So sum of bytes[24:] = 0
        assert program.calc_crc(False) == 0


class TestCombiCrc:
    """Test CRC calculation for combis."""
    
    def test_calc_crc_empty_data(self):
        """Empty raw_data should return 0."""
        combi = Combi(bank="INT-A", index=0, name="Test")
        assert combi.calc_crc(True) == 0
        assert combi.calc_crc(False) == 0
    
    def test_calc_crc_including_name(self):
        """CRC including name should sum all bytes."""
        raw_data = bytes([5, 10, 15, 20, 25])  # Sum = 75
        combi = Combi(bank="INT-A", index=0, name="Test", raw_data=raw_data)
        
        assert combi.calc_crc(True) == 75
    
    def test_calc_crc_excluding_name(self):
        """CRC excluding name should skip first 24 bytes."""
        # Create combi with 30 bytes of data
        raw_data = bytes([2] * 24 + [20] * 6)
        combi = Combi(bank="INT-A", index=0, name="Test", raw_data=raw_data)
        
        # Including name: 48 + 120 = 168
        assert combi.calc_crc(True) == 168
        
        # Excluding name: 120
        assert combi.calc_crc(False) == 120


class TestCrcComparison:
    """Test CRC for patch comparison use cases."""
    
    def test_identical_patches_same_crc(self):
        """Identical patches should have same CRC."""
        raw_data = bytes([1, 2, 3, 4, 5] * 10)
        
        prog1 = Program(bank="INT-A", index=0, name="Test", raw_data=raw_data)
        prog2 = Program(bank="INT-A", index=1, name="Test", raw_data=raw_data)
        
        assert prog1.calc_crc(True) == prog2.calc_crc(True)
        assert prog1.calc_crc(False) == prog2.calc_crc(False)
    
    def test_different_name_same_crc_excl(self):
        """Patches with different names but same data should have same CRC excluding name."""
        # Same data after name
        base_data = bytes([100] * 6)
        
        # Different names (first 24 bytes)
        raw_data1 = bytes([ord('A')] * 24) + base_data
        raw_data2 = bytes([ord('B')] * 24) + base_data
        
        prog1 = Program(bank="INT-A", index=0, name="AAAA", raw_data=raw_data1)
        prog2 = Program(bank="INT-A", index=1, name="BBBB", raw_data=raw_data2)
        
        # CRC including name should be different
        assert prog1.calc_crc(True) != prog2.calc_crc(True)
        
        # CRC excluding name should be same
        assert prog1.calc_crc(False) == prog2.calc_crc(False)
    
    def test_different_data_different_crc(self):
        """Patches with different data should have different CRC."""
        raw_data1 = bytes([1] * 30)
        raw_data2 = bytes([2] * 30)
        
        prog1 = Program(bank="INT-A", index=0, name="Test", raw_data=raw_data1)
        prog2 = Program(bank="INT-A", index=1, name="Test", raw_data=raw_data2)
        
        assert prog1.calc_crc(True) != prog2.calc_crc(True)
        assert prog1.calc_crc(False) != prog2.calc_crc(False)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
