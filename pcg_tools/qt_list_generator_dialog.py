"""Qt dialog for List Generator.

Based on C# ListGeneratorWindow.xaml and ListGeneratorWindow.xaml.cs.
Provides UI for generating various lists and reports from PCG files.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QRadioButton, QSpinBox,
    QLabel, QPushButton, QButtonGroup, QMessageBox, QGroupBox,
    QCheckBox, QComboBox, QLineEdit, QFileDialog, QScrollArea,
    QWidget, QGridLayout, QSlider
)
from PySide6.QtCore import Qt

from .list_generators import (
    ListGenerator, OutputFormat, SortMethod, FilterOnFavorites
)
from .models import PcgFile


class QtListGeneratorDialog(QDialog):
    """Dialog for generating lists and reports from PCG files.
    
    Based on C# ListGeneratorWindow.
    """
    
    def __init__(self, pcg: PcgFile, parent=None, other_pcg: PcgFile = None):
        super().__init__(parent)
        self.pcg = pcg
        self.other_pcg = other_pcg  # For differences list
        self.setWindowTitle("List Generator")
        self.setModal(True)
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        
        self._setup_ui()
        self._connect_signals()
        self._update_ui_state()
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        main_layout = QVBoxLayout(self)
        
        # Create scroll area for all the options
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QHBoxLayout(scroll_widget)
        
        # Left column
        left_column = QVBoxLayout()
        left_column.addWidget(self._create_list_type_group())
        left_column.addWidget(self._create_differences_options_group())
        left_column.addWidget(self._create_filter_text_group())
        left_column.addWidget(self._create_favorites_group())
        left_column.addStretch()
        
        # Middle column
        middle_column = QVBoxLayout()
        middle_column.addWidget(self._create_program_banks_group())
        middle_column.addWidget(self._create_combi_banks_group())
        middle_column.addStretch()
        
        # Right column
        right_column = QVBoxLayout()
        right_column.addWidget(self._create_setlists_group())
        right_column.addWidget(self._create_optional_columns_group())
        right_column.addWidget(self._create_sorting_group())
        right_column.addWidget(self._create_output_group())
        right_column.addStretch()
        
        scroll_layout.addLayout(left_column)
        scroll_layout.addLayout(middle_column)
        scroll_layout.addLayout(right_column)
        
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.generate_btn = QPushButton("Generate")
        self.generate_btn.setDefault(True)
        self.generate_btn.clicked.connect(self._on_generate)
        button_layout.addWidget(self.generate_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        main_layout.addLayout(button_layout)
    
    def _create_list_type_group(self) -> QGroupBox:
        """Create list type selection group."""
        group = QGroupBox("List Type")
        layout = QVBoxLayout(group)
        
        self.list_type_group = QButtonGroup(self)
        
        self.radio_patch_list = QRadioButton("Patch List")
        self.radio_patch_list.setChecked(True)
        self.list_type_group.addButton(self.radio_patch_list)
        layout.addWidget(self.radio_patch_list)
        
        self.radio_program_usage = QRadioButton("Program Usage List")
        self.list_type_group.addButton(self.radio_program_usage)
        layout.addWidget(self.radio_program_usage)
        
        self.radio_combi_content = QRadioButton("Combi Content List")
        self.list_type_group.addButton(self.radio_combi_content)
        layout.addWidget(self.radio_combi_content)
        
        self.radio_differences = QRadioButton("Differences List")
        self.list_type_group.addButton(self.radio_differences)
        layout.addWidget(self.radio_differences)
        
        self.radio_file_content = QRadioButton("File Content List")
        self.list_type_group.addButton(self.radio_file_content)
        layout.addWidget(self.radio_file_content)
        
        # Sub-type combo (for combi content list)
        layout.addWidget(QLabel("List Sub-Type:"))
        self.subtype_combo = QComboBox()
        self.subtype_combo.addItems(["Compact", "Short", "Long"])
        self.subtype_combo.setCurrentIndex(1)  # Default to Short
        layout.addWidget(self.subtype_combo)
        
        return group
    
    def _create_differences_options_group(self) -> QGroupBox:
        """Create differences list options group."""
        self.diff_options_group = QGroupBox("Differences List Options")
        layout = QVBoxLayout(self.diff_options_group)
        
        # Max differences slider
        layout.addWidget(QLabel("Max Number of Differences:"))
        slider_layout = QHBoxLayout()
        
        self.max_diff_slider = QSlider(Qt.Horizontal)
        self.max_diff_slider.setMinimum(10)
        self.max_diff_slider.setMaximum(500)
        self.max_diff_slider.setValue(500)
        self.max_diff_slider.setTickPosition(QSlider.TicksBelow)
        self.max_diff_slider.setTickInterval(50)
        slider_layout.addWidget(self.max_diff_slider)
        
        self.max_diff_label = QLabel("500")
        self.max_diff_label.setMinimumWidth(40)
        slider_layout.addWidget(self.max_diff_label)
        
        layout.addLayout(slider_layout)
        
        self.check_ignore_patch_names = QCheckBox("Ignore Patch Names")
        self.check_ignore_patch_names.setChecked(True)
        layout.addWidget(self.check_ignore_patch_names)
        
        self.check_ignore_setlist_desc = QCheckBox("Ignore Set List Slot Descriptions")
        self.check_ignore_setlist_desc.setChecked(True)
        layout.addWidget(self.check_ignore_setlist_desc)
        
        self.check_search_both = QCheckBox("Search Both Directions")
        layout.addWidget(self.check_search_both)
        
        # Compare file selection
        layout.addWidget(QLabel("Compare with:"))
        file_layout = QHBoxLayout()
        self.compare_file_edit = QLineEdit()
        self.compare_file_edit.setReadOnly(True)
        file_layout.addWidget(self.compare_file_edit)
        
        browse_btn = QPushButton("...")
        browse_btn.setMaximumWidth(30)
        browse_btn.clicked.connect(self._browse_compare_file)
        file_layout.addWidget(browse_btn)
        
        layout.addLayout(file_layout)
        
        return self.diff_options_group

    def _create_program_banks_group(self) -> QGroupBox:
        """Create program banks filter group."""
        group = QGroupBox("Filter Program Banks")
        layout = QVBoxLayout(group)
        
        # Internal banks (I-A through I-H)
        internal_layout = QHBoxLayout()
        self.prog_bank_checks = {}
        
        for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            bank_id = f"I-{letter}"
            check = QCheckBox(bank_id)
            check.setChecked(True)
            self.prog_bank_checks[bank_id] = check
            internal_layout.addWidget(check)
        layout.addLayout(internal_layout)
        
        # GM bank
        gm_layout = QHBoxLayout()
        self.prog_bank_checks['GM'] = QCheckBox("GM")
        self.prog_bank_checks['GM'].setChecked(True)
        gm_layout.addWidget(self.prog_bank_checks['GM'])
        gm_layout.addStretch()
        layout.addLayout(gm_layout)
        
        # User banks (U-A through U-H)
        user_layout = QHBoxLayout()
        for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            bank_id = f"U-{letter}"
            check = QCheckBox(bank_id)
            check.setChecked(True)
            self.prog_bank_checks[bank_id] = check
            user_layout.addWidget(check)
        layout.addLayout(user_layout)
        
        # User banks (U-AA through U-HH)
        user2_layout = QHBoxLayout()
        for letter in ['AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'GG', 'HH']:
            bank_id = f"U-{letter}"
            check = QCheckBox(bank_id)
            check.setChecked(True)
            self.prog_bank_checks[bank_id] = check
            user2_layout.addWidget(check)
        layout.addLayout(user2_layout)
        
        # Virtual banks checkbox
        self.check_prog_virtual = QCheckBox("All Virtual Banks")
        layout.addWidget(self.check_prog_virtual)
        
        # Options
        self.check_ignore_init_programs = QCheckBox("Ignore Empty/Init Programs")
        self.check_ignore_init_programs.setChecked(True)
        layout.addWidget(self.check_ignore_init_programs)
        
        self.check_ignore_first_program = QCheckBox("Ignore First Program")
        layout.addWidget(self.check_ignore_first_program)
        
        # Select/Deselect buttons
        btn_layout = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(lambda: self._select_all_banks(self.prog_bank_checks, True))
        btn_layout.addWidget(select_all_btn)
        
        deselect_all_btn = QPushButton("Deselect All")
        deselect_all_btn.clicked.connect(lambda: self._select_all_banks(self.prog_bank_checks, False))
        btn_layout.addWidget(deselect_all_btn)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        return group
    
    def _create_combi_banks_group(self) -> QGroupBox:
        """Create combi banks filter group."""
        group = QGroupBox("Filter Combi Banks")
        layout = QVBoxLayout(group)
        
        # Internal banks (I-A through I-H)
        internal_layout = QHBoxLayout()
        self.combi_bank_checks = {}
        
        for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            bank_id = f"I-{letter}"
            check = QCheckBox(bank_id)
            check.setChecked(True)
            self.combi_bank_checks[bank_id] = check
            internal_layout.addWidget(check)
        layout.addLayout(internal_layout)
        
        # User banks (U-A through U-H)
        user_layout = QHBoxLayout()
        for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            bank_id = f"U-{letter}"
            check = QCheckBox(bank_id)
            check.setChecked(True)
            self.combi_bank_checks[bank_id] = check
            user_layout.addWidget(check)
        layout.addLayout(user_layout)
        
        # Virtual banks checkbox
        self.check_combi_virtual = QCheckBox("All Virtual Banks")
        layout.addWidget(self.check_combi_virtual)
        
        # Options
        self.check_ignore_init_combis = QCheckBox("Ignore Empty/Init Combis")
        self.check_ignore_init_combis.setChecked(True)
        layout.addWidget(self.check_ignore_init_combis)
        
        self.check_ignore_muted_timbres = QCheckBox("Ignore Muted/Off Timbres")
        self.check_ignore_muted_timbres.setChecked(True)
        layout.addWidget(self.check_ignore_muted_timbres)
        
        self.check_ignore_first_timbre = QCheckBox("Ignore First Program Timbre")
        layout.addWidget(self.check_ignore_first_timbre)
        
        # Select/Deselect buttons
        btn_layout = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(lambda: self._select_all_banks(self.combi_bank_checks, True))
        btn_layout.addWidget(select_all_btn)
        
        deselect_all_btn = QPushButton("Deselect All")
        deselect_all_btn.clicked.connect(lambda: self._select_all_banks(self.combi_bank_checks, False))
        btn_layout.addWidget(deselect_all_btn)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        return group
    
    def _create_setlists_group(self) -> QGroupBox:
        """Create setlists filter group."""
        group = QGroupBox("Filter Set Lists")
        layout = QVBoxLayout(group)
        
        # Enable checkbox and range
        enable_layout = QHBoxLayout()
        self.check_setlists_enabled = QCheckBox("Enabled")
        self.check_setlists_enabled.setChecked(True)
        enable_layout.addWidget(self.check_setlists_enabled)
        
        enable_layout.addWidget(QLabel("Range:"))
        self.setlist_from_spin = QSpinBox()
        self.setlist_from_spin.setMinimum(1)
        self.setlist_from_spin.setMaximum(128)
        self.setlist_from_spin.setValue(1)
        enable_layout.addWidget(self.setlist_from_spin)
        
        enable_layout.addWidget(QLabel("to"))
        self.setlist_to_spin = QSpinBox()
        self.setlist_to_spin.setMinimum(1)
        self.setlist_to_spin.setMaximum(128)
        self.setlist_to_spin.setValue(128)
        enable_layout.addWidget(self.setlist_to_spin)
        
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(self._select_all_setlists)
        enable_layout.addWidget(select_all_btn)
        
        layout.addLayout(enable_layout)
        
        self.check_ignore_init_slots = QCheckBox("Ignore Empty/Init Set List Slots")
        self.check_ignore_init_slots.setChecked(True)
        layout.addWidget(self.check_ignore_init_slots)
        
        return group
    
    def _create_filter_text_group(self) -> QGroupBox:
        """Create text filter group."""
        group = QGroupBox("Filter on Text")
        layout = QVBoxLayout(group)
        
        # Enable and text input
        text_layout = QHBoxLayout()
        self.check_filter_text = QCheckBox("Filter on Text:")
        text_layout.addWidget(self.check_filter_text)
        
        self.filter_text_edit = QLineEdit()
        self.filter_text_edit.setEnabled(False)
        text_layout.addWidget(self.filter_text_edit)
        layout.addLayout(text_layout)
        
        self.check_case_sensitive = QCheckBox("Case Sensitive")
        self.check_case_sensitive.setEnabled(False)
        layout.addWidget(self.check_case_sensitive)
        
        return group
    
    def _create_favorites_group(self) -> QGroupBox:
        """Create favorites filter group."""
        group = QGroupBox("Filter on Favorites")
        layout = QVBoxLayout(group)
        
        self.favorites_combo = QComboBox()
        self.favorites_combo.addItems(["All", "Favorites Only", "Non-Favorites Only"])
        layout.addWidget(self.favorites_combo)
        
        return group
    
    def _create_optional_columns_group(self) -> QGroupBox:
        """Create optional columns group."""
        group = QGroupBox("Optional Columns")
        layout = QVBoxLayout(group)
        
        self.check_crc_excl_name = QCheckBox("CRC Value (excluding name)")
        layout.addWidget(self.check_crc_excl_name)
        
        self.check_crc_incl_name = QCheckBox("CRC Value (including name)")
        layout.addWidget(self.check_crc_incl_name)
        
        self.check_slot_ref_id = QCheckBox("Set List Slot Reference ID")
        self.check_slot_ref_id.setChecked(True)
        layout.addWidget(self.check_slot_ref_id)
        
        self.check_slot_ref_name = QCheckBox("Set List Slot Reference Name")
        self.check_slot_ref_name.setChecked(True)
        layout.addWidget(self.check_slot_ref_name)
        
        return group
    
    def _create_sorting_group(self) -> QGroupBox:
        """Create sorting options group."""
        group = QGroupBox("Sorting")
        layout = QVBoxLayout(group)
        
        self.sort_group = QButtonGroup(self)
        
        self.radio_sort_type_bank = QRadioButton("Type, Bank, Index")
        self.radio_sort_type_bank.setChecked(True)
        self.sort_group.addButton(self.radio_sort_type_bank)
        layout.addWidget(self.radio_sort_type_bank)
        
        self.radio_sort_category = QRadioButton("Category, then Patch Name")
        self.sort_group.addButton(self.radio_sort_category)
        layout.addWidget(self.radio_sort_category)
        
        self.radio_sort_alpha = QRadioButton("Patch Name (Alphabetical)")
        self.sort_group.addButton(self.radio_sort_alpha)
        layout.addWidget(self.radio_sort_alpha)
        
        return group
    
    def _create_output_group(self) -> QGroupBox:
        """Create output options group."""
        group = QGroupBox("Output")
        layout = QVBoxLayout(group)
        
        self.output_group = QButtonGroup(self)
        
        self.radio_ascii = QRadioButton("ASCII Table")
        self.radio_ascii.setChecked(True)
        self.output_group.addButton(self.radio_ascii)
        layout.addWidget(self.radio_ascii)
        
        self.radio_text = QRadioButton("Text")
        self.output_group.addButton(self.radio_text)
        layout.addWidget(self.radio_text)
        
        self.radio_csv = QRadioButton("CSV (Comma Separated Values)")
        self.output_group.addButton(self.radio_csv)
        layout.addWidget(self.radio_csv)
        
        self.radio_xml = QRadioButton("XML")
        self.output_group.addButton(self.radio_xml)
        layout.addWidget(self.radio_xml)
        
        # Output file
        layout.addWidget(QLabel("Output File:"))
        file_layout = QHBoxLayout()
        self.output_file_edit = QLineEdit()
        file_layout.addWidget(self.output_file_edit)
        
        browse_btn = QPushButton("...")
        browse_btn.setMaximumWidth(30)
        browse_btn.clicked.connect(self._browse_output_file)
        file_layout.addWidget(browse_btn)
        
        layout.addLayout(file_layout)
        
        return group

    def _connect_signals(self):
        """Connect UI signals."""
        # List type changes
        self.radio_patch_list.toggled.connect(self._update_ui_state)
        self.radio_program_usage.toggled.connect(self._update_ui_state)
        self.radio_combi_content.toggled.connect(self._update_ui_state)
        self.radio_differences.toggled.connect(self._update_ui_state)
        self.radio_file_content.toggled.connect(self._update_ui_state)
        
        # Max differences slider
        self.max_diff_slider.valueChanged.connect(
            lambda v: self.max_diff_label.setText(str(v))
        )
        
        # Text filter enable
        self.check_filter_text.toggled.connect(self._on_filter_text_toggled)
        
        # Output format changes - update file extension
        self.radio_ascii.toggled.connect(self._update_output_extension)
        self.radio_text.toggled.connect(self._update_output_extension)
        self.radio_csv.toggled.connect(self._update_output_extension)
        self.radio_xml.toggled.connect(self._update_output_extension)
    
    def _update_ui_state(self):
        """Update UI state based on selected list type."""
        is_differences = self.radio_differences.isChecked()
        is_combi_content = self.radio_combi_content.isChecked()
        
        # Differences options only for differences list
        self.diff_options_group.setEnabled(is_differences)
        
        # Sub-type only for combi content list
        self.subtype_combo.setEnabled(is_combi_content)
    
    def _on_filter_text_toggled(self, checked: bool):
        """Handle filter text checkbox toggle."""
        self.filter_text_edit.setEnabled(checked)
        self.check_case_sensitive.setEnabled(checked)
    
    def _select_all_banks(self, bank_checks: dict, select: bool):
        """Select or deselect all bank checkboxes."""
        for check in bank_checks.values():
            check.setChecked(select)
    
    def _select_all_setlists(self):
        """Select all setlists (set range to 1-128)."""
        self.setlist_from_spin.setValue(1)
        self.setlist_to_spin.setValue(128)
    
    def _browse_compare_file(self):
        """Browse for comparison PCG file."""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Select PCG File to Compare",
            "",
            "PCG Files (*.pcg);;All Files (*)"
        )
        if filepath:
            self.compare_file_edit.setText(filepath)
    
    def _browse_output_file(self):
        """Browse for output file."""
        # Determine extension based on format
        if self.radio_csv.isChecked():
            filter_str = "CSV Files (*.csv);;All Files (*)"
            default_ext = ".csv"
        elif self.radio_xml.isChecked():
            filter_str = "XML Files (*.xml);;All Files (*)"
            default_ext = ".xml"
        else:
            filter_str = "Text Files (*.txt);;All Files (*)"
            default_ext = ".txt"
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Save List As",
            "",
            filter_str
        )
        if filepath:
            # Ensure correct extension
            if not filepath.lower().endswith(default_ext):
                filepath += default_ext
            self.output_file_edit.setText(filepath)
    
    def _update_output_extension(self):
        """Update output file extension when format changes."""
        current = self.output_file_edit.text()
        if not current:
            return
        
        # Remove old extension
        import os
        base = os.path.splitext(current)[0]
        
        # Add new extension
        if self.radio_csv.isChecked():
            self.output_file_edit.setText(base + ".csv")
        elif self.radio_xml.isChecked():
            self.output_file_edit.setText(base + ".xml")
        else:
            self.output_file_edit.setText(base + ".txt")
    
    def _get_selected_program_banks(self) -> list:
        """Get list of selected program bank IDs."""
        selected = []
        for bank_id, check in self.prog_bank_checks.items():
            if check.isChecked():
                selected.append(bank_id)
        return selected if selected else None  # None means all banks
    
    def _get_selected_combi_banks(self) -> list:
        """Get list of selected combi bank IDs."""
        selected = []
        for bank_id, check in self.combi_bank_checks.items():
            if check.isChecked():
                selected.append(bank_id)
        return selected if selected else None  # None means all banks
    
    def _get_output_format(self) -> OutputFormat:
        """Get selected output format."""
        if self.radio_csv.isChecked():
            return OutputFormat.CSV
        elif self.radio_xml.isChecked():
            return OutputFormat.XML
        elif self.radio_ascii.isChecked():
            return OutputFormat.ASCII_TABLE
        else:
            return OutputFormat.TEXT
    
    def _get_sort_method(self) -> SortMethod:
        """Get selected sort method."""
        if self.radio_sort_alpha.isChecked():
            return SortMethod.ALPHABETICAL
        elif self.radio_sort_category.isChecked():
            return SortMethod.CATEGORICAL
        else:
            return SortMethod.TYPE_BANK_INDEX
    
    def _get_favorites_filter(self) -> FilterOnFavorites:
        """Get selected favorites filter."""
        index = self.favorites_combo.currentIndex()
        if index == 1:
            return FilterOnFavorites.YES
        elif index == 2:
            return FilterOnFavorites.NO
        else:
            return FilterOnFavorites.ALL
    
    def _on_generate(self):
        """Handle Generate button click."""
        output_file = self.output_file_edit.text().strip()
        if not output_file:
            QMessageBox.warning(
                self,
                "No Output File",
                "Please specify an output file."
            )
            return
        
        # For differences list, need a comparison file
        if self.radio_differences.isChecked():
            compare_file = self.compare_file_edit.text().strip()
            if not compare_file and not self.other_pcg:
                QMessageBox.warning(
                    self,
                    "No Comparison File",
                    "Please select a PCG file to compare with."
                )
                return
        
        try:
            # Create generator
            gen = ListGenerator(self.pcg)
            
            # Set output format
            gen.output_format = self._get_output_format()
            gen.sort_method = self._get_sort_method()
            
            # Set bank filters
            gen.selected_program_banks = self._get_selected_program_banks()
            gen.selected_combi_banks = self._get_selected_combi_banks()
            gen.include_virtual_program_banks = self.check_prog_virtual.isChecked()
            gen.include_virtual_combi_banks = self.check_combi_virtual.isChecked()
            
            # Set ignore options
            gen.ignore_init_programs = self.check_ignore_init_programs.isChecked()
            gen.ignore_init_combis = self.check_ignore_init_combis.isChecked()
            gen.ignore_init_setlist_slots = self.check_ignore_init_slots.isChecked()
            gen.ignore_first_program = self.check_ignore_first_program.isChecked()
            gen.ignore_muted_off_timbres = self.check_ignore_muted_timbres.isChecked()
            
            # Set setlist options
            gen.setlists_enabled = self.check_setlists_enabled.isChecked()
            gen.setlists_range_from = self.setlist_from_spin.value() - 1  # 0-indexed
            gen.setlists_range_to = self.setlist_to_spin.value() - 1
            
            # Set text filter
            gen.filter_on_text = self.check_filter_text.isChecked()
            gen.filter_text = self.filter_text_edit.text()
            gen.filter_case_sensitive = self.check_case_sensitive.isChecked()
            gen.filter_on_favorites = self._get_favorites_filter()
            
            # Set optional columns
            gen.optional_crc_including_name = self.check_crc_incl_name.isChecked()
            gen.optional_crc_excluding_name = self.check_crc_excl_name.isChecked()
            gen.optional_setlist_slot_reference_id = self.check_slot_ref_id.isChecked()
            gen.optional_setlist_slot_reference_name = self.check_slot_ref_name.isChecked()
            
            # Generate the appropriate list
            if self.radio_patch_list.isChecked():
                gen.generate_patch_list(
                    output_file,
                    include_crc_incl_name=self.check_crc_incl_name.isChecked(),
                    include_crc_excl_name=self.check_crc_excl_name.isChecked()
                )
            elif self.radio_program_usage.isChecked():
                gen.generate_program_usage_list(output_file)
            elif self.radio_combi_content.isChecked():
                style = self.subtype_combo.currentText().lower()
                gen.generate_combi_content_list(output_file, style=style)
            elif self.radio_differences.isChecked():
                # Load comparison file if needed
                if self.other_pcg:
                    other = self.other_pcg
                else:
                    from .reader import read_pcg_file
                    other = read_pcg_file(self.compare_file_edit.text())
                
                gen.generate_differences_list(
                    other,
                    output_file,
                    max_differences=self.max_diff_slider.value(),
                    ignore_patch_names=self.check_ignore_patch_names.isChecked(),
                    ignore_setlist_descriptions=self.check_ignore_setlist_desc.isChecked(),
                    search_both_directions=self.check_search_both.isChecked()
                )
            elif self.radio_file_content.isChecked():
                gen.generate_file_content_list(output_file)
            
            QMessageBox.information(
                self,
                "List Generated",
                f"List saved to:\n{output_file}"
            )
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to generate list:\n{str(e)}"
            )
