# Tech Stack

## Language
- Python 3.7+

## Dependencies
- `PySide6` - Qt-based GUI framework
- `click` - CLI framework

## Package Structure
- Pure Python package in `pcg_tools/`
- Entry point: `python -m pcg_tools`

## Installation
```bash
pip install -r requirements.txt
pip install -e .  # Development mode
```

## Common Commands

### Run GUI
```bash
python3 -m pcg_tools.gui_qt
```

### Run CLI
```bash
python -m pcg_tools --help
python -m pcg_tools info <file.pcg>
python -m pcg_tools export <file.pcg> output.csv
```

### Run Tests
```bash
python test_complete.py
```

## Code Style
- Follow PEP 8
- Use type hints where helpful
- Add docstrings to public functions
- Comment complex binary parsing logic

## Platform Support
- Windows, macOS, Linux
- Cross-platform GUI via Qt
