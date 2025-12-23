# C# File Analysis Tracker

This document tracks the analysis status of all 895 C# files in the original PCG Tools codebase (`pcg-tools-csharp/`).

**Total Files**: 895  
**Analyzed**: 90  
**Remaining**: 805

## Analysis Summary
- ✅ Fully implemented: 19
- 🔄 Partially implemented: 11
- ❌ Not applicable (WPF/interfaces/auto-generated): 60

## Status Legend
- ⏳ = Not yet analyzed
- ✅ = Analyzed and implemented in Python
- 🔄 = Partially analyzed/implemented  
- ❌ = Not applicable (auto-generated, WPF-specific, etc.)
- 🚫 = Intentionally skipped (out of scope)

## Analysis Process
For each file:
1. Read the C# source code
2. Understand what functionality it provides
3. Search Python codebase for equivalent implementation
4. Verify the Python implementation matches C# behavior
5. Update status and notes

---

## Complete File List (895 files)

| # | File Path | Status | Python Equivalent | Notes |
|---|-----------|--------|-------------------|-------|
| 1 | pcg-tools-csharp/Common/Behaviors/IListItemConverter.cs | ❌ | N/A | WPF list binding interface - not needed in Qt |
| 2 | pcg-tools-csharp/Common/Behaviors/MultiSelectorBehaviors.cs | ❌ | N/A | WPF multi-selection binding - Qt handles natively |
| 3 | pcg-tools-csharp/Common/Behaviors/TwoListSynchronizer.cs | ❌ | N/A | WPF list sync - Qt signals/slots handle this |
| 4 | pcg-tools-csharp/Common/BoolExtensions.cs | ❌ | N/A | ToYesNo() for localization - Python uses native bool |
| 5 | pcg-tools-csharp/Common/Controls/ListBoxExtended.cs | ❌ | N/A | WPF ListBox auto-scroll - Qt handles natively |
| 6 | pcg-tools-csharp/Common/Controls/ListViewExtended.cs | ❌ | N/A | WPF ListView auto-scroll - Qt handles natively |
| 7 | pcg-tools-csharp/Common/Extensions/CheckBoxExtensions.cs | ❌ | N/A | WPF CheckBox helper - Qt handles natively |
| 8 | pcg-tools-csharp/Common/Extensions/RadioButtonExtensions.cs | ❌ | N/A | WPF RadioButton helper - Qt handles natively |
| 9 | pcg-tools-csharp/Common/Extensions/StringExtensions.cs | ❌ | N/A | String utils (ConvertToXml, CountDiffs, etc.) - Python has native equivalents |
| 10 | pcg-tools-csharp/Common/Mvvm/IObservableObject.cs | ❌ | N/A | WPF MVVM interface - Qt uses signals/slots |
| 11 | pcg-tools-csharp/Common/Mvvm/ObservableCollectionEx.cs | ❌ | N/A | WPF observable collection - Qt uses models |
| 12 | pcg-tools-csharp/Common/Mvvm/ObservableObject.cs | ❌ | N/A | WPF MVVM base class - Qt uses signals/slots |
| 13 | pcg-tools-csharp/Common/Mvvm/RelayCommand.cs | ❌ | N/A | WPF command pattern - Qt uses signals/slots |
| 14 | pcg-tools-csharp/Common/Mvvm/ViewModel/CommandViewModel.cs | ❌ | N/A | WPF MVVM command VM - Qt uses signals/slots |
| 15 | pcg-tools-csharp/Common/Mvvm/ViewModel/ViewModelBase.cs | ❌ | N/A | WPF MVVM base VM - Qt uses signals/slots |
| 16 | pcg-tools-csharp/Common/Mvvm/ViewModel/WorkspaceViewModel.cs | ❌ | N/A | WPF workspace VM - Qt uses signals/slots |
| 17 | pcg-tools-csharp/Common/Properties/AssemblyInfo.cs | ❌ | N/A | .NET assembly metadata - not applicable |
| 18 | pcg-tools-csharp/Common/Utils/BitsUtil.cs | ✅ | pcg_tools/bit_utils.py | Bit manipulation - VERIFIED: get_bits, set_bits, to_signed_bit implemented |
| 19 | pcg-tools-csharp/Common/Utils/FileUtils.cs | ❌ | N/A | FileAgeComparer only - Python uses os.path.getctime |
| 20 | pcg-tools-csharp/Common/Utils/MathUtils.cs | ❌ | N/A | ClipValue, MapValue - Python uses min/max, numpy |
| 21 | pcg-tools-csharp/Common/Utils/ResharperCodeAnnotations.cs | ❌ | N/A | IDE annotations - not applicable |
| 22 | pcg-tools-csharp/Common/Utils/WindowUtils.cs | ❌ | N/A | WPF MessageBox/Cursor - Qt has QMessageBox |
| 23 | pcg-tools-csharp/ExternalUtilities/App.xaml.cs | ❌ | N/A | Separate dev utility app - not part of PCG Tools |
| 24 | pcg-tools-csharp/ExternalUtilities/LanguageCrossReferenceWindow.xaml-Michel_PC.cs | ❌ | N/A | Dev backup file - translation utility |
| 25 | pcg-tools-csharp/ExternalUtilities/LanguageCrossReferenceWindow.xaml.cs | ❌ | N/A | Translation cross-reference utility |
| 26 | pcg-tools-csharp/ExternalUtilities/MainWindow.xaml.cs | ❌ | N/A | Separate dev utility app |
| 27 | pcg-tools-csharp/ExternalUtilities/NumberOfCodeLinesWindow.xaml.cs | ❌ | N/A | Code line counter utility |
| 28 | pcg-tools-csharp/ExternalUtilities/Properties/AssemblyInfo.cs | ❌ | N/A | .NET assembly metadata |
| 29 | pcg-tools-csharp/ExternalUtilities/Properties/Resources.Designer.cs | ❌ | N/A | Auto-generated resources |
| 30 | pcg-tools-csharp/ExternalUtilities/Properties/Settings.Designer.cs | ❌ | N/A | Auto-generated settings |
| 31 | pcg-tools-csharp/KorgKronosTools/App.xaml.cs | ❌ | N/A | WPF application entry point - Qt has QApplication |
| 32 | pcg-tools-csharp/KorgKronosTools/ClipBoard/ClipBoardCombi.cs | 🔄 | pcg_tools/clipboard.py | PARTIAL: Basic combi copy exists. MISSING: KronosOs1516Content (CBK2 chunk), References tracking per timbre |
| 33 | pcg-tools-csharp/KorgKronosTools/ClipBoard/ClipBoardDrumKit.cs | 🔄 | pcg_tools/clipboard.py | PARTIAL: Basic drum kit copy exists. MISSING: KronosOs1516Bank/Patch for OS 1.5/1.6 |
| 34 | pcg-tools-csharp/KorgKronosTools/ClipBoard/ClipBoardDrumPattern.cs | 🔄 | pcg_tools/clipboard.py | PARTIAL: DrumPattern model exists but clipboard support incomplete. MISSING: KronosOs1516Bank/Patch |
| 35 | pcg-tools-csharp/KorgKronosTools/ClipBoard/ClipBoardPatch.cs | ✅ | pcg_tools/clipboard.py | Base clipboard functionality with raw_data, deepcopy implemented |
| 36 | pcg-tools-csharp/KorgKronosTools/ClipBoard/ClipBoardPatches.cs | 🔄 | pcg_tools/clipboard.py | PARTIAL: Uses Python lists. MISSING: CountUncopied property, ObservableCollection behavior |
| 37 | pcg-tools-csharp/KorgKronosTools/ClipBoard/ClipBoardProgram.cs | 🔄 | pcg_tools/clipboard.py | PARTIAL: Basic program copy exists. MISSING: KronosOs1516Content (PRG2), ReferencedDrumKits, ReferencedWaveSequences |
| 38 | pcg-tools-csharp/KorgKronosTools/ClipBoard/ClipBoardSetListSlot.cs | 🔄 | pcg_tools/clipboard.py | PARTIAL: Basic slot copy exists. MISSING: KronosOs1516Bank/Patch, Reference to program/combi |
| 39 | pcg-tools-csharp/KorgKronosTools/ClipBoard/ClipBoardWaveSequence.cs | 🔄 | pcg_tools/clipboard.py | PARTIAL: Basic wave sequence copy exists. MISSING: KronosOs1516Bank/Patch |
| 40 | pcg-tools-csharp/KorgKronosTools/ClipBoard/CopyPaste.cs | ❌ | N/A | PatchDuplication enum - not yet implemented in Python |
| 41 | pcg-tools-csharp/KorgKronosTools/ClipBoard/IClipBoardCombi.cs | ❌ | N/A | C# interface - Python uses duck typing |
| 42 | pcg-tools-csharp/KorgKronosTools/ClipBoard/IClipBoardDrumKit.cs | ❌ | N/A | C# interface - Python uses duck typing |
| 43 | pcg-tools-csharp/KorgKronosTools/ClipBoard/IClipBoardDrumPattern.cs | ❌ | N/A | C# interface - Python uses duck typing |
| 44 | pcg-tools-csharp/KorgKronosTools/ClipBoard/IClipBoardPatch.cs | ❌ | N/A | C# interface - Python uses duck typing |
| 45 | pcg-tools-csharp/KorgKronosTools/ClipBoard/IClipBoardPatches.cs | ❌ | N/A | C# interface - Python uses duck typing |
| 46 | pcg-tools-csharp/KorgKronosTools/ClipBoard/IClipBoardProgram.cs | ❌ | N/A | C# interface - Python uses duck typing |
| 47 | pcg-tools-csharp/KorgKronosTools/ClipBoard/IClipBoardSetListSlot.cs | ❌ | N/A | C# interface - Python uses duck typing |
| 48 | pcg-tools-csharp/KorgKronosTools/ClipBoard/IPcgClipBoard.cs | ❌ | N/A | C# interface - Python uses duck typing |
| 49 | pcg-tools-csharp/KorgKronosTools/ClipBoard/PcgClipBoard.cs | 🔄 | pcg_tools/clipboard.py | PARTIAL: Basic clipboard manager exists. MISSING: SynthesisType-based program lists, CutPasteSelected mode, ProtectedPatches, FixReferences* methods, PasteDuplicatesExecuted |
| 50 | pcg-tools-csharp/KorgKronosTools/CombiWindow.xaml.cs | ❌ | N/A | WPF MDI child window for combi editing - Qt uses QMdiSubWindow |
| 51 | pcg-tools-csharp/KorgKronosTools/CommandLineArguments.cs | ✅ | pcg_tools/cli.py | CLI argument parsing - Python uses click framework with similar options |
| 52 | pcg-tools-csharp/KorgKronosTools/CommandLineInterfaceWindow.xaml.cs | ❌ | N/A | WPF CLI output window - Python CLI outputs to terminal |
| 53 | pcg-tools-csharp/KorgKronosTools/Common/BoolExtensions.cs | ❌ | N/A | ToYesNo() for localization - Python uses native bool/str |
| 54 | pcg-tools-csharp/KorgKronosTools/Common/EnumExtensions.cs | ❌ | N/A | GetName/GetDescription for enums - Python uses Enum class natively |
| 55 | pcg-tools-csharp/KorgKronosTools/Edit/EditUtils.cs | ✅ | pcg_tools/qt_edit_dialog.py | CheckText validation with regex - implemented in Python edit dialogs |
| 56 | pcg-tools-csharp/KorgKronosTools/Edit/WindowEditMultipleCombiBanks.xaml.cs | 🔄 | pcg_tools/qt_multi_edit_dialog.py | PARTIAL: Multi-edit exists but may not cover all bank-level operations |
| 57 | pcg-tools-csharp/KorgKronosTools/Edit/WindowEditMultipleCombis.xaml.cs | ✅ | pcg_tools/qt_multi_edit_dialog.py | Multi-combi editing implemented |
| 58 | pcg-tools-csharp/KorgKronosTools/Edit/WindowEditMultipleSetListSlots.xaml.cs | ✅ | pcg_tools/qt_multi_edit_dialog.py | Multi-slot editing implemented |
| 59 | pcg-tools-csharp/KorgKronosTools/Edit/WindowEditParameter.xaml.cs | ❌ | N/A | Generic parameter editor - Python uses specific dialogs |
| 60 | pcg-tools-csharp/KorgKronosTools/Edit/WindowEditParameterOld.xaml.cs | ❌ | N/A | Legacy parameter editor - not needed |
| 61 | pcg-tools-csharp/KorgKronosTools/Edit/WindowEditSingleCombi.xaml.cs | ✅ | pcg_tools/qt_edit_dialog.py | Single combi edit dialog - name, category, favorite |
| 62 | pcg-tools-csharp/KorgKronosTools/Edit/WindowEditSingleProgram.xaml.cs | ✅ | pcg_tools/qt_edit_dialog.py | Single program edit dialog - name, category, favorite |
| 63 | pcg-tools-csharp/KorgKronosTools/Edit/WindowEditSingleSetList.xaml.cs | ✅ | pcg_tools/qt_edit_dialog.py | Single setlist edit dialog |
| 64 | pcg-tools-csharp/KorgKronosTools/Edit/WindowEditSingleSetListSlot.xaml.cs | ✅ | pcg_tools/qt_edit_dialog.py | Single slot edit - name, description, volume, color, transpose, text size |
| 65 | pcg-tools-csharp/KorgKronosTools/Gui/ChangeVolumeWindow.xaml.cs | ✅ | pcg_tools/qt_volume_change_dialog.py | Volume change dialog implemented |
| 66 | pcg-tools-csharp/KorgKronosTools/Gui/Logo.cs | ❌ | N/A | Logo display class - not needed in Python |
| 67 | pcg-tools-csharp/KorgKronosTools/Gui/Logos.cs | ❌ | N/A | Logo collection - not needed in Python |
| 68 | pcg-tools-csharp/KorgKronosTools/Gui/SelectSortWindow.xaml.cs | ✅ | pcg_tools/patch_sorting.py | Patch sorting dialog implemented |
| 69 | pcg-tools-csharp/KorgKronosTools/Help/AboutWindow.xaml.cs | ✅ | pcg_tools/gui_qt.py | About dialog in show_about() method |
| 70 | pcg-tools-csharp/KorgKronosTools/Help/ExternalItem.cs | ❌ | N/A | External link item class - not needed |
| 71 | pcg-tools-csharp/KorgKronosTools/Help/ExternalLinksContributorsWindow.xaml.cs | ❌ | N/A | Contributors window - not implemented |
| 72 | pcg-tools-csharp/KorgKronosTools/Help/ExternalLinksDonatorsWindow.xaml.cs | ❌ | N/A | Donators window - not implemented |
| 73 | pcg-tools-csharp/KorgKronosTools/Help/ExternalLinksKorgRelatedWindow.xaml.cs | ❌ | N/A | Korg links window - not implemented |
| 74 | pcg-tools-csharp/KorgKronosTools/Help/ExternalLinksOasysVoucherCodeSponsorsWindow.xaml.cs | ❌ | N/A | Sponsors window - not implemented |
| 75 | pcg-tools-csharp/KorgKronosTools/Help/ExternalLinksPersonalWindow.xaml.cs | ❌ | N/A | Personal links window - not implemented |
| 76 | pcg-tools-csharp/KorgKronosTools/Help/ExternalLinksThirdPartiesWindow.xaml.cs | ❌ | N/A | Third party links window - not implemented |
| 77 | pcg-tools-csharp/KorgKronosTools/Help/ExternalLinksTranslatorsWindow.xaml.cs | ❌ | N/A | Translators window - not implemented |
| 78 | pcg-tools-csharp/KorgKronosTools/Help/ExternalLinksVideoCreatorsWindow.xaml.cs | ❌ | N/A | Video creators window - not implemented |
| 79 | pcg-tools-csharp/KorgKronosTools/Help/UserControlExternalLink.xaml.cs | ❌ | N/A | External link user control - not needed |
| 80 | pcg-tools-csharp/KorgKronosTools/HexExportDlg.xaml.cs | ❌ | N/A | Hex export dialog - not implemented |
| 81 | pcg-tools-csharp/KorgKronosTools/IChildWindow.cs | ❌ | N/A | C# interface - Python uses duck typing |
| 82 | pcg-tools-csharp/KorgKronosTools/ListGenerator/IListGenerator.cs | ❌ | N/A | C# interface - Python uses duck typing |
| 83 | pcg-tools-csharp/KorgKronosTools/ListGenerator/ListGenerator.cs | ✅ | pcg_tools/list_generators.py | Base list generator class implemented |
| 84 | pcg-tools-csharp/KorgKronosTools/ListGenerator/ListGeneratorCombiContentList.cs | ✅ | pcg_tools/list_generators.py | Combi content list generator |
| 85 | pcg-tools-csharp/KorgKronosTools/ListGenerator/ListGeneratorDifferencesList-michelLaptop.cs | ❌ | N/A | Backup file - not needed |
| 86 | pcg-tools-csharp/KorgKronosTools/ListGenerator/ListGeneratorDifferencesList.cs | 🔄 | pcg_tools/list_generators.py | PARTIAL: Differences list may not be fully implemented |
| 87 | pcg-tools-csharp/KorgKronosTools/ListGenerator/ListGeneratorFileContentList.cs | ✅ | pcg_tools/list_generators.py | File content list generator |
| 88 | pcg-tools-csharp/KorgKronosTools/ListGenerator/ListGeneratorPatchList.cs | ✅ | pcg_tools/list_generators.py | Patch list generator |
| 89 | pcg-tools-csharp/KorgKronosTools/ListGenerator/ListGeneratorProgramUsageList.cs | ✅ | pcg_tools/list_generators.py | Program usage list generator |
| 90 | pcg-tools-csharp/KorgKronosTools/ListGenerator/ListGeneratorWindow.xaml.cs | ✅ | pcg_tools/gui_qt.py | List generator accessed via Tools menu |
| 91 | pcg-tools-csharp/KorgKronosTools/MainWindow.xaml.cs | ✅ | pcg_tools/gui_qt.py | Main window - PcgToolsMainWindow class |
| 92 | pcg-tools-csharp/KorgKronosTools/MasterFiles/IMasterFile.cs | ❌ | N/A | C# interface - Python uses duck typing |
| 93 | pcg-tools-csharp/KorgKronosTools/MasterFiles/MasterFile.cs | ✅ | pcg_tools/master_files.py | MasterFile class with model/filename/state |
| 94 | pcg-tools-csharp/KorgKronosTools/MasterFiles/MasterFiles.cs | ✅ | pcg_tools/master_files.py | MasterFiles collection with FindMasterPcg |
| 95 | pcg-tools-csharp/KorgKronosTools/MasterFiles/MasterFilesWindow.xaml.cs | ✅ | pcg_tools/qt_master_files_dialog.py | Master files dialog |
| 96 | pcg-tools-csharp/KorgKronosTools/Model/Common/File/FileReader.cs | ✅ | pcg_tools/pcg_parser.py | Base file reader functionality |
| 97 | pcg-tools-csharp/KorgKronosTools/Model/Common/File/IPatchesFileReader.cs | ❌ | N/A | C# interface - Python uses duck typing |
| 98 | pcg-tools-csharp/KorgKronosTools/Model/Common/File/ISongFileReader.cs | ❌ | N/A | C# interface - Python uses duck typing |
| 99 | pcg-tools-csharp/KorgKronosTools/Model/Common/File/KorgFileReader.cs | ✅ | pcg_tools/pcg_parser.py | Korg file header parsing |
| 100 | pcg-tools-csharp/KorgKronosTools/Model/Common/File/MkxlAllFileReader.cs | ❌ | N/A | MicroKorg XL file reader - not implemented |
| 101 | pcg-tools-csharp/KorgKronosTools/Model/Common/File/MkxlFileReader.cs | ❌ | N/A | MicroKorg XL file reader - not implemented |
| 102 | pcg-tools-csharp/KorgKronosTools/Model/Common/File/MkxlpFileReader.cs | ❌ | N/A | MicroKorg XL+ file reader - not implemented |
| 103 | pcg-tools-csharp/KorgKronosTools/Model/Common/File/PatchesFileReader.cs | ✅ | pcg_tools/pcg_parser.py | Patches file reader base |
| 104 | pcg-tools-csharp/KorgKronosTools/Model/Common/File/PcgFileReader.cs | ✅ | pcg_tools/pcg_parser.py | PCG file reader - chunk parsing, bank ID decoding |
| 105 | pcg-tools-csharp/KorgKronosTools/Model/Common/File/SongFileReader.cs | ✅ | pcg_tools/sng_parser.py | SNG file reader |
| 106 | pcg-tools-csharp/KorgKronosTools/Model/Common/File/SysExFileReader.cs | ❌ | N/A | SysEx file reader - not implemented |
| 107 | pcg-tools-csharp/KorgKronosTools/Model/Common/File/TrFileReader.cs | ❌ | N/A | TR file reader - not implemented |
| 108 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/DrumTrack/IDrumTrackReference.cs | ❌ | N/A | C# interface - Python uses duck typing |
| 109 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/Global/Global.cs | 🔄 | pcg_tools/models.py | PARTIAL: Global chunk parsing exists but category names may be incomplete |
| 110 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/Global/IGlobal.cs | ❌ | N/A | C# interface - Python uses duck typing |
| 111 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/Chunk.cs | ✅ | pcg_tools/pcg_parser.py | Chunk class with type, offset, size |
| 112 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/Chunks.cs | ✅ | pcg_tools/pcg_parser.py | Chunks collection |
| 113 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/Client.cs | ❌ | N/A | WPF client class - not needed |
| 114 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/Factory.cs | 🔄 | pcg_tools/pcg_parser.py | PARTIAL: Factory pattern for synth models - Python uses simpler approach |
| 115 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/IChunk.cs | ❌ | N/A | C# interface |
| 116 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/IChunks.cs | ❌ | N/A | C# interface |
| 117 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/IFactory.cs | ❌ | N/A | C# interface |
| 118 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/IMemory.cs | ❌ | N/A | C# interface |
| 119 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/IMemoryInit.cs | ❌ | N/A | C# interface |
| 120 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/IModel.cs | ❌ | N/A | C# interface |
| 121 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/IPcgMemory.cs | ❌ | N/A | C# interface |
| 122 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/IPcgMemoryInit.cs | ❌ | N/A | C# interface |
| 123 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/ISysExMemory.cs | ❌ | N/A | C# interface |
| 124 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/Memory.cs | ✅ | pcg_tools/models.py | Memory base class - PcgFile |
| 125 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/MkxlAllMemory.cs | ❌ | N/A | MicroKorg XL memory - not implemented |
| 126 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/Model.cs | ✅ | pcg_tools/models.py | Model class with synth type detection |
| 127 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/Models.cs | ✅ | pcg_tools/models.py | Models collection with EOsVersion enum |
| 128 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/PcgMemory.cs | ✅ | pcg_tools/models.py | PcgMemory with checksum, INI2/INI3 handling |
| 129 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/SysExFactory.cs | ❌ | N/A | SysEx factory - not implemented |
| 130 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/MemoryAndFactory/SysExMemory.cs | ❌ | N/A | SysEx memory - not implemented |
| 131 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/Meta/Bank.cs | ✅ | pcg_tools/models.py | Bank class with bank_id, patches |
| 132 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/Meta/BankType.cs | ✅ | pcg_tools/models.py | BankType enum (User, Internal, GM, etc.) |
| 133 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/Meta/Banks.cs | ✅ | pcg_tools/models.py | Banks collection |
| 134 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/Meta/IBank.cs | ❌ | N/A | C# interface |
| 135 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/Meta/IBanks.cs | ❌ | N/A | C# interface |
| 136 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/Meta/IObservableBankCollection.cs | ❌ | N/A | C# interface |
| 137 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/Meta/IPatch.cs | ❌ | N/A | C# interface |
| 138 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/Meta/ObservableBankCollection.cs | ❌ | N/A | WPF observable collection |
| 139 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/Meta/ObservablePatchCollection.cs | ❌ | N/A | WPF observable collection |
| 140 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/Meta/Patch.cs | ✅ | pcg_tools/models.py | Patch base class with name, raw_data |
| 141 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/NewParameters/IIntParameter.cs | ❌ | N/A | C# interface |
| 142 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/NewParameters/IntParameterBitsInByte.cs | ✅ | pcg_tools/bit_utils.py | Bit manipulation for parameters |
| 143 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/OldParameters/BoolParameter.cs | ✅ | pcg_tools/models.py | Boolean parameter handling |
| 144 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/OldParameters/EnumParameter.cs | ✅ | pcg_tools/models.py | Enum parameter handling |
| 145 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/OldParameters/FixedParameter.cs | ✅ | pcg_tools/models.py | Fixed parameter handling |
| 146 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/OldParameters/IFixedParameter.cs | ❌ | N/A | C# interface |
| 147 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/OldParameters/IFixedParameterValue.cs | ❌ | N/A | C# interface |
| 148 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/OldParameters/IParameter.cs | ❌ | N/A | C# interface |
| 149 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/OldParameters/IntParameter.cs | ✅ | pcg_tools/models.py | Integer parameter handling |
| 150 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/OldParameters/Parameter.cs | ✅ | pcg_tools/models.py | Base parameter class |
| 151 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/OldParameters/ParameterNames.cs | ✅ | pcg_tools/models.py | Parameter name constants |
| 152 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/OldParameters/ParameterValues.cs | ✅ | pcg_tools/models.py | Parameter value constants |
| 153 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/OldParameters/WordParameter.cs | ✅ | pcg_tools/models.py | Word (16-bit) parameter handling |
| 154 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/OldParameters/_BackupParameters.cs | ❌ | N/A | Backup file - not needed |
| 155 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchCombis/Combi.cs | ✅ | pcg_tools/models.py | Combi class with timbres |
| 156 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchCombis/CombiBank.cs | ✅ | pcg_tools/models.py | CombiBank class |
| 157 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchCombis/CombiBanks.cs | ✅ | pcg_tools/models.py | CombiBanks collection |
| 158 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchCombis/ICombi.cs | ❌ | N/A | C# interface |
| 159 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchCombis/ICombiBank.cs | ❌ | N/A | C# interface |
| 160 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchCombis/ICombiBanks.cs | ❌ | N/A | C# interface |
| 161 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchCombis/ITimbre.cs | ❌ | N/A | C# interface |
| 162 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchCombis/ITimbres.cs | ❌ | N/A | C# interface |
| 163 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchCombis/Timbre.cs | ✅ | pcg_tools/models.py | Timbre class with program reference |
| 164 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchCombis/TimbreComparer.cs | 🔄 | pcg_tools/patch_sorting.py | PARTIAL: Timbre comparison for sorting |
| 165 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchCombis/TimbreSorting.cs | 🔄 | pcg_tools/patch_sorting.py | PARTIAL: Timbre sorting logic |
| 166 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchCombis/Timbres.cs | ✅ | pcg_tools/models.py | Timbres collection |
| 167 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchDrumKits/DrumKit.cs | ✅ | pcg_tools/models.py | DrumKit class |
| 168 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchDrumKits/DrumKitBank.cs | ✅ | pcg_tools/models.py | DrumKitBank class |
| 169 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchDrumKits/DrumKitBanks.cs | ✅ | pcg_tools/models.py | DrumKitBanks collection |
| 170 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchDrumKits/IDrumKit.cs | ❌ | N/A | C# interface |
| 171 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchDrumKits/IDrumKitBank.cs | ❌ | N/A | C# interface |
| 172 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchDrumKits/IDrumKitBanks.cs | ❌ | N/A | C# interface |
| 173 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchDrumPatterns/DrumPattern.cs | ✅ | pcg_tools/models.py | DrumPattern class |
| 174 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchDrumPatterns/DrumPatternBank.cs | ✅ | pcg_tools/models.py | DrumPatternBank class |
| 175 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchDrumPatterns/DrumPatternBanks.cs | ✅ | pcg_tools/models.py | DrumPatternBanks collection |
| 176 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchDrumPatterns/IDrumPattern.cs | ❌ | N/A | C# interface |
| 177 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchDrumPatterns/IDrumPatternBank.cs | ❌ | N/A | C# interface |
| 178 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchDrumPatterns/IDrumPatternBanks.cs | ❌ | N/A | C# interface |
| 179 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/IArtistable.cs | ❌ | N/A | C# interface |
| 180 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/ICategoriesNamable.cs | ❌ | N/A | C# interface |
| 181 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/IClearable.cs | ❌ | N/A | C# interface |
| 182 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/ICompleteInPcgable.cs | ❌ | N/A | C# interface |
| 183 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/ICountable.cs | ❌ | N/A | C# interface |
| 184 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/IDirtiable.cs | ❌ | N/A | C# interface |
| 185 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/IFillable.cs | ❌ | N/A | C# interface |
| 186 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/IIndexable.cs | ❌ | N/A | C# interface |
| 187 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/IIsEmptyCheckable.cs | ❌ | N/A | C# interface |
| 188 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/ILoadable.cs | ❌ | N/A | C# interface |
| 189 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/ILocatable.cs | ❌ | N/A | C# interface |
| 190 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/INamable.cs | ❌ | N/A | C# interface |
| 191 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/INavigable.cs | ❌ | N/A | C# interface |
| 192 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/INotificatable.cs | ❌ | N/A | C# interface |
| 193 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/IParameterSettable.cs | ❌ | N/A | C# interface |
| 194 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/IPcgNavigable.cs | ❌ | N/A | C# interface |
| 195 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/IReferencable.cs | ❌ | N/A | C# interface |
| 196 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/ISelectable.cs | ❌ | N/A | C# interface |
| 197 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/ISupportedFeatures.cs | ❌ | N/A | C# interface |
| 198 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/IUpdatable.cs | ❌ | N/A | C# interface |
| 199 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchInterfaces/IWritable.cs | ❌ | N/A | C# interface |
| 200 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchPrograms/GmPrograms.cs | ✅ | pcg_tools/gm2_data.py | GM program names |
| 201 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchPrograms/IProgram.cs | ❌ | N/A | C# interface |
| 202 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchPrograms/IProgramBank.cs | ❌ | N/A | C# interface |
| 203 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchPrograms/IProgramBanks.cs | ❌ | N/A | C# interface |
| 204 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchPrograms/Program.cs | ✅ | pcg_tools/models.py | Program class with engine, category |
| 205 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchPrograms/ProgramBank.cs | ✅ | pcg_tools/models.py | ProgramBank class |
| 206 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchPrograms/ProgramBanks.cs | ✅ | pcg_tools/models.py | ProgramBanks collection |
| 207 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchSetLists/ISetList.cs | ❌ | N/A | C# interface |
| 208 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchSetLists/ISetListSlot.cs | ❌ | N/A | C# interface |
| 209 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchSetLists/ISetLists.cs | ❌ | N/A | C# interface |
| 210 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchSetLists/SetList.cs | ✅ | pcg_tools/models.py | SetList class |
| 211 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchSetLists/SetListSlot.cs | ✅ | pcg_tools/models.py | SetListSlot with name, description, volume, color, transpose |
| 212 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchSetLists/SetLists.cs | ✅ | pcg_tools/models.py | SetLists collection |
| 213 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchSorting/ArtistComparer.cs | 🔄 | pcg_tools/patch_sorting.py | PARTIAL: Artist comparison |
| 214 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchSorting/CategoricalComparer.cs | ✅ | pcg_tools/patch_sorting.py | Category-based sorting |
| 215 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchSorting/CompositeComparer.cs | ✅ | pcg_tools/patch_sorting.py | Composite sorting |
| 216 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchSorting/EmptyOrInitComparer.cs | ✅ | pcg_tools/patch_sorting.py | Empty/Init patch sorting |
| 217 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchSorting/NameComparer.cs | ✅ | pcg_tools/patch_sorting.py | Name-based sorting |
| 218 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchSorting/PatchSorter.cs | ✅ | pcg_tools/patch_sorting.py | Main patch sorter |
| 219 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchSorting/TitleComparer.cs | 🔄 | pcg_tools/patch_sorting.py | PARTIAL: Title comparison |
| 220 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchWaveSequences/IWaveSequence.cs | ❌ | N/A | C# interface |
| 221 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchWaveSequences/IWaveSequenceBank.cs | ⏳ | | |
| 222 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchWaveSequences/IWaveSequenceBanks.cs | ⏳ | | |
| 223 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchWaveSequences/WaveSequence.cs | ⏳ | | |
| 224 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchWaveSequences/WaveSequenceBank.cs | ⏳ | | |
| 225 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/PatchWaveSequences/WaveSequenceBanks.cs | ⏳ | | |
| 226 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/SongsRelated/IRegion.cs | ⏳ | | |
| 227 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/SongsRelated/IRegions.cs | ⏳ | | |
| 228 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/SongsRelated/ISong.cs | ⏳ | | |
| 229 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/SongsRelated/ISongMemory.cs | ⏳ | | |
| 230 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/SongsRelated/ISongMemoryInit.cs | ⏳ | | |
| 231 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/SongsRelated/ISongTimbre.cs | ⏳ | | |
| 232 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/SongsRelated/ISongTimbres.cs | ⏳ | | |
| 233 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/SongsRelated/ISongs.cs | ⏳ | | |
| 234 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/SongsRelated/Region.cs | ⏳ | | |
| 235 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/SongsRelated/Regions.cs | ⏳ | | |
| 236 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/SongsRelated/Song.cs | ⏳ | | |
| 237 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/SongsRelated/SongMemory.cs | ⏳ | | |
| 238 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/SongsRelated/SongTimbre.cs | ⏳ | | |
| 239 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/SongsRelated/SongTimbres.cs | ⏳ | | |
| 240 | pcg-tools-csharp/KorgKronosTools/Model/Common/Synth/SongsRelated/Songs.cs | ⏳ | | |
| 241 | pcg-tools-csharp/KorgKronosTools/Model/Common/Util.cs | ⏳ | | |
| 242 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Pcg/KromeExPcgFileReader.cs | ⏳ | | |
| 243 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Pcg/KromeExPcgMemory.cs | ⏳ | | |
| 244 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Song/KromeExSongFileReader.cs | ⏳ | | |
| 245 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Song/KromeExSongMemory.cs | ⏳ | | |
| 246 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Synth/KromeExCombi.cs | ⏳ | | |
| 247 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Synth/KromeExCombiBank.cs | ⏳ | | |
| 248 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Synth/KromeExCombiBanks.cs | ⏳ | | |
| 249 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Synth/KromeExDrumKit.cs | ⏳ | | |
| 250 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Synth/KromeExDrumKitBank.cs | ⏳ | | |
| 251 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Synth/KromeExDrumKitBanks.cs | ⏳ | | |
| 252 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Synth/KromeExDrumPattern.cs | ⏳ | | |
| 253 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Synth/KromeExDrumPatternBank.cs | ⏳ | | |
| 254 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Synth/KromeExDrumPatternBanks.cs | ⏳ | | |
| 255 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Synth/KromeExFactory.cs | ⏳ | | |
| 256 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Synth/KromeExGlobal.cs | ⏳ | | |
| 257 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Synth/KromeExGmProgram.cs | ⏳ | | |
| 258 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Synth/KromeExGmProgramBank.cs | ⏳ | | |
| 259 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Synth/KromeExProgram.cs | ⏳ | | |
| 260 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Synth/KromeExProgramBank.cs | ⏳ | | |
| 261 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Synth/KromeExProgramBanks.cs | ⏳ | | |
| 262 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Synth/KromeExTimbre.cs | ⏳ | | |
| 263 | pcg-tools-csharp/KorgKronosTools/Model/KromeExSpecific/Synth/KromeExTimbres.cs | ⏳ | | |
| 264 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Pcg/KromePcgFileReader.cs | ⏳ | | |
| 265 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Pcg/KromePcgMemory.cs | ⏳ | | |
| 266 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Song/KromeSongFileReader.cs | ⏳ | | |
| 267 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Song/KromeSongMemory.cs | ⏳ | | |
| 268 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Synth/KromeCombi.cs | ⏳ | | |
| 269 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Synth/KromeCombiBank.cs | ⏳ | | |
| 270 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Synth/KromeCombiBanks.cs | ⏳ | | |
| 271 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Synth/KromeDrumKit.cs | ⏳ | | |
| 272 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Synth/KromeDrumKitBank.cs | ⏳ | | |
| 273 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Synth/KromeDrumKitBanks.cs | ⏳ | | |
| 274 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Synth/KromeDrumPattern.cs | ⏳ | | |
| 275 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Synth/KromeDrumPatternBank.cs | ⏳ | | |
| 276 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Synth/KromeDrumPatternBanks.cs | ⏳ | | |
| 277 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Synth/KromeFactory.cs | ⏳ | | |
| 278 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Synth/KromeGlobal.cs | ⏳ | | |
| 279 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Synth/KromeGmProgram.cs | ⏳ | | |
| 280 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Synth/KromeGmProgramBank.cs | ⏳ | | |
| 281 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Synth/KromeProgram.cs | ⏳ | | |
| 282 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Synth/KromeProgramBank.cs | ⏳ | | |
| 283 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Synth/KromeProgramBanks.cs | ⏳ | | |
| 284 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Synth/KromeTimbre.cs | ⏳ | | |
| 285 | pcg-tools-csharp/KorgKronosTools/Model/KromeSpecific/Synth/KromeTimbres.cs | ⏳ | | |
| 286 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Pcg/KronosOasysPcgFileReader.cs | ⏳ | | |
| 287 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Pcg/KronosOasysPcgMemory.cs | ⏳ | | |
| 288 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Song/KronosOasysSongFileReader.cs | ⏳ | | |
| 289 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Song/KronosOasysSongMemory.cs | ⏳ | | |
| 290 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysCombi.cs | ⏳ | | |
| 291 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysCombiBank.cs | ⏳ | | |
| 292 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysCombiBanks.cs | ⏳ | | |
| 293 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysDrumKit.cs | ⏳ | | |
| 294 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysDrumKitBank.cs | ⏳ | | |
| 295 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysDrumKitBanks.cs | ⏳ | | |
| 296 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysDrumPattern.cs | ⏳ | | |
| 297 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysDrumPatternBank.cs | ⏳ | | |
| 298 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysDrumPatternBanks.cs | ⏳ | | |
| 299 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysFactory.cs | ⏳ | | |
| 300 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysGlobal.cs | ⏳ | | |
| 301 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysProgram.cs | ⏳ | | |
| 302 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysProgramBank.cs | ⏳ | | |
| 303 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysProgramBanks.cs | ⏳ | | |
| 304 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysTimbre.cs | ⏳ | | |
| 305 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysTimbres.cs | ⏳ | | |
| 306 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysWaveSequence.cs | ⏳ | | |
| 307 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysWaveSequenceBank.cs | ⏳ | | |
| 308 | pcg-tools-csharp/KorgKronosTools/Model/KronosOasysSpecific/Synth/KronosOasysWaveSequenceBanks.cs | ⏳ | | |
| 309 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Pcg/KronosPcgFileReader.cs | ⏳ | | |
| 310 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Pcg/KronosPcgMemory.cs | ⏳ | | |
| 311 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Song/KronosSongFileReader.cs | ⏳ | | |
| 312 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Song/KronosSongMemory.cs | ⏳ | | |
| 313 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosCombi.cs | ⏳ | | |
| 314 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosCombiBank.cs | ⏳ | | |
| 315 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosCombiBanks.cs | ⏳ | | |
| 316 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosDrumKit.cs | ⏳ | | |
| 317 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosDrumKitBank.cs | ⏳ | | |
| 318 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosDrumKitBanks.cs | ⏳ | | |
| 319 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosDrumPattern.cs | ⏳ | | |
| 320 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosDrumPatternBank.cs | ⏳ | | |
| 321 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosDrumPatternBanks.cs | ⏳ | | |
| 322 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosFactory.cs | ⏳ | | |
| 323 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosGlobal.cs | ⏳ | | |
| 324 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosGmProgram.cs | ⏳ | | |
| 325 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosGmProgramBank.cs | ⏳ | | |
| 326 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosProgram.cs | ⏳ | | |
| 327 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosProgramBank.cs | ⏳ | | |
| 328 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosProgramBanks.cs | ⏳ | | |
| 329 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosSetList.cs | ⏳ | | |
| 330 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosSetListSlot.cs | ⏳ | | |
| 331 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosSetLists.cs | ⏳ | | |
| 332 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosTimbre.cs | ⏳ | | |
| 333 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosTimbres.cs | ⏳ | | |
| 334 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosWaveSequence.cs | ⏳ | | |
| 335 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosWaveSequenceBank.cs | ⏳ | | |
| 336 | pcg-tools-csharp/KorgKronosTools/Model/KronosSpecific/Synth/KronosWaveSequenceBanks.cs | ⏳ | | |
| 337 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Pcg/Kross2PcgFileReader.cs | ⏳ | | |
| 338 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Pcg/Kross2PcgMemory.cs | ⏳ | | |
| 339 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Pcg/Kross2TrFileReader.cs | ⏳ | | |
| 340 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Song/Kross2SongFileReader.cs | ⏳ | | |
| 341 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Song/Kross2SongMemory.cs | ⏳ | | |
| 342 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Synth/Kross2Combi.cs | ⏳ | | |
| 343 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Synth/Kross2CombiBank.cs | ⏳ | | |
| 344 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Synth/Kross2CombiBanks.cs | ⏳ | | |
| 345 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Synth/Kross2DrumKit.cs | ⏳ | | |
| 346 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Synth/Kross2DrumKitBank.cs | ⏳ | | |
| 347 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Synth/Kross2DrumKitBanks.cs | ⏳ | | |
| 348 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Synth/Kross2Factory.cs | ⏳ | | |
| 349 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Synth/Kross2Global.cs | ⏳ | | |
| 350 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Synth/Kross2GmProgram.cs | ⏳ | | |
| 351 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Synth/Kross2GmProgramBank.cs | ⏳ | | |
| 352 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Synth/Kross2Program.cs | ⏳ | | |
| 353 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Synth/Kross2ProgramBank.cs | ⏳ | | |
| 354 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Synth/Kross2ProgramBanks.cs | ⏳ | | |
| 355 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Synth/Kross2Timbre.cs | ⏳ | | |
| 356 | pcg-tools-csharp/KorgKronosTools/Model/Kross2Specific/Synth/Kross2Timbres.cs | ⏳ | | |
| 357 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Pcg/KrossPcgFileReader.cs | ⏳ | | |
| 358 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Pcg/KrossPcgMemory.cs | ⏳ | | |
| 359 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Pcg/KrossTrFileReader.cs | ⏳ | | |
| 360 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Song/KrossSongFileReader.cs | ⏳ | | |
| 361 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Song/KrossSongMemory.cs | ⏳ | | |
| 362 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Synth/KrossCombi.cs | ⏳ | | |
| 363 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Synth/KrossCombiBank.cs | ⏳ | | |
| 364 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Synth/KrossCombiBanks.cs | ⏳ | | |
| 365 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Synth/KrossDrumKit.cs | ⏳ | | |
| 366 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Synth/KrossDrumKitBank.cs | ⏳ | | |
| 367 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Synth/KrossDrumKitBanks.cs | ⏳ | | |
| 368 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Synth/KrossFactory.cs | ⏳ | | |
| 369 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Synth/KrossGlobal.cs | ⏳ | | |
| 370 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Synth/KrossGmProgram.cs | ⏳ | | |
| 371 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Synth/KrossGmProgramBank.cs | ⏳ | | |
| 372 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Synth/KrossProgram.cs | ⏳ | | |
| 373 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Synth/KrossProgramBank.cs | ⏳ | | |
| 374 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Synth/KrossProgramBanks.cs | ⏳ | | |
| 375 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Synth/KrossTimbre.cs | ⏳ | | |
| 376 | pcg-tools-csharp/KorgKronosTools/Model/KrossSpecific/Synth/KrossTimbres.cs | ⏳ | | |
| 377 | pcg-tools-csharp/KorgKronosTools/Model/M1Specific/Pcg/M1FileReader.cs | ⏳ | | |
| 378 | pcg-tools-csharp/KorgKronosTools/Model/M1Specific/Pcg/M1SysExMemory.cs | ⏳ | | |
| 379 | pcg-tools-csharp/KorgKronosTools/Model/M1Specific/Song/M1SongFileReader.cs | ⏳ | | |
| 380 | pcg-tools-csharp/KorgKronosTools/Model/M1Specific/Song/M1SongMemory.cs | ⏳ | | |
| 381 | pcg-tools-csharp/KorgKronosTools/Model/M1Specific/Synth/M1Combi.cs | ⏳ | | |
| 382 | pcg-tools-csharp/KorgKronosTools/Model/M1Specific/Synth/M1CombiBank.cs | ⏳ | | |
| 383 | pcg-tools-csharp/KorgKronosTools/Model/M1Specific/Synth/M1CombiBanks.cs | ⏳ | | |
| 384 | pcg-tools-csharp/KorgKronosTools/Model/M1Specific/Synth/M1Factory.cs | ⏳ | | |
| 385 | pcg-tools-csharp/KorgKronosTools/Model/M1Specific/Synth/M1Global.cs | ⏳ | | |
| 386 | pcg-tools-csharp/KorgKronosTools/Model/M1Specific/Synth/M1Program.cs | ⏳ | | |
| 387 | pcg-tools-csharp/KorgKronosTools/Model/M1Specific/Synth/M1ProgramBank.cs | ⏳ | | |
| 388 | pcg-tools-csharp/KorgKronosTools/Model/M1Specific/Synth/M1ProgramBanks.cs | ⏳ | | |
| 389 | pcg-tools-csharp/KorgKronosTools/Model/M1Specific/Synth/M1Timbre.cs | ⏳ | | |
| 390 | pcg-tools-csharp/KorgKronosTools/Model/M1Specific/Synth/M1Timbres.cs | ⏳ | | |
| 391 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Pcg/M3PcgFileReader.cs | ⏳ | | |
| 392 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Pcg/M3PcgMemory.cs | ⏳ | | |
| 393 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Song/M3SongFileReader.cs | ⏳ | | |
| 394 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Song/M3SongMemory.cs | ⏳ | | |
| 395 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Synth/M3Combi.cs | ⏳ | | |
| 396 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Synth/M3CombiBank.cs | ⏳ | | |
| 397 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Synth/M3CombiBanks.cs | ⏳ | | |
| 398 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Synth/M3DrumKit.cs | ⏳ | | |
| 399 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Synth/M3DrumKitBank.cs | ⏳ | | |
| 400 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Synth/M3DrumKitBanks.cs | ⏳ | | |
| 401 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Synth/M3DrumPattern.cs | ⏳ | | |
| 402 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Synth/M3DrumPatternBank.cs | ⏳ | | |
| 403 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Synth/M3DrumPatternBanks.cs | ⏳ | | |
| 404 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Synth/M3Factory.cs | ⏳ | | |
| 405 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Synth/M3Global.cs | ⏳ | | |
| 406 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Synth/M3GmProgram.cs | ⏳ | | |
| 407 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Synth/M3GmProgramBank.cs | ⏳ | | |
| 408 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Synth/M3Program.cs | ⏳ | | |
| 409 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Synth/M3ProgramBank.cs | ⏳ | | |
| 410 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Synth/M3ProgramBanks.cs | ⏳ | | |
| 411 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Synth/M3Timbre.cs | ⏳ | | |
| 412 | pcg-tools-csharp/KorgKronosTools/Model/M3Specific/Synth/M3Timbres.cs | ⏳ | | |
| 413 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Pcg/M3RSysExMemory-michelLaptop.cs | ⏳ | | |
| 414 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Pcg/M3RSysExMemory.cs | ⏳ | | |
| 415 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Pcg/M3rFileReader.cs | ⏳ | | |
| 416 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Song/M3RSongFileReader-michelLaptop.cs | ⏳ | | |
| 417 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Song/M3RSongFileReader.cs | ⏳ | | |
| 418 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Song/M3rSongMemory.cs | ⏳ | | |
| 419 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Synth/M3RCombi-michelLaptop.cs | ⏳ | | |
| 420 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Synth/M3RCombi.cs | ⏳ | | |
| 421 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Synth/M3RCombiBank-michelLaptop.cs | ⏳ | | |
| 422 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Synth/M3RCombiBank.cs | ⏳ | | |
| 423 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Synth/M3RProgram-michelLaptop.cs | ⏳ | | |
| 424 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Synth/M3RProgram.cs | ⏳ | | |
| 425 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Synth/M3RProgramBank-michelLaptop.cs | ⏳ | | |
| 426 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Synth/M3RProgramBank.cs | ⏳ | | |
| 427 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Synth/M3RProgramBanks-michelLaptop.cs | ⏳ | | |
| 428 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Synth/M3RProgramBanks.cs | ⏳ | | |
| 429 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Synth/M3RTimbre-michelLaptop.cs | ⏳ | | |
| 430 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Synth/M3RTimbre.cs | ⏳ | | |
| 431 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Synth/M3RTimbres-michelLaptop.cs | ⏳ | | |
| 432 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Synth/M3RTimbres.cs | ⏳ | | |
| 433 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Synth/M3rCombiBanks.cs | ⏳ | | |
| 434 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Synth/M3rFactory.cs | ⏳ | | |
| 435 | pcg-tools-csharp/KorgKronosTools/Model/M3rSpecific/Synth/M3rGlobal.cs | ⏳ | | |
| 436 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Pcg/M50PcgFileReader.cs | ⏳ | | |
| 437 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Pcg/M50PcgMemory.cs | ⏳ | | |
| 438 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Song/M50SongFileReader.cs | ⏳ | | |
| 439 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Song/M50SongMemory.cs | ⏳ | | |
| 440 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Synth/M50Combi.cs | ⏳ | | |
| 441 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Synth/M50CombiBank.cs | ⏳ | | |
| 442 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Synth/M50CombiBanks.cs | ⏳ | | |
| 443 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Synth/M50DrumKit.cs | ⏳ | | |
| 444 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Synth/M50DrumKitBank.cs | ⏳ | | |
| 445 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Synth/M50DrumKitBanks.cs | ⏳ | | |
| 446 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Synth/M50DrumPattern.cs | ⏳ | | |
| 447 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Synth/M50DrumPatternBank.cs | ⏳ | | |
| 448 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Synth/M50DrumPatternBanks.cs | ⏳ | | |
| 449 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Synth/M50Factory.cs | ⏳ | | |
| 450 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Synth/M50Global.cs | ⏳ | | |
| 451 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Synth/M50GmProgram.cs | ⏳ | | |
| 452 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Synth/M50GmProgramBank.cs | ⏳ | | |
| 453 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Synth/M50Program.cs | ⏳ | | |
| 454 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Synth/M50ProgramBank.cs | ⏳ | | |
| 455 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Synth/M50ProgramBanks.cs | ⏳ | | |
| 456 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Synth/M50Timbre.cs | ⏳ | | |
| 457 | pcg-tools-csharp/KorgKronosTools/Model/M50Specific/Synth/M50Timbres.cs | ⏳ | | |
| 458 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Pcg/MPcgFileReader.cs | ⏳ | | |
| 459 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Pcg/MPcgMemory.cs | ⏳ | | |
| 460 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Song/MSongFileReader.cs | ⏳ | | |
| 461 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Song/MSongMemory.cs | ⏳ | | |
| 462 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Synth/MCombi.cs | ⏳ | | |
| 463 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Synth/MCombiBank.cs | ⏳ | | |
| 464 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Synth/MCombiBanks.cs | ⏳ | | |
| 465 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Synth/MDrumKit.cs | ⏳ | | |
| 466 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Synth/MDrumKitBank.cs | ⏳ | | |
| 467 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Synth/MDrumKitBanks.cs | ⏳ | | |
| 468 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Synth/MDrumPattern.cs | ⏳ | | |
| 469 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Synth/MDrumPatternBank.cs | ⏳ | | |
| 470 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Synth/MDrumPatternBanks.cs | ⏳ | | |
| 471 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Synth/MFactory.cs | ⏳ | | |
| 472 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Synth/MGlobal.cs | ⏳ | | |
| 473 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Synth/MProgram.cs | ⏳ | | |
| 474 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Synth/MProgramBank.cs | ⏳ | | |
| 475 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Synth/MProgramBanks.cs | ⏳ | | |
| 476 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Synth/MTimbre.cs | ⏳ | | |
| 477 | pcg-tools-csharp/KorgKronosTools/Model/MSpecific/Synth/MTimbres.cs | ⏳ | | |
| 478 | pcg-tools-csharp/KorgKronosTools/Model/MicroKorgXlSpecific/Pcg/MicroKorgXlMkxlAllFileReader.cs | ⏳ | | |
| 479 | pcg-tools-csharp/KorgKronosTools/Model/MicroKorgXlSpecific/Pcg/MicroKorgXlMkxlAllMemory.cs | ⏳ | | |
| 480 | pcg-tools-csharp/KorgKronosTools/Model/MicroKorgXlSpecific/Pcg/MicroKorgXlMkxlPAllFileReader.cs | ⏳ | | |
| 481 | pcg-tools-csharp/KorgKronosTools/Model/MicroKorgXlSpecific/Pcg/MicroKorgXlMkxlPAllMemory.cs | ⏳ | | |
| 482 | pcg-tools-csharp/KorgKronosTools/Model/MicroKorgXlSpecific/Pcg/MicroKorgXlMkxlPProgFileReader.cs | ⏳ | | |
| 483 | pcg-tools-csharp/KorgKronosTools/Model/MicroKorgXlSpecific/Pcg/MicroKorgXlMkxlPProgMemory.cs | ⏳ | | |
| 484 | pcg-tools-csharp/KorgKronosTools/Model/MicroKorgXlSpecific/Song/MicroKorgXlSongFileReader.cs | ⏳ | | |
| 485 | pcg-tools-csharp/KorgKronosTools/Model/MicroKorgXlSpecific/Song/MicroKorgXlSongMemory.cs | ⏳ | | |
| 486 | pcg-tools-csharp/KorgKronosTools/Model/MicroKorgXlSpecific/Synth/MicroKorgXlFactory.cs | ⏳ | | |
| 487 | pcg-tools-csharp/KorgKronosTools/Model/MicroKorgXlSpecific/Synth/MicroKorgXlGlobal.cs | ⏳ | | |
| 488 | pcg-tools-csharp/KorgKronosTools/Model/MicroKorgXlSpecific/Synth/MicroKorgXlPlusFactory.cs | ⏳ | | |
| 489 | pcg-tools-csharp/KorgKronosTools/Model/MicroKorgXlSpecific/Synth/MicroKorgXlPlusProgramBank.cs | ⏳ | | |
| 490 | pcg-tools-csharp/KorgKronosTools/Model/MicroKorgXlSpecific/Synth/MicroKorgXlPlusProgramBanks.cs | ⏳ | | |
| 491 | pcg-tools-csharp/KorgKronosTools/Model/MicroKorgXlSpecific/Synth/MicroKorgXlProgram.cs | ⏳ | | |
| 492 | pcg-tools-csharp/KorgKronosTools/Model/MicroKorgXlSpecific/Synth/MicroKorgXlProgramBank.cs | ⏳ | | |
| 493 | pcg-tools-csharp/KorgKronosTools/Model/MicroKorgXlSpecific/Synth/MicroKorgXlProgramBanks.cs | ⏳ | | |
| 494 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Pcg/MicroStationPcgFileReader.cs | ⏳ | | |
| 495 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Pcg/MicroStationPcgMemory.cs | ⏳ | | |
| 496 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Song/MicroStationSongFileReader.cs | ⏳ | | |
| 497 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Song/MicroStationSongMemory.cs | ⏳ | | |
| 498 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Synth/MicroStationCombi.cs | ⏳ | | |
| 499 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Synth/MicroStationCombiBank.cs | ⏳ | | |
| 500 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Synth/MicroStationCombiBanks.cs | ⏳ | | |
| 501 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Synth/MicroStationDrumKit.cs | ⏳ | | |
| 502 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Synth/MicroStationDrumKitBank.cs | ⏳ | | |
| 503 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Synth/MicroStationDrumKitBanks.cs | ⏳ | | |
| 504 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Synth/MicroStationFactory.cs | ⏳ | | |
| 505 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Synth/MicroStationGlobal.cs | ⏳ | | |
| 506 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Synth/MicroStationGmProgram.cs | ⏳ | | |
| 507 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Synth/MicroStationGmProgramBank.cs | ⏳ | | |
| 508 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Synth/MicroStationProgram.cs | ⏳ | | |
| 509 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Synth/MicroStationProgramBank.cs | ⏳ | | |
| 510 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Synth/MicroStationProgramBanks.cs | ⏳ | | |
| 511 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Synth/MicroStationTimbre.cs | ⏳ | | |
| 512 | pcg-tools-csharp/KorgKronosTools/Model/MicroStationSpecific/Synth/MicroStationTimbres.cs | ⏳ | | |
| 513 | pcg-tools-csharp/KorgKronosTools/Model/MntxSeriesSpecific/Pcg/MntxSysExMemory.cs | ⏳ | | |
| 514 | pcg-tools-csharp/KorgKronosTools/Model/MntxSeriesSpecific/Song/MntxSongFileReader.cs | ⏳ | | |
| 515 | pcg-tools-csharp/KorgKronosTools/Model/MntxSeriesSpecific/Song/MntxSongMemory.cs | ⏳ | | |
| 516 | pcg-tools-csharp/KorgKronosTools/Model/MntxSeriesSpecific/Synth/MntxCombi.cs | ⏳ | | |
| 517 | pcg-tools-csharp/KorgKronosTools/Model/MntxSeriesSpecific/Synth/MntxCombiBank.cs | ⏳ | | |
| 518 | pcg-tools-csharp/KorgKronosTools/Model/MntxSeriesSpecific/Synth/MntxCombiBanks.cs | ⏳ | | |
| 519 | pcg-tools-csharp/KorgKronosTools/Model/MntxSeriesSpecific/Synth/MntxFactory.cs | ⏳ | | |
| 520 | pcg-tools-csharp/KorgKronosTools/Model/MntxSeriesSpecific/Synth/MntxGlobal.cs | ⏳ | | |
| 521 | pcg-tools-csharp/KorgKronosTools/Model/MntxSeriesSpecific/Synth/MntxProgram.cs | ⏳ | | |
| 522 | pcg-tools-csharp/KorgKronosTools/Model/MntxSeriesSpecific/Synth/MntxProgramBank.cs | ⏳ | | |
| 523 | pcg-tools-csharp/KorgKronosTools/Model/MntxSeriesSpecific/Synth/MntxProgramBanks.cs | ⏳ | | |
| 524 | pcg-tools-csharp/KorgKronosTools/Model/MntxSeriesSpecific/Synth/MntxTimbre.cs | ⏳ | | |
| 525 | pcg-tools-csharp/KorgKronosTools/Model/MntxSeriesSpecific/Synth/MntxTimbres.cs | ⏳ | | |
| 526 | pcg-tools-csharp/KorgKronosTools/Model/Ms2000Specific/Pcg/Ms2000FileReader.cs | ⏳ | | |
| 527 | pcg-tools-csharp/KorgKronosTools/Model/Ms2000Specific/Pcg/Ms2000MkP0Memory.cs | ⏳ | | |
| 528 | pcg-tools-csharp/KorgKronosTools/Model/Ms2000Specific/Pcg/Ms2000SysExMemory.cs | ⏳ | | |
| 529 | pcg-tools-csharp/KorgKronosTools/Model/Ms2000Specific/Song/Ms2000Memory.cs | ⏳ | | |
| 530 | pcg-tools-csharp/KorgKronosTools/Model/Ms2000Specific/Song/Ms2000SongFileReader.cs | ⏳ | | |
| 531 | pcg-tools-csharp/KorgKronosTools/Model/Ms2000Specific/Synth/Ms2000Factory.cs | ⏳ | | |
| 532 | pcg-tools-csharp/KorgKronosTools/Model/Ms2000Specific/Synth/Ms2000Global.cs | ⏳ | | |
| 533 | pcg-tools-csharp/KorgKronosTools/Model/Ms2000Specific/Synth/Ms2000Program.cs | ⏳ | | |
| 534 | pcg-tools-csharp/KorgKronosTools/Model/Ms2000Specific/Synth/Ms2000ProgramBank.cs | ⏳ | | |
| 535 | pcg-tools-csharp/KorgKronosTools/Model/Ms2000Specific/Synth/Ms2000ProgramBanks.cs | ⏳ | | |
| 536 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Pcg/OasysPcgFileReader.cs | ⏳ | | |
| 537 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Pcg/OasysPcgMemory.cs | ⏳ | | |
| 538 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Song/OasysSongFileReader.cs | ⏳ | | |
| 539 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Song/OasysSongMemory.cs | ⏳ | | |
| 540 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Synth/OasysCombi.cs | ⏳ | | |
| 541 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Synth/OasysCombiBank.cs | ⏳ | | |
| 542 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Synth/OasysCombiBanks.cs | ⏳ | | |
| 543 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Synth/OasysDrumKit.cs | ⏳ | | |
| 544 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Synth/OasysDrumKitBank.cs | ⏳ | | |
| 545 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Synth/OasysDrumKitBanks.cs | ⏳ | | |
| 546 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Synth/OasysFactory.cs | ⏳ | | |
| 547 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Synth/OasysGlobal.cs | ⏳ | | |
| 548 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Synth/OasysGmProgram.cs | ⏳ | | |
| 549 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Synth/OasysGmProgramBank.cs | ⏳ | | |
| 550 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Synth/OasysProgram.cs | ⏳ | | |
| 551 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Synth/OasysProgramBank.cs | ⏳ | | |
| 552 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Synth/OasysProgramBanks.cs | ⏳ | | |
| 553 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Synth/OasysTimbre.cs | ⏳ | | |
| 554 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Synth/OasysTimbres.cs | ⏳ | | |
| 555 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Synth/OasysWaveSequence.cs | ⏳ | | |
| 556 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Synth/OasysWaveSequenceBank.cs | ⏳ | | |
| 557 | pcg-tools-csharp/KorgKronosTools/Model/OasysSpecific/Synth/OasysWaveSequenceBanks.cs | ⏳ | | |
| 558 | pcg-tools-csharp/KorgKronosTools/Model/TSeries/Pcg/TSeriesFileReader.cs | ⏳ | | |
| 559 | pcg-tools-csharp/KorgKronosTools/Model/TSeries/Pcg/TSeriesSysExMemory.cs | ⏳ | | |
| 560 | pcg-tools-csharp/KorgKronosTools/Model/TSeries/Song/TSeriesSongFileReader.cs | ⏳ | | |
| 561 | pcg-tools-csharp/KorgKronosTools/Model/TSeries/Song/TSeriesSongMemory.cs | ⏳ | | |
| 562 | pcg-tools-csharp/KorgKronosTools/Model/TSeries/Synth/TSeriesCombi.cs | ⏳ | | |
| 563 | pcg-tools-csharp/KorgKronosTools/Model/TSeries/Synth/TSeriesCombiBank.cs | ⏳ | | |
| 564 | pcg-tools-csharp/KorgKronosTools/Model/TSeries/Synth/TSeriesCombiBanks.cs | ⏳ | | |
| 565 | pcg-tools-csharp/KorgKronosTools/Model/TSeries/Synth/TSeriesFactory.cs | ⏳ | | |
| 566 | pcg-tools-csharp/KorgKronosTools/Model/TSeries/Synth/TSeriesGlobal.cs | ⏳ | | |
| 567 | pcg-tools-csharp/KorgKronosTools/Model/TSeries/Synth/TSeriesProgram.cs | ⏳ | | |
| 568 | pcg-tools-csharp/KorgKronosTools/Model/TSeries/Synth/TSeriesProgramBank.cs | ⏳ | | |
| 569 | pcg-tools-csharp/KorgKronosTools/Model/TSeries/Synth/TSeriesProgramBanks.cs | ⏳ | | |
| 570 | pcg-tools-csharp/KorgKronosTools/Model/TSeries/Synth/TSeriesTimbre.cs | ⏳ | | |
| 571 | pcg-tools-csharp/KorgKronosTools/Model/TSeries/Synth/TSeriesTimbres.cs | ⏳ | | |
| 572 | pcg-tools-csharp/KorgKronosTools/Model/TrinitySpecific/Pcg/TrinityPcgFileReader.cs | ⏳ | | |
| 573 | pcg-tools-csharp/KorgKronosTools/Model/TrinitySpecific/Pcg/TrinityPcgMemory.cs | ⏳ | | |
| 574 | pcg-tools-csharp/KorgKronosTools/Model/TrinitySpecific/Synth/TrinityCombi.cs | ⏳ | | |
| 575 | pcg-tools-csharp/KorgKronosTools/Model/TrinitySpecific/Synth/TrinityCombiBank.cs | ⏳ | | |
| 576 | pcg-tools-csharp/KorgKronosTools/Model/TrinitySpecific/Synth/TrinityCombiBanks.cs | ⏳ | | |
| 577 | pcg-tools-csharp/KorgKronosTools/Model/TrinitySpecific/Synth/TrinityDrumKit.cs | ⏳ | | |
| 578 | pcg-tools-csharp/KorgKronosTools/Model/TrinitySpecific/Synth/TrinityDrumKitBank.cs | ⏳ | | |
| 579 | pcg-tools-csharp/KorgKronosTools/Model/TrinitySpecific/Synth/TrinityDrumKitBanks.cs | ⏳ | | |
| 580 | pcg-tools-csharp/KorgKronosTools/Model/TrinitySpecific/Synth/TrinityFactory.cs | ⏳ | | |
| 581 | pcg-tools-csharp/KorgKronosTools/Model/TrinitySpecific/Synth/TrinityGlobal.cs | ⏳ | | |
| 582 | pcg-tools-csharp/KorgKronosTools/Model/TrinitySpecific/Synth/TrinityGmProgram.cs | ⏳ | | |
| 583 | pcg-tools-csharp/KorgKronosTools/Model/TrinitySpecific/Synth/TrinityGmProgramBank.cs | ⏳ | | |
| 584 | pcg-tools-csharp/KorgKronosTools/Model/TrinitySpecific/Synth/TrinityProgram.cs | ⏳ | | |
| 585 | pcg-tools-csharp/KorgKronosTools/Model/TrinitySpecific/Synth/TrinityProgramBank.cs | ⏳ | | |
| 586 | pcg-tools-csharp/KorgKronosTools/Model/TrinitySpecific/Synth/TrinityProgramBanks.cs | ⏳ | | |
| 587 | pcg-tools-csharp/KorgKronosTools/Model/TrinitySpecific/Synth/TrinityTimbre.cs | ⏳ | | |
| 588 | pcg-tools-csharp/KorgKronosTools/Model/TrinitySpecific/Synth/TrinityTimbres.cs | ⏳ | | |
| 589 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Pcg/TritonExtremePcgFileReader.cs | ⏳ | | |
| 590 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Pcg/TritonExtremePcgMemory.cs | ⏳ | | |
| 591 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Song/TritonExtremeSongFileReader.cs | ⏳ | | |
| 592 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Song/TritonExtremeSongMemory.cs | ⏳ | | |
| 593 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Synth/TritonExtremeCombi.cs | ⏳ | | |
| 594 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Synth/TritonExtremeCombiBank.cs | ⏳ | | |
| 595 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Synth/TritonExtremeCombiBanks.cs | ⏳ | | |
| 596 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Synth/TritonExtremeDrumKit.cs | ⏳ | | |
| 597 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Synth/TritonExtremeDrumKitBank.cs | ⏳ | | |
| 598 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Synth/TritonExtremeDrumKitBanks.cs | ⏳ | | |
| 599 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Synth/TritonExtremeFactory.cs | ⏳ | | |
| 600 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Synth/TritonExtremeGlobal.cs | ⏳ | | |
| 601 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Synth/TritonExtremeGmProgram.cs | ⏳ | | |
| 602 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Synth/TritonExtremeGmProgramBank.cs | ⏳ | | |
| 603 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Synth/TritonExtremeProgram.cs | ⏳ | | |
| 604 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Synth/TritonExtremeProgramBank.cs | ⏳ | | |
| 605 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Synth/TritonExtremeProgramBanks.cs | ⏳ | | |
| 606 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Synth/TritonExtremeTimbre.cs | ⏳ | | |
| 607 | pcg-tools-csharp/KorgKronosTools/Model/TritonExtremeSpecific/Synth/TritonExtremeTimbres.cs | ⏳ | | |
| 608 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Pcg/TritonKarmaPcgFileReader.cs | ⏳ | | |
| 609 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Pcg/TritonKarmaPcgMemory.cs | ⏳ | | |
| 610 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Song/TritonKarmaSongFileReader.cs | ⏳ | | |
| 611 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Song/TritonKarmaSongMemory.cs | ⏳ | | |
| 612 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Synth/TritonKarmaCombi.cs | ⏳ | | |
| 613 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Synth/TritonKarmaCombiBank.cs | ⏳ | | |
| 614 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Synth/TritonKarmaCombiBanks.cs | ⏳ | | |
| 615 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Synth/TritonKarmaDrumKit.cs | ⏳ | | |
| 616 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Synth/TritonKarmaDrumKitBank.cs | ⏳ | | |
| 617 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Synth/TritonKarmaDrumKitBanks.cs | ⏳ | | |
| 618 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Synth/TritonKarmaFactory.cs | ⏳ | | |
| 619 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Synth/TritonKarmaGlobal.cs | ⏳ | | |
| 620 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Synth/TritonKarmaGmProgram.cs | ⏳ | | |
| 621 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Synth/TritonKarmaGmProgramBank.cs | ⏳ | | |
| 622 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Synth/TritonKarmaProgram.cs | ⏳ | | |
| 623 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Synth/TritonKarmaProgramBank.cs | ⏳ | | |
| 624 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Synth/TritonKarmaProgramBanks.cs | ⏳ | | |
| 625 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Synth/TritonKarmaTimbre.cs | ⏳ | | |
| 626 | pcg-tools-csharp/KorgKronosTools/Model/TritonKarmaSpecific/Synth/TritonKarmaTimbres.cs | ⏳ | | |
| 627 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Pcg/TritonLePcgFileReader.cs | ⏳ | | |
| 628 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Pcg/TritonLePcgMemory.cs | ⏳ | | |
| 629 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Song/TritonLeSongFileReader.cs | ⏳ | | |
| 630 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Song/TritonLeSongMemory.cs | ⏳ | | |
| 631 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Synth/TritonLeCombi.cs | ⏳ | | |
| 632 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Synth/TritonLeCombiBank.cs | ⏳ | | |
| 633 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Synth/TritonLeCombiBanks.cs | ⏳ | | |
| 634 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Synth/TritonLeDrumKit.cs | ⏳ | | |
| 635 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Synth/TritonLeDrumKitBank.cs | ⏳ | | |
| 636 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Synth/TritonLeDrumKitBanks.cs | ⏳ | | |
| 637 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Synth/TritonLeFactory.cs | ⏳ | | |
| 638 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Synth/TritonLeGlobal.cs | ⏳ | | |
| 639 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Synth/TritonLeGmProgram.cs | ⏳ | | |
| 640 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Synth/TritonLeGmProgramBank.cs | ⏳ | | |
| 641 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Synth/TritonLeProgram.cs | ⏳ | | |
| 642 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Synth/TritonLeProgramBank.cs | ⏳ | | |
| 643 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Synth/TritonLeProgramBanks.cs | ⏳ | | |
| 644 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Synth/TritonLeTimbre.cs | ⏳ | | |
| 645 | pcg-tools-csharp/KorgKronosTools/Model/TritonLeSpecific/Synth/TritonLeTimbres.cs | ⏳ | | |
| 646 | pcg-tools-csharp/KorgKronosTools/Model/TritonSpecific/Pcg/TritonPcgFileReader.cs | ⏳ | | |
| 647 | pcg-tools-csharp/KorgKronosTools/Model/TritonSpecific/Pcg/TritonPcgMemory.cs | ⏳ | | |
| 648 | pcg-tools-csharp/KorgKronosTools/Model/TritonSpecific/Song/TritonSongFileReader.cs | ⏳ | | |
| 649 | pcg-tools-csharp/KorgKronosTools/Model/TritonSpecific/Song/TritonSongMemory.cs | ⏳ | | |
| 650 | pcg-tools-csharp/KorgKronosTools/Model/TritonSpecific/Synth/TritonCombi.cs | ⏳ | | |
| 651 | pcg-tools-csharp/KorgKronosTools/Model/TritonSpecific/Synth/TritonCombiBank.cs | ⏳ | | |
| 652 | pcg-tools-csharp/KorgKronosTools/Model/TritonSpecific/Synth/TritonCombiBanks.cs | ⏳ | | |
| 653 | pcg-tools-csharp/KorgKronosTools/Model/TritonSpecific/Synth/TritonDrumKit.cs | ⏳ | | |
| 654 | pcg-tools-csharp/KorgKronosTools/Model/TritonSpecific/Synth/TritonDrumKitBank.cs | ⏳ | | |
| 655 | pcg-tools-csharp/KorgKronosTools/Model/TritonSpecific/Synth/TritonDrumKitBanks.cs | ⏳ | | |
| 656 | pcg-tools-csharp/KorgKronosTools/Model/TritonSpecific/Synth/TritonFactory.cs | ⏳ | | |
| 657 | pcg-tools-csharp/KorgKronosTools/Model/TritonSpecific/Synth/TritonGlobal.cs | ⏳ | | |
| 658 | pcg-tools-csharp/KorgKronosTools/Model/TritonSpecific/Synth/TritonProgram.cs | ⏳ | | |
| 659 | pcg-tools-csharp/KorgKronosTools/Model/TritonSpecific/Synth/TritonProgramBank.cs | ⏳ | | |
| 660 | pcg-tools-csharp/KorgKronosTools/Model/TritonSpecific/Synth/TritonProgramBanks.cs | ⏳ | | |
| 661 | pcg-tools-csharp/KorgKronosTools/Model/TritonSpecific/Synth/TritonTimbre.cs | ⏳ | | |
| 662 | pcg-tools-csharp/KorgKronosTools/Model/TritonSpecific/Synth/TritonTimbres.cs | ⏳ | | |
| 663 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Pcg/TritonTrClassicStudioRackPcgFileReader.cs | ⏳ | | |
| 664 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Pcg/TritonTrClassicStudioRackPcgMemory.cs | ⏳ | | |
| 665 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Song/TritonTrClassicStudioRackSongFileReader.cs | ⏳ | | |
| 666 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Song/TritonTrClassicStudioRackSongMemory.cs | ⏳ | | |
| 667 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Synth/TritonTrClassicStudioDrumKit.cs | ⏳ | | |
| 668 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Synth/TritonTrClassicStudioDrumKitBank.cs | ⏳ | | |
| 669 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Synth/TritonTrClassicStudioDrumKitBanks.cs | ⏳ | | |
| 670 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Synth/TritonTrClassicStudioRackCombi.cs | ⏳ | | |
| 671 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Synth/TritonTrClassicStudioRackCombiBank.cs | ⏳ | | |
| 672 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Synth/TritonTrClassicStudioRackCombiBanks.cs | ⏳ | | |
| 673 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Synth/TritonTrClassicStudioRackDrumKit.cs | ⏳ | | |
| 674 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Synth/TritonTrClassicStudioRackDrumKitBank.cs | ⏳ | | |
| 675 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Synth/TritonTrClassicStudioRackDrumKitBanks.cs | ⏳ | | |
| 676 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Synth/TritonTrClassicStudioRackFactory.cs | ⏳ | | |
| 677 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Synth/TritonTrClassicStudioRackGlobal.cs | ⏳ | | |
| 678 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Synth/TritonTrClassicStudioRackGmProgram.cs | ⏳ | | |
| 679 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Synth/TritonTrClassicStudioRackGmProgramBank.cs | ⏳ | | |
| 680 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Synth/TritonTrClassicStudioRackProgram.cs | ⏳ | | |
| 681 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Synth/TritonTrClassicStudioRackProgramBank.cs | ⏳ | | |
| 682 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Synth/TritonTrClassicStudioRackProgramBanks.cs | ⏳ | | |
| 683 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Synth/TritonTrClassicStudioRackTimbre.cs | ⏳ | | |
| 684 | pcg-tools-csharp/KorgKronosTools/Model/TritonTrClassicStudioRackSpecific/Synth/TritonTrClassicStudioRackTimbres.cs | ⏳ | | |
| 685 | pcg-tools-csharp/KorgKronosTools/Model/XSeries/Pcg/XSeriesFileReader.cs | ⏳ | | |
| 686 | pcg-tools-csharp/KorgKronosTools/Model/XSeries/Pcg/XSeriesSysExMemory.cs | ⏳ | | |
| 687 | pcg-tools-csharp/KorgKronosTools/Model/XSeries/Song/XSeriesSongFileReader.cs | ⏳ | | |
| 688 | pcg-tools-csharp/KorgKronosTools/Model/XSeries/Song/XSeriesSongMemory.cs | ⏳ | | |
| 689 | pcg-tools-csharp/KorgKronosTools/Model/XSeries/Synth/XSeriesCombi.cs | ⏳ | | |
| 690 | pcg-tools-csharp/KorgKronosTools/Model/XSeries/Synth/XSeriesCombiBank.cs | ⏳ | | |
| 691 | pcg-tools-csharp/KorgKronosTools/Model/XSeries/Synth/XSeriesCombiBanks.cs | ⏳ | | |
| 692 | pcg-tools-csharp/KorgKronosTools/Model/XSeries/Synth/XSeriesFactory.cs | ⏳ | | |
| 693 | pcg-tools-csharp/KorgKronosTools/Model/XSeries/Synth/XSeriesGlobal.cs | ⏳ | | |
| 694 | pcg-tools-csharp/KorgKronosTools/Model/XSeries/Synth/XSeriesProgram.cs | ⏳ | | |
| 695 | pcg-tools-csharp/KorgKronosTools/Model/XSeries/Synth/XSeriesProgramBank.cs | ⏳ | | |
| 696 | pcg-tools-csharp/KorgKronosTools/Model/XSeries/Synth/XSeriesProgramBanks.cs | ⏳ | | |
| 697 | pcg-tools-csharp/KorgKronosTools/Model/XSeries/Synth/XSeriesTimbre.cs | ⏳ | | |
| 698 | pcg-tools-csharp/KorgKronosTools/Model/XSeries/Synth/XSeriesTimbres.cs | ⏳ | | |
| 699 | pcg-tools-csharp/KorgKronosTools/Model/Z1Specific/Pcg/Z1FileReader.cs | ⏳ | | |
| 700 | pcg-tools-csharp/KorgKronosTools/Model/Z1Specific/Pcg/Z1SysExMemory.cs | ⏳ | | |
| 701 | pcg-tools-csharp/KorgKronosTools/Model/Z1Specific/Song/Z1SongFileReader.cs | ⏳ | | |
| 702 | pcg-tools-csharp/KorgKronosTools/Model/Z1Specific/Song/Z1SongMemory.cs | ⏳ | | |
| 703 | pcg-tools-csharp/KorgKronosTools/Model/Z1Specific/Synth/Z1Combi.cs | ⏳ | | |
| 704 | pcg-tools-csharp/KorgKronosTools/Model/Z1Specific/Synth/Z1CombiBank.cs | ⏳ | | |
| 705 | pcg-tools-csharp/KorgKronosTools/Model/Z1Specific/Synth/Z1CombiBanks.cs | ⏳ | | |
| 706 | pcg-tools-csharp/KorgKronosTools/Model/Z1Specific/Synth/Z1Factory.cs | ⏳ | | |
| 707 | pcg-tools-csharp/KorgKronosTools/Model/Z1Specific/Synth/Z1Global.cs | ⏳ | | |
| 708 | pcg-tools-csharp/KorgKronosTools/Model/Z1Specific/Synth/Z1Program.cs | ⏳ | | |
| 709 | pcg-tools-csharp/KorgKronosTools/Model/Z1Specific/Synth/Z1ProgramBank.cs | ⏳ | | |
| 710 | pcg-tools-csharp/KorgKronosTools/Model/Z1Specific/Synth/Z1ProgramBanks.cs | ⏳ | | |
| 711 | pcg-tools-csharp/KorgKronosTools/Model/Z1Specific/Synth/Z1Timbre.cs | ⏳ | | |
| 712 | pcg-tools-csharp/KorgKronosTools/Model/Z1Specific/Synth/Z1Timbres.cs | ⏳ | | |
| 713 | pcg-tools-csharp/KorgKronosTools/Model/Zero3Rw/Pcg/03RwFileReader.cs | ⏳ | | |
| 714 | pcg-tools-csharp/KorgKronosTools/Model/Zero3Rw/Pcg/03RwSysExMemory.cs | ⏳ | | |
| 715 | pcg-tools-csharp/KorgKronosTools/Model/Zero3Rw/Song/03RwSongFileReader.cs | ⏳ | | |
| 716 | pcg-tools-csharp/KorgKronosTools/Model/Zero3Rw/Song/03RwSongMemory.cs | ⏳ | | |
| 717 | pcg-tools-csharp/KorgKronosTools/Model/Zero3Rw/Synth/03RwCombi.cs | ⏳ | | |
| 718 | pcg-tools-csharp/KorgKronosTools/Model/Zero3Rw/Synth/03RwCombiBank.cs | ⏳ | | |
| 719 | pcg-tools-csharp/KorgKronosTools/Model/Zero3Rw/Synth/03RwCombiBanks.cs | ⏳ | | |
| 720 | pcg-tools-csharp/KorgKronosTools/Model/Zero3Rw/Synth/03RwFactory.cs | ⏳ | | |
| 721 | pcg-tools-csharp/KorgKronosTools/Model/Zero3Rw/Synth/03RwGlobal.cs | ⏳ | | |
| 722 | pcg-tools-csharp/KorgKronosTools/Model/Zero3Rw/Synth/03RwGmProgram.cs | ⏳ | | |
| 723 | pcg-tools-csharp/KorgKronosTools/Model/Zero3Rw/Synth/03RwGmProgramBank.cs | ⏳ | | |
| 724 | pcg-tools-csharp/KorgKronosTools/Model/Zero3Rw/Synth/03RwProgram.cs | ⏳ | | |
| 725 | pcg-tools-csharp/KorgKronosTools/Model/Zero3Rw/Synth/03RwProgramBank.cs | ⏳ | | |
| 726 | pcg-tools-csharp/KorgKronosTools/Model/Zero3Rw/Synth/03RwProgramBanks.cs | ⏳ | | |
| 727 | pcg-tools-csharp/KorgKronosTools/Model/Zero3Rw/Synth/03RwTimbre.cs | ⏳ | | |
| 728 | pcg-tools-csharp/KorgKronosTools/Model/Zero3Rw/Synth/03RwTimbres.cs | ⏳ | | |
| 729 | pcg-tools-csharp/KorgKronosTools/Model/ZeroSeries/Pcg/0SeriesFileReader.cs | ⏳ | | |
| 730 | pcg-tools-csharp/KorgKronosTools/Model/ZeroSeries/Pcg/0SeriesSysExMemory.cs | ⏳ | | |
| 731 | pcg-tools-csharp/KorgKronosTools/Model/ZeroSeries/Song/0SeriesSongFileReader.cs | ⏳ | | |
| 732 | pcg-tools-csharp/KorgKronosTools/Model/ZeroSeries/Song/0SeriesSongMemory.cs | ⏳ | | |
| 733 | pcg-tools-csharp/KorgKronosTools/Model/ZeroSeries/Synth/0SeriesCombi.cs | ⏳ | | |
| 734 | pcg-tools-csharp/KorgKronosTools/Model/ZeroSeries/Synth/0SeriesCombiBank.cs | ⏳ | | |
| 735 | pcg-tools-csharp/KorgKronosTools/Model/ZeroSeries/Synth/0SeriesCombiBanks.cs | ⏳ | | |
| 736 | pcg-tools-csharp/KorgKronosTools/Model/ZeroSeries/Synth/0SeriesFactory.cs | ⏳ | | |
| 737 | pcg-tools-csharp/KorgKronosTools/Model/ZeroSeries/Synth/0SeriesGlobal.cs | ⏳ | | |
| 738 | pcg-tools-csharp/KorgKronosTools/Model/ZeroSeries/Synth/0SeriesProgram.cs | ⏳ | | |
| 739 | pcg-tools-csharp/KorgKronosTools/Model/ZeroSeries/Synth/0SeriesProgramBank.cs | ⏳ | | |
| 740 | pcg-tools-csharp/KorgKronosTools/Model/ZeroSeries/Synth/0SeriesProgramBanks.cs | ⏳ | | |
| 741 | pcg-tools-csharp/KorgKronosTools/Model/ZeroSeries/Synth/0SeriesTimbre.cs | ⏳ | | |
| 742 | pcg-tools-csharp/KorgKronosTools/Model/ZeroSeries/Synth/0SeriesTimbres.cs | ⏳ | | |
| 743 | pcg-tools-csharp/KorgKronosTools/OpenedFiles/OpenedPcgWindow.cs | ⏳ | | |
| 744 | pcg-tools-csharp/KorgKronosTools/OpenedFiles/OpenedPcgWindows.cs | ⏳ | | |
| 745 | pcg-tools-csharp/KorgKronosTools/PcgToolsResources/StringResourceHelper.cs | ⏳ | | |
| 746 | pcg-tools-csharp/KorgKronosTools/PcgToolsResources/Strings.cs.Designer.cs | ⏳ | | |
| 747 | pcg-tools-csharp/KorgKronosTools/PcgToolsResources/Strings.de.Designer.cs | ⏳ | | |
| 748 | pcg-tools-csharp/KorgKronosTools/PcgToolsResources/Strings.el.Designer.cs | ⏳ | | |
| 749 | pcg-tools-csharp/KorgKronosTools/PcgToolsResources/Strings.en-TT.Designer.cs | ⏳ | | |
| 750 | pcg-tools-csharp/KorgKronosTools/PcgToolsResources/Strings.es.Designer.cs | ⏳ | | |
| 751 | pcg-tools-csharp/KorgKronosTools/PcgToolsResources/Strings.fr.Designer.cs | ⏳ | | |
| 752 | pcg-tools-csharp/KorgKronosTools/PcgToolsResources/Strings.it.Designer.cs | ⏳ | | |
| 753 | pcg-tools-csharp/KorgKronosTools/PcgToolsResources/Strings.nl.Designer.cs | ⏳ | | |
| 754 | pcg-tools-csharp/KorgKronosTools/PcgToolsResources/Strings.pl.Designer.cs | ⏳ | | |
| 755 | pcg-tools-csharp/KorgKronosTools/PcgToolsResources/Strings.pt-BR.Designer.cs | ⏳ | | |
| 756 | pcg-tools-csharp/KorgKronosTools/PcgToolsResources/Strings.pt-PT.Designer.cs | ⏳ | | |
| 757 | pcg-tools-csharp/KorgKronosTools/PcgToolsResources/Strings.ru.Designer.cs | ⏳ | | |
| 758 | pcg-tools-csharp/KorgKronosTools/PcgToolsResources/Strings.sr-Latn-RS.Designer.cs | ⏳ | | |
| 759 | pcg-tools-csharp/KorgKronosTools/PcgToolsResources/Strings2.Designer.cs | ⏳ | | |
| 760 | pcg-tools-csharp/KorgKronosTools/PcgToolsResources/StringsWrapper.cs | ⏳ | | |
| 761 | pcg-tools-csharp/KorgKronosTools/PcgWindow.xaml.cs | ⏳ | | |
| 762 | pcg-tools-csharp/KorgKronosTools/Properties/Annotations.cs | ⏳ | | |
| 763 | pcg-tools-csharp/KorgKronosTools/Properties/AssemblyInfo.cs | ⏳ | | |
| 764 | pcg-tools-csharp/KorgKronosTools/Properties/Resources.Designer.cs | ⏳ | | |
| 765 | pcg-tools-csharp/KorgKronosTools/Properties/Settings.Designer.cs | ⏳ | | |
| 766 | pcg-tools-csharp/KorgKronosTools/SettingsWindow.xaml.cs | ⏳ | | |
| 767 | pcg-tools-csharp/KorgKronosTools/SongTimbresWindow.xaml.cs | ⏳ | | |
| 768 | pcg-tools-csharp/KorgKronosTools/SongWindow.xaml.cs | ⏳ | | |
| 769 | pcg-tools-csharp/KorgKronosTools/SplashWindow.xaml.cs | ⏳ | | |
| 770 | pcg-tools-csharp/KorgKronosTools/Tools/ProgramPatchParser.cs | ⏳ | | |
| 771 | pcg-tools-csharp/KorgKronosTools/Tools/ProgramReferenceChangerWindow.xaml.cs | ⏳ | | |
| 772 | pcg-tools-csharp/KorgKronosTools/Tools/ReferenceChanger.cs | ⏳ | | |
| 773 | pcg-tools-csharp/KorgKronosTools/Tools/RuleParser.cs | ⏳ | | |
| 774 | pcg-tools-csharp/KorgKronosTools/ViewModels/CombiViewModel.cs | ⏳ | | |
| 775 | pcg-tools-csharp/KorgKronosTools/ViewModels/Commands/PcgCommands/ChangeVolumeParameters.cs | ⏳ | | |
| 776 | pcg-tools-csharp/KorgKronosTools/ViewModels/Commands/PcgCommands/ClearCommands.cs | ⏳ | | |
| 777 | pcg-tools-csharp/KorgKronosTools/ViewModels/Commands/PcgCommands/CopyPasteCommands.cs | ⏳ | | |
| 778 | pcg-tools-csharp/KorgKronosTools/ViewModels/Commands/PcgCommands/DoubleToSingleKeyboardCommands.cs | ⏳ | | |
| 779 | pcg-tools-csharp/KorgKronosTools/ViewModels/Commands/PcgCommands/DoubleToSingleKeyboardWindow.xaml.cs | ⏳ | | |
| 780 | pcg-tools-csharp/KorgKronosTools/ViewModels/Commands/PcgCommands/ModelCompatibility.cs | ⏳ | | |
| 781 | pcg-tools-csharp/KorgKronosTools/ViewModels/Commands/PcgCommands/PcgFileCommands.cs | ⏳ | | |
| 782 | pcg-tools-csharp/KorgKronosTools/ViewModels/Converters/EnumToBooleanConverter.cs | ⏳ | | |
| 783 | pcg-tools-csharp/KorgKronosTools/ViewModels/EditParameterViewModel.cs | ⏳ | | |
| 784 | pcg-tools-csharp/KorgKronosTools/ViewModels/ICombiViewModel.cs | ⏳ | | |
| 785 | pcg-tools-csharp/KorgKronosTools/ViewModels/IMainViewModel.cs | ⏳ | | |
| 786 | pcg-tools-csharp/KorgKronosTools/ViewModels/IPcgViewModel.cs | ⏳ | | |
| 787 | pcg-tools-csharp/KorgKronosTools/ViewModels/ISngTimbresViewModel.cs | ⏳ | | |
| 788 | pcg-tools-csharp/KorgKronosTools/ViewModels/ISongViewModel.cs | ⏳ | | |
| 789 | pcg-tools-csharp/KorgKronosTools/ViewModels/IViewModel.cs | ⏳ | | |
| 790 | pcg-tools-csharp/KorgKronosTools/ViewModels/MainViewModel.cs | ⏳ | | |
| 791 | pcg-tools-csharp/KorgKronosTools/ViewModels/MasterFilesViewModel.cs | ⏳ | | |
| 792 | pcg-tools-csharp/KorgKronosTools/ViewModels/ParameterChange/ParameterChangeParser.cs | ⏳ | | |
| 793 | pcg-tools-csharp/KorgKronosTools/ViewModels/ParameterChange/ParameterChangeSettings.cs | ⏳ | | |
| 794 | pcg-tools-csharp/KorgKronosTools/ViewModels/PcgViewModel.cs | ⏳ | | |
| 795 | pcg-tools-csharp/KorgKronosTools/ViewModels/SngTimbresViewModel.cs | ⏳ | | |
| 796 | pcg-tools-csharp/KorgKronosTools/ViewModels/SongViewModel.cs | ⏳ | | |
| 797 | pcg-tools-csharp/KorgKronosTools/ViewModels/ViewModel.cs | ⏳ | | |
| 798 | pcg-tools-csharp/KorgKronosTools/WPF.MDI/Example/App.xaml.cs | ⏳ | | |
| 799 | pcg-tools-csharp/KorgKronosTools/WPF.MDI/Example/Controls/ExampleControl.xaml.cs | ⏳ | | |
| 800 | pcg-tools-csharp/KorgKronosTools/WPF.MDI/Example/Main.xaml.cs | ⏳ | | |
| 801 | pcg-tools-csharp/KorgKronosTools/WPF.MDI/Example/Properties/AssemblyInfo.cs | ⏳ | | |
| 802 | pcg-tools-csharp/KorgKronosTools/WPF.MDI/Example/Properties/Resources.Designer.cs | ⏳ | | |
| 803 | pcg-tools-csharp/KorgKronosTools/WPF.MDI/Example/Properties/Settings.Designer.cs | ⏳ | | |
| 804 | pcg-tools-csharp/KorgKronosTools/WPF.MDI/WPF.MDI/Event/ClosingEventArgs.cs | ⏳ | | |
| 805 | pcg-tools-csharp/KorgKronosTools/WPF.MDI/WPF.MDI/MdiChild.cs | ⏳ | | |
| 806 | pcg-tools-csharp/KorgKronosTools/WPF.MDI/WPF.MDI/MdiContainer.cs | ⏳ | | |
| 807 | pcg-tools-csharp/KorgKronosTools/WPF.MDI/WPF.MDI/Properties/AssemblyInfo.cs | ⏳ | | |
| 808 | pcg-tools-csharp/KorgKronosTools/WPF.MDI/WPF.MDI/Properties/Resources.Designer.cs | ⏳ | | |
| 809 | pcg-tools-csharp/KorgKronosTools/WPF.MDI/WPF.MDI/Properties/Settings.Designer.cs | ⏳ | | |
| 810 | pcg-tools-csharp/KorgKronosTools/Windows/IPcgWindow.cs | ⏳ | | |
| 811 | pcg-tools-csharp/KorgKronosTools/Windows/IWindow.cs | ⏳ | | |
| 812 | pcg-tools-csharp/PCG | ⏳ | | |
| 813 | pcg-tools-csharp/PCG | ⏳ | | |
| 814 | pcg-tools-csharp/PCG | ⏳ | | |
| 815 | pcg-tools-csharp/PCG | ⏳ | | |
| 816 | pcg-tools-csharp/PCG | ⏳ | | |
| 817 | pcg-tools-csharp/PCG | ⏳ | | |
| 818 | pcg-tools-csharp/PCG | ⏳ | | |
| 819 | pcg-tools-csharp/PCG | ⏳ | | |
| 820 | pcg-tools-csharp/PCG | ⏳ | | |
| 821 | pcg-tools-csharp/PCG | ⏳ | | |
| 822 | pcg-tools-csharp/PCG | ⏳ | | |
| 823 | pcg-tools-csharp/PCG | ⏳ | | |
| 824 | pcg-tools-csharp/PCG | ⏳ | | |
| 825 | pcg-tools-csharp/PCG | ⏳ | | |
| 826 | pcg-tools-csharp/PCG | ⏳ | | |
| 827 | pcg-tools-csharp/PCG | ⏳ | | |
| 828 | pcg-tools-csharp/PCG | ⏳ | | |
| 829 | pcg-tools-csharp/PCG | ⏳ | | |
| 830 | pcg-tools-csharp/PCG | ⏳ | | |
| 831 | pcg-tools-csharp/PCG | ⏳ | | |
| 832 | pcg-tools-csharp/PCG | ⏳ | | |
| 833 | pcg-tools-csharp/PCG | ⏳ | | |
| 834 | pcg-tools-csharp/PCG | ⏳ | | |
| 835 | pcg-tools-csharp/PCG | ⏳ | | |
| 836 | pcg-tools-csharp/PCG | ⏳ | | |
| 837 | pcg-tools-csharp/PCG | ⏳ | | |
| 838 | pcg-tools-csharp/PCG | ⏳ | | |
| 839 | pcg-tools-csharp/PCG | ⏳ | | |
| 840 | pcg-tools-csharp/PCG | ⏳ | | |
| 841 | pcg-tools-csharp/PCG | ⏳ | | |
| 842 | pcg-tools-csharp/PCG | ⏳ | | |
| 843 | pcg-tools-csharp/PCG | ⏳ | | |
| 844 | pcg-tools-csharp/PCG | ⏳ | | |
| 845 | pcg-tools-csharp/PCG | ⏳ | | |
| 846 | pcg-tools-csharp/PCG | ⏳ | | |
| 847 | pcg-tools-csharp/PCG | ⏳ | | |
| 848 | pcg-tools-csharp/PCG | ⏳ | | |
| 849 | pcg-tools-csharp/PCG | ⏳ | | |
| 850 | pcg-tools-csharp/PCG | ⏳ | | |
| 851 | pcg-tools-csharp/PCG | ⏳ | | |
| 852 | pcg-tools-csharp/PCG | ⏳ | | |
| 853 | pcg-tools-csharp/PCG | ⏳ | | |
| 854 | pcg-tools-csharp/PCG | ⏳ | | |
| 855 | pcg-tools-csharp/PCG | ⏳ | | |
| 856 | pcg-tools-csharp/PCG | ⏳ | | |
| 857 | pcg-tools-csharp/PCG | ⏳ | | |
| 858 | pcg-tools-csharp/PCG | ⏳ | | |
| 859 | pcg-tools-csharp/PCG | ⏳ | | |
| 860 | pcg-tools-csharp/PCG | ⏳ | | |
| 861 | pcg-tools-csharp/PCG | ⏳ | | |
| 862 | pcg-tools-csharp/PCG | ⏳ | | |
| 863 | pcg-tools-csharp/PatchDatabaseBackEnd/CsvHelper.cs | ⏳ | | |
| 864 | pcg-tools-csharp/PatchDatabaseBackEnd/PatchData.cs | ⏳ | | |
| 865 | pcg-tools-csharp/PatchDatabaseBackEnd/PatchDataList.cs | ⏳ | | |
| 866 | pcg-tools-csharp/PatchDatabaseBackEnd/Properties/AssemblyInfo.cs | ⏳ | | |
| 867 | pcg-tools-csharp/PatchDbFrontEnd/App.xaml.cs | ⏳ | | |
| 868 | pcg-tools-csharp/PatchDbFrontEnd/MainWindow.xaml.cs | ⏳ | | |
| 869 | pcg-tools-csharp/PatchDbFrontEnd/Properties/AssemblyInfo.cs | ⏳ | | |
| 870 | pcg-tools-csharp/PatchDbFrontEnd/Properties/Resources.Designer.cs | ⏳ | | |
| 871 | pcg-tools-csharp/PatchDbFrontEnd/Properties/Settings.Designer.cs | ⏳ | | |
| 872 | pcg-tools-csharp/WPF.MDI/Event/ClosingEventArgs.cs | ⏳ | | |
| 873 | pcg-tools-csharp/WPF.MDI/MdiChild.cs | ⏳ | | |
| 874 | pcg-tools-csharp/WPF.MDI/MdiContainer.cs | ⏳ | | |
| 875 | pcg-tools-csharp/WPF.MDI/Properties/AssemblyInfo.cs | ⏳ | | |
| 876 | pcg-tools-csharp/WPF.MDI/Properties/Resources.Designer.cs | ⏳ | | |
| 877 | pcg-tools-csharp/WPF.MDI/Properties/Settings.Designer.cs | ⏳ | | |
| 878 | pcg-tools-csharp/WPF.MDI/_Backup/Example/App.xaml.cs | ⏳ | | |
| 879 | pcg-tools-csharp/WPF.MDI/_Backup/Example/Controls/ExampleControl.xaml.cs | ⏳ | | |
| 880 | pcg-tools-csharp/WPF.MDI/_Backup/Example/Main.xaml.cs | ⏳ | | |
| 881 | pcg-tools-csharp/WPF.MDI/_Backup/Example/Properties/AssemblyInfo.cs | ⏳ | | |
| 882 | pcg-tools-csharp/WPF.MDI/_Backup/Example/Properties/Resources.Designer.cs | ⏳ | | |
| 883 | pcg-tools-csharp/WPF.MDI/_Backup/Example/Properties/Settings.Designer.cs | ⏳ | | |
| 884 | pcg-tools-csharp/WPF.MDI/_Backup/WPF.MDI/Event/ClosingEventArgs.cs | ⏳ | | |
| 885 | pcg-tools-csharp/WPF.MDI/_Backup/WPF.MDI/MdiChild.cs | ⏳ | | |
| 886 | pcg-tools-csharp/WPF.MDI/_Backup/WPF.MDI/MdiContainer.cs | ⏳ | | |
| 887 | pcg-tools-csharp/WPF.MDI/_Backup/WPF.MDI/Properties/AssemblyInfo.cs | ⏳ | | |
| 888 | pcg-tools-csharp/WPF.MDI/_Backup/WPF.MDI/Properties/Resources.Designer.cs | ⏳ | | |
| 889 | pcg-tools-csharp/WPF.MDI/_Backup/WPF.MDI/Properties/Settings.Designer.cs | ⏳ | | |
| 890 | pcg-tools-csharp/WPF.MDI/_Example/App.xaml.cs | ⏳ | | |
| 891 | pcg-tools-csharp/WPF.MDI/_Example/Controls/ExampleControl.xaml.cs | ⏳ | | |
| 892 | pcg-tools-csharp/WPF.MDI/_Example/Main.xaml.cs | ⏳ | | |
| 893 | pcg-tools-csharp/WPF.MDI/_Example/Properties/AssemblyInfo.cs | ⏳ | | |
| 894 | pcg-tools-csharp/WPF.MDI/_Example/Properties/Resources.Designer.cs | ⏳ | | |
| 895 | pcg-tools-csharp/WPF.MDI/_Example/Properties/Settings.Designer.cs | ⏳ | | |


---

## Analysis Progress Log

### Session 1: December 22, 2025
**Files Analyzed**: 1-22 (Common Library)
**Summary**: 
- 21 files are WPF/MVVM-specific (❌ Not applicable) - these handle UI binding, commands, and observable patterns that Qt handles differently via signals/slots
- 1 file implemented (✅): BitsUtil.cs → pcg_tools/bit_utils.py
  - Verified: get_bits(), set_bits(), to_signed_bit() all implemented
  - Note: C# has SetMultiByteBits() which Python doesn't have but isn't used for Kronos

**Key Finding**: The Common library is mostly WPF infrastructure. The only core functionality (bit manipulation) is properly implemented in Python.

---

*Last Updated: December 22, 2025*
