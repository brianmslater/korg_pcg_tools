"""Bank creation utilities for PCG files.

This module handles creating new user banks in existing PCG files.
Banks are stored as PBK1 (Program Bank) or MBK1 (Model Bank) chunks
within the PRG1 parent chunk.

Based on C# KronosProgramBanks.cs bank ID mappings:
- I-A = 0, I-B = 1, I-C = 2, I-D = 3, I-E = 4, I-F = 5
- GM = 6
- U-A = 17, U-B = 18, U-C = 19, U-D = 20, U-E = 21, U-F = 22, U-G = 23
- U-AA = 24, U-BB = 25, U-CC = 26, U-DD = 27, U-EE = 28, U-FF = 29, U-GG = 30
- Virtual banks start at 0x30 (48)
"""

import struct
from typing import Optional, Tuple
from .models import PcgFile, Bank, Program, Category


# Kronos program size (bytes per program)
KRONOS_PROGRAM_SIZE = 4960

# Bank ID encoding based on C# KronosProgramBanks.cs
# Internal banks: I-A=0 through I-F=5
# GM bank: 6
# User banks: U-A=17 through U-G=23
# Extended user banks: U-AA=24 through U-GG=30
# Virtual banks: 0x30 (48) and up

# Factory preset bank engine types based on Kronos factory content
# EXi banks use MBK1 chunks, HD-1 banks use PBK1 chunks
FACTORY_EXI_BANKS = {
    'I-A': 'SGX-1, EP-1 and best of all other EXi',
    'U-B': 'AL-1',
    'U-C': 'AL-1 and CX-3',
    'U-D': 'STR-1',
    'U-E': 'MS-20EX & PolysixEX',
    'U-F': 'MOD-7',
}

# HD-1 banks (use PBK1 chunks)
FACTORY_HD1_BANKS = {
    'I-B': 'HD-1',
    'I-C': 'HD-1',
    'I-D': 'HD-1',
    'I-E': 'HD-1',
    'I-F': 'HD-1',
    'U-A': 'HD-1 including Ambient Drums and Sound Effects',
    'U-G': 'Initialized HD-1 Programs',
    'GM': 'GM2 Main programs (HD-1)',
}


def encode_bank_id(bank_id: str) -> int:
    """Encode a bank ID string to raw integer value for PCG file.
    
    Based on C# KronosProgramBanks.cs bank ID mappings.
    
    Args:
        bank_id: Bank ID like 'I-A', 'U-A', 'U-GG', 'GM', 'V0-A'
    
    Returns:
        Raw bank ID integer for PCG file
    """
    # Internal banks: I-A=0 through I-F=5
    if bank_id.startswith('I-'):
        suffix = bank_id[2:]
        if len(suffix) == 1:
            idx = ord(suffix) - ord('A')
            if 0 <= idx <= 5:
                return idx
        raise ValueError(f"Invalid internal bank ID: {bank_id}")
    
    # GM bank
    if bank_id == 'GM':
        return 6
    
    # User banks: U-A=17 through U-G=23
    if bank_id.startswith('U-'):
        suffix = bank_id[2:]
        if len(suffix) == 1:
            idx = ord(suffix) - ord('A')
            if 0 <= idx <= 6:
                return 17 + idx
        # Extended user banks: U-AA=24 through U-GG=30
        elif len(suffix) == 2 and suffix[0] == suffix[1]:
            idx = ord(suffix[0]) - ord('A')
            if 0 <= idx <= 6:
                return 24 + idx
        raise ValueError(f"Invalid user bank ID: {bank_id}")
    
    # Virtual banks: V0-A through V7-H (0x30 + group*8 + bank)
    if bank_id.startswith('V'):
        # Format: V<group>-<letter> e.g., V0-A, V7-H
        parts = bank_id[1:].split('-')
        if len(parts) == 2:
            group = int(parts[0])
            letter = parts[1]
            if 0 <= group <= 7 and len(letter) == 1:
                bank_idx = ord(letter) - ord('A')
                if 0 <= bank_idx <= 7:
                    return 0x30 + group * 8 + bank_idx
        raise ValueError(f"Invalid virtual bank ID: {bank_id}")
    
    raise ValueError(f"Unknown bank ID format: {bank_id}")


def encode_user_bank_id(bank_id: str) -> int:
    """Encode a user bank ID string to raw integer value.
    
    Legacy function - use encode_bank_id() for all bank types.
    
    Args:
        bank_id: Bank ID like 'U-A', 'U-G', 'U-AA', 'U-GG'
    
    Returns:
        Raw bank ID integer for PCG file
    """
    return encode_bank_id(bank_id)


def decode_user_bank_id(raw_id: int) -> str:
    """Decode a raw bank ID to user bank string.
    
    Args:
        raw_id: Raw bank ID from PCG file
    
    Returns:
        Bank ID string like 'I-A', 'U-A', 'U-GG', 'GM', 'V0-A'
    """
    # Internal banks: 0-5
    if 0 <= raw_id <= 5:
        return f"I-{chr(ord('A') + raw_id)}"
    
    # GM bank: 6
    if raw_id == 6:
        return "GM"
    
    # User banks: 17-23
    if 17 <= raw_id <= 23:
        return f"U-{chr(ord('A') + raw_id - 17)}"
    
    # Extended user banks: 24-30
    if 24 <= raw_id <= 30:
        letter = chr(ord('A') + raw_id - 24)
        return f"U-{letter}{letter}"
    
    # Virtual banks: 0x30 (48) and up
    if raw_id >= 0x30:
        idx = raw_id - 0x30
        group = idx // 8
        bank = idx % 8
        if group <= 7 and bank <= 7:
            return f"V{group}-{chr(ord('A') + bank)}"
    
    return f"Unknown-{raw_id}"


def is_exi_bank(bank_id: str) -> bool:
    """Check if a bank is an EXi bank based on factory presets.
    
    Args:
        bank_id: Bank ID like 'I-A', 'U-B', etc.
    
    Returns:
        True if bank is EXi, False if HD-1
    """
    return bank_id in FACTORY_EXI_BANKS


def get_bank_engine_type(bank_id: str) -> str:
    """Get the default engine type for a bank based on factory presets.
    
    Args:
        bank_id: Bank ID like 'I-A', 'U-B', etc.
    
    Returns:
        'EXi' or 'HD-1'
    """
    return 'EXi' if is_exi_bank(bank_id) else 'HD-1'


def get_bank_description(bank_id: str) -> str:
    """Get the factory description for a bank.
    
    Args:
        bank_id: Bank ID like 'I-A', 'U-B', etc.
    
    Returns:
        Description string or empty string if not a factory bank
    """
    if bank_id in FACTORY_EXI_BANKS:
        return FACTORY_EXI_BANKS[bank_id]
    if bank_id in FACTORY_HD1_BANKS:
        return FACTORY_HD1_BANKS[bank_id]
    return ''


def create_empty_program(bank_id: str, index: int) -> Program:
    """Create an empty/initialized program.
    
    Uses the correct engine type based on factory preset designations.
    
    Args:
        bank_id: Bank ID for the program
        index: Program index (0-127)
    
    Returns:
        Initialized Program object
    """
    # Create raw data with initialized name
    raw_data = bytearray(KRONOS_PROGRAM_SIZE)
    
    # Set program name at offset 0 (24 bytes)
    name = f"Init Program {index:03d}"
    name_bytes = name.encode('ascii')[:24].ljust(24, b'\x00')
    raw_data[0:24] = name_bytes
    
    # Use correct engine type based on factory presets
    engine = get_bank_engine_type(bank_id)
    
    return Program(
        bank=bank_id,
        index=index,
        name=name,
        category=Category(0, 0),
        favorite=False,
        engine=engine,
        osc_mode="Single",
        raw_data=bytes(raw_data)
    )


def create_pbk1_chunk(bank_id: str, num_programs: int = 128) -> bytes:
    """Create a PBK1 (Program Bank) chunk for HD-1 programs.
    
    PBK1 structure:
    - 'PBK1' (4 bytes)
    - Chunk size (4 bytes, big-endian)
    - Gap/padding (4 bytes)
    - Number of programs (4 bytes, big-endian)
    - Program size (4 bytes, big-endian)
    - Bank ID (4 bytes, big-endian)
    - Program data (num_programs * program_size bytes)
    
    Args:
        bank_id: Bank ID (e.g., 'I-B', 'U-A', 'U-GG')
        num_programs: Number of programs (default 128)
    
    Returns:
        Complete PBK1 chunk as bytes
    """
    raw_bank_id = encode_bank_id(bank_id)
    program_size = KRONOS_PROGRAM_SIZE
    
    # Calculate chunk data size (excluding 'PBK1' and size field)
    # = gap(4) + num_progs(4) + prog_size(4) + bank_id(4) + programs
    chunk_data_size = 4 + 4 + 4 + 4 + (num_programs * program_size)
    
    # Build chunk
    chunk = bytearray()
    
    # Chunk ID
    chunk.extend(b'PBK1')
    
    # Chunk size (big-endian)
    chunk.extend(struct.pack('>I', chunk_data_size))
    
    # Gap/padding
    chunk.extend(b'\x00\x00\x00\x00')
    
    # Number of programs (big-endian)
    chunk.extend(struct.pack('>I', num_programs))
    
    # Program size (big-endian)
    chunk.extend(struct.pack('>I', program_size))
    
    # Bank ID (big-endian)
    chunk.extend(struct.pack('>I', raw_bank_id))
    
    # Program data (initialized)
    for i in range(num_programs):
        prog = create_empty_program(bank_id, i)
        chunk.extend(prog.raw_data)
    
    return bytes(chunk)


def create_mbk1_chunk(bank_id: str, num_programs: int = 128) -> bytes:
    """Create an MBK1 (Model Bank) chunk for EXi programs.
    
    MBK1 has the same structure as PBK1 but is used for EXi engine programs.
    
    Args:
        bank_id: Bank ID (e.g., 'I-A', 'U-B', 'U-C')
        num_programs: Number of programs (default 128)
    
    Returns:
        Complete MBK1 chunk as bytes
    """
    raw_bank_id = encode_bank_id(bank_id)
    program_size = KRONOS_PROGRAM_SIZE
    
    # Calculate chunk data size (excluding 'MBK1' and size field)
    chunk_data_size = 4 + 4 + 4 + 4 + (num_programs * program_size)
    
    # Build chunk
    chunk = bytearray()
    
    # Chunk ID - MBK1 for EXi banks
    chunk.extend(b'MBK1')
    
    # Chunk size (big-endian)
    chunk.extend(struct.pack('>I', chunk_data_size))
    
    # Gap/padding
    chunk.extend(b'\x00\x00\x00\x00')
    
    # Number of programs (big-endian)
    chunk.extend(struct.pack('>I', num_programs))
    
    # Program size (big-endian)
    chunk.extend(struct.pack('>I', program_size))
    
    # Bank ID (big-endian)
    chunk.extend(struct.pack('>I', raw_bank_id))
    
    # Program data (initialized with EXi engine type)
    for i in range(num_programs):
        prog = create_empty_program(bank_id, i)
        chunk.extend(prog.raw_data)
    
    return bytes(chunk)


def create_bank_chunk(bank_id: str, num_programs: int = 128) -> bytes:
    """Create the appropriate bank chunk (PBK1 or MBK1) based on bank type.
    
    Uses factory preset designations to determine if bank should be
    EXi (MBK1) or HD-1 (PBK1).
    
    Args:
        bank_id: Bank ID (e.g., 'I-A', 'U-B', 'U-GG')
        num_programs: Number of programs (default 128)
    
    Returns:
        Complete bank chunk as bytes (PBK1 or MBK1)
    """
    if is_exi_bank(bank_id):
        return create_mbk1_chunk(bank_id, num_programs)
    else:
        return create_pbk1_chunk(bank_id, num_programs)


def find_prg1_chunk(data: bytes) -> Optional[Tuple[int, int]]:
    """Find the PRG1 chunk in PCG data.
    
    Args:
        data: Raw PCG file data
    
    Returns:
        Tuple of (offset, size) or None if not found
    """
    offset = data.find(b'PRG1')
    if offset < 0:
        return None
    
    size = struct.unpack('>I', data[offset+4:offset+8])[0]
    return (offset, size)


def insert_bank_into_pcg(pcg: PcgFile, bank_id: str) -> bool:
    """Insert a new bank into a PCG file.
    
    This modifies the PCG's raw_data to include a new PBK1 or MBK1 chunk
    based on the bank's factory preset engine type.
    
    Args:
        pcg: PCG file object with raw_data
        bank_id: Bank ID to create (e.g., 'I-A', 'U-A', 'U-GG')
    
    Returns:
        True if successful, False otherwise
    """
    if not pcg.raw_data:
        return False
    
    # Check if bank already exists
    if pcg.has_program_bank(bank_id):
        return False  # Bank already exists
    
    # Find PRG1 chunk
    prg1_info = find_prg1_chunk(pcg.raw_data)
    if not prg1_info:
        return False
    
    prg1_offset, prg1_size = prg1_info
    
    # Create new bank chunk (PBK1 or MBK1 based on factory presets)
    new_chunk = create_bank_chunk(bank_id)
    new_chunk_size = len(new_chunk)
    
    # Calculate insertion point (end of PRG1 data, before next chunk)
    # PRG1 data ends at: prg1_offset + 8 + prg1_size
    insert_offset = prg1_offset + 8 + prg1_size
    
    # Build new raw_data
    raw_data = bytearray(pcg.raw_data)
    
    # Insert new chunk
    raw_data[insert_offset:insert_offset] = new_chunk
    
    # Update PRG1 chunk size
    new_prg1_size = prg1_size + new_chunk_size
    raw_data[prg1_offset+4:prg1_offset+8] = struct.pack('>I', new_prg1_size)
    
    # Update PCG raw_data
    pcg.raw_data = bytes(raw_data)
    
    # Create Bank object and add to pcg
    engine_type = get_bank_engine_type(bank_id)
    bank = Bank(bank_id=bank_id, bank_type='Program')
    for i in range(128):
        prog = create_empty_program(bank_id, i)
        prog._raw_offset = insert_offset + 24 + (i * KRONOS_PROGRAM_SIZE)
        bank.patches.append(prog)
    
    pcg.program_banks.append(bank)
    
    return True


def get_missing_banks(source_pcg: PcgFile, dest_pcg: PcgFile) -> list:
    """Get list of user banks in source that don't exist in destination.
    
    Args:
        source_pcg: Source PCG file
        dest_pcg: Destination PCG file
    
    Returns:
        List of bank IDs that exist in source but not in destination
    """
    source_banks = set(b.bank_id for b in source_pcg.program_banks if b.bank_id.startswith('U-'))
    dest_banks = set(b.bank_id for b in dest_pcg.program_banks if b.bank_id.startswith('U-'))
    
    return list(source_banks - dest_banks)
