# PCG Writer Quick Reference

## Critical Rule

**ALWAYS update BOTH formats when modifying setlist data!**

## Dual Format System

| Format | Chunks | Purpose | Parser Reads From |
|--------|--------|---------|-------------------|
| New | SLS1/SLD1/SDB1 | Efficient, modern | ✓ YES |
| Old | STL1/SBK1 | Legacy compatibility | No |

## Chunk Breakdown

| Chunk | Contains | Update Required |
|-------|----------|-----------------|
| **SLS1** | Setlist names, slot names | ✓ YES |
| **SLD1** | Patch references, descriptions | Future |
| **SDB1** | Colors, text sizes, transpose | Future |
| **SBK1** | Everything (old format) | ✓ YES |

## Update Pattern

```python
def _update_all_setlist_chunks(self, raw_data: bytearray):
    """Always update BOTH formats!"""
    self._update_sls1_names(raw_data)  # New format
    self._update_sbk1_names(raw_data)  # Old format
```

## File Offsets

### SLS1 (New Format)
```
Structure per setlist (3,612 bytes):
  -4: Marker (1E 02 00 00)
   0: Setlist name (24 bytes)
  24: Separator (28 0F 01 00)
  28: Slot 0 name (24 bytes, no marker)
  52: Slot 1 marker + name (28 bytes)
  80: Slot 2 marker + name (28 bytes)
  ... (128 slots total)
```

### SBK1 (Old Format)
```
Structure per setlist (69,416 bytes):
   0: Setlist name (24 bytes)
  24: Setlist data (69,392 bytes)

First setlist: chunk_data + 69,432
Spacing: 69,416 bytes
```

## Code Templates

### Update Setlist Name
```python
def _update_sls1_names(self, raw_data: bytearray):
    """Update SLS1 (new format)."""
    sls1_offset = raw_data.find(b'SLS1')
    if sls1_offset < 0:
        return
    
    # Find positions by marker
    marker = b'\x1e\x02\x00\x00'
    separator = b'\x28\x0f\x01\x00'
    
    # ... find all positions ...
    
    # Update each setlist
    for sl_idx, setlist in enumerate(self.pcg.set_lists):
        name_bytes = setlist.name.encode('ascii')[:24].ljust(24, b'\x00')
        raw_data[position:position+24] = name_bytes

def _update_sbk1_names(self, raw_data: bytearray):
    """Update SBK1 (old format)."""
    sbk1_offset = raw_data.find(b'SBK1')
    if sbk1_offset < 0:
        return
    
    sbk1_data_start = sbk1_offset + 8
    
    for sl_idx, setlist in enumerate(self.pcg.set_lists):
        if sl_idx == 0:
            name_pos = sbk1_data_start + 69432
        else:
            name_pos = sbk1_data_start + 69432 + (sl_idx * 69416)
        
        name_bytes = setlist.name.encode('ascii')[:24].ljust(24, b'\x00')
        raw_data[name_pos:name_pos+24] = name_bytes
```

## Testing Checklist

### Before Hardware Test
- [ ] Software test passes (`test_writer_complete.py`)
- [ ] Parser reads correct data
- [ ] Other setlists not corrupted
- [ ] File size unchanged

### Hardware Test
- [ ] File loads without errors
- [ ] Setlist name displays correctly
- [ ] Slots are accessible
- [ ] Patches play correctly
- [ ] No crashes or freezes

## Common Pitfalls

### ❌ DON'T
- Update only one format
- Assume SDB1 contains names (it doesn't!)
- Skip validation after changes
- Modify without backing up

### ✓ DO
- Update both SLS1 and SBK1
- Test with parser after writing
- Verify other setlists intact
- Keep backups of working files

## Debugging

### File Rejected by Kronos
**Cause:** Formats don't match
**Fix:** Ensure both SLS1 and SBK1 are updated

### Parser Reads Wrong Name
**Cause:** SLS1 not updated
**Fix:** Check `_update_sls1_names()` is called

### Name Appears Corrupted
**Cause:** Wrong offset or size
**Fix:** Verify marker pattern and separator

### Other Setlists Corrupted
**Cause:** Writing to wrong positions
**Fix:** Check index calculations

## Future Work

### Slot Names
- Update in SLS1 (after setlist name + separator)
- Update in SBK1 (within setlist data block)
- Test each slot individually

### Metadata (Colors, Sizes)
- Update in SDB1 (new format)
- Update in SBK1 (old format)
- Use bit manipulation for split fields

### Patch References
- Update in SLD1 (new format)
- Update in SBK1 (old format)
- Validate bank/index values

## Quick Commands

```bash
# Test writer fix
python3 test_writer_complete.py

# Analyze file structure
python3 deep_chunk_analysis_v2.py

# Create test file
python3 test_dual_format_write.py
```

## Status

- ✓ Setlist names: WORKING
- ⏳ Slot names: TODO
- ⏳ Metadata: TODO
- ⏳ Patch references: TODO

## Key Takeaway

**The Kronos dual-format system requires updating BOTH SLS1 (new) and SBK1 (old) formats. Always update both or the file will be rejected!**
