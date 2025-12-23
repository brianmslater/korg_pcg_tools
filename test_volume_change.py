"""Tests for volume change functionality.

Tests the volume change module based on C# implementation:
- ChangeVolumeParameters.cs
- Combi.cs ChangeVolume()
- SetListSlot.cs ChangeVolume()
- MathUtils.cs ClipValue() and MapValue()
"""

import pytest
from pcg_tools.volume_change import (
    VolumeChangeType, VolumeChangeParameters,
    clip_value, map_value,
    get_combi_minimum_volume, get_combi_maximum_volume,
    change_timbre_volume, change_combi_volume, change_slot_volume,
    find_volume_range_combis, find_volume_range_slots,
    change_volumes, is_timbre_active
)
from pcg_tools.models import Combi, Timbre, SetListSlot


class TestMathUtils:
    """Test math utility functions matching C# MathUtils."""
    
    def test_clip_value_within_range(self):
        """Value within range should be unchanged."""
        assert clip_value(50, 0, 127) == 50
        assert clip_value(0, 0, 127) == 0
        assert clip_value(127, 0, 127) == 127
    
    def test_clip_value_below_min(self):
        """Value below min should be clipped to min."""
        assert clip_value(-10, 0, 127) == 0
        assert clip_value(-100, -50, 50) == -50
    
    def test_clip_value_above_max(self):
        """Value above max should be clipped to max."""
        assert clip_value(200, 0, 127) == 127
        assert clip_value(100, -50, 50) == 50
    
    def test_map_value_full_range(self):
        """Map from 0-127 to 0-127 should be identity."""
        assert map_value(0, 0, 127, 0, 127) == 0
        assert map_value(64, 0, 127, 0, 127) == 64
        assert map_value(127, 0, 127, 0, 127) == 127
    
    def test_map_value_compress_range(self):
        """Map from 0-127 to smaller range."""
        # 0-127 -> 0-63 (half)
        assert map_value(0, 0, 127, 0, 63) == 0
        assert map_value(127, 0, 127, 0, 63) == 63
        assert map_value(64, 0, 127, 0, 63) == 32  # Approximately half
    
    def test_map_value_expand_range(self):
        """Map from smaller range to 0-127."""
        # 0-63 -> 0-127 (double)
        assert map_value(0, 0, 63, 0, 127) == 0
        assert map_value(63, 0, 63, 0, 127) == 127
    
    def test_map_value_offset_range(self):
        """Map to offset range."""
        # 0-127 -> 32-96
        assert map_value(0, 0, 127, 32, 96) == 32
        assert map_value(127, 0, 127, 32, 96) == 96
    
    def test_map_value_same_source(self):
        """Map with same source min/max should return min_dest."""
        assert map_value(50, 50, 50, 0, 127) == 0


class TestTimbreActive:
    """Test timbre active status detection."""
    
    def test_active_timbre_int(self):
        """Timbre with status 'Int' is active."""
        timbre = Timbre(
            program_bank="INT-A", program_index=0,
            midi_channel=1, status="Int", volume=100, mute=False
        )
        assert is_timbre_active(timbre) is True
    
    def test_active_timbre_on(self):
        """Timbre with status 'On' is active."""
        timbre = Timbre(
            program_bank="INT-A", program_index=0,
            midi_channel=1, status="On", volume=100, mute=False
        )
        assert is_timbre_active(timbre) is True
    
    def test_active_timbre_both(self):
        """Timbre with status 'Both' is active."""
        timbre = Timbre(
            program_bank="INT-A", program_index=0,
            midi_channel=1, status="Both", volume=100, mute=False
        )
        assert is_timbre_active(timbre) is True
    
    def test_inactive_timbre_off(self):
        """Timbre with status 'Off' is inactive."""
        timbre = Timbre(
            program_bank="INT-A", program_index=0,
            midi_channel=1, status="Off", volume=100, mute=False
        )
        assert is_timbre_active(timbre) is False
    
    def test_inactive_timbre_muted(self):
        """Muted timbre is inactive."""
        timbre = Timbre(
            program_bank="INT-A", program_index=0,
            midi_channel=1, status="Int", volume=100, mute=True
        )
        assert is_timbre_active(timbre) is False


class TestCombiVolumeRange:
    """Test combi min/max volume detection."""
    
    def _create_combi_with_timbres(self, volumes, statuses=None, mutes=None):
        """Helper to create a combi with timbres."""
        if statuses is None:
            statuses = ["Int"] * len(volumes)
        if mutes is None:
            mutes = [False] * len(volumes)
        
        timbres = []
        for i, (vol, status, mute) in enumerate(zip(volumes, statuses, mutes)):
            timbres.append(Timbre(
                program_bank="INT-A", program_index=i,
                midi_channel=i+1, status=status, volume=vol, mute=mute
            ))
        
        return Combi(bank="INT-A", index=0, name="Test", timbres=timbres)
    
    def test_min_volume_all_active(self):
        """Get minimum volume from all active timbres."""
        combi = self._create_combi_with_timbres([100, 50, 75, 25])
        assert get_combi_minimum_volume(combi) == 25
    
    def test_max_volume_all_active(self):
        """Get maximum volume from all active timbres."""
        combi = self._create_combi_with_timbres([100, 50, 75, 25])
        assert get_combi_maximum_volume(combi) == 100
    
    def test_min_volume_some_muted(self):
        """Muted timbres should be excluded from min."""
        combi = self._create_combi_with_timbres(
            [100, 10, 75, 25],
            mutes=[False, True, False, False]
        )
        # 10 is muted, so min should be 25
        assert get_combi_minimum_volume(combi) == 25
    
    def test_max_volume_some_off(self):
        """Off timbres should be excluded from max."""
        combi = self._create_combi_with_timbres(
            [100, 127, 75, 25],
            statuses=["Int", "Off", "Int", "Int"]
        )
        # 127 is off, so max should be 100
        assert get_combi_maximum_volume(combi) == 100


class TestVolumeChangeFixed:
    """Test fixed volume change."""
    
    def test_fixed_timbre_volume(self):
        """Fixed change sets timbre to exact value."""
        timbre = Timbre(
            program_bank="INT-A", program_index=0,
            midi_channel=1, status="Int", volume=50
        )
        params = VolumeChangeParameters(
            change_type=VolumeChangeType.FIXED,
            value=100
        )
        change_timbre_volume(timbre, params)
        assert timbre.volume == 100
    
    def test_fixed_slot_volume(self):
        """Fixed change sets slot to exact value."""
        slot = SetListSlot(
            set_list_index=0, slot_index=0, name="Test"
        )
        slot._volume = 50
        params = VolumeChangeParameters(
            change_type=VolumeChangeType.FIXED,
            value=100
        )
        change_slot_volume(slot, params)
        assert slot.volume == 100


class TestVolumeChangeRelative:
    """Test relative volume change."""
    
    def test_relative_increase(self):
        """Relative change increases volume."""
        timbre = Timbre(
            program_bank="INT-A", program_index=0,
            midi_channel=1, status="Int", volume=50
        )
        params = VolumeChangeParameters(
            change_type=VolumeChangeType.RELATIVE,
            value=20
        )
        change_timbre_volume(timbre, params)
        assert timbre.volume == 70
    
    def test_relative_decrease(self):
        """Relative change decreases volume."""
        timbre = Timbre(
            program_bank="INT-A", program_index=0,
            midi_channel=1, status="Int", volume=50
        )
        params = VolumeChangeParameters(
            change_type=VolumeChangeType.RELATIVE,
            value=-20
        )
        change_timbre_volume(timbre, params)
        assert timbre.volume == 30
    
    def test_relative_clips_at_max(self):
        """Relative change clips at 127."""
        timbre = Timbre(
            program_bank="INT-A", program_index=0,
            midi_channel=1, status="Int", volume=120
        )
        params = VolumeChangeParameters(
            change_type=VolumeChangeType.RELATIVE,
            value=20
        )
        change_timbre_volume(timbre, params)
        assert timbre.volume == 127
    
    def test_relative_clips_at_min(self):
        """Relative change clips at 0."""
        timbre = Timbre(
            program_bank="INT-A", program_index=0,
            midi_channel=1, status="Int", volume=10
        )
        params = VolumeChangeParameters(
            change_type=VolumeChangeType.RELATIVE,
            value=-20
        )
        change_timbre_volume(timbre, params)
        assert timbre.volume == 0


class TestVolumeChangePercentage:
    """Test percentage volume change."""
    
    def test_percentage_100(self):
        """100% keeps volume unchanged."""
        timbre = Timbre(
            program_bank="INT-A", program_index=0,
            midi_channel=1, status="Int", volume=50
        )
        params = VolumeChangeParameters(
            change_type=VolumeChangeType.PERCENTAGE,
            value=100
        )
        change_timbre_volume(timbre, params)
        assert timbre.volume == 50
    
    def test_percentage_50(self):
        """50% halves volume."""
        timbre = Timbre(
            program_bank="INT-A", program_index=0,
            midi_channel=1, status="Int", volume=100
        )
        params = VolumeChangeParameters(
            change_type=VolumeChangeType.PERCENTAGE,
            value=50
        )
        change_timbre_volume(timbre, params)
        assert timbre.volume == 50
    
    def test_percentage_200(self):
        """200% doubles volume (clipped)."""
        timbre = Timbre(
            program_bank="INT-A", program_index=0,
            midi_channel=1, status="Int", volume=100
        )
        params = VolumeChangeParameters(
            change_type=VolumeChangeType.PERCENTAGE,
            value=200
        )
        change_timbre_volume(timbre, params)
        assert timbre.volume == 127  # Clipped


class TestVolumeChangeMapped:
    """Test mapped volume change."""
    
    def test_mapped_full_to_half(self):
        """Map 0-127 to 0-63."""
        timbre = Timbre(
            program_bank="INT-A", program_index=0,
            midi_channel=1, status="Int", volume=127
        )
        params = VolumeChangeParameters(
            change_type=VolumeChangeType.MAPPED,
            value=0,
            to_value=63
        )
        change_timbre_volume(timbre, params)
        assert timbre.volume == 63
    
    def test_mapped_to_offset_range(self):
        """Map 0-127 to 32-96."""
        timbre = Timbre(
            program_bank="INT-A", program_index=0,
            midi_channel=1, status="Int", volume=0
        )
        params = VolumeChangeParameters(
            change_type=VolumeChangeType.MAPPED,
            value=32,
            to_value=96
        )
        change_timbre_volume(timbre, params)
        assert timbre.volume == 32


class TestVolumeChangeSmartMapped:
    """Test smart mapped volume change."""
    
    def test_smart_mapped_uses_actual_range(self):
        """Smart mapping uses actual min/max from selection."""
        timbre = Timbre(
            program_bank="INT-A", program_index=0,
            midi_channel=1, status="Int", volume=75  # Middle of 50-100 range
        )
        params = VolumeChangeParameters(
            change_type=VolumeChangeType.SMART_MAPPED,
            value=0,
            to_value=127
        )
        # If actual range is 50-100, 75 is at 50% -> should map to ~64
        change_timbre_volume(timbre, params, min_value=50, max_value=100)
        assert timbre.volume == 64  # (75-50)/(100-50) * 127 + 0.5 = 63.5 -> 64


class TestCombiVolumeChange:
    """Test volume change on entire combi."""
    
    def test_change_all_timbres(self):
        """Volume change affects all timbres."""
        timbres = [
            Timbre(program_bank="INT-A", program_index=i,
                   midi_channel=i+1, status="Int", volume=50+i*10)
            for i in range(4)
        ]
        combi = Combi(bank="INT-A", index=0, name="Test", timbres=timbres)
        
        params = VolumeChangeParameters(
            change_type=VolumeChangeType.FIXED,
            value=100
        )
        change_combi_volume(combi, params)
        
        for timbre in combi.timbres:
            assert timbre.volume == 100


class TestBatchVolumeChange:
    """Test batch volume change operations."""
    
    def test_change_multiple_combis(self):
        """Change volume on multiple combis."""
        combis = []
        for i in range(3):
            timbres = [
                Timbre(program_bank="INT-A", program_index=0,
                       midi_channel=1, status="Int", volume=50)
            ]
            combis.append(Combi(bank="INT-A", index=i, name=f"Test{i}", timbres=timbres))
        
        params = VolumeChangeParameters(
            change_type=VolumeChangeType.FIXED,
            value=100
        )
        count = change_volumes(combis=combis, params=params)
        
        assert count == 3
        for combi in combis:
            assert combi.timbres[0].volume == 100
    
    def test_change_multiple_slots(self):
        """Change volume on multiple slots."""
        slots = []
        for i in range(3):
            slot = SetListSlot(set_list_index=0, slot_index=i, name=f"Slot{i}")
            slot._volume = 50
            slots.append(slot)
        
        params = VolumeChangeParameters(
            change_type=VolumeChangeType.FIXED,
            value=100
        )
        count = change_volumes(slots=slots, params=params)
        
        assert count == 3
        for slot in slots:
            assert slot.volume == 100


class TestVolumeRangeFinding:
    """Test finding volume ranges for smart mapping."""
    
    def test_find_range_combis(self):
        """Find min/max across multiple combis."""
        combis = []
        for vol in [30, 50, 100]:
            timbres = [
                Timbre(program_bank="INT-A", program_index=0,
                       midi_channel=1, status="Int", volume=vol)
            ]
            combis.append(Combi(bank="INT-A", index=0, name="Test", timbres=timbres))
        
        min_val, max_val = find_volume_range_combis(combis)
        assert min_val == 30
        assert max_val == 100
    
    def test_find_range_slots(self):
        """Find min/max across multiple slots."""
        slots = []
        for vol in [30, 50, 100]:
            slot = SetListSlot(set_list_index=0, slot_index=0, name="Test")
            slot._volume = vol
            slots.append(slot)
        
        min_val, max_val = find_volume_range_slots(slots)
        assert min_val == 30
        assert max_val == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
