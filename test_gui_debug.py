#!/usr/bin/env python3
"""Debug GUI loading to see what's happening."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import sys
import os

# Suppress Tk warning
os.environ['TK_SILENCE_DEPRECATION'] = '1'

# Add to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pcg_tools.reader import read_pcg_file
from pcg_tools.operations import PatchOperations

class DebugPcgWindow:
    """Debug version of PCG window with print statements."""
    
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Debug PCG Window")
        self.window.geometry("900x600")
        
        self.pcg = None
        self.filepath = None
        
        print("Creating widgets...")
        self._create_widgets()
        print("Widgets created!")
        
    def _create_widgets(self):
        # Top frame with radio buttons
        top_frame = ttk.Frame(self.window)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.view_var = tk.StringVar(value="programs")
        
        ttk.Radiobutton(top_frame, text="Programs", variable=self.view_var, 
                       value="programs", command=self._switch_view).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(top_frame, text="Combis", variable=self.view_var, 
                       value="combis", command=self._switch_view).pack(side=tk.LEFT, padx=5)
        
        # Content frame
        self.content_frame = ttk.Frame(self.window)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Programs view
        self.programs_frame = ttk.Frame(self.content_frame)
        self._create_patch_list(self.programs_frame, "programs")
        
        # Combis view
        self.combis_frame = ttk.Frame(self.content_frame)
        self._create_patch_list(self.combis_frame, "combis")
        
        # Show programs by default
        self.programs_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button frame
        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Open PCG File", command=self.open_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", command=self.window.destroy).pack(side=tk.RIGHT, padx=5)
        
    def _create_patch_list(self, parent, list_type):
        columns = ('ID', 'Name', 'Category', 'Favorite')
        tree = ttk.Treeview(parent, columns=columns, show='tree headings', selectmode='extended')
        
        tree.heading('#0', text='Bank')
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Name')
        tree.heading('Category', text='Category')
        tree.heading('Favorite', text='Fav')
        
        tree.column('#0', width=100)
        tree.column('ID', width=100)
        tree.column('Name', width=400)
        tree.column('Category', width=150)
        tree.column('Favorite', width=50)
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        if list_type == "programs":
            self.programs_tree = tree
        else:
            self.combis_tree = tree
            
    def _switch_view(self):
        self.programs_frame.pack_forget()
        self.combis_frame.pack_forget()
        
        view = self.view_var.get()
        if view == "programs":
            self.programs_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.combis_frame.pack(fill=tk.BOTH, expand=True)
    
    def open_file(self):
        filename = filedialog.askopenfilename(
            title="Open PCG File",
            initialdir="/Volumes/KEYBOARD",
            filetypes=[("PCG Files", "*.PCG *.pcg"), ("All Files", "*.*")]
        )
        
        if filename:
            print(f"\n{'='*60}")
            print(f"Opening file: {filename}")
            self.load_file(filename)
            
    def load_file(self, filepath):
        try:
            print(f"Reading PCG file...")
            self.pcg = read_pcg_file(filepath)
            self.filepath = filepath
            
            print(f"✓ File loaded successfully!")
            print(f"  Program banks: {len(self.pcg.program_banks)}")
            print(f"  Combi banks: {len(self.pcg.combi_banks)}")
            
            print(f"\nCalling _update_display()...")
            self._update_display()
            print(f"✓ Display updated!")
            
            self.window.title(f"Debug PCG - {Path(filepath).name}")
            messagebox.showinfo("Success", f"Loaded {Path(filepath).name}", parent=self.window)
            
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to open file:\n{e}", parent=self.window)
    
    def _update_display(self):
        if not self.pcg:
            print("  No PCG loaded, skipping display update")
            return
        
        print(f"  Updating programs tree...")
        self.programs_tree.delete(*self.programs_tree.get_children())
        for bank in self.pcg.program_banks:
            print(f"    Adding bank {bank.bank_id} with {len(bank.patches)} patches")
            bank_node = self.programs_tree.insert('', 'end', text=f"Bank {bank.bank_id}")
            for i, prog in enumerate(bank.patches):
                cat = prog.category.name if prog.category else ""
                fav = "✓" if prog.favorite else ""
                self.programs_tree.insert(bank_node, 'end', values=(prog.id, prog.name, cat, fav))
                if i < 3:  # Show first 3
                    print(f"      [{i}] {prog.id}: {prog.name}")
        
        print(f"  Updating combis tree...")
        self.combis_tree.delete(*self.combis_tree.get_children())
        for bank in self.pcg.combi_banks:
            print(f"    Adding bank {bank.bank_id} with {len(bank.patches)} patches")
            bank_node = self.combis_tree.insert('', 'end', text=f"Bank {bank.bank_id}")
            for i, combi in enumerate(bank.patches):
                cat = combi.category.name if combi.category else ""
                fav = "✓" if combi.favorite else ""
                self.combis_tree.insert(bank_node, 'end', values=(combi.id, combi.name, cat, fav))
                if i < 3:  # Show first 3
                    print(f"      [{i}] {combi.id}: {combi.name}")

# Main app
root = tk.Tk()
root.title("PCG Tools Debug")
root.geometry("400x200")

ttk.Label(root, text="PCG Tools - Debug Mode", font=('Arial', 14, 'bold')).pack(pady=20)
ttk.Label(root, text="Click button to open a debug window").pack(pady=10)

def open_debug_window():
    window = DebugPcgWindow(root)

ttk.Button(root, text="Open Debug Window", command=open_debug_window).pack(pady=10)

print("\n" + "="*60)
print("DEBUG MODE - PCG Tools")
print("="*60)
print("Watch console output to see what happens when loading files")
print("="*60 + "\n")

root.mainloop()
