"""PCG file checksum calculation and fixing.

Based on C# KronosPcgMemory.cs FixChecksumValues() and FindIni2Or3Offset().

Checksum locations:
- Chunk header: offset +11 (always)
- INI2/INI3 entry: offset +54 from entry start (for Kronos OS 1.5/1.6)

INI2 structure:
- Starts at chunk offset +16
- Each entry is 64 bytes
- Entry format: chunk name (4 bytes) at start, checksum at +54
- INI3 marker may appear between entries (skip 16 bytes when found)
"""

import struct
from typing import Optional, Tuple, List


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


def find_ini2_offset(data: bytes) -> Optional[int]:
    """Find the offset of the INI2 chunk.
    
    Based on C# KronosPcgMemory.cs: Chunks.Collection[1].Offset
    INI2 is typically the second chunk after DIV1.
    
    Args:
        data: Full PCG file data
    
    Returns:
        Offset of INI2 chunk, or None if not found
    """
    # DIV1 is at 0x1C for Kronos
    div1_offset = 0x1C
    
    if len(data) < div1_offset + 8:
        return None
    
    # Check for DIV1
    if data[div1_offset:div1_offset+4] != b'DIV1':
        return None
    
    # Get DIV1 size and calculate next chunk offset
    div1_size = struct.unpack('>I', data[div1_offset+4:div1_offset+8])[0]
    
    # Next chunk is at DIV1 offset + size + BetweenChunkGapSize (12)
    ini2_offset = div1_offset + div1_size + 12
    
    if len(data) < ini2_offset + 4:
        return None
    
    # Verify it's INI2
    if data[ini2_offset:ini2_offset+4] == b'INI2':
        return ini2_offset
    
    return None


def has_ini3_marker(data: bytes) -> bool:
    """Check if the file has INI3 marker (Kronos OS 1.5/1.6).
    
    Based on C# KronosPcgMemory.cs: ChecksumType.Kronos1516
    
    Args:
        data: Full PCG file data
    
    Returns:
        True if INI3 marker is present
    """
    return b'INI3' in data


def find_ini2_entry_offset(
    data: bytes, 
    chunk_name: str, 
    occurrence: int = 0
) -> Optional[int]:
    """Find the offset of a chunk's entry in INI2.
    
    Based on C# KronosPcgMemory.cs FindIni2Or3Offset().
    
    INI2 structure:
    - Entries start at INI2 offset + 16
    - Each entry is 64 bytes
    - Entry contains chunk name at start
    - INI3 marker may appear (skip 16 bytes)
    
    Args:
        data: Full PCG file data
        chunk_name: Name of chunk to find (e.g., 'PBK1', 'CBK1')
        occurrence: Which occurrence to find (0-based, for multiple banks)
    
    Returns:
        Offset of the entry in INI2, or None if not found
    """
    ini2_offset = find_ini2_offset(data)
    if ini2_offset is None:
        return None
    
    chunk_name_bytes = chunk_name.encode('ascii')
    
    # Start scanning at INI2 + 16
    offset = ini2_offset + 16
    found_count = 0
    
    # Scan through INI2 entries (64 bytes each)
    while offset < len(data) - 4:
        entry_name = data[offset:offset+4]
        
        # Check for INI3 marker
        if entry_name == b'INI3':
            # Skip INI3 header (16 bytes)
            offset += 16
            continue
        
        # Check if this is the chunk we're looking for
        if entry_name == chunk_name_bytes:
            if found_count == occurrence:
                return offset
            found_count += 1
        
        # Move to next entry (64 bytes)
        offset += 64
        
        # Safety check - don't scan too far
        if offset > ini2_offset + 0x10000:  # Max 64KB for INI2
            break
    
    return None


def fix_ini2_checksum(
    data: bytearray, 
    chunk_name: str, 
    occurrence: int, 
    checksum: int
) -> bool:
    """Write checksum to INI2 entry.
    
    Based on C# KronosPcgMemory.cs: Content[offsetInIni2 + 54] = (byte) checksum
    
    Args:
        data: Full PCG file data (will be modified in place)
        chunk_name: Name of chunk (e.g., 'PBK1', 'CBK1')
        occurrence: Which occurrence (0-based)
        checksum: Checksum value to write
    
    Returns:
        True if checksum was written successfully
    """
    entry_offset = find_ini2_entry_offset(data, chunk_name, occurrence)
    if entry_offset is None:
        return False
    
    # Checksum is at entry offset + 54
    checksum_offset = entry_offset + 54
    if checksum_offset >= len(data):
        return False
    
    data[checksum_offset] = checksum & 0xFF
    return True


def fix_all_checksums_with_ini2(data: bytearray) -> int:
    """Fix checksums for all chunks, including INI2 entries.
    
    This is the enhanced version that handles Kronos OS 1.5/1.6 files
    which store checksums in both the chunk header and INI2.
    
    Based on C# KronosPcgMemory.cs FixChecksumValues().
    
    Args:
        data: Full PCG file data (will be modified in place)
    
    Returns:
        Number of checksums fixed
    """
    # Check if this file has INI3 (Kronos OS 1.5/1.6)
    has_ini3 = has_ini3_marker(data)
    
    # Track bank indices for INI2 lookups
    pbk_index = 0
    mbk_index = 0
    cbk_index = 0
    wbk_index = 0
    dbk_index = 0
    
    # Chunks that need checksums
    checksum_chunks = {b'PBK1', b'MBK1', b'CBK1', b'SBK1', b'GLB1', b'WBK1', b'DBK1'}
    
    chunks_fixed = 0
    
    # Find all chunks and fix their checksums
    # Use the iterate approach from structure_validator
    offset = 0x1C  # DIV1 offset for Kronos
    gap_size = 12  # BetweenChunkGapSize for Kronos
    
    while offset < len(data) - 8:
        chunk_id = data[offset:offset+4]
        
        # Check if valid chunk ID
        if not all(32 <= b < 127 for b in chunk_id):
            break
        
        chunk_size = struct.unpack('>I', data[offset+4:offset+8])[0]
        
        # Check if this is a container chunk
        if chunk_id in {b'PRG1', b'CMB1', b'DKT1', b'WSQ1', b'SLS1'}:
            # Scan inside container
            sub_offset = offset + 12
            sub_end = offset + 12 + chunk_size
            
            while sub_offset < sub_end - 8:
                sub_id = data[sub_offset:sub_offset+4]
                
                if not all(32 <= b < 127 for b in sub_id):
                    break
                
                sub_size = struct.unpack('>I', data[sub_offset+4:sub_offset+8])[0]
                
                if sub_id in checksum_chunks:
                    # Calculate checksum
                    checksum = calculate_chunk_checksum(data, sub_offset, sub_size)
                    
                    # Write to chunk header
                    data[sub_offset + 11] = checksum
                    
                    # Write to INI2 if Kronos OS 1.5/1.6
                    if has_ini3:
                        chunk_name = sub_id.decode('ascii')
                        
                        # Determine occurrence index
                        if chunk_name == 'PBK1':
                            fix_ini2_checksum(data, chunk_name, pbk_index, checksum)
                            pbk_index += 1
                        elif chunk_name == 'MBK1':
                            fix_ini2_checksum(data, chunk_name, mbk_index, checksum)
                            mbk_index += 1
                        elif chunk_name == 'CBK1':
                            fix_ini2_checksum(data, chunk_name, cbk_index, checksum)
                            cbk_index += 1
                        elif chunk_name == 'SBK1':
                            fix_ini2_checksum(data, 'SLS1', 0, checksum)
                        elif chunk_name == 'WBK1':
                            fix_ini2_checksum(data, chunk_name, wbk_index, checksum)
                            wbk_index += 1
                        elif chunk_name == 'DBK1':
                            fix_ini2_checksum(data, chunk_name, dbk_index, checksum)
                            dbk_index += 1
                        # GLB1 not implemented in C# either
                    
                    chunks_fixed += 1
                
                # Handle nested STL1 inside SLS1
                if sub_id == b'STL1':
                    stl_sub_offset = sub_offset + 12
                    stl_sub_end = sub_offset + 12 + sub_size
                    
                    while stl_sub_offset < stl_sub_end - 8:
                        stl_sub_id = data[stl_sub_offset:stl_sub_offset+4]
                        
                        if not all(32 <= b < 127 for b in stl_sub_id):
                            break
                        
                        stl_sub_size = struct.unpack('>I', data[stl_sub_offset+4:stl_sub_offset+8])[0]
                        
                        if stl_sub_id in checksum_chunks:
                            checksum = calculate_chunk_checksum(data, stl_sub_offset, stl_sub_size)
                            data[stl_sub_offset + 11] = checksum
                            chunks_fixed += 1
                        
                        stl_sub_offset += 12 + stl_sub_size
                
                sub_offset += 12 + sub_size
        
        offset += chunk_size + gap_size
    
    return chunks_fixed


def get_ini2_checksums(data: bytes) -> List[Tuple[str, int, int, int]]:
    """Get all checksums stored in INI2.
    
    Args:
        data: Full PCG file data
    
    Returns:
        List of (chunk_name, occurrence, entry_offset, checksum) tuples
    """
    ini2_offset = find_ini2_offset(data)
    if ini2_offset is None:
        return []
    
    results = []
    chunk_counts = {}
    
    # Start scanning at INI2 + 16
    offset = ini2_offset + 16
    
    while offset < len(data) - 64:
        entry_name = data[offset:offset+4]
        
        # Check for INI3 marker
        if entry_name == b'INI3':
            offset += 16
            continue
        
        # Check if valid chunk name
        if not all(32 <= b < 127 for b in entry_name):
            break
        
        chunk_name = entry_name.decode('ascii', errors='replace')
        
        # Track occurrence
        occurrence = chunk_counts.get(chunk_name, 0)
        chunk_counts[chunk_name] = occurrence + 1
        
        # Get checksum at offset + 54
        checksum = data[offset + 54]
        
        results.append((chunk_name, occurrence, offset, checksum))
        
        offset += 64
        
        # Safety limit
        if len(results) > 100:
            break
    
    return results
