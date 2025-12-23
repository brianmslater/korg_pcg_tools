"""Volume change operations for combis and set list slots.

Based on C# implementation:
- ChangeVolumeParameters.cs - Parameter types
- Combi.cs - ChangeVolume() method
- SetListSlot.cs - ChangeVolume() method
- MathUtils.cs - ClipValue() and MapValue() functions
"""

from enum import Enum
from typing import List, Optional, Tuple
from dataclasses import dataclass

from .models import Combi, SetListSlot, Timbre


class VolumeChangeType(Enum):
    """Volume change type matching C# EChangeType."""
    FIXED = "fixed"
    RELATIVE = "relative"
    PERCENTAGE = "percentage"
    MAPPED = "mapped"
    SMART_MAPPED = "smart_mapped"


@dataclass
class VolumeChangeParameters:
    """Parameters for volume change operation.
    
    Based on C# ChangeVolumeParameters class.
    """
    change_type: VolumeChangeType = VolumeChangeType.FIXED
    value: int = 127
    to_value: int = 127  # Only used for mapped types


def clip_value(value: int, min_val: int, max_val: int) -> int:
    """Clip value to range [min_val, max_val].
    
    Based on C# MathUtils.ClipValue().
    """
    return max(min_val, min(value, max_val))


def map_value(value: int, min_source: int, max_source: int, 
              min_dest: int, max_dest: int) -> int:
    """Map value from source range to destination range.
    
    Based on C# MathUtils.MapValue().
    """
    if max_source == min_source:
        return min_dest
    
    result = ((value - min_source) * 
              (max_dest - min_dest) / 
              (max_source - min_source) + min_dest + 0.5)
    return int(result)


def get_timbre_volume(timbre: Timbre) -> int:
    """Get volume from a timbre."""
    return timbre.volume


def set_timbre_volume(timbre: Timbre, volume: int) -> None:
    """Set volume on a timbre."""
    timbre.volume = clip_value(volume, 0, 127)


def is_timbre_active(timbre: Timbre) -> bool:
    """Check if timbre is active (not muted and has active status).
    
    Based on C# Combi.GetMinimumVolume() logic.
    """
    if timbre.mute:
        return False
    # Status values that count as active: Int, On, Both
    return timbre.status in ("Int", "On", "Both")


def get_combi_minimum_volume(combi: Combi) -> int:
    """Get minimum volume of all active timbres in a combi.
    
    Based on C# Combi.GetMinimumVolume().
    """
    min_volume = 127
    for timbre in combi.timbres:
        if is_timbre_active(timbre):
            min_volume = min(min_volume, timbre.volume)
    return min_volume


def get_combi_maximum_volume(combi: Combi) -> int:
    """Get maximum volume of all active timbres in a combi.
    
    Based on C# Combi.GetMaximumVolume().
    """
    max_volume = 0
    for timbre in combi.timbres:
        if is_timbre_active(timbre):
            max_volume = max(max_volume, timbre.volume)
    return max_volume


def change_timbre_volume(timbre: Timbre, params: VolumeChangeParameters,
                         min_value: int = 0, max_value: int = 127) -> None:
    """Change volume of a single timbre.
    
    Based on C# Combi.ChangeVolume() inner loop.
    """
    current = timbre.volume
    
    if params.change_type == VolumeChangeType.FIXED:
        new_volume = params.value
    elif params.change_type == VolumeChangeType.RELATIVE:
        new_volume = clip_value(current + params.value, 0, 127)
    elif params.change_type == VolumeChangeType.PERCENTAGE:
        new_volume = int(current * params.value / 100.0 + 0.5)
    elif params.change_type == VolumeChangeType.MAPPED:
        new_volume = map_value(current, 0, 127, params.value, params.to_value)
    elif params.change_type == VolumeChangeType.SMART_MAPPED:
        new_volume = map_value(current, min_value, max_value, params.value, params.to_value)
    else:
        raise ValueError(f"Unknown change type: {params.change_type}")
    
    timbre.volume = clip_value(new_volume, 0, 127)


def change_combi_volume(combi: Combi, params: VolumeChangeParameters,
                        min_value: int = 0, max_value: int = 127) -> None:
    """Change volume of all timbres in a combi.
    
    Based on C# Combi.ChangeVolume().
    """
    for timbre in combi.timbres:
        change_timbre_volume(timbre, params, min_value, max_value)


def change_slot_volume(slot: SetListSlot, params: VolumeChangeParameters,
                       min_value: int = 0, max_value: int = 127) -> None:
    """Change volume of a set list slot.
    
    Based on C# SetListSlot.ChangeVolume().
    """
    current = slot.volume
    
    if params.change_type == VolumeChangeType.FIXED:
        new_volume = params.value
    elif params.change_type == VolumeChangeType.RELATIVE:
        new_volume = clip_value(current + params.value, 0, 127)
    elif params.change_type == VolumeChangeType.PERCENTAGE:
        new_volume = int(current * params.value / 100.0 + 0.5)
    elif params.change_type == VolumeChangeType.MAPPED:
        new_volume = map_value(current, 0, 127, params.value, params.to_value)
    elif params.change_type == VolumeChangeType.SMART_MAPPED:
        new_volume = map_value(current, min_value, max_value, params.value, params.to_value)
    else:
        raise ValueError(f"Unknown change type: {params.change_type}")
    
    slot.volume = clip_value(new_volume, 0, 127)


def find_volume_range_combis(combis: List[Combi]) -> Tuple[int, int]:
    """Find min/max volume across all combis for smart mapping.
    
    Based on C# PcgViewModel.ChangeVolume() smart mapping logic.
    """
    min_val = 127
    max_val = 0
    
    for combi in combis:
        min_val = min(min_val, get_combi_minimum_volume(combi))
        max_val = max(max_val, get_combi_maximum_volume(combi))
    
    return min_val, max_val


def find_volume_range_slots(slots: List[SetListSlot]) -> Tuple[int, int]:
    """Find min/max volume across all slots for smart mapping.
    
    Based on C# PcgViewModel.ChangeVolume() smart mapping logic.
    """
    min_val = 127
    max_val = 0
    
    for slot in slots:
        min_val = min(min_val, slot.volume)
        max_val = max(max_val, slot.volume)
    
    return min_val, max_val


def change_volumes(combis: Optional[List[Combi]] = None,
                   slots: Optional[List[SetListSlot]] = None,
                   params: Optional[VolumeChangeParameters] = None) -> int:
    """Change volumes for combis and/or slots.
    
    Returns the number of items changed.
    
    Based on C# PcgViewModel.ChangeVolume().
    """
    if params is None:
        params = VolumeChangeParameters()
    
    changed = 0
    
    # Calculate min/max for smart mapping
    min_val = 127
    max_val = 0
    
    if params.change_type == VolumeChangeType.SMART_MAPPED:
        if combis:
            c_min, c_max = find_volume_range_combis(combis)
            min_val = min(min_val, c_min)
            max_val = max(max_val, c_max)
        if slots:
            s_min, s_max = find_volume_range_slots(slots)
            min_val = min(min_val, s_min)
            max_val = max(max_val, s_max)
    
    # Apply changes
    if combis:
        for combi in combis:
            change_combi_volume(combi, params, min_val, max_val)
            changed += 1
    
    if slots:
        for slot in slots:
            change_slot_volume(slot, params, min_val, max_val)
            changed += 1
    
    return changed
