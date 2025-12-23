#!/usr/bin/env python3
"""
Complete test runner for PCG Tools.

This script runs all tests and provides a summary of results.
Referenced in the steering doc as the main test validation command.

Usage:
    python3 test_complete.py
"""

import subprocess
import sys


def main():
    """Run all tests and report results."""
    print("=" * 80)
    print("PCG Tools - Complete Test Suite")
    print("=" * 80)
    print()
    
    # Files to ignore (standalone scripts, not pytest tests)
    ignore_files = [
        "test_direct_edit.py",
        "test_qt_dialog.py", 
        "test_stl1_check.py",
        "test_stl1_structure.py",
    ]
    
    # Build pytest command
    cmd = ["python3", "-m", "pytest", "-v", "--tb=short"]
    for f in ignore_files:
        cmd.extend(["--ignore", f])
    
    print(f"Running: {' '.join(cmd)}")
    print()
    
    # Run pytest
    result = subprocess.run(cmd)
    
    print()
    print("=" * 80)
    if result.returncode == 0:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 80)
    
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
