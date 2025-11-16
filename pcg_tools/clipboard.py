"""Clipboard management for copy/paste operations."""

from typing import List, Optional
from .models import Program, Combi, SetListSlot


class Clipboard:
    """Clipboard for patch copy/paste operations."""
    
    def __init__(self):
        self.programs: List[Program] = []
        self.combis: List[Combi] = []
        self.set_list_slots: List[SetListSlot] = []
        self.source_file: Optional[str] = None
        self.operation: str = "copy"  # "copy" or "cut"
        self.referenced_programs: List[Program] = []  # Programs referenced by combis
    
    def clear(self):
        """Clear the clipboard."""
        self.programs = []
        self.combis = []
        self.set_list_slots = []
        self.source_file = None
        self.operation = "copy"
        self.referenced_programs = []
    
    def is_empty(self) -> bool:
        """Check if clipboard is empty."""
        return not (self.programs or self.combis or self.set_list_slots)
    
    def copy_programs(self, programs: List[Program], source_file: str):
        """Copy programs to clipboard."""
        self.clear()
        self.programs = [self._clone_program(p) for p in programs]
        self.source_file = source_file
        self.operation = "copy"
    
    def cut_programs(self, programs: List[Program], source_file: str):
        """Cut programs to clipboard."""
        self.copy_programs(programs, source_file)
        self.operation = "cut"
    
    def copy_combis(self, combis: List[Combi], source_file: str, source_pcg=None, include_programs: bool = True):
        """Copy combis to clipboard, optionally with referenced programs.
        
        Args:
            combis: List of combis to copy
            source_file: Source filename
            source_pcg: Source PcgFile object (optional, for copying referenced programs)
            include_programs: Whether to also copy referenced programs
        """
        self.clear()
        self.combis = [self._clone_combi(c) for c in combis]
        self.source_file = source_file
        self.operation = "copy"
        
        # Copy referenced programs if requested and source_pcg is provided
        if include_programs and source_pcg:
            referenced_prog_keys = set()
            for combi in combis:
                for timbre in combi.timbres:
                    prog_key = (timbre.program_bank, timbre.program_index)
                    referenced_prog_keys.add(prog_key)
            
            # Find and copy the referenced programs
            for bank_id, index in referenced_prog_keys:
                prog = source_pcg.find_program(bank_id, index)
                if prog:
                    self.referenced_programs.append(self._clone_program(prog))
    
    def cut_combis(self, combis: List[Combi], source_file: str, source_pcg=None):
        """Cut combis to clipboard."""
        self.copy_combis(combis, source_file, source_pcg, include_programs=True)
        self.operation = "cut"
    
    def _clone_program(self, program: Program) -> Program:
        """Create a deep copy of a program."""
        return Program(
            bank=program.bank,
            index=program.index,
            name=program.name,
            category=program.category,
            favorite=program.favorite,
            raw_data=program.raw_data
        )
    
    def _clone_combi(self, combi: Combi) -> Combi:
        """Create a deep copy of a combi."""
        return Combi(
            bank=combi.bank,
            index=combi.index,
            name=combi.name,
            category=combi.category,
            favorite=combi.favorite,
            timbres=combi.timbres.copy(),
            raw_data=combi.raw_data
        )
    
    def get_summary(self) -> str:
        """Get a summary of clipboard contents."""
        parts = []
        if self.programs:
            parts.append(f"{len(self.programs)} program(s)")
        if self.combis:
            parts.append(f"{len(self.combis)} combi(s)")
        if self.set_list_slots:
            parts.append(f"{len(self.set_list_slots)} set list slot(s)")
        
        if not parts:
            return "Clipboard empty"
        
        op = "Cut" if self.operation == "cut" else "Copied"
        return f"{op}: {', '.join(parts)}"


# Global clipboard instance
_clipboard = Clipboard()


def get_clipboard() -> Clipboard:
    """Get the global clipboard instance."""
    return _clipboard
