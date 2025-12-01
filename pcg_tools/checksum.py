"""PCG file checksum calculation and fixing."""

import struct


def calculate_chunk_checksum(data: bytes, chunk_offset: int, chunk_size: int) -> int:
    """Calculate checksum for a chunk.
    
    Args:
        data: Full PCG file data
        chunk_offset: Offset to chunk header (where chunk ID starts)
        chunk_size: Size of chunk data (from chunk header)
    
    Returns:
        Checksum value (0-255)
    """
    checksum = 0
    # Calculate from offset+12 (after header) to offset+12+size
    data_start = chunk_offset + 12
    data_end = chunk_offset + 12 + chunk_size
    
    for i in range(data_start, data_end):
        if i < len(data):
            checksum = (checksum + data[i]) % 256
    
    return checksum


def fix_chunk_checksum(data: bytearray, chunk_offset: int, chunk_size: int):
    """Calculate and write checksum for a chunk.
    
    The checksum is stored at byte 11 of the chunk header.
    
    Args:
        data: Full PCG file data (will be modified in place)
        chunk_offset: Offset to chunk header
        chunk_size: Size of chunk data
    """
    checksum = calculate_chunk_checksum(data, chunk_offset, chunk_size)
    data[chunk_offset + 11] = checksum


def fix_all_checksums(data: bytearray):
    """Fix checksums for all chunks in a PCG file.
    
    Chunks that need checksums: PBK1, MBK1, CBK1, SBK1, GLB1, WBK1, DBK1
    
    Args:
        data: Full PCG file data (will be modified in place)
    """
    # Chunks that need checksums
    checksum_chunks = {b'PBK1', b'MBK1', b'CBK1', b'SBK1', b'GLB1', b'WBK1', b'DBK1'}
    
    # Find PCG1 chunk
    pcg1_offset = data.find(b'PCG1')
    if pcg1_offset < 0:
        return
    
    pcg1_size = struct.unpack('>I', data[pcg1_offset+4:pcg1_offset+8])[0]  # Big-endian!
    pcg1_end = pcg1_offset + 12 + pcg1_size
    
    # Scan for top-level chunks within PCG1
    offset = pcg1_offset + 12
    chunks_fixed = 0
    
    while offset < pcg1_end - 12:
        chunk_id = bytes(data[offset:offset+4])
        
        # Read chunk size
        if offset + 8 > len(data):
            break
        
        try:
            chunk_size = struct.unpack('>I', data[offset+4:offset+8])[0]  # Big-endian!
        except:
            break
        
        # Check if this is a container chunk (PRG1, CMB1, STL1, etc.)
        if chunk_id in {b'PRG1', b'CMB1', b'DKT1', b'WSQ1', b'SLS1', b'STL1'}:
            # Scan inside container for checksum chunks
            sub_offset = offset + 12
            sub_end = offset + 12 + chunk_size
            
            while sub_offset < sub_end - 12:
                sub_id = bytes(data[sub_offset:sub_offset+4])
                if sub_id in checksum_chunks:
                    sub_size = struct.unpack('>I', data[sub_offset+4:sub_offset+8])[0]  # Big-endian!
                    fix_chunk_checksum(data, sub_offset, sub_size)
                    chunks_fixed += 1
                    sub_offset += 12 + sub_size
                elif sub_id == b'STL1':
                    # STL1 is a nested container inside SLS1, scan it too
                    sub_size = struct.unpack('>I', data[sub_offset+4:sub_offset+8])[0]
                    stl1_sub_offset = sub_offset + 12
                    stl1_sub_end = sub_offset + 12 + sub_size
                    
                    while stl1_sub_offset < stl1_sub_end - 12:
                        stl1_sub_id = bytes(data[stl1_sub_offset:stl1_sub_offset+4])
                        if stl1_sub_id in checksum_chunks:
                            stl1_sub_size = struct.unpack('>I', data[stl1_sub_offset+4:stl1_sub_offset+8])[0]
                            fix_chunk_checksum(data, stl1_sub_offset, stl1_sub_size)
                            chunks_fixed += 1
                            stl1_sub_offset += 12 + stl1_sub_size
                        else:
                            try:
                                stl1_sub_size = struct.unpack('>I', data[stl1_sub_offset+4:stl1_sub_offset+8])[0]
                                stl1_sub_offset += 12 + stl1_sub_size
                            except:
                                break
                    
                    sub_offset += 12 + sub_size
                else:
                    # Skip unknown chunk
                    try:
                        sub_size = struct.unpack('>I', data[sub_offset+4:sub_offset+8])[0]  # Big-endian!
                        sub_offset += 12 + sub_size
                    except:
                        break
        
        # Move to next top-level chunk
        offset += 12 + chunk_size
    
    # Silently fix checksums - no output needed


def verify_chunk_checksum(data: bytes, chunk_offset: int, chunk_size: int) -> bool:
    """Verify if a chunk's checksum is correct.
    
    Args:
        data: Full PCG file data
        chunk_offset: Offset to chunk header
        chunk_size: Size of chunk data
    
    Returns:
        True if checksum is correct
    """
    stored_checksum = data[chunk_offset + 11]
    calculated_checksum = calculate_chunk_checksum(data, chunk_offset, chunk_size)
    return stored_checksum == calculated_checksum
