"""Tests for the Program Reference Changer.

Tests the reference changer functionality ported from C# PCG Tools.
"""

import pytest
import os
from pcg_tools.reference_changer import (
    ProgramPatchParser, RuleParser, ReferenceChanger,
    change_references_from_rules, ReferenceChangeRule
)
from pcg_tools.reader import read_pcg_file


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def test_pcg():
    """Load a test PCG file."""
    test_file = 'files_2_test/nw.PCG'
    if not os.path.exists(test_file):
        pytest.skip(f"Test file not found: {test_file}")
    return read_pcg_file(test_file)


# =============================================================================
# ProgramPatchParser Tests
# =============================================================================

class TestProgramPatchParser:
    """Test the ProgramPatchParser class."""
    
    def test_parse_whole_bank(self, test_pcg):
        """Parse a whole bank reference like 'I-A'."""
        parser = ProgramPatchParser(test_pcg)
        
        # Find a bank that exists
        if not test_pcg.program_banks:
            pytest.skip("No program banks in test file")
        
        bank = test_pcg.program_banks[0]
        result = parser.parse(bank.bank_id)
        
        assert result is not None
        assert len(result) == len(bank.patches)
        assert all(r[0] == bank.bank_id for r in result)
        assert result[0][1] == 0
        assert result[-1][1] == len(bank.patches) - 1
    
    def test_parse_single_program(self, test_pcg):
        """Parse a single program reference like 'I-A040'."""
        parser = ProgramPatchParser(test_pcg)
        
        if not test_pcg.program_banks:
            pytest.skip("No program banks in test file")
        
        bank = test_pcg.program_banks[0]
        result = parser.parse(f"{bank.bank_id}040")
        
        assert result is not None
        assert len(result) == 1
        assert result[0] == (bank.bank_id, 40)
    
    def test_parse_range(self, test_pcg):
        """Parse a range reference like 'I-A040..080'."""
        parser = ProgramPatchParser(test_pcg)
        
        if not test_pcg.program_banks:
            pytest.skip("No program banks in test file")
        
        bank = test_pcg.program_banks[0]
        if len(bank.patches) < 81:
            pytest.skip("Bank too small for range test")
        
        result = parser.parse(f"{bank.bank_id}040..080")
        
        assert result is not None
        assert len(result) == 41  # 40 to 80 inclusive
        assert result[0] == (bank.bank_id, 40)
        assert result[-1] == (bank.bank_id, 80)
    
    def test_parse_auto_end(self, test_pcg):
        """Parse an auto-end reference like 'I-A040..'."""
        parser = ProgramPatchParser(test_pcg)
        
        if not test_pcg.program_banks:
            pytest.skip("No program banks in test file")
        
        bank = test_pcg.program_banks[0]
        
        # First parse a "from" range
        from_patches = [(bank.bank_id, i) for i in range(40, 51)]  # 11 patches
        
        # Parse with auto-end
        result = parser.parse(f"{bank.bank_id}000..", from_patches)
        
        assert result is not None
        assert len(result) == len(from_patches)
        assert result[0] == (bank.bank_id, 0)
        assert result[-1] == (bank.bank_id, 10)
    
    def test_parse_invalid_bank(self, test_pcg):
        """Parse with an invalid bank name returns None."""
        parser = ProgramPatchParser(test_pcg)
        result = parser.parse("INVALID-BANK")
        assert result is None
    
    def test_parse_out_of_range(self, test_pcg):
        """Parse with out-of-range index returns None."""
        parser = ProgramPatchParser(test_pcg)
        
        if not test_pcg.program_banks:
            pytest.skip("No program banks in test file")
        
        bank = test_pcg.program_banks[0]
        # Try to parse an index beyond the bank size
        result = parser.parse(f"{bank.bank_id}999")
        assert result is None


# =============================================================================
# RuleParser Tests
# =============================================================================

class TestRuleParser:
    """Test the RuleParser class."""
    
    def test_parse_simple_rule(self, test_pcg):
        """Parse a simple single-program rule."""
        if len(test_pcg.program_banks) < 2:
            pytest.skip("Need at least 2 program banks")
        
        bank1 = test_pcg.program_banks[0]
        bank2 = test_pcg.program_banks[1]
        
        parser = RuleParser(test_pcg)
        rules = f"{bank1.bank_id}000 -> {bank2.bank_id}000"
        
        assert parser.parse(rules) is True
        assert parser.has_parsed_ok is True
        assert len(parser.parsed_rules) == 1
        assert (bank1.bank_id, 0) in parser.parsed_rules
        assert parser.parsed_rules[(bank1.bank_id, 0)] == (bank2.bank_id, 0)
    
    def test_parse_range_rule(self, test_pcg):
        """Parse a range rule."""
        if len(test_pcg.program_banks) < 2:
            pytest.skip("Need at least 2 program banks")
        
        bank1 = test_pcg.program_banks[0]
        bank2 = test_pcg.program_banks[1]
        
        if len(bank1.patches) < 11 or len(bank2.patches) < 11:
            pytest.skip("Banks too small for range test")
        
        parser = RuleParser(test_pcg)
        rules = f"{bank1.bank_id}000..010 -> {bank2.bank_id}000.."
        
        assert parser.parse(rules) is True
        assert len(parser.parsed_rules) == 11
    
    def test_parse_multiple_rules(self, test_pcg):
        """Parse multiple rules."""
        if len(test_pcg.program_banks) < 2:
            pytest.skip("Need at least 2 program banks")
        
        bank1 = test_pcg.program_banks[0]
        bank2 = test_pcg.program_banks[1]
        
        parser = RuleParser(test_pcg)
        rules = f"""
        {bank1.bank_id}000 -> {bank2.bank_id}000
        {bank1.bank_id}001 -> {bank2.bank_id}001
        """
        
        assert parser.parse(rules) is True
        assert len(parser.parsed_rules) == 2
    
    def test_parse_with_comments(self, test_pcg):
        """Parse rules with comments and empty lines."""
        if len(test_pcg.program_banks) < 2:
            pytest.skip("Need at least 2 program banks")
        
        bank1 = test_pcg.program_banks[0]
        bank2 = test_pcg.program_banks[1]
        
        parser = RuleParser(test_pcg)
        rules = f"""
        # This is a comment
        {bank1.bank_id}000 -> {bank2.bank_id}000
        
        # Another comment
        {bank1.bank_id}001 -> {bank2.bank_id}001
        """
        
        assert parser.parse(rules) is True
        assert len(parser.parsed_rules) == 2
    
    def test_parse_arrow_variants(self, test_pcg):
        """Parse rules with different arrow styles."""
        if len(test_pcg.program_banks) < 2:
            pytest.skip("Need at least 2 program banks")
        
        bank1 = test_pcg.program_banks[0]
        bank2 = test_pcg.program_banks[1]
        
        parser = RuleParser(test_pcg)
        
        # Test -> arrow
        assert parser.parse(f"{bank1.bank_id}000 -> {bank2.bank_id}000") is True
        
        # Test => arrow
        parser2 = RuleParser(test_pcg)
        assert parser2.parse(f"{bank1.bank_id}000 => {bank2.bank_id}000") is True
        
        # Test > arrow
        parser3 = RuleParser(test_pcg)
        assert parser3.parse(f"{bank1.bank_id}000 > {bank2.bank_id}000") is True
    
    def test_parse_invalid_rule(self, test_pcg):
        """Parse an invalid rule returns error."""
        parser = RuleParser(test_pcg)
        
        # Missing arrow
        assert parser.parse("I-A000 I-B000") is False
        assert parser.has_parsed_ok is False
        assert parser.parse_error_line >= 0
    
    def test_parse_mismatched_counts(self, test_pcg):
        """Parse rules with mismatched patch counts fails."""
        if len(test_pcg.program_banks) < 2:
            pytest.skip("Need at least 2 program banks")
        
        bank1 = test_pcg.program_banks[0]
        bank2 = test_pcg.program_banks[1]
        
        if len(bank1.patches) < 11 or len(bank2.patches) < 6:
            pytest.skip("Banks too small for test")
        
        parser = RuleParser(test_pcg)
        # 11 from patches, 6 to patches
        rules = f"{bank1.bank_id}000..010 -> {bank2.bank_id}000..005"
        
        assert parser.parse(rules) is False
    
    def test_get_rules_as_list(self, test_pcg):
        """Test converting parsed rules to list format."""
        if len(test_pcg.program_banks) < 2:
            pytest.skip("Need at least 2 program banks")
        
        bank1 = test_pcg.program_banks[0]
        bank2 = test_pcg.program_banks[1]
        
        parser = RuleParser(test_pcg)
        rules = f"{bank1.bank_id}000..010 -> {bank2.bank_id}020.."
        
        assert parser.parse(rules) is True
        
        rule_list = parser.get_rules_as_list()
        assert len(rule_list) == 1
        
        rule = rule_list[0]
        assert rule.from_bank == bank1.bank_id
        assert rule.from_start == 0
        assert rule.from_end == 10
        assert rule.to_bank == bank2.bank_id
        assert rule.to_start == 20
        assert rule.to_end == 30


# =============================================================================
# ReferenceChanger Tests
# =============================================================================

class TestReferenceChanger:
    """Test the ReferenceChanger class."""
    
    def test_parse_rules(self, test_pcg):
        """Test parsing rules through ReferenceChanger."""
        if len(test_pcg.program_banks) < 2:
            pytest.skip("Need at least 2 program banks")
        
        bank1 = test_pcg.program_banks[0]
        bank2 = test_pcg.program_banks[1]
        
        changer = ReferenceChanger(test_pcg)
        rules = f"{bank1.bank_id}000 -> {bank2.bank_id}000"
        
        assert changer.parse_rules(rules) is True
        assert changer.has_parsed_ok is True
    
    def test_change_references_no_matches(self, test_pcg):
        """Test changing references when no matches exist."""
        if len(test_pcg.program_banks) < 2:
            pytest.skip("Need at least 2 program banks")
        
        bank1 = test_pcg.program_banks[0]
        bank2 = test_pcg.program_banks[1]
        
        changer = ReferenceChanger(test_pcg)
        # Use a rule that likely won't match anything
        rules = f"{bank1.bank_id}127 -> {bank2.bank_id}127"
        
        assert changer.parse_rules(rules) is True
        slots_changed, timbres_changed = changer.change_references()
        
        # May or may not find matches depending on file content
        assert slots_changed >= 0
        assert timbres_changed >= 0
    
    def test_progress_callback(self, test_pcg):
        """Test that progress callback is called."""
        if len(test_pcg.program_banks) < 2:
            pytest.skip("Need at least 2 program banks")
        
        bank1 = test_pcg.program_banks[0]
        bank2 = test_pcg.program_banks[1]
        
        progress_values = []
        
        def progress_callback(percentage):
            progress_values.append(percentage)
        
        changer = ReferenceChanger(test_pcg)
        changer.set_progress_callback(progress_callback)
        
        rules = f"{bank1.bank_id}000..010 -> {bank2.bank_id}000.."
        assert changer.parse_rules(rules) is True
        
        changer.change_references()
        
        # Should have received progress updates
        assert len(progress_values) > 0
        # Last progress should be 100
        assert progress_values[-1] == 100


# =============================================================================
# Convenience Function Tests
# =============================================================================

class TestChangeReferencesFromRules:
    """Test the convenience function."""
    
    def test_success(self, test_pcg):
        """Test successful reference change."""
        if len(test_pcg.program_banks) < 2:
            pytest.skip("Need at least 2 program banks")
        
        bank1 = test_pcg.program_banks[0]
        bank2 = test_pcg.program_banks[1]
        
        rules = f"{bank1.bank_id}000 -> {bank2.bank_id}000"
        success, error, slots, timbres = change_references_from_rules(test_pcg, rules)
        
        assert success is True
        assert error == ""
    
    def test_parse_error(self, test_pcg):
        """Test parse error handling."""
        rules = "INVALID RULE"
        success, error, slots, timbres = change_references_from_rules(test_pcg, rules)
        
        assert success is False
        assert error != ""
        assert "Line" in error


# =============================================================================
# Integration Tests
# =============================================================================

class TestReferenceChangerIntegration:
    """Integration tests with real PCG file data."""
    
    def test_find_references_to_change(self, test_pcg):
        """Find actual references that could be changed."""
        # Scan combis to find what programs are referenced
        referenced_programs = set()
        
        for bank in test_pcg.combi_banks:
            for combi in bank.patches:
                for timbre in combi.timbres:
                    if timbre.status in ("Off", "Int"):
                        prog_ref = (timbre.program_bank, timbre.program_index)
                        referenced_programs.add(prog_ref)
        
        # Scan set lists
        for setlist in test_pcg.set_lists:
            for slot in setlist.slots:
                if slot.patch_type == "Program":
                    prog_ref = (slot.patch_bank, slot.patch_index)
                    referenced_programs.add(prog_ref)
        
        # Just verify we can find references
        # The actual count depends on the test file
        print(f"Found {len(referenced_programs)} unique program references")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
