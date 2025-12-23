"""
MPE (MIDI Polyphonic Expression) combi initialization.

Based on C# implementation:
- Model/Common/Synth/PatchCombis/Combi.cs - InitAsMpe()

MPE initialization sets up a combi for MIDI Polyphonic Expression by:
1. Setting each timbre to a unique MIDI channel (1-16)
2. Copying all parameters from timbre 0 to all other timbres
3. Copying the program reference from timbre 0 to all other timbres
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import Combi, Timbre


def init_combi_as_mpe(combi: 'Combi') -> None:
    """
    Initialize a combi for MPE (MIDI Polyphonic Expression).
    
    Based on C# Combi.InitAsMpe().
    
    Sets each timbre to a unique MIDI channel and copies all parameters
    from timbre 0 to all other timbres.
    
    Args:
        combi: The combi to initialize for MPE
    """
    if not combi.timbres or len(combi.timbres) == 0:
        return
    
    timbre0 = combi.timbres[0]
    
    # Set timbre 0 to MIDI channel 1 (value 0)
    timbre0.midi_channel = 0
    
    # Copy parameters from timbre 0 to all other timbres
    for i, timbre in enumerate(combi.timbres[1:], start=1):
        # Set MIDI channel to match timbre number (1-indexed)
        timbre.midi_channel = i
        
        # Copy program reference
        timbre.program_bank = timbre0.program_bank
        timbre.program_index = timbre0.program_index
        
        # Copy parameters that can be safely copied
        # Based on C# parameterNames array in InitAsMpe()
        timbre.status = timbre0.status
        timbre.mute = timbre0.mute
        timbre.volume = timbre0.volume
        timbre.bottom_key = timbre0.bottom_key
        timbre.top_key = timbre0.top_key
        timbre.bottom_velocity = timbre0.bottom_velocity
        timbre.top_velocity = timbre0.top_velocity
        timbre.osc_mode = timbre0.osc_mode
        timbre.osc_select = timbre0.osc_select
        
        # Note: Transpose, Detune, Portamento, Bend Range are NOT copied
        # because they can have negative values which require special handling
        # (as noted in C# source: "parameters with negative values cannot be set")


def can_init_as_mpe(combi: 'Combi') -> bool:
    """
    Check if a combi can be initialized for MPE.
    
    Args:
        combi: The combi to check
        
    Returns:
        True if the combi has timbres and can be initialized
    """
    return combi is not None and combi.timbres and len(combi.timbres) > 0
