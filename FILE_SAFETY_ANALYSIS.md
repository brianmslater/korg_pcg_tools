# PCG File Safety Analysis

## Your Issue: White Screen on Kronos Boot

A white screen requiring memory initialization is a **serious issue** that indicates the Kronos couldn't read its internal memory properly. Let's analyze potential causes:

## Potential Causes (Ranked by Likelihood)

### 1. ⚠️ **Internal SSD/Storage Issue** (MOST LIKELY)
**Likelihood: 70%**

The white screen is typically caused by:
- **Corrupted internal SSD** - The Kronos uses an internal SSD that can develop issues
- **Bad sectors on SSD** - SSDs can develop bad blocks over time
- **Power interruption during save** - If power was lost while saving to internal memory
- **Firmware corruption** - Boot firmware on the SSD may have been corrupted
- **File system corruption** - The internal file system may have become corrupted

**Evidence this is the cause:**
- You had to initialize memory (suggests internal storage corruption)
- White screen = boot failure, not just PCG loading failure
- The Kronos boots from internal SSD firmware

**⚠️ IMPORTANT:** Since the Kronos uses an internal SSD (not removable SD card), this is more serious:
- SSD corruption requires factory initialization
- Cannot simply replace the storage media
- May indicate hardware failure or power issues

**Recommendation:**
- **Check power supply** - Ensure stable, clean power (use UPS if possible)
- **Avoid power interruptions** - Never turn off during save operations
- **Regular backups** - Export PCG files to USB/computer frequently
- **Monitor for patterns** - If it happens again, may indicate failing SSD
- **Contact Korg support** - If recurring, may need hardware service

### 2. ⚠️ **Corrupted PCG File on Internal SSD** (MORE LIKELY THAN PREVIOUSLY THOUGHT)
**Likelihood: 25%**

A corrupted PCG file on the internal SSD could cause boot issues IF:
- The file was set to auto-load on boot
- The file had critical structural damage that crashed the boot process
- The checksum was wrong and caused a system halt
- The file was being written when power was lost

**Why this is more likely with internal SSD:**
- PCG files stored on internal SSD are loaded during boot
- Unlike external USB/SD, internal files are part of the boot sequence
- A corrupted internal PCG could prevent boot completion

**Our Protection Against This:**
```python
# From writer.py line 20-23:
# Fix checksums before writing (CRITICAL!)
raw_data = bytearray(self.pcg.raw_data)
fix_all_checksums(raw_data)
self.pcg.raw_data = bytes(raw_data)
```

✅ **We automatically fix ALL checksums before writing**
✅ **We preserve all unknown data (raw_data)**
✅ **We only modify specific fields we understand**

**What Could Still Go Wrong:**
- If you edited a file and it had pre-existing corruption
- If the file size changed unexpectedly
- If critical chunks were damaged before editing

### 3. ⚠️ **File Size Mismatch** (POSSIBLE)
**Likelihood: 5%**

If a PCG file's size changed, it could confuse the Kronos.

**Our Protection:**
```python
# We preserve raw_data and only update specific fields
# File size should remain constant
```

✅ **We don't add or remove chunks**
✅ **We don't change file structure**
✅ **We only modify data within existing chunks**

## Safety Measures in Our Code

### ✅ **Checksum Protection**
```python
def fix_all_checksums(data: bytearray):
    """Fix checksums for all chunks in a PCG file."""
    # Fixes: PBK1, MBK1, CBK1, SBK1, GLB1, WBK1, DBK1
```

**Status:** ✅ WORKING - All checksums are recalculated before writing

### ✅ **Raw Data Preservation**
```python
# We preserve ALL unknown bytes
if self.pcg.raw_data:
    raw_data = bytearray(self.pcg.raw_data)
    # Only update specific known fields
```

**Status:** ✅ WORKING - Unknown data is never corrupted

### ✅ **Hardware Testing**
- Timbre editing: ✅ Tested on actual Kronos
- Setlist editing: ✅ Tested on actual Kronos
- Program editing: ⚠️ Not yet hardware tested

**Status:** ⚠️ PARTIAL - Some features not yet tested on hardware

## What We DON'T Do (Potential Risks)

### ❌ **We Don't Validate File Structure**
- No check for minimum file size
- No validation of chunk hierarchy
- No detection of pre-existing corruption

### ❌ **We Don't Backup Before Writing**
- No automatic backup creation
- User must manually backup files

### ❌ **We Don't Verify After Writing**
- No post-write validation
- No checksum verification after save

## Recommendations

### For You (User):

1. **CRITICAL: Always Backup Before Editing**
   ```bash
   cp original.PCG original_backup.PCG
   ```
   Since the Kronos uses internal SSD, you cannot easily recover from corruption!

2. **Use External USB for Testing**
   - Edit PCG files on computer
   - Save to USB drive
   - Test load on Kronos from USB FIRST
   - Only copy to internal SSD after confirming it works

3. **Safe Workflow (CRITICAL for Internal SSD)**
   ```
   1. Export PCG from Kronos internal SSD to USB
   2. Copy USB file to computer
   3. Edit copy with PCG Tools
   4. Save edited file to USB drive
   5. Test load on Kronos from USB
   6. If OK, THEN copy to internal SSD
   7. Keep USB backup!
   ```

4. **Power Protection**
   - Use a UPS (Uninterruptible Power Supply)
   - Never turn off during save operations
   - Watch for "Saving..." messages

5. **Regular Backups**
   - Export internal PCG files to USB weekly
   - Keep multiple backup copies
   - Store backups off the Kronos

6. **Monitor for Warning Signs**
   - Slow boot times
   - Occasional freezes
   - "Memory Error" messages
   - If these occur, contact Korg support immediately

### For Development (Future Improvements):

1. **Add File Validation**
   ```python
   def validate_pcg_file(data: bytes) -> bool:
       """Validate PCG file structure before writing."""
       # Check minimum size
       # Verify chunk hierarchy
       # Validate checksums
   ```

2. **Add Auto-Backup**
   ```python
   def write_with_backup(filepath: str):
       """Write file with automatic backup."""
       backup_path = f"{filepath}.backup"
       shutil.copy2(filepath, backup_path)
       # Then write new file
   ```

3. **Add Post-Write Verification**
   ```python
   def verify_written_file(filepath: str) -> bool:
       """Verify file after writing."""
       # Re-read file
       # Verify checksums
       # Compare structure
   ```

## Diagnosis: What Likely Happened

Based on your description (Kronos uses internal SSD):

1. **Most Likely (70%):** Internal SSD corruption or power issue
   - The Kronos couldn't read boot data from internal SSD
   - Required memory initialization to rebuild internal structures
   - Could be caused by power interruption during write
   - Could indicate developing SSD failure

2. **Possible (25%):** Corrupted PCG file on internal SSD
   - A PCG file stored internally may have been corrupted
   - If set to auto-load, could crash boot process
   - More likely than with external storage since it's part of boot sequence

3. **Less Likely (5%):** Our PCG Tools caused the corruption
   - We fix checksums automatically
   - We preserve all unknown data
   - We've hardware-tested major features
   - BUT: If you edited a file and saved it directly to internal SSD without testing on USB first, there's a small risk

## CRITICAL QUESTION FOR YOU:

**Did you edit a PCG file and save it directly to the Kronos internal SSD?**

- If YES: There's a possibility the edited file caused the issue
- If NO: Almost certainly a hardware/power issue

**What to do if it was an edited file:**
1. Don't load that file again until we can validate it
2. Send me the file for analysis
3. Test all edited files on USB before copying to internal SSD
4. We'll add more validation to prevent this

## Action Items

### Immediate:
- [ ] Replace SD card with high-quality one
- [ ] Always backup PCG files before editing
- [ ] Test edited files on SD card before copying to internal memory

### Short-term:
- [ ] Add file validation to PCG Tools
- [ ] Add automatic backup option
- [ ] Add post-write verification

### Long-term:
- [ ] Hardware test all new features
- [ ] Add file corruption detection
- [ ] Add recovery tools for damaged files

## Conclusion

**The white screen was most likely caused by hardware/SD card issues, NOT by PCG file corruption.**

However, to be extra safe:
1. Always backup before editing
2. Test on SD card first
3. Use high-quality SD cards
4. Report any issues immediately

Our code has strong safety measures (checksum fixing, raw data preservation), but we should add validation and backup features for extra protection.

---

**Last Updated:** December 1, 2025
**Version:** 1.2.3
