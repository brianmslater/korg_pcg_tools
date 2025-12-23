"""Data models for PCG file structures."""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class OsVersion(Enum):
    """Kronos OS version enum.
    
    Based on C# Models.EOsVersion in Models.cs.
    Different OS versions have different offsets and chunk types.
    """
    KRONOS_10_11 = "1.0/1.1"  # Original Kronos OS
    KRONOS_15_16 = "1.5/1.6"  # Added PBK2/CBK2/STL2 chunks
    KRONOS_2X = "2.x"         # Extended user banks U-AA to U-GG
    KRONOS_3X = "3.x"         # Added Color parameter to setlist slots
    OASYS = "Oasys"           # Korg Oasys
    KROME = "Krome"
    KROME_EX = "Krome EX"
    KROSS = "Kross"
    KROSS_2 = "Kross 2"
    M3_1X = "M3 1.x"
    M3_20 = "M3 2.0"
    M50 = "M50"
    TRITON_EXTREME = "Triton Extreme"
    TRITON_CLASSIC = "Triton Classic/Studio/Rack"
    TRITON_LE = "Triton LE"
    TRITON_KARMA = "Triton Karma"
    UNKNOWN = "Unknown"


class SynthesisType(Enum):
    """Program synthesis type enum.
    
    Based on C# ProgramBank.SynthesisType in ProgramBank.cs.
    Used to categorize programs by their sound engine.
    """
    # Sampled types
    AI = "AI"           # M1 sample engine, Advanced Integrated
    AI2 = "AI2"         # Advanced Integrated 2
    ACCESS = "Access"   # Trinity Sample engine
    HI = "Hi"           # Triton/Karma Sample engine
    EDS = "EDS"         # M3/M50 Sample engine
    EDSI = "EDSi"       # MicroStation Sample engine
    EDSX = "EDSx"       # Krome (EX)/Kross(2) Sample engine
    HD1 = "HD-1"        # Kronos/Oasys Sample engine
    
    # Modeled types
    ANALOG_MODELING = "Analog Modeling"  # MS2000, MicroKorg
    MMT = "MMT"                           # MicroKorg XL (Plus)
    MOSS_Z1 = "MOSS-Z1"                   # Trinity option MOSS-TRI
    RADIAS = "Radias"                     # M3 option
    EXI = "EXi"                           # Oasys/Kronos modeled engine
    
    UNKNOWN = "Unknown"  # Unknown; Used for Oasys/Kronos where synthesis type is dynamic
    
    @classmethod
    def is_modeled(cls, synthesis_type: 'SynthesisType') -> bool:
        """Check if synthesis type is modeled (vs sampled).
        
        Based on C# Program.IsModeled().
        """
        modeled_types = {
            cls.ANALOG_MODELING, cls.MMT, cls.MOSS_Z1, cls.RADIAS, cls.EXI
        }
        return synthesis_type in modeled_types


def format_bank_id_for_display(bank_id: str) -> str:
    """Format bank ID for display to match Kronos hardware.
    
    Converts internal format to Kronos display format:
    - I-A -> INT-A
    - U-A -> USER-A
    - GM -> GM (unchanged)
    - g(1)-g(9), g(d) -> unchanged
    
    Args:
        bank_id: Internal bank ID (e.g., "I-A", "U-A", "GM", "g(1)")
    
    Returns:
        Formatted bank ID for display (e.g., "INT-A", "USER-A", "GM", "g(1)")
    """
    if bank_id.startswith("I-"):
        # Internal banks: I-A -> INT-A
        return "INT-" + bank_id[2:]
    elif bank_id.startswith("U-"):
        # User banks: U-A -> USER-A
        return "USER-" + bank_id[2:]
    else:
        # GM, g(1)-g(9), g(d), and other special banks remain unchanged
        return bank_id


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
    os_version: OsVersion = OsVersion.UNKNOWN


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
    osc_mode: str = ""  # Oscillator mode: Single, Double, Drums, Double Drums, etc.
    raw_data: bytes = b''
    _raw_offset: int = 0  # Track offset in file for writing back
    
    # Name length constant (matches C# MaxNameLength)
    NAME_LENGTH: int = 24
    
    @property
    def id(self) -> str:
        """Return program ID like 'INT-A000'."""
        display_bank = format_bank_id_for_display(self.bank)
        return f"{display_bank}{self.index:03d}"
    
    def calc_crc(self, including_name: bool = True) -> int:
        """Calculate CRC value for patch comparison.
        
        Based on C# Patch.CalcCrc().
        Sums all bytes and returns modulo 65536.
        
        Args:
            including_name: If True, include name bytes in CRC.
                           If False, skip first NAME_LENGTH bytes.
        
        Returns:
            CRC value (0-65535)
        """
        if not self.raw_data:
            return 0
        
        start = 0 if including_name else self.NAME_LENGTH
        value = sum(self.raw_data[start:])
        return value % (1 << 16)
    
    @property
    def byte_offset(self) -> int:
        """Return byte offset in file (for hex export)."""
        return self._raw_offset
    
    @property
    def byte_length(self) -> int:
        """Return byte length of patch data (for hex export)."""
        return len(self.raw_data) if self.raw_data else 0


@dataclass
class Timbre:
    """Timbre within a combi.
    
    Based on C# KronosTimbre.cs and KronosOasysTimbre.cs.
    Timbre size: 188 bytes (TimbresSizeConstant).
    """
    program_bank: str
    program_index: int
    midi_channel: int
    status: str
    volume: int = 127
    pan: int = 64
    mute: bool = False
    priority: bool = False  # Priority flag (offset +35, bit 4)
    bend_range: int = 0  # Bend range in semitones (offset +6, signed, -24 to +24)
    detune: int = 0  # Detune in cents (offset +8, 2 bytes, signed, -1200 to +1200)
    transpose: int = 0  # Transpose in semitones (offset +7, signed, -24 to +24)
    portamento: int = 0  # Portamento (offset +36, signed, -128 to +127)
    osc_mode: str = "Prg"  # Oscillator mode: Prg, Poly, Mono, Legato (offset +35, bits 1-0)
    osc_select: str = "Both"  # Oscillator select: Both, Osc1, Osc2 (offset +35, bits 3-2)
    bottom_key: int = 0  # Bottom key of zone (offset +38, 0-127, C-1 to G9)
    top_key: int = 127  # Top key of zone (offset +37, 0-127, C-1 to G9)
    bottom_velocity: int = 1  # Bottom velocity (offset +41, 1-127)
    top_velocity: int = 127  # Top velocity (offset +40, 1-127)
    
    @property
    def program_id(self) -> str:
        """Return referenced program ID."""
        display_bank = format_bank_id_for_display(self.program_bank)
        return f"{display_bank}{self.program_index:03d}"


@dataclass
class Combi:
    """Combination patch data."""
    bank: str
    index: int
    name: str
    category: Optional[Category] = None
    favorite: bool = False
    tempo: float = 120.0  # Tempo in BPM
    timbres: List[Timbre] = field(default_factory=list)
    raw_data: bytes = b''
    _raw_offset: int = 0  # Track offset in file for writing back
    
    # Name length constant (matches C# MaxNameLength)
    NAME_LENGTH: int = 24
    
    @property
    def id(self) -> str:
        """Return combi ID like 'INT-A000'."""
        display_bank = format_bank_id_for_display(self.bank)
        return f"{display_bank}{self.index:03d}"
    
    def calc_crc(self, including_name: bool = True) -> int:
        """Calculate CRC value for patch comparison.
        
        Based on C# Patch.CalcCrc().
        Sums all bytes and returns modulo 65536.
        
        Args:
            including_name: If True, include name bytes in CRC.
                           If False, skip first NAME_LENGTH bytes.
        
        Returns:
            CRC value (0-65535)
        """
        if not self.raw_data:
            return 0
        
        start = 0 if including_name else self.NAME_LENGTH
        value = sum(self.raw_data[start:])
        return value % (1 << 16)
    
    @property
    def byte_offset(self) -> int:
        """Return byte offset in file (for hex export)."""
        return self._raw_offset
    
    @property
    def byte_length(self) -> int:
        """Return byte length of patch data (for hex export)."""
        return len(self.raw_data) if self.raw_data else 0


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
    _volume: int = 127  # Internal storage
    hold: bool = False
    color: int = 0  # Color value (byte from STL1/SBK1 at +24)
    raw_data: Optional[bytearray] = None  # Raw slot data for bit-level operations
    _text_size: int = 2  # Internal storage, default to M (2)
    _raw_offset: int = 0  # Track offset in file for hex export
    
    @property
    def id(self) -> str:
        """Return slot ID like 'SL0-000'."""
        return f"SL{self.set_list_index}-{self.slot_index:03d}"
    
    @property
    def patch_id(self) -> str:
        """Return referenced patch ID."""
        if self.patch_bank and self.patch_type:
            display_bank = format_bank_id_for_display(self.patch_bank)
            return f"{display_bank}{self.patch_index:03d}"
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
    def volume(self) -> int:
        """Get volume from raw data.
        
        Volume is stored at byte +28.
        Range: 0-127
        
        Returns:
            Volume value
        """
        if self.raw_data and len(self.raw_data) >= 29:
            return self.raw_data[28]
        return self._volume
    
    @volume.setter
    def volume(self, value: int) -> None:
        """Set volume in raw data.
        
        Args:
            value: Volume (0-127)
        """
        value = max(0, min(127, value))
        self._volume = value
        if self.raw_data and len(self.raw_data) >= 29:
            self.raw_data[28] = value
    
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
    
    @property
    def byte_offset(self) -> int:
        """Return byte offset in file (for hex export)."""
        return self._raw_offset
    
    @property
    def byte_length(self) -> int:
        """Return byte length of slot data (for hex export)."""
        return len(self.raw_data) if self.raw_data else 0


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
    is_placeholder: bool = False  # True for unimplemented banks (g(1)-g(9), g(d))
    is_read_only: bool = False  # True for ROM banks (GM, g(1)-g(9), g(d))
    
    def __len__(self):
        return len(self.patches)
    
    @property
    def is_filled(self) -> bool:
        """Check if bank has any non-empty patches.
        
        Based on C# IsFilled property.
        """
        if not self.patches:
            return False
        for patch in self.patches:
            # Check if patch has a non-empty name
            if hasattr(patch, 'name') and patch.name:
                name = patch.name.strip()
                if name and not name.startswith("Init") and not name.startswith("[Empty"):
                    return True
        return False


@dataclass
class PcgFile:
    """Complete PCG file structure."""
    header: PcgHeader
    program_banks: List[Bank] = field(default_factory=list)
    combi_banks: List[Bank] = field(default_factory=list)
    set_lists: List[SetList] = field(default_factory=list)
    drum_kit_banks: List['DrumKitBank'] = field(default_factory=list)
    wave_sequence_banks: List['WaveSequenceBank'] = field(default_factory=list)
    has_global: bool = False
    has_set_lists: bool = False
    has_drum_kits: bool = False
    has_wave_sequences: bool = False
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
    
    def get_program_bank(self, bank_id: str) -> Optional[Bank]:
        """Get a program bank by ID."""
        for bank in self.program_banks:
            if bank.bank_id == bank_id:
                return bank
        return None
    
    def get_combi_bank(self, bank_id: str) -> Optional[Bank]:
        """Get a combi bank by ID."""
        for bank in self.combi_banks:
            if bank.bank_id == bank_id:
                return bank
        return None
    
    def has_program_bank(self, bank_id: str) -> bool:
        """Check if a program bank exists."""
        return self.get_program_bank(bank_id) is not None
    
    def has_combi_bank(self, bank_id: str) -> bool:
        """Check if a combi bank exists."""
        return self.get_combi_bank(bank_id) is not None
    
    def get_available_user_banks(self, bank_type: str = 'Program') -> List[str]:
        """Get list of user bank IDs that exist in this file.
        
        Args:
            bank_type: 'Program' or 'Combi'
        
        Returns:
            List of bank IDs like ['U-A', 'U-B', 'U-AA']
        """
        banks = self.program_banks if bank_type == 'Program' else self.combi_banks
        return [b.bank_id for b in banks if b.bank_id.startswith('U-')]
    
    def get_all_bank_ids(self, bank_type: str = 'Program') -> List[str]:
        """Get list of all bank IDs in this file.
        
        Args:
            bank_type: 'Program' or 'Combi'
        
        Returns:
            List of bank IDs
        """
        banks = self.program_banks if bank_type == 'Program' else self.combi_banks
        return [b.bank_id for b in banks]


# Helper functions for bank ID conversion

def parse_bank_id(display_id: str) -> str:
    """Convert display bank ID to internal format.
    
    Examples:
        INT-A -> I-A
        USER-A -> U-A
        GM -> GM
    """
    if display_id.startswith("INT-"):
        return "I-" + display_id[4:]
    elif display_id.startswith("USER-"):
        return "U-" + display_id[5:]
    return display_id


def get_user_bank_list() -> List[str]:
    """Get list of all possible Kronos user bank IDs.
    
    Returns:
        List of bank IDs: U-A through U-G, U-AA through U-GG
    """
    banks = []
    # Single letter banks: U-A through U-G
    for i in range(7):
        banks.append(f"U-{chr(65 + i)}")
    # Double letter banks: U-AA through U-GG
    for i in range(7):
        letter = chr(65 + i)
        banks.append(f"U-{letter}{letter}")
    return banks


def get_all_program_bank_ids() -> List[str]:
    """Get list of all possible Kronos program bank IDs.
    
    Based on C# KronosProgramBanks.CreateBanks() which creates all banks upfront.
    
    Returns:
        List of bank IDs in order: I-A to I-F, U-A to U-G, U-AA to U-GG
    """
    banks = []
    # Internal banks: I-A through I-F
    for i in range(6):
        banks.append(f"I-{chr(65 + i)}")
    # User banks: U-A through U-G
    for i in range(7):
        banks.append(f"U-{chr(65 + i)}")
    # Extended user banks: U-AA through U-GG
    for i in range(7):
        letter = chr(65 + i)
        banks.append(f"U-{letter}{letter}")
    return banks


def get_all_combi_bank_ids() -> List[str]:
    """Get list of all possible Kronos combi bank IDs.
    
    Based on C# KronosCombiBanks.CreateBanks() which creates all banks upfront.
    
    Returns:
        List of bank IDs in order: I-A to I-G, U-A to U-G
    """
    banks = []
    # Internal banks: I-A through I-G
    for i in range(7):
        banks.append(f"I-{chr(65 + i)}")
    # User banks: U-A through U-G
    for i in range(7):
        banks.append(f"U-{chr(65 + i)}")
    return banks



@dataclass
class DrumKit:
    """Drum kit data.
    
    Based on C# DrumKit.cs and KronosDrumKit.cs.
    """
    bank: str
    index: int
    name: str
    raw_data: bytes = b''
    _raw_offset: int = 0
    
    @property
    def id(self) -> str:
        """Return drum kit ID like 'INT-A000'."""
        display_bank = format_bank_id_for_display(self.bank)
        return f"{display_bank}{self.index:03d}"


@dataclass
class DrumKitBank:
    """Drum kit bank container.
    
    Based on C# DrumKitBank.cs.
    """
    bank_id: str
    drum_kits: List[DrumKit] = field(default_factory=list)
    byte_offset: int = 0
    patch_size: int = 0
    is_writable: bool = True
    is_loaded: bool = False


@dataclass
class WaveSequence:
    """Wave sequence data.
    
    Based on C# WaveSequence.cs and KronosWaveSequence.cs.
    """
    bank: str
    index: int
    name: str
    raw_data: bytes = b''
    _raw_offset: int = 0
    
    @property
    def id(self) -> str:
        """Return wave sequence ID like 'INT-A000'."""
        display_bank = format_bank_id_for_display(self.bank)
        return f"{display_bank}{self.index:03d}"


@dataclass
class WaveSequenceBank:
    """Wave sequence bank container.
    
    Based on C# WaveSequenceBank.cs.
    """
    bank_id: str
    wave_sequences: List[WaveSequence] = field(default_factory=list)
    byte_offset: int = 0
    patch_size: int = 0
    is_writable: bool = True
    is_loaded: bool = False
