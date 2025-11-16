# Installation Guide

## Quick Install

### From PyPI (when published)
```bash
pip install pcg-tools
```

### From Source
```bash
git clone https://github.com/yourusername/pcg-tools-python.git
cd pcg-tools-python
pip install -r requirements.txt
pip install -e .
```

## Platform-Specific Instructions

### Windows

#### Prerequisites
1. Install Python 3.7 or higher from [python.org](https://www.python.org/downloads/)
   - ✅ Check "Add Python to PATH" during installation
   - ✅ Include tkinter (usually included by default)

2. Open Command Prompt or PowerShell

#### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/pcg-tools-python.git
cd pcg-tools-python

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

#### Launch GUI
```bash
# Option 1: Double-click
launch_gui.bat

# Option 2: Command line
python -m pcg_tools gui

# Option 3: After installation
pcg-tools gui
```

### macOS

#### Prerequisites
1. Install Python 3.7 or higher
   ```bash
   # Using Homebrew
   brew install python@3.10
   
   # Or download from python.org
   ```

2. Ensure tkinter is available (usually included with Python)

#### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/pcg-tools-python.git
cd pcg-tools-python

# Install dependencies
pip3 install -r requirements.txt

# Install the package
pip3 install -e .
```

#### Launch GUI
```bash
# Option 1: Command line
python3 -m pcg_tools gui

# Option 2: After installation
pcg-tools gui
```

### Linux

#### Prerequisites
1. Install Python 3.7 or higher
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip python3-tk
   
   # Fedora
   sudo dnf install python3 python3-pip python3-tkinter
   
   # Arch
   sudo pacman -S python python-pip tk
   ```

2. Install git
   ```bash
   # Ubuntu/Debian
   sudo apt install git
   
   # Fedora
   sudo dnf install git
   
   # Arch
   sudo pacman -S git
   ```

#### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/pcg-tools-python.git
cd pcg-tools-python

# Install dependencies
pip3 install -r requirements.txt

# Install the package
pip3 install -e .
```

#### Launch GUI
```bash
# Option 1: Command line
python3 -m pcg_tools gui

# Option 2: After installation
pcg-tools gui
```

## Verification

### Test Installation
```bash
# Check version
python -m pcg_tools --help

# Run test suite
python test_complete.py

# Test GUI (should open window)
python -m pcg_tools gui
```

### Expected Output
```
Usage: python -m pcg_tools [OPTIONS] COMMAND [ARGS]...

  PCG Tools - Korg PCG file editor

Commands:
  combi-content  Generate combi content report
  differences    Compare two PCG files
  export         Export patch list
  gui            Launch GUI
  info           Display PCG file information
  list-patches   List all patches
  program-usage  Generate program usage report
```

## Troubleshooting

### Python Not Found
**Windows:**
- Reinstall Python with "Add to PATH" checked
- Or add Python manually to PATH

**macOS/Linux:**
- Use `python3` instead of `python`
- Use `pip3` instead of `pip`

### tkinter Not Found
**Windows:**
- Reinstall Python, ensure tkinter is selected

**macOS:**
- tkinter should be included with Python
- If missing: `brew install python-tk@3.10`

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

### Permission Errors
**macOS/Linux:**
```bash
# Use --user flag
pip3 install --user -r requirements.txt

# Or use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```bash
# Run as Administrator, or use --user flag
pip install --user -r requirements.txt
```

### GUI Won't Launch
1. Test tkinter:
   ```bash
   python -m tkinter
   ```
   Should open a small test window.

2. Check Python version:
   ```bash
   python --version
   ```
   Should be 3.7 or higher.

3. Reinstall dependencies:
   ```bash
   pip install --force-reinstall -r requirements.txt
   ```

## Virtual Environment (Recommended)

### Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Install in Virtual Environment
```bash
pip install -r requirements.txt
pip install -e .
```

### Deactivate
```bash
deactivate
```

## Development Installation

For contributing to the project:

```bash
# Clone repository
git clone https://github.com/yourusername/pcg-tools-python.git
cd pcg-tools-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install in development mode
pip install -e .

# Install development dependencies (if any)
pip install pytest black flake8

# Run tests
python test_complete.py
```

## Uninstallation

```bash
# If installed with pip
pip uninstall pcg-tools

# Remove cloned repository
rm -rf pcg-tools-python  # or rmdir /s pcg-tools-python on Windows
```

## Getting Help

- Check [README.md](README.md) for usage instructions
- See [QUICKSTART.md](QUICKSTART.md) for a quick guide
- Review [USAGE.md](USAGE.md) for detailed documentation
- Open an issue on GitHub for bugs or questions

## Next Steps

After installation:
1. Read [QUICKSTART.md](QUICKSTART.md) - Get started in 5 minutes
2. Try the GUI: `python -m pcg_tools gui`
3. Explore CLI commands: `python -m pcg_tools --help`
4. Check [USAGE.md](USAGE.md) for detailed features

---

**Enjoy editing your Korg PCG files!** 🎹
