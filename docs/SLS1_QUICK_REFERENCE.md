# SLS1/SLD1 Format - Quick Reference

## Format Overview

| Format | Purpose | Setlists | Slot Size | Metadata |
|--------|---------|----------|-----------|----------|
| STL1/SBK1 | Export | 1 | ~542 bytes | Color, Size, Patch Refs |
| SLS1/SLD1 | Internal | 16 | 7810 bytes | Names only |

## File Structure

```
PCG File
├─ PRG1 (Programs)
├─ CMB1 (Combis)
├─ SLS1 (Setlist Names)
│   └─ Marker + Name + Separator + 128 Slot Names
└─ SLD1 (Setlist Data)
    ├─ Setlist 0: CBK1 + 128 Combis + 24-byte gap
    ├─ Setlist 1: CBK1 + 128 Combis + 24-byte gap
    └─ ... (16 total)
```

## Quick Code Examples

### Parse PCG File

```python
from pcg_tools.reader import read_pcg_file

pcg = read_pcg_file('file.PCG')
print(f"Setlists: {len(pcg.set_lists)}")
```

### List All Setlists

```python
for sl in pcg.set_lists:
    print(f"[{sl.index}] {sl.name} - {len(sl.slots)} slots")
```

### Access Slots

```python
setlist = pcg.set_lists[0]
for slot in setlist.slots:
    if slot.name:
        print(f"[{slot.slot_index}] {slot.name}")
```

### Find Slot

```python
slot = setlist.slots[10]  # Slot 10
print(f"Name: {slot.name}")
print(f"Color: {slot.color_name}")
print(f"Type: {slot.patch_type}")
```

## Byte Offsets

### SLS1 Structure
```
Marker:     0x1E 0x02 0x00 0x00
Name:       24 bytes
Separator:  0x28 0x0F 0x01 0x00
Slot 0:     24 bytes (no marker)
Slot 1-127: Marker (4) + Name (24) = 28 bytes each
```

### SLD1 Structure
```
Setlist:
  CBK1:     4 bytes
  Size:     4 bytes
  Header:   16 bytes
  Slot 0:   7810 bytes (name at +24)
  Slot 1:   7810 bytes (name at +24)
  ...
  Slot 127: 7810 bytes (name at +24)
  Gap:      24 bytes
```

## Key Constants

```python
SLOT_SIZE = 7810  # 0x1E82
SLOTS_PER_SETLIST = 128
MAX_SETLISTS = 16
SETLIST_GAP = 24
MARKER = b'\x1E\x02\x00\x00'
SEPARATOR = b'\x28\x0F\x01\x00'
```

## Common Tasks

### Count Non-Empty Slots

```python
count = sum(1 for s in setlist.slots if s.name and len(s.name) >= 2)
```

### Search by Name

```python
results = [s for s in setlist.slots if 'piano' in s.name.lower()]
```

### Get Setlist by Name

```python
sl = next((s for s in pcg.set_lists if s.name == "NIGHTWISH"), None)
```

## Validation Checks

```python
# Check setlist count
assert len(pcg.set_lists) == 16

# Check slot count
for sl in pcg.set_lists:
    assert len(sl.slots) == 128

# Check slot indices
for sl in pcg.set_lists:
    indices = [s.slot_index for s in sl.slots]
    assert indices == list(range(128))
```

## Debugging

### Enable Debug Output

```python
from pcg_tools.pcg_parser import DEBUG
DEBUG = True  # Enable debug prints
```

### Check Format

```python
data = open('file.PCG', 'rb').read()
has_stl1 = b'STL1' in data
has_sls1 = b'SLS1' in data
print(f"STL1: {has_stl1}, SLS1: {has_sls1}")
```

### Inspect Slot

```python
slot = setlist.slots[0]
print(f"Index: {slot.slot_index}")
print(f"Name: {slot.name}")
print(f"Type: {slot.patch_type}")
print(f"Patch Index: {slot.patch_index}")
print(f"Color: {slot.color} ({slot.color_name})")
print(f"Size: {slot.text_size} ({slot.text_size_name})")
```

## Error Handling

```python
try:
    pcg = read_pcg_file('file.PCG')
except ValueError as e:
    print(f"Invalid PCG file: {e}")
except FileNotFoundError:
    print("File not found")
```

## Performance Tips

1. **Cache Results** - Don't re-parse unnecessarily
2. **Filter Early** - Skip empty slots when iterating
3. **Use Generators** - For large datasets
4. **Index Access** - Direct slot access is O(1)

## Common Pitfalls

❌ **Don't** assume color/text size are available in SLS1  
✓ **Do** check if values are 0 (not available)

❌ **Don't** modify slot indices  
✓ **Do** keep indices 0-127 in order

❌ **Don't** assume patch references exist  
✓ **Do** check patch_type before lookup

## Testing

```bash
# Run all tests
python3 test_sls1_complete.py

# Test specific file
python3 test_sls1_parsing.py your_file.PCG

# Launch GUI
python3 launch_gui_test_sls1.py
```

## Documentation

- `SLS1_PARSING_COMPLETE.md` - Implementation details
- `SLS1_USAGE_GUIDE.md` - Detailed usage examples
- `SLS1_TESTING_COMPLETE.md` - Test results
- `SESSION_FINAL_SUMMARY.md` - Complete summary

## Support

For issues or questions:
1. Check documentation in `docs/` folder
2. Run validation tests
3. Enable debug output
4. Check known limitations

---

**Quick Start:** `python3 -c "from pcg_tools.reader import read_pcg_file; pcg = read_pcg_file('file.PCG'); print(f'{len(pcg.set_lists)} setlists')"`
