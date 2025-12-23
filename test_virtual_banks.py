#!/usr/bin/env python3
"""Tests for Virtual Banks functionality.

Based on C# KronosProgramBanks.CreateVirtualBanks() and KronosCombiBanks.CreateVirtualBanks().
"""

import os
import sys
import unittest

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcg_tools.virtual_banks import (
    FIRST_VIRTUAL_BANK_ID,
    NUMBER_OF_VIRTUAL_BANKS,
    VIRTUAL_BANK_GROUPS,
    BANKS_PER_GROUP,
    BANK_NAMES,
    VirtualBank,
    generate_virtual_bank_ids,
    create_virtual_program_banks,
    create_virtual_combi_banks,
    is_virtual_bank_id,
    parse_virtual_bank_id,
    get_virtual_bank_pcg_id,
    pcg_id_to_virtual_bank_id,
    VirtualBankManager
)


class TestConstants(unittest.TestCase):
    """Tests for virtual bank constants."""
    
    def test_first_virtual_bank_id(self):
        """Test first virtual bank ID matches C#."""
        self.assertEqual(FIRST_VIRTUAL_BANK_ID, 0x30)
    
    def test_number_of_virtual_banks(self):
        """Test number of virtual banks (8 groups × 8 banks = 64)."""
        self.assertEqual(NUMBER_OF_VIRTUAL_BANKS, 64)
        self.assertEqual(VIRTUAL_BANK_GROUPS * BANKS_PER_GROUP, 64)
    
    def test_bank_names(self):
        """Test bank names A-H."""
        self.assertEqual(BANK_NAMES, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])


class TestGenerateVirtualBankIds(unittest.TestCase):
    """Tests for generate_virtual_bank_ids function."""
    
    def test_generates_64_banks(self):
        """Test that 64 virtual banks are generated."""
        banks = generate_virtual_bank_ids()
        self.assertEqual(len(banks), 64)
    
    def test_first_bank(self):
        """Test first virtual bank is V0-A with ID 0x30."""
        banks = generate_virtual_bank_ids()
        self.assertEqual(banks[0], ("V0-A", 0x30))
    
    def test_last_bank(self):
        """Test last virtual bank is V7-H with ID 0x6F."""
        banks = generate_virtual_bank_ids()
        self.assertEqual(banks[-1], ("V7-H", 0x6F))
    
    def test_bank_id_format(self):
        """Test all bank IDs follow V<group>-<letter> format."""
        banks = generate_virtual_bank_ids()
        for bank_id, _ in banks:
            self.assertTrue(bank_id.startswith('V'))
            self.assertIn('-', bank_id)
            parts = bank_id[1:].split('-')
            self.assertEqual(len(parts), 2)
            self.assertTrue(parts[0].isdigit())
            self.assertIn(parts[1], BANK_NAMES)


class TestCreateVirtualBanks(unittest.TestCase):
    """Tests for create_virtual_program_banks and create_virtual_combi_banks."""
    
    def test_create_program_banks_count(self):
        """Test 64 program banks are created."""
        banks = create_virtual_program_banks()
        self.assertEqual(len(banks), 64)
    
    def test_create_combi_banks_count(self):
        """Test 64 combi banks are created."""
        banks = create_virtual_combi_banks()
        self.assertEqual(len(banks), 64)
    
    def test_program_bank_pcg_ids(self):
        """Test program banks have correct PCG IDs."""
        banks = create_virtual_program_banks()
        self.assertEqual(banks[0].pcg_id, 0x30)
        self.assertEqual(banks[63].pcg_id, 0x6F)
    
    def test_combi_bank_pcg_ids(self):
        """Test combi banks have -1 PCG ID (per C# code)."""
        banks = create_virtual_combi_banks()
        for bank in banks:
            self.assertEqual(bank.pcg_id, -1)
    
    def test_bank_properties(self):
        """Test virtual bank properties."""
        banks = create_virtual_program_banks()
        for bank in banks:
            self.assertTrue(bank.is_virtual)
            self.assertTrue(bank.is_writable)
            self.assertFalse(bank.is_read_only)


class TestIsVirtualBankId(unittest.TestCase):
    """Tests for is_virtual_bank_id function."""
    
    def test_valid_virtual_bank_ids(self):
        """Test valid virtual bank IDs are recognized."""
        self.assertTrue(is_virtual_bank_id("V0-A"))
        self.assertTrue(is_virtual_bank_id("V7-H"))
        self.assertTrue(is_virtual_bank_id("V3-D"))
    
    def test_invalid_bank_ids(self):
        """Test non-virtual bank IDs are rejected."""
        self.assertFalse(is_virtual_bank_id("I-A"))
        self.assertFalse(is_virtual_bank_id("U-B"))
        self.assertFalse(is_virtual_bank_id("GM"))
        self.assertFalse(is_virtual_bank_id(""))
        self.assertFalse(is_virtual_bank_id(None))


class TestParseVirtualBankId(unittest.TestCase):
    """Tests for parse_virtual_bank_id function."""
    
    def test_parse_v0_a(self):
        """Test parsing V0-A."""
        result = parse_virtual_bank_id("V0-A")
        self.assertEqual(result, (0, 0))
    
    def test_parse_v7_h(self):
        """Test parsing V7-H."""
        result = parse_virtual_bank_id("V7-H")
        self.assertEqual(result, (7, 7))
    
    def test_parse_v3_d(self):
        """Test parsing V3-D."""
        result = parse_virtual_bank_id("V3-D")
        self.assertEqual(result, (3, 3))
    
    def test_parse_invalid(self):
        """Test parsing invalid bank IDs returns None."""
        self.assertIsNone(parse_virtual_bank_id("I-A"))
        self.assertIsNone(parse_virtual_bank_id("V8-A"))  # Invalid group
        self.assertIsNone(parse_virtual_bank_id("V0-I"))  # Invalid bank letter


class TestGetVirtualBankPcgId(unittest.TestCase):
    """Tests for get_virtual_bank_pcg_id function."""
    
    def test_v0_a_pcg_id(self):
        """Test V0-A has PCG ID 0x30."""
        self.assertEqual(get_virtual_bank_pcg_id("V0-A"), 0x30)
    
    def test_v7_h_pcg_id(self):
        """Test V7-H has PCG ID 0x6F."""
        self.assertEqual(get_virtual_bank_pcg_id("V7-H"), 0x6F)
    
    def test_invalid_returns_none(self):
        """Test invalid bank ID returns None."""
        self.assertIsNone(get_virtual_bank_pcg_id("I-A"))


class TestPcgIdToVirtualBankId(unittest.TestCase):
    """Tests for pcg_id_to_virtual_bank_id function."""
    
    def test_0x30_to_v0_a(self):
        """Test PCG ID 0x30 converts to V0-A."""
        self.assertEqual(pcg_id_to_virtual_bank_id(0x30), "V0-A")
    
    def test_0x6f_to_v7_h(self):
        """Test PCG ID 0x6F converts to V7-H."""
        self.assertEqual(pcg_id_to_virtual_bank_id(0x6F), "V7-H")
    
    def test_non_virtual_returns_none(self):
        """Test non-virtual PCG IDs return None."""
        self.assertIsNone(pcg_id_to_virtual_bank_id(0x00))
        self.assertIsNone(pcg_id_to_virtual_bank_id(0x2F))
        self.assertIsNone(pcg_id_to_virtual_bank_id(0x70))


class TestVirtualBankManager(unittest.TestCase):
    """Tests for VirtualBankManager class."""
    
    def test_initialize(self):
        """Test manager initialization."""
        manager = VirtualBankManager()
        manager.initialize()
        
        self.assertEqual(len(manager.program_banks), 64)
        self.assertEqual(len(manager.combi_banks), 64)
    
    def test_get_program_bank(self):
        """Test getting a program bank by ID."""
        manager = VirtualBankManager()
        manager.initialize()
        
        bank = manager.get_program_bank("V0-A")
        self.assertIsNotNone(bank)
        self.assertEqual(bank.bank_id, "V0-A")
    
    def test_get_combi_bank(self):
        """Test getting a combi bank by ID."""
        manager = VirtualBankManager()
        manager.initialize()
        
        bank = manager.get_combi_bank("V3-D")
        self.assertIsNotNone(bank)
        self.assertEqual(bank.bank_id, "V3-D")
    
    def test_get_all_bank_ids(self):
        """Test getting all bank IDs."""
        manager = VirtualBankManager()
        manager.initialize()
        
        program_ids = manager.get_all_program_bank_ids()
        combi_ids = manager.get_all_combi_bank_ids()
        
        self.assertEqual(len(program_ids), 64)
        self.assertEqual(len(combi_ids), 64)
        self.assertIn("V0-A", program_ids)
        self.assertIn("V7-H", combi_ids)


if __name__ == "__main__":
    unittest.main()
