# Original C# PCG Tools - Comprehensive Code Analysis

**Repository**: https://github.com/DaBlick/PCG-Tools  
**Author**: Michel Keijzers (MiKeSoft)  
**Analysis Date**: November 25, 2025  
**Purpose**: Identify missing features and implementation details from original C# codebase

---

## Executive Summary

After comprehensive review of the original C# PCG Tools codebase, I've identified several key features and implementation details that are either missing or partially implemented in our Python port. The original tools have significantly more advanced capabilities, particularly around:

1. **Full setlist editing with all metadata**
2. **Advanced copy/paste with dependency tracking**
3. **Parameter editing capabilities**
4. **Master file support**
5. **Multiple OS version handling**

---

## 1. SetList Implementation - CRITICAL FINDINGS

### 1.1 SetList Slot Structure (KronosSetListSlot.cs)

The original implementation reveals **complete setlist slot editing** with these fields:

#### **Name** (24 characters)
- Offset: ByteOffset + 0
- Fully editable

#### **Color** (16 colors)
- Stored as: `IntParameterBitsInByte("Color", this, 24, 5, 2, 0, 16)`
- Location: Byte offset +24, bits 5-2
- Range: 0-15 (16 colors)
- **Note**: Only available for OS versions 2.x and 3.x (NOT 1.0/1.1 or 1.5/1.6)

#### **Text Size** (5 sizes: S, XS, M, L, XL)
```csharp
public override TextSize SelectedTextSize
{
    get
    {
        return (TextSize)((BitsUtil.GetBits(PcgRoot.Content, ByteOffset + 29, 4, 4) << 2) + // MSB 1 bits
                             BitsUtil.GetBits(PcgRoot.Content, ByteOffset + 24, 7, 6)); // LSB 2 bits
    }
}
```
- **Split across two bytes**:
  - MSB (1 bit): Byte +29, bits 4-4
  - LSB (2 bits): Byte +24, bits 7-6
- Values: 0=S, 1=XS, 2=M, 3=L, 4=XL

#### **Volume** (0-127)
- Offset: ByteOffset + 28
- 1 byte, range 0-127

#### **Transpose** (-24 to +24 semitones)
```csharp
public override int Transpose
{
    get
    {
        return BitsUtil.ToSignedBit(6,
              (BitsUtil.GetBits(PcgRoot.Content, ByteOffset + 25, 7, 5) << 3) + // MSB 3 bits
               BitsUtil.GetBits(PcgRoot.Content, ByteOffset + 29, 7, 5)); // LSB 3 bits
    }
}
```
- **Split across two bytes**:
  - MSB (3 bits): Byte +25, bits 7-5
  - LSB (3 bits): Byte +29, bits 7-5
- 6-bit signed value: -24 to +24

#### **Patch Type** (Program/Combi/Song)
- Offset: ByteOffset + 24, bits 1-0
- Values: 0=Program, 1=Combi, 2=Song

#### **Bank Reference**
- Default: ByteOffset + 25 (for most OS versions)
- OS 1.5/1.6: Uses STL2 chunk at different offset

#### **Patch Index**
- Default: ByteOffset + 26
- OS 1.5/1.6: Uses STL2 chunk at different offset

#### **Description** (512 characters!)
- Offset: ByteOffset + 30 (DescriptionPcgOffset)
- Max length: 512 characters
- Supports multi-line text with \r\n

### 1.2 OS Version Differences - CRITICAL

The original code handles **multiple Kronos OS versions** with different formats:

```csharp
public enum EOsVersion
{
    EOsVersionKronos10_11,  // OS 1.0/1.1
    EOsVersionKronos15_16,  // OS 1.5/1.6 - SPECIAL FORMAT
    EOsVersionKronos2x,     // OS 2.x
    EOsVersionKronos3x      // OS 3.x
}
```

**OS 1.5/1.6 has a completely different structure**:
- Uses **STL2** and **SBK2** chunks for additional data
- Bank/patch references stored in separate location
- Special handling for EXi banks (U-AA through U-GG)

### 1.3 SetList Features We're Missing

**From SetListSlot.cs**:
1. ✅ Name editing - WE HAVE THIS
2. ✅ Color (16 colors) - WE HAVE THIS  
3. ❌ **Text Size editing** - MISSING (5 sizes: S, XS, M, L, XL)
4. ✅ Volume - WE HAVE THIS
5. ✅ Transpose - WE HAVE THIS
6. ❌ **Description editing** (512 chars) - PARTIALLY IMPLEMENTED
7. ❌ **Patch reference editing** - MISSING
8. ❌ **Clear slot operation** - MISSING
9. ❌ **OS version detection** - MISSING

---

## 2. Advanced Copy/Paste Features

### 2.1 Dependency Tracking (CopyPasteCommands.cs)

The original has **sophisticated dependency tracking**:

```csharp
// When copying a combi, automatically copy referenced programs
// When copying a setlist slot, copy both combi AND programs
```

**Features**:
- Copy with dependencies (programs used by combis)
- Copy with master file resolution
- Swap operations
- Clipboard recall
- Cross-window paste with validation

### 2.2 Copy Settings Dialog

The original has a **Copy/Paste Settings Dialog** (copy_paste_dialog.py exists but not fully integrated):
- Choose what to copy (patch only, with dependencies, etc.)
- Filter options
- Validation before paste

---

## 3. Master File Support

### 3.1 Master Files Feature

**From MasterFilesViewModel.cs**:
- Load a "master" PCG file that other files can reference
- When a patch references a program/combi not in current file, look it up in master
- Automatic resolution of external references

```csharp
var masterPcgMemory = MasterFiles.MasterFiles.Instances.FindMasterPcg(Root.Model);
if ((masterPcgMemory != null) && (masterPcgMemory.FileName != Root.FileName))
{
    var programBank = masterPcgMemory.ProgramBanks.BankCollection.FirstOrDefault(
        item => (item.PcgId == UsedProgramBank.PcgId) && item.IsFilled);
    return programBank == null ? null : programBank[programId] as Program;
}
```

**Use Case**: 
- Load factory PCG as master
- Work with smaller user PCG files
- Setlist slots can reference programs from master file

---

## 4. Parameter Editing

### 4.1 Edit Windows

The original has **dedicated edit windows**:
- `WindowEditSingleSetListSlot.xaml` - Full slot editor
- `WindowEditMultipleSetListSlots.xaml` - Batch editor
- `WindowEditSingleSetList.xaml` - Setlist properties editor

### 4.2 Parameter System

**From NewParameters namespace**:
- `IntParameterBitsInByte` - Edit specific bits in bytes
- `IntParameter` - Full byte/word parameters
- Parameter validation and constraints
- Undo/redo support at parameter level

---

## 5. Bank ID Handling

### 5.1 EXi Bank IDs (Critical for Setlists)

**From KronosSetListSlot.cs**:

```csharp
// EXi banks (U-AA through U-GG) have special handling
if (bank.Type == BankType.EType.UserExtended)
{
    switch (PcgRoot.Model.OsVersion)
    {
        case Models.EOsVersion.EOsVersionKronos10_11:
            Util.SetInt(PcgRoot, PcgRoot.Content, DefaultBankOffset, 1, 23); // 23 = U-G
            break;
        case Models.EOsVersion.EOsVersionKronos15_16:
            Util.SetInt(PcgRoot, PcgRoot.Content, DefaultBankOffset, 1, 23); // 23 = U-G
            Util.SetInt(PcgRoot, PcgRoot.Content, Stl2BankOffset, 1, bank.PcgId);
            break;
        case Models.EOsVersion.EOsVersionKronos2x:
            Util.SetInt(PcgRoot, PcgRoot.Content, DefaultBankOffset, 1, bank.PcgId);
            break;
    }
}
```

**Key Insight**: EXi banks are stored differently depending on OS version!

---

## 6. Additional Features We're Missing

### 6.1 List Generators

**From list_generators.py** - We have these, but original has more options:
- ✅ Program usage list
- ✅ Combi content list (short/long)
- ✅ Differences list
- ❌ **Cubase instrument definition export**
- ❌ **XSL stylesheet generation**
- ❌ **ASCII table format**

### 6.2 Patch Operations

**From operations.py** - We have basic operations, but missing:
- ❌ **Swap patches** (not just move)
- ❌ **Compact bank** (remove gaps)
- ❌ **Sort by category**
- ❌ **Batch operations** (apply to multiple selections)

### 6.3 GUI Features

**From GUI code**:
- ❌ **Favorite column display**
- ❌ **Content type column** (Sampled/Modeled)
- ❌ **Multi-window MDI** (we have single window)
- ❌ **Status bar with statistics**
- ❌ **Dirty flag tracking** (*)
- ❌ **Revert to saved**

### 6.4 Model Support

**From Model directory**:
The original supports **17 different Korg models**:
- Kronos/Kronos X (fully tested)
- Oasys
- Triton (all variants: Classic, Extreme, Le, Studio, Rack)
- Karma
- M3/M50
- Krome/Krome EX
- Kross/Kross 2
- Trinity
- Z1
- MS2000
- MicroKorg XL
- MicroStation
- M1
- 01/W series
- T series
- X series

---

## 7. Critical Implementation Details

### 7.1 Bit Manipulation Utilities

**From BitsUtil.cs**:
```csharp
public static int GetBits(byte[] content, int byteOffset, int highBit, int lowBit)
public static void SetBits(byte[] content, int byteOffset, int highBit, int lowBit, int value)
public static int ToSignedBit(int nrOfBits, int value)
```

We need these for:
- Text size (split across 2 bytes)
- Transpose (split across 2 bytes, signed)
- Color (bit field)
- Patch type (bit field)

### 7.2 Chunk Structure

**From PCG Structure Kronos.txt**:

```
# Set List Structure
0000 16A8  "SLS1"  Set Lists
0000 16B4  "SLD1"  Set List Data (slot names and metadata)
0000 16C0  "SDB1"  Set List Database (colors, sizes)
0007 24D8  "STL1"  Set Lists (OS 1.5/1.6)
0007 24E4  "SBK1"  Set List Bank (OS 1.5/1.6)
```

**Key Chunks**:
- **SLS1**: Container for all setlists
- **SLD1**: Slot data (names, descriptions, patch refs)
- **SDB1**: Metadata (colors, text sizes) - **WE HAVEN'T FULLY PARSED THIS**
- **STL1/SBK1**: OS 1.5/1.6 specific format

---

## 8. What We've Implemented vs Original

### 8.1 Fully Implemented ✅
1. Basic file reading/writing
2. Program/Combi name editing
3. Category editing
4. Favorite flags
5. Basic copy/paste
6. Move up/down
7. Sort patches
8. List generators (basic)
9. CLI interface
10. Setlist slot name editing
11. Setlist slot color (16 colors)
12. Setlist slot volume
13. Setlist slot transpose
14. Patch reference parsing (bank + index)

### 8.2 Partially Implemented ⚠️
1. Setlist editing (names only, not full metadata)
2. Description editing (UI exists, persistence unclear)
3. Copy/paste (basic, no dependency tracking)
4. Multi-window support (single window only)

### 8.3 Not Implemented ❌
1. **Text size editing** (5 sizes)
2. **Description persistence** (512 chars)
3. **Patch reference editing** (change which program/combi)
4. **Clear slot operation**
5. **OS version detection and handling**
6. **Master file support**
7. **Dependency tracking in copy/paste**
8. **Parameter editing system**
9. **Swap operations**
10. **Compact bank**
11. **Batch operations**
12. **Cubase export**
13. **Undo/redo** (at parameter level)
14. **Favorite column display**
15. **Status bar**
16. **Dirty flag tracking**
17. **Revert to saved**

---

## 9. Priority Recommendations

### 9.1 HIGH PRIORITY (User-Facing Features)

1. **Text Size Editing** ⭐⭐⭐
   - Location: Byte +29 (bit 4) + Byte +24 (bits 7-6)
   - 5 values: S, XS, M, L, XL
   - Visible on Kronos display

2. **Patch Reference Editing** ⭐⭐⭐
   - Allow changing which program/combi a slot uses
   - Update bank + index bytes
   - Critical for setlist workflow

3. **Description Persistence** ⭐⭐
   - 512 character descriptions
   - Multi-line support
   - Currently reads but may not write correctly

4. **Clear Slot Operation** ⭐⭐
   - Reset slot to default (I-A000)
   - Clear name, description, reset volume/transpose

5. **OS Version Detection** ⭐⭐
   - Detect OS 1.0/1.1 vs 1.5/1.6 vs 2.x vs 3.x
   - Handle different chunk structures
   - Critical for correct parsing

### 9.2 MEDIUM PRIORITY (Workflow Improvements)

6. **Swap Slots** ⭐
   - Exchange two slots completely
   - Useful for reordering

7. **Batch Operations** ⭐
   - Apply changes to multiple slots
   - Set volume/transpose for selection

8. **Status Bar** ⭐
   - Show file statistics
   - Model type
   - Dirty flag

9. **Revert to Saved** ⭐
   - Undo all changes
   - Reload from disk

### 9.3 LOW PRIORITY (Advanced Features)

10. **Master File Support**
    - Complex feature
    - Niche use case

11. **Parameter Editing**
    - Very complex
    - Use hardware instead

12. **Cubase Export**
    - Specific use case
    - Low demand

---

## 10. Code Snippets to Port

### 10.1 Text Size Reading/Writing

```python
def get_text_size(data, byte_offset):
    """Get text size from split bit fields."""
    msb = (data[byte_offset + 29] >> 4) & 0x01  # Bit 4 of byte +29
    lsb = (data[byte_offset + 24] >> 6) & 0x03  # Bits 7-6 of byte +24
    return (msb << 2) | lsb

def set_text_size(data, byte_offset, size):
    """Set text size in split bit fields."""
    # MSB (1 bit) goes to byte +29, bit 4
    data[byte_offset + 29] = (data[byte_offset + 29] & 0xEF) | ((size >> 2) << 4)
    # LSB (2 bits) go to byte +24, bits 7-6
    data[byte_offset + 24] = (data[byte_offset + 24] & 0x3F) | ((size & 0x03) << 6)
```

### 10.2 Transpose Reading/Writing

```python
def get_transpose(data, byte_offset):
    """Get transpose from split bit fields (signed 6-bit)."""
    msb = (data[byte_offset + 25] >> 5) & 0x07  # Bits 7-5 of byte +25
    lsb = (data[byte_offset + 29] >> 5) & 0x07  # Bits 7-5 of byte +29
    value = (msb << 3) | lsb
    # Convert to signed
    if value & 0x20:  # Bit 5 is sign bit
        value = value - 64
    return value

def set_transpose(data, byte_offset, transpose):
    """Set transpose in split bit fields (signed 6-bit)."""
    if transpose < 0:
        value = transpose + 64
    else:
        value = transpose
    # MSB (3 bits) go to byte +25, bits 7-5
    data[byte_offset + 25] = (data[byte_offset + 25] & 0x1F) | ((value >> 3) << 5)
    # LSB (3 bits) go to byte +29, bits 7-5
    data[byte_offset + 29] = (data[byte_offset + 29] & 0x1F) | ((value & 0x07) << 5)
```

### 10.3 OS Version Detection

```python
def detect_os_version(pcg_data):
    """Detect Kronos OS version from PCG structure."""
    # Check for STL1/SBK1 chunks (OS 1.5/1.6)
    if b'STL1' in pcg_data and b'SBK1' in pcg_data:
        return 'OS_1.5_1.6'
    
    # Check for color support in SLD1 (OS 2.x+)
    # OS 1.0/1.1 doesn't have color field
    # This requires parsing the actual slot structure
    
    # Default to OS 2.x/3.x
    return 'OS_2.x_3.x'
```

---

## 11. Testing Strategy

### 11.1 Test Files Needed

1. **OS 1.0/1.1 PCG** - No color support
2. **OS 1.5/1.6 PCG** - STL1/SBK1 format
3. **OS 2.x PCG** - Color support
4. **OS 3.x PCG** - Latest format
5. **PCG with EXi banks** - U-AA through U-GG
6. **PCG with all text sizes** - S, XS, M, L, XL
7. **PCG with long descriptions** - 512 character test

### 11.2 Validation Tests

1. Read text size from all slots
2. Write text size and verify on Kronos
3. Read/write transpose with negative values
4. Edit patch references and verify
5. Clear slots and verify reset
6. Test OS version detection

---

## 12. Documentation References

### 12.1 Key Files in Original Repo

- `/KorgKronosTools/Model/KronosSpecific/Synth/KronosSetListSlot.cs` - **CRITICAL**
- `/KorgKronosTools/Model/Common/Synth/PatchSetLists/SetListSlot.cs` - Base class
- `/Documentation/PCG Structure Kronos.txt` - Format documentation
- `/Documentation/Manual.pdf` - User manual (11MB)
- `/Common/Utils/BitsUtil.cs` - Bit manipulation utilities

### 12.2 Useful Code Patterns

The original uses:
- MVVM pattern (Model-View-ViewModel)
- WPF for GUI
- Extensive use of interfaces (ISetList, ISetListSlot, etc.)
- Property change notifications
- Command pattern for operations

---

## 13. Conclusion

The original C# PCG Tools is a **mature, feature-rich application** with significantly more capabilities than our Python port. The most critical missing features are:

1. **Text size editing** - Visible on Kronos, users expect this
2. **Patch reference editing** - Core setlist workflow
3. **OS version handling** - Required for correct parsing
4. **Description persistence** - May not be working correctly

The good news: We have the **complete source code** to reference, and the binary format is well-documented. The bit manipulation for text size and transpose is complex but straightforward to implement.

**Recommendation**: Focus on the HIGH PRIORITY items first, as these are user-visible features that affect the core setlist editing workflow.

---

**Analysis completed**: November 25, 2025  
**Next steps**: Implement text size editing and patch reference editing
