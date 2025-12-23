"""Track program references in combis and set lists.

Reference validation based on C# PCG Tools implementation:
- Timbre.cs: UsedProgramBank returns null if bank doesn't exist
- Timbre.cs: UsedProgram returns null if program index >= bank.Patches.Count
- KronosSetListSlot.cs: UsedPatch returns null if reference is invalid
"""

from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from .models import PcgFile, Program, Combi, Bank, SetListSlot


class ReferenceTracker:
    """Track which programs and combis are referenced.
    
    Tracks:
    - Programs used by combis (in timbres)
    - Programs used by set list slots
    - Combis used by set list slots
    """
    
    def __init__(self, pcg: PcgFile):
        self.pcg = pcg
        self._program_usage_in_combis: Dict[str, List[str]] = {}  # program_id -> [combi_ids]
        self._program_usage_in_slots: Dict[str, List[str]] = {}  # program_id -> [slot_ids]
        self._combi_usage_in_slots: Dict[str, List[str]] = {}  # combi_id -> [slot_ids]
        self._combi_programs: Dict[str, Set[str]] = {}  # combi_id -> {program_ids}
        self._build_references()
    
    def _build_references(self):
        """Build the reference maps."""
        self._program_usage_in_combis.clear()
        self._program_usage_in_slots.clear()
        self._combi_usage_in_slots.clear()
        self._combi_programs.clear()
        
        # Scan all combis for program references
        for bank in self.pcg.combi_banks:
            for combi in bank.patches:
                if not combi.name or combi.name.strip() == "":
                    continue
                
                combi_id = combi.id
                self._combi_programs[combi_id] = set()
                
                # Check each timbre
                for timbre in combi.timbres:
                    # Only count timbres that are ON (status != "OFF")
                    if timbre.status == "Off":
                        continue
                    
                    prog_id = timbre.program_id
                    if prog_id:
                        # Add to combi's program list
                        self._combi_programs[combi_id].add(prog_id)
                        
                        # Add to program's usage list
                        if prog_id not in self._program_usage_in_combis:
                            self._program_usage_in_combis[prog_id] = []
                        self._program_usage_in_combis[prog_id].append(combi_id)
        
        # Scan all set list slots for program/combi references
        for setlist in self.pcg.set_lists:
            for slot in setlist.slots:
                if not slot.patch_bank or not slot.patch_type:
                    continue
                
                slot_id = slot.id if hasattr(slot, 'id') else f"{setlist.name}/{slot.name}"
                patch_id = f"{slot.patch_bank}{slot.patch_index:03d}"
                
                if slot.patch_type == "Program":
                    if patch_id not in self._program_usage_in_slots:
                        self._program_usage_in_slots[patch_id] = []
                    self._program_usage_in_slots[patch_id].append(slot_id)
                elif slot.patch_type == "Combi":
                    if patch_id not in self._combi_usage_in_slots:
                        self._combi_usage_in_slots[patch_id] = []
                    self._combi_usage_in_slots[patch_id].append(slot_id)
    
    def get_program_usage_in_combis(self, program_id: str) -> List[str]:
        """Get list of combi IDs that use this program."""
        return self._program_usage_in_combis.get(program_id, [])
    
    def get_program_usage_in_slots(self, program_id: str) -> List[str]:
        """Get list of slot IDs that reference this program."""
        return self._program_usage_in_slots.get(program_id, [])
    
    def get_combi_usage_in_slots(self, combi_id: str) -> List[str]:
        """Get list of slot IDs that reference this combi."""
        return self._combi_usage_in_slots.get(combi_id, [])
    
    # Legacy method names for compatibility
    def get_program_usage(self, program_id: str) -> List[str]:
        """Get list of combi IDs that use this program (legacy)."""
        return self.get_program_usage_in_combis(program_id)
    
    def get_combi_programs(self, combi_id: str) -> Set[str]:
        """Get set of program IDs used by this combi."""
        return self._combi_programs.get(combi_id, set())
    
    def is_program_used(self, program_id: str) -> bool:
        """Check if a program is used by any combi or slot."""
        return (program_id in self._program_usage_in_combis or 
                program_id in self._program_usage_in_slots)
    
    def is_combi_used(self, combi_id: str) -> bool:
        """Check if a combi is used by any slot."""
        return combi_id in self._combi_usage_in_slots
    
    def get_all_referenced_programs(self, combi_ids: List[str]) -> Set[str]:
        """Get all programs referenced by a list of combis."""
        all_progs = set()
        for combi_id in combi_ids:
            all_progs.update(self.get_combi_programs(combi_id))
        return all_progs
    
    def get_program_reference_count(self, program_id: str) -> int:
        """Get total number of references to this program (combis + slots)."""
        combi_refs = len(self.get_program_usage_in_combis(program_id))
        slot_refs = len(self.get_program_usage_in_slots(program_id))
        return combi_refs + slot_refs
    
    def get_combi_reference_count(self, combi_id: str) -> int:
        """Get total number of references to this combi (slots only)."""
        return len(self.get_combi_usage_in_slots(combi_id))
    
    # Legacy method
    def get_usage_count(self, program_id: str) -> int:
        """Get number of combis using this program (legacy)."""
        return len(self.get_program_usage_in_combis(program_id))
    
    def refresh(self):
        """Rebuild the reference maps."""
        self._build_references()


class ProgramRemapper:
    """Handle program reference remapping when copying/pasting."""
    
    def __init__(self):
        self.remap_table: Dict[str, str] = {}  # old_prog_id -> new_prog_id
    
    def add_mapping(self, old_id: str, new_id: str):
        """Add a program ID mapping."""
        self.remap_table[old_id] = new_id
    
    def get_mapped_id(self, old_id: str) -> str:
        """Get the new ID for an old program ID."""
        return self.remap_table.get(old_id, old_id)
    
    def remap_combi(self, combi: Combi) -> Combi:
        """Remap all program references in a combi."""
        # Create a copy
        new_combi = Combi(
            bank=combi.bank,
            index=combi.index,
            name=combi.name,
            category=combi.category,
            favorite=combi.favorite,
            timbres=combi.timbres.copy(),
            raw_data=combi.raw_data
        )
        
        # Remap each timbre's program reference
        for timbre in new_combi.timbres:
            if timbre.program_id in self.remap_table:
                old_id = timbre.program_id
                new_id = self.remap_table[old_id]
                
                # Parse new bank and index
                new_bank = new_id[:-3]
                new_index = int(new_id[-3:])
                
                timbre.program_bank = new_bank
                timbre.program_index = new_index
                timbre.program_id = new_id
        
        return new_combi
    
    def clear(self):
        """Clear all mappings."""
        self.remap_table.clear()



@dataclass
class InvalidReference:
    """Details about an invalid reference.
    
    Based on C# PCG Tools reference validation patterns.
    """
    source_type: str  # "timbre" or "slot"
    source_id: str  # e.g., "INT-A000/T1" or "SL0-000"
    ref_type: str  # "program" or "combi"
    ref_bank: str  # Referenced bank ID
    ref_index: int  # Referenced patch index
    reason: str  # Why the reference is invalid
    
    def __str__(self) -> str:
        return f"{self.source_type} {self.source_id}: {self.ref_type} {self.ref_bank}{self.ref_index:03d} - {self.reason}"


def validate_timbre_references(combi: Combi, pcg_file: PcgFile, 
                                report_missing_banks: bool = False) -> List[InvalidReference]:
    """Validate that all timbre program references in a combi exist.
    
    Based on C# Timbre.cs UsedProgram/UsedProgramBank logic:
    - Returns invalid if bank doesn't exist (GetBankWithPcgId returns null)
    - Returns invalid if program index >= bank.Patches.Count
    - GM/GM2 banks are always valid (ROM banks)
    - Internal banks (I-A through I-F) may not be in file but exist on hardware
    
    Args:
        combi: The combi to validate
        pcg_file: The PCG file containing the banks
        report_missing_banks: If True, report references to banks not in file.
                             If False (default), only report out-of-range indices.
    
    Returns:
        List of InvalidReference objects for any invalid references
    """
    invalid_refs = []
    
    for i, timbre in enumerate(combi.timbres):
        # Skip OFF timbres - they don't need valid references
        if timbre.status == "Off":
            continue
        
        source_id = f"{combi.id}/T{i+1}"
        ref_bank = timbre.program_bank
        ref_index = timbre.program_index
        
        # Check if bank exists
        bank = pcg_file.get_program_bank(ref_bank)
        
        if bank is None:
            # GM2 banks (g(1)-g(9), g(d)) are ROM banks - always valid
            if ref_bank.startswith('g('):
                continue
            # GM bank is also ROM - always valid
            if ref_bank == 'GM':
                continue
            # Internal banks (I-A through I-F) exist on hardware even if not in file
            if ref_bank.startswith('I-') and not report_missing_banks:
                continue
            
            if report_missing_banks:
                invalid_refs.append(InvalidReference(
                    source_type="timbre",
                    source_id=source_id,
                    ref_type="program",
                    ref_bank=ref_bank,
                    ref_index=ref_index,
                    reason=f"Bank '{ref_bank}' not in file"
                ))
            continue
        
        # Check if program index is valid
        if ref_index >= len(bank.patches):
            invalid_refs.append(InvalidReference(
                source_type="timbre",
                source_id=source_id,
                ref_type="program",
                ref_bank=ref_bank,
                ref_index=ref_index,
                reason=f"Program index {ref_index} out of range (bank has {len(bank.patches)} programs)"
            ))
    
    return invalid_refs


def validate_slot_references(slot: SetListSlot, pcg_file: PcgFile,
                             report_missing_banks: bool = False) -> List[InvalidReference]:
    """Validate that a set list slot's patch reference exists.
    
    Based on C# KronosSetListSlot.cs UsedPatch logic:
    - Returns invalid if bank doesn't exist
    - Returns invalid if patch index >= bank.Patches.Count
    - GM/GM2 banks are always valid for programs
    - Internal banks may not be in file but exist on hardware
    
    Args:
        slot: The set list slot to validate
        pcg_file: The PCG file containing the banks
        report_missing_banks: If True, report references to banks not in file.
                             If False (default), only report out-of-range indices.
    
    Returns:
        List of InvalidReference objects for any invalid references
    """
    invalid_refs = []
    
    # Empty slots don't need validation
    if not slot.patch_bank or not slot.patch_type:
        return invalid_refs
    
    source_id = slot.id
    ref_bank = slot.patch_bank
    ref_index = slot.patch_index
    ref_type = slot.patch_type.lower()  # "program" or "combi"
    
    # Get the appropriate bank
    if ref_type == "program":
        bank = pcg_file.get_program_bank(ref_bank)
        
        # GM2 banks (g(1)-g(9), g(d)) are ROM banks - always valid
        if ref_bank.startswith('g('):
            return invalid_refs
        # GM bank is also ROM - always valid
        if ref_bank == 'GM':
            return invalid_refs
        # Internal banks (I-A through I-F) exist on hardware even if not in file
        if ref_bank.startswith('I-') and bank is None and not report_missing_banks:
            return invalid_refs
    elif ref_type == "combi":
        bank = pcg_file.get_combi_bank(ref_bank)
        # Internal combi banks (I-A through I-G) exist on hardware even if not in file
        if ref_bank.startswith('I-') and bank is None and not report_missing_banks:
            return invalid_refs
    else:
        # Song type - not validated
        return invalid_refs
    
    if bank is None:
        if report_missing_banks:
            invalid_refs.append(InvalidReference(
                source_type="slot",
                source_id=source_id,
                ref_type=ref_type,
                ref_bank=ref_bank,
                ref_index=ref_index,
                reason=f"Bank '{ref_bank}' not in file"
            ))
        return invalid_refs
    
    # Check if patch index is valid
    if ref_index >= len(bank.patches):
        invalid_refs.append(InvalidReference(
            source_type="slot",
            source_id=source_id,
            ref_type=ref_type,
            ref_bank=ref_bank,
            ref_index=ref_index,
            reason=f"{ref_type.capitalize()} index {ref_index} out of range (bank has {len(bank.patches)} patches)"
        ))
    
    return invalid_refs


def validate_all_references(pcg_file: PcgFile, 
                            report_missing_banks: bool = False) -> List[InvalidReference]:
    """Validate all references in a PCG file.
    
    Validates:
    - All timbre references in all combis
    - All slot references in all set lists
    
    Args:
        pcg_file: The PCG file to validate
        report_missing_banks: If True, report references to banks not in file.
                             If False (default), only report out-of-range indices.
    
    Returns:
        List of all InvalidReference objects found
    """
    all_invalid = []
    
    # Validate combi timbre references
    for bank in pcg_file.combi_banks:
        for combi in bank.patches:
            invalid = validate_timbre_references(combi, pcg_file, report_missing_banks)
            all_invalid.extend(invalid)
    
    # Validate set list slot references
    for setlist in pcg_file.set_lists:
        for slot in setlist.slots:
            invalid = validate_slot_references(slot, pcg_file, report_missing_banks)
            all_invalid.extend(invalid)
    
    return all_invalid

