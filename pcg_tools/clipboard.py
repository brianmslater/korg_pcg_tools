"""Clipboard functionality for copying/pasting patches with program remapping."""

from typing import Optional, List, Dict, Set
from copy import deepcopy
from .models import Combi, Program, Timbre, SetListSlot


class Clipboard:
    """Clipboard for patches with program reference tracking."""
    
    def __init__(self):
        self.combi: Optional[Combi] = None
        self.programs: List[Program] = []
        self.program_map: Dict[str, Program] = {}  # program_id -> Program
        self.slot: Optional[SetListSlot] = None
        self.program: Optional[Program] = None  # Single program for copy/paste
    
    def copy_combi(self, combi: Combi, pcg):
        """Copy a combi and all programs it references.
        
        Args:
            combi: The combi to copy
            pcg: The PCG file to get programs from
        """
        # Deep copy the combi
        self.combi = deepcopy(combi)
        self.programs = []
        self.program_map = {}
        
        # Find all unique programs referenced by timbres
        referenced_program_ids = set()
        for timbre in combi.timbres:
            if timbre.status != "Off":
                referenced_program_ids.add(timbre.program_id)
        
        # Copy all referenced programs
        for bank in pcg.program_banks:
            for program in bank.patches:
                if program.id in referenced_program_ids:
                    prog_copy = deepcopy(program)
                    self.programs.append(prog_copy)
                    self.program_map[program.id] = prog_copy
    
    def paste_combi(self, target_combi: Combi, pcg, remap_programs: bool = True) -> Dict[str, str]:
        """Paste the clipboard combi to a target location.
        
        Args:
            target_combi: The combi to paste into
            pcg: The PCG file to paste programs into
            remap_programs: If True, copy programs and remap references
        
        Returns:
            Dictionary mapping old program IDs to new program IDs
        """
        if not self.combi:
            return {}
        
        program_remap = {}
        
        if remap_programs and self.programs:
            # Find available program slots
            program_remap = self._remap_programs(pcg)
        
        # Copy combi properties
        target_combi.name = self.combi.name
        target_combi.category = deepcopy(self.combi.category) if self.combi.category else None
        target_combi.favorite = self.combi.favorite
        target_combi.tempo = self.combi.tempo
        
        # Copy timbres with remapped program references
        target_combi.timbres = []
        for timbre in self.combi.timbres:
            new_timbre = deepcopy(timbre)
            
            # Remap program reference if needed
            if remap_programs and timbre.program_id in program_remap:
                new_prog_id = program_remap[timbre.program_id]
                # Parse new program ID (e.g., "I-B042" -> bank="I-B", index=42)
                new_timbre.program_bank = new_prog_id[:-3]
                new_timbre.program_index = int(new_prog_id[-3:])
            
            target_combi.timbres.append(new_timbre)
        
        # Copy raw_data
        target_combi.raw_data = deepcopy(self.combi.raw_data)
        
        return program_remap
    
    def _remap_programs(self, pcg) -> Dict[str, str]:
        """Copy programs to available slots and return mapping.
        
        Args:
            pcg: The PCG file to paste programs into
        
        Returns:
            Dictionary mapping old program IDs to new program IDs
        """
        program_remap = {}
        
        # Build a set of existing program IDs
        existing_programs = set()
        for bank in pcg.program_banks:
            for program in bank.patches:
                existing_programs.add(program.id)
        
        # For each program to paste, find an available slot
        for old_program in self.programs:
            old_id = old_program.id
            
            # If program already exists with same name, reuse it
            for bank in pcg.program_banks:
                for program in bank.patches:
                    if program.name == old_program.name and program.id in existing_programs:
                        program_remap[old_id] = program.id
                        break
                if old_id in program_remap:
                    break
            
            # If not found, find first empty slot
            if old_id not in program_remap:
                new_slot = self._find_empty_program_slot(pcg)
                if new_slot:
                    bank_id, index = new_slot
                    # Copy program to new slot
                    for bank in pcg.program_banks:
                        if bank.bank_id == bank_id:
                            if index < len(bank.patches):
                                target_program = bank.patches[index]
                                # Copy all properties
                                target_program.name = old_program.name
                                target_program.category = deepcopy(old_program.category)
                                target_program.favorite = old_program.favorite
                                target_program.engine = old_program.engine
                                target_program.osc_mode = old_program.osc_mode
                                target_program.raw_data = deepcopy(old_program.raw_data)
                                
                                new_id = f"{bank_id}{index:03d}"
                                program_remap[old_id] = new_id
                                existing_programs.add(new_id)
                            break
        
        return program_remap
    
    def _find_empty_program_slot(self, pcg) -> Optional[tuple]:
        """Find first empty program slot.
        
        Returns:
            Tuple of (bank_id, index) or None if no empty slots
        """
        for bank in pcg.program_banks:
            for i, program in enumerate(bank.patches):
                # Consider a program "empty" if it has a generic init name
                if (program.name.startswith("Init") or 
                    program.name.startswith("[Empty") or
                    program.name.strip() == ""):
                    return (bank.bank_id, i)
        
        return None
    
    def copy_slot(self, slot: SetListSlot):
        """Copy a setlist slot.
        
        Args:
            slot: The setlist slot to copy
        """
        self.slot = deepcopy(slot)
    
    def paste_slot(self, target_slot: SetListSlot):
        """Paste the clipboard slot to a target location.
        
        Args:
            target_slot: The slot to paste into
        """
        if not self.slot:
            return
        
        # Copy all properties except the slot position
        target_slot.name = self.slot.name
        target_slot.notes = self.slot.notes
        target_slot.patch_type = self.slot.patch_type
        target_slot.patch_bank = self.slot.patch_bank
        target_slot.patch_index = self.slot.patch_index
        target_slot.transpose = self.slot.transpose
        target_slot.volume = self.slot.volume
        target_slot.hold = self.slot.hold
        target_slot.color = self.slot.color
        target_slot._text_size = self.slot._text_size
        target_slot._description = self.slot._description
        
        # Copy raw_data if available
        if self.slot.raw_data:
            target_slot.raw_data = deepcopy(self.slot.raw_data)
            
            # Update the name in raw_data if it exists
            # Slot names in SLS1 are stored at the beginning of each slot's raw data
            if len(target_slot.raw_data) >= 24:
                name_bytes = target_slot.name.encode('ascii', errors='ignore')[:24]
                name_bytes = name_bytes.ljust(24, b'\x00')
                target_slot.raw_data[0:24] = name_bytes
    
    def has_combi(self) -> bool:
        """Check if clipboard has a combi."""
        return self.combi is not None
    
    def copy_program(self, program: Program):
        """Copy a single program.
        
        Args:
            program: The program to copy
        """
        self.program = deepcopy(program)
    
    def paste_program(self, target_program: Program):
        """Paste the clipboard program to a target location.
        
        Args:
            target_program: The program to paste into
        """
        if not self.program:
            return
        
        # Copy all properties except the program position (bank/index)
        target_program.name = self.program.name
        target_program.category = deepcopy(self.program.category) if self.program.category else None
        target_program.favorite = self.program.favorite
        target_program.engine = self.program.engine
        target_program.osc_mode = self.program.osc_mode
        
        # Copy raw_data
        if self.program.raw_data:
            target_program.raw_data = deepcopy(self.program.raw_data)
    
    def has_combi(self) -> bool:
        """Check if clipboard has a combi."""
        return self.combi is not None
    
    def has_slot(self) -> bool:
        """Check if clipboard has a slot."""
        return self.slot is not None
    
    def has_program(self) -> bool:
        """Check if clipboard has a program."""
        return self.program is not None
    
    def clear(self):
        """Clear the clipboard."""
        self.combi = None
        self.programs = []
        self.program_map = {}
        self.slot = None
        self.program = None


# Global clipboard instance
_clipboard = Clipboard()


def get_clipboard() -> Clipboard:
    """Get the global clipboard instance."""
    return _clipboard
