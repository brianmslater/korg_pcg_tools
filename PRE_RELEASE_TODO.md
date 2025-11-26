# Pre-Release TODO

Quick checklist of remaining tasks before v1.1.0 release.

## Critical (Must Do)

### 1. Test CLI Commands ⏳
Test each command with a real PCG file:

```bash
# Get a test PCG file first
cd korg_pcg_tools

# Test info command
python3 -m pcg_tools info test_files/your_file.PCG

# Test export
python3 -m pcg_tools export test_files/your_file.PCG output.csv

# Test program-usage
python3 -m pcg_tools program-usage test_files/your_file.PCG usage.csv

# Test combi-content
python3 -m pcg_tools combi-content test_files/your_file.PCG content.csv

# Test list-patches
python3 -m pcg_tools list-patches test_files/your_file.PCG

# Test differences (need 2 files)
python3 -m pcg_tools differences file1.PCG file2.PCG diff.csv
```

**Status**: ⏳ Needs testing with actual PCG file

### 2. Test Simple Setlist Editor ⏳
- [ ] Launch editor
- [ ] Open a PCG file
- [ ] Edit setlist name
- [ ] Edit slot properties
- [ ] Save file
- [ ] Verify recent files work
- [ ] Verify window position saves
- [ ] Test on different platform (if possible)

**Status**: ⏳ Needs final verification

### 3. Verify Examples ⏳
Check that example scripts work:

```bash
cd examples
python3 basic_usage.py
```

**Status**: ⏳ Needs testing

### 4. Check All Documentation Links ⏳
Go through README.md and verify every link works:
- [ ] Internal links (to other .md files)
- [ ] Cross-references
- [ ] External links (if any)

**Status**: ⏳ Needs verification

### 5. Update Version Numbers ⏳
Ensure version is 1.1.0 everywhere:
- [ ] setup.py
- [ ] simple_setlist_editor.py (About dialog)
- [ ] README.md
- [ ] CHANGELOG.md

**Status**: ⏳ Needs update

## Important (Should Do)

### 6. Create GitHub Repository Description
Write a compelling one-liner for GitHub:

**Suggestion**: 
> Cross-platform Python tool for editing Korg PCG files. Hardware-tested setlist editor for Kronos. CLI for automation and reports.

**Status**: ⏳ Needs writing

### 7. Select GitHub Topics/Tags
Choose relevant tags:
- [ ] korg
- [ ] kronos
- [ ] synthesizer
- [ ] music
- [ ] pcg
- [ ] python
- [ ] cross-platform
- [ ] music-production

**Status**: ⏳ Needs selection

### 8. Add Screenshots
Take screenshots for README:
- [ ] Simple Setlist Editor main window
- [ ] Edit slot dialog
- [ ] CLI output example

**Status**: ⏳ Optional but nice

### 9. Test Installation from Scratch
On a clean system (or VM):

```bash
git clone <repo-url>
cd korg_pcg_tools
pip install -r requirements.txt
python3 simple_setlist_editor.py
```

**Status**: ⏳ Needs testing

## Nice to Have

### 10. Create Demo GIF/Video
Short demo showing:
- Opening a file
- Editing a setlist name
- Editing a slot
- Saving

**Status**: ⏳ Optional

### 11. Add Badges to README
Consider adding:
- License badge
- Python version badge
- Platform badge

**Status**: ⏳ Optional

### 12. Set Up GitHub Issues
Create initial issues for:
- [ ] Program/Combi editing GUI
- [ ] Copy/paste operations
- [ ] Batch operations
- [ ] Feature requests template

**Status**: ⏳ Optional

## Before Publishing

### Final Checklist
- [ ] All critical items complete
- [ ] CLI tested and working
- [ ] Simple Editor tested and working
- [ ] Documentation links verified
- [ ] Version numbers updated
- [ ] No sensitive data in repo
- [ ] .gitignore complete
- [ ] LICENSE file present
- [ ] README renders correctly

### Git Tagging
```bash
git tag -a v1.1.0 -m "Release v1.1.0 - Simple Setlist Editor"
git push origin v1.1.0
```

### GitHub Release
1. Go to GitHub → Releases → New Release
2. Tag: v1.1.0
3. Title: "v1.1.0 - Simple Setlist Editor (Hardware Tested)"
4. Description: Copy from RELEASE_NOTES_v1.1.0.md
5. Attach: None needed (source code auto-attached)
6. Publish!

---

## Current Status

**Overall Progress**: ~70% complete

**Blockers**: None identified

**Estimated Time to Release**: 1-2 hours of testing

**Next Steps**:
1. Test CLI with real PCG file
2. Final Simple Editor verification
3. Update version numbers
4. Test installation
5. Publish!

---

**Last Updated**: November 26, 2025
