#!/usr/bin/env python3
"""Tests for Double to Single Keyboard Setup functionality.

Based on C# DoubleToSingleKeyboardCommands.cs.
"""

import os
import sys
import unittest
from copy import deepcopy

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcg_tools.double_to_single import (
    uses_midi_channel,
    switch_midi_channels,
    set_name_suffix,
    process_double_to_single,
    DoubleToSingleResult
)
from pcg_tools.models import PcgFile, PcgHeader, Combi, Timbre, SetList, SetListSlot, Bank


class MockTimbre:
    """Mock timbre for testing."""
    def __init__(self, status="Int", midi_channel=0):
        self.status = status
        self.midi_channel = midi_channel


class MockCombi:
    """Mock combi for testing."""
    def __init__(self, name="Test Combi", timbres=None):
        self.name = name
        self.timbres = timbres or []
        self.category = None
        self.favorite = False
        self.tempo = 120.0
        self.raw_data = None


class MockSetListSlot:
    """Mock setlist slot for testing."""
    def __init__(self, name="", patch_type="Combi", patch_bank="I-A", patch_index=0):
        self.name = name
        self._description = ""
        self.notes = ""
        self.patch_type = patch_type
        self.patch_bank = patch_bank
        self.patch_index = patch_index
        self._transpose = 0
        self._volume = 127
        self.hold = False
        self.color = 0
        self._text_size = 0
        self.raw_data = None


class TestUsesMidiChannel(unittest.TestCase):
    """Tests for uses_midi_channel function."""
    
    def test_uses_channel_with_int_status(self):
        """Test that Int status timbres are checked."""
        combi = MockCombi(timbres=[
            MockTimbre(status="Int", midi_channel=0),  # Channel 1
            MockTimbre(status="Int", midi_channel=1),  # Channel 2
        ])
        
        self.assertTrue(uses_midi_channel(combi, 1))
        self.assertTrue(uses_midi_channel(combi, 2))
        self.assertFalse(uses_midi_channel(combi, 3))
    
    def test_uses_channel_with_on_status(self):
        """Test that On status timbres are checked."""
        combi = MockCombi(timbres=[
            MockTimbre(status="On", midi_channel=4),  # Channel 5
        ])
        
        self.assertTrue(uses_midi_channel(combi, 5))
        self.assertFalse(uses_midi_channel(combi, 1))
    
    def test_ignores_both_status(self):
        """Test that Both status is NOT checked (per C# implementation)."""
        combi = MockCombi(timbres=[
            MockTimbre(status="Both", midi_channel=0),  # Channel 1
        ])
        
        # C# UsesMidiChannel only checks "On" and "Int", not "Both"
        self.assertFalse(uses_midi_channel(combi, 1))
    
    def test_ignores_off_status(self):
        """Test that Off status timbres are ignored."""
        combi = MockCombi(timbres=[
            MockTimbre(status="Off", midi_channel=0),
        ])
        
        self.assertFalse(uses_midi_channel(combi, 1))
    
    def test_ignores_mute_status(self):
        """Test that Mute status timbres are ignored."""
        combi = MockCombi(timbres=[
            MockTimbre(status="Mute", midi_channel=0),
        ])
        
        self.assertFalse(uses_midi_channel(combi, 1))


class TestSwitchMidiChannels(unittest.TestCase):
    """Tests for switch_midi_channels function."""
    
    def test_switch_channels(self):
        """Test basic channel switching."""
        combi = MockCombi(timbres=[
            MockTimbre(status="Int", midi_channel=0),  # Channel 1
            MockTimbre(status="Int", midi_channel=1),  # Channel 2
            MockTimbre(status="Int", midi_channel=2),  # Channel 3 (unchanged)
        ])
        
        switch_midi_channels(combi, 1, 2)
        
        self.assertEqual(combi.timbres[0].midi_channel, 1)  # Was 0 (ch1), now 1 (ch2)
        self.assertEqual(combi.timbres[1].midi_channel, 0)  # Was 1 (ch2), now 0 (ch1)
        self.assertEqual(combi.timbres[2].midi_channel, 2)  # Unchanged
    
    def test_switch_includes_both_status(self):
        """Test that Both status IS included in switching (per C# SwitchMidiChannels)."""
        combi = MockCombi(timbres=[
            MockTimbre(status="Both", midi_channel=0),  # Channel 1
        ])
        
        switch_midi_channels(combi, 1, 2)
        
        self.assertEqual(combi.timbres[0].midi_channel, 1)  # Switched to channel 2
    
    def test_switch_ignores_off_status(self):
        """Test that Off status timbres are not switched."""
        combi = MockCombi(timbres=[
            MockTimbre(status="Off", midi_channel=0),
        ])
        
        switch_midi_channels(combi, 1, 2)
        
        self.assertEqual(combi.timbres[0].midi_channel, 0)  # Unchanged


class TestSetNameSuffix(unittest.TestCase):
    """Tests for set_name_suffix function."""
    
    def test_short_name_with_suffix(self):
        """Test suffix is right-padded for short names."""
        slot = MockSetListSlot(name="Test")
        set_name_suffix(slot, "/MC1")
        
        # Name should be "Test" + spaces + "/MC1" = 24 chars total
        self.assertEqual(len(slot.name), 24)
        self.assertTrue(slot.name.endswith("/MC1"))
        self.assertTrue(slot.name.startswith("Test"))
    
    def test_long_name_truncated(self):
        """Test long names are truncated to fit suffix."""
        slot = MockSetListSlot(name="A" * 24)  # Max length name
        set_name_suffix(slot, "/MC1")
        
        # Name should be truncated to fit suffix
        self.assertEqual(len(slot.name), 24)
        self.assertTrue(slot.name.endswith("/MC1"))
        self.assertEqual(slot.name[:20], "A" * 20)  # 24 - 4 = 20 chars for name
    
    def test_exact_fit_name(self):
        """Test name that exactly fits with suffix."""
        slot = MockSetListSlot(name="A" * 20)  # 20 chars + 4 for suffix = 24
        set_name_suffix(slot, "/MC1")
        
        self.assertEqual(slot.name, "A" * 20 + "/MC1")
        self.assertEqual(len(slot.name), 24)


class TestProcessDoubleToSingle(unittest.TestCase):
    """Tests for process_double_to_single function."""
    
    def _create_mock_pcg(self):
        """Create a mock PCG file for testing."""
        from pcg_tools.models import PcgHeader, WorkstationModel
        header = PcgHeader(
            magic=b'KORG',
            product_id=0x50,
            file_type=0x00,
            major_version=1,
            minor_version=0,
            model=WorkstationModel.KRONOS
        )
        pcg = PcgFile(header=header)
        return pcg
    
    def test_no_setlists_error(self):
        """Test error when no setlists present."""
        pcg = self._create_mock_pcg()
        pcg.set_lists = None
        
        result = process_double_to_single(pcg, 0, 1, "U-A", 1, 2)
        
        self.assertFalse(result.success)
        self.assertIn("not present", result.error_message.lower())
    
    def test_invalid_source_index(self):
        """Test error for invalid source setlist index."""
        pcg = self._create_mock_pcg()
        pcg.set_lists = [SetList(0, "SL0")]
        
        result = process_double_to_single(pcg, 5, 0, "U-A", 1, 2)
        
        self.assertFalse(result.success)
        self.assertIn("invalid", result.error_message.lower())
    
    def test_invalid_target_index(self):
        """Test error for invalid target setlist index."""
        pcg = self._create_mock_pcg()
        pcg.set_lists = [SetList(0, "SL0")]
        
        result = process_double_to_single(pcg, 0, 5, "U-A", 1, 2)
        
        self.assertFalse(result.success)
        self.assertIn("invalid", result.error_message.lower())


class TestDoubleToSingleResult(unittest.TestCase):
    """Tests for DoubleToSingleResult class."""
    
    def test_default_values(self):
        """Test default result values."""
        result = DoubleToSingleResult()
        
        self.assertTrue(result.success)
        self.assertEqual(result.error_message, "")
        self.assertEqual(result.slots_created, 0)
        self.assertEqual(result.combis_created, 0)


if __name__ == "__main__":
    unittest.main()
