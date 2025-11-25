#!/usr/bin/env python3
"""Launch GUI and automatically load soundcheck file for testing."""

import sys
sys.path.insert(0, '.')

from PySide6.QtWidgets import QApplication
from pcg_tools.gui_qt import PcgMainWindow

def main():
    """Launch GUI with test file."""
    app = QApplication(sys.argv)
    
    window = PcgMainWindow()
    window.show()
    
    # Auto-load the soundcheck file for testing
    test_file = 'test_files/soundcheck9_25_25_combined2.PCG'
    print(f"Auto-loading test file: {test_file}")
    
    # Simulate opening the file
    try:
        from pcg_tools.reader import read_pcg_file
        from pathlib import Path
        
        window.pcg = read_pcg_file(test_file)
        window.filepath = test_file
        window.is_dirty = False
        
        window.welcome_widget.hide()
        window.content_widget.show()
        
        window.load_programs()
        window.load_combis()
        window.load_setlists()
        
        window.setWindowTitle(f"PCG Tools - {Path(test_file).name}")
        window.statusbar.showMessage(f"Loaded: {Path(test_file).name}")
        
        print(f"✓ Loaded {len(window.pcg.set_lists)} setlists")
        print(f"✓ GUI ready - check the Set Lists tab")
        
    except Exception as e:
        print(f"✗ Error loading file: {e}")
        import traceback
        traceback.print_exc()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
