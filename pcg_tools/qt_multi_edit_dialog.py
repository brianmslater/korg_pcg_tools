"""Multi-edit dialogs for PCG Tools.

Ported from C# WindowEditMultipleCombis.xaml.cs and WindowEditMultipleSetListSlots.xaml.cs
Provides batch editing for multiple combis and set list slots.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QSpinBox, QCheckBox, QPushButton,
    QComboBox, QGroupBox, QTextEdit, QMessageBox
)
from PySide6.QtCore import Qt
from typing import List, Optional

from .models import Combi, SetListSlot, Category


class EditMultipleCombisDialog(QDialog):
    """Dialog for batch editing multiple combis.
    
    Ported from C# WindowEditMultipleCombis.xaml.cs
    Allows editing name, category, subcategory, and favorite for multiple combis.
    """
    
    def __init__(self, parent, combis: List[Combi]):
        super().__init__(parent)
        self.combis = combis
        self.result = False
        
        # Determine common values
        self._analyze_common_values()
        
        self.setWindowTitle(f"Edit {len(combis)} Combis")
        self.setMinimumWidth(500)
        self.setModal(True)
        
        self._create_ui()
        self._load_values()
    
    def _analyze_common_values(self):
        """Analyze combis to find common values."""
        if not self.combis:
            self.common_category = None
            self.common_subcategory = None
            self.common_favorite = None
            return
        
        # Check if all combis have same category
        categories = set()
        subcategories = set()
        favorites = set()
        
        for combi in self.combis:
            if combi.category:
                categories.add(combi.category.main_category)
                subcategories.add(combi.category.sub_category)
            favorites.add(combi.favorite)
        
        self.common_category = list(categories)[0] if len(categories) == 1 else None
        self.common_subcategory = list(subcategories)[0] if len(subcategories) == 1 else None
        self.common_favorite = list(favorites)[0] if len(favorites) == 1 else None
    
    def _create_ui(self):
        """Create the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Info label
        info_label = QLabel(f"Editing {len(self.combis)} combis")
        info_label.setStyleSheet("font-weight: bold; color: #666;")
        layout.addWidget(info_label)
        
        # IDs display (read-only)
        ids_text = ", ".join([c.id for c in self.combis[:5]])
        if len(self.combis) > 5:
            ids_text += f", ... (+{len(self.combis) - 5} more)"
        
        form = QFormLayout()
        
        id_label = QLabel(ids_text)
        id_label.setStyleSheet("color: #888;")
        form.addRow("IDs:", id_label)
        
        # Name prefix/suffix options
        name_group = QGroupBox("Name Modification")
        name_layout = QVBoxLayout(name_group)
        
        # Prefix
        prefix_layout = QHBoxLayout()
        self.prefix_check = QCheckBox("Add Prefix:")
        self.prefix_edit = QLineEdit()
        self.prefix_edit.setMaxLength(10)
        self.prefix_edit.setEnabled(False)
        self.prefix_check.toggled.connect(self.prefix_edit.setEnabled)
        prefix_layout.addWidget(self.prefix_check)
        prefix_layout.addWidget(self.prefix_edit)
        name_layout.addLayout(prefix_layout)
        
        # Suffix
        suffix_layout = QHBoxLayout()
        self.suffix_check = QCheckBox("Add Suffix:")
        self.suffix_edit = QLineEdit()
        self.suffix_edit.setMaxLength(10)
        self.suffix_edit.setEnabled(False)
        self.suffix_check.toggled.connect(self.suffix_edit.setEnabled)
        suffix_layout.addWidget(self.suffix_check)
        suffix_layout.addWidget(self.suffix_edit)
        name_layout.addLayout(suffix_layout)
        
        layout.addWidget(name_group)
        
        # Category group
        cat_group = QGroupBox("Category")
        cat_layout = QFormLayout(cat_group)
        
        # Category checkbox and combo
        cat_row = QHBoxLayout()
        self.category_check = QCheckBox("Set Category:")
        self.category_combo = QComboBox()
        self.category_combo.setEnabled(False)
        self.category_check.toggled.connect(self.category_combo.setEnabled)
        self._populate_categories()
        cat_row.addWidget(self.category_check)
        cat_row.addWidget(self.category_combo)
        cat_row.addStretch()
        cat_layout.addRow(cat_row)
        
        # Subcategory checkbox and combo
        subcat_row = QHBoxLayout()
        self.subcategory_check = QCheckBox("Set Sub-Category:")
        self.subcategory_combo = QComboBox()
        self.subcategory_combo.setEnabled(False)
        self.subcategory_check.toggled.connect(self.subcategory_combo.setEnabled)
        self._populate_subcategories()
        subcat_row.addWidget(self.subcategory_check)
        subcat_row.addWidget(self.subcategory_combo)
        subcat_row.addStretch()
        cat_layout.addRow(subcat_row)
        
        layout.addWidget(cat_group)
        
        # Favorite group
        fav_group = QGroupBox("Favorite")
        fav_layout = QHBoxLayout(fav_group)
        
        self.favorite_check = QCheckBox("Set Favorite:")
        self.favorite_value = QCheckBox("Mark as Favorite")
        self.favorite_value.setEnabled(False)
        self.favorite_check.toggled.connect(self.favorite_value.setEnabled)
        fav_layout.addWidget(self.favorite_check)
        fav_layout.addWidget(self.favorite_value)
        fav_layout.addStretch()
        
        layout.addWidget(fav_group)
        
        # Error label
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.setDefault(True)
        self.ok_button.clicked.connect(self._on_ok)
        button_layout.addWidget(self.ok_button)
        
        layout.addLayout(button_layout)
    
    def _populate_categories(self):
        """Populate category combo box."""
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
        for i, name in enumerate(categories):
            self.category_combo.addItem(f"{i}: {name}", i)
    
    def _populate_subcategories(self):
        """Populate subcategory combo box."""
        for i in range(8):
            self.subcategory_combo.addItem(f"Sub {i}", i)
    
    def _load_values(self):
        """Load common values into controls."""
        # Set category if common
        if self.common_category is not None:
            self.category_check.setChecked(True)
            self.category_combo.setCurrentIndex(self.common_category)
        
        # Set subcategory if common
        if self.common_subcategory is not None:
            self.subcategory_check.setChecked(True)
            self.subcategory_combo.setCurrentIndex(self.common_subcategory)
        
        # Set favorite if common
        if self.common_favorite is not None:
            self.favorite_check.setChecked(True)
            self.favorite_value.setChecked(self.common_favorite)
    
    def _validate(self) -> bool:
        """Validate inputs."""
        # Check prefix length
        if self.prefix_check.isChecked():
            prefix = self.prefix_edit.text()
            for combi in self.combis:
                if len(prefix + combi.name) > 24:
                    self.error_label.setText(f"Prefix would make '{combi.name}' too long")
                    return False
        
        # Check suffix length
        if self.suffix_check.isChecked():
            suffix = self.suffix_edit.text()
            for combi in self.combis:
                if len(combi.name + suffix) > 24:
                    self.error_label.setText(f"Suffix would make '{combi.name}' too long")
                    return False
        
        self.error_label.setText("")
        return True
    
    def _on_ok(self):
        """Handle OK button click."""
        if not self._validate():
            return
        
        # Apply changes to all combis
        for combi in self.combis:
            # Apply prefix
            if self.prefix_check.isChecked():
                prefix = self.prefix_edit.text()
                new_name = prefix + combi.name
                if len(new_name) <= 24:
                    combi.name = new_name
            
            # Apply suffix
            if self.suffix_check.isChecked():
                suffix = self.suffix_edit.text()
                new_name = combi.name + suffix
                if len(new_name) <= 24:
                    combi.name = new_name
            
            # Apply category
            if self.category_check.isChecked():
                cat_value = self.category_combo.currentData()
                if combi.category:
                    combi.category.main_category = cat_value
                else:
                    combi.category = Category(
                        main_category=cat_value,
                        sub_category=0,
                        name=self.category_combo.currentText().split(": ")[1]
                    )
            
            # Apply subcategory
            if self.subcategory_check.isChecked():
                subcat_value = self.subcategory_combo.currentData()
                if combi.category:
                    combi.category.sub_category = subcat_value
            
            # Apply favorite
            if self.favorite_check.isChecked():
                combi.favorite = self.favorite_value.isChecked()
            
            # Update raw_data
            self._update_combi_raw_data(combi)
        
        self.result = True
        self.accept()
    
    def _update_combi_raw_data(self, combi: Combi):
        """Update combi raw_data with changes.
        
        Based on C# KronosCombi.cs:
        - Name: offset 0, 24 bytes
        - Category: offset 4790, bits 4-0
        - SubCategory: offset 4790, bits 7-5
        - Favorite: offset 4791, bit 0
        """
        if not combi.raw_data:
            return
        
        raw_data = bytearray(combi.raw_data)
        
        # Update name (offset 0, 24 bytes)
        if len(raw_data) >= 24:
            name_bytes = combi.name.encode('ascii', errors='replace')[:24]
            name_bytes = name_bytes.ljust(24, b'\x00')
            raw_data[0:24] = name_bytes
        
        # Update category and subcategory (offset 4790)
        if len(raw_data) >= 4791 and combi.category:
            cat_byte = 0
            cat_byte |= (combi.category.main_category & 0x1F)
            cat_byte |= ((combi.category.sub_category & 0x07) << 5)
            raw_data[4790] = cat_byte
        
        # Update favorite (offset 4791, bit 0)
        if len(raw_data) >= 4792:
            if combi.favorite:
                raw_data[4791] |= 0x01
            else:
                raw_data[4791] &= ~0x01
        
        combi.raw_data = bytes(raw_data)
    
    def get_result(self) -> bool:
        """Return whether changes were applied."""
        return self.result



class EditMultipleSetListSlotsDialog(QDialog):
    """Dialog for batch editing multiple set list slots.
    
    Ported from C# WindowEditMultipleSetListSlots.xaml.cs
    Allows editing name, volume, and description for multiple slots.
    """
    
    def __init__(self, parent, slots: List[SetListSlot]):
        super().__init__(parent)
        self.slots = slots
        self.result = False
        
        # Determine common values
        self._analyze_common_values()
        
        self.setWindowTitle(f"Edit {len(slots)} Set List Slots")
        self.setMinimumWidth(500)
        self.setModal(True)
        
        self._create_ui()
        self._load_values()
    
    def _analyze_common_values(self):
        """Analyze slots to find common values."""
        if not self.slots:
            self.common_volume = None
            self.common_color = None
            return
        
        # Check if all slots have same volume
        volumes = set(slot.volume for slot in self.slots if hasattr(slot, 'volume'))
        colors = set(slot.color for slot in self.slots if hasattr(slot, 'color'))
        
        self.common_volume = list(volumes)[0] if len(volumes) == 1 else None
        self.common_color = list(colors)[0] if len(colors) == 1 else None
    
    def _create_ui(self):
        """Create the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Info label
        info_label = QLabel(f"Editing {len(self.slots)} set list slots")
        info_label.setStyleSheet("font-weight: bold; color: #666;")
        layout.addWidget(info_label)
        
        # IDs display (read-only)
        ids_text = ", ".join([f"Slot {s.slot_index:03d}" for s in self.slots[:5]])
        if len(self.slots) > 5:
            ids_text += f", ... (+{len(self.slots) - 5} more)"
        
        form = QFormLayout()
        
        id_label = QLabel(ids_text)
        id_label.setStyleSheet("color: #888;")
        form.addRow("Slots:", id_label)
        
        layout.addLayout(form)
        
        # Name modification group
        name_group = QGroupBox("Name Modification")
        name_layout = QVBoxLayout(name_group)
        
        # Prefix
        prefix_layout = QHBoxLayout()
        self.prefix_check = QCheckBox("Add Prefix:")
        self.prefix_edit = QLineEdit()
        self.prefix_edit.setMaxLength(10)
        self.prefix_edit.setEnabled(False)
        self.prefix_check.toggled.connect(self.prefix_edit.setEnabled)
        prefix_layout.addWidget(self.prefix_check)
        prefix_layout.addWidget(self.prefix_edit)
        name_layout.addLayout(prefix_layout)
        
        # Suffix
        suffix_layout = QHBoxLayout()
        self.suffix_check = QCheckBox("Add Suffix:")
        self.suffix_edit = QLineEdit()
        self.suffix_edit.setMaxLength(10)
        self.suffix_edit.setEnabled(False)
        self.suffix_check.toggled.connect(self.suffix_edit.setEnabled)
        suffix_layout.addWidget(self.suffix_check)
        suffix_layout.addWidget(self.suffix_edit)
        name_layout.addLayout(suffix_layout)
        
        layout.addWidget(name_group)
        
        # Volume group
        vol_group = QGroupBox("Volume")
        vol_layout = QHBoxLayout(vol_group)
        
        self.volume_check = QCheckBox("Set Volume:")
        self.volume_spin = QSpinBox()
        self.volume_spin.setRange(0, 127)
        self.volume_spin.setValue(127)
        self.volume_spin.setEnabled(False)
        self.volume_check.toggled.connect(self.volume_spin.setEnabled)
        vol_layout.addWidget(self.volume_check)
        vol_layout.addWidget(self.volume_spin)
        vol_layout.addStretch()
        
        layout.addWidget(vol_group)
        
        # Color group
        color_group = QGroupBox("Color")
        color_layout = QHBoxLayout(color_group)
        
        self.color_check = QCheckBox("Set Color:")
        self.color_combo = QComboBox()
        self._populate_colors()
        self.color_combo.setEnabled(False)
        self.color_check.toggled.connect(self.color_combo.setEnabled)
        color_layout.addWidget(self.color_check)
        color_layout.addWidget(self.color_combo)
        color_layout.addStretch()
        
        layout.addWidget(color_group)
        
        # Description group
        desc_group = QGroupBox("Description")
        desc_layout = QVBoxLayout(desc_group)
        
        self.desc_check = QCheckBox("Set Description:")
        self.desc_check.toggled.connect(self._on_desc_check_toggled)
        desc_layout.addWidget(self.desc_check)
        
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(100)
        self.desc_edit.setEnabled(False)
        self.desc_edit.textChanged.connect(self._update_desc_length)
        desc_layout.addWidget(self.desc_edit)
        
        self.desc_length_label = QLabel("0 of 512 characters")
        self.desc_length_label.setStyleSheet("color: #888;")
        desc_layout.addWidget(self.desc_length_label)
        
        layout.addWidget(desc_group)
        
        # Error label
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.setDefault(True)
        self.ok_button.clicked.connect(self._on_ok)
        button_layout.addWidget(self.ok_button)
        
        layout.addLayout(button_layout)
    
    def _populate_colors(self):
        """Populate color combo box."""
        from .models import SLOT_COLOR_VALUES
        
        sorted_colors = sorted(SLOT_COLOR_VALUES.items(), key=lambda x: x[1])
        for color_name, color_value in sorted_colors:
            self.color_combo.addItem(color_name, color_value)
    
    def _on_desc_check_toggled(self, checked: bool):
        """Handle description checkbox toggle."""
        self.desc_edit.setEnabled(checked)
        self.desc_length_label.setEnabled(checked)
    
    def _update_desc_length(self):
        """Update description length label."""
        length = len(self.desc_edit.toPlainText())
        max_length = 512  # Typical max for set list slot description
        self.desc_length_label.setText(f"{length} of {max_length} characters")
        
        if length > max_length:
            self.desc_length_label.setStyleSheet("color: red;")
        else:
            self.desc_length_label.setStyleSheet("color: #888;")
    
    def _load_values(self):
        """Load common values into controls."""
        # Set volume if common
        if self.common_volume is not None:
            self.volume_check.setChecked(True)
            self.volume_spin.setValue(self.common_volume)
        
        # Set color if common
        if self.common_color is not None:
            self.color_check.setChecked(True)
            for i in range(self.color_combo.count()):
                if self.color_combo.itemData(i) == self.common_color:
                    self.color_combo.setCurrentIndex(i)
                    break
    
    def _validate(self) -> bool:
        """Validate inputs."""
        # Check prefix length
        if self.prefix_check.isChecked():
            prefix = self.prefix_edit.text()
            for slot in self.slots:
                if len(prefix + slot.name) > 24:
                    self.error_label.setText(f"Prefix would make slot name too long")
                    return False
        
        # Check suffix length
        if self.suffix_check.isChecked():
            suffix = self.suffix_edit.text()
            for slot in self.slots:
                if len(slot.name + suffix) > 24:
                    self.error_label.setText(f"Suffix would make slot name too long")
                    return False
        
        # Check description length
        if self.desc_check.isChecked():
            if len(self.desc_edit.toPlainText()) > 512:
                self.error_label.setText("Description too long (max 512 characters)")
                return False
        
        self.error_label.setText("")
        return True
    
    def _on_ok(self):
        """Handle OK button click."""
        if not self._validate():
            return
        
        # Apply changes to all slots
        for slot in self.slots:
            # Apply prefix
            if self.prefix_check.isChecked():
                prefix = self.prefix_edit.text()
                new_name = prefix + slot.name
                if len(new_name) <= 24:
                    slot.name = new_name
            
            # Apply suffix
            if self.suffix_check.isChecked():
                suffix = self.suffix_edit.text()
                new_name = slot.name + suffix
                if len(new_name) <= 24:
                    slot.name = new_name
            
            # Apply volume
            if self.volume_check.isChecked():
                slot.volume = self.volume_spin.value()
            
            # Apply color
            if self.color_check.isChecked():
                slot.color = self.color_combo.currentData()
            
            # Apply description
            if self.desc_check.isChecked():
                slot.description = self.desc_edit.toPlainText()[:512]
        
        self.result = True
        self.accept()
    
    def get_result(self) -> bool:
        """Return whether changes were applied."""
        return self.result


class EditMultipleProgamsDialog(QDialog):
    """Dialog for batch editing multiple programs.
    
    Similar to EditMultipleCombisDialog but for programs.
    """
    
    def __init__(self, parent, programs: List):
        super().__init__(parent)
        self.programs = programs
        self.result = False
        
        # Determine common values
        self._analyze_common_values()
        
        self.setWindowTitle(f"Edit {len(programs)} Programs")
        self.setMinimumWidth(500)
        self.setModal(True)
        
        self._create_ui()
        self._load_values()
    
    def _analyze_common_values(self):
        """Analyze programs to find common values."""
        if not self.programs:
            self.common_category = None
            self.common_subcategory = None
            self.common_favorite = None
            return
        
        # Check if all programs have same category
        categories = set()
        subcategories = set()
        favorites = set()
        
        for prog in self.programs:
            if prog.category:
                categories.add(prog.category.main_category)
                subcategories.add(prog.category.sub_category)
            favorites.add(prog.favorite)
        
        self.common_category = list(categories)[0] if len(categories) == 1 else None
        self.common_subcategory = list(subcategories)[0] if len(subcategories) == 1 else None
        self.common_favorite = list(favorites)[0] if len(favorites) == 1 else None
    
    def _create_ui(self):
        """Create the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Info label
        info_label = QLabel(f"Editing {len(self.programs)} programs")
        info_label.setStyleSheet("font-weight: bold; color: #666;")
        layout.addWidget(info_label)
        
        # IDs display (read-only)
        ids_text = ", ".join([p.id for p in self.programs[:5]])
        if len(self.programs) > 5:
            ids_text += f", ... (+{len(self.programs) - 5} more)"
        
        form = QFormLayout()
        
        id_label = QLabel(ids_text)
        id_label.setStyleSheet("color: #888;")
        form.addRow("IDs:", id_label)
        
        layout.addLayout(form)
        
        # Name modification group
        name_group = QGroupBox("Name Modification")
        name_layout = QVBoxLayout(name_group)
        
        # Prefix
        prefix_layout = QHBoxLayout()
        self.prefix_check = QCheckBox("Add Prefix:")
        self.prefix_edit = QLineEdit()
        self.prefix_edit.setMaxLength(10)
        self.prefix_edit.setEnabled(False)
        self.prefix_check.toggled.connect(self.prefix_edit.setEnabled)
        prefix_layout.addWidget(self.prefix_check)
        prefix_layout.addWidget(self.prefix_edit)
        name_layout.addLayout(prefix_layout)
        
        # Suffix
        suffix_layout = QHBoxLayout()
        self.suffix_check = QCheckBox("Add Suffix:")
        self.suffix_edit = QLineEdit()
        self.suffix_edit.setMaxLength(10)
        self.suffix_edit.setEnabled(False)
        self.suffix_check.toggled.connect(self.suffix_edit.setEnabled)
        suffix_layout.addWidget(self.suffix_check)
        suffix_layout.addWidget(self.suffix_edit)
        name_layout.addLayout(suffix_layout)
        
        layout.addWidget(name_group)
        
        # Category group
        cat_group = QGroupBox("Category")
        cat_layout = QFormLayout(cat_group)
        
        # Category checkbox and combo
        cat_row = QHBoxLayout()
        self.category_check = QCheckBox("Set Category:")
        self.category_combo = QComboBox()
        self.category_combo.setEnabled(False)
        self.category_check.toggled.connect(self.category_combo.setEnabled)
        self._populate_categories()
        cat_row.addWidget(self.category_check)
        cat_row.addWidget(self.category_combo)
        cat_row.addStretch()
        cat_layout.addRow(cat_row)
        
        # Subcategory checkbox and combo
        subcat_row = QHBoxLayout()
        self.subcategory_check = QCheckBox("Set Sub-Category:")
        self.subcategory_combo = QComboBox()
        self.subcategory_combo.setEnabled(False)
        self.subcategory_check.toggled.connect(self.subcategory_combo.setEnabled)
        self._populate_subcategories()
        subcat_row.addWidget(self.subcategory_check)
        subcat_row.addWidget(self.subcategory_combo)
        subcat_row.addStretch()
        cat_layout.addRow(subcat_row)
        
        layout.addWidget(cat_group)
        
        # Favorite group
        fav_group = QGroupBox("Favorite")
        fav_layout = QHBoxLayout(fav_group)
        
        self.favorite_check = QCheckBox("Set Favorite:")
        self.favorite_value = QCheckBox("Mark as Favorite")
        self.favorite_value.setEnabled(False)
        self.favorite_check.toggled.connect(self.favorite_value.setEnabled)
        fav_layout.addWidget(self.favorite_check)
        fav_layout.addWidget(self.favorite_value)
        fav_layout.addStretch()
        
        layout.addWidget(fav_group)
        
        # Error label
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.setDefault(True)
        self.ok_button.clicked.connect(self._on_ok)
        button_layout.addWidget(self.ok_button)
        
        layout.addLayout(button_layout)
    
    def _populate_categories(self):
        """Populate category combo box."""
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
        for i, name in enumerate(categories):
            self.category_combo.addItem(f"{i}: {name}", i)
    
    def _populate_subcategories(self):
        """Populate subcategory combo box."""
        for i in range(8):
            self.subcategory_combo.addItem(f"Sub {i}", i)
    
    def _load_values(self):
        """Load common values into controls."""
        # Set category if common
        if self.common_category is not None:
            self.category_check.setChecked(True)
            self.category_combo.setCurrentIndex(self.common_category)
        
        # Set subcategory if common
        if self.common_subcategory is not None:
            self.subcategory_check.setChecked(True)
            self.subcategory_combo.setCurrentIndex(self.common_subcategory)
        
        # Set favorite if common
        if self.common_favorite is not None:
            self.favorite_check.setChecked(True)
            self.favorite_value.setChecked(self.common_favorite)
    
    def _validate(self) -> bool:
        """Validate inputs."""
        # Check prefix length
        if self.prefix_check.isChecked():
            prefix = self.prefix_edit.text()
            for prog in self.programs:
                if len(prefix + prog.name) > 24:
                    self.error_label.setText(f"Prefix would make '{prog.name}' too long")
                    return False
        
        # Check suffix length
        if self.suffix_check.isChecked():
            suffix = self.suffix_edit.text()
            for prog in self.programs:
                if len(prog.name + suffix) > 24:
                    self.error_label.setText(f"Suffix would make '{prog.name}' too long")
                    return False
        
        self.error_label.setText("")
        return True
    
    def _on_ok(self):
        """Handle OK button click."""
        if not self._validate():
            return
        
        # Apply changes to all programs
        for prog in self.programs:
            # Apply prefix
            if self.prefix_check.isChecked():
                prefix = self.prefix_edit.text()
                new_name = prefix + prog.name
                if len(new_name) <= 24:
                    prog.name = new_name
            
            # Apply suffix
            if self.suffix_check.isChecked():
                suffix = self.suffix_edit.text()
                new_name = prog.name + suffix
                if len(new_name) <= 24:
                    prog.name = new_name
            
            # Apply category
            if self.category_check.isChecked():
                cat_value = self.category_combo.currentData()
                if prog.category:
                    prog.category.main_category = cat_value
                else:
                    prog.category = Category(
                        main_category=cat_value,
                        sub_category=0,
                        name=self.category_combo.currentText().split(": ")[1]
                    )
            
            # Apply subcategory
            if self.subcategory_check.isChecked():
                subcat_value = self.subcategory_combo.currentData()
                if prog.category:
                    prog.category.sub_category = subcat_value
            
            # Apply favorite
            if self.favorite_check.isChecked():
                prog.favorite = self.favorite_value.isChecked()
            
            # Update raw_data
            self._update_program_raw_data(prog)
        
        self.result = True
        self.accept()
    
    def _update_program_raw_data(self, prog):
        """Update program raw_data with changes.
        
        Based on C# KronosProgram.cs:
        - Name: offset 0, 24 bytes
        - Category: offset 2568, bits 4-0
        - SubCategory: offset 2568, bits 7-5
        - Favorite: offset 2558, bit 5
        """
        if not prog.raw_data:
            return
        
        raw_data = bytearray(prog.raw_data)
        
        # Update name (offset 0, 24 bytes)
        if len(raw_data) >= 24:
            name_bytes = prog.name.encode('ascii', errors='replace')[:24]
            name_bytes = name_bytes.ljust(24, b'\x00')
            raw_data[0:24] = name_bytes
        
        # Update category and subcategory (offset 2568)
        if len(raw_data) >= 2569 and prog.category:
            cat_byte = 0
            cat_byte |= (prog.category.main_category & 0x1F)
            cat_byte |= ((prog.category.sub_category & 0x07) << 5)
            raw_data[2568] = cat_byte
        
        # Update favorite (offset 2558, bit 5)
        if len(raw_data) >= 2559:
            if prog.favorite:
                raw_data[2558] |= 0x20
            else:
                raw_data[2558] &= ~0x20
        
        prog.raw_data = bytes(raw_data)
    
    def get_result(self) -> bool:
        """Return whether changes were applied."""
        return self.result
