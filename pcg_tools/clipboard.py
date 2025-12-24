"""Clipboard functionality for copying/pasting patches with program remapping."""

from typing import Optional, List, Dict, Set
from copy import deepcopy
from enum import Enum
from .models import Combi, Program, Timbre, SetListSlot, DrumKit, WaveSequence, SynthesisType


class CopyType(Enum):
    """Type of content in clipboard. Based on C# PcgClipBoard.CopyType enum."""
    PROGRAMS = "Programs"
    COMBIS = "Combis"
    SET_LIST_SLOTS = "SetListSlots"
    DRUM_KITS = "DrumKits"
    DRUM_PATTERNS = "DrumPatterns"
    WAVE_SEQUENCES = "WaveSequences"


def program_may_use_user_samples(program: Program) -> bool:
    """Check if a program might use user samples.
    
    User samples are stored in KSC files and must be loaded separately.
    Programs from User banks (U-A through U-GG) are more likely to use user samples.
    HD-1 programs can reference user multisamples.
    
    Returns True if the program might use user samples that need to be loaded separately.
    """
    if not program or not program.id:
        return False
    
    # Check if program is from a User bank (more likely to use user samples)
    prog_id = program.id
    if prog_id.startswith("U-") or prog_id.startswith("USER-"):
        return True
    
    return False


def get_user_sample_warning(programs: List[Program]) -> Optional[str]:
    """Get a warning message if any programs might use user samples.
    
    Returns a warning string if user samples might be needed, None otherwise.
    """
    user_sample_programs = []
    for prog in programs:
        if program_may_use_user_samples(prog):
            user_sample_programs.append(prog.name if prog.name else prog.id)
    
    if not user_sample_programs:
        return None
    
    if len(user_sample_programs) == 1:
        return (f"The program '{user_sample_programs[0]}' may use user samples.\n\n"
                "User samples are stored in KSC files and must be loaded on the "
                "destination Kronos for the program to sound correct.")
    else:
        prog_list = ", ".join(user_sample_programs[:5])
        if len(user_sample_programs) > 5:
            prog_list += f" and {len(user_sample_programs) - 5} more"
        return (f"The following programs may use user samples:\n{prog_list}\n\n"
                "User samples are stored in KSC files and must be loaded on the "
                "destination Kronos for these programs to sound correct.")


class ClipBoardPatch:
    """Wrapper for a copied patch with tracking info."""
    def __init__(self, patch, data: bytes = None):
        self.patch = patch
        self.data = data or (patch.raw_data if hasattr(patch, 'raw_data') else b'')
        self.original_location = patch
        self.paste_destination = None
        self.synthesis_type: Optional[SynthesisType] = None


class Clipboard:
    """Clipboard for patches with program reference tracking."""
    
    def __init__(self):
        self._programs_by_type: Dict[SynthesisType, List[ClipBoardPatch]] = {
            st: [] for st in SynthesisType
        }
        self.program: Optional[Program] = None
        self.programs: List[Program] = []
        self.program_map: Dict[str, Program] = {}
        self.combi: Optional[Combi] = None
        self._combis: List[ClipBoardPatch] = []
        self.slot: Optional[SetListSlot] = None
        self._set_list_slots: List[ClipBoardPatch] = []
        self.drum_kit: Optional[DrumKit] = None
        self.drum_kits: List[DrumKit] = []
        self._drum_kits: List[ClipBoardPatch] = []
        self.wave_sequence: Optional[WaveSequence] = None
        self.wave_sequences: List[WaveSequence] = []
        self._wave_sequences: List[ClipBoardPatch] = []
        self.cut_paste_selected: bool = False
        self.protected_patches: Set = set()
        self.paste_duplicates_executed: bool = False
        self.copy_file_name: Optional[str] = None
        self.paste_pcg_memory = None
        self._previous_clipboard: Optional['Clipboard'] = None

    def get_user_sample_warning(self) -> Optional[str]:
        """Get a warning if clipboard contents might use user samples.
        
        Returns a warning message if programs in the clipboard might use user samples,
        None otherwise.
        """
        programs_to_check = []
        
        # Check single program
        if self.program:
            programs_to_check.append(self.program)
        
        # Check programs from combi
        if self.programs:
            programs_to_check.extend(self.programs)
        
        return get_user_sample_warning(programs_to_check)

    @property
    def selected_copy_type(self) -> CopyType:
        if self._set_list_slots:
            return CopyType.SET_LIST_SLOTS
        if self._combis:
            return CopyType.COMBIS
        if any(progs for progs in self._programs_by_type.values()):
            return CopyType.PROGRAMS
        if self._drum_kits:
            return CopyType.DRUM_KITS
        return CopyType.WAVE_SEQUENCES

    def copy_combi(self, combi: Combi, pcg):
        self.combi = deepcopy(combi)
        self.programs = []
        self.program_map = {}
        self._combis.append(ClipBoardPatch(combi))
        referenced_program_ids = set()
        for timbre in combi.timbres:
            if timbre.status != "Off":
                referenced_program_ids.add(timbre.program_id)
        if not self.cut_paste_selected:
            for bank in pcg.program_banks:
                for program in bank.patches:
                    if program.id in referenced_program_ids:
                        prog_copy = deepcopy(program)
                        self.programs.append(prog_copy)
                        self.program_map[program.id] = prog_copy

    def paste_combi(self, target_combi: Combi, pcg, remap_programs: bool = True) -> Dict[str, str]:
        if not self.combi:
            return {}
        program_remap = {}
        if remap_programs and self.programs:
            program_remap = self._remap_programs(pcg)
        target_combi.name = self.combi.name
        target_combi.category = deepcopy(self.combi.category) if self.combi.category else None
        target_combi.favorite = self.combi.favorite
        target_combi.tempo = self.combi.tempo
        target_combi.timbres = []
        for timbre in self.combi.timbres:
            new_timbre = deepcopy(timbre)
            if remap_programs and timbre.program_id in program_remap:
                new_prog_id = program_remap[timbre.program_id]
                new_timbre.program_bank = new_prog_id[:-3]
                new_timbre.program_index = int(new_prog_id[-3:])
            target_combi.timbres.append(new_timbre)
        target_combi.raw_data = deepcopy(self.combi.raw_data)
        if self.cut_paste_selected:
            self.protected_patches.add(target_combi)
        return program_remap

    def _remap_programs(self, pcg) -> Dict[str, str]:
        program_remap = {}
        existing_programs = set()
        for bank in pcg.program_banks:
            for program in bank.patches:
                existing_programs.add(program.id)
        for old_program in self.programs:
            old_id = old_program.id
            for bank in pcg.program_banks:
                for program in bank.patches:
                    if program.name == old_program.name and program.id in existing_programs:
                        program_remap[old_id] = program.id
                        break
                if old_id in program_remap:
                    break
            if old_id not in program_remap:
                new_slot = self._find_empty_program_slot(pcg)
                if new_slot:
                    bank_id, index = new_slot
                    for bank in pcg.program_banks:
                        if bank.bank_id == bank_id:
                            if index < len(bank.patches):
                                target_program = bank.patches[index]
                                target_program.name = old_program.name
                                target_program.category = deepcopy(old_program.category)
                                target_program.favorite = old_program.favorite
                                target_program.engine = old_program.engine
                                target_program.osc_mode = old_program.osc_mode
                                target_program.raw_data = deepcopy(old_program.raw_data)
                                new_id = f"{bank_id}{index:03d}"
                                program_remap[old_id] = new_id
                                existing_programs.add(new_id)
                            break
        return program_remap

    def _find_empty_program_slot(self, pcg) -> Optional[tuple]:
        for bank in pcg.program_banks:
            for i, program in enumerate(bank.patches):
                if program.name.startswith("Init") or program.name.startswith("[Empty") or program.name.strip() == "":
                    return (bank.bank_id, i)
        return None

    def copy_slot(self, slot: SetListSlot):
        self.slot = deepcopy(slot)
        self._set_list_slots.append(ClipBoardPatch(slot))

    def paste_slot(self, target_slot: SetListSlot):
        if not self.slot:
            return
        target_slot.name = self.slot.name
        target_slot.notes = self.slot.notes
        target_slot.patch_type = self.slot.patch_type
        target_slot.patch_bank = self.slot.patch_bank
        target_slot.patch_index = self.slot.patch_index
        target_slot.transpose = self.slot.transpose
        target_slot.volume = self.slot.volume
        target_slot.hold = self.slot.hold
        target_slot.color = self.slot.color
        target_slot._text_size = self.slot._text_size
        target_slot._description = self.slot._description
        if self.slot.raw_data:
            target_slot.raw_data = deepcopy(self.slot.raw_data)
            if len(target_slot.raw_data) >= 24:
                name_bytes = target_slot.name.encode('ascii', errors='ignore')[:24]
                name_bytes = name_bytes.ljust(24, b'\x00')
                target_slot.raw_data[0:24] = name_bytes
        if self.cut_paste_selected:
            self.protected_patches.add(target_slot)

    def copy_program(self, program: Program, synthesis_type: SynthesisType = None):
        self.program = deepcopy(program)
        if synthesis_type:
            cb_patch = ClipBoardPatch(program)
            cb_patch.synthesis_type = synthesis_type
            self._programs_by_type[synthesis_type].append(cb_patch)

    def paste_program(self, target_program: Program):
        if not self.program:
            return
        target_program.name = self.program.name
        target_program.category = deepcopy(self.program.category) if self.program.category else None
        target_program.favorite = self.program.favorite
        target_program.engine = self.program.engine
        target_program.osc_mode = self.program.osc_mode
        if self.program.raw_data:
            target_program.raw_data = deepcopy(self.program.raw_data)
        if self.cut_paste_selected:
            self.protected_patches.add(target_program)

    def has_combi(self) -> bool:
        return self.combi is not None

    def has_slot(self) -> bool:
        return self.slot is not None

    def has_program(self) -> bool:
        return self.program is not None

    def find_program(self, program_to_find: Program) -> Optional[ClipBoardPatch]:
        for synthesis_type, programs in self._programs_by_type.items():
            for cb_patch in programs:
                if cb_patch.data == program_to_find.raw_data:
                    return cb_patch
        return None

    def fix_references_to_program(self, pasted_patch: ClipBoardPatch, program: Program, pcg):
        if not self.cut_paste_selected:
            return
        original = pasted_patch.original_location
        for bank in pcg.combi_banks:
            if bank.is_read_only:
                continue
            for combi in bank.patches:
                for timbre in combi.timbres:
                    if timbre.program_id == original.id:
                        timbre.program_bank = program.bank
                        timbre.program_index = program.index
        for setlist in pcg.set_lists:
            for slot in setlist.slots:
                if slot.patch_type == "Program" and slot.patch_id == original.id:
                    slot.patch_bank = program.bank
                    slot.patch_index = program.index

    def fix_references_to_combi(self, pasted_patch: ClipBoardPatch, combi: Combi, pcg):
        if not self.cut_paste_selected:
            return
        original = pasted_patch.original_location
        for setlist in pcg.set_lists:
            for slot in setlist.slots:
                if slot.patch_type == "Combi" and slot.patch_id == original.id:
                    slot.patch_bank = combi.bank
                    slot.patch_index = combi.index

    def copy_drum_kit(self, drum_kit: DrumKit):
        self.drum_kit = deepcopy(drum_kit)
        self._drum_kits.append(ClipBoardPatch(drum_kit))

    def copy_drum_kits(self, drum_kits: List[DrumKit]):
        self.drum_kits = [deepcopy(dk) for dk in drum_kits]
        for dk in drum_kits:
            self._drum_kits.append(ClipBoardPatch(dk))

    def paste_drum_kit(self, target_drum_kit: DrumKit):
        if not self.drum_kit:
            return
        target_drum_kit.name = self.drum_kit.name
        if self.drum_kit.raw_data:
            target_drum_kit.raw_data = deepcopy(self.drum_kit.raw_data)
        if self.cut_paste_selected:
            self.protected_patches.add(target_drum_kit)

    def has_drum_kit(self) -> bool:
        return self.drum_kit is not None or len(self.drum_kits) > 0

    def find_drum_kit(self, drum_kit_to_find: DrumKit) -> Optional[ClipBoardPatch]:
        for cb_patch in self._drum_kits:
            if cb_patch.data == drum_kit_to_find.raw_data:
                return cb_patch
        return None

    def copy_wave_sequence(self, wave_sequence: WaveSequence):
        self.wave_sequence = deepcopy(wave_sequence)
        self._wave_sequences.append(ClipBoardPatch(wave_sequence))

    def copy_wave_sequences(self, wave_sequences: List[WaveSequence]):
        self.wave_sequences = [deepcopy(ws) for ws in wave_sequences]
        for ws in wave_sequences:
            self._wave_sequences.append(ClipBoardPatch(ws))

    def paste_wave_sequence(self, target_wave_sequence: WaveSequence):
        if not self.wave_sequence:
            return
        target_wave_sequence.name = self.wave_sequence.name
        if self.wave_sequence.raw_data:
            target_wave_sequence.raw_data = deepcopy(self.wave_sequence.raw_data)
        if self.cut_paste_selected:
            self.protected_patches.add(target_wave_sequence)

    def has_wave_sequence(self) -> bool:
        return self.wave_sequence is not None or len(self.wave_sequences) > 0

    def memorize(self):
        self._previous_clipboard = Clipboard()
        if self.program:
            self._previous_clipboard.program = deepcopy(self.program)
        self._previous_clipboard.programs = [deepcopy(p) for p in self.programs]
        self._previous_clipboard.program_map = {k: deepcopy(v) for k, v in self.program_map.items()}
        if self.combi:
            self._previous_clipboard.combi = deepcopy(self.combi)
        if self.slot:
            self._previous_clipboard.slot = deepcopy(self.slot)
        if self.drum_kit:
            self._previous_clipboard.drum_kit = deepcopy(self.drum_kit)
        self._previous_clipboard.drum_kits = [deepcopy(dk) for dk in self.drum_kits]
        if self.wave_sequence:
            self._previous_clipboard.wave_sequence = deepcopy(self.wave_sequence)
        self._previous_clipboard.wave_sequences = [deepcopy(ws) for ws in self.wave_sequences]
        self.protected_patches = set()

    def recall(self):
        if not self._previous_clipboard:
            return
        self.program = deepcopy(self._previous_clipboard.program) if self._previous_clipboard.program else None
        self.programs = [deepcopy(p) for p in self._previous_clipboard.programs]
        self.program_map = {k: deepcopy(v) for k, v in self._previous_clipboard.program_map.items()}
        self.combi = deepcopy(self._previous_clipboard.combi) if self._previous_clipboard.combi else None
        self.slot = deepcopy(self._previous_clipboard.slot) if self._previous_clipboard.slot else None
        self.drum_kit = deepcopy(self._previous_clipboard.drum_kit) if self._previous_clipboard.drum_kit else None
        self.drum_kits = [deepcopy(dk) for dk in self._previous_clipboard.drum_kits]
        self.wave_sequence = deepcopy(self._previous_clipboard.wave_sequence) if self._previous_clipboard.wave_sequence else None
        self.wave_sequences = [deepcopy(ws) for ws in self._previous_clipboard.wave_sequences]
        self.protected_patches = set()

    def has_memory(self) -> bool:
        if not self._previous_clipboard:
            return False
        return (
            self._previous_clipboard.program is not None or
            len(self._previous_clipboard.programs) > 0 or
            self._previous_clipboard.combi is not None or
            self._previous_clipboard.slot is not None or
            self._previous_clipboard.drum_kit is not None or
            len(self._previous_clipboard.drum_kits) > 0 or
            self._previous_clipboard.wave_sequence is not None or
            len(self._previous_clipboard.wave_sequences) > 0
        )

    def exit_copy_paste_mode(self):
        self.clear()
        self._previous_clipboard = None
        self.cut_paste_selected = False
        self.protected_patches = set()
        self.paste_duplicates_executed = False
        self.paste_pcg_memory = None

    def clear(self):
        self.combi = None
        self.programs = []
        self.program_map = {}
        self.slot = None
        self.program = None
        self.drum_kit = None
        self.drum_kits = []
        self.wave_sequence = None
        self.wave_sequences = []
        self._combis = []
        self._set_list_slots = []
        self._drum_kits = []
        self._wave_sequences = []
        for st in SynthesisType:
            self._programs_by_type[st] = []
        self.paste_duplicates_executed = False
        self.paste_pcg_memory = None
        self.protected_patches = set()

    @property
    def is_empty(self) -> bool:
        return (
            self.program is None and
            len(self.programs) == 0 and
            self.combi is None and
            self.slot is None and
            self.drum_kit is None and
            len(self.drum_kits) == 0 and
            self.wave_sequence is None and
            len(self.wave_sequences) == 0
        )

    @property
    def is_pasting_finished(self) -> bool:
        for programs in self._programs_by_type.values():
            for cb_patch in programs:
                if cb_patch.paste_destination is None:
                    return False
        for cb_patch in self._combis:
            if cb_patch.paste_destination is None:
                return False
        for cb_patch in self._set_list_slots:
            if cb_patch.paste_destination is None:
                return False
        for cb_patch in self._drum_kits:
            if cb_patch.paste_destination is None:
                return False
        for cb_patch in self._wave_sequences:
            if cb_patch.paste_destination is None:
                return False
        return True


_clipboard = Clipboard()


def get_clipboard() -> Clipboard:
    return _clipboard
