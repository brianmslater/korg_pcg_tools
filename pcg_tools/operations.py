"""Patch operations (move, sort, compact, clear, etc.)."""

from typing import List, Callable
from .models import PcgFile, Program, Combi, Bank, Timbre
from .clipboard import get_clipboard


class PatchOperations:
    """Operations on patches within a PCG file."""
    
    def __init__(self, pcg: PcgFile):
        self.pcg = pcg
        self.clipboard = get_clipboard()
    
    def move_program_up(self, bank_id: str, index: int) -> bool:
        """Move a program up one position."""
        if index <= 0:
            return False
        
        bank = self._find_program_bank(bank_id)
        if not bank or index >= len(bank.patches):
            return False
        
        # Swap with previous
        bank.patches[index], bank.patches[index-1] = bank.patches[index-1], bank.patches[index]
        
        # Update indices
        bank.patches[index].index = index
        bank.patches[index-1].index = index - 1
        
        self.pcg.is_dirty = True
        return True
    
    def move_program_down(self, bank_id: str, index: int) -> bool:
        """Move a program down one position."""
        bank = self._find_program_bank(bank_id)
        if not bank or index >= len(bank.patches) - 1:
            return False
        
        # Swap with next
        bank.patches[index], bank.patches[index+1] = bank.patches[index+1], bank.patches[index]
        
        # Update indices
        bank.patches[index].index = index
        bank.patches[index+1].index = index + 1
        
        self.pcg.is_dirty = True
        return True
    
    def move_combi_up(self, bank_id: str, index: int) -> bool:
        """Move a combi up one position."""
        if index <= 0:
            return False
        
        bank = self._find_combi_bank(bank_id)
        if not bank or index >= len(bank.patches):
            return False
        
        # Swap with previous
        bank.patches[index], bank.patches[index-1] = bank.patches[index-1], bank.patches[index]
        
        # Update indices
        bank.patches[index].index = index
        bank.patches[index-1].index = index - 1
        
        self.pcg.is_dirty = True
        return True
    
    def move_combi_down(self, bank_id: str, index: int) -> bool:
        """Move a combi down one position."""
        bank = self._find_combi_bank(bank_id)
        if not bank or index >= len(bank.patches) - 1:
            return False
        
        # Swap with next
        bank.patches[index], bank.patches[index+1] = bank.patches[index+1], bank.patches[index]
        
        # Update indices
        bank.patches[index].index = index
        bank.patches[index+1].index = index + 1
        
        self.pcg.is_dirty = True
        return True
    
    def sort_programs(self, bank_id: str, key: Callable = None, reverse: bool = False):
        """Sort programs in a bank."""
        bank = self._find_program_bank(bank_id)
        if not bank:
            return
        
        if key is None:
            key = lambda p: p.name
        
        bank.patches.sort(key=key, reverse=reverse)
        
        # Update indices
        for i, patch in enumerate(bank.patches):
            patch.index = i
        
        self.pcg.is_dirty = True
    
    def sort_combis(self, bank_id: str, key: Callable = None, reverse: bool = False):
        """Sort combis in a bank."""
        bank = self._find_combi_bank(bank_id)
        if not bank:
            return
        
        if key is None:
            key = lambda c: c.name
        
        bank.patches.sort(key=key, reverse=reverse)
        
        # Update indices
        for i, patch in enumerate(bank.patches):
            patch.index = i
        
        self.pcg.is_dirty = True
    
    def compact_programs(self, bank_id: str):
        """Move empty programs to the end."""
        bank = self._find_program_bank(bank_id)
        if not bank:
            return
        
        # Separate empty and non-empty
        non_empty = [p for p in bank.patches if not self._is_empty_program(p)]
        empty = [p for p in bank.patches if self._is_empty_program(p)]
        
        # Combine
        bank.patches = non_empty + empty
        
        # Update indices
        for i, patch in enumerate(bank.patches):
            patch.index = i
        
        self.pcg.is_dirty = True
    
    def compact_combis(self, bank_id: str):
        """Move empty combis to the end."""
        bank = self._find_combi_bank(bank_id)
        if not bank:
            return
        
        # Separate empty and non-empty
        non_empty = [c for c in bank.patches if not self._is_empty_combi(c)]
        empty = [c for c in bank.patches if self._is_empty_combi(c)]
        
        # Combine
        bank.patches = non_empty + empty
        
        # Update indices
        for i, patch in enumerate(bank.patches):
            patch.index = i
        
        self.pcg.is_dirty = True
    
    def clear_program(self, bank_id: str, index: int):
        """Clear a program (reset to init)."""
        program = self.pcg.find_program(bank_id, index)
        if program:
            program.name = f"Init Program"
            program.favorite = False
            if program.category:
                program.category.main_category = 0
                program.category.sub_category = 0
            self.pcg.is_dirty = True
    
    def clear_combi(self, bank_id: str, index: int):
        """Clear a combi (reset to init)."""
        combi = self.pcg.find_combi(bank_id, index)
        if combi:
            combi.name = f"Init Combi"
            combi.favorite = False
            if combi.category:
                combi.category.main_category = 0
                combi.category.sub_category = 0
            combi.timbres = []
            self.pcg.is_dirty = True
    
    def paste_programs(self, target_bank_id: str, target_index: int) -> int:
        """Paste programs from clipboard into a bank. Returns number of programs pasted."""
        # Get programs from clipboard
        programs = self.clipboard.programs
        if not programs:
            return 0
        
        bank = self._find_program_bank(target_bank_id)
        if not bank:
            return 0
        
        pasted = 0
        for i, program in enumerate(programs):
            target_idx = target_index + i
            if target_idx >= len(bank.patches):
                break
            
            # Copy program data
            target_prog = bank.patches[target_idx]
            target_prog.name = program.name
            target_prog.category = program.category
            target_prog.favorite = program.favorite
            target_prog.raw_data = program.raw_data
            
            pasted += 1
        
        self.pcg.is_dirty = True
        return pasted
    
    def paste_combis(self, target_bank_id: str, target_index: int) -> int:
        """Paste combis from clipboard into a bank. Returns number of combis pasted.
        
        Also copies all referenced programs and remaps them to empty slots.
        """
        # Get combis from clipboard
        combis = self.clipboard.combis
        if not combis:
            return 0
        
        bank = self._find_combi_bank(target_bank_id)
        if not bank:
            return 0
        
        # Step 1: Collect all unique programs referenced by the combis
        referenced_programs = {}  # {(bank, index): Program}
        for combi in combis:
            for timbre in combi.timbres:
                prog_key = (timbre.program_bank, timbre.program_index)
                if prog_key not in referenced_programs:
                    # Try to find the program in the clipboard source
                    source_prog = self._find_program_in_clipboard_source(timbre.program_bank, timbre.program_index)
                    if source_prog:
                        referenced_programs[prog_key] = source_prog
        
        # Step 2: Find empty program slots and copy referenced programs
        program_remap = {}  # {(old_bank, old_index): (new_bank, new_index)}
        if referenced_programs:
            program_remap = self._copy_programs_to_empty_slots(referenced_programs)
        
        # Step 3: Paste combis and remap timbre references
        pasted = 0
        for i, combi in enumerate(combis):
            target_idx = target_index + i
            if target_idx >= len(bank.patches):
                break
            
            # Copy combi data
            target_combi = bank.patches[target_idx]
            target_combi.name = combi.name
            target_combi.category = combi.category
            target_combi.favorite = combi.favorite
            target_combi.raw_data = combi.raw_data
            
            # Copy and remap timbres
            target_combi.timbres = []
            for timbre in combi.timbres:
                # Create new timbre with remapped program reference
                old_key = (timbre.program_bank, timbre.program_index)
                if old_key in program_remap:
                    new_bank, new_index = program_remap[old_key]
                    new_timbre = Timbre(
                        program_bank=new_bank,
                        program_index=new_index,
                        midi_channel=timbre.midi_channel,
                        status=timbre.status,
                        volume=timbre.volume,
                        pan=timbre.pan,
                        mute=timbre.mute
                    )
                    target_combi.timbres.append(new_timbre)
                else:
                    # Keep original reference if program wasn't found
                    target_combi.timbres.append(timbre)
            
            pasted += 1
        
        self.pcg.is_dirty = True
        return pasted
    
    def _find_program_in_clipboard_source(self, bank_id: str, index: int):
        """Find a program from the clipboard's referenced programs."""
        # First check clipboard's referenced programs
        for prog in self.clipboard.referenced_programs:
            if prog.bank == bank_id and prog.index == index:
                return prog
        
        # Fallback: try to find it in the current file
        return self.pcg.find_program(bank_id, index)
    
    def _copy_programs_to_empty_slots(self, programs_dict: dict) -> dict:
        """Copy programs to empty slots in the destination file.
        
        Args:
            programs_dict: {(bank, index): Program}
            
        Returns:
            Remap dictionary: {(old_bank, old_index): (new_bank, new_index)}
        """
        remap = {}
        
        # Find empty slots in program banks
        for old_key, program in programs_dict.items():
            old_bank, old_index = old_key
            
            # Find first empty slot
            new_location = self._find_empty_program_slot()
            if new_location:
                new_bank_id, new_index = new_location
                
                # Copy program to empty slot
                bank = self._find_program_bank(new_bank_id)
                if bank and new_index < len(bank.patches):
                    target_prog = bank.patches[new_index]
                    target_prog.name = program.name
                    target_prog.category = program.category
                    target_prog.favorite = program.favorite
                    target_prog.raw_data = program.raw_data
                    
                    # Record the remapping
                    remap[old_key] = (new_bank_id, new_index)
        
        return remap
    
    def _find_empty_program_slot(self):
        """Find the first empty program slot in any bank.
        
        Returns:
            Tuple of (bank_id, index) or None if no empty slots found.
        """
        for bank in self.pcg.program_banks:
            for i, program in enumerate(bank.patches):
                if self._is_empty_program(program):
                    return (bank.bank_id, i)
        return None
    
    def _find_program_bank(self, bank_id: str) -> Bank:
        """Find a program bank by ID."""
        for bank in self.pcg.program_banks:
            if bank.bank_id == bank_id:
                return bank
        return None
    
    def _find_combi_bank(self, bank_id: str) -> Bank:
        """Find a combi bank by ID."""
        for bank in self.pcg.combi_banks:
            if bank.bank_id == bank_id:
                return bank
        return None
    
    def _is_empty_program(self, program: Program) -> bool:
        """Check if a program is empty/init."""
        return "init" in program.name.lower() or "empty" in program.name.lower() or not program.name.strip()
    
    def _is_empty_combi(self, combi: Combi) -> bool:
        """Check if a combi is empty/init."""
        return "init" in combi.name.lower() or "empty" in combi.name.lower() or not combi.name.strip()


def clear_setlist_slot(slot) -> None:
    """Clear a setlist slot to default state.
    
    Resets all fields to their default values:
    - Name: "Init Slot"
    - Patch type: Program
    - Bank: I-A (0)
    - Patch index: 0
    - Transpose: 0
    - Volume: 127
    - Text size: M (Medium)
    - Description: empty
    
    Args:
        slot: SetListSlot to clear
    """
    from .models import SlotTextSize
    
    # Clear name (24 bytes)
    if slot.raw_data and len(slot.raw_data) >= 24:
        slot.raw_data[0:24] = b'\x00' * 24
    slot.name = "Init Slot"
    
    # Set to Program type (0)
    slot.patch_type_value = 0
    slot.patch_type = "Program"
    
    # Set to bank I-A (0)
    slot.patch_bank_id = 0
    slot.patch_bank = "I-A"
    
    # Set to patch 0
    slot.patch_index_value = 0
    slot.patch_index = 0
    
    # Reset volume to 127
    slot.volume = 127
    if slot.raw_data and len(slot.raw_data) >= 29:
        slot.raw_data[28] = 0x7F
    
    # Reset transpose to 0
    slot.transpose = 0
    
    # Reset text size to M (Medium)
    slot.text_size = SlotTextSize.M
    
    # Clear description (512 bytes)
    slot.description = ""
    
    # Reset color to default (0)
    slot.color = 0


def swap_setlist_slots(slot1, slot2) -> None:
    """Swap two setlist slots completely.
    
    Exchanges all data between two slots including:
    - Raw data
    - All properties
    
    Args:
        slot1: First SetListSlot
        slot2: Second SetListSlot
    """
    if not slot1.raw_data or not slot2.raw_data:
        return
    
    # Swap raw data
    slot1.raw_data, slot2.raw_data = slot2.raw_data, slot1.raw_data
    
    # Swap indices
    slot1.slot_index, slot2.slot_index = slot2.slot_index, slot1.slot_index


def batch_set_volume(slots: List, volume: int) -> None:
    """Set volume for multiple slots.
    
    Args:
        slots: List of SetListSlot objects
        volume: Volume value (0-127)
    """
    volume = max(0, min(127, volume))
    for slot in slots:
        slot.volume = volume
        if slot.raw_data and len(slot.raw_data) >= 29:
            slot.raw_data[28] = volume


def batch_set_transpose(slots: List, transpose: int) -> None:
    """Set transpose for multiple slots.
    
    Args:
        slots: List of SetListSlot objects
        transpose: Transpose value (-24 to +24)
    """
    for slot in slots:
        slot.transpose = transpose


def batch_set_text_size(slots: List, text_size) -> None:
    """Set text size for multiple slots.
    
    Args:
        slots: List of SetListSlot objects
        text_size: SlotTextSize enum value
    """
    for slot in slots:
        slot.text_size = text_size
