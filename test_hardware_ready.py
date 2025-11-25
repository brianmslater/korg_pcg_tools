#!/usr/bin/env python3
"""
Hardware Testing Script
=======================
This script helps you prepare a PCG file for testing on your Kronos hardware.

It will:
1. Load a PCG file with setlists
2. Show you what's in it
3. Let you make test edits via GUI
4. Save a test version for hardware testing

Usage:
    python test_hardware_ready.py [input_file.PCG]
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, '.')

from PySide6.QtWidgets import QApplication
from pcg_tools.gui_qt import PcgMainWindow
from pcg_tools.reader import read_pcg_file


def analyze_pcg(filepath):
    """Analyze a PCG file and show what's in it."""
    print(f"\n{'='*60}")
    print(f"Analyzing: {filepath}")
    print(f"{'='*60}\n")
    
    pcg = read_pcg_file(filepath)
    
    print(f"✓ File loaded successfully")
    print(f"  Size: {os.path.getsize(filepath):,} bytes")
    
    # Check for setlists
    if pcg.set_lists:
        print(f"\n📋 Found {len(pcg.set_lists)} setlist(s):")
        for i, setlist in enumerate(pcg.set_lists, 1):
            print(f"\n  Setlist {i}: {setlist.name}")
            print(f"    Slots: {len(setlist.slots)}")
            
            # Show first few non-empty slots
            non_empty = [s for s in setlist.slots if s.name and s.name.strip()]
            if non_empty:
                print(f"    Non-empty slots: {len(non_empty)}")
                print(f"\n    Sample slots:")
                for slot in non_empty[:3]:
                    print(f"      Slot {slot.slot_index}: {slot.name}")
                    print(f"        Type: {slot.patch_type}, Bank: {slot.patch_bank}, Index: {slot.patch_index}")
                    print(f"        Text Size: {slot.text_size_name}, Transpose: {slot.transpose}")
                    if slot.color:
                        print(f"        Color: {slot.color_name}")
    else:
        print("\n⚠️  No setlists found in this file")
    
    # Check for programs
    if pcg.program_banks:
        total_programs = sum(len([p for p in bank.patches if p]) for bank in pcg.program_banks)
        print(f"\n🎹 Found {total_programs} program(s)")
    
    # Check for combis
    if pcg.combi_banks:
        total_combis = sum(len([c for c in bank.patches if c]) for bank in pcg.combi_banks)
        print(f"🎼 Found {total_combis} combi(s)")
    
    print(f"\n{'='*60}\n")
    
    return pcg


def main():
    # Find a test file
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        # Look for test files
        test_files = [
            "test_files/test_soundcheck9_25_25_combined.PCG",
            "SETLIST Movie TV Themes LOAD SEPARATELY.PCG",
            "test_files/test_output_nw.PCG",
        ]
        
        input_file = None
        for f in test_files:
            if os.path.exists(f):
                input_file = f
                break
        
        if not input_file:
            print("❌ No PCG file specified and no test files found")
            print("\nUsage: python test_hardware_ready.py <file.PCG>")
            print("\nOr place a PCG file in the current directory")
            return 1
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return 1
    
    # Analyze the file
    try:
        pcg = analyze_pcg(input_file)
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    if not pcg.set_lists:
        print("This file has no setlists to edit.")
        return 1
    
    # Prepare output filename
    base = os.path.splitext(input_file)[0]
    output_file = f"{base}_HARDWARE_TEST.PCG"
    
    print(f"🎯 TESTING INSTRUCTIONS")
    print(f"{'='*60}")
    print(f"\n1. The GUI will now open")
    print(f"2. Make some test edits:")
    print(f"   - Change text sizes (Small/Medium/Large)")
    print(f"   - Adjust transpose values")
    print(f"   - Edit descriptions")
    print(f"   - Change colors")
    print(f"\n3. Click 'Save PCG' when done")
    print(f"4. Output will be saved as:")
    print(f"   {output_file}")
    print(f"\n5. Load this file on your Kronos and verify:")
    print(f"   ✓ Setlists appear correctly")
    print(f"   ✓ Text sizes display as expected")
    print(f"   ✓ Transpose values work")
    print(f"   ✓ Colors show properly")
    print(f"   ✓ Descriptions are correct")
    print(f"\n{'='*60}\n")
    
    input("Press Enter to launch the GUI...")
    
    # Launch GUI
    app = QApplication(sys.argv)
    window = PcgMainWindow()
    window.show()
    
    # Load the file
    window.pcg = pcg
    window.filepath = input_file
    window.is_dirty = False
    
    # Hide welcome, show content
    window.welcome_widget.hide()
    window.content_widget.show()
    
    # Load all data
    window.load_programs()
    window.load_combis()
    window.load_setlists()
    
    # Update window title
    from pathlib import Path
    window.setWindowTitle(f"PCG Tools - {Path(input_file).name} [HARDWARE TEST]")
    window.statusbar.showMessage(f"Loaded: {Path(input_file).name} - Ready for testing")
    
    print(f"\n✓ GUI launched successfully")
    print(f"✓ Go to the 'Set Lists' tab to make your edits")
    print(f"✓ When done, use File > Save As: {output_file}\n")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
