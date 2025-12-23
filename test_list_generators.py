#!/usr/bin/env python3
"""Test list generator functionality.

Tests the enhanced list generators matching C# implementation:
- Patch List (with CRC columns)
- Program Usage List
- Combi Content List (compact/short/long)
- Differences List
- File Content List
- Output formats: Text, CSV, ASCII Table, XML
"""

import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from pcg_tools.reader import read_pcg_file
from pcg_tools.list_generators import (
    ListGenerator, OutputFormat, SortMethod, FilterOnFavorites
)


def find_test_pcg():
    """Find a test PCG file."""
    test_dirs = ['files_2_test', '.', 'examples']
    for dir_path in test_dirs:
        if os.path.exists(dir_path):
            for f in os.listdir(dir_path):
                if f.lower().endswith('.pcg'):
                    return os.path.join(dir_path, f)
    return None


def test_patch_list_formats():
    """Test patch list generation in all formats."""
    pcg_file = find_test_pcg()
    if not pcg_file:
        print("SKIP: No test PCG file found")
        return True
    
    print(f"Testing with: {pcg_file}")
    pcg = read_pcg_file(pcg_file)
    gen = ListGenerator(pcg)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test Text format
        gen.output_format = OutputFormat.TEXT
        output = os.path.join(tmpdir, 'patch_list.txt')
        gen.generate_patch_list(output)
        assert os.path.exists(output), "Text output not created"
        with open(output) as f:
            content = f.read()
            assert 'PATCH LIST' in content, "Missing header in text output"
        print("  ✓ Text format")
        
        # Test CSV format
        gen.output_format = OutputFormat.CSV
        output = os.path.join(tmpdir, 'patch_list.csv')
        gen.generate_patch_list(output)
        assert os.path.exists(output), "CSV output not created"
        with open(output) as f:
            content = f.read()
            assert 'Type,ID,Name' in content, "Missing header in CSV output"
        print("  ✓ CSV format")
        
        # Test ASCII Table format
        gen.output_format = OutputFormat.ASCII_TABLE
        output = os.path.join(tmpdir, 'patch_list_ascii.txt')
        gen.generate_patch_list(output)
        assert os.path.exists(output), "ASCII table output not created"
        with open(output) as f:
            content = f.read()
            assert '+---' in content, "Missing table borders in ASCII output"
        print("  ✓ ASCII Table format")
        
        # Test XML format
        gen.output_format = OutputFormat.XML
        output = os.path.join(tmpdir, 'patch_list.xml')
        gen.generate_patch_list(output)
        assert os.path.exists(output), "XML output not created"
        xsl_file = os.path.join(tmpdir, 'patch_list.xsl')
        assert os.path.exists(xsl_file), "XSL stylesheet not created"
        with open(output) as f:
            content = f.read()
            assert '<?xml version' in content, "Missing XML declaration"
            assert '<patch_list' in content, "Missing root element"
        print("  ✓ XML format (with XSL)")
        
        # Test with CRC columns
        gen.output_format = OutputFormat.CSV
        output = os.path.join(tmpdir, 'patch_list_crc.csv')
        gen.generate_patch_list(output, include_crc_incl_name=True, include_crc_excl_name=True)
        with open(output) as f:
            content = f.read()
            assert 'CRC Inc' in content, "Missing CRC Inc column"
            assert 'CRC Exc' in content, "Missing CRC Exc column"
        print("  ✓ CRC columns")
    
    return True


def test_program_usage_list():
    """Test program usage list generation."""
    pcg_file = find_test_pcg()
    if not pcg_file:
        print("SKIP: No test PCG file found")
        return True
    
    pcg = read_pcg_file(pcg_file)
    gen = ListGenerator(pcg)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for fmt, ext in [(OutputFormat.TEXT, 'txt'), (OutputFormat.CSV, 'csv'),
                         (OutputFormat.ASCII_TABLE, 'ascii.txt'), (OutputFormat.XML, 'xml')]:
            gen.output_format = fmt
            output = os.path.join(tmpdir, f'usage.{ext}')
            gen.generate_program_usage_list(output)
            assert os.path.exists(output), f"Output not created for {fmt}"
        print("  ✓ Program usage list (all formats)")
    
    return True


def test_combi_content_list():
    """Test combi content list generation."""
    pcg_file = find_test_pcg()
    if not pcg_file:
        print("SKIP: No test PCG file found")
        return True
    
    pcg = read_pcg_file(pcg_file)
    gen = ListGenerator(pcg)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test all styles
        for style in ['compact', 'short', 'long']:
            gen.output_format = OutputFormat.TEXT
            output = os.path.join(tmpdir, f'combi_{style}.txt')
            gen.generate_combi_content_list(output, style=style)
            assert os.path.exists(output), f"Output not created for style {style}"
        print("  ✓ Combi content list (compact/short/long)")
        
        # Test ASCII table
        gen.output_format = OutputFormat.ASCII_TABLE
        output = os.path.join(tmpdir, 'combi_ascii.txt')
        gen.generate_combi_content_list(output, style='short')
        assert os.path.exists(output), "ASCII output not created"
        print("  ✓ Combi content ASCII table")
    
    return True


def test_file_content_list():
    """Test file content list generation."""
    pcg_file = find_test_pcg()
    if not pcg_file:
        print("SKIP: No test PCG file found")
        return True
    
    pcg = read_pcg_file(pcg_file)
    gen = ListGenerator(pcg)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for fmt, ext in [(OutputFormat.TEXT, 'txt'), (OutputFormat.CSV, 'csv'),
                         (OutputFormat.ASCII_TABLE, 'ascii.txt'), (OutputFormat.XML, 'xml')]:
            gen.output_format = fmt
            output = os.path.join(tmpdir, f'content.{ext}')
            gen.generate_file_content_list(output)
            assert os.path.exists(output), f"Output not created for {fmt}"
        print("  ✓ File content list (all formats)")
    
    return True


def test_differences_list():
    """Test differences list generation."""
    pcg_file = find_test_pcg()
    if not pcg_file:
        print("SKIP: No test PCG file found")
        return True
    
    pcg1 = read_pcg_file(pcg_file)
    pcg2 = read_pcg_file(pcg_file)  # Compare with itself (should find no differences)
    
    gen = ListGenerator(pcg1)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        gen.output_format = OutputFormat.TEXT
        output = os.path.join(tmpdir, 'diff.txt')
        gen.generate_differences_list(pcg2, output)
        assert os.path.exists(output), "Differences output not created"
        
        # Test ASCII table
        gen.output_format = OutputFormat.ASCII_TABLE
        output = os.path.join(tmpdir, 'diff_ascii.txt')
        gen.generate_differences_list(pcg2, output)
        assert os.path.exists(output), "ASCII differences output not created"
        
        print("  ✓ Differences list")
    
    return True


def test_sorting():
    """Test sorting options."""
    pcg_file = find_test_pcg()
    if not pcg_file:
        print("SKIP: No test PCG file found")
        return True
    
    pcg = read_pcg_file(pcg_file)
    gen = ListGenerator(pcg)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for sort in [SortMethod.TYPE_BANK_INDEX, SortMethod.ALPHABETICAL, SortMethod.CATEGORICAL]:
            gen.sort_method = sort
            gen.output_format = OutputFormat.TEXT
            output = os.path.join(tmpdir, f'sorted_{sort.value}.txt')
            gen.generate_patch_list(output)
            assert os.path.exists(output), f"Output not created for sort {sort}"
        print("  ✓ Sorting options")
    
    return True


def test_filtering():
    """Test filtering options."""
    pcg_file = find_test_pcg()
    if not pcg_file:
        print("SKIP: No test PCG file found")
        return True
    
    pcg = read_pcg_file(pcg_file)
    gen = ListGenerator(pcg)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test text filter
        gen.filter_on_text = True
        gen.filter_text = "Piano"
        gen.output_format = OutputFormat.TEXT
        output = os.path.join(tmpdir, 'filtered.txt')
        gen.generate_patch_list(output)
        assert os.path.exists(output), "Filtered output not created"
        
        # Reset filter
        gen.filter_on_text = False
        
        # Test ignore init
        gen.ignore_init_programs = True
        gen.ignore_init_combis = True
        output = os.path.join(tmpdir, 'no_init.txt')
        gen.generate_patch_list(output)
        assert os.path.exists(output), "No-init output not created"
        
        print("  ✓ Filtering options")
    
    return True


def test_patch_id_compression():
    """Test patch ID compression matching C# Util.GetPatchIdsString().
    
    Based on C# test cases in ListGeneratorFileContentList.TestPatchIdsString().
    """
    from pcg_tools.list_generators import ListGenerator
    from pcg_tools.models import PcgFile, PcgHeader, WorkstationModel
    
    # Create a minimal PCG for testing
    header = PcgHeader(
        magic=b'KORG',
        product_id=0x50,  # Kronos
        file_type=0x00,
        major_version=3,
        minor_version=0,
        model=WorkstationModel.KRONOS
    )
    pcg = PcgFile(header=header)
    gen = ListGenerator(pcg)
    
    # Test empty list
    result = gen._compress_patch_ids([])
    assert result == '', f"Empty list should return empty string, got: {result}"
    
    # Test single patch
    result = gen._compress_patch_ids(['I-A001'])
    assert result == 'I-A001', f"Single patch failed: {result}"
    
    # Test range of two consecutive
    result = gen._compress_patch_ids(['I-A003', 'I-A004'])
    assert result == 'I-A003~I-A004', f"Range of two failed: {result}"
    
    # Test range of three consecutive
    result = gen._compress_patch_ids(['I-A004', 'I-A005', 'I-A006'])
    assert result == 'I-A004~I-A006', f"Range of three failed: {result}"
    
    # Test two separate patches (gap)
    result = gen._compress_patch_ids(['I-A005', 'I-A007'])
    assert result == 'I-A005, I-A007', f"Two separate patches failed: {result}"
    
    # Test range and a separate patch
    result = gen._compress_patch_ids(['I-A002', 'I-A003', 'I-A012'])
    assert result == 'I-A002~I-A003, I-A012', f"Range and separate failed: {result}"
    
    # Test separate patch and a range
    result = gen._compress_patch_ids(['I-A004', 'I-A011', 'I-A012'])
    assert result == 'I-A004, I-A011~I-A012', f"Separate and range failed: {result}"
    
    # Test two patches in separate banks
    result = gen._compress_patch_ids(['I-A004', 'I-B005'])
    assert result == 'I-A004, I-B005', f"Separate banks failed: {result}"
    
    # Test two ranges in separate banks
    result = gen._compress_patch_ids(['I-A004', 'I-A005', 'I-C006', 'I-C007'])
    assert result == 'I-A004~I-A005, I-C006~I-C007', f"Two ranges separate banks failed: {result}"
    
    print("  ✓ Patch ID compression (C# parity)")
    return True


def test_virtual_banks_support():
    """Test virtual banks support in list generator.
    
    Based on C# ListGeneratorWindow.SetGeneratorProgramParameters() and
    SetGeneratorCombiParameters() which add all virtual banks when the
    Virtual Banks checkbox is checked.
    """
    from pcg_tools.list_generators import ListGenerator
    from pcg_tools.models import PcgFile, PcgHeader, WorkstationModel, Bank
    from pcg_tools.virtual_banks import is_virtual_bank_id
    
    # Create a minimal PCG for testing
    header = PcgHeader(
        magic=b'KORG',
        product_id=0x50,  # Kronos
        file_type=0x00,
        major_version=3,
        minor_version=0,
        model=WorkstationModel.KRONOS
    )
    pcg = PcgFile(header=header)
    
    # Add some test banks including a virtual bank
    pcg.program_banks = [
        Bank(bank_id='I-A', bank_type='Int', patches=[]),
        Bank(bank_id='U-A', bank_type='User', patches=[]),
        Bank(bank_id='V0-A', bank_type='Virtual', patches=[]),  # Virtual bank
    ]
    pcg.combi_banks = [
        Bank(bank_id='I-A', bank_type='Int', patches=[]),
        Bank(bank_id='V0-B', bank_type='Virtual', patches=[]),  # Virtual bank
    ]
    
    gen = ListGenerator(pcg)
    
    # Test 1: Default behavior - all banks selected
    banks = gen._get_selected_program_banks()
    assert len(banks) == 3, f"Expected 3 banks, got {len(banks)}"
    print("  ✓ Default: all banks selected")
    
    # Test 2: Select specific banks (no virtual)
    gen.selected_program_banks = ['I-A', 'U-A']
    gen.include_virtual_program_banks = False
    banks = gen._get_selected_program_banks()
    assert len(banks) == 2, f"Expected 2 banks, got {len(banks)}"
    assert all(not is_virtual_bank_id(b.bank_id) for b in banks), "Should not include virtual banks"
    print("  ✓ Selected banks without virtual")
    
    # Test 3: Enable virtual banks - should add virtual banks
    gen.include_virtual_program_banks = True
    banks = gen._get_selected_program_banks()
    # Should include I-A, U-A, and V0-A (virtual)
    bank_ids = [b.bank_id for b in banks]
    assert 'V0-A' in bank_ids, f"Virtual bank V0-A should be included, got: {bank_ids}"
    print("  ✓ Virtual banks enabled adds virtual banks")
    
    # Test 4: Combi banks with virtual
    gen.selected_combi_banks = ['I-A']
    gen.include_virtual_combi_banks = False
    banks = gen._get_selected_combi_banks()
    assert len(banks) == 1, f"Expected 1 bank, got {len(banks)}"
    
    gen.include_virtual_combi_banks = True
    banks = gen._get_selected_combi_banks()
    bank_ids = [b.bank_id for b in banks]
    assert 'V0-B' in bank_ids, f"Virtual bank V0-B should be included, got: {bank_ids}"
    print("  ✓ Combi virtual banks support")
    
    # Test 5: is_virtual_bank_id function
    assert is_virtual_bank_id('V0-A') == True
    assert is_virtual_bank_id('V7-H') == True
    assert is_virtual_bank_id('I-A') == False
    assert is_virtual_bank_id('U-GG') == False
    print("  ✓ is_virtual_bank_id function")
    
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("List Generator Tests")
    print("=" * 60)
    
    tests = [
        ("Patch List Formats", test_patch_list_formats),
        ("Program Usage List", test_program_usage_list),
        ("Combi Content List", test_combi_content_list),
        ("File Content List", test_file_content_list),
        ("Differences List", test_differences_list),
        ("Sorting", test_sorting),
        ("Filtering", test_filtering),
        ("Patch ID Compression", test_patch_id_compression),
        ("Virtual Banks Support", test_virtual_banks_support),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        print(f"\n{name}:")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"  ✗ FAILED")
        except Exception as e:
            failed += 1
            print(f"  ✗ ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
