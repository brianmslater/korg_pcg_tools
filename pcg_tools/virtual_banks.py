"""Virtual Banks support for Kronos.

Based on C# KronosProgramBanks.CreateVirtualBanks() and KronosCombiBanks.CreateVirtualBanks().

Virtual banks are banks that don't exist on the actual hardware but are used
for organizing patches in the software. They allow users to aggregate patches
from multiple banks into virtual collections.

Kronos supports 64 virtual banks (8 groups × 8 banks each):
- V0-A through V0-H (group 0)
- V1-A through V1-H (group 1)
- ...
- V7-A through V7-H (group 7)
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass, field

# Constants from C# ProgramBanks.cs and CombiBanks.cs
FIRST_VIRTUAL_BANK_ID = 0x30
NUMBER_OF_VIRTUAL_BANKS = 64  # 8 groups × 8 banks
VIRTUAL_BANK_GROUPS = 8
BANKS_PER_GROUP = 8
BANK_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']


@dataclass
class VirtualBank:
    """A virtual bank for organizing patches.
    
    Based on C# BankType.EType.Virtual.
    """
    bank_id: str  # e.g., "V0-A", "V3-H"
    pcg_id: int   # Internal ID (0x30 + index)
    group_index: int  # 0-7
    bank_index: int   # 0-7 (A-H)
    patches: List = field(default_factory=list)
    is_loaded: bool = False
    
    @property
    def is_virtual(self) -> bool:
        """Virtual banks are always virtual."""
        return True
    
    @property
    def is_writable(self) -> bool:
        """Virtual banks are writable."""
        return True
    
    @property
    def is_read_only(self) -> bool:
        """Virtual banks are not read-only."""
        return False


def generate_virtual_bank_ids() -> List[Tuple[str, int]]:
    """Generate all virtual bank IDs and their PCG IDs.
    
    Returns:
        List of (bank_id, pcg_id) tuples for all 64 virtual banks.
    """
    banks = []
    for group_index in range(VIRTUAL_BANK_GROUPS):
        for bank_index, bank_name in enumerate(BANK_NAMES):
            bank_id = f"V{group_index}-{bank_name}"
            pcg_id = FIRST_VIRTUAL_BANK_ID + group_index * BANKS_PER_GROUP + bank_index
            banks.append((bank_id, pcg_id))
    return banks


def create_virtual_program_banks() -> List[VirtualBank]:
    """Create all 64 virtual program banks.
    
    Based on C# KronosProgramBanks.CreateVirtualBanks().
    
    Returns:
        List of VirtualBank objects for programs.
    """
    banks = []
    for group_index in range(VIRTUAL_BANK_GROUPS):
        for bank_index, bank_name in enumerate(BANK_NAMES):
            bank_id = f"V{group_index}-{bank_name}"
            pcg_id = FIRST_VIRTUAL_BANK_ID + group_index * BANKS_PER_GROUP + bank_index
            bank = VirtualBank(
                bank_id=bank_id,
                pcg_id=pcg_id,
                group_index=group_index,
                bank_index=bank_index
            )
            banks.append(bank)
    return banks


def create_virtual_combi_banks() -> List[VirtualBank]:
    """Create all 64 virtual combi banks.
    
    Based on C# KronosCombiBanks.CreateVirtualBanks().
    
    Returns:
        List of VirtualBank objects for combis.
    """
    banks = []
    for group_index in range(VIRTUAL_BANK_GROUPS):
        for bank_index, bank_name in enumerate(BANK_NAMES):
            bank_id = f"V{group_index}-{bank_name}"
            # Combi virtual banks use -1 as pcg_id per C# code
            pcg_id = -1
            bank = VirtualBank(
                bank_id=bank_id,
                pcg_id=pcg_id,
                group_index=group_index,
                bank_index=bank_index
            )
            banks.append(bank)
    return banks


def is_virtual_bank_id(bank_id: str) -> bool:
    """Check if a bank ID is a virtual bank.
    
    Args:
        bank_id: Bank ID string (e.g., "V0-A", "I-A", "U-B")
    
    Returns:
        True if the bank ID is a virtual bank.
    """
    if not bank_id or len(bank_id) < 4:
        return False
    return bank_id.startswith('V') and '-' in bank_id


def parse_virtual_bank_id(bank_id: str) -> Optional[Tuple[int, int]]:
    """Parse a virtual bank ID into group and bank indices.
    
    Args:
        bank_id: Virtual bank ID (e.g., "V0-A", "V7-H")
    
    Returns:
        Tuple of (group_index, bank_index) or None if invalid.
    """
    if not is_virtual_bank_id(bank_id):
        return None
    
    try:
        # Format: V<group>-<bank>
        parts = bank_id[1:].split('-')
        if len(parts) != 2:
            return None
        
        group_index = int(parts[0])
        bank_letter = parts[1].upper()
        
        if group_index < 0 or group_index >= VIRTUAL_BANK_GROUPS:
            return None
        
        if bank_letter not in BANK_NAMES:
            return None
        
        bank_index = BANK_NAMES.index(bank_letter)
        return (group_index, bank_index)
    except (ValueError, IndexError):
        return None


def get_virtual_bank_pcg_id(bank_id: str) -> Optional[int]:
    """Get the PCG ID for a virtual bank.
    
    Args:
        bank_id: Virtual bank ID (e.g., "V0-A")
    
    Returns:
        PCG ID or None if invalid.
    """
    parsed = parse_virtual_bank_id(bank_id)
    if parsed is None:
        return None
    
    group_index, bank_index = parsed
    return FIRST_VIRTUAL_BANK_ID + group_index * BANKS_PER_GROUP + bank_index


def pcg_id_to_virtual_bank_id(pcg_id: int) -> Optional[str]:
    """Convert a PCG ID to a virtual bank ID.
    
    Based on C# PcgFileReader.ProgramBankId2ProgramIndex() virtual bank handling.
    
    Args:
        pcg_id: PCG ID (0x30 to 0x6F for virtual banks)
    
    Returns:
        Virtual bank ID string or None if not a virtual bank.
    """
    if pcg_id < FIRST_VIRTUAL_BANK_ID:
        return None
    if pcg_id >= FIRST_VIRTUAL_BANK_ID + NUMBER_OF_VIRTUAL_BANKS:
        return None
    
    index = pcg_id - FIRST_VIRTUAL_BANK_ID
    group_index = index // BANKS_PER_GROUP
    bank_index = index % BANKS_PER_GROUP
    
    return f"V{group_index}-{BANK_NAMES[bank_index]}"


class VirtualBankManager:
    """Manager for virtual banks in a PCG file.
    
    Provides methods to work with virtual banks for organizing patches.
    """
    
    def __init__(self):
        self.program_banks: List[VirtualBank] = []
        self.combi_banks: List[VirtualBank] = []
        self._initialized = False
    
    def initialize(self):
        """Initialize virtual banks."""
        if self._initialized:
            return
        
        self.program_banks = create_virtual_program_banks()
        self.combi_banks = create_virtual_combi_banks()
        self._initialized = True
    
    def get_program_bank(self, bank_id: str) -> Optional[VirtualBank]:
        """Get a virtual program bank by ID."""
        if not self._initialized:
            self.initialize()
        
        for bank in self.program_banks:
            if bank.bank_id == bank_id:
                return bank
        return None
    
    def get_combi_bank(self, bank_id: str) -> Optional[VirtualBank]:
        """Get a virtual combi bank by ID."""
        if not self._initialized:
            self.initialize()
        
        for bank in self.combi_banks:
            if bank.bank_id == bank_id:
                return bank
        return None
    
    def get_all_program_bank_ids(self) -> List[str]:
        """Get all virtual program bank IDs."""
        if not self._initialized:
            self.initialize()
        return [bank.bank_id for bank in self.program_banks]
    
    def get_all_combi_bank_ids(self) -> List[str]:
        """Get all virtual combi bank IDs."""
        if not self._initialized:
            self.initialize()
        return [bank.bank_id for bank in self.combi_banks]
