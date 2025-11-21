"""Edit dialog for patches."""

import tkinter as tk
from tkinter import ttk, messagebox
from .models import Program, Combi
import re


def validate_korg_name(name: str) -> tuple[bool, str]:
    """Validate a name according to Korg specifications.
    
    Korg allows:
    - ASCII printable characters (32-126)
    - Maximum 24 characters
    - No control characters
    
    Args:
        name: Name to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(name) > 24:
        return False, "Name must be 24 characters or less"
    
    if len(name) == 0:
        return False, "Name cannot be empty"
    
    # Check for valid ASCII printable characters only
    for char in name:
        if ord(char) < 32 or ord(char) > 126:
            return False, f"Invalid character: '{char}' (only ASCII printable characters allowed)"
    
    return True, ""


def sanitize_korg_name(name: str) -> str:
    """Sanitize a name to be Korg-compatible.
    
    Args:
        name: Name to sanitize
    
    Returns:
        Sanitized name (max 24 chars, ASCII printable only)
    """
    # Remove non-ASCII printable characters
    sanitized = ''.join(c for c in name if 32 <= ord(c) <= 126)
    
    # Truncate to 24 characters
    sanitized = sanitized[:24]
    
    # If empty after sanitization, use default
    if not sanitized:
        sanitized = "Untitled"
    
    return sanitized


class EditSetListDialog:
    """Dialog for editing setlist properties."""
    
    def __init__(self, parent, setlist):
        self.parent = parent
        self.setlist = setlist
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Set List")
        self.dialog.geometry("400x150")
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
        self.name_var = tk.StringVar(value=self.setlist.name)
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=30)
        name_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
        name_entry.focus()
        
        # Character count
        self.char_count_label = ttk.Label(main_frame, text=f"{len(self.setlist.name)}/24")
        self.char_count_label.grid(row=0, column=2, padx=5)
        self.name_var.trace('w', self._update_char_count)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=3, pady=20)
        
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
    
    def _on_ok(self):
        """Handle OK button."""
        name = self.name_var.get()
        
        # Validate name
        is_valid, error_msg = validate_korg_name(name)
        if not is_valid:
            messagebox.showerror("Invalid Name", error_msg, parent=self.dialog)
            return
        
        # Update setlist
        self.setlist.name = name
        
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
        
        # Category
        ttk.Label(main_frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=5)
        current_cat = self.patch.category.name if self.patch.category else ""
        self.category_var = tk.StringVar(value=current_cat)
        self.category_combo = ttk.Combobox(main_frame, textvariable=self.category_var, width=27, state='readonly')
        self.category_combo['values'] = self._get_categories()
        self.category_combo.grid(row=1, column=1, sticky=tk.EW, pady=5)
        self.category_combo.bind('<<ComboboxSelected>>', self._on_category_change)
        
        # Sub-Category
        ttk.Label(main_frame, text="Sub-Category:").grid(row=2, column=0, sticky=tk.W, pady=5)
        current_subcat = self.patch.category.sub_name if self.patch.category else ""
        self.subcategory_var = tk.StringVar(value=current_subcat)
        self.subcategory_combo = ttk.Combobox(main_frame, textvariable=self.subcategory_var, width=27, state='readonly')
        self.subcategory_combo['values'] = self._get_subcategories(current_cat)
        self.subcategory_combo.grid(row=2, column=1, sticky=tk.EW, pady=5)
        
        # Favorite
        self.favorite_var = tk.BooleanVar(value=self.patch.favorite)
        favorite_check = ttk.Checkbutton(main_frame, text="Mark as Favorite", variable=self.favorite_var)
        favorite_check.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
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
    
    def _on_category_change(self, event=None):
        """Handle category selection change."""
        category = self.category_var.get()
        subcategories = self._get_subcategories(category)
        self.subcategory_combo['values'] = subcategories
        if subcategories:
            self.subcategory_combo.current(0)
    
    def _get_categories(self):
        """Get list of available categories."""
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
            "No Assign"
        ]
    
    def _get_subcategories(self, category):
        """Get list of subcategories for a given category."""
        subcategories = {
            "Keyboard": [
                "Acoustic Piano",
                "Electric Piano",
                "Clavi/Harpsichord",
                "Mallet",
                "Organ",
                "Other"
            ],
            "Organ": [
                "Tonewheel",
                "Combo Organ",
                "Pipe Organ",
                "Other"
            ],
            "Bass": [
                "Acoustic Bass",
                "Electric Bass",
                "Synth Bass",
                "Other"
            ],
            "Guitar/Plucked": [
                "Acoustic Guitar",
                "Electric Guitar",
                "Distortion Guitar",
                "Harp/Koto",
                "Other"
            ],
            "Strings/Ensemble": [
                "Strings",
                "Slow Strings",
                "Synth Strings",
                "Choir/Voice",
                "Other"
            ],
            "Brass": [
                "Trumpet/Trombone",
                "French Horn/Tuba",
                "Brass Section",
                "Synth Brass",
                "Other"
            ],
            "Sax/Woodwind": [
                "Saxophone",
                "Clarinet",
                "Flute",
                "Other"
            ],
            "Synth Lead": [
                "Analog Lead",
                "Digital Lead",
                "Distortion Lead",
                "Other"
            ],
            "Synth Pad/Strings": [
                "Warm Pad",
                "Bright Pad",
                "Synth Strings",
                "Choir Pad",
                "Other"
            ],
            "Synth PolyKey": [
                "Analog PolyKey",
                "Digital PolyKey",
                "Other"
            ],
            "Synth Comp/Seq": [
                "Synth Comp",
                "Synth Sequence",
                "Other"
            ],
            "Drums/Percussion": [
                "Drum Kit",
                "Percussion",
                "Synth Drums",
                "Other"
            ],
            "Sound Effects": [
                "Nature",
                "Mechanical",
                "Sci-Fi",
                "Other"
            ],
            "Ethnic": [
                "Asian",
                "African",
                "Other"
            ],
            "Vocoder": [
                "Vocoder",
                "Other"
            ],
            "Combination": [
                "Combination",
                "Other"
            ],
            "No Assign": [
                "No Assign"
            ]
        }
        
        return subcategories.get(category, ["Other"])
    
    def _on_ok(self):
        """Handle OK button."""
        name = self.name_var.get()
        
        # Validate name
        is_valid, error_msg = validate_korg_name(name)
        if not is_valid:
            messagebox.showerror("Invalid Name", error_msg, parent=self.dialog)
            return
        
        # Update patch
        self.patch.name = name
        self.patch.favorite = self.favorite_var.get()
        
        # Update category and subcategory
        if self.patch.category:
            self.patch.category.name = self.category_var.get()
            self.patch.category.sub_name = self.subcategory_var.get()
        else:
            # Create category if it doesn't exist
            from .models import Category
            self.patch.category = Category(
                main_category=0,
                sub_category=0,
                name=self.category_var.get(),
                sub_name=self.subcategory_var.get()
            )
        
        # Update raw_data with new name
        self._update_raw_data_name()
        
        # Update raw_data with favorite flag (if needed)
        self._update_raw_data_favorite()
        
        self.result = True
        self.dialog.destroy()
    
    def _update_raw_data_name(self):
        """Update the raw_data with the new name."""
        if not self.patch.raw_data or len(self.patch.raw_data) < 24:
            return
        
        # Name is at offset 0 in both Program and Combi raw data
        # Convert name to bytes (24 bytes, null-padded)
        name_bytes = self.patch.name.encode('ascii', errors='replace')[:24]
        name_bytes = name_bytes.ljust(24, b'\x00')
        
        # Update raw_data
        raw_data = bytearray(self.patch.raw_data)
        raw_data[0:24] = name_bytes
        self.patch.raw_data = bytes(raw_data)
    
    def _update_raw_data_favorite(self):
        """Update the raw_data with the favorite flag."""
        if not self.patch.raw_data or len(self.patch.raw_data) < 30:
            return
        
        # Favorite flag is typically at offset 24-25 in Kronos patches
        # This is a simplified implementation - actual location may vary
        raw_data = bytearray(self.patch.raw_data)
        
        # For Kronos, favorite is often stored as a bit flag
        # We'll set/clear a flag byte at offset 24
        if self.patch.favorite:
            raw_data[24] |= 0x01  # Set bit 0
        else:
            raw_data[24] &= ~0x01  # Clear bit 0
        
        self.patch.raw_data = bytes(raw_data)
    
    def _on_cancel(self):
        """Handle Cancel button."""
        self.result = False
        self.dialog.destroy()
    
    def show(self):
        """Show dialog and wait for result."""
        self.dialog.wait_window()
        return self.result
