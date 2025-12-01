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



class QtEditTimbreDialog(QDialog):
    """Qt-based edit dialog for combi timbres."""
    
    def __init__(self, parent, timbre, combi):
        super().__init__(parent)
        self.timbre = timbre
        self.combi = combi
        self.result = False
        
        self.setWindowTitle(f"Edit Timbre - {combi.name}")
        self.setMinimumWidth(500)
        self.setModal(True)
        
        self._create_widgets()
        self._load_values()
    
    def _create_widgets(self):
        """Create dialog widgets."""
        layout = QVBoxLayout(self)
        
        # Form layout for fields
        form = QFormLayout()
        
        # Program reference (read-only)
        program_label = QLabel(self.timbre.program_id)
        program_label.setStyleSheet("font-weight: bold;")
        form.addRow("Program:", program_label)
        
        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Off", "Int", "Both", "Ext", "Ex2"])
        self.status_combo.setCurrentText(self.timbre.status)
        form.addRow("Status:", self.status_combo)
        
        # MIDI Channel (display as 1-16)
        self.midi_ch_spin = QSpinBox()
        self.midi_ch_spin.setRange(1, 16)
        self.midi_ch_spin.setValue(self.timbre.midi_channel + 1)
        form.addRow("MIDI Channel:", self.midi_ch_spin)
        
        # Volume
        self.volume_spin = QSpinBox()
        self.volume_spin.setRange(0, 127)
        self.volume_spin.setValue(self.timbre.volume)
        form.addRow("Volume:", self.volume_spin)
        
        # Transpose
        self.transpose_spin = QSpinBox()
        self.transpose_spin.setRange(-128, 127)
        self.transpose_spin.setValue(self.timbre.transpose)
        form.addRow("Transpose:", self.transpose_spin)
        
        # Mute
        self.mute_check = QCheckBox("Mute this timbre")
        self.mute_check.setChecked(self.timbre.mute)
        form.addRow("", self.mute_check)
        
        # Key Zone
        key_zone_layout = QHBoxLayout()
        self.bottom_key_spin = QSpinBox()
        self.bottom_key_spin.setRange(0, 127)
        self.bottom_key_spin.setValue(self.timbre.bottom_key)
        key_zone_layout.addWidget(QLabel("Bottom:"))
        key_zone_layout.addWidget(self.bottom_key_spin)
        key_zone_layout.addWidget(QLabel("Top:"))
        self.top_key_spin = QSpinBox()
        self.top_key_spin.setRange(0, 127)
        self.top_key_spin.setValue(self.timbre.top_key)
        key_zone_layout.addWidget(self.top_key_spin)
        form.addRow("Key Zone:", key_zone_layout)
        
        # Velocity Zone
        vel_zone_layout = QHBoxLayout()
        self.bottom_vel_spin = QSpinBox()
        self.bottom_vel_spin.setRange(1, 127)
        self.bottom_vel_spin.setValue(self.timbre.bottom_velocity)
        vel_zone_layout.addWidget(QLabel("Bottom:"))
        vel_zone_layout.addWidget(self.bottom_vel_spin)
        vel_zone_layout.addWidget(QLabel("Top:"))
        self.top_vel_spin = QSpinBox()
        self.top_vel_spin.setRange(1, 127)
        self.top_vel_spin.setValue(self.timbre.top_velocity)
        vel_zone_layout.addWidget(self.top_vel_spin)
        form.addRow("Velocity Zone:", vel_zone_layout)
        
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
    
    def _load_values(self):
        """Load current values into widgets."""
        # Already done in _create_widgets
        pass
    
    def _on_ok(self):
        """Handle OK button."""
        # Update timbre properties
        self.timbre.status = self.status_combo.currentText()
        self.timbre.midi_channel = self.midi_ch_spin.value() - 1  # Convert back to 0-15
        self.timbre.volume = self.volume_spin.value()
        self.timbre.transpose = self.transpose_spin.value()
        self.timbre.mute = self.mute_check.isChecked()
        self.timbre.bottom_key = self.bottom_key_spin.value()
        self.timbre.top_key = self.top_key_spin.value()
        self.timbre.bottom_velocity = self.bottom_vel_spin.value()
        self.timbre.top_velocity = self.top_vel_spin.value()
        
        # Update raw_data
        self._update_raw_data()
        
        self.result = True
        self.accept()
    
    def _update_raw_data(self):
        """Update the combi raw_data with timbre changes."""
        if not self.combi.raw_data:
            return
        
        raw_data = bytearray(self.combi.raw_data)
        
        # Find which timbre this is (0-15)
        timbre_index = self.combi.timbres.index(self.timbre)
        
        # Calculate timbre offset
        # From C# KronosTimbres.cs: TimbresOffsetConstant = 4802
        # Each timbre is 188 bytes
        timbre_base = 4802
        timbre_offset = timbre_base + (timbre_index * 188)
        
        if timbre_offset + 188 > len(raw_data):
            return
        
        # Update timbre parameters based on verified offsets
        # Status (offset +2, bits 7-5) and MIDI Channel (offset +2, bits 4-0)
        status_value = ["Off", "Int", "Both", "Ext", "Ex2"].index(self.timbre.status)
        byte_2 = (status_value << 5) | (self.timbre.midi_channel & 0x1F)
        raw_data[timbre_offset + 2] = byte_2
        
        # Volume (offset +5)
        raw_data[timbre_offset + 5] = self.timbre.volume
        
        # Transpose (offset +7, signed)
        transpose_byte = self.timbre.transpose if self.timbre.transpose >= 0 else (256 + self.timbre.transpose)
        raw_data[timbre_offset + 7] = transpose_byte
        
        # Mute (offset +34, bit 7)
        if self.timbre.mute:
            raw_data[timbre_offset + 34] |= 0x80
        else:
            raw_data[timbre_offset + 34] &= 0x7F
        
        # Key zones (offset +37/+38)
        raw_data[timbre_offset + 37] = self.timbre.top_key
        raw_data[timbre_offset + 38] = self.timbre.bottom_key
        
        # Velocity zones (offset +40/+41)
        raw_data[timbre_offset + 40] = self.timbre.top_velocity
        raw_data[timbre_offset + 41] = self.timbre.bottom_velocity
        
        # Update combi raw_data
        self.combi.raw_data = bytes(raw_data)
