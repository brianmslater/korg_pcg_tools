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
        self.dialog.geometry("450x180")
        self.dialog.resizable(False, False)
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
        self.name_var.trace_add('write', self._update_char_count)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=3, pady=20, sticky=tk.EW)
        
        # Center the buttons
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(3, weight=1)
        
        ttk.Button(button_frame, text="OK", command=self._on_ok, width=12).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel, width=12).grid(row=0, column=2, padx=5)
        
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
        self.dialog.geometry("450x300")
        self.dialog.resizable(False, False)
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
        
        # ID (read-only)
        ttk.Label(main_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        id_label = ttk.Label(main_frame, text=self.patch.id, font=('TkDefaultFont', 9, 'bold'))
        id_label.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Name
        ttk.Label(main_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar(value=self.patch.name)
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=30)
        name_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
        name_entry.focus()
        
        # Character count
        self.char_count_label = ttk.Label(main_frame, text=f"{len(self.patch.name)}/24")
        self.char_count_label.grid(row=1, column=2, padx=5)
        self.name_var.trace_add('write', self._update_char_count)
        
        # Favorite checkbox (on same row as name, right side)
        self.favorite_var = tk.BooleanVar(value=self.patch.favorite)
        favorite_check = ttk.Checkbutton(main_frame, text="Is Favorite", variable=self.favorite_var)
        favorite_check.grid(row=1, column=3, sticky=tk.W, padx=10, pady=5)
        
        # Category
        ttk.Label(main_frame, text="Category:").grid(row=2, column=0, sticky=tk.W, pady=5)
        current_cat = self.patch.category.main_category if self.patch.category else 0
        self.category_var = tk.IntVar(value=current_cat)
        self.category_spinbox = ttk.Spinbox(main_frame, from_=0, to=16, textvariable=self.category_var, width=10)
        self.category_spinbox.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Category name (read-only label)
        self.category_name_label = ttk.Label(main_frame, text=self._get_category_name(current_cat))
        self.category_name_label.grid(row=2, column=2, columnspan=2, sticky=tk.W, padx=5)
        self.category_var.trace_add('write', self._update_category_name)
        
        # Sub-Category
        ttk.Label(main_frame, text="Sub Category:").grid(row=3, column=0, sticky=tk.W, pady=5)
        current_subcat = self.patch.category.sub_category if self.patch.category else 0
        self.subcategory_var = tk.IntVar(value=current_subcat)
        self.subcategory_spinbox = ttk.Spinbox(main_frame, from_=0, to=7, textvariable=self.subcategory_var, width=10)
        self.subcategory_spinbox.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20, sticky=tk.EW)
        
        # Center the buttons
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(3, weight=1)
        
        ttk.Button(button_frame, text="OK", command=self._on_ok, width=12).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel, width=12).grid(row=0, column=2, padx=5)
        
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
    
    def _update_category_name(self, *args):
        """Update category name label when category changes."""
        try:
            cat_num = self.category_var.get()
            cat_name = self._get_category_name(cat_num)
            self.category_name_label.config(text=cat_name)
        except:
            pass
    
    def _get_category_name(self, category_num):
        """Get category name from number."""
        categories = [
            "Keyboard",           # 0
            "Organ",              # 1
            "Bass",               # 2
            "Guitar/Plucked",     # 3
            "Strings/Ensemble",   # 4
            "Brass",              # 5
            "Sax/Woodwind",       # 6
            "Synth Lead",         # 7
            "Synth Pad/Strings",  # 8
            "Synth PolyKey",      # 9
            "Synth Comp/Seq",     # 10
            "Drums/Percussion",   # 11
            "Sound Effects",      # 12
            "Ethnic",             # 13
            "Vocoder",            # 14
            "Combination",        # 15
            "No Assign"           # 16
        ]
        if 0 <= category_num < len(categories):
            return categories[category_num]
        return "Unknown"
    
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
            self.patch.category.main_category = self.category_var.get()
            self.patch.category.sub_category = self.subcategory_var.get()
            self.patch.category.name = self._get_category_name(self.category_var.get())
        else:
            # Create category if it doesn't exist
            from .models import Category
            self.patch.category = Category(
                main_category=self.category_var.get(),
                sub_category=self.subcategory_var.get(),
                name=self._get_category_name(self.category_var.get())
            )
        
        # Update raw_data with all changes
        self._update_raw_data()
        
        self.result = True
        self.dialog.destroy()
    
    def _update_raw_data(self):
        """Update the raw_data with all changes."""
        if not self.patch.raw_data:
            return
        
        raw_data = bytearray(self.patch.raw_data)
        
        # Update name (offset 0, 24 bytes)
        if len(raw_data) >= 24:
            name_bytes = self.patch.name.encode('ascii', errors='replace')[:24]
            name_bytes = name_bytes.ljust(24, b'\x00')
            raw_data[0:24] = name_bytes
        
        # Update based on patch type
        if isinstance(self.patch, Program):
            self._update_program_raw_data(raw_data)
        elif isinstance(self.patch, Combi):
            self._update_combi_raw_data(raw_data)
        
        self.patch.raw_data = bytes(raw_data)
    
    def _update_program_raw_data(self, raw_data):
        """Update program-specific raw data.
        
        Based on C# KronosProgram.cs:
        - Category: offset 2568, bits 4-0
        - SubCategory: offset 2568, bits 7-5
        - Favorite: offset 2558, bit 5
        """
        if len(raw_data) < 2569:
            return
        
        # Update category byte (offset 2568)
        cat_byte = raw_data[2568]
        # Clear category bits (4-0) and subcategory bits (7-5)
        cat_byte = 0
        # Set category (bits 4-0)
        cat_byte |= (self.patch.category.main_category & 0x1F)
        # Set subcategory (bits 7-5)
        cat_byte |= ((self.patch.category.sub_category & 0x07) << 5)
        raw_data[2568] = cat_byte
        
        # Update favorite flag (offset 2558, bit 5)
        if self.patch.favorite:
            raw_data[2558] |= 0x20  # Set bit 5
        else:
            raw_data[2558] &= ~0x20  # Clear bit 5
    
    def _update_combi_raw_data(self, raw_data):
        """Update combi-specific raw data.
        
        Based on C# KronosCombi.cs:
        - Category: offset 4790, bits 4-0
        - SubCategory: offset 4790, bits 7-5
        - Favorite: offset 4791, bit 0
        """
        if len(raw_data) < 4792:
            return
        
        # Update category byte (offset 4790)
        cat_byte = raw_data[4790]
        # Clear category bits (4-0) and subcategory bits (7-5)
        cat_byte = 0
        # Set category (bits 4-0)
        cat_byte |= (self.patch.category.main_category & 0x1F)
        # Set subcategory (bits 7-5)
        cat_byte |= ((self.patch.category.sub_category & 0x07) << 5)
        raw_data[4790] = cat_byte
        
        # Update favorite flag (offset 4791, bit 0)
        if self.patch.favorite:
            raw_data[4791] |= 0x01  # Set bit 0
        else:
            raw_data[4791] &= ~0x01  # Clear bit 0
    
    def _on_cancel(self):
        """Handle Cancel button."""
        self.result = False
        self.dialog.destroy()
    
    def show(self):
        """Show dialog and wait for result."""
        self.dialog.wait_window()
        return self.result
