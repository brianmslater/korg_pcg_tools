# Project Structure

## Main Package: `pcg_tools/`

### Core Modules
- `models.py` - Data structures (PcgFile, Program, Combi, Bank, SetList, SetListSlot)
- `pcg_parser.py` - Low-level binary PCG file parser (chunk-based: PCG1, PRG1, CMB1, SLS1)
- `reader.py` - High-level file reading API
- `writer.py` - PCG file writer (hardware-tested)
- `bit_utils.py` - Binary manipulation utilities

### User Interfaces
- `gui_qt.py` - Main Qt-based GUI (PySide6)
- `qt_edit_dialog.py` - Qt edit dialogs for patches
- `cli.py` - Click-based command-line interface
- `__main__.py` - Package entry point

### Operations
- `clipboard.py` - Copy/paste operations
- `advanced_clipboard.py` - Extended clipboard features
- `operations.py` - Patch management (move, sort, compact)
- `batch_operations.py` - Bulk operations
- `undo.py` - Undo/redo support

### Specialized
- `setlist_editor.py` - Setlist editing logic
- `gm2_data.py` - GM2 bank definitions (ROM data)
- `reference_tracker.py` - Track program usage in combis
- `list_generators.py` - Report generation (CSV, TXT)
- `settings.py` / `window_settings.py` - User preferences

## Other Directories
- `docs/` - Technical documentation, platform guides
- `examples/` - Usage examples (`basic_usage.py`)
- `test_*.py` - Test scripts (root level)

## Key Files
- `requirements.txt` - Python dependencies
- `setup.py` - Package installation
- `launch_gui.bat` / `run_gui_macos.sh` - Platform launchers
