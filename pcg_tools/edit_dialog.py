"""Edit dialog for patches."""

import tkinter as tk
from tkinter import ttk, messagebox
from .models import Program, Combi


class EditPatchDialog:
    """Dialog for editing patch properties."""
    
    def __init__(self, parent, patch, patch_type="program"):
        self.parent = parent
        self.patch = patch
        self.patch_type = patch_type
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Edit {patch_type.capitalize()}")
        self.dialog.geometry("400x250")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.dialog.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
    
    def _create_widgets(self):
        """Create dialog widgets."""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Name
        ttk.Label(main_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar(value=self.patch.name)
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=30)
        name_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
        name_entry.focus()
        
        # Character count
        self.char_count_label = ttk.Label(main_frame, text=f"{len(self.patch.name)}/24")
        self.char_count_label.grid(row=0, column=2, padx=5)
        self.name_var.trace('w', self._update_char_count)
        
        # Category (if available)
        if self.patch.category:
            ttk.Label(main_frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=5)
            self.category_var = tk.StringVar(value=self.patch.category.name or "")
            category_combo = ttk.Combobox(main_frame, textvariable=self.category_var, width=27)
            category_combo['values'] = self._get_categories()
            category_combo.grid(row=1, column=1, sticky=tk.EW, pady=5)
        
        # Favorite
        self.favorite_var = tk.BooleanVar(value=self.patch.favorite)
        favorite_check = ttk.Checkbutton(main_frame, text="Favorite", variable=self.favorite_var)
        favorite_check.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="OK", command=self._on_ok, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel, width=10).pack(side=tk.LEFT, padx=5)
        
        # Configure grid
        main_frame.columnconfigure(1, weight=1)
        
        # Bind Enter and Escape
        self.dialog.bind('<Return>', lambda e: self._on_ok())
        self.dialog.bind('<Escape>', lambda e: self._on_cancel())
    
    def _update_char_count(self, *args):
        """Update character count label."""
        count = len(self.name_var.get())
        self.char_count_label.config(text=f"{count}/24")
        if count > 24:
            self.char_count_label.config(foreground='red')
        else:
            self.char_count_label.config(foreground='black')
    
    def _get_categories(self):
        """Get list of available categories."""
        # TODO: Load from model-specific category list
        return [
            "Keyboard",
            "Organ",
            "Bass",
            "Guitar/Plucked",
            "Strings/Ensemble",
            "Brass",
            "Sax/Woodwind",
            "Synth Lead",
            "Synth Pad/Strings",
            "Synth PolyKey",
            "Synth Comp/Seq",
            "Drums/Percussion",
            "Sound Effects",
            "Ethnic",
            "Vocoder",
            "Combination",
            "User"
        ]
    
    def _on_ok(self):
        """Handle OK button."""
        name = self.name_var.get()
        
        # Validate name length
        if len(name) > 24:
            messagebox.showerror("Error", "Name must be 24 characters or less", parent=self.dialog)
            return
        
        # Update patch
        self.patch.name = name
        self.patch.favorite = self.favorite_var.get()
        
        if self.patch.category and hasattr(self, 'category_var'):
            self.patch.category.name = self.category_var.get()
        
        self.result = True
        self.dialog.destroy()
    
    def _on_cancel(self):
        """Handle Cancel button."""
        self.result = False
        self.dialog.destroy()
    
    def show(self):
        """Show dialog and wait for result."""
        self.dialog.wait_window()
        return self.result
