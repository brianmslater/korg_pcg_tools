#!/usr/bin/env python3
"""Test the advanced copy/paste features."""

import sys
from pcg_tools.reader import read_pcg_file
from pcg_tools.advanced_clipboard import get_advanced_clipboard
from pcg_tools.copy_paste_dialog import get_copy_paste_settings
from pcg_tools.reference_tracker import ReferenceTracker


def test_single_file(test_file):
    """Test advanced features on a single file."""
    print("\n" + "="*80)
    print(f"TESTING: {test_file}")
    print("="*80)
    
    try:
        pcg = read_pcg_file(test_file)
        print(f"[OK] Loaded: {pcg.header.model.value}")
        print(f"  Program banks: {len(pcg.program_banks)}")
        print(f"  Combi banks: {len(pcg.combi_banks)}")
    except Exception as e:
        print(f"[FAIL] Failed to load: {e}")
        return False
    
    # Test reference tracking
    print("\n" + "="*50)
    print("TEST 1: REFERENCE TRACKING")
    print("="*50)
    
    try:
        ref_tracker = pcg.get_reference_tracker()
        print("[OK] Reference tracker created")
        
        # Test program usage - check ALL programs in the file
        program_count = 0
        used_count = 0
        usage_examples = []
        
        for bank in pcg.program_banks:
            for i, program in enumerate(bank.patches):
                program_count += 1
                usage = ref_tracker.get_usage_count(program.id)
                if usage > 0:
                    used_count += 1
                    usage_examples.append((program.id, program.name, usage))
                # Debug first program
                if i == 0:
                    print(f"  Debug: First program ID: {program.id}, usage: {usage}")
        
        # Show top 5 most used programs
        usage_examples.sort(key=lambda x: x[2], reverse=True)
        if usage_examples:
            print(f"\n  Top 5 most used programs:")
            for prog_id, name, usage in usage_examples[:5]:
                name_display = name[:20] if name else "(empty)"
                # Handle Unicode encoding issues
                try:
                    print(f"  {prog_id} - {name_display:20} used by {usage} combi(s)")
                except UnicodeEncodeError:
                    name_safe = name_display.encode('ascii', errors='replace').decode('ascii')
                    print(f"  {prog_id} - {name_safe:20} used by {usage} combi(s)")
        else:
            print(f"\n  No programs found with usage data")
        
        print(f"\n[OK] Found {program_count} total programs, {used_count} are used by combis")
        
    except Exception as e:
        print(f"[FAIL] Reference tracking failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test combi program references
    print("\n" + "="*50)
    print("TEST 2: COMBI PROGRAM REFERENCES")
    print("="*50)
    
    try:
        combi_count = 0
        for bank in pcg.combi_banks:
            for combi in bank.patches:
                if combi.name.strip():
                    combi_count += 1
                    programs = ref_tracker.get_combi_programs(combi.id)
                    if combi_count <= 3:  # Show first 3
                        print(f"  {combi.id} - {combi.name[:20]:20} uses {len(programs)} program(s)")
                        for prog_id in list(programs)[:3]:
                            print(f"    -> {prog_id}")
        
        print(f"\n[OK] Analyzed {combi_count} combis")
        
    except Exception as e:
        print(f"[FAIL] Combi analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test advanced clipboard
    print("\n" + "="*50)
    print("TEST 3: ADVANCED CLIPBOARD")
    print("="*50)
    
    try:
        clipboard = get_advanced_clipboard()
        
        # Copy some programs
        test_programs = []
        for bank in pcg.program_banks:
            for program in bank.patches[:3]:
                if program.name.strip():
                    test_programs.append(program)
                    break
            if test_programs:
                break
        
        if test_programs:
            clipboard.copy_programs(test_programs, test_file)
            print(f"[OK] Copied {len(test_programs)} program(s)")
            print(f"  {clipboard.get_summary()}")
        
        # Copy a combi with dependencies
        test_combi = None
        for bank in pcg.combi_banks:
            for combi in bank.patches:
                if combi.name.strip():
                    test_combi = combi
                    break
            if test_combi:
                break
        
        if test_combi:
            clipboard.copy_combis([test_combi], pcg, test_file)
            print(f"[OK] Copied combi with dependencies")
            print(f"  {clipboard.get_summary()}")
        
    except Exception as e:
        print(f"[FAIL] Clipboard test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def test_advanced_features():
    """Test advanced copy/paste features on multiple files."""
    print("="*80)
    print("ADVANCED FEATURES TEST - MULTIPLE FILES")
    print("="*80)
    
    test_files = [
        "test_files/files/GLAM V3/GLAMV3.PCG",
        r"E:\Downloads\KRONOS 3 Ultimate Covers 128  (1)\KRONOS 3 Ultimate Covers 128\Narf Ultimate Covers K3.PCG",
        r"E:\Downloads\Audora-80s90s-v2 (1)\AUDORA-80's90's.PCG"
    ]
    
    all_passed = True
    results = []
    
    for test_file in test_files:
        try:
            success = test_single_file(test_file)
            results.append((test_file, "PASSED" if success else "FAILED"))
            if not success:
                all_passed = False
        except Exception as e:
            print(f"\n[FAIL] Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_file, f"ERROR: {e}"))
            all_passed = False
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    for test_file, result in results:
        file_name = test_file.split("\\")[-1] if "\\" in test_file else test_file.split("/")[-1]
        print(f"  {file_name:40} {result}")
    
    print("\n" + "="*80)
    if all_passed:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED!")
    print("="*80)
    
    return all_passed


if __name__ == "__main__":
    success = test_advanced_features()
    sys.exit(0 if success else 1)
