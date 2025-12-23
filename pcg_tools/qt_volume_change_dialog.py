"""Qt dialog for batch volume change.

Based on C# ChangeVolumeWindow.xaml and ChangeVolumeWindow.xaml.cs.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QRadioButton, QSpinBox,
    QLabel, QPushButton, QButtonGroup, QMessageBox, QGroupBox
)
from PySide6.QtCore import Qt

from .volume_change import VolumeChangeType, VolumeChangeParameters


class QtVolumeChangeDialog(QDialog):
    """Dialog for changing volume of combis and set list slots.
    
    Based on C# ChangeVolumeWindow.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Change Volume")
        self.setModal(True)
        self.setMinimumWidth(350)
        
        self.parameters = VolumeChangeParameters()
        self._setup_ui()
        
        # Default to Fixed mode
        self.radio_fixed.setChecked(True)
        self._on_fixed_checked()
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        
        # Change type group
        type_group = QGroupBox("Change Type")
        type_layout = QVBoxLayout(type_group)
        
        self.button_group = QButtonGroup(self)
        
        self.radio_fixed = QRadioButton("Fixed - Set all volumes to a specific value")
        self.radio_relative = QRadioButton("Relative - Add/subtract from current volumes")
        self.radio_percentage = QRadioButton("Percentage - Scale volumes by percentage")
        self.radio_mapped = QRadioButton("Mapped - Map 0-127 to a new range")
        self.radio_smart_mapped = QRadioButton("Smart Mapped - Map actual range to new range")
        
        self.button_group.addButton(self.radio_fixed)
        self.button_group.addButton(self.radio_relative)
        self.button_group.addButton(self.radio_percentage)
        self.button_group.addButton(self.radio_mapped)
        self.button_group.addButton(self.radio_smart_mapped)
        
        type_layout.addWidget(self.radio_fixed)
        type_layout.addWidget(self.radio_relative)
        type_layout.addWidget(self.radio_percentage)
        type_layout.addWidget(self.radio_mapped)
        type_layout.addWidget(self.radio_smart_mapped)
        
        layout.addWidget(type_group)
        
        # Value inputs
        value_group = QGroupBox("Values")
        value_layout = QHBoxLayout(value_group)
        
        self.value_label = QLabel("Value:")
        self.value_spin = QSpinBox()
        self.value_spin.setMinimum(0)
        self.value_spin.setMaximum(127)
        self.value_spin.setValue(127)
        
        self.to_label = QLabel("to")
        self.to_spin = QSpinBox()
        self.to_spin.setMinimum(0)
        self.to_spin.setMaximum(127)
        self.to_spin.setValue(127)
        self.to_spin.setEnabled(False)
        
        value_layout.addWidget(self.value_label)
        value_layout.addWidget(self.value_spin)
        value_layout.addWidget(self.to_label)
        value_layout.addWidget(self.to_spin)
        value_layout.addStretch()
        
        layout.addWidget(value_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        ok_btn = QPushButton("OK")
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self._on_ok)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(ok_btn)
        
        layout.addLayout(button_layout)
        
        # Connect radio buttons
        self.radio_fixed.toggled.connect(self._on_fixed_checked)
        self.radio_relative.toggled.connect(self._on_relative_checked)
        self.radio_percentage.toggled.connect(self._on_percentage_checked)
        self.radio_mapped.toggled.connect(self._on_mapped_checked)
        self.radio_smart_mapped.toggled.connect(self._on_smart_mapped_checked)
    
    def _on_fixed_checked(self):
        """Handle Fixed radio button checked."""
        if not self.radio_fixed.isChecked():
            return
        self.value_spin.setMinimum(0)
        self.value_spin.setMaximum(127)
        self.value_spin.setValue(127)
        self.to_label.setEnabled(False)
        self.to_spin.setEnabled(False)
        self.value_label.setText("Volume:")
    
    def _on_relative_checked(self):
        """Handle Relative radio button checked."""
        if not self.radio_relative.isChecked():
            return
        self.value_spin.setMinimum(-127)
        self.value_spin.setMaximum(127)
        self.value_spin.setValue(0)
        self.to_label.setEnabled(False)
        self.to_spin.setEnabled(False)
        self.value_label.setText("Change:")
    
    def _on_percentage_checked(self):
        """Handle Percentage radio button checked."""
        if not self.radio_percentage.isChecked():
            return
        self.value_spin.setMinimum(0)
        self.value_spin.setMaximum(1000)
        self.value_spin.setValue(100)
        self.to_label.setEnabled(False)
        self.to_spin.setEnabled(False)
        self.value_label.setText("Percent:")
    
    def _on_mapped_checked(self):
        """Handle Mapped radio button checked."""
        if not self.radio_mapped.isChecked():
            return
        self.value_spin.setMinimum(0)
        self.value_spin.setMaximum(127)
        self.value_spin.setValue(0)
        self.to_label.setEnabled(True)
        self.to_spin.setEnabled(True)
        self.to_spin.setValue(127)
        self.value_label.setText("From:")
    
    def _on_smart_mapped_checked(self):
        """Handle Smart Mapped radio button checked."""
        if not self.radio_smart_mapped.isChecked():
            return
        self.value_spin.setMinimum(0)
        self.value_spin.setMaximum(127)
        self.value_spin.setValue(0)
        self.to_label.setEnabled(True)
        self.to_spin.setEnabled(True)
        self.to_spin.setValue(127)
        self.value_label.setText("From:")
    
    def _on_ok(self):
        """Handle OK button click."""
        # Validate mapped values
        if (self.radio_mapped.isChecked() or self.radio_smart_mapped.isChecked()):
            if self.value_spin.value() > self.to_spin.value():
                QMessageBox.warning(
                    self,
                    "Invalid Values",
                    "The 'From' value cannot be higher than the 'to' value."
                )
                return
        
        # Set parameters
        if self.radio_fixed.isChecked():
            self.parameters.change_type = VolumeChangeType.FIXED
        elif self.radio_relative.isChecked():
            self.parameters.change_type = VolumeChangeType.RELATIVE
        elif self.radio_percentage.isChecked():
            self.parameters.change_type = VolumeChangeType.PERCENTAGE
        elif self.radio_mapped.isChecked():
            self.parameters.change_type = VolumeChangeType.MAPPED
        elif self.radio_smart_mapped.isChecked():
            self.parameters.change_type = VolumeChangeType.SMART_MAPPED
        
        self.parameters.value = self.value_spin.value()
        self.parameters.to_value = self.to_spin.value()
        
        self.accept()
    
    def get_parameters(self) -> VolumeChangeParameters:
        """Get the configured parameters."""
        return self.parameters
