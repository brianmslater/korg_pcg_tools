"""Advanced clipboard with program reference tracking and remapping."""

from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass
import copy
from .models import Program, Combi, PcgFile
from .reference_tracker import ReferenceTracker, ProgramRemapper
from .copy_paste_dialog import CopyPasteSettings, get_copy_paste_settings


@dataclass
class ClipboardItem:
    """An item in the clipboard."""
    type: str  # "program" or "combi"
    patch: object  # Program or Combi
    source_file: str = ""  # Source file path
    dependencies: List[Program] = None  # Referenced programs (for combis)
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class AdvancedClipboard:
    """Advanced clipboard with reference tracking and remapping."""
    
    def __init__(self):
        self.items: List[ClipboardItem] = []
        self.settings = get_copy_paste_settings()
        self._last_source_file: Optional[str] = None
    
    def copy_programs(self, programs: List[Program], source_file: Optional[str] = None):
        """Copy programs to clipboard."""
        self.clear()
        self._last_source_file = source_file
        
        for program in programs:
            item = ClipboardItem(
                type="program",
                patch=copy.deepcopy(program),
                source_file=source_file or ""
            )
            self.items.append(item)
    
    def copy_combis(self, combis: List[Combi], pcg: PcgFile, source_file: Optional[str] = None):
        """Copy combis to clipboard with optional program dependencies."""
        self.clear()
        self._last_source_file = source_file
        
        # Get reference tracker
        ref_tracker = pcg.get_reference_tracker()
        
        # Collect all referenced programs if enabled
        all_referenced_programs = set()
        if self.settings.copy_with_programs:
            for combi in combis:
                referenced = ref_tracker.get_combi_programs(combi.id)
                all_referenced_programs.update(referenced)
        
        # Find the actual program objects
        program_objects = {}
        if all_referenced_programs:
            for prog_id in all_referenced_programs:
                bank_id = prog_id[:-3]
                index = int(prog_id[-3:])
                program = pcg.find_program(bank_id, index)
                if program:
                    program_objects[prog_id] = program
        
        # Handle duplicate detection
        if self.settings.check_duplicates and program_objects:
            program_objects = self._remove_duplicates(program_objects)
        
        # Copy combis with their dependencies
        for combi in combis:
            # Get dependencies for this combi
            combi_deps = []
            if self.settings.copy_with_programs:
                referenced = ref_tracker.get_combi_programs(combi.id)
                for prog_id in referenced:
                    if prog_id in program_objects:
                        combi_deps.append(copy.deepcopy(program_objects[prog_id]))
            
            item = ClipboardItem(
                type="combi",
                patch=copy.deepcopy(combi),
                source_file=source_file or "",
                dependencies=combi_deps
            )
            self.items.append(item)
    
    def _remove_duplicates(self, programs: Dict[str, Program]) -> Dict[str, Program]:
        """Remove duplicate programs based on settings."""
        if not self.settings.check_duplicates:
            return programs
        
        unique_programs = {}
        seen_signatures = set()
        
        for prog_id, program in programs.items():
            signature = self._get_program_signature(program)
            
            if signature not in seen_signatures:
                unique_programs[prog_id] = program
                seen_signatures.add(signature)
        
        return unique_programs
    
    def _get_program_signature(self, program: Program) -> str:
        """Get a signature for duplicate detection."""
        if self.settings.duplicate_mode == "bytewise":
            return str(hash(program.raw_data))
        elif self.settings.duplicate_mode == "name":
            return program.name.strip().lower()
        elif self.settings.duplicate_mode == "likename":
            # Remove ignored characters
            name = program.name.strip().lower()
            for char in self.settings.ignore_chars_for_duplicate:
                name = name.replace(char, "")
            return name
        else:
            return str(hash(program.raw_data))
    
    def paste_to_bank(self, target_pcg: PcgFile, bank_type: str, bank_id: str, 
                     start_index: int) -> Tuple[int, List[str]]:
        """Paste clipboard contents to a bank with smart remapping.
        
        Returns:
            Tuple of (patches_pasted, warnings)
        """
        if not self.items:
            return 0, ["Clipboard is empty"]
        
        warnings = []
        patches_pasted = 0
        
        # Get target bank
        if bank_type == "programs":
            target_banks = target_pcg.program_banks
        else:
            target_banks = target_pcg.combi_banks
        
        target_bank = None
        for bank in target_banks:
            if bank.bank_id == bank_id:
                target_bank = bank
                break
        
        if not target_bank:
            return 0, [f"Target bank {bank_id} not found"]
        
        # Create remapper for program references
        remapper = ProgramRemapper()
        
        # First pass: paste programs and build remap table
        program_paste_index = start_index
        for item in self.items:
            if item.type == "program":
                if program_paste_index >= len(target_bank.patches):
                    warnings.append("Ran out of space in target bank")
                    break
                
                # Check if we should skip empty slots
                if (self.settings.skip_empty and 
                    target_bank.patches[program_paste_index].name.strip()):
                    program_paste_index += 1
                    continue
                
                # Check if we should overwrite
                if (not self.settings.overwrite_existing and 
                    target_bank.patches[program_paste_index].name.strip()):
                    program_paste_index += 1
                    continue
                
                # Paste the program
                old_id = item.patch.id
                new_program = copy.deepcopy(item.patch)
                new_program.bank = bank_id
                new_program.index = program_paste_index
                
                target_bank.patches[program_paste_index] = new_program
                
                # Add to remap table
                new_id = new_program.id
                remapper.add_mapping(old_id, new_id)
                
                patches_pasted += 1
                program_paste_index += 1
        
        # Second pass: paste combis and their dependencies
        combi_paste_index = start_index
        for item in self.items:
            if item.type == "combi":
                if bank_type != "combis":
                    warnings.append("Cannot paste combis to program bank")
                    continue
                
                if combi_paste_index >= len(target_bank.patches):
                    warnings.append("Ran out of space in target bank")
                    break
                
                # Paste dependencies first
                dep_start_index = self._find_space_for_dependencies(
                    target_pcg, item.dependencies, remapper
                )
                
                if dep_start_index >= 0:
                    self._paste_dependencies(
                        target_pcg, item.dependencies, dep_start_index, remapper
                    )
                
                # Paste the combi with remapped references
                new_combi = copy.deepcopy(item.patch)
                new_combi.bank = bank_id
                new_combi.index = combi_paste_index
                
                # Remap program references if enabled
                if self.settings.remap_references:
                    new_combi = remapper.remap_combi(new_combi)
                
                target_bank.patches[combi_paste_index] = new_combi
                patches_pasted += 1
                combi_paste_index += 1
        
        # Refresh references
        target_pcg.refresh_references()
        
        return patches_pasted, warnings
    
    def _find_space_for_dependencies(self, pcg: PcgFile, dependencies: List[Program], 
                                   remapper: ProgramRemapper) -> int:
        """Find space for dependency programs."""
        if not dependencies:
            return -1
        
        # Look for space in program banks
        for bank in pcg.program_banks:
            for i, patch in enumerate(bank.patches):
                if not patch.name.strip():  # Empty slot
                    # Check if we have enough consecutive slots
                    available = 0
                    for j in range(i, len(bank.patches)):
                        if not bank.patches[j].name.strip():
                            available += 1
                        else:
                            break
                    
                    if available >= len(dependencies):
                        return i
        
        return -1  # No space found
    
    def _paste_dependencies(self, pcg: PcgFile, dependencies: List[Program], 
                          start_index: int, remapper: ProgramRemapper):
        """Paste dependency programs."""
        # Find first program bank with space
        for bank in pcg.program_banks:
            if start_index < len(bank.patches):
                paste_index = start_index
                
                for dep in dependencies:
                    if paste_index >= len(bank.patches):
                        break
                    
                    old_id = dep.id
                    new_program = copy.deepcopy(dep)
                    new_program.bank = bank.bank_id
                    new_program.index = paste_index
                    
                    bank.patches[paste_index] = new_program
                    
                    # Add to remap table
                    new_id = new_program.id
                    remapper.add_mapping(old_id, new_id)
                    
                    paste_index += 1
                
                break
    
    def clear(self):
        """Clear the clipboard."""
        self.items.clear()
    
    def is_empty(self) -> bool:
        """Check if clipboard is empty."""
        return len(self.items) == 0
    
    def get_summary(self) -> str:
        """Get a summary of clipboard contents."""
        if not self.items:
            return "Clipboard is empty"
        
        program_count = sum(1 for item in self.items if item.type == "program")
        combi_count = sum(1 for item in self.items if item.type == "combi")
        
        parts = []
        if program_count:
            parts.append(f"{program_count} program(s)")
        if combi_count:
            parts.append(f"{combi_count} combi(s)")
        
        # Count dependencies
        total_deps = sum(len(item.dependencies) for item in self.items)
        if total_deps:
            parts.append(f"{total_deps} dependency program(s)")
        
        return "Copied: " + ", ".join(parts)


# Global clipboard instance
_advanced_clipboard = None


def get_advanced_clipboard() -> AdvancedClipboard:
    """Get the global advanced clipboard instance."""
    global _advanced_clipboard
    if _advanced_clipboard is None:
        _advanced_clipboard = AdvancedClipboard()
    return _advanced_clipboard
