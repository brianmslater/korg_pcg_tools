"""Qt dialog for Double to Single Keyboard Setup.

Based on C# DoubleToSingleKeyboardWindow.xaml.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QComboBox, QSpinBox, QPushButton, QGroupBox,
    QMessageBox
)
from PySide6.QtCore import Qt

from .models import PcgFile
from .double_to_single import process_double_to_single


class DoubleToSingleKeyboardDialog(QDialog):
    """Dialog for Double to Single Keyboard Setup.
    
    Based on C# DoubleToSingleKeyboardWindow.
    """
    
    def __init__(self, pcg: PcgFile, parent=None):
        super().__init__(parent)
        self.pcg = pcg
        self.setWindowTitle("Double to Single Keyboard Setup")
        self.setMinimumWidth(400)
        self._setup_ui()
        self._populate_controls()
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Set Lists group
        setlist_group = QGroupBox("Set Lists")
        setlist_layout = QFormLayout(setlist_group)
        
        self.source_setlist_combo = QComboBox()
        setlist_layout.addRow("Source Set List:", self.source_setlist_combo)
        
        self.target_setlist_combo = QComboBox()
        setlist_layout.addRow("Target Set List:", self.target_setlist_combo)
        
        layout.addWidget(setlist_group)
        
        # Target Combi Bank group
        combi_group = QGroupBox("Target Combi Bank")
        combi_layout = QFormLayout(combi_group)
        
        self.target_combi_combo = QComboBox()
        combi_layout.addRow("Combi Bank:", self.target_combi_combo)
        
        layout.addWidget(combi_group)
        
        # MIDI Channels group
        midi_group = QGroupBox("MIDI Channels")
        midi_layout = QFormLayout(midi_group)
        
        self.main_channel_spin = QSpinBox()
        self.main_channel_spin.setRange(1, 16)
        self.main_channel_spin.setValue(1)
        midi_layout.addRow("Main Keyboard Channel:", self.main_channel_spin)
        
        self.secondary_channel_spin = QSpinBox()
        self.secondary_channel_spin.setRange(1, 16)
        self.secondary_channel_spin.setValue(2)
        midi_layout.addRow("Secondary Keyboard Channel:", self.secondary_channel_spin)
        
        layout.addWidget(midi_group)
        
        # Description
        desc_label = QLabel(
            "This tool duplicates set list slots for dual keyboard setups.\n"
            "Slots using the secondary MIDI channel will be duplicated with\n"
            "MIDI channels swapped, allowing single keyboard playback."
        )
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(desc_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self._on_ok)
        button_layout.addWidget(self.ok_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
    
    def _populate_controls(self):
        """Populate combo boxes with data from PCG file."""
        # Populate set list combos
        if self.pcg.set_lists:
            for i, setlist in enumerate(self.pcg.set_lists):
                display = f"SL{i}: {setlist.name}" if setlist.name else f"SL{i}"
                self.source_setlist_combo.addItem(display, i)
                self.target_setlist_combo.addItem(display, i)
        
        # Populate combi bank combo (only writable banks)
        for bank in self.pcg.combi_banks:
            if not bank.is_read_only:
                self.target_combi_combo.addItem(bank.bank_id, bank.bank_id)
        
        # Set defaults
        if self.source_setlist_combo.count() > 0:
            self.source_setlist_combo.setCurrentIndex(0)
        if self.target_setlist_combo.count() > 1:
            self.target_setlist_combo.setCurrentIndex(1)
        if self.target_combi_combo.count() > 0:
            self.target_combi_combo.setCurrentIndex(0)
    
    def _on_ok(self):
        """Handle OK button click."""
        # Get selected values
        source_index = self.source_setlist_combo.currentData()
        target_index = self.target_setlist_combo.currentData()
        target_bank = self.target_combi_combo.currentData()
        main_channel = self.main_channel_spin.value()
        secondary_channel = self.secondary_channel_spin.value()
        
        # Validate
        if source_index == target_index:
            QMessageBox.warning(
                self, "Invalid Selection",
                "Source and target set lists must be different."
            )
            return
        
        if main_channel == secondary_channel:
            QMessageBox.warning(
                self, "Invalid Selection",
                "Main and secondary MIDI channels must be different."
            )
            return
        
        if target_bank is None:
            QMessageBox.warning(
                self, "Invalid Selection",
                "Please select a target combi bank."
            )
            return
        
        # Process
        result = process_double_to_single(
            self.pcg,
            source_index,
            target_index,
            target_bank,
            main_channel,
            secondary_channel
        )
        
        if result.success:
            QMessageBox.information(
                self, "Success",
                f"Conversion complete!\n\n"
                f"Set list slots created: {result.slots_created}\n"
                f"Combis created: {result.combis_created}"
            )
            self.accept()
        else:
            QMessageBox.warning(
                self, "Error",
                f"Conversion failed:\n{result.error_message}"
            )
