"""Copy/Paste settings dialog matching original PCG Tools."""

import tkinter as tk
from tkinter import ttk
from typing import Optional, List
from .models import Program, Combi


class CopyPasteSettings:
    """Settings for copy/paste operations."""
    
    def __init__(self):
        # Copy settings
        self.copy_with_programs = True  # Copy referenced programs with combis
        self.check_duplicates = True  # Check for duplicate programs
        self.duplicate_mode = "bytewise"  # "bytewise", "name", "likename"
        
        # Paste settings
        self.remap_references = True  # Remap program references when pasting
        self.skip_empty = False  # Skip empty destination slots
        self.overwrite_existing = True  # Overwrite existing patches
        
        # Advanced
        self.ignore_chars_for_duplicate = "0123456789"  # Chars to ignore for like-name matching


class CopyPasteDialog:
    """Dialog for copy/paste settings."""
    
    def __init__(self, parent, settings: CopyPasteSettings, operation: str = "copy"):
        self.settings = settings
        self.operation = operation  # "copy" or "paste"
        self.result = None
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"{operation.capitalize()} Settings")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        
        # Center dialog
        self._center_dialog(parent)
        
        # Wait for dialog
        self.dialog.wait_window()
    
    def _center_dialog(self, parent):
        """Center dialog on parent."""
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.dialog.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
    
    def _create_widgets(self):
        """Create dialog widgets."""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(
            main_frame,
            text=f"{self.operation.capitalize()} Options",
            font=('Arial', 12, 'bold')
        ).pack(pady=10)
        
        if self.operation == "copy":
            self._create_copy_options(main_frame)
        else:
            self._create_paste_options(main_frame)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(side=tk.BOTTOM, pady=10)
        
        ttk.Button(btn_frame, text="OK", command=self._on_ok, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self._on_cancel, width=10).pack(side=tk.LEFT, padx=5)
    
    def _create_copy_options(self, parent):
        """Create copy-specific options."""
        # Copy with programs
        self.copy_with_programs_var = tk.BooleanVar(value=self.settings.copy_with_programs)
        ttk.Checkbutton(
            parent,
            text="Copy referenced programs with combis",
            variable=self.copy_with_programs_var
        ).pack(anchor=tk.W, pady=5)
        
        # Check duplicates
        self.check_duplicates_var = tk.BooleanVar(value=self.settings.check_duplicates)
        ttk.Checkbutton(
            parent,
            text="Check for duplicate programs",
            variable=self.check_duplicates_var
        ).pack(anchor=tk.W, pady=5)
        
        # Duplicate detection mode
        dup_frame = ttk.LabelFrame(parent, text="Duplicate Detection", padding="10")
        dup_frame.pack(fill=tk.X, pady=10)
        
        self.dup_mode_var = tk.StringVar(value=self.settings.duplicate_mode)
        
        ttk.Radiobutton(
            dup_frame,
            text="Bytewise comparison (exact match)",
            variable=self.dup_mode_var,
            value="bytewise"
        ).pack(anchor=tk.W)
        
        ttk.Radiobutton(
            dup_frame,
            text="Name comparison (same name)",
            variable=self.dup_mode_var,
            value="name"
        ).pack(anchor=tk.W)
        
        ttk.Radiobutton(
            dup_frame,
            text="Like-name comparison (similar name)",
            variable=self.dup_mode_var,
            value="likename"
        ).pack(anchor=tk.W)
        
        # Ignore characters
        ignore_frame = ttk.Frame(dup_frame)
        ignore_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(ignore_frame, text="Ignore characters:").pack(side=tk.LEFT)
        self.ignore_chars_var = tk.StringVar(value=self.settings.ignore_chars_for_duplicate)
        ttk.Entry(ignore_frame, textvariable=self.ignore_chars_var, width=20).pack(side=tk.LEFT, padx=5)
    
    def _create_paste_options(self, parent):
        """Create paste-specific options."""
        # Remap references
        self.remap_var = tk.BooleanVar(value=self.settings.remap_references)
        ttk.Checkbutton(
            parent,
            text="Automatically remap program references",
            variable=self.remap_var
        ).pack(anchor=tk.W, pady=5)
        
        # Skip empty
        self.skip_empty_var = tk.BooleanVar(value=self.settings.skip_empty)
        ttk.Checkbutton(
            parent,
            text="Skip empty destination slots",
            variable=self.skip_empty_var
        ).pack(anchor=tk.W, pady=5)
        
        # Overwrite existing
        self.overwrite_var = tk.BooleanVar(value=self.settings.overwrite_existing)
        ttk.Checkbutton(
            parent,
            text="Overwrite existing patches",
            variable=self.overwrite_var
        ).pack(anchor=tk.W, pady=5)
        
        # Info
        info_frame = ttk.LabelFrame(parent, text="Information", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        info_text = tk.Text(info_frame, height=6, wrap=tk.WORD)
        info_text.pack(fill=tk.BOTH, expand=True)
        info_text.insert('1.0', 
            "When pasting combis with 'remap references' enabled:\n\n"
            "• Referenced programs will be copied to the destination\n"
            "• Program references in combis will be updated automatically\n"
            "• Duplicate programs will be detected and reused\n"
            "• This ensures combis work correctly after pasting"
        )
        info_text.config(state='disabled')
    
    def _on_ok(self):
        """Handle OK button."""
        if self.operation == "copy":
            self.settings.copy_with_programs = self.copy_with_programs_var.get()
            self.settings.check_duplicates = self.check_duplicates_var.get()
            self.settings.duplicate_mode = self.dup_mode_var.get()
            self.settings.ignore_chars_for_duplicate = self.ignore_chars_var.get()
        else:
            self.settings.remap_references = self.remap_var.get()
            self.settings.skip_empty = self.skip_empty_var.get()
            self.settings.overwrite_existing = self.overwrite_var.get()
        
        self.result = True
        self.dialog.destroy()
    
    def _on_cancel(self):
        """Handle Cancel button."""
        self.result = False
        self.dialog.destroy()


# Global settings instance
_copy_paste_settings = None


def get_copy_paste_settings() -> CopyPasteSettings:
    """Get the global copy/paste settings instance."""
    global _copy_paste_settings
    if _copy_paste_settings is None:
        _copy_paste_settings = CopyPasteSettings()
    return _copy_paste_settings
