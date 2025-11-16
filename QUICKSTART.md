# PCG Tools Python - Quick Start Guide

## Installation

```bash
# Navigate to the project directory
cd pcg_tools_python

# Install dependencies
pip install -r requirements.txt

# Optional: Install in development mode
pip install -e .
```

## Quick Test

Run the basic tests to verify installation:

```bash
python test_basic.py
```

You should see:
```
============================================================
PCG Tools Python - Basic Tests
============================================================
Testing models...
✓ Header creation works
✓ Program creation works
✓ Bank creation works
✓ PCG file creation works

All model tests passed! ✓
...
```

## Using the GUI

Launch the graphical interface:

```bash
python -m pcg_tools gui
```

Or directly:

```bash
python -m pcg_tools.gui
```

Then:
1. Click **File → Open PCG...** to load a PCG file
2. Browse programs and combis in the tabs
3. Use **Tools → Export Patch List...** to export data

## Using the Command Line

### Get file information

```bash
python -m pcg_tools info your_file.pcg
```

### List all patches

```bash
python -m pcg_tools list-patches your_file.pcg
```

### Export to CSV

```bash
python -m pcg_tools export your_file.pcg output.csv
```

### Export to text

```bash
python -m pcg_tools export your_file.pcg output.txt --format txt
```

### Get help

```bash
python -m pcg_tools --help
python -m pcg_tools info --help
```

## Using as a Python Library

```python
from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file

# Read a PCG file
pcg = read_pcg_file("myfile.pcg")

# Display info
print(f"Model: {pcg.header.model.value}")
print(f"Programs: {len(pcg.get_all_programs())}")

# List programs
for bank in pcg.program_banks:
    for program in bank.patches:
        print(f"{program.id}: {program.name}")

# Save (if modified)
write_pcg_file(pcg, "modified.pcg")
```

## Supported File Types

- **.pcg** - Korg PCG files (Program/Combi/Global)
- Supported models:
  - Korg Kronos / Kronos X
  - Korg Oasys
  - Korg Triton (all variants)
  - Korg Karma
  - Korg M3 / M50
  - Korg Krome
  - Korg Trinity

## Common Issues

### "No module named 'click'"

Install dependencies:
```bash
pip install click
```

### "No module named 'tkinter'" (Linux only)

Install tkinter:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### GUI doesn't start

Make sure you're using Python 3.8 or later:
```bash
python --version
```

## Next Steps

- Read [USAGE.md](USAGE.md) for detailed usage instructions
- Read [IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md) for technical details
- Check [examples/basic_usage.py](examples/basic_usage.py) for code examples

## Getting Help

- Check the documentation files in this directory
- Review the example scripts in the `examples/` folder
- Refer to the original PCG Tools documentation

## Platform Notes

### Windows
- Works out of the box with Python 3.8+
- GUI uses native Windows look and feel

### macOS
- Works on macOS 10.14+
- GUI uses native macOS look and feel
- Install Python from python.org or use Homebrew

### Linux
- Works on any modern distribution
- May need to install tkinter separately (see above)
- GUI uses system theme

## Development

To contribute or modify:

1. Clone/fork the repository
2. Install in development mode: `pip install -e .`
3. Make changes
4. Run tests: `python test_basic.py`
5. Test CLI: `python -m pcg_tools --help`
6. Test GUI: `python -m pcg_tools gui`

## License

Free for non-commercial use, based on the original PCG Tools by Michel Keijzers.
