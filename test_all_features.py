#!/usr/bin/env python3
"""
Comprehensive test suite for PCG Tools v1.3.0
Tests all major features added in this release.
"""

import sys
import traceback
from pathlib import Path

# Test results tracking
tests_passed = 0
tests_failed = 0
test_results = []

def run_test(test_name, test_func):
    """Run a test and track results."""
    global tests_passed, tests_failed
    
    print(f"\n{'='*60}")
    print(f"Running: {test_name}")
    print('='*60)
    
    try:
        test_func()
        tests_passed += 1
        test_results.append((test_name, "✅ PASS"))
        print(f"\n✅ {test_name} PASSED")
    except Exception as e:
        tests_failed += 1
        test_results.append((test_name, f"❌ FAIL: {str(e)}"))
        print(f"\n❌ {test_name} FAILED")
        print(f"Error: {e}")
        traceback.print_exc()

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    from pcg_tools.reader import read_pcg_file
    from pcg_tools.writer import write_pcg_file
    from pcg_tools.clipboard import get_clipboard
    from pcg_tools.batch_operations import BatchOperations
    from pcg_tools.models import Program, Combi, SetListSlot
    
    print("✓ All imports successful")

def test_file_operations():
    """Test basic file read/write operations."""
    print("Testing file operations...")
    
    from pcg_tools.reader import read_pcg_file
    from pcg_tools.writer import write_pcg_file
    
    # Read test file
    pcg = read_pcg_file("test_files/soundcheck_BASE_FOR_TESTING.PCG")
    assert pcg is not None, "Failed to read PCG file"
    assert len(pcg.program_banks) > 0, "No program banks found"
    assert len(pcg.combi_banks) > 0, "No combi banks found"
    assert len(pcg.set_lists) > 0, "No setlists found"
    
    print(f"✓ Read PCG file: {len(pcg.program_banks)} program banks, "
          f"{len(pcg.combi_banks)} combi banks, {len(pcg.set_lists)} setlists")
    
    # Write test file
    output_file = "test_files/test_all_features_output.PCG"
    write_pcg_file(pcg, output_file)
    
    # Verify written file
    pcg2 = read_pcg_file(output_file)
    assert pcg2 is not None, "Failed to read written file"
    
    print(f"✓ Write/read cycle successful")

def test_program_copy_paste():
    """Test program copy/paste functionality."""
    print("Testing program copy/paste...")
    
    from pcg_tools.reader import read_pcg_file
    from pcg_tools.clipboard import get_clipboard
    
    pcg = read_pcg_file("test_files/soundcheck_BASE_FOR_TESTING.PCG")
    bank = pcg.program_banks[0]
    
    clipboard = get_clipboard()
    
    # Copy program
    source = bank.patches[0]
    clipboard.copy_program(source)
    assert clipboard.has_program(), "Clipboard should have program"
    
    # Paste program
    target = bank.patches[10]
    original_name = target.name
    clipboard.paste_program(target)
    
    assert target.name == source.name, "Program name should match after paste"
    print(f"✓ Copied '{source.name}' to slot 10")

def test_slot_copy_paste():
    """Test setlist slot copy/paste functionality."""
    print("Testing slot copy/paste...")
    
    from pcg_tools.reader import read_pcg_file
    from pcg_tools.clipboard import get_clipboard
    
    pcg = read_pcg_file("test_files/soundcheck_BASE_FOR_TESTING.PCG")
    setlist = pcg.set_lists[0]
    
    clipboard = get_clipboard()
    
    if len(setlist.slots) > 0:
        # Copy slot
        source = setlist.slots[0]
        clipboard.copy_slot(source)
        assert clipboard.has_slot(), "Clipboard should have slot"
        
        # Paste slot
        if len(setlist.slots) > 1:
            target = setlist.slots[1]
            clipboard.paste_slot(target)
            assert target.name == source.name, "Slot name should match after paste"
            print(f"✓ Copied slot '{source.name}'")
        else:
            print("✓ Copy successful (not enough slots to test paste)")
    else:
        print("✓ No slots to test (skipped)")

def test_batch_operations():
    """Test batch operations."""
    print("Testing batch operations...")
    
    from pcg_tools.reader import read_pcg_file
    from pcg_tools.batch_operations import BatchOperations
    
    pcg = read_pcg_file("test_files/soundcheck_BASE_FOR_TESTING.PCG")
    bank = pcg.program_banks[0]
    
    original_count = len(bank.patches)
    
    # Test sort
    BatchOperations.sort_programs(bank, key="name")
    print(f"✓ Sorted {len(bank.patches)} programs by name")
    
    # Test move favorites
    bank.patches[0].favorite = True
    bank.patches[1].favorite = True
    BatchOperations.move_favorites_to_top(bank)
    assert bank.patches[0].favorite, "First patch should be favorite"
    print(f"✓ Moved favorites to top")
    
    # Test capitalize
    BatchOperations.capitalize_names(bank, style="upper")
    print(f"✓ Capitalized names")
    
    # Test remove duplicates
    bank.patches.append(bank.patches[0])  # Add duplicate
    BatchOperations.remove_duplicates(bank, by="name")
    print(f"✓ Removed duplicates")

def test_move_operations():
    """Test move up/down operations."""
    print("Testing move operations...")
    
    from pcg_tools.reader import read_pcg_file
    from pcg_tools.batch_operations import BatchOperations
    
    pcg = read_pcg_file("test_files/soundcheck_BASE_FOR_TESTING.PCG")
    bank = pcg.program_banks[0]
    
    # Test move down
    first_name = bank.patches[0].name
    result = BatchOperations.move_patch_down(bank, 0)
    assert result, "Move down should succeed"
    assert bank.patches[1].name == first_name, "Patch should have moved down"
    print(f"✓ Moved patch down")
    
    # Test move up
    result = BatchOperations.move_patch_up(bank, 1)
    assert result, "Move up should succeed"
    assert bank.patches[0].name == first_name, "Patch should have moved back up"
    print(f"✓ Moved patch up")

def test_file_safety():
    """Test file safety features."""
    print("Testing file safety features...")
    
    from pcg_tools.reader import read_pcg_file
    from pcg_tools.writer import write_pcg_file
    import os
    
    pcg = read_pcg_file("test_files/soundcheck_BASE_FOR_TESTING.PCG")
    
    # Test auto-backup
    test_file = "test_files/test_safety.PCG"
    backup_file = test_file + ".backup"
    
    # Create initial file
    write_pcg_file(pcg, test_file, create_backup=False)
    
    # Modify and save (should create backup)
    pcg.program_banks[0].patches[0].name = "Modified"
    write_pcg_file(pcg, test_file, create_backup=True)
    
    # Check backup was created
    assert os.path.exists(backup_file), "Backup file should be created"
    print(f"✓ Auto-backup created")
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)
    if os.path.exists(backup_file):
        os.remove(backup_file)

def test_cli_commands():
    """Test CLI commands."""
    print("Testing CLI commands...")
    
    import subprocess
    
    test_file = "test_files/soundcheck_BASE_FOR_TESTING.PCG"
    
    # Test info command
    result = subprocess.run(
        ["python3", "-m", "pcg_tools", "info", test_file],
        capture_output=True,
        text=True,
        cwd="."
    )
    assert result.returncode == 0, "Info command should succeed"
    assert "Korg Kronos" in result.stdout, "Should show model info"
    print(f"✓ CLI info command works")
    
    # Test list-patches command
    result = subprocess.run(
        ["python3", "-m", "pcg_tools", "list-patches", test_file],
        capture_output=True,
        text=True,
        cwd="."
    )
    assert result.returncode == 0, "List-patches command should succeed"
    print(f"✓ CLI list-patches command works")

def print_summary():
    """Print test summary."""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, result in test_results:
        print(f"{result:50} {test_name}")
    
    print("\n" + "="*60)
    print(f"Total Tests: {tests_passed + tests_failed}")
    print(f"Passed: {tests_passed} ✅")
    print(f"Failed: {tests_failed} ❌")
    print(f"Success Rate: {tests_passed/(tests_passed+tests_failed)*100:.1f}%")
    print("="*60)
    
    if tests_failed == 0:
        print("\n🎉 ALL TESTS PASSED! v1.3.0 is ready for release!")
        return 0
    else:
        print(f"\n⚠️  {tests_failed} test(s) failed. Please review errors above.")
        return 1

def main():
    """Run all tests."""
    print("="*60)
    print("PCG Tools v1.3.0 - Comprehensive Test Suite")
    print("="*60)
    
    # Run all tests
    run_test("Module Imports", test_imports)
    run_test("File Operations", test_file_operations)
    run_test("Program Copy/Paste", test_program_copy_paste)
    run_test("Slot Copy/Paste", test_slot_copy_paste)
    run_test("Batch Operations", test_batch_operations)
    run_test("Move Operations", test_move_operations)
    run_test("File Safety", test_file_safety)
    run_test("CLI Commands", test_cli_commands)
    
    # Print summary
    return print_summary()

if __name__ == "__main__":
    sys.exit(main())
