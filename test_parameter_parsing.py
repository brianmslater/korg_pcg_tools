#!/usr/bin/env python3
"""Test script to verify program and combi parameter parsing."""

import sys
from pcg_tools.reader import read_pcg_file

def test_parameter_parsing(pcg_file):
    """Test parsing of program and combi parameters."""
    print(f"Testing parameter parsing on: {pcg_file}\n")
    
    # Parse the PCG file
    pcg = read_pcg_file(pcg_file)
    
    # Test Program Parameters
    print("=" * 80)
    print("PROGRAM PARAMETERS TEST")
    print("=" * 80)
    
    programs = pcg.get_all_programs()[:10]  # Test first 10 programs
    
    for prog in programs:
        if prog.name and not prog.name.startswith("[Empty"):
            print(f"\n{prog.id}: {prog.name}")
            print(f"  Engine: {prog.engine}")
            print(f"  OSC Mode: {prog.osc_mode}")
            print(f"  Favorite: {prog.favorite}")
            if prog.category:
                print(f"  Category: {prog.category.main_category} / SubCategory: {prog.category.sub_category}")
    
    # Test Combi Parameters
    print("\n" + "=" * 80)
    print("COMBI PARAMETERS TEST")
    print("=" * 80)
    
    combis = pcg.get_all_combis()[:10]  # Test first 10 combis
    
    for combi in combis:
        if combi.name and not combi.name.startswith("[Empty"):
            print(f"\n{combi.id}: {combi.name}")
            print(f"  Tempo: {combi.tempo} BPM")
            print(f"  Favorite: {combi.favorite}")
            if combi.category:
                print(f"  Category: {combi.category.main_category} / SubCategory: {combi.category.sub_category}")
            print(f"  Timbres: {len(combi.timbres)}")
            
            # Show first 3 active timbres
            active_timbres = [t for t in combi.timbres if t.status != "OFF"][:3]
            for i, timbre in enumerate(active_timbres):
                print(f"    Timbre {i+1}: {timbre.program_id} (Ch {timbre.midi_channel})")
                print(f"      Status: {timbre.status}, Vol: {timbre.volume}, Pan: {timbre.pan}")
                print(f"      Detune: {timbre.detune}, Transpose: {timbre.transpose}")
                print(f"      Key Zone: {timbre.bottom_key}-{timbre.top_key}")
                print(f"      Vel Zone: {timbre.bottom_velocity}-{timbre.top_velocity}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_parameter_parsing.py <pcg_file>")
        sys.exit(1)
    
    test_parameter_parsing(sys.argv[1])
