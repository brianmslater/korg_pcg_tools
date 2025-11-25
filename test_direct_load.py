#!/usr/bin/env python3
"""Direct test - automatically loads a PCG file and displays it."""

import tkinter as tk
from tkinter import ttk
from pathlib import Path
import sys
import os

# Suppress Tk warning
os.environ['TK_SILENCE_DEPRECATION'] = '1'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcg_tools.reader import read_pcg_file

# Test file - change this to any PCG file on your KEYBOARD device
TEST_FILE = "/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG"

print(f"\n{'='*70}")
print(f"DIRECT LOAD TEST")
print(f"{'='*70}")
print(f"Loading: {TEST_FILE}")

try:
    pcg = read_pcg_file(TEST_FILE)
    print(f"✓ File loaded successfully!")
    print(f"  Program banks: {len(pcg.program_banks)}")
    print(f"  Combi banks: {len(pcg.combi_banks)}")
    
    # Create GUI
    root = tk.Tk()
    root.title(f"PCG Test - {Path(TEST_FILE).name}")
    root.geometry("900x600")
    
    # Create notebook
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Programs tab
    programs_frame = ttk.Frame(notebook)
    notebook.add(programs_frame, text=f"Programs ({sum(len(b.patches) for b in pcg.program_banks)})")
    
    columns = ('ID', 'Name', 'Category', 'Favorite')
    programs_tree = ttk.Treeview(programs_frame, columns=columns, show='tree headings', selectmode='extended')
    
    programs_tree.heading('#0', text='Bank')
    programs_tree.heading('ID', text='ID')
    programs_tree.heading('Name', text='Name')
    programs_tree.heading('Category', text='Category')
    programs_tree.heading('Favorite', text='Fav')
    
    programs_tree.column('#0', width=100)
    programs_tree.column('ID', width=100)
    programs_tree.column('Name', width=400)
    programs_tree.column('Category', width=150)
    programs_tree.column('Favorite', width=50)
    
    scrollbar = ttk.Scrollbar(programs_frame, orient=tk.VERTICAL, command=programs_tree.yview)
    programs_tree.configure(yscrollcommand=scrollbar.set)
    
    programs_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Populate programs
    print(f"\nPopulating programs tree...")
    for bank in pcg.program_banks:
        print(f"  Bank {bank.bank_id}: {len(bank.patches)} patches")
        bank_node = programs_tree.insert('', 'end', text=f"Bank {bank.bank_id}")
        for i, prog in enumerate(bank.patches):
            cat = prog.category.name if prog.category else ""
            fav = "✓" if prog.favorite else ""
            programs_tree.insert(bank_node, 'end', values=(prog.id, prog.name, cat, fav))
            if i < 5:
                print(f"    [{i}] {prog.id}: {prog.name}")
    
    # Combis tab
    combis_frame = ttk.Frame(notebook)
    notebook.add(combis_frame, text=f"Combis ({sum(len(b.patches) for b in pcg.combi_banks)})")
    
    combis_tree = ttk.Treeview(combis_frame, columns=columns, show='tree headings', selectmode='extended')
    
    combis_tree.heading('#0', text='Bank')
    combis_tree.heading('ID', text='ID')
    combis_tree.heading('Name', text='Name')
    combis_tree.heading('Category', text='Category')
    combis_tree.heading('Favorite', text='Fav')
    
    combis_tree.column('#0', width=100)
    combis_tree.column('ID', width=100)
    combis_tree.column('Name', width=400)
    combis_tree.column('Category', width=150)
    combis_tree.column('Favorite', width=50)
    
    scrollbar2 = ttk.Scrollbar(combis_frame, orient=tk.VERTICAL, command=combis_tree.yview)
    combis_tree.configure(yscrollcommand=scrollbar2.set)
    
    combis_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Populate combis
    print(f"\nPopulating combis tree...")
    for bank in pcg.combi_banks:
        print(f"  Bank {bank.bank_id}: {len(bank.patches)} patches")
        bank_node = combis_tree.insert('', 'end', text=f"Bank {bank.bank_id}")
        for i, combi in enumerate(bank.patches):
            cat = combi.category.name if combi.category else ""
            fav = "✓" if combi.favorite else ""
            combis_tree.insert(bank_node, 'end', values=(combi.id, combi.name, cat, fav))
            if i < 5:
                print(f"    [{i}] {combi.id}: {combi.name}")
    
    # Status
    status = ttk.Label(root, text=f"Loaded: {Path(TEST_FILE).name}", relief=tk.SUNKEN)
    status.pack(side=tk.BOTTOM, fill=tk.X)
    
    print(f"\n{'='*70}")
    print(f"✓ GUI CREATED - Check if patches are visible in the window")
    print(f"{'='*70}\n")
    
    root.mainloop()
    
except FileNotFoundError:
    print(f"\n✗ ERROR: File not found: {TEST_FILE}")
    print(f"\nAvailable test files:")
    print(f"  - /Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG")
    print(f"  - /Volumes/KEYBOARD/Narf Sounds Movie TV Themes/Narf Sounds Movie TV Themes.PCG")
    print(f"\nEdit TEST_FILE variable in this script to use a different file.\n")
    sys.exit(1)
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
