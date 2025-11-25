# PCG Tools Python - Implementation Plan
## Based on Original C# Code Analysis

**Created**: November 25, 2025  
**Status**: Planning Phase  
**Goal**: Achieve feature parity with original C# PCG Tools for core setlist functionality

---

## Overview

This plan implements the missing features discovered in the original C# codebase analysis. We'll focus on **user-visible, high-impact features** first, particularly those affecting the setlist editing workflow.

---

## Phase 1: Foundation - Bit Manipulation & Utilities (Week 1)

### 1.1 Create Bit Utilities Module
**File**: `korg_pcg_tools/pcg_tools/bit_utils.py`

**Purpose**: Low-level bit manipulation for complex field parsing

```python
def get_bits(data, byte_offset, high_bit, low_bit):
    """Extract bits from a byte range."""
    
def set_bits(data, byte_offset, high_bit, low_bit, value):
    """Set bits in a byte range."""
    
def to_signed_bit(num_bits, value):
    """Convert unsigned to signed bit value."""
    
def from_signed_bit(num_bits, value):
    """Convert signed to unsigned bit value."""
```

**Why First**: All advanced features depend on bit manipulation

**Testing**: 
- Unit tests for all bit operations
- Test with known values from C# code
- Verify edge cases (sign bits, overflow)

**Estimated Time**: 1 day

---

### 1.2 OS Version Detection
**File**: `korg_pcg_tools/pcg_tools/os_version.py`

**Purpose**: Detect Kronos OS version to handle format differences

```python
class KronosOsVersion(Enum):
    OS_1_0_1_1 = "1.0/1.1"  # No color support
    OS_1_5_1_6 = "1.5/1.6"  # STL1/SBK1 format
    OS_2_X = "2.x"          # Color support
    OS_3_X = "3.x"          # Latest

def detect_os_version(pcg_data):
    """Detect OS version from PCG structure."""
    
def get_slot_offsets(os_version):
    """Get byte offsets based on OS version."""
```

**Why Now**: Different OS versions have different structures

**Testing**:
- Test with PCG files from each OS version
- Verify chunk detection (STL1/SBK1 presence)
- Validate offset calculations

**Estimated Time**: 2 days

---

## Phase 2: Text Size Implementation (Week 1-2)

### 2.1 Text Size Reading
**File**: `korg_pcg_tools/pcg_tools/models.py` (extend SetListSlot)

**Implementation**:
```python
class TextSize(Enum):
    S = 0   # Small
    XS = 1  # Extra Small
    M = 2   # Medium
    L = 3   # Large
    XL = 4  # Extra Large

@property
def text_size(self):
    """Get text size from split bit fields."""
    if not self.raw_data or len(self.raw_data) < 30:
        return TextSize.M  # Default
    
    # MSB (1 bit): Byte +29, bit 4
    msb = (self.raw_data[29] >> 4) & 0x01
    # LSB (2 bits): Byte +24, bits 7-6
    lsb = (self.raw_data[24] >> 6) & 0x03
    
    value = (msb << 2) | lsb
    return TextSize(value)

@text_size.setter
def text_size(self, size: TextSize):
    """Set text size in split bit fields."""
    if not self.raw_data or len(self.raw_data) < 30:
        return
    
    value = size.value
    # MSB (1 bit) -> byte +29, bit 4
    self.raw_data[29] = (self.raw_data[29] & 0xEF) | ((value >> 2) << 4)
    # LSB (2 bits) -> byte +24, bits 7-6
    self.raw_data[24] = (self.raw_data[24] & 0x3F) | ((value & 0x03) << 6)
```

**Testing**:
- Read text sizes from test files
- Verify all 5 sizes parse correctly
- Test with files from different OS versions

**Estimated Time**: 1 day

---

### 2.2 Text Size Writing & GUI
**Files**: 
- `korg_pcg_tools/pcg_tools/writer.py` (ensure text size persists)
- `korg_pcg_tools/pcg_tools/gui_qt.py` (add UI control)

**GUI Changes**:
```python
# Add to setlist slot editor
self.text_size_combo = QComboBox()
self.text_size_combo.addItems(['S', 'XS', 'M', 'L', 'XL'])
self.text_size_combo.currentIndexChanged.connect(self.on_text_size_changed)
```

**Testing**:
- Write text size and verify in hex editor
- Load modified file on Kronos and verify display
- Test all 5 sizes

**Estimated Time**: 2 days

---

## Phase 3: Enhanced Transpose Handling (Week 2)

### 3.1 Fix Transpose Reading/Writing
**File**: `korg_pcg_tools/pcg_tools/models.py`

**Current Issue**: We may not be handling the split bit fields correctly

**Implementation**:
```python
@property
def transpose(self):
    """Get transpose from split bit fields (signed 6-bit)."""
    if not self.raw_data or len(self.raw_data) < 30:
        return 0
    
    # MSB (3 bits): Byte +25, bits 7-5
    msb = (self.raw_data[25] >> 5) & 0x07
    # LSB (3 bits): Byte +29, bits 7-5
    lsb = (self.raw_data[29] >> 5) & 0x07
    
    value = (msb << 3) | lsb
    
    # Convert to signed (6-bit, range -32 to +31)
    if value & 0x20:  # Bit 5 is sign bit
        value = value - 64
    
    return value

@transpose.setter
def transpose(self, value: int):
    """Set transpose in split bit fields (signed 6-bit)."""
    if not self.raw_data or len(self.raw_data) < 30:
        return
    
    # Clamp to valid range
    value = max(-24, min(24, value))
    
    # Convert to unsigned
    if value < 0:
        value = value + 64
    
    # MSB (3 bits) -> byte +25, bits 7-5
    self.raw_data[25] = (self.raw_data[25] & 0x1F) | ((value >> 3) << 5)
    # LSB (3 bits) -> byte +29, bits 7-5
    self.raw_data[29] = (self.raw_data[29] & 0x1F) | ((value & 0x07) << 5)
```

**Testing**:
- Test negative transpose values (-24 to -1)
- Test positive transpose values (0 to +24)
- Verify on Kronos hardware

**Estimated Time**: 1 day

---

## Phase 4: Patch Reference Editing (Week 2-3)

### 4.1 Patch Reference Model
**File**: `korg_pcg_tools/pcg_tools/models.py`

**Add to SetListSlot**:
```python
@property
def patch_type(self):
    """Get patch type (Program/Combi/Song)."""
    if not self.raw_data or len(self.raw_data) < 25:
        return 'Program'
    
    type_value = self.raw_data[24] & 0x03  # Bits 1-0
    return ['Program', 'Combi', 'Song'][type_value]

@patch_type.setter
def patch_type(self, value: str):
    """Set patch type."""
    if not self.raw_data or len(self.raw_data) < 25:
        return
    
    type_map = {'Program': 0, 'Combi': 1, 'Song': 2}
    type_value = type_map.get(value, 0)
    
    self.raw_data[24] = (self.raw_data[24] & 0xFC) | type_value

@property
def patch_bank_id(self):
    """Get referenced bank ID."""
    if not self.raw_data or len(self.raw_data) < 26:
        return 0
    return self.raw_data[25]

@patch_bank_id.setter
def patch_bank_id(self, value: int):
    """Set referenced bank ID."""
    if not self.raw_data or len(self.raw_data) < 26:
        return
    self.raw_data[25] = value & 0xFF

@property
def patch_index(self):
    """Get referenced patch index (0-127)."""
    if not self.raw_data or len(self.raw_data) < 27:
        return 0
    return self.raw_data[26]

@patch_index.setter
def patch_index(self, value: int):
    """Set referenced patch index."""
    if not self.raw_data or len(self.raw_data) < 27:
        return
    self.raw_data[26] = value & 0x7F
```

**Testing**:
- Read existing patch references
- Change references and verify
- Test with Programs, Combis, and Songs

**Estimated Time**: 2 days

---

### 4.2 Patch Reference GUI
**File**: `korg_pcg_tools/pcg_tools/gui_qt.py`

**Add Patch Selector**:
```python
class PatchReferenceWidget(QWidget):
    """Widget for selecting patch references."""
    
    def __init__(self, pcg_file, parent=None):
        super().__init__(parent)
        self.pcg_file = pcg_file
        
        layout = QVBoxLayout()
        
        # Type selector
        self.type_combo = QComboBox()
        self.type_combo.addItems(['Program', 'Combi', 'Song'])
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        
        # Bank selector
        self.bank_combo = QComboBox()
        
        # Patch selector
        self.patch_combo = QComboBox()
        
        layout.addWidget(QLabel("Type:"))
        layout.addWidget(self.type_combo)
        layout.addWidget(QLabel("Bank:"))
        layout.addWidget(self.bank_combo)
        layout.addWidget(QLabel("Patch:"))
        layout.addWidget(self.patch_combo)
        
        self.setLayout(layout)
    
    def on_type_changed(self, patch_type):
        """Update bank list when type changes."""
        self.bank_combo.clear()
        if patch_type == 'Program':
            banks = self.pcg_file.program_banks
        elif patch_type == 'Combi':
            banks = self.pcg_file.combi_banks
        else:
            return
        
        for bank in banks:
            self.bank_combo.addItem(f"{bank.bank_id} - {bank.name}", bank)
```

**Testing**:
- Select different patch types
- Browse banks and patches
- Apply changes and verify

**Estimated Time**: 2 days

---

## Phase 5: Description Persistence (Week 3)

### 5.1 Verify Description Writing
**File**: `korg_pcg_tools/pcg_tools/writer.py`

**Investigation**:
1. Check if descriptions are being written to raw_data
2. Verify 512-character limit
3. Test multi-line descriptions (\r\n)

**Implementation**:
```python
def write_setlist_slot_description(slot, description):
    """Write description to slot raw data."""
    if not slot.raw_data or len(slot.raw_data) < 542:  # 30 + 512
        return
    
    # Truncate to 512 chars
    description = description[:512]
    
    # Convert to bytes
    desc_bytes = description.encode('ascii', errors='ignore')
    
    # Pad with nulls
    desc_bytes = desc_bytes.ljust(512, b'\x00')
    
    # Write to offset +30
    slot.raw_data[30:542] = desc_bytes
```

**Testing**:
- Write short descriptions
- Write 512-character descriptions
- Write multi-line descriptions
- Verify on Kronos

**Estimated Time**: 1 day

---

### 5.2 Description Editor GUI
**File**: `korg_pcg_tools/pcg_tools/gui_qt.py`

**Enhance Editor**:
```python
# Replace single-line description with multi-line
self.description_edit = QTextEdit()
self.description_edit.setMaximumHeight(100)
self.description_edit.setPlaceholderText("Enter description (max 512 characters)")
self.description_edit.textChanged.connect(self.on_description_changed)

# Add character counter
self.char_count_label = QLabel("0 / 512")

def on_description_changed(self):
    text = self.description_edit.toPlainText()
    length = len(text)
    self.char_count_label.setText(f"{length} / 512")
    
    if length > 512:
        self.char_count_label.setStyleSheet("color: red;")
    else:
        self.char_count_label.setStyleSheet("")
```

**Testing**:
- Enter multi-line text
- Test character limit
- Verify persistence

**Estimated Time**: 1 day

---

## Phase 6: Clear Slot Operation (Week 3)

### 6.1 Clear Slot Implementation
**File**: `korg_pcg_tools/pcg_tools/operations.py`

**Add Operation**:
```python
def clear_setlist_slot(slot):
    """Clear a setlist slot to default state."""
    if not slot.raw_data:
        return
    
    # Clear name (24 bytes)
    slot.raw_data[0:24] = b'\x00' * 24
    
    # Set to Program type
    slot.raw_data[24] = (slot.raw_data[24] & 0xFC) | 0x00
    
    # Set to bank I-A (0x00)
    slot.raw_data[25] = 0x00
    
    # Set to patch 0
    slot.raw_data[26] = 0x00
    
    # Reset volume to 127
    slot.raw_data[28] = 0x7F
    
    # Reset transpose to 0
    slot.transpose = 0
    
    # Reset text size to M
    slot.text_size = TextSize.M
    
    # Clear description (512 bytes)
    slot.raw_data[30:542] = b'\x00' * 512
    
    slot.name = "Init Slot"
```

**Testing**:
- Clear various slots
- Verify all fields reset
- Test on Kronos

**Estimated Time**: 1 day

---

### 6.2 Clear Slot GUI
**File**: `korg_pcg_tools/pcg_tools/gui_qt.py`

**Add Menu/Button**:
```python
# Add to context menu
clear_action = QAction("Clear Slot", self)
clear_action.triggered.connect(self.clear_selected_slots)
context_menu.addAction(clear_action)

def clear_selected_slots(self):
    """Clear selected setlist slots."""
    selected = self.get_selected_slots()
    
    if not selected:
        return
    
    reply = QMessageBox.question(
        self,
        "Clear Slots",
        f"Clear {len(selected)} slot(s)? This will reset them to default state.",
        QMessageBox.Yes | QMessageBox.No
    )
    
    if reply == QMessageBox.Yes:
        for slot in selected:
            clear_setlist_slot(slot)
        self.refresh_display()
```

**Testing**:
- Clear single slot
- Clear multiple slots
- Verify confirmation dialog

**Estimated Time**: 1 day

---

## Phase 7: Advanced Features (Week 4)

### 7.1 Swap Slots Operation
**File**: `korg_pcg_tools/pcg_tools/operations.py`

```python
def swap_setlist_slots(slot1, slot2):
    """Swap two setlist slots completely."""
    # Swap raw data
    slot1.raw_data, slot2.raw_data = slot2.raw_data, slot1.raw_data
    
    # Update indices
    slot1.index, slot2.index = slot2.index, slot1.index
```

**Estimated Time**: 1 day

---

### 7.2 Batch Operations
**File**: `korg_pcg_tools/pcg_tools/operations.py`

```python
def batch_set_volume(slots, volume):
    """Set volume for multiple slots."""
    for slot in slots:
        slot.volume = volume

def batch_set_transpose(slots, transpose):
    """Set transpose for multiple slots."""
    for slot in slots:
        slot.transpose = transpose

def batch_set_text_size(slots, text_size):
    """Set text size for multiple slots."""
    for slot in slots:
        slot.text_size = text_size
```

**Estimated Time**: 1 day

---

### 7.3 Status Bar
**File**: `korg_pcg_tools/pcg_tools/gui_qt.py`

```python
class StatusBar(QStatusBar):
    """Enhanced status bar with file statistics."""
    
    def update_stats(self, pcg_file):
        """Update statistics display."""
        prog_count = sum(len(bank.programs) for bank in pcg_file.program_banks)
        combi_count = sum(len(bank.combis) for bank in pcg_file.combi_banks)
        setlist_count = len(pcg_file.set_lists) if pcg_file.set_lists else 0
        
        self.showMessage(
            f"Programs: {prog_count} | "
            f"Combis: {combi_count} | "
            f"Setlists: {setlist_count} | "
            f"Model: {pcg_file.header.model.value}"
        )
```

**Estimated Time**: 1 day

---

### 7.4 Dirty Flag & Revert
**File**: `korg_pcg_tools/pcg_tools/gui_qt.py`

```python
class PcgWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_dirty = False
        self.original_data = None
    
    def mark_dirty(self):
        """Mark file as modified."""
        if not self.is_dirty:
            self.is_dirty = True
            self.update_title()
    
    def update_title(self):
        """Update window title with dirty flag."""
        title = self.filename or "Untitled"
        if self.is_dirty:
            title += " *"
        self.setWindowTitle(f"PCG Tools - {title}")
    
    def revert_to_saved(self):
        """Revert all changes."""
        if not self.is_dirty:
            return
        
        reply = QMessageBox.question(
            self,
            "Revert to Saved",
            "Discard all changes and reload from disk?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.load_file(self.filename)
            self.is_dirty = False
            self.update_title()
```

**Estimated Time**: 1 day

---

## Phase 8: Testing & Validation (Week 4-5)

### 8.1 Comprehensive Test Suite
**File**: `korg_pcg_tools/test_advanced_setlist_features.py`

```python
def test_text_size_all_values():
    """Test all 5 text sizes."""
    
def test_transpose_negative_values():
    """Test negative transpose values."""
    
def test_patch_reference_editing():
    """Test changing patch references."""
    
def test_description_512_chars():
    """Test maximum length descriptions."""
    
def test_clear_slot():
    """Test clearing slots."""
    
def test_swap_slots():
    """Test swapping slots."""
    
def test_batch_operations():
    """Test batch volume/transpose changes."""
```

**Estimated Time**: 3 days

---

### 8.2 Hardware Validation
**Testing on Actual Kronos**:

1. Create test PCG with all features
2. Load on Kronos and verify:
   - Text sizes display correctly
   - Transpose works
   - Patch references are correct
   - Descriptions show properly
   - Colors display correctly

**Estimated Time**: 2 days

---

## Phase 9: Documentation (Week 5)

### 9.1 User Documentation
**Files**:
- Update `USAGE.md` with new features
- Update `QUICK_REFERENCE.md`
- Create `ADVANCED_SETLIST_EDITING.md`

**Estimated Time**: 2 days

---

### 9.2 Developer Documentation
**Files**:
- Update `TECHNICAL_REFERENCE.md` with bit field details
- Update `CONTRIBUTING.md` with new modules
- Document OS version differences

**Estimated Time**: 1 day

---

## Implementation Timeline

### Week 1: Foundation
- ✅ Day 1: Bit utilities module
- ✅ Day 2-3: OS version detection
- ✅ Day 4: Text size reading
- ✅ Day 5: Text size writing & GUI

### Week 2: Core Features
- ✅ Day 1: Enhanced transpose
- ✅ Day 2-3: Patch reference model
- ✅ Day 4-5: Patch reference GUI

### Week 3: Editing Features
- ✅ Day 1: Description persistence
- ✅ Day 2: Description GUI
- ✅ Day 3: Clear slot operation
- ✅ Day 4: Clear slot GUI
- ✅ Day 5: Buffer/catch-up

### Week 4: Advanced Features
- ✅ Day 1: Swap slots
- ✅ Day 2: Batch operations
- ✅ Day 3: Status bar
- ✅ Day 4: Dirty flag & revert
- ✅ Day 5: Integration testing

### Week 5: Testing & Documentation
- ✅ Day 1-3: Comprehensive testing
- ✅ Day 4-5: Hardware validation
- ✅ Day 6-7: Documentation

**Total Estimated Time**: 5 weeks (25 working days)

---

## Success Criteria

### Must Have ✅
1. Text size editing (all 5 sizes)
2. Patch reference editing (type, bank, index)
3. Description persistence (512 chars)
4. Clear slot operation
5. All features work on actual Kronos hardware

### Should Have ⭐
1. Swap slots operation
2. Batch operations (volume, transpose, text size)
3. Status bar with statistics
4. Dirty flag tracking
5. Revert to saved

### Nice to Have 💡
1. OS version auto-detection
2. Enhanced error handling
3. Undo/redo for operations
4. Keyboard shortcuts for new features

---

## Risk Mitigation

### Risk 1: Bit Field Complexity
**Mitigation**: 
- Create comprehensive unit tests first
- Validate against C# code output
- Test with known good files

### Risk 2: OS Version Differences
**Mitigation**:
- Get test files from all OS versions
- Implement version detection early
- Add fallback handling

### Risk 3: Hardware Validation
**Mitigation**:
- Test frequently on actual Kronos
- Keep backup of original files
- Document any discrepancies

### Risk 4: Description Persistence
**Mitigation**:
- Verify with hex editor
- Compare with original C# output
- Test with various lengths

---

## Dependencies

### External
- None (pure Python implementation)

### Internal
- Existing models.py structure
- Current GUI framework (Qt)
- Writer module for persistence

### Test Files Needed
1. OS 1.0/1.1 PCG file
2. OS 1.5/1.6 PCG file
3. OS 2.x PCG file
4. OS 3.x PCG file
5. PCG with all text sizes
6. PCG with long descriptions
7. PCG with EXi banks

---

## Post-Implementation

### Version 3.0 Release
- All Phase 1-7 features complete
- Comprehensive testing passed
- Hardware validation complete
- Documentation updated

### Future Enhancements (v3.1+)
- Master file support
- Dependency tracking in copy/paste
- Parameter editing system
- Support for additional Korg models

---

## Notes

1. **Incremental Development**: Each phase builds on previous phases
2. **Test-Driven**: Write tests before implementation
3. **Hardware Validation**: Test on Kronos frequently
4. **Documentation**: Update docs as features are added
5. **Backward Compatibility**: Ensure existing functionality still works

---

**Plan Status**: Ready for Implementation  
**Next Step**: Begin Phase 1 - Bit Utilities Module  
**Target Completion**: 5 weeks from start date
