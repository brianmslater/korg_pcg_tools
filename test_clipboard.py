#!/usr/bin/env python3
"""Test clipboard functionality including Phase 3 enhancements."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcg_tools.clipboard import Clipboard, get_clipboard
from pcg_tools.models import Program, Combi, SetListSlot, DrumKit, WaveSequence, Category


def test_clipboard_basic():
    """Test basic clipboard operations."""
    clipboard = Clipboard()
    
    # Test is_empty
    assert clipboard.is_empty, "New clipboard should be empty"
    
    # Test program copy/paste
    program = Program(bank="I-A", index=0, name="Test Program")
    program.engine = "HD-1"
    program.favorite = True
    
    clipboard.copy_program(program)
    assert clipboard.has_program(), "Clipboard should have program"
    assert not clipboard.is_empty, "Clipboard should not be empty"
    
    target = Program(bank="U-A", index=0, name="")
    clipboard.paste_program(target)
    assert target.name == "Test Program"
    assert target.engine == "HD-1"
    assert target.favorite == True
    
    print("✓ Basic program copy/paste works")


def test_drum_kit_clipboard():
    """Test drum kit clipboard operations (Task 3.1.1)."""
    clipboard = Clipboard()
    
    # Create a drum kit
    drum_kit = DrumKit(bank="I-A", index=0, name="Test Drum Kit")
    drum_kit.raw_data = b'\x00\x01\x02\x03'
    
    # Test copy
    clipboard.copy_drum_kit(drum_kit)
    assert clipboard.has_drum_kit(), "Clipboard should have drum kit"
    assert not clipboard.is_empty, "Clipboard should not be empty"
    
    # Test paste
    target = DrumKit(bank="U-A", index=0, name="")
    clipboard.paste_drum_kit(target)
    assert target.name == "Test Drum Kit"
    assert target.raw_data == b'\x00\x01\x02\x03'
    
    # Test multiple drum kits
    clipboard.clear()
    drum_kits = [
        DrumKit(bank="I-A", index=0, name="Kit 1"),
        DrumKit(bank="I-A", index=1, name="Kit 2"),
    ]
    clipboard.copy_drum_kits(drum_kits)
    assert clipboard.has_drum_kit(), "Clipboard should have drum kits"
    assert len(clipboard.drum_kits) == 2
    
    print("✓ Drum kit clipboard works (Task 3.1.1)")


def test_wave_sequence_clipboard():
    """Test wave sequence clipboard operations (Task 3.1.3)."""
    clipboard = Clipboard()
    
    # Create a wave sequence
    wave_seq = WaveSequence(bank="I-A", index=0, name="Test Wave Seq")
    wave_seq.raw_data = b'\x10\x20\x30\x40'
    
    # Test copy
    clipboard.copy_wave_sequence(wave_seq)
    assert clipboard.has_wave_sequence(), "Clipboard should have wave sequence"
    assert not clipboard.is_empty, "Clipboard should not be empty"
    
    # Test paste
    target = WaveSequence(bank="U-A", index=0, name="")
    clipboard.paste_wave_sequence(target)
    assert target.name == "Test Wave Seq"
    assert target.raw_data == b'\x10\x20\x30\x40'
    
    # Test multiple wave sequences
    clipboard.clear()
    wave_seqs = [
        WaveSequence(bank="I-A", index=0, name="WS 1"),
        WaveSequence(bank="I-A", index=1, name="WS 2"),
    ]
    clipboard.copy_wave_sequences(wave_seqs)
    assert clipboard.has_wave_sequence(), "Clipboard should have wave sequences"
    assert len(clipboard.wave_sequences) == 2
    
    print("✓ Wave sequence clipboard works (Task 3.1.3)")


def test_clipboard_recall():
    """Test clipboard recall functionality (Task 3.2.1)."""
    clipboard = Clipboard()
    
    # Copy a program
    program1 = Program(bank="I-A", index=0, name="Program 1")
    clipboard.copy_program(program1)
    
    # Memorize current state
    clipboard.memorize()
    assert clipboard.has_memory(), "Clipboard should have memory"
    
    # Copy a different program
    program2 = Program(bank="I-A", index=1, name="Program 2")
    clipboard.copy_program(program2)
    assert clipboard.program.name == "Program 2"
    
    # Recall previous state
    clipboard.recall()
    assert clipboard.program.name == "Program 1", "Should recall Program 1"
    
    # Test with drum kit
    clipboard.clear()
    drum_kit = DrumKit(bank="I-A", index=0, name="Memorized Kit")
    clipboard.copy_drum_kit(drum_kit)
    clipboard.memorize()
    
    clipboard.clear()
    assert clipboard.is_empty, "Clipboard should be empty after clear"
    
    clipboard.recall()
    assert clipboard.drum_kit.name == "Memorized Kit", "Should recall drum kit"
    
    print("✓ Clipboard recall works (Task 3.2.1)")


def test_exit_copy_paste_mode():
    """Test exit copy/paste mode (Task 3.2.2)."""
    clipboard = Clipboard()
    
    # Add various items to clipboard
    clipboard.copy_program(Program(bank="I-A", index=0, name="Test"))
    clipboard.copy_drum_kit(DrumKit(bank="I-A", index=0, name="Kit"))
    clipboard.memorize()
    
    assert not clipboard.is_empty, "Clipboard should have content"
    assert clipboard.has_memory(), "Clipboard should have memory"
    
    # Exit copy/paste mode
    clipboard.exit_copy_paste_mode()
    
    assert clipboard.is_empty, "Clipboard should be empty after exit"
    assert not clipboard.has_memory(), "Memory should be cleared after exit"
    
    print("✓ Exit copy/paste mode works (Task 3.2.2)")


def test_global_clipboard():
    """Test global clipboard instance."""
    clipboard1 = get_clipboard()
    clipboard2 = get_clipboard()
    
    assert clipboard1 is clipboard2, "Should return same instance"
    
    print("✓ Global clipboard instance works")


def main():
    """Run all clipboard tests."""
    print("Testing clipboard functionality (Phase 3)...")
    print()
    
    test_clipboard_basic()
    test_drum_kit_clipboard()
    test_wave_sequence_clipboard()
    test_clipboard_recall()
    test_exit_copy_paste_mode()
    test_global_clipboard()
    
    print()
    print("=" * 50)
    print("All clipboard tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
