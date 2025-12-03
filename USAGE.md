# PCG Tools Usage Guide

## Installation

```bash
cd pcg_tools_python
pip install -e .
```

Or install dependencies only:

```bash
pip install -r requirements.txt
```

## Command Line Usage

### Display File Information

```bash
python -m pcg_tools info myfile.pcg
```

Output:
```
============================================================
PCG File: myfile.pcg
============================================================
Model: Korg Kronos
Version: 2.0
Product ID: 0x68

Program Banks: 6
Combi Banks: 4
Set Lists: 1
Has Global: True

Total Programs: 768
Total Combis: 512
============================================================
```

### List All Patches

```bash
python -m pcg_tools list-patches myfile.pcg
```

### Export Patch List

Export to CSV:
```bash
python -m pcg_tools export myfile.pcg patches.csv --format csv
```

Export to text:
```bash
python -m pcg_tools export myfile.pcg patches.txt --format txt
```

### Launch GUI

```bash
python -m pcg_tools gui
```

Or directly:
```bash
python -m pcg_tools.gui
```

## GUI Usage

The GUI provides:

1. **File Menu**
   - Open PCG files
   - Save changes
   - Save As to create new files

2. **Programs Tab**
   - View all program banks (including GM2 banks)
   - See program names, categories, and favorites
   - GM2 banks (g(1)-g(9), g(d)) shown with [ROM] indicator
   - Copy from ROM banks (edit/paste disabled)

3. **Combis Tab**
   - View all combi banks
   - See combi names, categories, and favorites

4. **Tools Menu**
   - Export patch lists to CSV or text

## Python API Usage

### Basic Reading

```python
from pcg_tools.reader import read_pcg_file

# Read a PCG file
pcg = read_pcg_file("myfile.pcg")

# Access file info
print(f"Model: {pcg.header.model.value}")
print(f"Programs: {len(pcg.get_all_programs())}")
print(f"Combis: {len(pcg.get_all_combis())}")
```

### Iterate Through Patches

```python
# List all programs
for bank in pcg.program_banks:
    print(f"Bank {bank.bank_id}:")
    for program in bank.patches:
        print(f"  {program.id}: {program.name}")

# List all combis
for bank in pcg.combi_banks:
    print(f"Bank {bank.bank_id}:")
    for combi in bank.patches:
        print(f"  {combi.id}: {combi.name}")
```

### Find Specific Patches

```python
# Find all favorite programs
favorites = [p for p in pcg.get_all_programs() if p.favorite]

# Find programs by name
pianos = [p for p in pcg.get_all_programs() if "Piano" in p.name]

# Find programs by category
from pcg_tools.models import Category
keyboards = [p for p in pcg.get_all_programs() 
             if p.category and "Keyboard" in p.category.name]
```

### Modify and Save

```python
from pcg_tools.writer import write_pcg_file

# Modify patch names
for program in pcg.get_all_programs():
    if "Init" in program.name:
        program.name = program.name.replace("Init", "Empty")

# Save changes
write_pcg_file(pcg, "modified.pcg")
```

## Supported Models

- Korg Kronos / Kronos X
- Korg Oasys
- Korg Triton (Classic, Extreme, Studio, LE, Rack)
- Korg Karma
- Korg M3
- Korg M50
- Korg Krome
- Korg Trinity

## Current Limitations

This is a Python port focusing on core functionality. The following features from the original PCG Tools are planned for future releases:

- Full binary parsing of all patch parameters
- Copy/paste patches between files
- Timbre editing in combis
- Set list management
- Drum kit and wave sequence support
- Master file connections
- Advanced list generation options

## Platform Compatibility

PCG Tools Python works on:
- Windows (7, 10, 11)
- macOS (10.14+)
- Linux (any modern distribution)

The GUI uses tkinter which is included with Python on most platforms.

## Troubleshooting

### "No module named 'tkinter'"

On Linux, install tkinter:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### "Failed to open file"

Make sure:
1. The file is a valid PCG file (starts with "KORG")
2. The file is not corrupted
3. You have read permissions

### GUI doesn't start

Try running from command line to see error messages:
```bash
python -m pcg_tools gui
```

## Contributing

This is an open-source port. Contributions welcome for:
- Additional model support
- Binary format parsing improvements
- New features
- Bug fixes

## License

Free for non-commercial use, based on the original PCG Tools license.
