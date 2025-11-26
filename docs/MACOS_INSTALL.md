# macOS Installation Guide for PCG Tools

## Problem

Your system is using the built-in macOS Python with Tk 8.5, which has critical bugs that prevent GUI widgets from displaying content. This is a known issue with the Apple-provided Python.

## Solution

Install Python 3 with a working Tk version using Homebrew.

## Installation Steps

### 1. Install Homebrew (if not already installed)

Open Terminal and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Python via Homebrew

```bash
brew install python-tk@3.12
```

This installs Python 3.12 with Tk 8.6, which works properly on macOS.

### 3. Verify Installation

```bash
/opt/homebrew/bin/python3 --version
/opt/homebrew/bin/python3 -c "import tkinter; print(f'Tk version: {tkinter.TkVersion}')"
```

You should see Tk version 8.6 or higher.

### 4. Install PCG Tools Dependencies

```bash
/opt/homebrew/bin/python3 -m pip install click
```

### 5. Run PCG Tools with Homebrew Python

```bash
cd /path/to/korg_pcg_tools
/opt/homebrew/bin/python3 -m pcg_tools gui
```

## Alternative: Use the CLI Instead

If you can't install Homebrew Python, you can use the command-line interface which doesn't require GUI:

```bash
# View file info
python3 -m pcg_tools info yourfile.PCG

# Export patch list
python3 -m pcg_tools export yourfile.PCG output.csv

# List all patches
python3 -m pcg_tools list-patches yourfile.PCG

# Generate reports
python3 -m pcg_tools program-usage yourfile.PCG usage.csv
python3 -m pcg_tools combi-content yourfile.PCG content.csv
```

## Why This Happens

Apple's system Python uses Tk 8.5 from 2007, which has known rendering bugs on modern macOS. The Homebrew version includes Tk 8.6+ which fixes these issues.

## Quick Test

After installing Homebrew Python, test if it works:

```bash
cd /path/to/korg_pcg_tools
/opt/homebrew/bin/python3 test_text_widget.py
```

You should now see the patch data displayed in the window.
