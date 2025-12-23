"""Qt-based Program Reference Changer dialog.

Ported from C# Tools/ProgramReferenceChangerWindow.xaml
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QProgressBar, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal

from .models import PcgFile
from .reference_changer import ReferenceChanger, RuleParser


class ReferenceChangerWorker(QThread):
    """Background worker for reference changing."""
    
    progress = Signal(int)
    finished = Signal(bool, int, int)  # success, error_line, changes_made
    
    def __init__(self, pcg: PcgFile, rules: str):
        super().__init__()
        self.pcg = pcg
        self.rules = rules
    
    def run(self):
        """Execute the reference change operation."""
        changer = ReferenceChanger(self.pcg)
        changer.set_progress_callback(self._on_progress)
        
        if not changer.parse_rules(self.rules):
            self.finished.emit(False, changer.parse_error_line, 0)
            return
        
        slots_changed, timbres_changed = changer.change_references()
        total_changes = slots_changed + timbres_changed
        self.finished.emit(True, -1, total_changes)
    
    def _on_progress(self, percentage: int):
        """Emit progress signal."""
        self.progress.emit(percentage)


class QtReferenceChangerDialog(QDialog):
    """Dialog for changing program references in combis and set list slots.
    
    Rule Syntax:
        source -> destination
        
    Examples:
        I-A040 -> U-A001       Single program
        I-A -> U-A             Whole bank
        I-A040..080 -> U-A001..  Range
    """
    
    def __init__(self, parent, pcg: PcgFile):
        super().__init__(parent)
        self.pcg = pcg
        self.worker = None
        self.changes_made = 0
        
        self.setWindowTitle("Program Reference Changer")
        self.setMinimumWidth(550)
        self.setMinimumHeight(400)
        self.setModal(True)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create dialog widgets."""
        layout = QVBoxLayout(self)
        
        # Help text
        help_label = QLabel(
            "Enter rules to change program references in combis and set list slots.\n"
            "Format: source -> destination\n"
            "Examples: I-A040 -> U-A001 (single), I-A -> U-A (bank), I-A040..080 -> U-A001.. (range)"
        )
        help_label.setWordWrap(True)
        help_label.setStyleSheet("color: #666; margin-bottom: 8px;")
        layout.addWidget(help_label)
        
        # Rules text area
        rules_label = QLabel("Reference Rules:")
        layout.addWidget(rules_label)
        
        self.rules_text = QTextEdit()
        self.rules_text.setPlaceholderText(
            "# Enter rules here, one per line\n"
            "# Lines starting with # are comments\n"
            "#\n"
            "# Examples:\n"
            "# I-A040 -> U-A001\n"
            "# I-A -> U-A\n"
            "# I-A040..080 -> U-A001.."
        )
        self.rules_text.setMinimumHeight(200)
        layout.addWidget(self.rules_text)
        
        # From File button
        from_file_btn = QPushButton("Load from File...")
        from_file_btn.clicked.connect(self._load_from_file)
        layout.addWidget(from_file_btn)
        
        # Progress section (initially hidden)
        self.progress_label = QLabel("Processing rules...")
        self.progress_label.setVisible(False)
        layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        self.ok_btn = QPushButton("Apply Changes")
        self.ok_btn.setDefault(True)
        self.ok_btn.clicked.connect(self._on_apply)
        button_layout.addWidget(self.ok_btn)
        
        layout.addLayout(button_layout)
    
    def _load_from_file(self):
        """Load rules from a text file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Rules File",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.rules_text.setPlainText(f.read())
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to load file:\n{str(e)}"
                )
    
    def _on_apply(self):
        """Apply the reference changes."""
        rules = self.rules_text.toPlainText().strip()
        
        if not rules:
            QMessageBox.warning(
                self,
                "No Rules",
                "Please enter at least one reference change rule."
            )
            return
        
        # Show progress
        self.progress_label.setVisible(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.ok_btn.setEnabled(False)
        self.rules_text.setEnabled(False)
        
        # Start worker thread
        self.worker = ReferenceChangerWorker(self.pcg, rules)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()
    
    def _on_progress(self, percentage: int):
        """Update progress bar."""
        self.progress_bar.setValue(percentage)
    
    def _on_finished(self, success: bool, error_line: int, changes: int):
        """Handle completion of reference changing."""
        self.progress_label.setVisible(False)
        self.progress_bar.setVisible(False)
        self.ok_btn.setEnabled(True)
        self.rules_text.setEnabled(True)
        
        if success:
            self.changes_made = changes
            if changes > 0:
                QMessageBox.information(
                    self,
                    "Success",
                    f"Successfully changed {changes} reference(s)."
                )
                self.accept()
            else:
                QMessageBox.information(
                    self,
                    "No Changes",
                    "No matching references were found to change."
                )
        else:
            QMessageBox.critical(
                self,
                "Parse Error",
                f"Error in rules at line {error_line + 1}.\n"
                "Please check the rule syntax."
            )
    
    def get_changes_made(self) -> int:
        """Return the number of changes made."""
        return self.changes_made
