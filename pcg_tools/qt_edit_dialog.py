"""Qt-based edit dialog for patches - replaces Tkinter version."""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QSpinBox, QCheckBox, QPushButton,
    QMessageBox
)
from PySide6.QtCore import Qt
from .models import Program, Combi, Category


class QtEditPatchDialog(QDialog):
    """Qt-based edit dialog for programs and combis."""
    
    def __init__(self, parent, patch, patch_type="program"):
        super().__init__(parent)
        self.patch = patch
        self.patch_type = patch_type
        self.result = False
        
        self.setWindowTitle(f"Edit {patch_type.capitalize()}")
        self.setMinimumWidth(500)
        self.setModal(True)
        
        self._create_widgets()
        self._load_values()
    
    def _create_widgets(self):
        """Create dialog widgets."""
        layout = QVBoxLayout(self)
        
        # Form layout for fields
        form = QFormLayout()
        
        # ID (read-only)
        id_label = QLabel(self.patch.id)
        id_label.setStyleSheet("font-weight: bold;")
        form.addRow("ID:", id_label)
        
        # Name
        self.name_edit = QLineEdit(self.patch.name)
        self.name_edit.setMaxLength(24)
        self.name_edit.textChanged.connect(self._update_char_count)
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.name_edit)
        self.char_count_label = QLabel(f"{len(self.patch.name)}/24")
        name_layout.addWidget(self.char_count_label)
        
        form.addRow("Name:", name_layout)
        
        # Favorite checkbox (on same row as name would be cluttered, so separate row)
        self.favorite_check = QCheckBox("Mark as Favorite")
        self.favorite_check.setChecked(self.patch.favorite)
        form.addRow("", self.favorite_check)
        
        # Category
        self.category_spin = QSpinBox()
        self.category_spin.setRange(0, 16)
        self.category_spin.setValue(
            self.patch.category.main_category if self.patch.category else 0
        )
        self.category_spin.valueChanged.connect(self._update_category_name)
        
        category_layout = QHBoxLayout()
        category_layout.addWidget(self.category_spin)
        self.category_name_label = QLabel()
        self.category_name_label.setStyleSheet("color: #666;")
        category_layout.addWidget(self.category_name_label)
        category_layout.addStretch()
        
        form.addRow("Category:", category_layout)
        
        # Sub-Category
        self.subcategory_spin = QSpinBox()
        self.subcategory_spin.setRange(0, 7)
        self.subcategory_spin.setValue(
            self.patch.category.sub_category if self.patch.category else 0
        )
        form.addRow("Sub Category:", self.subcategory_spin)
        
        # Add form to main layout
        layout.addLayout(form)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        ok_button = QPushButton("OK")
        ok_button.setDefault(True)
        ok_button.clicked.connect(self._on_ok)
        button_layout.addWidget(ok_button)
        
        layout.addLayout(button_layout)
        
        # Update category name initially
        self._update_category_name()
    
    def _load_values(self):
        """Load current values into widgets."""
        # Already done in _create_widgets
        pass
    
    def _update_char_count(self):
        """Update character count label."""
        count = len(self.name_edit.text())
        self.char_count_label.setText(f"{count}/24")
        if count > 24:
            self.char_count_label.setStyleSheet("color: red;")
        else:
            self.char_count_label.setStyleSheet("")
    
    def _update_category_name(self):
        """Update category name label."""
        cat_num = self.category_spin.value()
        cat_name = self._get_category_name(cat_num)
        self.category_name_label.setText(cat_name)
    
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
    
    def _validate_name(self, name):
        """Validate patch name."""
        if len(name) == 0:
            return False, "Name cannot be empty"
        
        if len(name) > 24:
            return False, "Name must be 24 characters or less"
        
        # Check for valid ASCII printable characters
        for char in name:
            if ord(char) < 32 or ord(char) > 126:
                return False, f"Invalid character: '{char}' (only ASCII printable characters allowed)"
        
        return True, ""
    
    def _on_ok(self):
        """Handle OK button."""
        name = self.name_edit.text()
        
        # Validate name
        is_valid, error_msg = self._validate_name(name)
        if not is_valid:
            QMessageBox.warning(self, "Invalid Name", error_msg)
            return
        
        # Update patch
        self.patch.name = name
        self.patch.favorite = self.favorite_check.isChecked()
        
        # Update category
        if self.patch.category:
            self.patch.category.main_category = self.category_spin.value()
            self.patch.category.sub_category = self.subcategory_spin.value()
            self.patch.category.name = self._get_category_name(self.category_spin.value())
        else:
            # Create category if it doesn't exist
            self.patch.category = Category(
                main_category=self.category_spin.value(),
                sub_category=self.subcategory_spin.value(),
                name=self._get_category_name(self.category_spin.value())
            )
        
        # Update raw_data
        self._update_raw_data()
        
        self.result = True
        self.accept()
    
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
        cat_byte = 0
        cat_byte |= (self.patch.category.main_category & 0x1F)
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
        cat_byte = 0
        cat_byte |= (self.patch.category.main_category & 0x1F)
        cat_byte |= ((self.patch.category.sub_category & 0x07) << 5)
        raw_data[4790] = cat_byte
        
        # Update favorite flag (offset 4791, bit 0)
        if self.patch.favorite:
            raw_data[4791] |= 0x01  # Set bit 0
        else:
            raw_data[4791] &= ~0x01  # Clear bit 0
    
    def get_result(self):
        """Return whether user clicked OK."""
        return self.result
