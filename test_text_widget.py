#!/usr/bin/env python3
"""Test with Text widget instead - more reliable on old macOS Tk."""

import tkinter as tk
from tkinter import ttk, font as tkfont
from pathlib import Path
import sys
import os

os.environ['TK_SILENCE_DEPRECATION'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcg_tools.reader import read_pcg_file

TEST_FILE = "/Volumes/KEYBOARD/Nightwish Legacy/KRONOS/nw.PCG"

print(f"\n{'='*70}")
print(f"TEXT WIDGET TEST - Using Text widget instead of Listbox/Treeview")
print(f"{'='*70}")
print(f"Loading: {TEST_FILE}")

try:
    pcg = read_pcg_file(TEST_FILE)
    print(f"✓ File loaded: {len(pcg.program_banks)} program banks, {len(pcg.combi_banks)} combi banks")
    
    root = tk.Tk()
    root.title(f"Text Widget Test - {Path(TEST_FILE).name}")
    root.geometry("900x600")
    
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Programs tab with Text widget
    programs_frame = ttk.Frame(notebook)
    notebook.add(programs_frame, text="Programs")
    
    # Header
    header = ttk.Label(programs_frame, text="ID          Name                                     Category             Fav", 
                      font=('Monaco', 11), anchor=tk.W, background='lightgray')
    header.pack(fill=tk.X, pady=(0, 2))
    
    # Text widget with scrollbar
    text_frame = ttk.Frame(programs_frame)
    text_frame.pack(fill=tk.BOTH, expand=True)
    
    text_widget = tk.Text(text_frame, font=('Monaco', 11), wrap=tk.NONE, state=tk.NORMAL)
    scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Populate programs
    print(f"\nPopulating programs text widget...")
    count = 0
    for bank in pcg.program_banks:
        print(f"  Bank {bank.bank_id}: {len(bank.patches)} patches")
        for i, prog in enumerate(bank.patches):
            cat = prog.category.name if prog.category else ""
            fav = "✓" if prog.favorite else " "
            
            line = f"{prog.id:<12}{prog.name:<41}{cat:<21}{fav}\n"
            text_widget.insert(tk.END, line)
            count += 1
            
            if i < 5:
                print(f"    [{i}] {prog.id}: {prog.name}")
    
    text_widget.config(state=tk.DISABLED)  # Make read-only
    print(f"  Total: {count} programs inserted")
    
    # Combis tab
    combis_frame = ttk.Frame(notebook)
    notebook.add(combis_frame, text="Combis")
    
    header2 = ttk.Label(combis_frame, text="ID          Name                                     Category             Fav", 
                       font=('Monaco', 11), anchor=tk.W, background='lightgray')
    header2.pack(fill=tk.X, pady=(0, 2))
    
    text_frame2 = ttk.Frame(combis_frame)
    text_frame2.pack(fill=tk.BOTH, expand=True)
    
    text_widget2 = tk.Text(text_frame2, font=('Monaco', 11), wrap=tk.NONE, state=tk.NORMAL)
    scrollbar2 = ttk.Scrollbar(text_frame2, orient=tk.VERTICAL, command=text_widget2.yview)
    text_widget2.configure(yscrollcommand=scrollbar2.set)
    
    text_widget2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Populate combis
    print(f"\nPopulating combis text widget...")
    count = 0
    for bank in pcg.combi_banks:
        print(f"  Bank {bank.bank_id}: {len(bank.patches)} patches")
        for i, combi in enumerate(bank.patches):
            cat = combi.category.name if combi.category else ""
            fav = "✓" if combi.favorite else " "
            
            line = f"{combi.id:<12}{combi.name:<41}{cat:<21}{fav}\n"
            text_widget2.insert(tk.END, line)
            count += 1
            
            if i < 5:
                print(f"    [{i}] {combi.id}: {combi.name}")
    
    text_widget2.config(state=tk.DISABLED)
    print(f"  Total: {count} combis inserted")
    
    # Status
    status = ttk.Label(root, text=f"Loaded: {Path(TEST_FILE).name} - Text widget view", relief=tk.SUNKEN)
    status.pack(side=tk.BOTTOM, fill=tk.X)
    
    print(f"\n{'='*70}")
    print(f"✓ TEXT WIDGET GUI CREATED")
    print(f"  Text widgets are more reliable than Listbox/Treeview on old Tk")
    print(f"  Can you see the patch data now?")
    print(f"{'='*70}\n")
    
    root.mainloop()
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
