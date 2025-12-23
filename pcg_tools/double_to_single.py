"""Double to Single Keyboard Setup functionality.

Based on C# DoubleToSingleKeyboardCommands.cs.
Converts dual keyboard setups to single keyboard by duplicating set list slots
and combis with MIDI channel switching.
"""

from typing import Optional, Tuple, List
from copy import deepcopy
from .models import PcgFile, SetList, SetListSlot, Combi, Bank


def uses_midi_channel(combi: Combi, midi_channel: int) -> bool:
    """Check if combi uses a specific MIDI channel.
    
    Based on C# Combi.UsesMidiChannel().
    Note: Only checks "On" and "Int" status, NOT "Both" (per C# implementation).
    
    Args:
        combi: The combi to check
        midi_channel: MIDI channel (1-16)
    
    Returns:
        True if any enabled timbre uses the specified MIDI channel
    """
    for timbre in combi.timbres:
        # Check if timbre is enabled (status is "Int" or "On" - NOT "Both" per C#)
        if timbre.status in ("Int", "On"):
            # MIDI channel is stored as 0-15, but displayed as 1-16
            if timbre.midi_channel == midi_channel - 1:
                return True
    return False


def switch_midi_channels(combi: Combi, main_channel: int, secondary_channel: int) -> None:
    """Switch two MIDI channels in all enabled timbres.
    
    Based on C# Combi.SwitchMidiChannels().
    
    Args:
        combi: The combi to modify
        main_channel: Main MIDI channel (1-16)
        secondary_channel: Secondary MIDI channel (1-16)
    """
    for timbre in combi.timbres:
        # Only switch for enabled timbres
        if timbre.status in ("Int", "On", "Both"):
            if timbre.midi_channel == main_channel - 1:
                timbre.midi_channel = secondary_channel - 1
            elif timbre.midi_channel == secondary_channel - 1:
                timbre.midi_channel = main_channel - 1


def set_name_suffix(slot_or_combi, suffix: str) -> None:
    """Add suffix to name, right-padded to max name length.
    
    Based on C# Patch.SetNameSuffix().
    The suffix is placed at the right edge of the max name length,
    with spaces padding between the original name and suffix.
    
    Args:
        slot_or_combi: SetListSlot or Combi to modify
        suffix: Suffix to add (e.g., "/MC1")
    """
    max_len = 24  # Kronos name length
    current_name = slot_or_combi.name
    
    # Truncate name if needed to fit suffix
    truncated_name = current_name[:min(len(current_name), max_len - len(suffix))]
    
    # Calculate padding needed between name and suffix
    padding_len = max(0, max_len - len(truncated_name) - len(suffix))
    
    # Build new name: truncated_name + padding + suffix
    slot_or_combi.name = truncated_name + (' ' * padding_len) + suffix


class DoubleToSingleResult:
    """Result of double to single keyboard conversion."""
    
    def __init__(self):
        self.success: bool = True
        self.error_message: str = ""
        self.slots_created: int = 0
        self.combis_created: int = 0


def process_double_to_single(
    pcg: PcgFile,
    source_setlist_index: int,
    target_setlist_index: int,
    target_combi_bank_id: str,
    main_midi_channel: int,
    secondary_midi_channel: int
) -> DoubleToSingleResult:
    """Process double to single keyboard conversion.
    
    Based on C# DoubleToSingleKeyboardCommands.Process().
    
    For each non-empty slot in source set list:
    1. Copy slot to target set list with "/MCx" suffix (main channel)
    2. If slot references a combi that uses secondary channel:
       - Copy combi to target bank with "/MCy" suffix
       - Switch MIDI channels in the copied combi
       - Copy slot again with "/MCy" suffix, referencing the new combi
    
    Args:
        pcg: The PCG file
        source_setlist_index: Index of source set list (0-15)
        target_setlist_index: Index of target set list (0-15)
        target_combi_bank_id: Bank ID for new combis (e.g., "U-A")
        main_midi_channel: Main keyboard MIDI channel (1-16)
        secondary_midi_channel: Secondary keyboard MIDI channel (1-16)
    
    Returns:
        DoubleToSingleResult with success status and counts
    """
    result = DoubleToSingleResult()
    
    # Validate inputs
    if not pcg.set_lists:
        result.success = False
        result.error_message = "Set lists not present in file"
        return result
    
    if source_setlist_index < 0 or source_setlist_index >= len(pcg.set_lists):
        result.success = False
        result.error_message = f"Invalid source set list index: {source_setlist_index}"
        return result
    
    if target_setlist_index < 0 or target_setlist_index >= len(pcg.set_lists):
        result.success = False
        result.error_message = f"Invalid target set list index: {target_setlist_index}"
        return result
    
    source_setlist = pcg.set_lists[source_setlist_index]
    target_setlist = pcg.set_lists[target_setlist_index]
    
    # Check target set list is empty
    filled_count = sum(1 for slot in target_setlist.slots if slot.name.strip() and not slot.name.startswith("Init"))
    if filled_count > 0:
        result.success = False
        result.error_message = "Target set list is not empty"
        return result
    
    # Find target combi bank
    target_combi_bank = None
    for bank in pcg.combi_banks:
        if bank.bank_id == target_combi_bank_id:
            target_combi_bank = bank
            break
    
    if target_combi_bank is None:
        result.success = False
        result.error_message = f"Target combi bank {target_combi_bank_id} not found"
        return result
    
    if target_combi_bank.is_read_only:
        result.success = False
        result.error_message = f"Target combi bank {target_combi_bank_id} is read-only"
        return result
    
    # Process slots
    current_target_slot_index = 0
    current_target_combi_index = 0
    
    for source_slot in source_setlist.slots:
        # Skip empty/init slots
        if not source_slot.name.strip() or source_slot.name.startswith("Init"):
            continue
        
        # Check if we have room in target set list
        if current_target_slot_index >= len(target_setlist.slots):
            result.success = False
            result.error_message = "Not enough slots in target set list"
            return result
        
        # Copy slot to target with main channel suffix
        target_slot = target_setlist.slots[current_target_slot_index]
        _copy_slot(source_slot, target_slot)
        set_name_suffix(target_slot, f"/MC{main_midi_channel}")
        current_target_slot_index += 1
        result.slots_created += 1
        
        # If slot references a combi, check for secondary channel usage
        if source_slot.patch_type == "Combi":
            source_combi = _find_combi(pcg, source_slot.patch_bank, source_slot.patch_index)
            
            if source_combi and uses_midi_channel(source_combi, secondary_midi_channel):
                # Need to create secondary combi and slot
                
                # Check room in target combi bank
                if current_target_combi_index >= len(target_combi_bank.patches):
                    result.success = False
                    result.error_message = "Not enough space in target combi bank"
                    return result
                
                # Copy combi with channel switch
                target_combi = target_combi_bank.patches[current_target_combi_index]
                _copy_combi(source_combi, target_combi)
                set_name_suffix(target_combi, f"/MC{secondary_midi_channel}")
                switch_midi_channels(target_combi, main_midi_channel, secondary_midi_channel)
                current_target_combi_index += 1
                result.combis_created += 1
                
                # Check room for secondary slot
                if current_target_slot_index >= len(target_setlist.slots):
                    result.success = False
                    result.error_message = "Not enough slots in target set list"
                    return result
                
                # Copy slot referencing new combi
                secondary_slot = target_setlist.slots[current_target_slot_index]
                _copy_slot(source_slot, secondary_slot)
                set_name_suffix(secondary_slot, f"/MC{secondary_midi_channel}")
                # Update reference to new combi
                secondary_slot.patch_bank = target_combi_bank_id
                secondary_slot.patch_index = current_target_combi_index - 1
                current_target_slot_index += 1
                result.slots_created += 1
    
    return result


def _find_combi(pcg: PcgFile, bank_id: str, index: int) -> Optional[Combi]:
    """Find a combi by bank and index."""
    for bank in pcg.combi_banks:
        if bank.bank_id == bank_id:
            if 0 <= index < len(bank.patches):
                return bank.patches[index]
    return None


def _copy_slot(source: SetListSlot, target: SetListSlot) -> None:
    """Copy slot properties."""
    target.name = source.name
    target._description = source._description
    target.notes = source.notes
    target.patch_type = source.patch_type
    target.patch_bank = source.patch_bank
    target.patch_index = source.patch_index
    target._transpose = source._transpose
    target._volume = source._volume
    target.hold = source.hold
    target.color = source.color
    target._text_size = source._text_size
    
    if source.raw_data:
        target.raw_data = bytearray(source.raw_data)


def _copy_combi(source: Combi, target: Combi) -> None:
    """Copy combi properties."""
    target.name = source.name
    target.category = deepcopy(source.category) if source.category else None
    target.favorite = source.favorite
    target.tempo = source.tempo
    target.timbres = deepcopy(source.timbres)
    
    if source.raw_data:
        target.raw_data = deepcopy(source.raw_data)
