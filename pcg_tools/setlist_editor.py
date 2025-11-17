"""Set list editing dialog."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from .models import SetListSlot, PcgFile


class SetListSlotEditor:
    """Dialog for editing set list slots."""
    
    def __init__(self, parent, slot: SetListSlot, pcg: PcgFile):
        self.slot = slot
        self.pcg = pcg
        self.result = None
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Edit Set List Slot {slot.slot_index:03d}")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.geometry("500x400")
        self._center_dialog(parent)
        
        self._create_widgets()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def _center_dialog(self, parent):
        """Center dialog on parent window."""
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.dialog.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
    
    def _create_widgets(self):
        """Create dialog widgets."""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # Slot name
        ttk.Label(main_frame, text="Slot Name:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar(value=self.slot.name)
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=40)
        name_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Patch selection
        ttk.Label(main_frame, text="Patch:").grid(row=row, column=0, sticky=tk.W, pady=5)
        patch_frame = ttk.Frame(main_frame)
        patch_frame.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Patch type
        self.patch_type_var = tk.StringVar(value=self.slot.patch_type or "Program")
        ttk.Radiobutton(patch_frame, text="Program", variable=self.patch_type_var, 
                       value="Program", command=self._on_patch_type_changed).pack(side=tk.LEFT)
        ttk.Radiobutton(patch_frame, text="Combi", variable=self.patch_type_var, 
                       value="Combi", command=self._on_patch_type_changed).pack(side=tk.LEFT, padx=10)
        row += 1
        
        # Patch selection dropdown
        ttk.Label(main_frame, text="Select Patch:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.patch_var = tk.StringVar(value=self.slot.patch_id or "")
        self.patch_combo = ttk.Combobox(main_frame, textvariable=self.patch_var, width=37, state='readonly')
        self.patch_combo.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        self._update_patch_list()
        row += 1
        
        # Transpose
        ttk.Label(main_frame, text="Transpose:").grid(row=row, column=0, sticky=tk.W, pady=5)
        transpose_frame = ttk.Frame(main_frame)
        transpose_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        self.transpose_var = tk.IntVar(value=self.slot.transpose)
        transpose_spin = ttk.Spinbox(transpose_frame, from_=-24, to=24, textvariable=self.transpose_var, width=10)
        transpose_spin.pack(side=tk.LEFT)
        ttk.Label(transpose_frame, text="semitones (-24 to +24)").pack(side=tk.LEFT, padx=10)
        row += 1
        
        # Volume
        ttk.Label(main_frame, text="Volume:").grid(row=row, column=0, sticky=tk.W, pady=5)
        volume_frame = ttk.Frame(main_frame)
        volume_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        self.volume_var = tk.IntVar(value=self.slot.volume)
        volume_spin = ttk.Spinbox(volume_frame, from_=0, to=127, textvariable=self.volume_var, width=10)
        volume_spin.pack(side=tk.LEFT)
        ttk.Label(volume_frame, text="(0-127)").pack(side=tk.LEFT, padx=10)
        row += 1
        
        # Notes
        ttk.Label(main_frame, text="Notes:").grid(row=row, column=0, sticky=(tk.W, tk.N), pady=5)
        notes_frame = ttk.Frame(main_frame)
        notes_frame.grid(row=row, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        notes_frame.columnconfigure(0, weight=1)
        notes_frame.rowconfigure(0, weight=1)
        
        self.notes_text = tk.Text(notes_frame, height=8, width=40, wrap=tk.WORD)
        self.notes_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.notes_text.insert('1.0', self.slot.notes or "")
        
        notes_scroll = ttk.Scrollbar(notes_frame, orient=tk.VERTICAL, command=self.notes_text.yview)
        notes_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.notes_text.config(yscrollcommand=notes_scroll.set)
        
        main_frame.rowconfigure(row, weight=1)
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="OK", command=self._on_ok, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel, width=10).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter/Escape
        self.dialog.bind('<Return>', lambda e: self._on_ok())
        self.dialog.bind('<Escape>', lambda e: self._on_cancel())
    
    def _update_patch_list(self):
        """Update the patch selection list based on type."""
        patches = []
        
        if self.patch_type_var.get() == "Program":
            for bank in self.pcg.program_banks:
                for prog in bank.patches:
                    if prog.name.strip():  # Only show non-empty patches
                        patches.append(f"{prog.id} - {prog.name}")
        else:  # Combi
            for bank in self.pcg.combi_banks:
                for combi in bank.patches:
                    if combi.name.strip():  # Only show non-empty patches
                        patches.append(f"{combi.id} - {combi.name}")
        
        self.patch_combo['values'] = patches
        
        # Try to select current patch
        current = self.slot.patch_id
        if current:
            for i, patch in enumerate(patches):
                if patch.startswith(current):
                    self.patch_combo.current(i)
                    break
    
    def _on_patch_type_changed(self):
        """Handle patch type change."""
        self._update_patch_list()
    
    def _on_ok(self):
        """Handle OK button."""
        # Validate
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Slot name cannot be empty", parent=self.dialog)
            return
        
        if len(name) > 24:
            messagebox.showerror("Error", "Slot name cannot exceed 24 characters", parent=self.dialog)
            return
        
        # Get selected patch
        patch_str = self.patch_var.get()
        if patch_str:
            patch_id = patch_str.split(' - ')[0]
        else:
            patch_id = ""
        
        # Get notes
        notes = self.notes_text.get('1.0', tk.END).strip()
        
        # Update slot
        self.slot.name = name
        self.slot.patch_type = self.patch_type_var.get()
        self.slot.patch_id = patch_id
        self.slot.transpose = self.transpose_var.get()
        self.slot.volume = self.volume_var.get()
        self.slot.notes = notes
        
        self.result = True
        self.dialog.destroy()
    
    def _on_cancel(self):
        """Handle Cancel button."""
        self.result = False
        self.dialog.destroy()


class SetListEditor:
    """Dialog for editing set list properties."""
    
    def __init__(self, parent, setlist):
        self.setlist = setlist
        self.result = None
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Edit Set List: {setlist.name}")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.geometry("400x250")
        self._center_dialog(parent)
        
        self._create_widgets()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def _center_dialog(self, parent):
        """Center dialog on parent window."""
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.dialog.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
    
    def _create_widgets(self):
        """Create dialog widgets."""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # Set list name
        ttk.Label(main_frame, text="Name:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar(value=self.setlist.name)
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=40)
        name_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Description
        ttk.Label(main_frame, text="Description:").grid(row=row, column=0, sticky=(tk.W, tk.N), pady=5)
        desc_frame = ttk.Frame(main_frame)
        desc_frame.grid(row=row, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        desc_frame.columnconfigure(0, weight=1)
        desc_frame.rowconfigure(0, weight=1)
        
        self.desc_text = tk.Text(desc_frame, height=6, width=40, wrap=tk.WORD)
        self.desc_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.desc_text.insert('1.0', self.setlist.description or "")
        
        desc_scroll = ttk.Scrollbar(desc_frame, orient=tk.VERTICAL, command=self.desc_text.yview)
        desc_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.desc_text.config(yscrollcommand=desc_scroll.set)
        
        main_frame.rowconfigure(row, weight=1)
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="OK", command=self._on_ok, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel, width=10).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter/Escape
        self.dialog.bind('<Return>', lambda e: self._on_ok())
        self.dialog.bind('<Escape>', lambda e: self._on_cancel())
    
    def _on_ok(self):
        """Handle OK button."""
        # Validate
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Set list name cannot be empty", parent=self.dialog)
            return
        
        if len(name) > 24:
            messagebox.showerror("Error", "Set list name cannot exceed 24 characters", parent=self.dialog)
            return
        
        # Get description
        description = self.desc_text.get('1.0', tk.END).strip()
        
        # Update set list
        self.setlist.name = name
        self.setlist.description = description
        
        self.result = True
        self.dialog.destroy()
    
    def _on_cancel(self):
        """Handle Cancel button."""
        self.result = False
        self.dialog.destroy()
