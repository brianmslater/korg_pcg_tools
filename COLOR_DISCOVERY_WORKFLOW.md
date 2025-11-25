# SDB1 Color Discovery - Quick Workflow

## 🎯 Goal
Discover where setlist slot colors are stored in the SDB1 chunk.

## 📋 Quick Steps

### 1. Make Test File (On Kronos)
```
Load: soundcheck9_25_25_combined2.PCG
Go to: SC 10/4 setlist → Slot 0
Change: Navy → Brick
Save as: soundcheck_color_test.PCG
Copy to computer: test_files/
```

### 2. Compare Files
```bash
python3 compare_pcg_files.py \
  test_files/soundcheck9_25_25_combined2.PCG \
  test_files/soundcheck_color_test.PCG
```

### 3. Find Color Change
Look for:
- Byte changing from `0xA4` (164) or `0xA5` (165) → `0x88` (136) or `0x89` (137)
- In SDB1 chunk
- Note the offset

### 4. Test Pattern
```bash
python3 test_color_pattern.py \
  test_files/soundcheck9_25_25_combined2.PCG \
  0x[BASE] 0x[SETLIST_MULT] 0x[SLOT_MULT]
```

### 5. Verify
- Test with more color changes
- Confirm pattern works for all setlists
- Document findings

## 🔍 What to Look For

### In Comparison Output
```
Group X: 1 bytes changed
  Location: 0x00XXXXXX
  Chunk: SDB1 (offset +YYYY)
  
  Byte changes:
    0x00XXXXXX: 0xA4 (164) → 0x88 (136)
                 Navy      → Brick      ← THIS IS IT!
```

### Pattern Calculation
```
If color is at SDB1 + 0x12345 for Setlist 4, Slot 0:

Try patterns like:
- 0x12345 = base + (4 * X) + (0 * Y)
- Solve for base, X, Y by testing more slots
```

## 📊 Test Matrix

| Test | Setlist | Slot | From | To | Purpose |
|------|---------|------|------|----|----|
| 1 | 4 | 0 | Navy | Brick | Find base pattern |
| 2 | 4 | 1 | Indigo | Gold | Verify slot multiplier |
| 3 | 4 | 10 | ? | Brick | Verify slot multiplier |
| 4 | 0 | 0 | ? | Navy | Verify setlist multiplier |
| 5 | 8 | 0 | ? | Gold | Verify setlist multiplier |

## 🛠️ Tools Created

1. **`compare_pcg_files.py`** - Binary comparison tool
2. **`test_color_pattern.py`** - Pattern verification tool
3. **`BINARY_COMPARISON_GUIDE.md`** - Detailed guide
4. **`COLOR_DISCOVERY_WORKFLOW.md`** - This quick reference

## ✅ Success Criteria

Pattern is confirmed when:
- ✓ All 5 test slots match expected colors
- ✓ Pattern works across different setlists
- ✓ Pattern works for all 128 slots
- ✓ Pattern works for all 16 setlists

## 📝 Document Your Findings

Create `SDB1_COLOR_FINDINGS.md`:
```markdown
# SDB1 Color Structure - DISCOVERED

## Pattern
offset = SDB1 + 0x[BASE] + (setlist_idx * 0x[X]) + (slot_idx * 0x[Y])

## Verified Test Cases
[List all tests that passed]

## Implementation
[Code snippet for parser]
```

## 🚀 After Discovery

1. Update `pcg_parser.py` with `_parse_sdb1_colors()`
2. Test with multiple PCG files
3. Update GUI to show colors
4. Update documentation
5. Close the issue!

---

**Status:** 🔬 Ready for Testing  
**Next Action:** Make test file on Kronos  
**Expected Time:** 15-30 minutes
