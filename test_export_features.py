#!/usr/bin/env python3
"""
Test script for export features (Cubase export, Hex export).

Tests the export functionality based on C# implementation.
"""

import os
import sys
import unittest
from pathlib import Path

# Add pcg_tools to path
sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.cubase_export import export_to_cubase, _is_gm_bank, _get_bank_pcg_id
from pcg_tools.hex_export import generate_hex_export, format_single_patch_hex
from pcg_tools.models import Program, Combi, Category, Bank, PcgFile, PcgHeader, WorkstationModel


class TestCubaseExport(unittest.TestCase):
    """Test Cubase export functionality."""
    
    def test_is_gm_bank(self):
        """Test GM bank detection."""
        # GM banks
        gm_bank = Bank(bank_id="GM", bank_type="Program", patches=[])
        self.assertTrue(_is_gm_bank(gm_bank))
        
        g1_bank = Bank(bank_id="g(1)", bank_type="Program", patches=[])
        self.assertTrue(_is_gm_bank(g1_bank))
        
        # Non-GM banks
        int_bank = Bank(bank_id="I-A", bank_type="Program", patches=[])
        self.assertFalse(_is_gm_bank(int_bank))
        
        user_bank = Bank(bank_id="U-A", bank_type="Program", patches=[])
        self.assertFalse(_is_gm_bank(user_bank))
    
    def test_get_bank_pcg_id(self):
        """Test bank PCG ID calculation."""
        # Internal banks: I-A=0, I-B=1, ..., I-F=5
        self.assertEqual(_get_bank_pcg_id(Bank(bank_id="I-A", bank_type="Program", patches=[])), 0)
        self.assertEqual(_get_bank_pcg_id(Bank(bank_id="I-B", bank_type="Program", patches=[])), 1)
        self.assertEqual(_get_bank_pcg_id(Bank(bank_id="I-F", bank_type="Program", patches=[])), 5)
        
        # GM bank
        self.assertEqual(_get_bank_pcg_id(Bank(bank_id="GM", bank_type="Program", patches=[])), 6)
        
        # User banks: U-A=17, U-B=18, ...
        self.assertEqual(_get_bank_pcg_id(Bank(bank_id="U-A", bank_type="Program", patches=[])), 17)
        self.assertEqual(_get_bank_pcg_id(Bank(bank_id="U-B", bank_type="Program", patches=[])), 18)
    
    def test_export_header_format(self):
        """Test Cubase export header format."""
        # Create a minimal PcgFile with header
        header = PcgHeader(
            magic=b'KORG',
            product_id=0x68,
            file_type=0,
            major_version=1,
            minor_version=0,
            model=WorkstationModel.KRONOS
        )
        pcg = PcgFile(header=header)
        content = export_to_cubase(pcg)
        
        # Check header lines
        self.assertIn("[cubase parse file]", content)
        self.assertIn("[parser version 0001]", content)
        self.assertIn("[device manufacturer]Korg", content)
        self.assertIn("[device name] KRONOS(KORG)", content)
        self.assertIn("[define patchnames]", content)
        self.assertIn("[end]", content)


class TestHexExport(unittest.TestCase):
    """Test hex export functionality."""
    
    def test_generate_hex_export_empty(self):
        """Test hex export with no patches."""
        result = generate_hex_export([], b'')
        self.assertEqual(result.strip(), "")
    
    def test_generate_hex_export_format(self):
        """Test hex export format."""
        # Create a mock program with raw data
        prog = Program(
            bank="I-A",
            index=0,
            name="Test Program",
            raw_data=b'Test Program\x00' + b'\x00' * 12 + b'\x01\x02\x03\x04',
            _raw_offset=100
        )
        
        # Create mock content
        content = b'\x00' * 100 + prog.raw_data
        
        result = generate_hex_export([prog], content)
        
        # Check format - uses INT-A format from format_bank_id_for_display
        self.assertIn("INT-A000: Test Program", result)
        self.assertIn("00000000", result)  # Offset
    
    def test_hex_export_columns(self):
        """Test hex export column formatting."""
        prog = Program(
            bank="I-A",
            index=0,
            name="Test",
            raw_data=bytes(range(32)),  # 32 bytes of test data
            _raw_offset=100  # Non-zero offset required
        )
        
        # Content must include data at the offset
        content = b'\x00' * 100 + prog.raw_data
        result = generate_hex_export([prog], content, columns_per_line=16)
        
        # Should have lines of hex data (32 bytes / 16 columns = 2 data lines)
        # Filter out header line and empty lines
        lines = [l for l in result.split('\n') if l.strip() and not l.startswith('INT-')]
        self.assertGreaterEqual(len(lines), 2)
    
    def test_format_single_patch_hex(self):
        """Test single patch hex formatting."""
        prog = Program(
            bank="I-B",
            index=5,
            name="Single Test",
            raw_data=b'ABCDEFGH',
            _raw_offset=50  # Non-zero offset required
        )
        
        # Content must include data at the offset
        content = b'\x00' * 50 + prog.raw_data
        result = format_single_patch_hex(prog, content)
        
        # Uses INT-B format from format_bank_id_for_display
        self.assertIn("INT-B005: Single Test", result)


class TestModelByteProperties(unittest.TestCase):
    """Test byte_offset and byte_length properties on models."""
    
    def test_program_byte_properties(self):
        """Test Program byte_offset and byte_length."""
        prog = Program(
            bank="I-A",
            index=0,
            name="Test",
            raw_data=b'\x00' * 100,
            _raw_offset=500
        )
        
        self.assertEqual(prog.byte_offset, 500)
        self.assertEqual(prog.byte_length, 100)
    
    def test_combi_byte_properties(self):
        """Test Combi byte_offset and byte_length."""
        combi = Combi(
            bank="I-A",
            index=0,
            name="Test Combi",
            raw_data=b'\x00' * 200,
            _raw_offset=1000
        )
        
        self.assertEqual(combi.byte_offset, 1000)
        self.assertEqual(combi.byte_length, 200)
    
    def test_setlist_slot_byte_properties(self):
        """Test SetListSlot byte_offset and byte_length."""
        from pcg_tools.models import SetListSlot
        
        slot = SetListSlot(
            set_list_index=0,
            slot_index=0,
            name="Test Slot",
            raw_data=bytearray(b'\x00' * 542),
            _raw_offset=2000
        )
        
        self.assertEqual(slot.byte_offset, 2000)
        self.assertEqual(slot.byte_length, 542)


class TestExportWithRealFiles(unittest.TestCase):
    """Test export features with real PCG files."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_files_dir = Path("files_2_test")
    
    def test_cubase_export_real_file(self):
        """Test Cubase export with a real PCG file."""
        if not self.test_files_dir.exists():
            self.skipTest("Test files directory not found")
        
        pcg_files = list(self.test_files_dir.glob("**/*.PCG")) + \
                    list(self.test_files_dir.glob("**/*.pcg"))
        
        if not pcg_files:
            self.skipTest("No PCG files found in test directory")
        
        from pcg_tools.reader import read_pcg_file
        
        pcg_path = pcg_files[0]
        pcg = read_pcg_file(str(pcg_path))
        
        content = export_to_cubase(pcg, filename=str(pcg_path))
        
        # Verify basic structure
        self.assertIn("[cubase parse file]", content)
        self.assertIn("[end]", content)
        
        print(f"  Exported {pcg_path.name} to Cubase format")
        print(f"  Content length: {len(content)} characters")
    
    def test_hex_export_real_file(self):
        """Test hex export with a real PCG file."""
        if not self.test_files_dir.exists():
            self.skipTest("Test files directory not found")
        
        pcg_files = list(self.test_files_dir.glob("**/*.PCG")) + \
                    list(self.test_files_dir.glob("**/*.pcg"))
        
        if not pcg_files:
            self.skipTest("No PCG files found in test directory")
        
        from pcg_tools.reader import read_pcg_file
        
        pcg_path = pcg_files[0]
        pcg = read_pcg_file(str(pcg_path))
        
        # Get first program
        if pcg.program_banks and pcg.program_banks[0].patches:
            prog = pcg.program_banks[0].patches[0]
            
            result = generate_hex_export([prog], pcg.raw_data)
            
            self.assertIn(prog.id, result)
            print(f"  Hex export for {prog.id}: {prog.name}")
            print(f"  Offset: 0x{prog.byte_offset:08x}, Length: {prog.byte_length}")


if __name__ == "__main__":
    print("=" * 60)
    print("Export Features Tests")
    print("=" * 60)
    unittest.main(verbosity=2)
