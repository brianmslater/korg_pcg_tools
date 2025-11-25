# Quick Start - PCG Writer

## ✅ Status: WORKING ON HARDWARE!

The PCG writer now successfully saves files that load on Kronos.

## Basic Usage

```python
from pcg_tools.reader import read_pcg_file
from pcg_tools.writer import write_pcg_file

# Read file
pcg = read_pcg_file('my_file.PCG')

# Edit setlist name
pcg.set_lists[0].name = "My New Name"

# Save - will work on hardware!
write_pcg_file(pcg, 'my_file_modified.PCG')
```

## That's It!

The writer now:
- ✅ Updates SLS1 chunk (what displays)
- ✅ Leaves SBK1 chunk unchanged (validation)
- ✅ Files load on Kronos
- ✅ Names show correctly

## Examples

### Rename Multiple Setlists
```python
pcg = read_pcg_file('input.PCG')

pcg.set_lists[0].name = "Rock"
pcg.set_lists[1].name = "Jazz"  
pcg.set_lists[2].name = "Classical"

write_pcg_file(pcg, 'output.PCG')
```

### Organize Your Setlists
```python
pcg = read_pcg_file('input.PCG')

# Rename based on content
for i, setlist in enumerate(pcg.set_lists):
    if setlist.slots[0].name:  # Has content
        setlist.name = f"Setlist {i+1}"
    else:  # Empty
        setlist.name = f"Empty {i+1}"

write_pcg_file(pcg, 'organized.PCG')
```

## What Works

✅ Setlist names
✅ File loading
✅ Name display
✅ All slots functional

## What's Next

Coming soon:
- Slot name editing
- Metadata editing (colors, sizes)
- Full GUI integration

## Need Help?

See:
- `WRITER_WORKING.md` - Complete guide
- `SOLUTION_CONFIRMED.md` - Technical details
- `SESSION_FINAL_NOV25.md` - Full story

---

**Last Updated:** November 25, 2025
**Status:** ✅ Working on Hardware
