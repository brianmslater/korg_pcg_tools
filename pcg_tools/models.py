"""Data models for PCG file structures."""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class WorkstationModel(Enum):
    """Supported Korg workstation models."""
    KRONOS = "Korg Kronos"
    KRONOS_X = "Korg Kronos X"
    OASYS = "Korg Oasys"
    TRITON = "Korg Triton"
    TRITON_EXTREME = "Korg Triton Extreme"
    TRITON_STUDIO = "Korg Triton Studio"
    TRITON_LE = "Korg Triton LE"
    KARMA = "Korg Karma"
    M3 = "Korg M3"
    M50 = "Korg M50"
    KROME = "Korg Krome"
    TRINITY = "Korg Trinity"


class SlotTextSize(Enum):
    """Setlist slot text size options.
    
    Based on C# PCG Tools implementation.
    Values are 3-bit fields split across two bytes:
    - MSB (1 bit): Byte +29, bit 4
    - LSB (2 bits): Byte +24, bits 7-6
    """
    S = 0    # Small
    XS = 1   # Extra Small
    M = 2    # Medium (default)
    L = 3    # Large
    XL = 4   # Extra Large


# Complete Kronos setlist slot colors (all 16 official colors)
# Values confirmed from "SETLIST Movie TV Themes LOAD SEPARATELY 2.PCG" analysis
SLOT_COLORS = {
    0: "Default",
    136: "Brick",
    137: "Brick",      # Variant found in Preload setlists
    140: "Burgundy",
    144: "Ivy",
    148: "Olive",
    152: "Gold",
    153: "Gold",       # Variant found in Preload setlists
    156: "Cacao",
    157: "Cacao",      # Variant found in Preload setlists
    160: "Indigo",
    164: "Navy",
    165: "Navy",       # Variant found in Preload setlists
    168: "Rose",
    172: "Lavender",
    174: "Lavender",   # Variant found in Preload setlists
    176: "Azure",
    180: "Denim",
    181: "Denim",      # Variant found in Preload setlists
    184: "Silver",
    188: "Slate",
    196: "Charcoal",
}

# Reverse mapping for writing (all 16 colors)
SLOT_COLOR_VALUES = {
    "Default": 0,
    "Brick": 136,
    "Burgundy": 140,
    "Ivy": 144,
    "Olive": 148,
    "Gold": 152,
    "Cacao": 156,
    "Indigo": 160,
    "Navy": 164,
    "Rose": 168,
    "Lavender": 172,
    "Azure": 176,
    "Denim": 180,
    "Silver": 184,
    "Slate": 188,
    "Charcoal": 196,
}

# Official Kronos color list (alphabetical for reference)
OFFICIAL_KRONOS_COLORS = [
    "Azure", "Brick", "Burgundy", "Cacao", "Charcoal", "Default", "Denim", "Gold",
    "Indigo", "Ivy", "Lavender", "Navy", "Olive", "Rose", "Silver", "Slate"
]


@dataclass
class PcgHeader:
    """PCG file header information."""
    magic: bytes  # Should be b'KORG'
    product_id: int
    file_type: int
    major_version: int
    minor_version: int
    model: WorkstationModel
    os_version: Optional[str] = None


@dataclass
class Category:
    """Patch category information."""
    main_category: int
    sub_category: int
    name: str = ""
    sub_name: str = ""


@dataclass
class Program:
    """Program patch data."""
    bank: str
    index: int
    name: str
    category: Optional[Category] = None
    favorite: bool = False
    engine: str = ""  # Engine type (HD-1, AL-1, CX-3, STR-1, EP-1, etc.)
    raw_data: bytes = b''
    
    @property
    def id(self) -> str:
        """Return program ID like 'I-A000'."""
        return f"{self.bank}{self.index:03d}"


@dataclass
class Timbre:
    """Timbre within a combi."""
    program_bank: str
    program_index: int
    midi_channel: int
    status: str
    volume: int = 127
    pan: int = 64
    mute: bool = False
    
    @property
    def program_id(self) -> str:
        """Return referenced program ID."""
        return f"{self.program_bank}{self.program_index:03d}"


@dataclass
class Combi:
    """Combination patch data."""
    bank: str
    index: int
    name: str
    category: Optional[Category] = None
    favorite: bool = False
    timbres: List[Timbre] = field(default_factory=list)
    raw_data: bytes = b''
    
    @property
    def id(self) -> str:
        """Return combi ID like 'I-A000'."""
        return f"{self.bank}{self.index:03d}"


@dataclass
class SetListSlot:
    """Set list slot data."""
    set_list_index: int
    slot_index: int
    name: str
    _description: str = ""  # Internal storage
    notes: str = ""  # User notes for the slot
    patch_type: str = ""  # "Program" or "Combi"
    patch_bank: str = ""
    patch_index: int = 0
    _transpose: int = 0  # Internal storage
    volume: int = 127
    hold: bool = False
    color: int = 0  # Color value (byte from STL1/SBK1 at +24)
    raw_data: Optional[bytearray] = None  # Raw slot data for bit-level operations
    _text_size: int = 2  # Internal storage, default to M (2)
    
    @property
    def id(self) -> str:
        """Return slot ID like 'SL0-000'."""
        return f"SL{self.set_list_index}-{self.slot_index:03d}"
    
    @property
    def patch_id(self) -> str:
        """Return referenced patch ID."""
        if self.patch_bank and self.patch_type:
            return f"{self.patch_bank}{self.patch_index:03d}"
        return "None"
    
    @property
    def color_name(self) -> str:
        """Return human-readable color name."""
        return SLOT_COLORS.get(self.color, f"Unknown({self.color})")
    
    @property
    def text_size(self) -> SlotTextSize:
        """Get text size from split bit fields.
        
        Text size is stored as 3 bits split across two bytes:
        - MSB (1 bit): Byte +29, bit 4
        - LSB (2 bits): Byte +24, bits 7-6
        
        Returns:
            SlotTextSize enum value
        """
        if self.raw_data and len(self.raw_data) >= 30:
            from .bit_utils import get_bits
            # MSB (1 bit): Byte +29, bit 4
            msb = get_bits(self.raw_data, 29, 4, 4)
            # LSB (2 bits): Byte +24, bits 7-6
            lsb = get_bits(self.raw_data, 24, 7, 6)
            value = (msb << 2) | lsb
            try:
                return SlotTextSize(value)
            except ValueError:
                return SlotTextSize.M  # Default to Medium
        return SlotTextSize(self._text_size)
    
    @text_size.setter
    def text_size(self, size: SlotTextSize) -> None:
        """Set text size in split bit fields.
        
        Args:
            size: SlotTextSize enum value
        """
        self._text_size = size.value
        if self.raw_data and len(self.raw_data) >= 30:
            from .bit_utils import set_bits
            value = size.value
            # MSB (1 bit) -> byte +29, bit 4
            set_bits(self.raw_data, 29, 4, 4, (value >> 2) & 0x01)
            # LSB (2 bits) -> byte +24, bits 7-6
            set_bits(self.raw_data, 24, 7, 6, value & 0x03)
    
    @property
    def text_size_name(self) -> str:
        """Return human-readable text size name."""
        return self.text_size.name
    
    @property
    def patch_type_value(self) -> int:
        """Get patch type from raw data.
        
        Patch type is stored at byte +24, bits 1-0:
        - 0 = Program
        - 1 = Combi
        - 2 = Song
        
        Returns:
            Patch type value (0-2)
        """
        if self.raw_data and len(self.raw_data) >= 25:
            from .bit_utils import get_bits
            return get_bits(self.raw_data, 24, 1, 0)
        # Map string to value
        type_map = {'Program': 0, 'Combi': 1, 'Song': 2}
        return type_map.get(self.patch_type, 0)
    
    @patch_type_value.setter
    def patch_type_value(self, value: int) -> None:
        """Set patch type in raw data.
        
        Args:
            value: Patch type value (0=Program, 1=Combi, 2=Song)
        """
        value_map = {0: 'Program', 1: 'Combi', 2: 'Song'}
        self.patch_type = value_map.get(value, 'Program')
        
        if self.raw_data and len(self.raw_data) >= 25:
            from .bit_utils import set_bits
            set_bits(self.raw_data, 24, 1, 0, value & 0x03)
    
    @property
    def patch_bank_id(self) -> int:
        """Get referenced bank ID from raw data.
        
        Bank ID is stored at byte +25, bits 4-0 (lower 5 bits).
        Bits 7-5 are used by transpose MSB.
        
        Returns:
            Bank ID (0-31)
        """
        if self.raw_data and len(self.raw_data) >= 26:
            from .bit_utils import get_bits
            return get_bits(self.raw_data, 25, 4, 0)
        return 0
    
    @patch_bank_id.setter
    def patch_bank_id(self, value: int) -> None:
        """Set referenced bank ID in raw data.
        
        Args:
            value: Bank ID (0-31)
        """
        if self.raw_data and len(self.raw_data) >= 26:
            from .bit_utils import set_bits
            set_bits(self.raw_data, 25, 4, 0, value & 0x1F)
    
    @property
    def patch_index_value(self) -> int:
        """Get referenced patch index from raw data.
        
        Patch index is stored at byte +26.
        
        Returns:
            Patch index (0-127)
        """
        if self.raw_data and len(self.raw_data) >= 27:
            return self.raw_data[26]
        return self.patch_index
    
    @patch_index_value.setter
    def patch_index_value(self, value: int) -> None:
        """Set referenced patch index in raw data.
        
        Args:
            value: Patch index (0-127)
        """
        self.patch_index = value & 0x7F
        if self.raw_data and len(self.raw_data) >= 27:
            self.raw_data[26] = value & 0x7F
    
    @property
    def transpose(self) -> int:
        """Get transpose from split bit fields (signed 6-bit).
        
        Transpose is stored as 6 bits split across two bytes:
        - MSB (3 bits): Byte +25, bits 7-5
        - LSB (3 bits): Byte +29, bits 7-5
        Range: -24 to +24 semitones
        
        Returns:
            Transpose value in semitones
        """
        if self.raw_data and len(self.raw_data) >= 30:
            from .bit_utils import get_bits, to_signed_bit
            # MSB (3 bits): Byte +25, bits 7-5
            msb = get_bits(self.raw_data, 25, 7, 5)
            # LSB (3 bits): Byte +29, bits 7-5
            lsb = get_bits(self.raw_data, 29, 7, 5)
            unsigned = (msb << 3) | lsb
            # Convert to signed 6-bit value
            return to_signed_bit(6, unsigned)
        return self._transpose
    
    @transpose.setter
    def transpose(self, value: int) -> None:
        """Set transpose in split bit fields (signed 6-bit).
        
        Args:
            value: Transpose in semitones (-24 to +24)
        """
        # Clamp to valid range
        value = max(-24, min(24, value))
        self._transpose = value
        
        if self.raw_data and len(self.raw_data) >= 30:
            from .bit_utils import set_bits, from_signed_bit
            # Convert to unsigned 6-bit
            unsigned = from_signed_bit(6, value)
            # MSB (3 bits) -> byte +25, bits 7-5
            set_bits(self.raw_data, 25, 7, 5, (unsigned >> 3) & 0x07)
            # LSB (3 bits) -> byte +29, bits 7-5
            set_bits(self.raw_data, 29, 7, 5, unsigned & 0x07)
    
    @property
    def description(self) -> str:
        """Get description from raw data.
        
        Description is stored at byte +30, max 512 characters.
        Supports multi-line text with \\r\\n.
        
        Returns:
            Description string
        """
        if self.raw_data and len(self.raw_data) >= 542:  # 30 + 512
            # Read description bytes
            desc_bytes = bytes(self.raw_data[30:542])
            # Find null terminator
            null_pos = desc_bytes.find(b'\x00')
            if null_pos >= 0:
                desc_bytes = desc_bytes[:null_pos]
            # Decode to string
            try:
                return desc_bytes.decode('ascii', errors='ignore')
            except:
                return ""
        return self._description
    
    @description.setter
    def description(self, value: str) -> None:
        """Set description in raw data.
        
        Args:
            value: Description string (max 512 characters)
        """
        # Truncate to 512 chars
        value = value[:512]
        self._description = value
        
        if self.raw_data and len(self.raw_data) >= 542:
            # Convert to bytes
            desc_bytes = value.encode('ascii', errors='ignore')
            # Pad with nulls to 512 bytes
            desc_bytes = desc_bytes.ljust(512, b'\x00')
            # Write to raw data
            self.raw_data[30:542] = desc_bytes


@dataclass
class SetList:
    """Set list containing slots."""
    index: int
    name: str
    description: str = ""
    color: int = 0
    slots: List[SetListSlot] = field(default_factory=list)
    
    @property
    def id(self) -> str:
        """Return set list ID like 'SL0'."""
        return f"SL{self.index}"


@dataclass
class Bank:
    """Bank containing patches."""
    bank_id: str
    bank_type: str  # 'Program', 'Combi', 'SetList'
    patches: List = field(default_factory=list)
    
    def __len__(self):
        return len(self.patches)


@dataclass
class PcgFile:
    """Complete PCG file structure."""
    header: PcgHeader
    program_banks: List[Bank] = field(default_factory=list)
    combi_banks: List[Bank] = field(default_factory=list)
    set_lists: List[SetList] = field(default_factory=list)
    has_global: bool = False
    has_set_lists: bool = False
    raw_data: bytes = b''
    is_dirty: bool = False
    _reference_tracker: Optional[object] = field(default=None, init=False, repr=False)
    
    def get_all_programs(self) -> List[Program]:
        """Get all programs from all banks."""
        programs = []
        for bank in self.program_banks:
            programs.extend(bank.patches)
        return programs
    
    def get_all_combis(self) -> List[Combi]:
        """Get all combis from all banks."""
        combis = []
        for bank in self.combi_banks:
            combis.extend(bank.patches)
        return combis
    
    def find_program(self, bank: str, index: int) -> Optional[Program]:
        """Find a program by bank and index."""
        for prog_bank in self.program_banks:
            if prog_bank.bank_id == bank:
                if 0 <= index < len(prog_bank.patches):
                    return prog_bank.patches[index]
        return None
    
    def find_combi(self, bank: str, index: int) -> Optional[Combi]:
        """Find a combi by bank and index."""
        for combi_bank in self.combi_banks:
            if combi_bank.bank_id == bank:
                if 0 <= index < len(combi_bank.patches):
                    return combi_bank.patches[index]
        return None
    
    def get_reference_tracker(self):
        """Get the reference tracker, creating it if needed."""
        if self._reference_tracker is None:
            from .reference_tracker import ReferenceTracker
            self._reference_tracker = ReferenceTracker(self)
        return self._reference_tracker
    
    def refresh_references(self):
        """Refresh the reference tracker."""
        if self._reference_tracker is not None:
            self._reference_tracker.refresh()
    
    def get_program_usage(self, program_id: str) -> List[str]:
        """Get list of combi IDs that use this program."""
        return self.get_reference_tracker().get_program_usage(program_id)
    
    def get_combi_programs(self, combi_id: str) -> set:
        """Get set of program IDs used by this combi."""
        return self.get_reference_tracker().get_combi_programs(combi_id)
    
    def is_program_used(self, program_id: str) -> bool:
        """Check if a program is used by any combi."""
        return self.get_reference_tracker().is_program_used(program_id)
