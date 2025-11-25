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
    """Setlist slot text size options."""
    XS = 1   # Extra Small (estimated)
    S = 4    # Small (estimated)
    M = 0    # Medium (confirmed)
    L = 8    # Large (estimated)
    XL = 16  # Extra Large (confirmed)


# Complete Kronos setlist slot colors (all 16 official colors)
# Values confirmed from "SETLIST Movie TV Themes LOAD SEPARATELY 2.PCG" analysis
SLOT_COLORS = {
    0: "Default",
    136: "Brick",
    140: "Burgundy",
    144: "Ivy",
    148: "Olive",
    152: "Gold",
    156: "Cacao",
    160: "Indigo",
    164: "Navy",
    168: "Rose",
    172: "Lavender",
    176: "Azure",
    180: "Denim",
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
    description: str = ""
    notes: str = ""  # User notes for the slot
    patch_type: str = ""  # "Program" or "Combi"
    patch_bank: str = ""
    patch_index: int = 0
    transpose: int = 0
    volume: int = 127
    hold: bool = False
    color: int = 0  # Color value (byte from STL1/SBK1 at +24)
    text_size: int = 0  # Text size value (byte from STL1/SBK1 at +29)
    
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
    def text_size_name(self) -> str:
        """Return human-readable text size name."""
        if self.text_size == 0:
            return "M"
        elif self.text_size == 16:
            return "XL"
        else:
            return f"Unknown({self.text_size})"


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
