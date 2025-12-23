#!/usr/bin/env python3
"""
Test script for additional features (Phase 8).

Tests MPE initialization and Clear Program functionality.
"""

import os
import sys
import unittest
from pathlib import Path

# Add pcg_tools to path
sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.models import Program, Combi, Timbre, Category
from pcg_tools.mpe_init import init_combi_as_mpe, can_init_as_mpe
from pcg_tools.clear_program import ClearProgramManager, clear_timbre


class TestMpeInit(unittest.TestCase):
    """Test MPE combi initialization."""
    
    def _create_test_combi(self, num_timbres: int = 16) -> Combi:
        """Create a test combi with timbres."""
        timbres = []
        for i in range(num_timbres):
            timbre = Timbre(
                program_bank="I-A",
                program_index=0,
                midi_channel=0,
                status="INT",
                volume=100,
                pan=64,
                mute=False,
                bottom_key=0,
                top_key=127,
                bottom_velocity=1,
                top_velocity=127,
                osc_mode="Poly",
                osc_select="Both"
            )
            timbres.append(timbre)
        
        return Combi(
            bank="I-A",
            index=0,
            name="Test Combi",
            timbres=timbres
        )
    
    def test_can_init_as_mpe_with_timbres(self):
        """Test can_init_as_mpe returns True for combi with timbres."""
        combi = self._create_test_combi()
        self.assertTrue(can_init_as_mpe(combi))
    
    def test_can_init_as_mpe_empty_combi(self):
        """Test can_init_as_mpe returns False for combi without timbres."""
        combi = Combi(bank="I-A", index=0, name="Empty", timbres=[])
        self.assertFalse(can_init_as_mpe(combi))
    
    def test_can_init_as_mpe_none(self):
        """Test can_init_as_mpe returns False for None."""
        self.assertFalse(can_init_as_mpe(None))
    
    def test_init_mpe_sets_midi_channels(self):
        """Test that MPE init sets unique MIDI channels."""
        combi = self._create_test_combi()
        init_combi_as_mpe(combi)
        
        # Each timbre should have a unique MIDI channel (0-15)
        for i, timbre in enumerate(combi.timbres):
            self.assertEqual(timbre.midi_channel, i)
    
    def test_init_mpe_copies_program(self):
        """Test that MPE init copies program from timbre 0."""
        combi = self._create_test_combi()
        
        # Set timbre 0 to a specific program
        combi.timbres[0].program_bank = "U-A"
        combi.timbres[0].program_index = 42
        
        init_combi_as_mpe(combi)
        
        # All timbres should have the same program
        for timbre in combi.timbres:
            self.assertEqual(timbre.program_bank, "U-A")
            self.assertEqual(timbre.program_index, 42)
    
    def test_init_mpe_copies_parameters(self):
        """Test that MPE init copies parameters from timbre 0."""
        combi = self._create_test_combi()
        
        # Set timbre 0 parameters
        combi.timbres[0].volume = 80
        combi.timbres[0].status = "EXT"
        combi.timbres[0].mute = True
        combi.timbres[0].bottom_key = 24
        combi.timbres[0].top_key = 96
        
        init_combi_as_mpe(combi)
        
        # All timbres should have the same parameters
        for timbre in combi.timbres:
            self.assertEqual(timbre.volume, 80)
            self.assertEqual(timbre.status, "EXT")
            self.assertEqual(timbre.mute, True)
            self.assertEqual(timbre.bottom_key, 24)
            self.assertEqual(timbre.top_key, 96)


class TestClearProgram(unittest.TestCase):
    """Test Clear Program functionality."""
    
    def _create_test_pcg(self):
        """Create a minimal test PCG file."""
        from pcg_tools.models import PcgFile, PcgHeader, Bank, WorkstationModel
        
        header = PcgHeader(
            magic=b'KORG',
            product_id=0x68,
            file_type=0,
            major_version=1,
            minor_version=0,
            model=WorkstationModel.KRONOS
        )
        
        # Create some test programs
        programs = []
        for i in range(5):
            prog = Program(
                bank="I-A",
                index=i,
                name=f"Program {i}",
                category=Category(main_category=0, sub_category=0)
            )
            programs.append(prog)
        
        bank = Bank(bank_id="I-A", bank_type="Program", patches=programs)
        
        return PcgFile(header=header, program_banks=[bank])
    
    def test_clear_program_manager_default(self):
        """Test ClearProgramManager initializes to first program."""
        pcg = self._create_test_pcg()
        manager = ClearProgramManager(pcg)
        
        clear_prog = manager.get_clear_program()
        self.assertIsNotNone(clear_prog)
        self.assertEqual(clear_prog.name, "Program 0")
    
    def test_clear_program_manager_set_custom(self):
        """Test setting a custom clear program."""
        pcg = self._create_test_pcg()
        manager = ClearProgramManager(pcg)
        
        # Set a different program as clear program
        custom_prog = pcg.program_banks[0].patches[3]
        manager.assigned_clear_program = custom_prog
        
        clear_prog = manager.get_clear_program()
        self.assertEqual(clear_prog.name, "Program 3")
    
    def test_clear_program_display(self):
        """Test clear program display string."""
        pcg = self._create_test_pcg()
        manager = ClearProgramManager(pcg)
        
        display = manager.get_clear_program_display()
        self.assertIn("INT-A000", display)
        self.assertIn("Program 0", display)
    
    def test_clear_timbre(self):
        """Test clearing a timbre."""
        timbre = Timbre(
            program_bank="U-A",
            program_index=50,
            midi_channel=0,
            status="INT"
        )
        
        clear_prog = Program(
            bank="I-A",
            index=0,
            name="Clear Program"
        )
        
        clear_timbre(timbre, clear_prog)
        
        self.assertEqual(timbre.program_bank, "I-A")
        self.assertEqual(timbre.program_index, 0)
    
    def test_clear_timbre_default(self):
        """Test clearing a timbre with no clear program."""
        timbre = Timbre(
            program_bank="U-A",
            program_index=50,
            midi_channel=0,
            status="INT"
        )
        
        clear_timbre(timbre, None)
        
        # Should default to I-A, 0
        self.assertEqual(timbre.program_bank, "I-A")
        self.assertEqual(timbre.program_index, 0)


if __name__ == "__main__":
    print("=" * 60)
    print("Additional Features Tests (Phase 8)")
    print("=" * 60)
    unittest.main(verbosity=2)
