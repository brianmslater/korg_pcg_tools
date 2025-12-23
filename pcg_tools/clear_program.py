"""
Assigned Clear Program functionality.

Based on C# implementation:
- Model/Common/Synth/MemoryAndFactory/PcgMemory.cs - AssignedClearProgram property
- Model/Common/Synth/PatchCombis/Timbre.cs - Clear() method

The Assigned Clear Program is the program that gets assigned to timbres
when they are cleared. By default, it's the first program in the first bank.
Users can set a custom program to use when clearing timbres.
"""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .models import PcgFile, Program, Timbre


class ClearProgramManager:
    """
    Manages the assigned clear program for a PCG file.
    
    Based on C# PcgMemory.AssignedClearProgram.
    """
    
    def __init__(self, pcg: 'PcgFile'):
        self.pcg = pcg
        self._assigned_clear_program: Optional['Program'] = None
        
        # Initialize to first program in first bank (default behavior)
        self._initialize_default()
    
    def _initialize_default(self) -> None:
        """Initialize the assigned clear program to the default (first program)."""
        if self.pcg.program_banks and len(self.pcg.program_banks) > 0:
            first_bank = self.pcg.program_banks[0]
            if first_bank.patches and len(first_bank.patches) > 0:
                self._assigned_clear_program = first_bank.patches[0]
    
    @property
    def assigned_clear_program(self) -> Optional['Program']:
        """Get the currently assigned clear program."""
        return self._assigned_clear_program
    
    @assigned_clear_program.setter
    def assigned_clear_program(self, program: Optional['Program']) -> None:
        """Set the assigned clear program."""
        self._assigned_clear_program = program
    
    def get_clear_program(self) -> Optional['Program']:
        """
        Get the program to use when clearing timbres.
        
        Returns the assigned clear program if set, otherwise returns
        the first program in the first bank.
        
        Returns:
            The program to use for clearing, or None if no programs exist
        """
        if self._assigned_clear_program is not None:
            return self._assigned_clear_program
        
        # Fall back to first program in first bank
        if self.pcg.program_banks and len(self.pcg.program_banks) > 0:
            first_bank = self.pcg.program_banks[0]
            if first_bank.patches and len(first_bank.patches) > 0:
                return first_bank.patches[0]
        
        return None
    
    def get_clear_program_display(self) -> str:
        """
        Get a display string for the assigned clear program.
        
        Based on C# CombiViewModel.AssignedClearProgram property.
        
        Returns:
            String like "INT-A000 Piano" or "None" if no program
        """
        program = self.get_clear_program()
        if program:
            return f"{program.id} {program.name}"
        return "None"


def clear_timbre(timbre: 'Timbre', clear_program: Optional['Program']) -> None:
    """
    Clear a timbre by setting it to the clear program.
    
    Based on C# Timbre.Clear().
    
    Args:
        timbre: The timbre to clear
        clear_program: The program to assign (or None for default)
    """
    if clear_program:
        timbre.program_bank = clear_program.bank
        timbre.program_index = clear_program.index
    else:
        # Default to first bank, first program
        timbre.program_bank = "I-A"
        timbre.program_index = 0
