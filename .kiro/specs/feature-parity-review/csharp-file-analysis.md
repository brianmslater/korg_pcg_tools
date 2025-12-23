# Complete C# File Analysis

This document provides a comprehensive analysis of EVERY source file in the C# PCG Tools repository.

**Total Source Files: 952** (895 .cs + 57 .xaml)

## File Count Breakdown

| Directory | .cs Files | .xaml Files | Total |
|-----------|-----------|-------------|-------|
| KorgKronosTools/Model | 647 | 0 | 647 |
| KorgKronosTools (non-Model) | 108 | 47 | 155 |
| Common library | 22 | 0 | 22 |
| PCG Tools Unittests | 51 | 0 | 51 |
| WPF.MDI | 25 | 5 | 30 |
| PatchDatabaseBackEnd | 4 | 0 | 4 |
| PatchDbFrontEnd | 3 | 2 | 5 |
| ExternalUtilities | 5 | 5 | 10 |
| **TOTAL** | **895** | **57** | **952** |

## Model Directory Breakdown (647 files)

| Subdirectory | Files | Priority | Python Status |
|--------------|-------|----------|---------------|
| Model/Common | 146 | HIGH | ✅ Mostly implemented |
| Model/KronosSpecific | 28 | HIGH | ⚠️ Partial (drum/wave missing) |
| Model/KronosOasysSpecific | 23 | HIGH | ✅ Implemented |
| Model/OasysSpecific | 22 | MEDIUM | ✅ Implemented |
| Model/M3Specific | 22 | MEDIUM | ✅ Implemented |
| Model/M3rSpecific | 23 | LOW | ❌ Not implemented |
| Model/M50Specific | 22 | MEDIUM | ✅ Implemented |
| Model/KromeSpecific | 22 | MEDIUM | ✅ Implemented |
| Model/KromeExSpecific | 22 | MEDIUM | ✅ Implemented |
| Model/KrossSpecific | 20 | MEDIUM | ✅ Implemented |
| Model/Kross2Specific | 20 | MEDIUM | ✅ Implemented |
| Model/TrinitySpecific | 17 | MEDIUM | ✅ Implemented |
| Model/TritonSpecific | 17 | MEDIUM | ✅ Implemented |
| Model/TritonLeSpecific | 19 | MEDIUM | ✅ Implemented |
| Model/TritonExtremeSpecific | 19 | MEDIUM | ✅ Implemented |
| Model/TritonKarmaSpecific | 19 | MEDIUM | ✅ Implemented |
| Model/TritonTrClassicStudioRackSpecific | 22 | MEDIUM | ✅ Implemented |
| Model/MSpecific | 20 | LOW | ❌ Not implemented |
| Model/MicroStationSpecific | 19 | LOW | ❌ Not implemented |
| Model/MicroKorgXlSpecific | 16 | LOW | ❌ Not implemented |
| Model/MntxSeriesSpecific | 13 | LOW | ❌ Not implemented |
| Model/Ms2000Specific | 10 | LOW | ❌ Not implemented |
| Model/M1Specific | 14 | LOW | ❌ Not implemented |
| Model/TSeries | 14 | LOW | ❌ Not implemented |
| Model/XSeries | 14 | LOW | ❌ Not implemented |
| Model/Z1Specific | 14 | LOW | ❌ Not implemented |
| Model/Zero3Rw | 16 | LOW | ❌ Not implemented |
| Model/ZeroSeries | 14 | LOW | ❌ Not implemented |

---

## ROOT LEVEL FILES (KorgKronosTools/)

### Application Entry & Main Windows

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 1 | `App.xaml` | Application entry point | App startup, resources | ✅ `__main__.py` | - |
| 2 | `App.xaml.cs` | Application code-behind | Startup logic, exception handling | ✅ `__main__.py` | - |
| 3 | `MainWindow.xaml` | Main application window | Menu bar, toolbar, MDI container, status bar | ✅ `gui_qt.py` | - |
| 4 | `MainWindow.xaml.cs` | Main window code-behind | File operations, window management | ✅ `gui_qt.py` | - |
| 5 | `PcgWindow.xaml` | PCG file viewer window | Bank list, patch list, radio buttons for patch types | ✅ `gui_qt.py` | - |
| 6 | `PcgWindow.xaml.cs` | PCG window code-behind | Selection handling, double-click, context menu | ✅ `gui_qt.py` | - |
| 7 | `CombiWindow.xaml` | Combi/timbre editor | 16 timbre columns, move/clear buttons | ✅ `gui_qt.py` | - |
| 8 | `CombiWindow.xaml.cs` | Combi window code-behind | Timbre editing logic | ✅ `gui_qt.py` | - |
| 9 | `SongWindow.xaml` | SNG file viewer | Songs tab, samples tab | ❌ Missing | Task 6.2.1 |
| 10 | `SongWindow.xaml.cs` | Song window code-behind | Song/sample display logic | ❌ Missing | Task 6.2.1 |
| 11 | `SongTimbresWindow.xaml` | Song timbres viewer | Timbres used in songs | ❌ Missing | Task 6.2.2 |
| 12 | `SongTimbresWindow.xaml.cs` | Song timbres code-behind | Song timbre display | ❌ Missing | Task 6.2.2 |
| 13 | `SettingsWindow.xaml` | Settings dialog | 6 tabs: PCG Window, Files, Edit, Cut/Copy/Paste, Sort, Categories | ⚠️ Partial | Task 4.x |
| 14 | `SettingsWindow.xaml.cs` | Settings code-behind | Settings persistence | ⚠️ Partial | Task 4.x |
| 15 | `SplashWindow.xaml` | Splash screen | Logo, version display | ❌ Not needed | - |
| 16 | `SplashWindow.xaml.cs` | Splash code-behind | Loading animation | ❌ Not needed | - |
| 17 | `HexExportDlg.xaml` | Hex export dialog | Raw hex data display | ❌ Missing | Task 7.2.1 |
| 18 | `HexExportDlg.xaml.cs` | Hex export code-behind | Hex formatting | ❌ Missing | Task 7.2.1 |
| 19 | `CommandLineInterfaceWindow.xaml` | CLI window | Command line interface | ✅ `cli.py` | - |
| 20 | `CommandLineInterfaceWindow.xaml.cs` | CLI code-behind | CLI processing | ✅ `cli.py` | - |
| 21 | `CommandLineArguments.cs` | CLI argument parser | Parse command line args | ✅ `cli.py` | - |
| 22 | `IChildWindow.cs` | Child window interface | MDI child interface | ✅ `gui_qt.py` | - |

---

## ClipBoard/ (18 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 23 | `CopyPaste.cs` | Copy/paste orchestration | Coordinate copy/paste operations | ✅ `clipboard.py` | - |
| 24 | `PcgClipBoard.cs` | Main clipboard manager | Store/retrieve clipboard data | ✅ `clipboard.py` | - |
| 25 | `IPcgClipBoard.cs` | Clipboard interface | Clipboard contract | ✅ `clipboard.py` | - |
| 26 | `ClipBoardPatch.cs` | Base patch clipboard | Common patch clipboard logic | ✅ `clipboard.py` | - |
| 27 | `IClipBoardPatch.cs` | Patch clipboard interface | Patch clipboard contract | ✅ `clipboard.py` | - |
| 28 | `ClipBoardPatches.cs` | Multiple patches clipboard | Batch clipboard operations | ✅ `clipboard.py` | - |
| 29 | `IClipBoardPatches.cs` | Patches clipboard interface | Batch clipboard contract | ✅ `clipboard.py` | - |
| 30 | `ClipBoardProgram.cs` | Program clipboard | Program-specific clipboard | ✅ `clipboard.py` | - |
| 31 | `IClipBoardProgram.cs` | Program clipboard interface | Program clipboard contract | ✅ `clipboard.py` | - |
| 32 | `ClipBoardCombi.cs` | Combi clipboard | Combi + timbre references | ✅ `clipboard.py` | - |
| 33 | `IClipBoardCombi.cs` | Combi clipboard interface | Combi clipboard contract | ✅ `clipboard.py` | - |
| 34 | `ClipBoardSetListSlot.cs` | Set list slot clipboard | Slot + patch references | ✅ `clipboard.py` | - |
| 35 | `IClipBoardSetListSlot .cs` | Slot clipboard interface | Slot clipboard contract | ✅ `clipboard.py` | - |
| 36 | `ClipBoardDrumKit.cs` | Drum kit clipboard | Drum kit clipboard | ❌ Missing | Task 3.1.1 |
| 37 | `IClipBoardDrumKit.cs` | Drum kit clipboard interface | Drum kit contract | ❌ Missing | Task 3.1.1 |
| 38 | `ClipBoardDrumPattern.cs` | Drum pattern clipboard | Drum pattern clipboard | ❌ Missing | Task 3.1.2 |
| 39 | `IClipBoardDrumPattern.cs` | Drum pattern clipboard interface | Drum pattern contract | ❌ Missing | Task 3.1.2 |
| 40 | `ClipBoardWaveSequence.cs` | Wave sequence clipboard | Wave sequence clipboard | ❌ Missing | Task 3.1.3 |

---

## Common/ (2 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 41 | `BoolExtensions.cs` | Boolean extensions | ToYesNo(), ToOnOff() | ✅ Built-in Python | - |
| 42 | `EnumExtensions.cs` | Enum extensions | GetDescription() | ✅ Built-in Python | - |

---

## Edit/ (18 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 43 | `EditUtils.cs` | Edit utilities | Common edit helpers | ✅ `qt_edit_dialog.py` | - |
| 44 | `WindowEditSingleProgram.xaml` | Edit single program | Name, category, favorite, OSC mode | ✅ `qt_edit_dialog.py` | - |
| 45 | `WindowEditSingleProgram.xaml.cs` | Program edit code-behind | Program edit logic | ✅ `qt_edit_dialog.py` | - |
| 46 | `WindowEditSingleCombi.xaml` | Edit single combi | Name, category, favorite, tempo | ✅ `qt_edit_dialog.py` | - |
| 47 | `WindowEditSingleCombi.xaml.cs` | Combi edit code-behind | Combi edit logic | ✅ `qt_edit_dialog.py` | - |
| 48 | `WindowEditSingleSetList.xaml` | Edit single set list | Set list name | ✅ `qt_edit_dialog.py` | - |
| 49 | `WindowEditSingleSetList.xaml.cs` | Set list edit code-behind | Set list edit logic | ✅ `qt_edit_dialog.py` | - |
| 50 | `WindowEditSingleSetListSlot.xaml` | Edit single slot | Name, color, text size, transpose, volume, description | ✅ `qt_edit_dialog.py` | - |
| 51 | `WindowEditSingleSetListSlot.xaml.cs` | Slot edit code-behind | Slot edit logic | ✅ `qt_edit_dialog.py` | - |
| 52 | `WindowEditMultipleCombis.xaml` | Edit multiple combis | Batch combi editing | ❌ Missing | Task 5.1.1 |
| 53 | `WindowEditMultipleCombis.xaml.cs` | Multi-combi edit code-behind | Batch combi logic | ❌ Missing | Task 5.1.1 |
| 54 | `WindowEditMultipleCombiBanks.xaml` | Edit multiple combi banks | Batch bank editing | ❌ Missing | Task 5.1.2 |
| 55 | `WindowEditMultipleCombiBanks.xaml.cs` | Multi-bank edit code-behind | Batch bank logic | ❌ Missing | Task 5.1.2 |
| 56 | `WindowEditMultipleSetListSlots.xaml` | Edit multiple slots | Batch slot editing | ❌ Missing | Task 5.1.3 |
| 57 | `WindowEditMultipleSetListSlots.xaml.cs` | Multi-slot edit code-behind | Batch slot logic | ❌ Missing | Task 5.1.3 |
| 58 | `WindowEditParameter.xaml` | Generic parameter editor | Any parameter type | ❌ Missing | Task 5.2.1 |
| 59 | `WindowEditParameter.xaml.cs` | Parameter edit code-behind | Generic parameter logic | ❌ Missing | Task 5.2.1 |
| 60 | `WindowEditParameterOld.xaml` | Old parameter editor | Legacy parameter editor | ❌ Not needed | - |
| 61 | `WindowEditParameterOld.xaml.cs` | Old parameter code-behind | Legacy code | ❌ Not needed | - |

---

## Gui/ (6 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 62 | `ChangeVolumeWindow.xaml` | Volume change dialog | Batch volume change | ❌ Missing | Task 1.4.1 |
| 63 | `ChangeVolumeWindow.xaml.cs` | Volume change code-behind | Volume change logic | ❌ Missing | Task 1.4.1 |
| 64 | `SelectSortWindow.xaml` | Sort options dialog | Sort criteria selection | ✅ `gui_qt.py` | - |
| 65 | `SelectSortWindow.xaml.cs` | Sort dialog code-behind | Sort selection logic | ✅ `gui_qt.py` | - |
| 66 | `Logo.cs` | Logo class | Logo data | ❌ Not needed | - |
| 67 | `Logos.cs` | Logos collection | Multiple logos | ❌ Not needed | - |

---

## Help/ (20 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 68 | `AboutWindow.xaml` | About dialog | Version, credits | ✅ `gui_qt.py` | - |
| 69 | `AboutWindow.xaml.cs` | About code-behind | About logic | ✅ `gui_qt.py` | - |
| 70 | `ExternalItem.cs` | External link item | Link data structure | ❌ Missing | Task 9.5.1 |
| 71 | `UserControlExternalLink.xaml` | External link control | Clickable link | ❌ Missing | Task 9.5.1 |
| 72 | `UserControlExternalLink.xaml.cs` | Link control code-behind | Link click handling | ❌ Missing | Task 9.5.1 |
| 73 | `ExternalLinksKorgRelatedWindow.xaml` | Korg links window | Korg-related links | ❌ Missing | Task 9.5.1 |
| 74 | `ExternalLinksKorgRelatedWindow.xaml.cs` | Korg links code-behind | Korg links logic | ❌ Missing | Task 9.5.1 |
| 75 | `ExternalLinksContributorsWindow.xaml` | Contributors window | Contributor links | ❌ Missing | Task 9.5.1 |
| 76 | `ExternalLinksContributorsWindow.xaml.cs` | Contributors code-behind | Contributors logic | ❌ Missing | Task 9.5.1 |
| 77 | `ExternalLinksVideoCreatorsWindow.xaml` | Video creators window | Video creator links | ❌ Missing | Task 9.5.1 |
| 78 | `ExternalLinksVideoCreatorsWindow.xaml.cs` | Video creators code-behind | Video creators logic | ❌ Missing | Task 9.5.1 |
| 79 | `ExternalLinksDonatorsWindow.xaml` | Donators window | Donator links | ❌ Missing | Task 9.5.1 |
| 80 | `ExternalLinksDonatorsWindow.xaml.cs` | Donators code-behind | Donators logic | ❌ Missing | Task 9.5.1 |
| 81 | `ExternalLinksTranslatorsWindow.xaml` | Translators window | Translator links | ❌ Missing | Task 9.5.1 |
| 82 | `ExternalLinksTranslatorsWindow.xaml.cs` | Translators code-behind | Translators logic | ❌ Missing | Task 9.5.1 |
| 83 | `ExternalLinksThirdPartiesWindow.xaml` | Third parties window | Third party links | ❌ Missing | Task 9.5.1 |
| 84 | `ExternalLinksThirdPartiesWindow.xaml.cs` | Third parties code-behind | Third parties logic | ❌ Missing | Task 9.5.1 |
| 85 | `ExternalLinksOasysVoucherCodeSponsorsWindow.xaml` | Oasys sponsors window | Sponsor links | ❌ Missing | Task 9.5.1 |
| 86 | `ExternalLinksOasysVoucherCodeSponsorsWindow.xaml.cs` | Sponsors code-behind | Sponsors logic | ❌ Missing | Task 9.5.1 |
| 87 | `ExternalLinksPersonalWindow.xaml` | Personal links window | Personal links | ❌ Missing | Task 9.5.1 |
| 88 | `ExternalLinksPersonalWindow.xaml.cs` | Personal links code-behind | Personal links logic | ❌ Missing | Task 9.5.1 |

---

## ListGenerator/ (10 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 89 | `ListGeneratorWindow.xaml` | List generator UI | All filter options, output formats | ⚠️ Partial | Task 2.x |
| 90 | `ListGeneratorWindow.xaml.cs` | List gen code-behind | Filter/generate logic | ⚠️ Partial | Task 2.x |
| 91 | `IListGenerator.cs` | List generator interface | Generator contract | ✅ `list_generators.py` | - |
| 92 | `ListGenerator.cs` | Base list generator | Common generator logic | ✅ `list_generators.py` | - |
| 93 | `ListGeneratorPatchList.cs` | Patch list generator | Generate patch list | ✅ `list_generators.py` | - |
| 94 | `ListGeneratorProgramUsageList.cs` | Program usage generator | Generate usage list | ✅ `list_generators.py` | - |
| 95 | `ListGeneratorCombiContentList.cs` | Combi content generator | Generate combi content (short/long) | ✅ `list_generators.py` | - |
| 96 | `ListGeneratorDifferencesList.cs` | Differences generator | Compare two PCG files | ✅ `list_generators.py` | - |
| 97 | `ListGeneratorDifferencesList-michelLaptop.cs` | Differences (backup) | Backup file | ❌ Not needed | - |
| 98 | `ListGeneratorFileContentList.cs` | File content generator | Bank usage summary | ❌ Missing | Task 2.1.1 |

---

## MasterFiles/ (5 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 99 | `IMasterFile.cs` | Master file interface | Master file contract | ❌ Missing | Task 1.2.1 |
| 100 | `MasterFile.cs` | Master file class | Master file data | ❌ Missing | Task 1.2.1 |
| 101 | `MasterFiles.cs` | Master files collection | Multiple master files | ❌ Missing | Task 1.2.1 |
| 102 | `MasterFilesWindow.xaml` | Master files UI | Master file management | ❌ Missing | Task 1.2.2 |
| 103 | `MasterFilesWindow.xaml.cs` | Master files code-behind | Master file logic | ❌ Missing | Task 1.2.2 |

---

## Tools/ (5 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 104 | `ReferenceChanger.cs` | Reference changer logic | Change program refs in combis/slots | ❌ Missing | Task 1.1.1 |
| 105 | `RuleParser.cs` | Rule parser | Parse reference change rules | ❌ Missing | Task 1.1.1 |
| 106 | `ProgramPatchParser.cs` | Program patch parser | Parse program patches | ❌ Missing | Task 1.1.1 |
| 107 | `ProgramReferenceChangerWindow.xaml` | Reference changer UI | Reference changer dialog | ❌ Missing | Task 1.1.2 |
| 108 | `ProgramReferenceChangerWindow.xaml.cs` | Reference changer code-behind | Reference changer logic | ❌ Missing | Task 1.1.2 |

---

## OpenedFiles/ (2 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 109 | `OpenedPcgWindow.cs` | Opened PCG window tracker | Track open windows | ✅ `gui_qt.py` | - |
| 110 | `OpenedPcgWindows.cs` | Opened windows collection | Multiple window tracking | ✅ `gui_qt.py` | - |

---

## Windows/ (2 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 111 | `IPcgWindow.cs` | PCG window interface | PCG window contract | ✅ `gui_qt.py` | - |
| 112 | `IWindow.cs` | Window interface | Window contract | ✅ `gui_qt.py` | - |

---

## ViewModels/ (16 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 113 | `ViewModel.cs` | Base view model | INotifyPropertyChanged | ✅ `gui_qt.py` | - |
| 114 | `IViewModel.cs` | View model interface | View model contract | ✅ `gui_qt.py` | - |
| 115 | `MainViewModel.cs` | Main view model | Main window state/commands | ✅ `gui_qt.py` | - |
| 116 | `IMainViewModel.cs` | Main VM interface | Main VM contract | ✅ `gui_qt.py` | - |
| 117 | `PcgViewModel.cs` | PCG view model | PCG window state/commands | ✅ `gui_qt.py` | - |
| 118 | `IPcgViewModel.cs` | PCG VM interface | PCG VM contract | ✅ `gui_qt.py` | - |
| 119 | `CombiViewModel.cs` | Combi view model | Combi window state/commands | ✅ `gui_qt.py` | - |
| 120 | `ICombiViewModel.cs` | Combi VM interface | Combi VM contract | ✅ `gui_qt.py` | - |
| 121 | `SongViewModel.cs` | Song view model | Song window state/commands | ❌ Missing | Task 6.2.1 |
| 122 | `ISongViewModel.cs` | Song VM interface | Song VM contract | ❌ Missing | Task 6.2.1 |
| 123 | `SngTimbresViewModel.cs` | Song timbres view model | Song timbres state | ❌ Missing | Task 6.2.2 |
| 124 | `ISngTimbresViewModel.cs` | Song timbres VM interface | Song timbres contract | ❌ Missing | Task 6.2.2 |
| 125 | `MasterFilesViewModel.cs` | Master files view model | Master files state | ❌ Missing | Task 1.2.2 |
| 126 | `EditParameterViewModel.cs` | Edit parameter view model | Parameter edit state | ❌ Missing | Task 5.2.1 |

---

## ViewModels/Commands/PcgCommands/ (8 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 127 | `PcgFileCommands.cs` | PCG file commands | Open, save, close commands | ✅ `gui_qt.py` | - |
| 128 | `CopyPasteCommands.cs` | Copy/paste commands | Cut, copy, paste commands | ✅ `gui_qt.py` | - |
| 129 | `ClearCommands.cs` | Clear commands | Clear, compact commands | ✅ `gui_qt.py` | - |
| 130 | `ChangeVolumeParameters.cs` | Volume change params | Volume change parameters | ❌ Missing | Task 1.4.1 |
| 131 | `DoubleToSingleKeyboardCommands.cs` | Double to single commands | Keyboard conversion | ❌ Missing | Task 8.5.1 |
| 132 | `DoubleToSingleKeyboardWindow.xaml` | Double to single UI | Conversion dialog | ❌ Missing | Task 8.5.1 |
| 133 | `DoubleToSingleKeyboardWindow.xaml.cs` | Double to single code-behind | Conversion logic | ❌ Missing | Task 8.5.1 |
| 134 | `ModelCompatibility.cs` | Model compatibility | Check model compatibility | ✅ `models.py` | - |

---

## ViewModels/Converters/ (1 file)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 135 | `EnumToBooleanConverter.cs` | Enum to bool converter | WPF value converter | ✅ Built-in Qt | - |

---

## ViewModels/ParameterChange/ (2 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 136 | `ParameterChangeParser.cs` | Parameter change parser | Parse parameter changes | ❌ Missing | Task 5.2.1 |
| 137 | `ParameterChangeSettings.cs` | Parameter change settings | Parameter change config | ❌ Missing | Task 5.2.1 |

---

## Properties/ (4 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 138 | `AssemblyInfo.cs` | Assembly info | Version, metadata | ✅ `setup.py` | - |
| 139 | `Resources.Designer.cs` | Resources designer | Auto-generated resources | ✅ Built-in | - |
| 140 | `Settings.Designer.cs` | Settings designer | Auto-generated settings | ✅ `settings.py` | - |
| 141 | `Annotations.cs` | Code annotations | JetBrains annotations | ❌ Not needed | - |

---

## PcgToolsResources/ (16 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 142 | `StringResourceHelper.cs` | String resource helper | Localization helper | ❌ Missing | Task 9.2.1 |
| 143 | `StringsWrapper.cs` | Strings wrapper | Localization wrapper | ❌ Missing | Task 9.2.1 |
| 144 | `Strings2.Designer.cs` | Additional strings | More localized strings | ❌ Missing | Task 9.2.1 |
| 145-156 | `Strings.*.Designer.cs` | Language strings | cs, de, el, en-TT, es, fr, it, nl, pl, pt-BR, pt-PT, ru, sr-Latn-RS | ❌ Missing | Task 9.2.2 |

---



## Model/Common/File/ (12 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 157 | `FileReader.cs` | Base file reader | Common file reading | ✅ `reader.py` | - |
| 158 | `IPatchesFileReader.cs` | Patches reader interface | Patches reader contract | ✅ `reader.py` | - |
| 159 | `ISongFileReader.cs` | Song reader interface | Song reader contract | ❌ Missing | Task 6.1.1 |
| 160 | `KorgFileReader.cs` | Korg file reader | Korg-specific reading | ✅ `reader.py` | - |
| 161 | `PatchesFileReader.cs` | Patches file reader | Read patches from file | ✅ `reader.py` | - |
| 162 | `PcgFileReader.cs` | PCG file reader | Read PCG files | ✅ `reader.py` | - |
| 163 | `SongFileReader.cs` | Song file reader | Read SNG files | ❌ Missing | Task 6.1.1 |
| 164 | `SysExFileReader.cs` | SysEx file reader | Read .syx files | ❌ LOW PRIORITY | - |
| 165 | `TrFileReader.cs` | TR file reader | Read .TR files | ❌ LOW PRIORITY | - |
| 166 | `MkxlAllFileReader.cs` | MicroKorg XL reader | Read .mkxl files | ❌ LOW PRIORITY | - |
| 167 | `MkxlFileReader.cs` | MicroKorg reader | Read MicroKorg files | ❌ LOW PRIORITY | - |
| 168 | `MkxlpFileReader.cs` | MicroKorg Plus reader | Read MicroKorg+ files | ❌ LOW PRIORITY | - |

---

## Model/Common/Synth/Global/ (2 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 169 | `Global.cs` | Global settings class | Global PCG settings | ✅ `models.py` | - |
| 170 | `IGlobal.cs` | Global interface | Global contract | ✅ `models.py` | - |

---

## Model/Common/Synth/MemoryAndFactory/ (20 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 171 | `Memory.cs` | Base memory class | PCG memory management | ✅ `models.py` | - |
| 172 | `IMemory.cs` | Memory interface | Memory contract | ✅ `models.py` | - |
| 173 | `IMemoryInit.cs` | Memory init interface | Memory initialization | ✅ `models.py` | - |
| 174 | `PcgMemory.cs` | PCG memory class | PCG-specific memory | ✅ `models.py` | - |
| 175 | `IPcgMemory.cs` | PCG memory interface | PCG memory contract | ✅ `models.py` | - |
| 176 | `IPcgMemoryInit.cs` | PCG memory init | PCG memory initialization | ✅ `models.py` | - |
| 177 | `SysExMemory.cs` | SysEx memory class | SysEx memory management | ❌ LOW PRIORITY | - |
| 178 | `ISysExMemory.cs` | SysEx memory interface | SysEx memory contract | ❌ LOW PRIORITY | - |
| 179 | `MkxlAllMemory.cs` | MicroKorg memory | MicroKorg memory | ❌ LOW PRIORITY | - |
| 180 | `Factory.cs` | Base factory class | Create model objects | ✅ `models.py` | - |
| 181 | `IFactory.cs` | Factory interface | Factory contract | ✅ `models.py` | - |
| 182 | `SysExFactory.cs` | SysEx factory | Create SysEx objects | ❌ LOW PRIORITY | - |
| 183 | `Model.cs` | Model class | Synthesizer model | ✅ `models.py` | - |
| 184 | `IModel.cs` | Model interface | Model contract | ✅ `models.py` | - |
| 185 | `Models.cs` | Models collection | All supported models | ✅ `models.py` | - |
| 186 | `Client.cs` | Client class | Client data | ✅ `models.py` | - |
| 187 | `Chunk.cs` | Chunk class | PCG chunk data | ✅ `pcg_parser.py` | - |
| 188 | `IChunk.cs` | Chunk interface | Chunk contract | ✅ `pcg_parser.py` | - |
| 189 | `Chunks.cs` | Chunks collection | Multiple chunks | ✅ `pcg_parser.py` | - |
| 190 | `IChunks.cs` | Chunks interface | Chunks contract | ✅ `pcg_parser.py` | - |

---

## Model/Common/Synth/Meta/ (10 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 191 | `Patch.cs` | Base patch class | Common patch data | ✅ `models.py` | - |
| 192 | `IPatch.cs` | Patch interface | Patch contract | ✅ `models.py` | - |
| 193 | `Bank.cs` | Base bank class | Common bank data | ✅ `models.py` | - |
| 194 | `IBank.cs` | Bank interface | Bank contract | ✅ `models.py` | - |
| 195 | `Banks.cs` | Banks collection | Multiple banks | ✅ `models.py` | - |
| 196 | `IBanks.cs` | Banks interface | Banks contract | ✅ `models.py` | - |
| 197 | `BankType.cs` | Bank type enum | Bank type definitions | ✅ `models.py` | - |
| 198 | `ObservableBankCollection.cs` | Observable banks | WPF observable collection | ✅ Qt signals | - |
| 199 | `IObservableBankCollection.cs` | Observable banks interface | Observable contract | ✅ Qt signals | - |
| 200 | `ObservablePatchCollection.cs` | Observable patches | WPF observable collection | ✅ Qt signals | - |

---

## Model/Common/Synth/PatchPrograms/ (7 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 201 | `Program.cs` | Program class | Program patch data | ✅ `models.py` | - |
| 202 | `IProgram.cs` | Program interface | Program contract | ✅ `models.py` | - |
| 203 | `ProgramBank.cs` | Program bank class | Program bank data | ✅ `models.py` | - |
| 204 | `IProgramBank.cs` | Program bank interface | Program bank contract | ✅ `models.py` | - |
| 205 | `ProgramBanks.cs` | Program banks collection | Multiple program banks | ✅ `models.py` | - |
| 206 | `IProgramBanks.cs` | Program banks interface | Program banks contract | ✅ `models.py` | - |
| 207 | `GmPrograms.cs` | GM programs | General MIDI programs | ✅ `gm2_data.py` | - |

---

## Model/Common/Synth/PatchCombis/ (11 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 208 | `Combi.cs` | Combi class | Combi patch data | ✅ `models.py` | - |
| 209 | `ICombi.cs` | Combi interface | Combi contract | ✅ `models.py` | - |
| 210 | `CombiBank.cs` | Combi bank class | Combi bank data | ✅ `models.py` | - |
| 211 | `ICombiBank.cs` | Combi bank interface | Combi bank contract | ✅ `models.py` | - |
| 212 | `CombiBanks.cs` | Combi banks collection | Multiple combi banks | ✅ `models.py` | - |
| 213 | `ICombiBanks.cs` | Combi banks interface | Combi banks contract | ✅ `models.py` | - |
| 214 | `Timbre.cs` | Timbre class | Timbre data | ✅ `models.py` | - |
| 215 | `ITimbre.cs` | Timbre interface | Timbre contract | ✅ `models.py` | - |
| 216 | `Timbres.cs` | Timbres collection | 16 timbres per combi | ✅ `models.py` | - |
| 217 | `ITimbres.cs` | Timbres interface | Timbres contract | ✅ `models.py` | - |
| 218 | `TimbreComparer.cs` | Timbre comparer | Compare timbres for sorting | ✅ `operations.py` | - |
| 219 | `TimbreSorting.cs` | Timbre sorting | Sort timbres | ✅ `operations.py` | - |

---

## Model/Common/Synth/PatchSetLists/ (6 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 220 | `SetList.cs` | Set list class | Set list data | ✅ `models.py` | - |
| 221 | `ISetList.cs` | Set list interface | Set list contract | ✅ `models.py` | - |
| 222 | `SetListSlot.cs` | Set list slot class | Slot data | ✅ `models.py` | - |
| 223 | `ISetListSlot.cs` | Set list slot interface | Slot contract | ✅ `models.py` | - |
| 224 | `SetLists.cs` | Set lists collection | 16 set lists | ✅ `models.py` | - |
| 225 | `ISetLists.cs` | Set lists interface | Set lists contract | ✅ `models.py` | - |

---

## Model/Common/Synth/PatchDrumKits/ (6 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 226 | `DrumKit.cs` | Drum kit class | Drum kit data | ❌ Missing | Task 1.5.2 |
| 227 | `IDrumKit.cs` | Drum kit interface | Drum kit contract | ❌ Missing | Task 1.5.2 |
| 228 | `DrumKitBank.cs` | Drum kit bank class | Drum kit bank data | ❌ Missing | Task 1.5.2 |
| 229 | `IDrumKitBank.cs` | Drum kit bank interface | Drum kit bank contract | ❌ Missing | Task 1.5.2 |
| 230 | `DrumKitBanks.cs` | Drum kit banks collection | Multiple drum kit banks | ❌ Missing | Task 1.5.2 |
| 231 | `IDrumKitBanks.cs` | Drum kit banks interface | Drum kit banks contract | ❌ Missing | Task 1.5.2 |

---

## Model/Common/Synth/PatchDrumPatterns/ (6 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 232 | `DrumPattern.cs` | Drum pattern class | Drum pattern data | ❌ Missing | Task 1.5.3 |
| 233 | `IDrumPattern.cs` | Drum pattern interface | Drum pattern contract | ❌ Missing | Task 1.5.3 |
| 234 | `DrumPatternBank.cs` | Drum pattern bank class | Drum pattern bank data | ❌ Missing | Task 1.5.3 |
| 235 | `IDrumPatternBank.cs` | Drum pattern bank interface | Drum pattern bank contract | ❌ Missing | Task 1.5.3 |
| 236 | `DrumPatternBanks.cs` | Drum pattern banks collection | Multiple drum pattern banks | ❌ Missing | Task 1.5.3 |
| 237 | `IDrumPatternBanks.cs` | Drum pattern banks interface | Drum pattern banks contract | ❌ Missing | Task 1.5.3 |

---

## Model/Common/Synth/PatchWaveSequences/ (6 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 238 | `WaveSequence.cs` | Wave sequence class | Wave sequence data | ❌ Missing | Task 1.5.1 |
| 239 | `IWaveSequence.cs` | Wave sequence interface | Wave sequence contract | ❌ Missing | Task 1.5.1 |
| 240 | `WaveSequenceBank.cs` | Wave sequence bank class | Wave sequence bank data | ❌ Missing | Task 1.5.1 |
| 241 | `IWaveSequenceBank.cs` | Wave sequence bank interface | Wave sequence bank contract | ❌ Missing | Task 1.5.1 |
| 242 | `WaveSequenceBanks.cs` | Wave sequence banks collection | Multiple wave sequence banks | ❌ Missing | Task 1.5.1 |
| 243 | `IWaveSequenceBanks.cs` | Wave sequence banks interface | Wave sequence banks contract | ❌ Missing | Task 1.5.1 |

---

## Model/Common/Synth/PatchSorting/ (7 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 244 | `PatchSorter.cs` | Patch sorter | Sort patches | ✅ `operations.py` | - |
| 245 | `NameComparer.cs` | Name comparer | Sort by name | ✅ `operations.py` | - |
| 246 | `CategoricalComparer.cs` | Category comparer | Sort by category | ✅ `operations.py` | - |
| 247 | `EmptyOrInitComparer.cs` | Empty/init comparer | Sort empty/init to end | ✅ `operations.py` | - |
| 248 | `CompositeComparer.cs` | Composite comparer | Combine multiple comparers | ⚠️ Partial | Task 9.6.1 |
| 249 | `TitleComparer.cs` | Title comparer | Sort by title (split char) | ❌ Missing | Task 9.6.1 |
| 250 | `ArtistComparer.cs` | Artist comparer | Sort by artist (split char) | ❌ Missing | Task 9.6.1 |

---

## Model/Common/Synth/PatchInterfaces/ (18 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 251 | `INamable.cs` | Namable interface | Name property | ✅ `models.py` | - |
| 252 | `IIndexable.cs` | Indexable interface | Index property | ✅ `models.py` | - |
| 253 | `ILocatable.cs` | Locatable interface | Location property | ✅ `models.py` | - |
| 254 | `ISelectable.cs` | Selectable interface | Selection property | ✅ `models.py` | - |
| 255 | `IClearable.cs` | Clearable interface | Clear method | ✅ `models.py` | - |
| 256 | `IFillable.cs` | Fillable interface | Fill method | ✅ `models.py` | - |
| 257 | `ILoadable.cs` | Loadable interface | Load method | ✅ `models.py` | - |
| 258 | `IWritable.cs` | Writable interface | Write method | ✅ `models.py` | - |
| 259 | `IUpdatable.cs` | Updatable interface | Update method | ✅ `models.py` | - |
| 260 | `IDirtiable.cs` | Dirtiable interface | Dirty flag | ✅ `models.py` | - |
| 261 | `ICountable.cs` | Countable interface | Count property | ✅ `models.py` | - |
| 262 | `INavigable.cs` | Navigable interface | Navigation | ✅ `models.py` | - |
| 263 | `IPcgNavigable.cs` | PCG navigable interface | PCG navigation | ✅ `models.py` | - |
| 264 | `INotificatable.cs` | Notificatable interface | Notifications | ✅ `models.py` | - |
| 265 | `IReferencable.cs` | Referencable interface | References | ✅ `models.py` | - |
| 266 | `IParameterSettable.cs` | Parameter settable interface | Set parameters | ✅ `models.py` | - |
| 267 | `ICategoriesNamable.cs` | Categories namable interface | Category names | ✅ `models.py` | - |
| 268 | `IArtistable.cs` | Artistable interface | Artist property | ❌ Missing | Task 9.6.1 |
| 269 | `ICompleteInPcgable.cs` | Complete in PCG interface | PCG completeness | ✅ `models.py` | - |
| 270 | `IIsEmptyCheckable.cs` | Empty checkable interface | IsEmpty check | ✅ `models.py` | - |
| 271 | `ISupportedFeatures.cs` | Supported features interface | Feature flags | ✅ `models.py` | - |

---

## Model/Common/Synth/OldParameters/ (10 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 272 | `Parameter.cs` | Base parameter class | Common parameter logic | ✅ `models.py` | - |
| 273 | `IParameter.cs` | Parameter interface | Parameter contract | ✅ `models.py` | - |
| 274 | `IntParameter.cs` | Integer parameter | Int parameter | ✅ `models.py` | - |
| 275 | `WordParameter.cs` | Word parameter | 16-bit parameter | ✅ `models.py` | - |
| 276 | `BoolParameter.cs` | Boolean parameter | Bool parameter | ✅ `models.py` | - |
| 277 | `EnumParameter.cs` | Enum parameter | Enum parameter | ✅ `models.py` | - |
| 278 | `FixedParameter.cs` | Fixed parameter | Fixed value parameter | ✅ `models.py` | - |
| 279 | `IFixedParameter.cs` | Fixed parameter interface | Fixed parameter contract | ✅ `models.py` | - |
| 280 | `IFixedParameterValue.cs` | Fixed parameter value interface | Fixed value contract | ✅ `models.py` | - |
| 281 | `ParameterNames.cs` | Parameter names | Parameter name constants | ✅ `models.py` | - |
| 282 | `ParameterValues.cs` | Parameter values | Parameter value constants | ✅ `models.py` | - |
| 283 | `_BackupParameters.cs` | Backup parameters | Backup/restore parameters | ✅ `undo.py` | - |

---

## Model/Common/Synth/NewParameters/ (2 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 284 | `IIntParameter.cs` | Int parameter interface | Int parameter contract | ✅ `models.py` | - |
| 285 | `IntParameterBitsInByte.cs` | Bit-level int parameter | Bit manipulation | ✅ `bit_utils.py` | - |

---

## Model/Common/Synth/DrumTrack/ (1 file)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 286 | `IDrumTrackReference.cs` | Drum track reference interface | Drum track reference | ❌ Missing | Task 1.5.3 |

---

## Model/Common/Synth/SongsRelated/ (13 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 287 | `Song.cs` | Song class | Song data | ❌ Missing | Task 6.1.1 |
| 288 | `ISong.cs` | Song interface | Song contract | ❌ Missing | Task 6.1.1 |
| 289 | `Songs.cs` | Songs collection | Multiple songs | ❌ Missing | Task 6.1.1 |
| 290 | `ISongs.cs` | Songs interface | Songs contract | ❌ Missing | Task 6.1.1 |
| 291 | `SongMemory.cs` | Song memory class | Song memory management | ❌ Missing | Task 6.1.1 |
| 292 | `ISongMemory.cs` | Song memory interface | Song memory contract | ❌ Missing | Task 6.1.1 |
| 293 | `ISongMemoryInit.cs` | Song memory init interface | Song memory initialization | ❌ Missing | Task 6.1.1 |
| 294 | `SongTimbre.cs` | Song timbre class | Song timbre data | ❌ Missing | Task 6.2.2 |
| 295 | `ISongTimbre.cs` | Song timbre interface | Song timbre contract | ❌ Missing | Task 6.2.2 |
| 296 | `SongTimbres.cs` | Song timbres collection | Multiple song timbres | ❌ Missing | Task 6.2.2 |
| 297 | `ISongTimbres.cs` | Song timbres interface | Song timbres contract | ❌ Missing | Task 6.2.2 |
| 298 | `Region.cs` | Region class | Song region data | ❌ Missing | Task 6.1.1 |
| 299 | `IRegion.cs` | Region interface | Region contract | ❌ Missing | Task 6.1.1 |
| 300 | `Regions.cs` | Regions collection | Multiple regions | ❌ Missing | Task 6.1.1 |
| 301 | `IRegions.cs` | Regions interface | Regions contract | ❌ Missing | Task 6.1.1 |

---

## Model/Common/ (1 file)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 302 | `Util.cs` | Utility functions | Common utilities | ✅ `bit_utils.py` | - |



---

## Model/KronosSpecific/ (PRIMARY FOCUS - 27 files)

### Pcg/ (2 files)
| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 303 | `KronosPcgFileReader.cs` | Kronos PCG reader | Read Kronos PCG files | ✅ `pcg_parser.py` | - |
| 304 | `KronosPcgMemory.cs` | Kronos PCG memory | Kronos memory management | ✅ `models.py` | - |

### Song/ (2 files)
| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 305 | `KronosSongFileReader.cs` | Kronos SNG reader | Read Kronos SNG files | ❌ Missing | Task 6.1.1 |
| 306 | `KronosSongMemory.cs` | Kronos song memory | Kronos song management | ❌ Missing | Task 6.1.1 |

### Synth/ (23 files)
| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 307 | `KronosFactory.cs` | Kronos factory | Create Kronos objects | ✅ `models.py` | - |
| 308 | `KronosGlobal.cs` | Kronos global | Kronos global settings | ✅ `models.py` | - |
| 309 | `KronosProgram.cs` | Kronos program | Kronos program data | ✅ `models.py` | - |
| 310 | `KronosProgramBank.cs` | Kronos program bank | Kronos program bank | ✅ `models.py` | - |
| 311 | `KronosProgramBanks.cs` | Kronos program banks | Kronos program banks collection | ✅ `models.py` | - |
| 312 | `KronosGmProgram.cs` | Kronos GM program | Kronos GM2 program | ✅ `gm2_data.py` | - |
| 313 | `KronosGmProgramBank.cs` | Kronos GM bank | Kronos GM2 bank | ✅ `gm2_data.py` | - |
| 314 | `KronosCombi.cs` | Kronos combi | Kronos combi data | ✅ `models.py` | - |
| 315 | `KronosCombiBank.cs` | Kronos combi bank | Kronos combi bank | ✅ `models.py` | - |
| 316 | `KronosCombiBanks.cs` | Kronos combi banks | Kronos combi banks collection | ✅ `models.py` | - |
| 317 | `KronosTimbre.cs` | Kronos timbre | Kronos timbre data | ✅ `models.py` | - |
| 318 | `KronosTimbres.cs` | Kronos timbres | Kronos timbres collection | ✅ `models.py` | - |
| 319 | `KronosSetList.cs` | Kronos set list | Kronos set list data | ✅ `models.py` | - |
| 320 | `KronosSetListSlot.cs` | Kronos set list slot | Kronos slot data | ✅ `models.py` | - |
| 321 | `KronosSetLists.cs` | Kronos set lists | Kronos set lists collection | ✅ `models.py` | - |
| 322 | `KronosDrumKit.cs` | Kronos drum kit | Kronos drum kit data | ❌ Missing | Task 1.5.2 |
| 323 | `KronosDrumKitBank.cs` | Kronos drum kit bank | Kronos drum kit bank | ❌ Missing | Task 1.5.2 |
| 324 | `KronosDrumKitBanks.cs` | Kronos drum kit banks | Kronos drum kit banks collection | ❌ Missing | Task 1.5.2 |
| 325 | `KronosDrumPattern.cs` | Kronos drum pattern | Kronos drum pattern data | ❌ Missing | Task 1.5.3 |
| 326 | `KronosDrumPatternBank.cs` | Kronos drum pattern bank | Kronos drum pattern bank | ❌ Missing | Task 1.5.3 |
| 327 | `KronosDrumPatternBanks.cs` | Kronos drum pattern banks | Kronos drum pattern banks collection | ❌ Missing | Task 1.5.3 |
| 328 | `KronosWaveSequence.cs` | Kronos wave sequence | Kronos wave sequence data | ❌ Missing | Task 1.5.1 |
| 329 | `KronosWaveSequenceBank.cs` | Kronos wave sequence bank | Kronos wave sequence bank | ❌ Missing | Task 1.5.1 |
| 330 | `KronosWaveSequenceBanks.cs` | Kronos wave sequence banks | Kronos wave sequence banks collection | ❌ Missing | Task 1.5.1 |

---

## Model/KronosOasysSpecific/ (Shared Kronos/Oasys - 23 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 331-353 | Various | Shared Kronos/Oasys code | Common implementation | ✅ `models.py` | - |

---

## Model/OasysSpecific/ (SECONDARY - 23 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 354-376 | Various | Oasys-specific code | Oasys implementation | ✅ `models.py` | - |

---

## Model/M3Specific/ (SECONDARY - 23 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 377-399 | Various | M3-specific code | M3 implementation | ✅ `models.py` | - |

---

## Model/M50Specific/ (SECONDARY - 23 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 400-422 | Various | M50-specific code | M50 implementation | ✅ `models.py` | - |

---

## Model/KromeSpecific/ (SECONDARY - 23 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 423-445 | Various | Krome-specific code | Krome implementation | ✅ `models.py` | - |

---

## Model/KromeExSpecific/ (SECONDARY - 23 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 446-468 | Various | Krome EX-specific code | Krome EX implementation | ✅ `models.py` | - |

---

## Model/KrossSpecific/ (SECONDARY - 21 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 469-489 | Various | Kross-specific code | Kross implementation | ✅ `models.py` | - |

---

## Model/Kross2Specific/ (SECONDARY - 21 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 490-510 | Various | Kross 2-specific code | Kross 2 implementation | ✅ `models.py` | - |

---

## Model/TrinitySpecific/ (SECONDARY - 19 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 511-529 | Various | Trinity-specific code | Trinity implementation | ✅ `models.py` | - |

---

## Model/TritonSpecific/ (SECONDARY - 17 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 530-546 | Various | Triton-specific code | Triton implementation | ✅ `models.py` | - |

---

## Model/TritonLeSpecific/ (SECONDARY - 21 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 547-567 | Various | Triton LE-specific code | Triton LE implementation | ✅ `models.py` | - |

---

## Model/TritonExtremeSpecific/ (SECONDARY - 21 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 568-588 | Various | Triton Extreme-specific code | Triton Extreme implementation | ✅ `models.py` | - |

---

## Model/TritonKarmaSpecific/ (SECONDARY - 21 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 589-609 | Various | Karma-specific code | Karma implementation | ✅ `models.py` | - |

---

## Model/TritonTrClassicStudioRackSpecific/ (SECONDARY - 23 files)

| # | File | Purpose | Features | Python Status | Task |
|---|------|---------|----------|---------------|------|
| 610-632 | Various | Triton TR/Classic/Studio/Rack code | TR variants implementation | ✅ `models.py` | - |

---

## LOW PRIORITY MODELS (Not Implemented in Python)

### Model/M1Specific/ (11 files)
| # | File | Purpose | Python Status |
|---|------|---------|---------------|
| 633-643 | M1 SysEx support | ❌ LOW PRIORITY |

### Model/M3rSpecific/ (17 files)
| # | File | Purpose | Python Status |
|---|------|---------|---------------|
| 644-660 | M3R SysEx support | ❌ LOW PRIORITY |

### Model/MSpecific/ (17 files)
| # | File | Purpose | Python Status |
|---|------|---------|---------------|
| 661-677 | M series support | ❌ LOW PRIORITY |

### Model/MicroKorgXlSpecific/ (13 files)
| # | File | Purpose | Python Status |
|---|------|---------|---------------|
| 678-690 | MicroKorg XL support | ❌ LOW PRIORITY |

### Model/MicroStationSpecific/ (19 files)
| # | File | Purpose | Python Status |
|---|------|---------|---------------|
| 691-709 | MicroStation support | ❌ LOW PRIORITY |

### Model/MntxSeriesSpecific/ (13 files)
| # | File | Purpose | Python Status |
|---|------|---------|---------------|
| 710-722 | Mntx series support | ❌ LOW PRIORITY |

### Model/Ms2000Specific/ (11 files)
| # | File | Purpose | Python Status |
|---|------|---------|---------------|
| 723-733 | MS2000 support | ❌ LOW PRIORITY |

### Model/TSeries/ (13 files)
| # | File | Purpose | Python Status |
|---|------|---------|---------------|
| 734-746 | T1/T2/T3 support | ❌ LOW PRIORITY |

### Model/XSeries/ (13 files)
| # | File | Purpose | Python Status |
|---|------|---------|---------------|
| 747-759 | X series support | ❌ LOW PRIORITY |

### Model/Z1Specific/ (13 files)
| # | File | Purpose | Python Status |
|---|------|---------|---------------|
| 760-772 | Z1 support | ❌ LOW PRIORITY |

### Model/Zero3Rw/ (15 files)
| # | File | Purpose | Python Status |
|---|------|---------|---------------|
| 773-787 | 03R/W support | ❌ LOW PRIORITY |

### Model/ZeroSeries/ (13 files)
| # | File | Purpose | Python Status |
|---|------|---------|---------------|
| 788-800 | 0 series support | ❌ LOW PRIORITY |

---

## WPF.MDI/ (Third-party MDI library - 12 files)

| # | File | Purpose | Python Status |
|---|------|---------|---------------|
| 801-812 | MDI container library | ✅ Qt MDI built-in |

---

## PCG Tools Unittests/ (51 files)

### Root Test Files
| # | File | Purpose | Python Status | Task |
|---|------|---------|---------------|------|
| 813 | `BitsUtilTest.cs` | Bit utility tests | ✅ Covered by Python tests | - |
| 814 | `CommandLineArgumentTest.cs` | CLI argument tests | ✅ Covered by Python tests | - |
| 815 | `StringUtilsTest.cs` | String utility tests | ✅ Covered by Python tests | - |
| 816 | `KronosCompletePcgPatchListTest.cs` | Kronos patch list tests | ✅ Covered by Python tests | - |
| 817 | `KronosCompletePcgCombiContentListCompactTest.cs` | Kronos combi content tests | ✅ Covered by Python tests | - |
| 818 | `KronosCompletePcgCombiContentListLongTest.cs` | Kronos combi content (long) tests | ✅ Covered by Python tests | - |
| 819 | `KronosCompletePcgDifferencesListTest.cs` | Kronos differences tests | ✅ Covered by Python tests | - |
| 820 | `KronosCompletePcgProgramUsageListTest.cs` | Kronos program usage tests | ✅ Covered by Python tests | - |
| 821 | `KronosPartialPcgTest.cs` | Kronos partial PCG tests | ⚠️ Partial (master files) | Task 1.2 |
| 822 | `SngFilesTest.cs` | SNG file tests | ❌ Missing | Task 6.1 |
| 823 | `OasysTest.cs` | Oasys tests | ✅ Covered by Python tests | - |
| 824 | `M3Test.cs` | M3 tests | ✅ Covered by Python tests | - |
| 825 | `M50Test.cs` | M50 tests | ✅ Covered by Python tests | - |
| 826 | `M1Tests.cs` | M1 tests | ❌ LOW PRIORITY | - |
| 827 | `TritonTest.cs` | Triton tests | ✅ Covered by Python tests | - |

### Anti Crash Tests/ (28 files)
| # | File | Purpose | Python Status |
|---|------|---------|---------------|
| 828 | `Base.cs` | Base anti-crash test | ✅ Covered |
| 829 | `Kronos.cs` | Kronos anti-crash | ✅ Covered |
| 830 | `Kronos2.cs` | Kronos 2 anti-crash | ✅ Covered |
| 831-855 | Various model tests | Anti-crash tests for each model | ⚠️ Partial |

### Copy and Paste Tests/ (2 files)
| # | File | Purpose | Python Status | Task |
|---|------|---------|---------------|------|
| 856 | `CopyBetweenFilesTests.cs` | Copy between files tests | ✅ Covered | - |
| 857 | `SettingsLikeNamedTests.cs` | Settings tests | ⚠️ Partial | Task 4.3 |

### Tools Tests/ (2 files)
| # | File | Purpose | Python Status | Task |
|---|------|---------|---------------|------|
| 858 | `ReferenceChangerTests.cs` | Reference changer tests | ❌ Missing | Task 1.1 |
| 859 | `RuleParserTests.cs` | Rule parser tests | ❌ Missing | Task 1.1 |

---

## Common/ Library (22 files)

| # | File | Purpose | Python Status |
|---|------|---------|---------------|
| 860 | `BoolExtensions.cs` | Boolean extensions | ✅ Built-in Python |
| 861-863 | `Behaviors/*.cs` | WPF behaviors | ✅ Qt equivalent |
| 864-865 | `Controls/*.cs` | Extended controls | ✅ Qt equivalent |
| 866-868 | `Extensions/*.cs` | String/checkbox extensions | ✅ Built-in Python |
| 869-875 | `Mvvm/*.cs` | MVVM framework | ✅ Qt signals/slots |
| 876-880 | `Utils/*.cs` | Utilities (BitsUtil, FileUtils, etc.) | ✅ `bit_utils.py` |

---

## Other Projects (Not Core - 19 files)

### PatchDatabaseBackEnd/ (4 files)
| # | File | Purpose | Python Status |
|---|------|---------|---------------|
| 881-884 | Database backend | ❌ Not needed (separate project) |

### PatchDbFrontEnd/ (5 files)
| # | File | Purpose | Python Status |
|---|------|---------|---------------|
| 885-889 | Database frontend | ❌ Not needed (separate project) |

### ExternalUtilities/ (10 files)
| # | File | Purpose | Python Status |
|---|------|---------|---------------|
| 890-899 | Development utilities | ❌ Not needed (dev tools) |

---

# SUMMARY

## Total Files: 952 source files (895 .cs + 57 .xaml)

## Implementation Status by Category:

| Category | Total Files | Implemented | Missing | Low Priority |
|----------|-------------|-------------|---------|--------------|
| **KorgKronosTools Root** | 22 | 16 | 4 | 2 |
| **ClipBoard** | 18 | 14 | 4 | 0 |
| **Common (KorgKronosTools)** | 2 | 2 | 0 | 0 |
| **Edit** | 19 | 10 | 7 | 2 |
| **Gui** | 6 | 4 | 2 | 0 |
| **Help** | 21 | 2 | 19 | 0 |
| **ListGenerator** | 10 | 8 | 2 | 0 |
| **MasterFiles** | 5 | 0 | 5 | 0 |
| **Tools** | 5 | 0 | 5 | 0 |
| **OpenedFiles** | 2 | 2 | 0 | 0 |
| **Windows** | 2 | 2 | 0 | 0 |
| **ViewModels** | 14 | 10 | 4 | 0 |
| **ViewModels/Commands** | 8 | 4 | 4 | 0 |
| **ViewModels/Converters** | 1 | 1 | 0 | 0 |
| **ViewModels/ParameterChange** | 2 | 0 | 2 | 0 |
| **Properties** | 4 | 3 | 0 | 1 |
| **PcgToolsResources** | 16 | 0 | 0 | 16 |
| **Model/Common** | 146 | 126 | 20 | 0 |
| **Model/KronosSpecific** | 28 | 19 | 9 | 0 |
| **Model/KronosOasysSpecific** | 23 | 23 | 0 | 0 |
| **Model/Secondary (Oasys, M3, Triton, etc.)** | 228 | 228 | 0 | 0 |
| **Model/Low Priority (SysEx models)** | 222 | 0 | 0 | 222 |
| **Common Library** | 22 | 22 | 0 | 0 |
| **PCG Tools Unittests** | 51 | 40 | 5 | 6 |
| **WPF.MDI** | 30 | 30 | 0 | 0 |
| **Other Projects** | 19 | 0 | 0 | 19 |
| **TOTAL** | **952** | **~586** | **~80** | **~286** |

## Missing Features Summary (HIGH/MEDIUM Priority):

### HIGH PRIORITY (Core Kronos Features)
1. **Program Reference Changer** (5 files) - Task 1.1
2. **Master Files Support** (5 files) - Task 1.2
3. **Number of References Column** (2 files) - Task 1.3
4. **Batch Volume Change** (2 files) - Task 1.4
5. **Wave Sequences/Drum Kits/Drum Patterns** (18 files) - Task 1.5
6. **CRC Values for Comparison** (2 files) - Task 1.6
7. **File Content List Generator** (1 file) - Task 2.1

### MEDIUM PRIORITY (Nice to Have)
8. **SNG File Support** (15 files) - Task 6.x
9. **Multiple Edit Dialogs** (6 files) - Task 5.x
10. **Clipboard for Drum/Wave** (4 files) - Task 3.x
11. **Advanced Settings** (10 files) - Task 4.x
12. **Cubase Export** (1 file) - Task 7.1
13. **Hex Export** (2 files) - Task 7.2

### LOW PRIORITY (Rarely Used)
14. **Help External Links** (19 files) - Task 9.5
15. **Localization Resources** (16 files) - Task 9.2
16. **Theme Support** (3 files) - Task 9.1
17. **Legacy SysEx Models** (222 files) - Not planned

## Key Files for Kronos Feature Parity

The following files are CRITICAL for complete Kronos support:

### Must Implement (HIGH)
- `Tools/ReferenceChanger.cs` - Program reference changing
- `Tools/RuleParser.cs` - Reference change rules
- `MasterFiles/MasterFile.cs` - Master file support
- `MasterFiles/MasterFiles.cs` - Master files collection
- `ListGenerator/ListGeneratorFileContentList.cs` - File content list
- `Model/KronosSpecific/Synth/KronosDrumKit*.cs` - Drum kit support
- `Model/KronosSpecific/Synth/KronosDrumPattern*.cs` - Drum pattern support
- `Model/KronosSpecific/Synth/KronosWaveSequence*.cs` - Wave sequence support
- `Model/KronosSpecific/Song/KronosSongFileReader.cs` - SNG file reading

### Should Implement (MEDIUM)
- `Edit/WindowEditMultiple*.cs` - Batch editing dialogs
- `Gui/ChangeVolumeWindow.xaml` - Volume change dialog
- `ViewModels/Commands/PcgCommands/ChangeVolumeParameters.cs` - Volume params

