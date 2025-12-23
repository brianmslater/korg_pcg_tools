"""PCG File Structure Reference Module.

This module defines all constants, offsets, and mappings for the Korg PCG binary
file format. It serves as the authoritative reference for parsing and writing
PCG files.

Based on:
- Original C# PCG Tools source code (KronosPcgMemory.cs, KronosProgram.cs, etc.)
- Official Korg documentation (PCG Structure Kronos.txt)
- Real PCG file analysis and hardware testing

References:
- C# KronosProgram.cs: Program parameter offsets
- C# KronosCombi.cs: Combi parameter offsets  
- C# KronosTimbres.cs: Timbre structure (TimbresOffsetConstant = 4802)
- C# KronosTimbre.cs: Timbre size (TimbresSizeConstant = 188)
- C# KronosSetListSlot.cs: Set list slot structure
"""

from enum import IntEnum
from typing import Dict, Optional, Tuple


# =============================================================================
# FILE HEADER CONSTANTS
# =============================================================================

class FileHeader:
    """PCG file header structure (16 bytes)."""
    MAGIC = b'KORG'
    MAGIC_OFFSET = 0x00
    MAGIC_SIZE = 4
    
    PRODUCT_ID_OFFSET = 0x04
    FILE_TYPE_OFFSET = 0x05
    MAJOR_VERSION_OFFSET = 0x06
    MINOR_VERSION_OFFSET = 0x07
    CHECKSUM_FLAG_OFFSET = 0x08
    RESERVED_OFFSET = 0x09
    RESERVED_SIZE = 7
    
    HEADER_SIZE = 16


class ProductId(IntEnum):
    """Korg synthesizer product IDs."""
    TRINITY = 0x3B
    TRITON = 0x50  # Sub-ID at 0x08: 0x00=Classic, 0x01=Extreme
    KARMA = 0x5D
    TRITON_LE = 0x63
    KRONOS = 0x68
    OASYS = 0x70
    M3 = 0x75
    M50 = 0x85
    MICROSTATION = 0x8D
    KROME = 0x95
    KROSS = 0x96
    KROSS_2 = 0xC9
    KROME_EX = 0xD2


class FileType(IntEnum):
    """PCG file types."""
    PCG = 0x00
    SNG = 0x01


# =============================================================================
# CHUNK CONSTANTS
# =============================================================================

class ChunkId:
    """Chunk identifier constants (4-byte ASCII)."""
    PCG1 = b'PCG1'  # Main container
    DIV1 = b'DIV1'  # Bank presence flags
    INI1 = b'INI1'  # Initialization chunk
    INI2 = b'INI2'  # Checksum chunk (OS 2.x/3.x)
    INI3 = b'INI3'  # Checksum chunk (OS 1.5/1.6)
    
    # Program chunks
    PRG1 = b'PRG1'  # Program container
    PBK1 = b'PBK1'  # HD-1 program bank
    MBK1 = b'MBK1'  # EXi program bank
    PRG2 = b'PRG2'  # Extended program data (OS 1.5+)
    
    # Combi chunks
    CMB1 = b'CMB1'  # Combi container
    CBK1 = b'CBK1'  # Combi bank
    CMB2 = b'CMB2'  # Extended combi data (OS 1.5+)
    
    # Set list chunks
    SLS1 = b'SLS1'  # Set list container
    SLD1 = b'SLD1'  # Set list display data
    SDB1 = b'SDB1'  # Set list browser names
    STL1 = b'STL1'  # Set list data container
    SBK1 = b'SBK1'  # Set list bank
    STL2 = b'STL2'  # Extended set list data (OS 1.5+)
    
    # Drum kit chunks
    DKT1 = b'DKT1'  # Drum kit container
    DBK1 = b'DBK1'  # Drum kit bank
    
    # Wave sequence chunks
    WSQ1 = b'WSQ1'  # Wave sequence container
    WBK1 = b'WBK1'  # Wave sequence bank
    
    # Other chunks
    GLB1 = b'GLB1'  # Global settings
    DPI1 = b'DPI1'  # Drum patterns


class ChunkStructure:
    """Common chunk structure offsets."""
    ID_OFFSET = 0
    ID_SIZE = 4
    SIZE_OFFSET = 4
    SIZE_SIZE = 4
    DATA_OFFSET = 8
    HEADER_SIZE = 8
    
    # Bank chunk structure (PBK1, MBK1, CBK1, DBK1, WBK1)
    BANK_NUM_ITEMS_OFFSET = 12
    BANK_ITEM_SIZE_OFFSET = 16
    BANK_ID_OFFSET = 20
    BANK_DATA_OFFSET = 24
    
    # Checksum byte offset within chunk header
    CHECKSUM_OFFSET = 11


# =============================================================================
# DIV1 BANK PRESENCE FLAGS
# =============================================================================

class Div1Offsets:
    """DIV1 chunk offsets for bank presence flags.
    
    Reference: PCG Structure Kronos.txt
    """
    # DIV1 location from PCG1 start (model-specific)
    KRONOS_OASYS_OFFSET = 0x1C
    TRITON_OFFSET = 0x18
    M3_KROME_KROSS_OFFSET = 0x1C
    
    # Offsets within DIV1 data
    PROG_BANKS_1 = 0x08  # 2 bytes: I-A through U-CC
    PROG_BANKS_2 = 0x0C  # 2 bytes: U-DD through U-GG
    PROG_BANK_COUNT = 0x0E  # 2 bytes
    
    COMBI_BANKS = 0x10  # 2 bytes
    COMBI_BANK_COUNT = 0x14  # 2 bytes
    
    DRUMKIT_BANKS = 0x18  # 2 bytes
    DRUMKIT_BANK_COUNT = 0x1C  # 2 bytes
    
    WAVESEQ_BANKS = 0x20  # 2 bytes
    WAVESEQ_BANK_COUNT = 0x24  # 2 bytes
    
    FLAGS = 0x28  # 4 bytes: DPI, SetLists, Reserved, Global


class Div1Flags:
    """DIV1 flag bit positions."""
    # Program bank flags (offset +8, 2 bytes)
    PROG_I_A = 0x0001
    PROG_I_B = 0x0002
    PROG_I_C = 0x0004
    PROG_I_D = 0x0008
    PROG_I_E = 0x0010
    PROG_I_F = 0x0020
    PROG_GM = 0x0040
    PROG_U_A = 0x0100
    PROG_U_B = 0x0200
    PROG_U_C = 0x0400
    PROG_U_D = 0x0800
    PROG_U_E = 0x1000
    PROG_U_F = 0x2000
    PROG_U_G = 0x4000
    PROG_U_AA = 0x8000
    
    # Extended program bank flags (offset +12, 2 bytes)
    PROG_U_BB = 0x0001
    PROG_U_CC = 0x0002
    PROG_U_DD = 0x0004
    PROG_U_EE = 0x0008
    PROG_U_FF = 0x0010
    PROG_U_GG = 0x0020


# =============================================================================
# KRONOS PROGRAM STRUCTURE
# =============================================================================

class KronosProgramOffsets:
    """Kronos program data structure offsets.
    
    Reference: C# KronosProgram.cs
    Typical program size: ~4200 bytes (HD-1) or ~4960 bytes
    
    Engine Type Detection:
    The engine type (HD-1 vs EXi) is determined by the OSC Mode parameter:
    - OSC Mode value 3 = "- (EXI)" indicates EXi engine
    - Other values (Single, Double, Drums, Double Drums) indicate HD-1 engine
    
    This matches the C# implementation in KronosProgram.cs and KronosProgramBank.cs
    where BankSynthesisType is set based on OSC Mode.
    """
    NAME = 0x0000  # 24 bytes, ASCII null-padded
    NAME_SIZE = 24
    
    # OSC mode and favorite (offset 2558, 2 bytes)
    # OSC Mode determines engine type: value 3 = EXi, others = HD-1
    OSC_MODE_OFFSET = 2558
    OSC_MODE_BITS = (0, 2)  # Bits 0-2: 0=Single, 1=Double, 2=Drums, 3=EXi, 4=Unused, 5=DoubleDrums
    FAVORITE_BIT = 5  # Bit 5 of byte 2558
    
    # Category (offset 2568, 1 byte)
    CATEGORY_OFFSET = 2568
    CATEGORY_BITS = (0, 4)  # Bits 0-4 (main category, 0-17)
    SUBCATEGORY_BITS = (5, 7)  # Bits 5-7 (sub-category, 0-7)


class OscMode(IntEnum):
    """Program oscillator modes."""
    SINGLE = 0
    DOUBLE = 1
    DRUMS = 2
    EXI = 3  # Not used for HD-1
    UNUSED = 4
    DOUBLE_DRUMS = 5


# =============================================================================
# KRONOS COMBI STRUCTURE
# =============================================================================

class KronosCombiOffsets:
    """Kronos combi data structure offsets.
    
    Reference: C# KronosCombi.cs
    Combi size: 7810 bytes (0x1E82)
    """
    NAME = 0x0000  # 24 bytes
    NAME_SIZE = 24
    
    TEMPO = 0x0518  # 2 bytes, little-endian, divide by 100 for BPM
    
    CATEGORY_OFFSET = 0x12B6  # 4790 decimal
    CATEGORY_BITS = (0, 4)  # Bits 0-4
    SUBCATEGORY_BITS = (5, 7)  # Bits 5-7
    
    FAVORITE_OFFSET = 0x12B7  # 4791 decimal
    FAVORITE_BIT = 0  # Bit 0
    
    # Timbre data
    TIMBRES_OFFSET = 0x12C2  # 4802 decimal (TimbresOffsetConstant)
    TIMBRES_COUNT = 16
    
    COMBI_SIZE = 7810  # 0x1E82


# =============================================================================
# KRONOS TIMBRE STRUCTURE
# =============================================================================

class KronosTimbreOffsets:
    """Kronos timbre data structure offsets (188 bytes per timbre).
    
    Reference: C# KronosTimbre.cs, KronosOasysTimbre.cs
    Timbre size: 188 bytes (TimbresSizeConstant)
    """
    TIMBRE_SIZE = 188
    
    PROGRAM_INDEX = 0  # 1 byte (0-127)
    PROGRAM_BANK = 1  # 1 byte (PcgId)
    
    # Status and MIDI channel (offset +2)
    STATUS_CHANNEL = 2
    STATUS_BITS = (5, 7)  # Bits 5-7: 0=Off, 1=Int, 2=Both, 3=Ext, 4=Ex2
    MIDI_CHANNEL_BITS = (0, 4)  # Bits 0-4
    
    VOLUME = 5  # 1 byte (0-127)
    BEND_RANGE = 6  # 1 byte, signed
    TRANSPOSE = 7  # 1 byte, signed (-24 to +24)
    DETUNE = 8  # 2 bytes, signed, little-endian
    
    # Mute and OSC flags (offsets +34, +35)
    MUTE_OFFSET = 34
    MUTE_BIT = 7  # Bit 7
    
    OSC_FLAGS_OFFSET = 35
    PRIORITY_BIT = 4  # Bit 4
    OSC_SELECT_BITS = (2, 3)  # Bits 2-3
    OSC_MODE_BITS = (0, 1)  # Bits 0-1
    
    PORTAMENTO = 36  # 1 byte, signed
    TOP_KEY = 37  # 1 byte (0-127)
    BOTTOM_KEY = 38  # 1 byte (0-127)
    TOP_VELOCITY = 40  # 1 byte (1-127)
    BOTTOM_VELOCITY = 41  # 1 byte (1-127)


class TimbreStatus(IntEnum):
    """Timbre status values."""
    OFF = 0
    INT = 1
    BOTH = 2
    EXT = 3
    EX2 = 4


class TimbreOscMode(IntEnum):
    """Timbre oscillator mode values."""
    PRG = 0  # Use program setting
    POLY = 1
    MONO = 2
    LEGATO = 3


class TimbreOscSelect(IntEnum):
    """Timbre oscillator select values."""
    BOTH = 0
    OSC1 = 1
    OSC2 = 2


# =============================================================================
# KRONOS SET LIST SLOT STRUCTURE
# =============================================================================

class KronosSetListSlotOffsets:
    """Kronos set list slot data structure offsets.
    
    Reference: C# KronosSetListSlot.cs
    Slot size: 542 bytes (calculated from SBK1 total_size / num_setlists / 128)
    """
    NAME = 0  # 24 bytes
    NAME_SIZE = 24
    
    # Type and color (offset +24)
    TYPE_COLOR = 24
    PATCH_TYPE_BITS = (0, 1)  # Bits 0-1: 0=Program, 1=Combi, 2=Song
    TEXT_SIZE_LSB_BITS = (6, 7)  # Bits 6-7
    COLOR_BITS = (2, 5)  # Bits 2-5 (color index)
    
    # Bank and transpose MSB (offset +25)
    BANK_TRANSPOSE = 25
    BANK_ID_BITS = (0, 4)  # Bits 0-4
    TRANSPOSE_MSB_BITS = (5, 7)  # Bits 5-7
    
    PATCH_INDEX = 26  # 1 byte (0-127)
    RESERVED = 27  # 1 byte
    VOLUME = 28  # 1 byte (0-127)
    
    # Transpose LSB and text size MSB (offset +29)
    TRANSPOSE_TEXT = 29
    TRANSPOSE_LSB_BITS = (5, 7)  # Bits 5-7
    TEXT_SIZE_MSB_BIT = 4  # Bit 4
    
    DESCRIPTION = 30  # 512 bytes
    DESCRIPTION_SIZE = 512
    
    SLOT_SIZE = 542


class PatchType(IntEnum):
    """Set list slot patch types."""
    PROGRAM = 0
    COMBI = 1
    SONG = 2


class TextSize(IntEnum):
    """Set list slot text sizes."""
    S = 0
    XS = 1
    M = 2
    L = 3
    XL = 4


# =============================================================================
# GLOBAL SETTINGS STRUCTURE
# =============================================================================

class KronosGlobalOffsets:
    """Kronos global settings (GLB1) offsets.
    
    Reference: C# KronosOasysGlobal.cs
    """
    # Category names start at offset 12912 from GLB1 data
    CATEGORIES_OFFSET = 12912
    
    NUM_CATEGORIES = 18
    NUM_SUBCATEGORIES = 8
    CATEGORY_NAME_SIZE = 24
    
    # Total size: 18 × 8 × 24 = 3456 bytes per type (program/combi)


# =============================================================================
# CHECKSUM CONSTANTS
# =============================================================================

class ChecksumConstants:
    """Checksum calculation constants.
    
    Reference: C# KronosPcgMemory.cs, KrossPcgMemory.cs
    """
    # Chunks requiring checksums
    CHECKSUM_CHUNKS = {b'PBK1', b'MBK1', b'CBK1', b'SBK1', b'GLB1', b'WBK1', b'DBK1'}
    
    # INI2 entry size
    INI2_ENTRY_SIZE = 64
    INI2_HEADER_SIZE = 16
    
    # Checksum storage offsets
    CHUNK_CHECKSUM_OFFSET = 11  # Within chunk header
    INI2_CHECKSUM_OFFSET_KROSS = 22  # For Kross, Krome, etc.
    INI2_CHECKSUM_OFFSET_KRONOS_15 = 54  # For Kronos OS 1.5/1.6


# =============================================================================
# BANK ID MAPPINGS
# =============================================================================

# Program bank IDs in chunk headers
PROGRAM_BANK_CHUNK_IDS: Dict[str, int] = {
    'I-A': 0x00000,
    'I-B': 0x00001,
    'I-C': 0x00002,
    'I-D': 0x00003,
    'I-E': 0x00004,
    'I-F': 0x08000,  # Special case
    'GM': 0x00006,
    'U-A': 0x20000,
    'U-B': 0x20001,
    'U-C': 0x20002,
    'U-D': 0x20003,
    'U-E': 0x20004,
    'U-F': 0x20005,
    'U-G': 0x20006,
    'U-AA': 0x20007,
    'U-BB': 0x20008,
    'U-CC': 0x20009,
    'U-DD': 0x2000A,
    'U-EE': 0x2000B,
    'U-FF': 0x2000C,
    'U-GG': 0x2000D,
}

# Reverse mapping for chunk headers
CHUNK_ID_TO_PROGRAM_BANK: Dict[int, str] = {v: k for k, v in PROGRAM_BANK_CHUNK_IDS.items()}

# Timbre bank PcgIds (different from chunk headers!)
TIMBRE_BANK_PCGIDS: Dict[str, int] = {
    'I-A': 0,
    'I-B': 1,
    'I-C': 2,
    'I-D': 3,
    'I-E': 4,
    'I-F': 5,
    'GM': 6,
    'U-A': 17,
    'U-B': 18,
    'U-C': 19,
    'U-D': 20,
    'U-E': 21,
    'U-F': 22,
    'U-G': 23,
    'U-AA': 24,
    'U-BB': 25,
    'U-CC': 26,
    'U-DD': 27,
    'U-EE': 28,
    'U-FF': 29,
    'U-GG': 30,
}

# Reverse mapping for timbre PcgIds
PCGID_TO_TIMBRE_BANK: Dict[int, str] = {v: k for k, v in TIMBRE_BANK_PCGIDS.items()}

# Set list slot bank IDs (5-bit values)
SLOT_BANK_IDS: Dict[str, int] = {
    'I-A': 0,
    'I-B': 1,
    'I-C': 2,
    'I-D': 3,
    'I-E': 4,
    'I-F': 5,
    'I-G': 6,
    'I-H': 7,
    'GM': 14,
    'U-A': 23,
    'U-B': 24,
    'U-C': 25,
    'U-D': 26,
    'U-E': 27,
    'U-F': 28,
    'U-G': 29,
    'U-AA': 30,
    'U-BB': 31,
    # Extended banks use different encoding
}

# Reverse mapping for slot bank IDs
SLOT_ID_TO_BANK: Dict[int, str] = {v: k for k, v in SLOT_BANK_IDS.items()}

# Combi bank IDs in chunk headers
COMBI_BANK_CHUNK_IDS: Dict[str, int] = {
    'I-A': 0x00000,
    'I-B': 0x00001,
    'I-C': 0x00002,
    'I-D': 0x00003,
    'I-E': 0x00004,
    'I-F': 0x00005,
    'I-G': 0x00006,
    'U-A': 0x20000,
    'U-B': 0x20001,
    'U-C': 0x20002,
    'U-D': 0x20003,
    'U-E': 0x20004,
    'U-F': 0x20005,
    'U-G': 0x20006,
}

# Reverse mapping for combi chunk headers
CHUNK_ID_TO_COMBI_BANK: Dict[int, str] = {v: k for k, v in COMBI_BANK_CHUNK_IDS.items()}


# =============================================================================
# COLOR MAPPINGS
# =============================================================================

# Kronos set list slot colors
SLOT_COLORS: Dict[int, str] = {
    0: 'Default',
    136: 'Brick',
    137: 'Brick',
    140: 'Burgundy',
    144: 'Ivy',
    148: 'Olive',
    152: 'Gold',
    153: 'Gold',
    156: 'Cacao',
    157: 'Cacao',
    160: 'Indigo',
    164: 'Navy',
    165: 'Navy',
    168: 'Rose',
    172: 'Lavender',
    173: 'Lavender',
    174: 'Lavender',
    176: 'Azure',
    180: 'Denim',
    181: 'Denim',
    184: 'Silver',
    188: 'Slate',
    196: 'Charcoal',
}

# Color index to value mapping (for encoding)
COLOR_INDEX_TO_VALUE: Dict[int, int] = {
    0: 0,      # Default
    1: 136,    # Brick
    2: 140,    # Burgundy
    3: 144,    # Ivy
    4: 148,    # Olive
    5: 152,    # Gold
    6: 156,    # Cacao
    7: 160,    # Indigo
    8: 164,    # Navy
    9: 168,    # Rose
    10: 172,   # Lavender
    11: 176,   # Azure
    12: 180,   # Denim
    13: 184,   # Silver
    14: 188,   # Slate
    15: 196,   # Charcoal
}


# =============================================================================
# BANK ID MAPPING FUNCTIONS
# =============================================================================

def bank_name_to_pcgid(bank_name: str, context: str = 'chunk') -> int:
    """Convert bank name to PcgId value.
    
    Args:
        bank_name: Bank name like 'I-A', 'U-G', 'GM', etc.
        context: 'chunk' for chunk headers, 'timbre' for timbre references,
                 'slot' for set list slot references, 'combi' for combi banks
    
    Returns:
        Integer PcgId value
    
    Examples:
        >>> bank_name_to_pcgid('I-A', 'chunk')
        0
        >>> bank_name_to_pcgid('I-F', 'chunk')
        32768  # 0x8000
        >>> bank_name_to_pcgid('U-A', 'timbre')
        17
        >>> bank_name_to_pcgid('U-A', 'slot')
        23
    
    Raises:
        ValueError: If bank_name is not recognized for the given context
    """
    bank_name = bank_name.upper().strip()
    
    if context == 'chunk':
        if bank_name in PROGRAM_BANK_CHUNK_IDS:
            return PROGRAM_BANK_CHUNK_IDS[bank_name]
        raise ValueError(f"Unknown program bank name for chunk context: {bank_name}")
    
    elif context == 'combi':
        if bank_name in COMBI_BANK_CHUNK_IDS:
            return COMBI_BANK_CHUNK_IDS[bank_name]
        raise ValueError(f"Unknown combi bank name: {bank_name}")
    
    elif context == 'timbre':
        if bank_name in TIMBRE_BANK_PCGIDS:
            return TIMBRE_BANK_PCGIDS[bank_name]
        raise ValueError(f"Unknown bank name for timbre context: {bank_name}")
    
    elif context == 'slot':
        if bank_name in SLOT_BANK_IDS:
            return SLOT_BANK_IDS[bank_name]
        raise ValueError(f"Unknown bank name for slot context: {bank_name}")
    
    else:
        raise ValueError(f"Unknown context: {context}")


def pcgid_to_bank_name(pcgid: int, context: str = 'chunk', is_combi: bool = False) -> str:
    """Convert PcgId value to bank name.
    
    Args:
        pcgid: Integer PcgId value
        context: 'chunk' for chunk headers, 'timbre' for timbre references,
                 'slot' for set list slot references
        is_combi: If True and context='chunk', use combi bank mapping
    
    Returns:
        Bank name string like 'I-A', 'U-G', 'GM', etc.
    
    Examples:
        >>> pcgid_to_bank_name(0, 'chunk')
        'I-A'
        >>> pcgid_to_bank_name(0x8000, 'chunk')
        'I-F'
        >>> pcgid_to_bank_name(17, 'timbre')
        'U-A'
        >>> pcgid_to_bank_name(23, 'slot')
        'U-A'
    
    Raises:
        ValueError: If pcgid is not recognized for the given context
    """
    if context == 'chunk':
        if is_combi:
            if pcgid in CHUNK_ID_TO_COMBI_BANK:
                return CHUNK_ID_TO_COMBI_BANK[pcgid]
            # Handle user banks with high bit
            bank_type = (pcgid >> 16) & 0xFFFF
            sub_index = pcgid & 0xFFFF
            if bank_type == 0 and sub_index < 7:
                return f"I-{chr(65 + sub_index)}"
            elif bank_type == 2 and sub_index < 7:
                return f"U-{chr(65 + sub_index)}"
        else:
            if pcgid in CHUNK_ID_TO_PROGRAM_BANK:
                return CHUNK_ID_TO_PROGRAM_BANK[pcgid]
            # Handle special cases
            if pcgid == 0x8000:
                return 'I-F'
            if pcgid >= 0x20000:
                user_idx = pcgid - 0x20000
                if user_idx < 7:
                    return f"U-{chr(65 + user_idx)}"
                elif user_idx < 14:
                    letter = chr(65 + (user_idx - 7))
                    return f"U-{letter}{letter}"
        raise ValueError(f"Unknown PcgId for chunk context: 0x{pcgid:08X}")
    
    elif context == 'timbre':
        if pcgid in PCGID_TO_TIMBRE_BANK:
            return PCGID_TO_TIMBRE_BANK[pcgid]
        raise ValueError(f"Unknown PcgId for timbre context: {pcgid}")
    
    elif context == 'slot':
        if pcgid in SLOT_ID_TO_BANK:
            return SLOT_ID_TO_BANK[pcgid]
        # Handle extended user banks
        if pcgid >= 23:
            user_idx = pcgid - 23
            if user_idx < 7:
                return f"U-{chr(65 + user_idx)}"
            elif user_idx < 14:
                letter = chr(65 + (user_idx - 7))
                return f"U-{letter}{letter}"
        raise ValueError(f"Unknown PcgId for slot context: {pcgid}")
    
    else:
        raise ValueError(f"Unknown context: {context}")


def slot_bank_id_to_name(bank_id: int, is_combi: bool = False) -> str:
    """Convert set list slot bank ID (5-bit value) to bank name.
    
    This is a convenience wrapper for pcgid_to_bank_name with slot context.
    
    The slot bank ID mapping is:
    - 0-6: I-A through I-G (Internal program/combi banks)
    - 7-13: U-A through U-G (User banks)
    - 14: GM
    - 15-23: g(1) through g(9) (EXi banks) - rarely used in slots
    - 24: g(d) (EXi drums)
    - 25-31: U-AA through U-GG (Extended user banks)
    
    Note: The SLOT_BANK_IDS mapping uses a different scheme where U-A=23.
    This function handles the actual binary format from STL1/SBK1.
    
    Args:
        bank_id: 5-bit bank ID from slot data (0-31)
        is_combi: True if this is a combi bank reference
    
    Returns:
        Bank name string like 'I-A', 'U-A', etc.
    
    Examples:
        >>> slot_bank_id_to_name(0)
        'I-A'
        >>> slot_bank_id_to_name(7)
        'U-A'
        >>> slot_bank_id_to_name(14)
        'GM'
        >>> slot_bank_id_to_name(23)
        'U-A'  # When using SLOT_BANK_IDS mapping
    """
    # First check if it's in our defined mapping (reverse lookup)
    if bank_id in SLOT_ID_TO_BANK:
        return SLOT_ID_TO_BANK[bank_id]
    
    # Internal banks: 0-6 = I-A through I-G
    if bank_id <= 6:
        return f"I-{chr(65 + bank_id)}"
    
    # User banks: 7-13 = U-A through U-G (alternative encoding)
    if 7 <= bank_id <= 13:
        return f"U-{chr(65 + (bank_id - 7))}"
    
    # GM bank
    if bank_id == 14:
        return 'GM'
    
    # EXi banks: 15-22 = g(1) through g(8)
    if 15 <= bank_id <= 22:
        return f"g({bank_id - 14})"
    
    # User banks with SLOT_BANK_IDS encoding: 23-29 = U-A through U-G
    if 23 <= bank_id <= 29:
        return f"U-{chr(65 + (bank_id - 23))}"
    
    # Extended user banks: 30-36 = U-AA through U-GG
    if 30 <= bank_id <= 36:
        letter = chr(65 + (bank_id - 30))
        return f"U-{letter}{letter}"
    
    return f"?-{bank_id}"


def get_div1_offset(product_id: int) -> int:
    """Get DIV1 chunk offset from PCG1 start based on product ID.
    
    Args:
        product_id: Product ID byte from file header
    
    Returns:
        Offset to DIV1 chunk from PCG1 start
    """
    if product_id == ProductId.TRITON:
        return Div1Offsets.TRITON_OFFSET
    else:
        # Kronos, Oasys, M3, Krome, Kross all use 0x1C
        return Div1Offsets.KRONOS_OASYS_OFFSET


def calculate_timbre_offset(combi_offset: int, timbre_index: int) -> int:
    """Calculate the byte offset for a specific timbre within a combi.
    
    Args:
        combi_offset: Byte offset to the start of the combi data
        timbre_index: Timbre index (0-15)
    
    Returns:
        Byte offset to the timbre data
    
    Example:
        >>> calculate_timbre_offset(0x10CAA64, 0)
        17853282  # 0x10CAA64 + 4802 + 0
    """
    return combi_offset + KronosCombiOffsets.TIMBRES_OFFSET + (timbre_index * KronosTimbreOffsets.TIMBRE_SIZE)


def calculate_category_offset(glb1_data_offset: int, category_type: str, 
                              main_cat: int, sub_cat: int) -> int:
    """Calculate the byte offset for a category name in GLB1.
    
    Args:
        glb1_data_offset: Byte offset to GLB1 chunk data start
        category_type: 'program' or 'combi'
        main_cat: Main category index (0-17)
        sub_cat: Sub-category index (0-7)
    
    Returns:
        Byte offset to the category name (24 bytes)
    """
    base = glb1_data_offset + KronosGlobalOffsets.CATEGORIES_OFFSET
    
    if category_type == 'combi':
        # Skip program categories
        base += (KronosGlobalOffsets.NUM_CATEGORIES * 
                 KronosGlobalOffsets.NUM_SUBCATEGORIES * 
                 KronosGlobalOffsets.CATEGORY_NAME_SIZE)
    
    return base + (main_cat * KronosGlobalOffsets.NUM_SUBCATEGORIES * 
                   KronosGlobalOffsets.CATEGORY_NAME_SIZE) + (sub_cat * KronosGlobalOffsets.CATEGORY_NAME_SIZE)


def decode_slot_transpose(byte_25: int, byte_29: int) -> int:
    """Decode set list slot transpose from split bit fields.
    
    Transpose is stored as a 6-bit unsigned value split across two bytes:
    - MSB (3 bits): byte 25, bits 5-7
    - LSB (3 bits): byte 29, bits 5-7
    
    Args:
        byte_25: Byte at offset +25 from slot name
        byte_29: Byte at offset +29 from slot name
    
    Returns:
        Signed transpose value (-24 to +24)
    """
    msb = (byte_25 >> 5) & 0x07
    lsb = (byte_29 >> 5) & 0x07
    unsigned = (msb << 3) | lsb
    
    # Convert 6-bit unsigned to signed
    if unsigned >= 32:
        return unsigned - 64
    return unsigned


def encode_slot_transpose(transpose: int) -> Tuple[int, int]:
    """Encode set list slot transpose to split bit fields.
    
    Args:
        transpose: Signed transpose value (-24 to +24)
    
    Returns:
        Tuple of (msb_bits, lsb_bits) to OR into bytes 25 and 29
    """
    # Convert signed to 6-bit unsigned
    if transpose < 0:
        unsigned = transpose + 64
    else:
        unsigned = transpose
    
    msb = (unsigned >> 3) & 0x07
    lsb = unsigned & 0x07
    
    return (msb << 5, lsb << 5)


def decode_slot_text_size(byte_24: int, byte_29: int) -> int:
    """Decode set list slot text size from split bit fields.
    
    Text size is stored as a 3-bit value split across two bytes:
    - MSB (1 bit): byte 29, bit 4
    - LSB (2 bits): byte 24, bits 6-7
    
    Args:
        byte_24: Byte at offset +24 from slot name
        byte_29: Byte at offset +29 from slot name
    
    Returns:
        Text size value (0-4: S, XS, M, L, XL)
    """
    msb = (byte_29 >> 4) & 0x01
    lsb = (byte_24 >> 6) & 0x03
    return (msb << 2) | lsb


def encode_slot_text_size(text_size: int) -> Tuple[int, int]:
    """Encode set list slot text size to split bit fields.
    
    Args:
        text_size: Text size value (0-4)
    
    Returns:
        Tuple of (byte_24_bits, byte_29_bits) to OR into the bytes
    """
    msb = (text_size >> 2) & 0x01
    lsb = text_size & 0x03
    
    return (lsb << 6, msb << 4)



# =============================================================================
# DIV1 PARSING FUNCTIONS
# =============================================================================

from dataclasses import dataclass, field
from typing import List, Set
import struct


@dataclass
class Div1Info:
    """Parsed DIV1 chunk information.
    
    Contains bank presence flags and counts for all bank types.
    """
    # Program banks
    prog_banks_1: int = 0  # Flags for I-A through U-AA
    prog_banks_2: int = 0  # Flags for U-BB through U-GG
    prog_bank_count: int = 0
    
    # Combi banks
    combi_banks: int = 0
    combi_bank_count: int = 0
    
    # Drum kit banks
    drumkit_banks: int = 0
    drumkit_bank_count: int = 0
    
    # Wave sequence banks
    waveseq_banks: int = 0
    waveseq_bank_count: int = 0
    
    # Other flags
    has_dpi: bool = False
    has_setlists: bool = False
    has_global: bool = False
    
    def get_present_program_banks(self) -> Set[str]:
        """Get set of present program bank names.
        
        Returns:
            Set of bank names like {'I-A', 'U-A', 'U-B'}
        """
        banks = set()
        
        # Check prog_banks_1 flags
        flag_map_1 = [
            (Div1Flags.PROG_I_A, 'I-A'),
            (Div1Flags.PROG_I_B, 'I-B'),
            (Div1Flags.PROG_I_C, 'I-C'),
            (Div1Flags.PROG_I_D, 'I-D'),
            (Div1Flags.PROG_I_E, 'I-E'),
            (Div1Flags.PROG_I_F, 'I-F'),
            (Div1Flags.PROG_GM, 'GM'),
            (Div1Flags.PROG_U_A, 'U-A'),
            (Div1Flags.PROG_U_B, 'U-B'),
            (Div1Flags.PROG_U_C, 'U-C'),
            (Div1Flags.PROG_U_D, 'U-D'),
            (Div1Flags.PROG_U_E, 'U-E'),
            (Div1Flags.PROG_U_F, 'U-F'),
            (Div1Flags.PROG_U_G, 'U-G'),
            (Div1Flags.PROG_U_AA, 'U-AA'),
        ]
        
        for flag, name in flag_map_1:
            if self.prog_banks_1 & flag:
                banks.add(name)
        
        # Check prog_banks_2 flags
        flag_map_2 = [
            (Div1Flags.PROG_U_BB, 'U-BB'),
            (Div1Flags.PROG_U_CC, 'U-CC'),
            (Div1Flags.PROG_U_DD, 'U-DD'),
            (Div1Flags.PROG_U_EE, 'U-EE'),
            (Div1Flags.PROG_U_FF, 'U-FF'),
            (Div1Flags.PROG_U_GG, 'U-GG'),
        ]
        
        for flag, name in flag_map_2:
            if self.prog_banks_2 & flag:
                banks.add(name)
        
        return banks
    
    def get_present_combi_banks(self) -> Set[str]:
        """Get set of present combi bank names.
        
        Returns:
            Set of bank names like {'I-A', 'U-A'}
        """
        banks = set()
        
        # Combi bank flags follow similar pattern
        # Bits 0-6: I-A through I-G
        # Bits 8-14: U-A through U-G
        for i in range(7):
            if self.combi_banks & (1 << i):
                banks.add(f'I-{chr(65 + i)}')  # I-A through I-G
        
        for i in range(7):
            if self.combi_banks & (1 << (8 + i)):
                banks.add(f'U-{chr(65 + i)}')  # U-A through U-G
        
        return banks
    
    def is_program_bank_present(self, bank_name: str) -> bool:
        """Check if a program bank is present.
        
        Args:
            bank_name: Bank name like 'I-A', 'U-B', 'GM'
        
        Returns:
            True if bank is present
        """
        return bank_name in self.get_present_program_banks()
    
    def is_combi_bank_present(self, bank_name: str) -> bool:
        """Check if a combi bank is present.
        
        Args:
            bank_name: Bank name like 'I-A', 'U-B'
        
        Returns:
            True if bank is present
        """
        return bank_name in self.get_present_combi_banks()


def parse_div1_chunk(data: bytes, div1_offset: int = None) -> Optional[Div1Info]:
    """Parse DIV1 chunk to extract bank presence flags.
    
    Based on C# PcgFileReader and PCG Structure documentation.
    
    Args:
        data: Full PCG file data
        div1_offset: Offset to DIV1 chunk (default: 0x1C for Kronos)
    
    Returns:
        Div1Info with parsed flags, or None if DIV1 not found
    """
    if div1_offset is None:
        div1_offset = Div1Offsets.KRONOS_OASYS_OFFSET
    
    # Verify DIV1 chunk
    if len(data) < div1_offset + 44:  # DIV1 is typically 44 bytes
        return None
    
    if data[div1_offset:div1_offset+4] != ChunkId.DIV1:
        return None
    
    # Parse DIV1 data (offsets are from chunk start, not data start)
    info = Div1Info()
    
    # Program banks (offset +8 from chunk start = +0 from data)
    # Note: DIV1 data starts at chunk_offset + 8 (after ID and size)
    data_start = div1_offset + 8
    
    # Read program bank flags
    info.prog_banks_1 = struct.unpack('>H', data[data_start:data_start+2])[0]
    info.prog_banks_2 = struct.unpack('>H', data[data_start+4:data_start+6])[0]
    info.prog_bank_count = struct.unpack('>H', data[data_start+6:data_start+8])[0]
    
    # Read combi bank flags
    info.combi_banks = struct.unpack('>H', data[data_start+8:data_start+10])[0]
    info.combi_bank_count = struct.unpack('>H', data[data_start+12:data_start+14])[0]
    
    # Read drum kit bank flags
    info.drumkit_banks = struct.unpack('>H', data[data_start+16:data_start+18])[0]
    info.drumkit_bank_count = struct.unpack('>H', data[data_start+20:data_start+22])[0]
    
    # Read wave sequence bank flags
    info.waveseq_banks = struct.unpack('>H', data[data_start+24:data_start+26])[0]
    info.waveseq_bank_count = struct.unpack('>H', data[data_start+28:data_start+30])[0]
    
    # Read other flags (offset +32 from data start)
    if data_start + 35 < len(data):
        info.has_dpi = data[data_start + 32] != 0
        info.has_setlists = data[data_start + 33] != 0
        info.has_global = data[data_start + 35] != 0
    
    return info


def get_div1_offset_for_model(product_id: int) -> int:
    """Get DIV1 offset for a specific model.
    
    Args:
        product_id: Product ID from file header
    
    Returns:
        DIV1 offset from PCG1 start
    """
    if product_id == ProductId.TRITON:
        return Div1Offsets.TRITON_OFFSET
    else:
        # Kronos, Oasys, M3, Krome, Kross all use 0x1C
        return Div1Offsets.KRONOS_OASYS_OFFSET


def validate_div1_against_chunks(
    data: bytes, 
    div1_info: Div1Info,
    chunks: List[Tuple[bytes, int, int]]
) -> List[str]:
    """Validate DIV1 flags against actual chunks present.
    
    Args:
        data: Full PCG file data
        div1_info: Parsed DIV1 information
        chunks: List of (chunk_id, offset, size) tuples
    
    Returns:
        List of inconsistency messages (empty if consistent)
    """
    issues = []
    
    # Find actual bank chunks
    actual_prog_banks = set()
    actual_combi_banks = set()
    
    for chunk_id, offset, size in chunks:
        if chunk_id == ChunkId.PBK1 or chunk_id == ChunkId.MBK1:
            # Read bank ID from chunk
            if offset + 24 < len(data):
                bank_id = struct.unpack('>I', data[offset+20:offset+24])[0]
                bank_name = pcgid_to_bank_name(bank_id, 'chunk')
                if bank_name:
                    actual_prog_banks.add(bank_name)
        
        elif chunk_id == ChunkId.CBK1:
            if offset + 24 < len(data):
                bank_id = struct.unpack('>I', data[offset+20:offset+24])[0]
                bank_name = pcgid_to_bank_name(bank_id, 'combi_chunk')
                if bank_name:
                    actual_combi_banks.add(bank_name)
    
    # Compare with DIV1 flags
    div1_prog_banks = div1_info.get_present_program_banks()
    div1_combi_banks = div1_info.get_present_combi_banks()
    
    # Check for banks in DIV1 but not in chunks
    for bank in div1_prog_banks - actual_prog_banks:
        issues.append(f"DIV1 indicates program bank {bank} present, but no chunk found")
    
    # Check for banks in chunks but not in DIV1
    for bank in actual_prog_banks - div1_prog_banks:
        issues.append(f"Program bank {bank} chunk found, but DIV1 flag not set")
    
    # Same for combi banks
    for bank in div1_combi_banks - actual_combi_banks:
        issues.append(f"DIV1 indicates combi bank {bank} present, but no chunk found")
    
    for bank in actual_combi_banks - div1_combi_banks:
        issues.append(f"Combi bank {bank} chunk found, but DIV1 flag not set")
    
    return issues



# =============================================================================
# DRUM KIT PARSING FUNCTIONS
# =============================================================================

@dataclass
class DrumKitBankInfo:
    """Parsed drum kit bank information."""
    bank_id: int
    bank_name: str
    num_drum_kits: int
    drum_kit_size: int
    byte_offset: int
    drum_kits: List[Tuple[str, int]] = field(default_factory=list)  # (name, offset)


def drumkit_bank_id_to_index(bank_id: int) -> int:
    """Convert drum kit bank ID to index.
    
    Based on C# PcgFileReader.DrumKitBankId2DrumKitIndex():
    - 0 (INT) -> 0
    - 0x20000 (USER-A) -> 1
    - 0x20001 (USER-B) -> 2
    - etc.
    
    Args:
        bank_id: Bank ID from DBK1 chunk
    
    Returns:
        Bank index
    """
    return bank_id if bank_id < 0x20000 else bank_id - 0x20000 + 1


def drumkit_bank_id_to_name(bank_id: int) -> str:
    """Convert drum kit bank ID to name.
    
    Args:
        bank_id: Bank ID from DBK1 chunk
    
    Returns:
        Bank name like 'INT' or 'USER-A'
    """
    if bank_id == 0:
        return 'INT'
    elif bank_id >= 0x20000:
        user_idx = bank_id - 0x20000
        if user_idx < 7:
            return f'USER-{chr(65 + user_idx)}'
        elif user_idx < 14:
            letter = chr(65 + (user_idx - 7))
            return f'USER-{letter}{letter}'
    return f'UNKNOWN-{bank_id:X}'


def parse_dkt1_chunk(data: bytes, dkt1_offset: int) -> List[DrumKitBankInfo]:
    """Parse DKT1 (drum kit container) chunk.
    
    Based on C# PcgFileReader.ReadDkt1Chunk().
    
    Args:
        data: Full PCG file data
        dkt1_offset: Offset to DKT1 chunk
    
    Returns:
        List of DrumKitBankInfo for each DBK1 found
    """
    if len(data) < dkt1_offset + 8:
        return []
    
    # Verify DKT1 chunk
    if data[dkt1_offset:dkt1_offset+4] != ChunkId.DKT1:
        return []
    
    chunk_size = struct.unpack('>I', data[dkt1_offset+4:dkt1_offset+8])[0]
    
    banks = []
    
    # Scan for DBK1 chunks inside DKT1
    # DKT1 data starts at offset + 12 (after header + gap)
    offset = dkt1_offset + 12
    end_offset = dkt1_offset + 12 + chunk_size
    
    while offset < end_offset - 8:
        sub_id = data[offset:offset+4]
        
        if sub_id != ChunkId.DBK1:
            break
        
        bank_info = parse_dbk1_chunk(data, offset)
        if bank_info:
            banks.append(bank_info)
            # Move to next chunk
            sub_size = struct.unpack('>I', data[offset+4:offset+8])[0]
            offset += 12 + sub_size
        else:
            break
    
    return banks


def parse_dbk1_chunk(data: bytes, dbk1_offset: int) -> Optional[DrumKitBankInfo]:
    """Parse DBK1 (drum kit bank) chunk.
    
    Based on C# PcgFileReader.ReadDbk1Chunk().
    
    DBK1 structure (Kronos/Oasys):
    - +0: 'DBK1' (4 bytes)
    - +4: chunk size (4 bytes)
    - +8: header (4 bytes)
    - +12: num_drum_kits (4 bytes)
    - +16: drum_kit_size (4 bytes)
    - +20: bank_id (4 bytes)
    - +24: drum kit data starts
    
    Args:
        data: Full PCG file data
        dbk1_offset: Offset to DBK1 chunk
    
    Returns:
        DrumKitBankInfo or None if invalid
    """
    if len(data) < dbk1_offset + 24:
        return None
    
    # Verify DBK1 chunk
    if data[dbk1_offset:dbk1_offset+4] != ChunkId.DBK1:
        return None
    
    chunk_size = struct.unpack('>I', data[dbk1_offset+4:dbk1_offset+8])[0]
    
    # Read bank info (Kronos uses offset 12 for num_drum_kits)
    num_drum_kits = struct.unpack('>I', data[dbk1_offset+12:dbk1_offset+16])[0]
    drum_kit_size = struct.unpack('>I', data[dbk1_offset+16:dbk1_offset+20])[0]
    bank_id = struct.unpack('>I', data[dbk1_offset+20:dbk1_offset+24])[0]
    
    bank_name = drumkit_bank_id_to_name(bank_id)
    
    # Parse drum kit names
    drum_kits = []
    kit_offset = dbk1_offset + 24
    
    for i in range(num_drum_kits):
        if kit_offset + 24 > len(data):
            break
        
        # Drum kit name is at the start of each drum kit (24 bytes)
        name_bytes = data[kit_offset:kit_offset+24]
        name = name_bytes.split(b'\x00')[0].decode('ascii', errors='replace').strip()
        
        drum_kits.append((name, kit_offset))
        kit_offset += drum_kit_size
    
    return DrumKitBankInfo(
        bank_id=bank_id,
        bank_name=bank_name,
        num_drum_kits=num_drum_kits,
        drum_kit_size=drum_kit_size,
        byte_offset=dbk1_offset,
        drum_kits=drum_kits
    )



# =============================================================================
# WAVE SEQUENCE PARSING FUNCTIONS
# =============================================================================

@dataclass
class WaveSequenceBankInfo:
    """Parsed wave sequence bank information."""
    bank_id: int
    bank_name: str
    num_wave_seqs: int
    wave_seq_size: int
    byte_offset: int
    wave_sequences: List[Tuple[str, int]] = field(default_factory=list)  # (name, offset)


def waveseq_bank_id_to_index(bank_id: int) -> int:
    """Convert wave sequence bank ID to index.
    
    Based on C# PcgFileReader.WaveSequenceBankId2WaveSequenceIndex():
    - 0 (INT) -> 0
    - 0x20000 (USER-A) -> 1
    - 0x20001 (USER-B) -> 2
    - etc.
    
    Args:
        bank_id: Bank ID from WBK1 chunk
    
    Returns:
        Bank index
    """
    return bank_id if bank_id < 0x20000 else bank_id - 0x20000 + 1


def waveseq_bank_id_to_name(bank_id: int) -> str:
    """Convert wave sequence bank ID to name.
    
    Args:
        bank_id: Bank ID from WBK1 chunk
    
    Returns:
        Bank name like 'INT' or 'USER-A'
    """
    if bank_id == 0:
        return 'INT'
    elif bank_id >= 0x20000:
        user_idx = bank_id - 0x20000
        if user_idx < 7:
            return f'USER-{chr(65 + user_idx)}'
        elif user_idx < 14:
            letter = chr(65 + (user_idx - 7))
            return f'USER-{letter}{letter}'
    return f'UNKNOWN-{bank_id:X}'


def parse_wsq1_chunk(data: bytes, wsq1_offset: int) -> List[WaveSequenceBankInfo]:
    """Parse WSQ1 (wave sequence container) chunk.
    
    Based on C# PcgFileReader.ReadWsq1Chunk().
    
    Args:
        data: Full PCG file data
        wsq1_offset: Offset to WSQ1 chunk
    
    Returns:
        List of WaveSequenceBankInfo for each WBK1 found
    """
    if len(data) < wsq1_offset + 8:
        return []
    
    # Verify WSQ1 chunk
    if data[wsq1_offset:wsq1_offset+4] != ChunkId.WSQ1:
        return []
    
    chunk_size = struct.unpack('>I', data[wsq1_offset+4:wsq1_offset+8])[0]
    
    banks = []
    
    # Scan for WBK1 chunks inside WSQ1
    # WSQ1 data starts at offset + 12 (after header + gap)
    offset = wsq1_offset + 12
    end_offset = wsq1_offset + 12 + chunk_size
    
    while offset < end_offset - 8:
        sub_id = data[offset:offset+4]
        
        if sub_id != ChunkId.WBK1:
            break
        
        bank_info = parse_wbk1_chunk(data, offset)
        if bank_info:
            banks.append(bank_info)
            # Move to next chunk
            sub_size = struct.unpack('>I', data[offset+4:offset+8])[0]
            offset += 12 + sub_size
        else:
            break
    
    return banks


def parse_wbk1_chunk(data: bytes, wbk1_offset: int) -> Optional[WaveSequenceBankInfo]:
    """Parse WBK1 (wave sequence bank) chunk.
    
    Based on C# PcgFileReader.ReadWbk1Chunk().
    
    WBK1 structure:
    - +0: 'WBK1' (4 bytes)
    - +4: chunk size (4 bytes)
    - +8: header (4 bytes)
    - +12: num_wave_seqs (4 bytes)
    - +16: wave_seq_size (4 bytes)
    - +20: bank_id (4 bytes)
    - +24: wave sequence data starts
    
    Args:
        data: Full PCG file data
        wbk1_offset: Offset to WBK1 chunk
    
    Returns:
        WaveSequenceBankInfo or None if invalid
    """
    if len(data) < wbk1_offset + 24:
        return None
    
    # Verify WBK1 chunk
    if data[wbk1_offset:wbk1_offset+4] != ChunkId.WBK1:
        return None
    
    chunk_size = struct.unpack('>I', data[wbk1_offset+4:wbk1_offset+8])[0]
    
    # Read bank info
    num_wave_seqs = struct.unpack('>I', data[wbk1_offset+12:wbk1_offset+16])[0]
    wave_seq_size = struct.unpack('>I', data[wbk1_offset+16:wbk1_offset+20])[0]
    bank_id = struct.unpack('>I', data[wbk1_offset+20:wbk1_offset+24])[0]
    
    bank_name = waveseq_bank_id_to_name(bank_id)
    
    # Parse wave sequence names
    wave_sequences = []
    seq_offset = wbk1_offset + 24
    
    for i in range(num_wave_seqs):
        if seq_offset + 24 > len(data):
            break
        
        # Wave sequence name is at the start of each wave sequence (24 bytes)
        name_bytes = data[seq_offset:seq_offset+24]
        name = name_bytes.split(b'\x00')[0].decode('ascii', errors='replace').strip()
        
        wave_sequences.append((name, seq_offset))
        seq_offset += wave_seq_size
    
    return WaveSequenceBankInfo(
        bank_id=bank_id,
        bank_name=bank_name,
        num_wave_seqs=num_wave_seqs,
        wave_seq_size=wave_seq_size,
        byte_offset=wbk1_offset,
        wave_sequences=wave_sequences
    )



# =============================================================================
# GLB1 CATEGORY PARSING FUNCTIONS
# =============================================================================

# Category constants for Kronos/Oasys
KRONOS_CATEGORY_OFFSET = 12912  # Offset from GLB1 data start to categories
KRONOS_CATEGORY_NAME_LENGTH = 24
KRONOS_NUM_CATEGORIES = 18
KRONOS_NUM_SUBCATEGORIES = 8


@dataclass
class CategoryInfo:
    """Category name information."""
    index: int
    name: str
    subcategories: List[str] = field(default_factory=list)


@dataclass
class GlobalCategoryInfo:
    """Parsed global category information."""
    program_categories: List[CategoryInfo] = field(default_factory=list)
    combi_categories: List[CategoryInfo] = field(default_factory=list)
    glb1_offset: int = 0


def parse_glb1_categories(
    data: bytes,
    glb1_offset: int,
    category_offset: int = KRONOS_CATEGORY_OFFSET,
    category_name_length: int = KRONOS_CATEGORY_NAME_LENGTH,
    num_categories: int = KRONOS_NUM_CATEGORIES,
    num_subcategories: int = KRONOS_NUM_SUBCATEGORIES
) -> Optional[GlobalCategoryInfo]:
    """Parse category names from GLB1 chunk.
    
    Based on C# Global.cs CalcCategoryNameOffset() and CalcSubCategoryNameOffset().
    
    Category structure (Kronos/Oasys):
    - 18 main categories × 24 bytes = 432 bytes for program categories
    - 18 × 8 subcategories × 24 bytes = 3456 bytes for program subcategories
    - Same structure repeated for combi categories
    
    Args:
        data: Full PCG file data
        glb1_offset: Offset to GLB1 chunk
        category_offset: Offset from GLB1 data to categories (12912 for Kronos)
        category_name_length: Length of each category name (24 for Kronos)
        num_categories: Number of main categories (18 for Kronos)
        num_subcategories: Number of subcategories per category (8 for Kronos)
    
    Returns:
        GlobalCategoryInfo or None if invalid
    """
    if len(data) < glb1_offset + 8:
        return None
    
    # Verify GLB1 chunk
    if data[glb1_offset:glb1_offset+4] != ChunkId.GLB1:
        return None
    
    chunk_size = struct.unpack('>I', data[glb1_offset+4:glb1_offset+8])[0]
    
    # GLB1 data starts at offset + 12 (after header + 4 unknown bytes)
    glb1_data_start = glb1_offset + 12
    
    # Calculate category data start
    cat_start = glb1_data_start + category_offset
    
    # Size of one category type (main + subcategories)
    subcategories_size = num_subcategories * category_name_length
    size_per_category_type = num_categories * (category_name_length + subcategories_size)
    
    result = GlobalCategoryInfo(glb1_offset=glb1_offset)
    
    # Parse program categories
    offset = cat_start
    for i in range(num_categories):
        if offset + category_name_length > len(data):
            break
        
        # Read main category name
        name_bytes = data[offset:offset + category_name_length]
        name = name_bytes.split(b'\x00')[0].decode('ascii', errors='replace').strip()
        
        cat_info = CategoryInfo(index=i, name=name)
        offset += category_name_length
        result.program_categories.append(cat_info)
    
    # Parse program subcategories
    for i, cat_info in enumerate(result.program_categories):
        for j in range(num_subcategories):
            if offset + category_name_length > len(data):
                break
            
            name_bytes = data[offset:offset + category_name_length]
            name = name_bytes.split(b'\x00')[0].decode('ascii', errors='replace').strip()
            cat_info.subcategories.append(name)
            offset += category_name_length
    
    # Parse combi categories (same structure, after program categories)
    combi_cat_start = cat_start + size_per_category_type
    offset = combi_cat_start
    
    for i in range(num_categories):
        if offset + category_name_length > len(data):
            break
        
        name_bytes = data[offset:offset + category_name_length]
        name = name_bytes.split(b'\x00')[0].decode('ascii', errors='replace').strip()
        
        cat_info = CategoryInfo(index=i, name=name)
        offset += category_name_length
        result.combi_categories.append(cat_info)
    
    # Parse combi subcategories
    for i, cat_info in enumerate(result.combi_categories):
        for j in range(num_subcategories):
            if offset + category_name_length > len(data):
                break
            
            name_bytes = data[offset:offset + category_name_length]
            name = name_bytes.split(b'\x00')[0].decode('ascii', errors='replace').strip()
            cat_info.subcategories.append(name)
            offset += category_name_length
    
    return result


def get_category_name(
    categories: GlobalCategoryInfo,
    category_type: str,
    main_index: int,
    sub_index: int = -1
) -> str:
    """Get category name by index.
    
    Args:
        categories: Parsed category info
        category_type: 'Program' or 'Combi'
        main_index: Main category index (0-17)
        sub_index: Subcategory index (0-7), or -1 for main category only
    
    Returns:
        Category name string
    """
    cat_list = (categories.program_categories if category_type == 'Program'
                else categories.combi_categories)
    
    if main_index < 0 or main_index >= len(cat_list):
        return f"Category {main_index}"
    
    cat_info = cat_list[main_index]
    
    if sub_index < 0:
        return cat_info.name
    
    if sub_index >= len(cat_info.subcategories):
        return f"{cat_info.name}/{sub_index}"
    
    return f"{cat_info.name}/{cat_info.subcategories[sub_index]}"



# =============================================================================
# EXTENDED DATA CHUNKS (PRG2/CMB2/STL2) - Kronos OS 1.5+
# =============================================================================

@dataclass
class ExtendedDataInfo:
    """Information about extended data chunks (PRG2/CMB2/STL2).
    
    These chunks are present in Kronos OS 1.5+ files and contain additional
    parameters not stored in the main PBK1/CBK1/SBK1 chunks.
    
    Based on C# KronosProgramBank.cs, KronosCombiBank.cs, KronosSetListSlot.cs.
    """
    # OS version detection
    has_ini3: bool = False  # INI3 presence indicates OS 1.5/1.6
    os_version: str = ""  # "1.5/1.6", "2.x/3.x", or ""
    
    # PRG2 chunk info
    has_prg2: bool = False
    prg2_offset: int = 0
    prg2_size: int = 0
    pbk2_offsets: Dict[str, int] = field(default_factory=dict)  # bank_name -> offset
    
    # CMB2 chunk info
    has_cmb2: bool = False
    cmb2_offset: int = 0
    cmb2_size: int = 0
    cbk2_offsets: Dict[str, int] = field(default_factory=dict)  # bank_name -> offset
    
    # STL2 chunk info
    has_stl2: bool = False
    stl2_offset: int = 0
    stl2_size: int = 0
    stl2_pcg_offset: int = 0  # Offset to actual slot data (after SBK2 header)


class ExtendedDataConstants:
    """Constants for extended data chunks.
    
    Based on C# KronosProgram.cs, KronosCombi.cs, KronosSetListSlot.cs.
    """
    # Gap between PRG2/CMB2/STL2 and their sub-chunks
    SIZE_BETWEEN_PRG2_AND_PBK2 = 8  # KronosProgram.SizeBetweenPrg2AndPbk2
    SIZE_BETWEEN_CMB2_AND_CBK2 = 8  # KronosCombi.SizeBetweenCmb2AndCbk2
    SIZE_BETWEEN_STL2_AND_SBK2 = 8  # KronosSetListSlot.SizeBetweenStl2AndSbk2
    
    # Parameters per chunk
    PARAMETERS_IN_PBK2 = 66  # KronosProgramBanks.ParametersInPbk2Chunk
    PARAMETERS_IN_CBK2 = 2   # KronosCombiBanks.ParametersInCbk2Chunk (Bank, Program)
    
    # Number of programs/combis per bank
    PROGRAMS_PER_BANK = 128
    COMBIS_PER_BANK = 128
    TIMBRES_PER_COMBI = 16
    
    # Set list constants
    NUM_SETLISTS = 128
    SLOTS_PER_SETLIST = 128


def detect_kronos_os_version(data: bytes) -> str:
    """Detect Kronos OS version from PCG file data.
    
    Based on C# PcgFileReader.cs - INI3 presence indicates OS 1.5/1.6.
    
    Args:
        data: Full PCG file data
    
    Returns:
        OS version string: "1.5/1.6", "2.x/3.x", or "" if not Kronos
    """
    # Check if this is a Kronos file
    if len(data) < 16:
        return ""
    
    if data[0:4] != b'KORG':
        return ""
    
    product_id = data[4]
    if product_id != ProductId.KRONOS:
        return ""
    
    # Search for INI3 chunk
    offset = 0x1C  # Start after file header + PCG1 header
    gap_size = 12  # Kronos gap size
    
    while offset < len(data) - 8:
        chunk_id = data[offset:offset+4]
        
        if not all(32 <= b < 127 for b in chunk_id):
            break
        
        if chunk_id == ChunkId.INI3:
            return "1.5/1.6"
        
        chunk_size = struct.unpack('>I', data[offset+4:offset+8])[0]
        offset += chunk_size + gap_size
    
    return "2.x/3.x"


def find_extended_data_chunks(data: bytes) -> ExtendedDataInfo:
    """Find and parse extended data chunks (PRG2/CMB2/STL2).
    
    Based on C# PcgFileReader.cs ReadPrg2Chunk(), ReadCmb2Chunk(), ReadStl2Chunk().
    
    Args:
        data: Full PCG file data
    
    Returns:
        ExtendedDataInfo with chunk locations and offsets
    """
    info = ExtendedDataInfo()
    
    # Detect OS version
    info.os_version = detect_kronos_os_version(data)
    info.has_ini3 = info.os_version == "1.5/1.6"
    
    if not info.os_version:
        return info  # Not a Kronos file
    
    # Scan for extended data chunks
    offset = 0x1C  # Start after file header + PCG1 header
    gap_size = 12  # Kronos gap size
    
    while offset < len(data) - 8:
        chunk_id = data[offset:offset+4]
        
        if not all(32 <= b < 127 for b in chunk_id):
            break
        
        chunk_size = struct.unpack('>I', data[offset+4:offset+8])[0]
        
        if chunk_id == ChunkId.PRG2:
            info.has_prg2 = True
            info.prg2_offset = offset
            info.prg2_size = chunk_size
            _parse_prg2_banks(data, offset, chunk_size, info)
        
        elif chunk_id == ChunkId.CMB2:
            info.has_cmb2 = True
            info.cmb2_offset = offset
            info.cmb2_size = chunk_size
            _parse_cmb2_banks(data, offset, chunk_size, info)
        
        elif chunk_id == ChunkId.STL2:
            info.has_stl2 = True
            info.stl2_offset = offset
            info.stl2_size = chunk_size
            # STL2 data offset: chunk_offset + gap + 16 (SBK2 header)
            info.stl2_pcg_offset = offset + ExtendedDataConstants.SIZE_BETWEEN_STL2_AND_SBK2 + 4 + 16
        
        offset += chunk_size + gap_size
    
    return info


def _parse_prg2_banks(data: bytes, prg2_offset: int, chunk_size: int, info: ExtendedDataInfo):
    """Parse PBK2 sub-chunks within PRG2.
    
    Based on C# PcgFileReader.cs ReadPrg2Chunk().
    
    Args:
        data: Full PCG file data
        prg2_offset: Offset to PRG2 chunk
        chunk_size: PRG2 chunk size
        info: ExtendedDataInfo to populate
    """
    # Skip PRG2 header + gap
    offset = prg2_offset + ExtendedDataConstants.SIZE_BETWEEN_PRG2_AND_PBK2 + 4
    start = offset
    bank_index = 0
    
    # Bank names in order (matching C# writable banks order)
    bank_names = ['U-A', 'U-B', 'U-C', 'U-D', 'U-E', 'U-F', 'U-G',
                  'U-AA', 'U-BB', 'U-CC', 'U-DD', 'U-EE', 'U-FF', 'U-GG']
    
    while offset - start < chunk_size and bank_index < len(bank_names):
        if offset + 8 > len(data):
            break
        
        sub_id = data[offset:offset+4]
        if sub_id != b'PBK2':
            break
        
        sub_size = struct.unpack('>I', data[offset+4:offset+8])[0]
        
        # Store PBK2 offset (data starts at offset + 16: chunk header + 8 zeros)
        if bank_index < len(bank_names):
            info.pbk2_offsets[bank_names[bank_index]] = offset + 16
        
        bank_index += 1
        offset += sub_size + 12  # chunk size + gap
    
    return info


def _parse_cmb2_banks(data: bytes, cmb2_offset: int, chunk_size: int, info: ExtendedDataInfo):
    """Parse CBK2 sub-chunks within CMB2.
    
    Based on C# PcgFileReader.cs ReadCmb2Chunk().
    
    Args:
        data: Full PCG file data
        cmb2_offset: Offset to CMB2 chunk
        chunk_size: CMB2 chunk size
        info: ExtendedDataInfo to populate
    """
    # Skip CMB2 header + gap
    offset = cmb2_offset + ExtendedDataConstants.SIZE_BETWEEN_CMB2_AND_CBK2 + 4
    start = offset
    bank_index = 0
    
    # Bank names in order (matching C# writable banks order)
    bank_names = ['U-A', 'U-B', 'U-C', 'U-D', 'U-E', 'U-F', 'U-G']
    
    while offset - start < chunk_size and bank_index < len(bank_names):
        if offset + 8 > len(data):
            break
        
        sub_id = data[offset:offset+4]
        if sub_id != b'CBK2':
            break
        
        sub_size = struct.unpack('>I', data[offset+4:offset+8])[0]
        
        # Store CBK2 offset (data starts at offset + 16: chunk header + 8 zeros)
        if bank_index < len(bank_names):
            info.cbk2_offsets[bank_names[bank_index]] = offset + 16
        
        bank_index += 1
        offset += sub_size + 12  # chunk size + gap
    
    return info


def get_pbk2_parameter_offset(
    pbk2_offset: int,
    program_index: int,
    parameter_index: int,
    programs_per_bank: int = 128
) -> int:
    """Calculate offset to a specific parameter in PBK2 chunk.
    
    Based on C# KronosProgramBank.cs GetParameterOffsetInPbk2().
    
    PBK2 parameter layout:
    - Parameters 0-31: for each program, 32 bytes
    - Parameters 32-63: for each program, 32 bytes
    - Parameter 64: for each program, 1 byte
    - Parameter 65: for each program, 1 byte
    
    Args:
        pbk2_offset: Offset to PBK2 data start
        program_index: Program index (0-127)
        parameter_index: Parameter index (0-65)
        programs_per_bank: Number of programs per bank (default 128)
    
    Returns:
        Byte offset to the parameter
    """
    offset = pbk2_offset
    
    if parameter_index < 32:
        offset += 32 * program_index + parameter_index
    elif parameter_index < 64:
        offset += 32 * (programs_per_bank + program_index) + parameter_index - 32
    elif parameter_index == 64:
        offset += 32 * (2 * programs_per_bank) + program_index
    elif parameter_index == 65:
        offset += 32 * (2 * programs_per_bank) + programs_per_bank + program_index
    
    return offset


def get_cbk2_parameter_offset(
    cbk2_offset: int,
    combi_index: int,
    timbre_index: int,
    parameter_index: int,
    combis_per_bank: int = 128,
    timbres_per_combi: int = 16
) -> int:
    """Calculate offset to a specific parameter in CBK2 chunk.
    
    Based on C# KronosCombiBank.cs GetParameterOffsetInCbk2().
    
    CBK2 parameter layout:
    - Parameter 0 (Bank): for each combi, for each timbre, 1 byte
    - Parameter 1 (Program): for each combi, for each timbre, 1 byte
    
    Args:
        cbk2_offset: Offset to CBK2 data start
        combi_index: Combi index (0-127)
        timbre_index: Timbre index (0-15)
        parameter_index: Parameter index (0=Bank, 1=Program)
        combis_per_bank: Number of combis per bank (default 128)
        timbres_per_combi: Number of timbres per combi (default 16)
    
    Returns:
        Byte offset to the parameter
    """
    return (cbk2_offset + 
            parameter_index * combis_per_bank * timbres_per_combi +
            combi_index * timbres_per_combi + 
            timbre_index)


def get_stl2_bank_offset(
    stl2_pcg_offset: int,
    setlist_index: int,
    slot_index: int,
    num_setlists: int = 128,
    slots_per_setlist: int = 128
) -> int:
    """Calculate offset to bank byte in STL2 chunk.
    
    Based on C# KronosSetListSlot.cs Stl2BankOffset property.
    
    Args:
        stl2_pcg_offset: Offset to STL2 data start (after SBK2 header)
        setlist_index: Set list index (0-127)
        slot_index: Slot index (0-127)
        num_setlists: Number of set lists (default 128)
        slots_per_setlist: Number of slots per set list (default 128)
    
    Returns:
        Byte offset to the bank byte
    """
    return stl2_pcg_offset + slots_per_setlist * setlist_index + slot_index


def get_stl2_patch_offset(
    stl2_pcg_offset: int,
    setlist_index: int,
    slot_index: int,
    num_setlists: int = 128,
    slots_per_setlist: int = 128
) -> int:
    """Calculate offset to patch byte in STL2 chunk.
    
    Based on C# KronosSetListSlot.cs Stl2PatchOffset property.
    
    Args:
        stl2_pcg_offset: Offset to STL2 data start (after SBK2 header)
        setlist_index: Set list index (0-127)
        slot_index: Slot index (0-127)
        num_setlists: Number of set lists (default 128)
        slots_per_setlist: Number of slots per set list (default 128)
    
    Returns:
        Byte offset to the patch byte
    """
    # Patch bytes come after all bank bytes
    return (num_setlists * slots_per_setlist + 
            stl2_pcg_offset + 
            slots_per_setlist * setlist_index + 
            slot_index)


def copy_pbk2_data(
    source_data: bytes,
    dest_data: bytearray,
    source_pbk2_offset: int,
    dest_pbk2_offset: int,
    source_program_index: int,
    dest_program_index: int,
    programs_per_bank: int = 128
) -> None:
    """Copy PBK2 data from one program to another.
    
    Based on C# KronosProgramBanks.cs CopyPbk2Content().
    
    Args:
        source_data: Source PCG file data
        dest_data: Destination PCG file data (mutable)
        source_pbk2_offset: Source PBK2 data offset
        dest_pbk2_offset: Destination PBK2 data offset
        source_program_index: Source program index
        dest_program_index: Destination program index
        programs_per_bank: Number of programs per bank
    """
    for parameter in range(ExtendedDataConstants.PARAMETERS_IN_PBK2):
        src_offset = get_pbk2_parameter_offset(
            source_pbk2_offset, source_program_index, parameter, programs_per_bank)
        dst_offset = get_pbk2_parameter_offset(
            dest_pbk2_offset, dest_program_index, parameter, programs_per_bank)
        
        if src_offset < len(source_data) and dst_offset < len(dest_data):
            dest_data[dst_offset] = source_data[src_offset]


def copy_cbk2_data(
    source_data: bytes,
    dest_data: bytearray,
    source_cbk2_offset: int,
    dest_cbk2_offset: int,
    source_combi_index: int,
    dest_combi_index: int,
    combis_per_bank: int = 128,
    timbres_per_combi: int = 16
) -> None:
    """Copy CBK2 data from one combi to another.
    
    Based on C# KronosCombiBanks.cs CopyCbk2Content() (implied from SwapCbk2Content).
    
    Args:
        source_data: Source PCG file data
        dest_data: Destination PCG file data (mutable)
        source_cbk2_offset: Source CBK2 data offset
        dest_cbk2_offset: Destination CBK2 data offset
        source_combi_index: Source combi index
        dest_combi_index: Destination combi index
        combis_per_bank: Number of combis per bank
        timbres_per_combi: Number of timbres per combi
    """
    for parameter in range(ExtendedDataConstants.PARAMETERS_IN_CBK2):
        for timbre in range(timbres_per_combi):
            src_offset = get_cbk2_parameter_offset(
                source_cbk2_offset, source_combi_index, timbre, parameter,
                combis_per_bank, timbres_per_combi)
            dst_offset = get_cbk2_parameter_offset(
                dest_cbk2_offset, dest_combi_index, timbre, parameter,
                combis_per_bank, timbres_per_combi)
            
            if src_offset < len(source_data) and dst_offset < len(dest_data):
                dest_data[dst_offset] = source_data[src_offset]


def copy_stl2_data(
    source_data: bytes,
    dest_data: bytearray,
    source_stl2_offset: int,
    dest_stl2_offset: int,
    source_setlist_index: int,
    source_slot_index: int,
    dest_setlist_index: int,
    dest_slot_index: int,
    num_setlists: int = 128,
    slots_per_setlist: int = 128
) -> None:
    """Copy STL2 data from one slot to another.
    
    Based on C# KronosPcgMemory.cs paste logic for set list slots.
    
    Args:
        source_data: Source PCG file data
        dest_data: Destination PCG file data (mutable)
        source_stl2_offset: Source STL2 data offset
        dest_stl2_offset: Destination STL2 data offset
        source_setlist_index: Source set list index
        source_slot_index: Source slot index
        dest_setlist_index: Destination set list index
        dest_slot_index: Destination slot index
        num_setlists: Number of set lists
        slots_per_setlist: Number of slots per set list
    """
    # Copy bank byte
    src_bank_offset = get_stl2_bank_offset(
        source_stl2_offset, source_setlist_index, source_slot_index,
        num_setlists, slots_per_setlist)
    dst_bank_offset = get_stl2_bank_offset(
        dest_stl2_offset, dest_setlist_index, dest_slot_index,
        num_setlists, slots_per_setlist)
    
    if src_bank_offset < len(source_data) and dst_bank_offset < len(dest_data):
        dest_data[dst_bank_offset] = source_data[src_bank_offset]
    
    # Copy patch byte
    src_patch_offset = get_stl2_patch_offset(
        source_stl2_offset, source_setlist_index, source_slot_index,
        num_setlists, slots_per_setlist)
    dst_patch_offset = get_stl2_patch_offset(
        dest_stl2_offset, dest_setlist_index, dest_slot_index,
        num_setlists, slots_per_setlist)
    
    if src_patch_offset < len(source_data) and dst_patch_offset < len(dest_data):
        dest_data[dst_patch_offset] = source_data[src_patch_offset]



def swap_pbk2_data(
    data: bytearray,
    pbk2_offset_1: int,
    pbk2_offset_2: int,
    program_index_1: int,
    program_index_2: int,
    programs_per_bank: int = 128
) -> None:
    """Swap PBK2 data between two programs.
    
    Based on C# KronosProgramBanks.cs SwapPbk2Content().
    
    Args:
        data: PCG file data (mutable)
        pbk2_offset_1: First program's PBK2 data offset
        pbk2_offset_2: Second program's PBK2 data offset
        program_index_1: First program index
        program_index_2: Second program index
        programs_per_bank: Number of programs per bank
    """
    for parameter in range(ExtendedDataConstants.PARAMETERS_IN_PBK2):
        offset_1 = get_pbk2_parameter_offset(
            pbk2_offset_1, program_index_1, parameter, programs_per_bank)
        offset_2 = get_pbk2_parameter_offset(
            pbk2_offset_2, program_index_2, parameter, programs_per_bank)
        
        if offset_1 < len(data) and offset_2 < len(data):
            # Swap bytes
            temp = data[offset_1]
            data[offset_1] = data[offset_2]
            data[offset_2] = temp


def swap_cbk2_data(
    data: bytearray,
    cbk2_offset_1: int,
    cbk2_offset_2: int,
    combi_index_1: int,
    combi_index_2: int,
    combis_per_bank: int = 128,
    timbres_per_combi: int = 16
) -> None:
    """Swap CBK2 data between two combis.
    
    Based on C# KronosCombiBanks.cs SwapCbk2Content().
    
    Args:
        data: PCG file data (mutable)
        cbk2_offset_1: First combi's CBK2 data offset
        cbk2_offset_2: Second combi's CBK2 data offset
        combi_index_1: First combi index
        combi_index_2: Second combi index
        combis_per_bank: Number of combis per bank
        timbres_per_combi: Number of timbres per combi
    """
    for parameter in range(ExtendedDataConstants.PARAMETERS_IN_CBK2):
        for timbre in range(timbres_per_combi):
            offset_1 = get_cbk2_parameter_offset(
                cbk2_offset_1, combi_index_1, timbre, parameter,
                combis_per_bank, timbres_per_combi)
            offset_2 = get_cbk2_parameter_offset(
                cbk2_offset_2, combi_index_2, timbre, parameter,
                combis_per_bank, timbres_per_combi)
            
            if offset_1 < len(data) and offset_2 < len(data):
                # Swap bytes
                temp = data[offset_1]
                data[offset_1] = data[offset_2]
                data[offset_2] = temp


def swap_stl2_data(
    data: bytearray,
    stl2_offset: int,
    setlist_index_1: int,
    slot_index_1: int,
    setlist_index_2: int,
    slot_index_2: int,
    num_setlists: int = 128,
    slots_per_setlist: int = 128
) -> None:
    """Swap STL2 data between two slots.
    
    Based on C# KronosSetListSlot.cs SwapOs1516Data().
    
    Args:
        data: PCG file data (mutable)
        stl2_offset: STL2 data offset
        setlist_index_1: First set list index
        slot_index_1: First slot index
        setlist_index_2: Second set list index
        slot_index_2: Second slot index
        num_setlists: Number of set lists
        slots_per_setlist: Number of slots per set list
    """
    # Get offsets for both slots
    bank_offset_1 = get_stl2_bank_offset(
        stl2_offset, setlist_index_1, slot_index_1, num_setlists, slots_per_setlist)
    bank_offset_2 = get_stl2_bank_offset(
        stl2_offset, setlist_index_2, slot_index_2, num_setlists, slots_per_setlist)
    patch_offset_1 = get_stl2_patch_offset(
        stl2_offset, setlist_index_1, slot_index_1, num_setlists, slots_per_setlist)
    patch_offset_2 = get_stl2_patch_offset(
        stl2_offset, setlist_index_2, slot_index_2, num_setlists, slots_per_setlist)
    
    # Swap bank bytes
    if bank_offset_1 < len(data) and bank_offset_2 < len(data):
        temp = data[bank_offset_1]
        data[bank_offset_1] = data[bank_offset_2]
        data[bank_offset_2] = temp
    
    # Swap patch bytes
    if patch_offset_1 < len(data) and patch_offset_2 < len(data):
        temp = data[patch_offset_1]
        data[patch_offset_1] = data[patch_offset_2]
        data[patch_offset_2] = temp


def calc_pbk2_differences(
    data1: bytes,
    data2: bytes,
    pbk2_offset_1: int,
    pbk2_offset_2: int,
    program_index_1: int,
    program_index_2: int,
    programs_per_bank: int = 128,
    max_diffs: int = -1
) -> int:
    """Calculate number of byte differences in PBK2 data between two programs.
    
    Based on C# KronosProgram.cs CalcByteDifferences() PBK2 section.
    
    Args:
        data1: First PCG file data
        data2: Second PCG file data
        pbk2_offset_1: First program's PBK2 data offset
        pbk2_offset_2: Second program's PBK2 data offset
        program_index_1: First program index
        program_index_2: Second program index
        programs_per_bank: Number of programs per bank
        max_diffs: Stop counting after this many differences (-1 = count all)
    
    Returns:
        Number of byte differences
    """
    diffs = 0
    
    for parameter in range(ExtendedDataConstants.PARAMETERS_IN_PBK2):
        offset_1 = get_pbk2_parameter_offset(
            pbk2_offset_1, program_index_1, parameter, programs_per_bank)
        offset_2 = get_pbk2_parameter_offset(
            pbk2_offset_2, program_index_2, parameter, programs_per_bank)
        
        if offset_1 < len(data1) and offset_2 < len(data2):
            if data1[offset_1] != data2[offset_2]:
                diffs += 1
                if max_diffs >= 0 and diffs >= max_diffs:
                    return diffs
    
    return diffs


def calc_cbk2_differences(
    data1: bytes,
    data2: bytes,
    cbk2_offset_1: int,
    cbk2_offset_2: int,
    combi_index_1: int,
    combi_index_2: int,
    combis_per_bank: int = 128,
    timbres_per_combi: int = 16,
    max_diffs: int = -1
) -> int:
    """Calculate number of byte differences in CBK2 data between two combis.
    
    Based on C# KronosCombi.cs CalcByteDifferences() CBK2 section.
    
    Args:
        data1: First PCG file data
        data2: Second PCG file data
        cbk2_offset_1: First combi's CBK2 data offset
        cbk2_offset_2: Second combi's CBK2 data offset
        combi_index_1: First combi index
        combi_index_2: Second combi index
        combis_per_bank: Number of combis per bank
        timbres_per_combi: Number of timbres per combi
        max_diffs: Stop counting after this many differences (-1 = count all)
    
    Returns:
        Number of byte differences
    """
    diffs = 0
    
    for parameter in range(ExtendedDataConstants.PARAMETERS_IN_CBK2):
        for timbre in range(timbres_per_combi):
            offset_1 = get_cbk2_parameter_offset(
                cbk2_offset_1, combi_index_1, timbre, parameter,
                combis_per_bank, timbres_per_combi)
            offset_2 = get_cbk2_parameter_offset(
                cbk2_offset_2, combi_index_2, timbre, parameter,
                combis_per_bank, timbres_per_combi)
            
            if offset_1 < len(data1) and offset_2 < len(data2):
                if data1[offset_1] != data2[offset_2]:
                    diffs += 1
                    if max_diffs >= 0 and diffs >= max_diffs:
                        return diffs
    
    return diffs


def calc_stl2_differences(
    data1: bytes,
    data2: bytes,
    stl2_offset_1: int,
    stl2_offset_2: int,
    setlist_index_1: int,
    slot_index_1: int,
    setlist_index_2: int,
    slot_index_2: int,
    num_setlists: int = 128,
    slots_per_setlist: int = 128
) -> int:
    """Calculate number of byte differences in STL2 data between two slots.
    
    Based on C# KronosSetListSlot.cs CalcByteDifferences() SLS2 section.
    
    Args:
        data1: First PCG file data
        data2: Second PCG file data
        stl2_offset_1: First slot's STL2 data offset
        stl2_offset_2: Second slot's STL2 data offset
        setlist_index_1: First set list index
        slot_index_1: First slot index
        setlist_index_2: Second set list index
        slot_index_2: Second slot index
        num_setlists: Number of set lists
        slots_per_setlist: Number of slots per set list
    
    Returns:
        Number of byte differences (0, 1, or 2)
    """
    diffs = 0
    
    # Compare bank bytes
    bank_offset_1 = get_stl2_bank_offset(
        stl2_offset_1, setlist_index_1, slot_index_1, num_setlists, slots_per_setlist)
    bank_offset_2 = get_stl2_bank_offset(
        stl2_offset_2, setlist_index_2, slot_index_2, num_setlists, slots_per_setlist)
    
    if bank_offset_1 < len(data1) and bank_offset_2 < len(data2):
        if data1[bank_offset_1] != data2[bank_offset_2]:
            diffs += 1
    
    # Compare patch bytes
    patch_offset_1 = get_stl2_patch_offset(
        stl2_offset_1, setlist_index_1, slot_index_1, num_setlists, slots_per_setlist)
    patch_offset_2 = get_stl2_patch_offset(
        stl2_offset_2, setlist_index_2, slot_index_2, num_setlists, slots_per_setlist)
    
    if patch_offset_1 < len(data1) and patch_offset_2 < len(data2):
        if data1[patch_offset_1] != data2[patch_offset_2]:
            diffs += 1
    
    return diffs



# =============================================================================
# PROGRAM WAVE SEQUENCE REFERENCES - Based on C# KronosProgram.cs
# =============================================================================

class ProgramWaveSequenceOffsets:
    """Program wave sequence reference offsets.
    
    Reference: C# KronosProgram.cs GetUsedWaveSequence(), GetZoneMsType(), GetZoneMsByteOffset()
    
    Each program can have up to 2 oscillators (OSC 1, OSC 2) with 8 zones each.
    Each zone can reference a wave sequence.
    """
    # Base offset for OSC 1 zone 0
    OSC1_ZONE0_BASE = 2774
    
    # Offset between OSC 1 and OSC 2
    OSC_OFFSET = 3240 - 2774  # 466 bytes
    
    # Offset between zones
    ZONE_OFFSET = 2796 - 2774  # 22 bytes
    
    # Within each zone:
    MS_TYPE_OFFSET = 0  # 1 byte: 0=Off, 1=MS (Sample), 2=Wave Sequence
    MS_BANK_OFFSET = 1  # 1 byte (for OS 1.0/1.1) or 16 (for OS 2.x/3.x)
    MS_NUMBER_OFFSET = 2  # 1 byte (for OS 1.0/1.1) or 17 (for OS 2.x/3.x)
    
    # For OS 2.x/3.x, wave sequence index is a 2-byte value at offset 16
    WAVESEQ_INDEX_OFFSET_2X = 16


class MsType(IntEnum):
    """Multi-sample type values."""
    OFF = 0
    SAMPLE = 1  # MS (Multi-Sample)
    WAVE_SEQUENCE = 2


def get_zone_ms_byte_offset(program_offset: int, osc: int, zone: int) -> int:
    """Calculate byte offset for a zone's MS data within a program.
    
    Based on C# KronosProgram.cs GetZoneMsByteOffset().
    
    Args:
        program_offset: Byte offset to program data start
        osc: Oscillator index (0 or 1)
        zone: Zone index (0-7)
    
    Returns:
        Byte offset to the zone's MS data
    """
    return (program_offset + 
            ProgramWaveSequenceOffsets.OSC1_ZONE0_BASE + 
            osc * ProgramWaveSequenceOffsets.OSC_OFFSET + 
            zone * ProgramWaveSequenceOffsets.ZONE_OFFSET)


def get_zone_ms_type(data: bytes, program_offset: int, osc: int, zone: int) -> int:
    """Get the MS type for a zone.
    
    Based on C# KronosProgram.cs GetZoneMsType().
    
    Args:
        data: PCG file data
        program_offset: Byte offset to program data start
        osc: Oscillator index (0 or 1)
        zone: Zone index (0-7)
    
    Returns:
        MsType value (0=Off, 1=Sample, 2=WaveSequence)
    """
    offset = get_zone_ms_byte_offset(program_offset, osc, zone)
    if offset < len(data):
        return data[offset] & 0x03
    return MsType.OFF


def get_zone_wave_sequence_ref(
    data: bytes, 
    program_offset: int, 
    osc: int, 
    zone: int,
    os_version: str = "2.x/3.x"
) -> Optional[Tuple[int, int]]:
    """Get wave sequence bank and index for a zone.
    
    Based on C# KronosProgram.cs GetUsedWaveSequence().
    
    Args:
        data: PCG file data
        program_offset: Byte offset to program data start
        osc: Oscillator index (0 or 1)
        zone: Zone index (0-7)
        os_version: "1.0/1.1", "1.5/1.6", or "2.x/3.x"
    
    Returns:
        Tuple of (bank_index, patch_index) or None if not a wave sequence
    """
    ms_type = get_zone_ms_type(data, program_offset, osc, zone)
    if ms_type != MsType.WAVE_SEQUENCE:
        return None
    
    zone_offset = get_zone_ms_byte_offset(program_offset, osc, zone)
    
    if os_version in ("1.0/1.1", "1.5/1.6"):
        # Bank at offset +16, patch at offset +17
        if zone_offset + 18 > len(data):
            return None
        bank_id = data[zone_offset + 16]
        patch_index = data[zone_offset + 17]
        
        # Convert bank ID: 0x40+ = User banks
        if bank_id >= 0x40:
            bank_index = bank_id - 0x40  # U-A..U-G
        else:
            bank_index = bank_id
        
        return (bank_index, patch_index)
    
    else:  # OS 2.x/3.x
        # Wave sequence index is a 2-byte value at offset +16
        if zone_offset + 18 > len(data):
            return None
        waveseq_index = struct.unpack('<H', data[zone_offset + 16:zone_offset + 18])[0]
        
        # Need to convert linear index to bank/patch
        # This requires knowing the wave sequence bank sizes
        # For now, return as (0, index) - caller needs to resolve
        return (0, waveseq_index)


def set_zone_wave_sequence_ref(
    data: bytearray,
    program_offset: int,
    osc: int,
    zone: int,
    bank_index: int,
    patch_index: int,
    os_version: str = "2.x/3.x"
) -> None:
    """Set wave sequence reference for a zone.
    
    Based on C# KronosProgram.cs SetWaveSequence().
    
    Args:
        data: PCG file data (mutable)
        program_offset: Byte offset to program data start
        osc: Oscillator index (0 or 1)
        zone: Zone index (0-7)
        bank_index: Wave sequence bank index
        patch_index: Wave sequence patch index
        os_version: "1.0/1.1", "1.5/1.6", or "2.x/3.x"
    """
    zone_offset = get_zone_ms_byte_offset(program_offset, osc, zone)
    
    if os_version in ("1.0/1.1", "1.5/1.6"):
        # Bank at offset +1 (7 bits), patch at offset +2 (7 bits)
        if zone_offset + 3 <= len(data):
            # Convert bank index to ID
            if bank_index >= 0x40:
                bank_id = bank_index
            else:
                bank_id = bank_index
            
            data[zone_offset + 1] = (data[zone_offset + 1] & 0x80) | (bank_id & 0x7F)
            data[zone_offset + 2] = (data[zone_offset + 2] & 0x80) | (patch_index & 0x7F)
    
    else:  # OS 2.x/3.x
        # Wave sequence index as 2-byte value at offset +16
        if zone_offset + 18 <= len(data):
            # For OS 2.x/3.x, need to calculate linear index
            # This is simplified - caller should provide the correct linear index
            waveseq_index = patch_index  # Simplified
            data[zone_offset + 16:zone_offset + 18] = struct.pack('<H', waveseq_index)


# =============================================================================
# DRUM TRACK PARAMETERS - Based on C# KronosProgram.cs, KronosCombi.cs
# =============================================================================

class DrumTrackOffsets:
    """Drum track parameter offsets.
    
    Reference: C# KronosProgram.cs, KronosCombi.cs GetParam()
    """
    # Common drum track pattern (in both Program and Combi)
    PATTERN_NUMBER = 1292  # 2 bytes, little-endian, subtract 1 for display
    PATTERN_BANK = 1294    # 1 byte, bits 0-1
    
    # Program-specific drum track
    PROGRAM_NUMBER = 2688  # 1 byte, bits 0-6
    PROGRAM_BANK = 2689    # 1 byte, bits 0-6


def get_drum_track_pattern(data: bytes, patch_offset: int) -> Tuple[int, int]:
    """Get drum track pattern number and bank.
    
    Args:
        data: PCG file data
        patch_offset: Byte offset to program or combi data start
    
    Returns:
        Tuple of (pattern_number, pattern_bank)
    """
    if patch_offset + DrumTrackOffsets.PATTERN_BANK + 1 > len(data):
        return (0, 0)
    
    pattern_num = struct.unpack('<H', 
        data[patch_offset + DrumTrackOffsets.PATTERN_NUMBER:
             patch_offset + DrumTrackOffsets.PATTERN_NUMBER + 2])[0]
    pattern_bank = data[patch_offset + DrumTrackOffsets.PATTERN_BANK] & 0x03
    
    return (pattern_num, pattern_bank)


def get_program_drum_track_program(data: bytes, program_offset: int) -> Tuple[int, int]:
    """Get drum track program number and bank (program-specific).
    
    Args:
        data: PCG file data
        program_offset: Byte offset to program data start
    
    Returns:
        Tuple of (program_number, program_bank)
    """
    if program_offset + DrumTrackOffsets.PROGRAM_BANK + 1 > len(data):
        return (0, 0)
    
    prog_num = data[program_offset + DrumTrackOffsets.PROGRAM_NUMBER] & 0x7F
    prog_bank = data[program_offset + DrumTrackOffsets.PROGRAM_BANK] & 0x7F
    
    return (prog_num, prog_bank)


# =============================================================================
# DPI1 DRUM PATTERN PARSING - Based on C# PcgFileReader.cs
# =============================================================================

@dataclass
class DrumPatternBankInfo:
    """Parsed drum pattern bank information."""
    bank_id: int
    bank_name: str
    num_patterns: int
    pattern_size: int
    byte_offset: int
    patterns: List[Tuple[str, int]] = field(default_factory=list)  # (name, offset)


@dataclass
class DrumPatternInfo:
    """Parsed DPI1 chunk information."""
    dpn1_offset: int = 0  # DPN1 sub-chunk offset
    dpd1_offset: int = 0  # DPD1 sub-chunk offset
    dps1_offset: int = 0  # DPS1 sub-chunk offset
    banks: List[DrumPatternBankInfo] = field(default_factory=list)


def parse_dpi1_chunk(data: bytes, dpi1_offset: int) -> Optional[DrumPatternInfo]:
    """Parse DPI1 (drum pattern container) chunk.
    
    Based on C# PcgFileReader.cs ReadDpi1Chunk().
    
    DPI1 structure:
    - DPN1: Drum pattern names
    - DPD1: Drum pattern data (contains pattern names + other data)
    - DPS1: Drum pattern sequences (contains DPV1 sub-chunks)
    
    Args:
        data: Full PCG file data
        dpi1_offset: Offset to DPI1 chunk
    
    Returns:
        DrumPatternInfo or None if invalid
    """
    if len(data) < dpi1_offset + 12:
        return None
    
    # Verify DPI1 chunk
    if data[dpi1_offset:dpi1_offset+4] != ChunkId.DPI1:
        return None
    
    chunk_size = struct.unpack('>I', data[dpi1_offset+4:dpi1_offset+8])[0]
    
    info = DrumPatternInfo()
    
    # Skip DPI1 header (12 bytes)
    offset = dpi1_offset + 12
    
    # Find DPN1
    if offset + 8 > len(data):
        return info
    
    if data[offset:offset+4] == b'DPN1':
        info.dpn1_offset = offset
        dpn1_size = struct.unpack('>I', data[offset+4:offset+8])[0]
        offset += dpn1_size + 12  # Skip DPN1
    
    # Find DPD1
    if offset + 8 > len(data):
        return info
    
    if data[offset:offset+4] == b'DPD1':
        info.dpd1_offset = offset
        dpd1_size = struct.unpack('>I', data[offset+4:offset+8])[0]
        
        # Parse DPD1 content
        dpd1_data_offset = offset + 12
        
        if dpd1_data_offset + 8 <= len(data):
            num_patterns = struct.unpack('>I', data[dpd1_data_offset:dpd1_data_offset+4])[0]
            pattern_size = struct.unpack('>I', data[dpd1_data_offset+4:dpd1_data_offset+8])[0]
            
            # Create user bank info
            bank_info = DrumPatternBankInfo(
                bank_id=1,  # User bank
                bank_name='USER',
                num_patterns=num_patterns,
                pattern_size=pattern_size,
                byte_offset=dpd1_data_offset + 12
            )
            
            # Parse pattern names
            pattern_offset = dpd1_data_offset + 12
            for i in range(num_patterns):
                if pattern_offset + 24 > len(data):
                    break
                
                name_bytes = data[pattern_offset:pattern_offset+24]
                name = name_bytes.split(b'\x00')[0].decode('ascii', errors='replace').strip()
                bank_info.patterns.append((name, pattern_offset))
                pattern_offset += pattern_size
            
            info.banks.append(bank_info)
        
        offset += dpd1_size + 12  # Skip DPD1
    
    # Find DPS1
    if offset + 8 <= len(data):
        if data[offset:offset+4] == b'DPS1':
            info.dps1_offset = offset
    
    return info


# =============================================================================
# VIRTUAL BANK HANDLING - Based on C# KronosProgramBanks.cs, KronosCombiBanks.cs
# =============================================================================

class VirtualBankConstants:
    """Virtual bank constants.
    
    Reference: C# KronosProgramBanks.cs, KronosCombiBanks.cs
    """
    # First virtual bank ID
    FIRST_VIRTUAL_BANK_ID = 0x30
    
    # Number of virtual banks (8 groups × 8 banks)
    NUM_VIRTUAL_BANKS = 64
    
    # Bank names per group
    BANK_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    
    # Number of groups
    NUM_GROUPS = 8


def get_virtual_bank_name(bank_id: int) -> Optional[str]:
    """Convert virtual bank ID to name.
    
    Args:
        bank_id: Bank ID (0x30 to 0x6F)
    
    Returns:
        Bank name like 'V0-A', 'V7-H', or None if not a virtual bank
    """
    if bank_id < VirtualBankConstants.FIRST_VIRTUAL_BANK_ID:
        return None
    
    virtual_index = bank_id - VirtualBankConstants.FIRST_VIRTUAL_BANK_ID
    if virtual_index >= VirtualBankConstants.NUM_VIRTUAL_BANKS:
        return None
    
    group = virtual_index // len(VirtualBankConstants.BANK_LETTERS)
    letter_index = virtual_index % len(VirtualBankConstants.BANK_LETTERS)
    
    return f"V{group}-{VirtualBankConstants.BANK_LETTERS[letter_index]}"


def get_virtual_bank_id(bank_name: str) -> Optional[int]:
    """Convert virtual bank name to ID.
    
    Args:
        bank_name: Bank name like 'V0-A', 'V7-H'
    
    Returns:
        Bank ID or None if not a valid virtual bank name
    """
    if not bank_name.startswith('V') or '-' not in bank_name:
        return None
    
    try:
        parts = bank_name[1:].split('-')
        group = int(parts[0])
        letter = parts[1].upper()
        
        if group < 0 or group >= VirtualBankConstants.NUM_GROUPS:
            return None
        
        if letter not in VirtualBankConstants.BANK_LETTERS:
            return None
        
        letter_index = VirtualBankConstants.BANK_LETTERS.index(letter)
        
        return (VirtualBankConstants.FIRST_VIRTUAL_BANK_ID + 
                group * len(VirtualBankConstants.BANK_LETTERS) + 
                letter_index)
    except (ValueError, IndexError):
        return None


def is_virtual_bank(bank_id: int) -> bool:
    """Check if a bank ID is a virtual bank.
    
    Args:
        bank_id: Bank ID to check
    
    Returns:
        True if virtual bank
    """
    return (bank_id >= VirtualBankConstants.FIRST_VIRTUAL_BANK_ID and
            bank_id < VirtualBankConstants.FIRST_VIRTUAL_BANK_ID + 
                      VirtualBankConstants.NUM_VIRTUAL_BANKS)


# =============================================================================
# GM BANK HANDLING - Based on C# KronosGmProgramBank.cs
# =============================================================================

class GmBankConstants:
    """GM bank constants.
    
    Reference: C# KronosGmProgramBank.cs, KronosProgramBanks.cs
    """
    # GM bank PcgId
    GM_BANK_PCGID = 6
    
    # GM bank is read-only (ROM data)
    IS_READONLY = True
    
    # GM bank synthesis type
    SYNTHESIS_TYPE = 'HD1'
    
    # Number of GM programs
    NUM_PROGRAMS = 128
    
    # GM2 sub-banks (g(1) through g(9), g(d))
    GM2_SUB_BANKS = ['g(1)', 'g(2)', 'g(3)', 'g(4)', 'g(5)', 
                     'g(6)', 'g(7)', 'g(8)', 'g(9)', 'g(d)']


def is_gm_bank(bank_id: int) -> bool:
    """Check if a bank ID is the GM bank.
    
    Args:
        bank_id: Bank ID to check
    
    Returns:
        True if GM bank
    """
    return bank_id == GmBankConstants.GM_BANK_PCGID


def get_gm2_sub_bank_name(sub_bank_index: int) -> Optional[str]:
    """Get GM2 sub-bank name.
    
    Args:
        sub_bank_index: Sub-bank index (0-9)
    
    Returns:
        Sub-bank name like 'g(1)' or None if invalid
    """
    if 0 <= sub_bank_index < len(GmBankConstants.GM2_SUB_BANKS):
        return GmBankConstants.GM2_SUB_BANKS[sub_bank_index]
    return None


# =============================================================================
# OS 1.5/1.6 TIMBRE PROGRAM REFERENCE HELPERS
# Based on C# KronosTimbre.cs UsedProgramBankId, UsedProgramId, UsedProgram
# =============================================================================

def get_timbre_program_ref_os15(
    data: bytes,
    combi_offset: int,
    timbre_index: int,
    cbk2_offset: int,
    combis_per_bank: int = 128,
    timbres_per_combi: int = 16
) -> Tuple[int, int]:
    """Get timbre program reference for OS 1.5/1.6 files.
    
    Based on C# KronosTimbre.cs UsedProgramBankId and UsedProgramId properties.
    
    For OS 1.5/1.6, the program bank and index are stored in CBK2 chunk
    when available, otherwise in CMB1.
    
    Args:
        data: PCG file data
        combi_offset: Byte offset to combi data start
        timbre_index: Timbre index (0-15)
        cbk2_offset: CBK2 data offset (0 if not available)
        combis_per_bank: Number of combis per bank
        timbres_per_combi: Number of timbres per combi
    
    Returns:
        Tuple of (bank_id, program_index)
    """
    timbre_offset = combi_offset + KronosCombiOffsets.TIMBRES_OFFSET + timbre_index * KronosTimbreOffsets.TIMBRE_SIZE
    
    if cbk2_offset > 0:
        # Read from CBK2
        # Bank is at parameter 0, program is at parameter 1
        # But we need the combi index within the bank
        # For simplicity, assume combi_index = 0 (caller should provide)
        combi_index = 0  # This should be passed in
        
        bank_offset = get_cbk2_parameter_offset(
            cbk2_offset, combi_index, timbre_index, 0,
            combis_per_bank, timbres_per_combi)
        prog_offset = get_cbk2_parameter_offset(
            cbk2_offset, combi_index, timbre_index, 1,
            combis_per_bank, timbres_per_combi)
        
        if bank_offset < len(data) and prog_offset < len(data):
            return (data[bank_offset], data[prog_offset])
    
    # Fall back to CMB1
    if timbre_offset + 2 <= len(data):
        return (data[timbre_offset + 1], data[timbre_offset])
    
    return (0, 0)


def set_timbre_program_ref_os15(
    data: bytearray,
    combi_offset: int,
    combi_index: int,
    timbre_index: int,
    bank_id: int,
    program_index: int,
    cbk2_offset: int,
    combis_per_bank: int = 128,
    timbres_per_combi: int = 16
) -> None:
    """Set timbre program reference for OS 1.5/1.6 files.
    
    Based on C# KronosTimbre.cs UsedProgram setter.
    
    For OS 1.5/1.6, writes to both CMB1 and CBK2.
    
    Args:
        data: PCG file data (mutable)
        combi_offset: Byte offset to combi data start
        combi_index: Combi index within bank
        timbre_index: Timbre index (0-15)
        bank_id: Program bank ID
        program_index: Program index
        cbk2_offset: CBK2 data offset (0 if not available)
        combis_per_bank: Number of combis per bank
        timbres_per_combi: Number of timbres per combi
    """
    timbre_offset = combi_offset + KronosCombiOffsets.TIMBRES_OFFSET + timbre_index * KronosTimbreOffsets.TIMBRE_SIZE
    
    # Write to CMB1
    if timbre_offset + 2 <= len(data):
        # For extended user banks (U-AA etc), write 127 to CMB1 program index
        if bank_id >= 24:  # Extended user bank
            data[timbre_offset] = 127
            data[timbre_offset + 1] = 23  # U-G as placeholder
        else:
            data[timbre_offset] = program_index
            data[timbre_offset + 1] = bank_id
    
    # Write to CBK2 if available
    if cbk2_offset > 0:
        bank_offset = get_cbk2_parameter_offset(
            cbk2_offset, combi_index, timbre_index, 0,
            combis_per_bank, timbres_per_combi)
        prog_offset = get_cbk2_parameter_offset(
            cbk2_offset, combi_index, timbre_index, 1,
            combis_per_bank, timbres_per_combi)
        
        if bank_offset < len(data) and prog_offset < len(data):
            data[bank_offset] = bank_id
            data[prog_offset] = program_index


# =============================================================================
# COMBI TEMPO - Based on C# KronosCombi.cs
# =============================================================================

def get_combi_tempo(data: bytes, combi_offset: int) -> float:
    """Get combi tempo in BPM.
    
    Based on C# KronosCombi.cs Tempo parameter.
    
    Args:
        data: PCG file data
        combi_offset: Byte offset to combi data start
    
    Returns:
        Tempo in BPM (divide raw value by 100)
    """
    tempo_offset = combi_offset + KronosCombiOffsets.TEMPO
    if tempo_offset + 2 <= len(data):
        raw_tempo = struct.unpack('<H', data[tempo_offset:tempo_offset+2])[0]
        return raw_tempo / 100.0
    return 120.0  # Default


def set_combi_tempo(data: bytearray, combi_offset: int, tempo_bpm: float) -> None:
    """Set combi tempo.
    
    Args:
        data: PCG file data (mutable)
        combi_offset: Byte offset to combi data start
        tempo_bpm: Tempo in BPM
    """
    tempo_offset = combi_offset + KronosCombiOffsets.TEMPO
    if tempo_offset + 2 <= len(data):
        raw_tempo = int(tempo_bpm * 100)
        data[tempo_offset:tempo_offset+2] = struct.pack('<H', raw_tempo)


# =============================================================================
# CHUNK ITERATION UTILITIES - Based on C# PcgFileReader.cs
# =============================================================================

def iterate_chunks(
    data: bytes,
    start_offset: int = 0x1C,
    gap_size: int = 12
) -> List[Tuple[bytes, int, int]]:
    """Iterate through all chunks in a PCG file.
    
    Based on C# PcgFileReader.cs ReadContent() loop.
    
    Args:
        data: Full PCG file data
        start_offset: Offset to first chunk (0x1C for Kronos)
        gap_size: Gap between chunks (12 for Kronos)
    
    Yields:
        Tuples of (chunk_id, offset, size)
    """
    chunks = []
    offset = start_offset
    
    while offset < len(data) - 8:
        chunk_id = data[offset:offset+4]
        
        # Validate chunk ID (should be printable ASCII)
        if not all(32 <= b < 127 for b in chunk_id):
            break
        
        chunk_size = struct.unpack('>I', data[offset+4:offset+8])[0]
        
        chunks.append((chunk_id, offset, chunk_size))
        
        offset += chunk_size + gap_size
    
    return chunks


def find_chunk(
    data: bytes,
    chunk_id: bytes,
    start_offset: int = 0x1C,
    gap_size: int = 12,
    occurrence: int = 0
) -> Optional[Tuple[int, int]]:
    """Find a specific chunk in a PCG file.
    
    Args:
        data: Full PCG file data
        chunk_id: 4-byte chunk ID to find
        start_offset: Offset to first chunk
        gap_size: Gap between chunks
        occurrence: Which occurrence to find (0 = first)
    
    Returns:
        Tuple of (offset, size) or None if not found
    """
    found = 0
    
    for cid, offset, size in iterate_chunks(data, start_offset, gap_size):
        if cid == chunk_id:
            if found == occurrence:
                return (offset, size)
            found += 1
    
    return None
