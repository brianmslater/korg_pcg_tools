# SLS1/SLD1 Format - Usage Guide

## Quick Start

### Parsing SLS1 Setlists

```python
from pcg_tools.pcg_parser import PcgBinaryParser
from pcg_tools.models import PcgFile, PcgHeader, WorkstationModel

# Read PCG file
with open('your_file.PCG', 'rb') as f:
    data = f.read()

# Create PCG object
header = PcgHeader(
    magic=b'KORG',
    product_id=0,
    file_type=0,
    major_version=1,
    minor_version=0,
    model=WorkstationModel.KRONOS
)
pcg = PcgFile(header=header, raw_data=data)

# Parse setlists
parser = PcgBinaryParser(data)
parser.parse_sls1_chunk(pcg)

# Access setlists
for setlist in pcg.set_lists:
    print(f"Setlist {setlist.index}: {setlist.name}")
    for slot in setlist.slots:
        if slot.name:
            print(f"  [{slot.slot_index:3d}] {slot.name}")
```

## SetListSlot Fields

### Available Fields (SLS1 Format)

- `set_list_index` - Setlist number (0-15)
- `slot_index` - Slot number (0-127)
- `name` - Combi name from SLD1
- `description` - Custom label from SLS1 (if different from name)
- `patch_type` - Always "Combi" for SLS1 format
- `patch_index` - Slot index (0-127)

### Not Available (SLS1 Format)

- `color` - Set to 0 (not available in SLS1)
- `text_size` - Set to 0 (not available in SLS1)
- `patch_bank` - Empty string (not available in SLS1)
- `transpose` - Set to 0
- `volume` - Set to 127 (default)

## Format Detection

```python
# Check which format is present
has_stl1 = b'STL1' in data  # Single setlist export
has_sls1 = b'SLS1' in data  # Internal 16 setlists

if has_stl1:
    parser.parse_stl1_chunk(pcg)  # Parse STL1 format
elif has_sls1:
    parser.parse_sls1_chunk(pcg)  # Parse SLS1 format
```

## Common Tasks

### List All Setlists

```python
for sl in pcg.set_lists:
    non_empty = sum(1 for s in sl.slots if s.name and len(s.name) >= 2)
    print(f"[{sl.index:2d}] {sl.name} - {non_empty} slots")
```

### Find a Specific Slot

```python
def find_slot(pcg, setlist_index, slot_index):
    """Find a specific slot by setlist and slot index."""
    if setlist_index < len(pcg.set_lists):
        setlist = pcg.set_lists[setlist_index]
        for slot in setlist.slots:
            if slot.slot_index == slot_index:
                return slot
    return None

# Usage
slot = find_slot(pcg, 0, 10)  # Setlist 0, Slot 10
if slot:
    print(f"Slot: {slot.name}")
```

### Search for Slots by Name

```python
def search_slots(pcg, search_term):
    """Search for slots containing a term in their name."""
    results = []
    for setlist in pcg.set_lists:
        for slot in setlist.slots:
            if slot.name and search_term.lower() in slot.name.lower():
                results.append((setlist, slot))
    return results

# Usage
results = search_slots(pcg, "piano")
for setlist, slot in results:
    print(f"Setlist {setlist.index}, Slot {slot.slot_index}: {slot.name}")
```

### Count Empty Slots

```python
def count_empty_slots(pcg):
    """Count empty slots in all setlists."""
    total = 0
    empty = 0
    for setlist in pcg.set_lists:
        for slot in setlist.slots:
            total += 1
            if not slot.name or len(slot.name) < 2:
                empty += 1
    return empty, total

empty, total = count_empty_slots(pcg)
print(f"Empty: {empty}/{total} ({empty*100//total}%)")
```

## Validation

### Check Setlist Integrity

```python
def validate_setlists(pcg):
    """Validate setlist structure."""
    issues = []
    
    # Check count
    if len(pcg.set_lists) != 16:
        issues.append(f"Expected 16 setlists, found {len(pcg.set_lists)}")
    
    # Check each setlist
    for setlist in pcg.set_lists:
        # Check slot count
        if len(setlist.slots) != 128:
            issues.append(f"Setlist {setlist.index} has {len(setlist.slots)} slots")
        
        # Check slot indices
        indices = [s.slot_index for s in setlist.slots]
        if indices != list(range(128)):
            issues.append(f"Setlist {setlist.index} has incorrect indices")
    
    return issues

issues = validate_setlists(pcg)
if issues:
    print("Issues found:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("✓ All validation checks passed")
```

## Performance Tips

1. **Cache Results**: If you need to search multiple times, cache the parsed data
2. **Filter Early**: Filter empty slots early to reduce processing
3. **Use Generators**: For large datasets, use generators instead of lists

```python
# Generator for non-empty slots
def non_empty_slots(pcg):
    for setlist in pcg.set_lists:
        for slot in setlist.slots:
            if slot.name and len(slot.name) >= 2:
                yield setlist, slot

# Usage
for setlist, slot in non_empty_slots(pcg):
    print(f"{setlist.name}: {slot.name}")
```

## Troubleshooting

### No Setlists Found

```python
if not pcg.set_lists:
    # Check if file has SLS1 chunk
    if b'SLS1' not in data:
        print("File does not contain SLS1 chunk")
    else:
        print("Parsing failed - check file format")
```

### Incorrect Slot Names

```python
# Verify SLD1 chunk is present
if b'SLD1' not in data:
    print("Warning: No SLD1 chunk - slot names may be incomplete")
```

### Empty Setlists

```python
# Check if setlist has any non-empty slots
for setlist in pcg.set_lists:
    non_empty = sum(1 for s in setlist.slots if s.name and len(s.name) >= 2)
    if non_empty == 0:
        print(f"Setlist {setlist.index} is empty")
```

## See Also

- `SLS1_PARSING_COMPLETE.md` - Implementation details
- `SESSION_SUMMARY_SLS1_COMPLETE.md` - Development summary
- `test_sls1_complete.py` - Complete test example
- `test_both_setlist_formats.py` - STL1 vs SLS1 comparison
