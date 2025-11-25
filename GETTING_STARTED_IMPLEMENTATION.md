# Getting Started with Implementation
## Quick Start Guide for Phase 1

**Date**: November 25, 2025  
**Goal**: Begin implementing features discovered in C# code analysis  
**First Task**: Create bit utilities module

---

## Prerequisites

### 1. Review Key Documents
- ✅ Read `ORIGINAL_CSHARP_ANALYSIS.md` - Understand what we're building
- ✅ Read `IMPLEMENTATION_PLAN.md` - Understand the roadmap
- ✅ Review `IMPLEMENTATION_CHECKLIST.md` - Track progress

### 2. Set Up Development Environment
```bash
cd korg_pcg_tools
source venv/bin/activate  # or venv_tk/bin/activate
```

### 3. Get Test Files
You'll need PCG files from different OS versions:
- OS 1.0/1.1 (no color support)
- OS 1.5/1.6 (STL1/SBK1 format)
- OS 2.x (color support)
- OS 3.x (latest)

**Current Test Files**:
- `test_files/soundcheck9_25_25_combined2.PCG` - OS 3.x
- `SETLIST Movie TV Themes LOAD SEPARATELY.PCG` - OS 3.x

---

## Phase 1, Task 1: Bit Utilities Module

### Step 1: Create the Module

```bash
touch korg_pcg_tools/pcg_tools/bit_utils.py
```

### Step 2: Implement Core Functions

**File**: `korg_pcg_tools/pcg_tools/bit_utils.py`

```python
"""
Bit manipulation utilities for PCG file parsing.

Based on the original C# PCG Tools BitsUtil.cs implementation.
These utilities handle complex bit field operations needed for
setlist slot metadata (text size, transpose, etc.).
"""


def get_bits(data: bytes, byte_offset: int, high_bit: int, low_bit: int) -> int:
    """
    Extract bits from a byte range.
    
    Args:
        data: Byte array to read from
        byte_offset: Offset of the byte to read
        high_bit: Highest bit position (7 = MSB, 0 = LSB)
        low_bit: Lowest bit position (7 = MSB, 0 = LSB)
    
    Returns:
        Integer value of the extracted bits
    
    Example:
        # Get bits 7-5 from byte at offset 25
        value = get_bits(data, 25, 7, 5)
        # If byte is 0b11010000, returns 0b110 (6)
    """
    if byte_offset >= len(data):
        return 0
    
    byte_value = data[byte_offset]
    
    # Create mask for the bit range
    num_bits = high_bit - low_bit + 1
    mask = (1 << num_bits) - 1
    
    # Shift and mask
    return (byte_value >> low_bit) & mask


def set_bits(data: bytearray, byte_offset: int, high_bit: int, low_bit: int, value: int) -> None:
    """
    Set bits in a byte range.
    
    Args:
        data: Byte array to modify (must be bytearray, not bytes)
        byte_offset: Offset of the byte to modify
        high_bit: Highest bit position (7 = MSB, 0 = LSB)
        low_bit: Lowest bit position (7 = MSB, 0 = LSB)
        value: Value to set (will be masked to fit bit range)
    
    Example:
        # Set bits 7-5 of byte at offset 25 to value 6 (0b110)
        set_bits(data, 25, 7, 5, 6)
        # If byte was 0b00010000, becomes 0b11010000
    """
    if byte_offset >= len(data):
        return
    
    # Create mask for the bit range
    num_bits = high_bit - low_bit + 1
    mask = (1 << num_bits) - 1
    
    # Mask the value to fit in the bit range
    value = value & mask
    
    # Clear the bits in the byte
    clear_mask = ~(mask << low_bit) & 0xFF
    byte_value = data[byte_offset] & clear_mask
    
    # Set the new bits
    data[byte_offset] = byte_value | (value << low_bit)


def to_signed_bit(num_bits: int, value: int) -> int:
    """
    Convert unsigned bit value to signed integer.
    
    Args:
        num_bits: Number of bits in the value (e.g., 6 for 6-bit signed)
        value: Unsigned value to convert
    
    Returns:
        Signed integer value
    
    Example:
        # Convert 6-bit unsigned to signed
        # 0b111111 (63) -> -1
        # 0b100000 (32) -> -32
        # 0b011111 (31) -> 31
        signed = to_signed_bit(6, 63)  # Returns -1
    """
    sign_bit = 1 << (num_bits - 1)
    
    if value & sign_bit:
        # Negative number
        max_value = 1 << num_bits
        return value - max_value
    else:
        # Positive number
        return value


def from_signed_bit(num_bits: int, value: int) -> int:
    """
    Convert signed integer to unsigned bit value.
    
    Args:
        num_bits: Number of bits in the result (e.g., 6 for 6-bit signed)
        value: Signed value to convert
    
    Returns:
        Unsigned bit value
    
    Example:
        # Convert signed to 6-bit unsigned
        # -1 -> 0b111111 (63)
        # -32 -> 0b100000 (32)
        # 31 -> 0b011111 (31)
        unsigned = from_signed_bit(6, -1)  # Returns 63
    """
    if value < 0:
        max_value = 1 << num_bits
        return value + max_value
    else:
        return value


def get_bit(data: bytes, byte_offset: int, bit_position: int) -> bool:
    """
    Get a single bit value.
    
    Args:
        data: Byte array to read from
        byte_offset: Offset of the byte to read
        bit_position: Bit position (7 = MSB, 0 = LSB)
    
    Returns:
        True if bit is set, False otherwise
    """
    return get_bits(data, byte_offset, bit_position, bit_position) == 1


def set_bit(data: bytearray, byte_offset: int, bit_position: int, value: bool = True) -> None:
    """
    Set a single bit value.
    
    Args:
        data: Byte array to modify
        byte_offset: Offset of the byte to modify
        bit_position: Bit position (7 = MSB, 0 = LSB)
        value: True to set bit, False to clear bit
    """
    set_bits(data, byte_offset, bit_position, bit_position, 1 if value else 0)


def clear_bit(data: bytearray, byte_offset: int, bit_position: int) -> None:
    """
    Clear a single bit (set to 0).
    
    Args:
        data: Byte array to modify
        byte_offset: Offset of the byte to modify
        bit_position: Bit position (7 = MSB, 0 = LSB)
    """
    set_bit(data, byte_offset, bit_position, False)
```

### Step 3: Create Unit Tests

**File**: `korg_pcg_tools/test_bit_utils.py`

```python
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
            self.assertEqual(signed, value)
    
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


if __name__ == '__main__':
    unittest.main()
```

### Step 4: Run Tests

```bash
cd korg_pcg_tools
python -m pytest test_bit_utils.py -v
```

Or:

```bash
python test_bit_utils.py
```

### Step 5: Verify All Tests Pass

Expected output:
```
test_get_bits_full_byte (__main__.TestBitUtils) ... ok
test_get_bits_high_nibble (__main__.TestBitUtils) ... ok
test_get_bits_low_nibble (__main__.TestBitUtils) ... ok
test_get_bits_middle_bits (__main__.TestBitUtils) ... ok
test_set_bits_full_byte (__main__.TestBitUtils) ... ok
test_set_bits_high_nibble (__main__.TestBitUtils) ... ok
test_set_bits_low_nibble (__main__.TestBitUtils) ... ok
test_set_bits_preserves_other_bits (__main__.TestBitUtils) ... ok
test_to_signed_bit_positive (__main__.TestBitUtils) ... ok
test_to_signed_bit_negative (__main__.TestBitUtils) ... ok
test_from_signed_bit_positive (__main__.TestBitUtils) ... ok
test_from_signed_bit_negative (__main__.TestBitUtils) ... ok
test_signed_bit_round_trip (__main__.TestBitUtils) ... ok
test_get_bit (__main__.TestBitUtils) ... ok
test_set_bit (__main__.TestBitUtils) ... ok
test_clear_bit (__main__.TestBitUtils) ... ok

----------------------------------------------------------------------
Ran 16 tests in 0.001s

OK
```

---

## Next Steps

Once bit_utils.py is complete and tested:

1. ✅ Update `IMPLEMENTATION_CHECKLIST.md` - Mark Phase 1, Task 1 complete
2. ➡️ Move to Phase 1, Task 2 - OS Version Detection
3. 📝 Document any issues or learnings

---

## Tips for Success

### 1. Test-Driven Development
- Write tests first
- Run tests frequently
- Keep tests passing

### 2. Reference C# Code
- Original file: `/tmp/pcg-tools-original/Common/Utils/BitsUtil.cs`
- Compare behavior with C# implementation
- Use same test cases

### 3. Document as You Go
- Add docstrings to all functions
- Comment complex logic
- Update technical documentation

### 4. Commit Frequently
```bash
git add pcg_tools/bit_utils.py test_bit_utils.py
git commit -m "Add bit manipulation utilities module

- Implement get_bits/set_bits for bit field extraction
- Implement signed/unsigned bit conversion
- Add comprehensive unit tests
- All tests passing

Part of Phase 1 implementation plan."
```

---

## Common Issues & Solutions

### Issue 1: Byte vs Bytearray
**Problem**: `bytes` objects are immutable, `set_bits` needs mutable data

**Solution**: Use `bytearray` for data that will be modified
```python
# Wrong
data = bytes([0x00])
set_bits(data, 0, 7, 0, 0xFF)  # Error!

# Right
data = bytearray([0x00])
set_bits(data, 0, 7, 0, 0xFF)  # Works!
```

### Issue 2: Bit Numbering
**Problem**: Confusion about bit positions (MSB vs LSB)

**Solution**: Remember bit 7 is MSB (leftmost), bit 0 is LSB (rightmost)
```
Byte: 0b11010110
Bits:   76543210
```

### Issue 3: Sign Extension
**Problem**: Negative numbers in Python are infinite precision

**Solution**: Use `to_signed_bit` to properly handle fixed-width signed values

---

## Validation Checklist

Before moving to next task:

- [ ] All unit tests pass
- [ ] Code follows PEP 8
- [ ] All functions have docstrings
- [ ] Complex logic has comments
- [ ] No debug print statements
- [ ] Git commit created
- [ ] Checklist updated

---

## Questions?

If you encounter issues:

1. Review the C# code in `/tmp/pcg-tools-original/Common/Utils/BitsUtil.cs`
2. Check the analysis in `ORIGINAL_CSHARP_ANALYSIS.md`
3. Look at existing bit manipulation in `pcg_parser.py`
4. Test with known values from actual PCG files

---

**Ready to start?** Create `bit_utils.py` and begin coding! 🚀
