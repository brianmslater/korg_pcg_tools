"""GM2 (General MIDI Level 2) bank definitions.

These banks are ROM banks on the Kronos hardware and are not stored in PCG files.
They provide additional sound variations beyond the standard GM bank.

References:
- GM2 Specification (General MIDI Level 2)
- Korg Kronos Parameter Guide
"""

# GM Category mappings (main_category, sub_category)
# Based on standard GM instrument categories
GM2_CATEGORIES = {
    "Piano": (0, 0),
    "Chromatic Percussion": (1, 0),
    "Organ": (2, 0),
    "Guitar": (3, 0),
    "Bass": (4, 0),
    "Strings": (5, 0),
    "Ensemble": (6, 0),
    "Brass": (7, 0),
    "Reed": (8, 0),
    "Pipe": (9, 0),
    "Synth Lead": (10, 0),
    "Synth Pad": (11, 0),
    "Synth Effects": (12, 0),
    "Ethnic": (13, 0),
    "Percussive": (14, 0),
    "Sound Effects": (15, 0),
    "Drums": (16, 0),
}

# GM2 Drum Kits (g(d) bank)
# Based on GM2 specification
GM2_DRUM_KITS = {
    0: "Standard Kit",
    1: "Standard Kit 2",
    8: "Room Kit",
    16: "Power Kit",
    24: "Electronic Kit",
    25: "TR-808 Kit",
    32: "Jazz Kit",
    40: "Brush Kit",
    48: "Orchestra Kit",
    56: "SFX Kit",
    127: "CM-64/CM-32L",
}

# GM2 Main Program Banks g(1) through g(9)
# These provide variations of the standard GM programs
# Each bank contains 128 programs (0-127)

# g(1) - Piano variations (GM2 Bank MSB 121)
GM2_G1_PROGRAMS = {
    0: "Grand Piano KSP",
    1: "Grand Piano",
    2: "Piano Strings",
    3: "Dream",
    4: "Bright Piano",
    5: "Piano Strings 2",
    6: "Piano Strings 3",
    7: "Piano Strings 4",
    8: "Electric Grand Piano",
    16: "Honky-tonk Piano",
    24: "Electric Piano 1",
    25: "Electric Piano 2",
    32: "Harpsichord",
    40: "Clavi",
}

# g(2) - Chromatic Percussion variations (GM2 Bank MSB 121)
GM2_G2_PROGRAMS = {
    8: "Celesta",
    9: "Glockenspiel",
    10: "Music Box",
    11: "Vibraphone",
    12: "Marimba",
    13: "Xylophone",
    14: "Tubular Bells",
    15: "Dulcimer",
    16: "Drawbar Organ",
    17: "Percussive Organ",
    18: "Rock Organ",
}

# g(3) - Organ variations (GM2 Bank MSB 121)
GM2_G3_PROGRAMS = {
    16: "Drawbar Organ",
    17: "Percussive Organ",
    18: "Rock Organ",
    19: "Church Organ",
    20: "Reed Organ",
    21: "Accordion",
    22: "Harmonica",
    23: "Tango Accordion",
}

# g(4) - Guitar variations (GM2 Bank MSB 121)
GM2_G4_PROGRAMS = {
    24: "Nylon Guitar",
    25: "Steel Guitar",
    26: "Jazz Guitar",
    27: "Clean Guitar",
    28: "Muted Guitar",
    29: "Overdrive Guitar",
    30: "Distortion Guitar",
    31: "Guitar Harmonics",
}

# g(5) - Bass variations (GM2 Bank MSB 121)
GM2_G5_PROGRAMS = {
    32: "Acoustic Bass",
    33: "Fingered Bass",
    34: "Picked Bass",
    35: "Fretless Bass",
    36: "Slap Bass 1",
    37: "Slap Bass 2",
    38: "Synth Bass 1",
    39: "Synth Bass 2",
}

# g(6) - Strings/Orchestra variations (GM2 Bank MSB 121)
GM2_G6_PROGRAMS = {
    40: "Violin",
    41: "Viola",
    42: "Cello",
    43: "Contrabass",
    44: "Tremolo Strings",
    45: "Pizzicato Strings",
    46: "Orchestral Harp",
    47: "Timpani",
}

# g(7) - Ensemble variations (GM2 Bank MSB 121)
GM2_G7_PROGRAMS = {
    48: "String Ensemble 1",
    49: "String Ensemble 2",
    50: "Synth Strings 1",
    51: "Synth Strings 2",
    52: "Choir Aahs",
    53: "Voice Oohs",
    54: "Synth Voice",
    55: "Orchestra Hit",
}

# g(8) - Brass variations (GM2 Bank MSB 121)
GM2_G8_PROGRAMS = {
    56: "Trumpet",
    57: "Trombone",
    58: "Tuba",
    59: "Muted Trumpet",
    60: "French Horn",
    61: "Brass Section",
    62: "Synth Brass 1",
    63: "Synth Brass 2",
}

# g(9) - Reed/Pipe variations (GM2 Bank MSB 121)
GM2_G9_PROGRAMS = {
    64: "Soprano Sax",
    65: "Alto Sax",
    66: "Tenor Sax",
    67: "Baritone Sax",
    68: "Oboe",
    69: "English Horn",
    70: "Bassoon",
    71: "Clarinet",
    72: "Piccolo",
    73: "Flute",
    74: "Recorder",
    75: "Pan Flute",
    76: "Blown Bottle",
    77: "Shakuhachi",
    78: "Whistle",
    79: "Ocarina",
}

# Map bank IDs to their program definitions
GM2_BANK_PROGRAMS = {
    "g(1)": GM2_G1_PROGRAMS,
    "g(2)": GM2_G2_PROGRAMS,
    "g(3)": GM2_G3_PROGRAMS,
    "g(4)": GM2_G4_PROGRAMS,
    "g(5)": GM2_G5_PROGRAMS,
    "g(6)": GM2_G6_PROGRAMS,
    "g(7)": GM2_G7_PROGRAMS,
    "g(8)": GM2_G8_PROGRAMS,
    "g(9)": GM2_G9_PROGRAMS,
    "g(d)": GM2_DRUM_KITS,
}


def get_gm2_program_name(bank_id: str, index: int) -> str:
    """Get the name of a GM2 program.
    
    Args:
        bank_id: Bank ID (e.g., "g(1)", "g(d)")
        index: Program index (0-127)
    
    Returns:
        Program name or default name if not defined
    """
    if bank_id not in GM2_BANK_PROGRAMS:
        return f"{bank_id}{index:03d}"
    
    programs = GM2_BANK_PROGRAMS[bank_id]
    if index in programs:
        return programs[index]
    
    # Return default name for undefined slots
    return f"{bank_id}{index:03d}"


def get_gm2_category(bank_id: str, index: int):
    """Get the category for a GM2 program.
    
    Args:
        bank_id: Bank ID (e.g., "g(1)", "g(d)")
        index: Program index (0-127)
    
    Returns:
        Tuple of (main_category, sub_category) or None
    """
    # Map bank to category
    category_map = {
        "g(1)": "Piano",
        "g(2)": "Chromatic Percussion",
        "g(3)": "Organ",
        "g(4)": "Guitar",
        "g(5)": "Bass",
        "g(6)": "Strings",
        "g(7)": "Ensemble",
        "g(8)": "Brass",
        "g(9)": "Reed",
        "g(d)": "Drums",
    }
    
    category_name = category_map.get(bank_id)
    if category_name and category_name in GM2_CATEGORIES:
        return GM2_CATEGORIES[category_name]
    
    return None


def is_gm2_bank(bank_id: str) -> bool:
    """Check if a bank ID is a GM2 bank.
    
    Args:
        bank_id: Bank ID to check
    
    Returns:
        True if this is a GM2 bank (g(1)-g(9) or g(d))
    """
    if bank_id == "g(d)":
        return True
    if bank_id.startswith("g(") and bank_id.endswith(")"):
        try:
            num = int(bank_id[2:-1])
            return 1 <= num <= 9
        except ValueError:
            return False
    return False
