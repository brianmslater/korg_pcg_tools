# PCG Tools - Quick Start Guide

Get started with PCG Tools in 5 minutes!

## Installation

```bash
# Navigate to the project directory
cd korg_pcg_tools

# Install dependencies (only 'click' required)
pip install -r requirements.txt
```

That's it! No complex setup needed.

## Simple Setlist Editor (Recommended!)

The easiest way to edit setlists:

```bash
./edit-setlists
```

Or:

```bash
python3 simple_setlist_editor.py
```

### Quick Tutorial

1. **Open a file**: Click "Browse..." or press Ctrl+O
2. **Select setlist**: Choose from dropdown
3. **Edit setlist name**: Click "Edit Setlist Name" button
4. **Edit slots**: Double-click any slot to edit
   - Change name, color, text size
   - Adjust transpose and volume
   - Add notes
5. **Save**: Click "Save File" or press Ctrl+S

**Hardware tested and confirmed working on Korg Kronos!**

See [SIMPLE_EDITOR_GUIDE.md](SIMPLE_EDITOR_GUIDE.md) for full details.

## Command-Line Interface

### Get file information

```bash
python -m pcg_tools info your_file.PCG
```

### List all patches

```bash
python -m pcg_tools list-patches your_file.PCG
```

### Export to CSV

```bash
python -m pcg_tools export your_file.PCG output.csv
```

### Generate reports

```bash
# Program usage report
python -m pcg_tools program-usage your_file.PCG usage.csv

# Combi content report
python -m pcg_tools combi-content your_file.PCG content.csv
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
pcg = read_pcg_file("myfile.PCG")

# Display info
print(f"Model: {pcg.header.model.value}")
print(f"Setlists: {len(pcg.set_lists)}")

# Edit setlist name
if pcg.set_lists:
    pcg.set_lists[0].name = "My New Setlist"
    
    # Edit first slot
    slot = pcg.set_lists[0].slots[0]
    slot.name = "My Favorite Song"
    slot.transpose = 2
    slot.volume = 120

# Save changes
write_pcg_file(pcg, "modified.PCG")
```

See [examples/basic_usage.py](examples/basic_usage.py) for more examples.

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

### "No module named 'tkinter'"

Install tkinter for your platform:

**macOS:**
```bash
brew install python-tk@3.12
```

**Ubuntu/Debian:**
```bash
sudo apt install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

### Simple Setlist Editor won't start

Make sure you're using Python 3.7 or later:
```bash
python3 --version
```

Test tkinter:
```bash
python3 -m tkinter
```

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

## Next Steps

- **[SIMPLE_EDITOR_GUIDE.md](SIMPLE_EDITOR_GUIDE.md)** - Complete setlist editor guide
- **[USAGE.md](USAGE.md)** - Detailed CLI usage
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Command reference
- **[docs/TECHNICAL_REFERENCE.md](docs/TECHNICAL_REFERENCE.md)** - PCG format details
- **[examples/basic_usage.py](examples/basic_usage.py)** - Code examples

## Getting Help

1. Check [SIMPLE_EDITOR_GUIDE.md](SIMPLE_EDITOR_GUIDE.md) for setlist editing
2. See [KNOWN_ISSUES.md](KNOWN_ISSUES.md) for limitations
3. Review [INSTALL.md](INSTALL.md) for installation problems
4. Open an issue on GitHub for bugs

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

To contribute:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Make changes
4. Test: `python3 simple_setlist_editor.py`
5. Test CLI: `python -m pcg_tools --help`

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.

Inspired by the original PCG Tools by Michel Keijzers.

---

**Ready to edit setlists? Launch the Simple Setlist Editor and start organizing your Kronos!** 🎹
