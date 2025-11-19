#!/usr/bin/env python3
"""Test the advanced copy/paste features."""

import sys
from pcg_tools.reader import read_pcg_file
from pcg_tools.advanced_clipboard import get_advanced_clipboard
from pcg_tools.copy_paste_dialog import get_copy_paste_settings
from pcg_tools.reference_tracker import ReferenceTracker


def test_advanced_features():
    """Test advanced copy/paste features."""
    print("="*80)
    print("ADVANCED FEATURES TEST")
    print("="*80)
    
    # Load test file
    test_file = "test_files/files/GLAM V3/GLAMV3.PCG"
    print(f"\nLoading test file: {test_file}")
    
    try:
        pcg = read_pcg_file(test_file)
        print(f"✓ Loaded: {pcg.header.model.value}")
        print(f"  Program banks: {len(pcg.program_banks)}")
        print(f"  Combi banks: {len(pcg.combi_banks)}")
    except Exception as e:
        print(f"✗ Failed to load: {e}")
        return False
    
    # Test reference tracking
    print("\n" + "="*50)
    print("TEST 1: REFERENCE TRACKING")
    print("="*50)
    
    try:
        ref_tracker = pcg.get_reference_tracker()
        print("✓ Reference tracker created")
        
        # Test program usage
        program_count = 0
        used_count = 0
        
        for bank in pcg.program_banks:
            for program in bank.patches:
                if program.name.strip():
                    program_count += 1
                    usage = ref_tracker.get_usage_count(program.id)
                    if usage > 0:
                        used_count += 1
                        if used_count <= 5:  # Show first 5
                            print(f"  {program.id} - {program.name[:20]:20} used by {usage} combi(s)")
        
        print(f"\n✓ Found {program_count} programs, {used_count} are used by combis")
        
    except Exception as e:
        print(f"✗ Reference tracking failed: {e}")
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
                            print(f"    → {prog_id}")
        
        print(f"\n✓ Analyzed {combi_count} combis")
        
    except Exception as e:
        print(f"✗ Combi analysis failed: {e}")
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
            print(f"✓ Copied {len(test_programs)} program(s)")
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
            print(f"✓ Copied combi with dependencies")
            print(f"  {clipboard.get_summary()}")
        
    except Exception as e:
        print(f"✗ Clipboard test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*80)
    print("ALL TESTS PASSED!")
    print("="*80)
    return True


if __name__ == "__main__":
    success = test_advanced_features()
    sys.exit(0 if success else 1)
