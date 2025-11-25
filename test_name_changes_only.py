#!/usr/bin/env python3
"""
Test Name Changes Only - This WILL Work!
=========================================
Since SLS1 name writing is implemented, we can test that the
basic read/write pipeline works by editing slot names.
"""

import sys
sys.path.insert(0, '.')

from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file

def main():
    input_file = 'test_files/soundcheck9_25_25_combined2.PCG'
    output_file = 'test_files/soundcheck_NAME_TEST.PCG'
    
    print("🎯 Name Change Test (This Works!)")
    print("=" * 60)
    print(f"\n📂 Loading: {input_file}")
    
    # Load PCG
    pcg = read_pcg_file(input_file)
    print(f"✓ Loaded {len(pcg.set_lists)} setlists")
    
    # Edit names in first setlist
    if pcg.set_lists:
        setlist = pcg.set_lists[0]
        original_name = setlist.name
        
        # Change setlist name
        setlist.name = "*** HARDWARE TEST ***"
        print(f"\n📝 Setlist name: '{original_name}' → '{setlist.name}'")
        
        # Change first 3 slot names
        print(f"\n📝 Slot name changes:")
        for i in range(min(3, len(setlist.slots))):
            slot = setlist.slots[i]
            if slot.name:
                original = slot.name
                slot.name = f"TEST SLOT {i+1}"
                print(f"   Slot {i}: '{original}' → '{slot.name}'")
    
    # Save
    print(f"\n💾 Saving to: {output_file}")
    write_pcg_file(pcg, output_file)
    print("✓ File saved")
    
    # Verify
    print("\n🔍 Verifying changes...")
    pcg_verify = read_pcg_file(output_file)
    setlist_verify = pcg_verify.set_lists[0]
    
    print(f"\n✅ Verification:")
    print(f"   Setlist name: {setlist_verify.name}")
    for i in range(min(3, len(setlist_verify.slots))):
        slot = setlist_verify.slots[i]
        print(f"   Slot {i}: {slot.name}")
    
    print("\n" + "=" * 60)
    print("🎯 HARDWARE TEST INSTRUCTIONS")
    print("=" * 60)
    print(f"\n1. Copy to USB: {output_file}")
    print("2. Load on Kronos")
    print("3. Check first setlist:")
    print(f"   - Name should be: *** HARDWARE TEST ***")
    print(f"   - First 3 slots should be: TEST SLOT 1, TEST SLOT 2, TEST SLOT 3")
    print("\n4. If names appear correctly, the read/write pipeline WORKS!")
    print("   (Transpose/text_size need more work)")
    print("=" * 60)

if __name__ == '__main__':
    main()
