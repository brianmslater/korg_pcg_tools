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
