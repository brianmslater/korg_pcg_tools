# GM2 Banks Quick Reference

## Overview

GM2 (General MIDI Level 2) banks provide additional sound variations beyond the standard GM bank. These are ROM banks on the Kronos hardware and are displayed as read-only in PCG Tools.

## Bank List

### g(1) - Piano Variations
- g(1)000: Grand Piano KSP
- g(1)001: Grand Piano
- g(1)002: Piano Strings
- g(1)003: Dream
- g(1)004: Bright Piano
- g(1)005: Piano Strings 2
- g(1)006: Piano Strings 3
- g(1)007: Piano Strings 4
- g(1)008-127: Additional variations

### g(2) - Chromatic Percussion
- g(2)000: Celesta
- g(2)001: Glockenspiel
- g(2)002: Music Box
- g(2)003: Vibraphone
- g(2)004: Marimba
- g(2)005: Xylophone
- g(2)006: Tubular Bells
- g(2)007: Dulcimer
- g(2)008-127: Additional variations

### g(3) - Organ Variations
- g(3)000: Drawbar Organ
- g(3)001: Percussive Organ
- g(3)002: Rock Organ
- g(3)003: Church Organ
- g(3)004: Reed Organ
- g(3)005: Accordion
- g(3)006: Harmonica
- g(3)007: Tango Accordion
- g(3)008-127: Additional variations

### g(4) - Guitar Variations
- g(4)000: Nylon Guitar
- g(4)001: Steel Guitar
- g(4)002: Jazz Guitar
- g(4)003: Clean Guitar
- g(4)004: Muted Guitar
- g(4)005: Overdrive Guitar
- g(4)006: Distortion Guitar
- g(4)007: Guitar Harmonics
- g(4)008-127: Additional variations

### g(5) - Bass Variations
- g(5)000: Acoustic Bass
- g(5)001: Fingered Bass
- g(5)002: Picked Bass
- g(5)003: Fretless Bass
- g(5)004: Slap Bass 1
- g(5)005: Slap Bass 2
- g(5)006: Synth Bass 1
- g(5)007: Synth Bass 2
- g(5)008-127: Additional variations

### g(6) - Strings/Orchestra
- g(6)000: Violin
- g(6)001: Viola
- g(6)002: Cello
- g(6)003: Contrabass
- g(6)004: Tremolo Strings
- g(6)005: Pizzicato Strings
- g(6)006: Orchestral Harp
- g(6)007: Timpani
- g(6)008-127: Additional variations

### g(7) - Ensemble
- g(7)000: String Ensemble 1
- g(7)001: String Ensemble 2
- g(7)002: Synth Strings 1
- g(7)003: Synth Strings 2
- g(7)004: Choir Aahs
- g(7)005: Voice Oohs
- g(7)006: Synth Voice
- g(7)007: Orchestra Hit
- g(7)008-127: Additional variations

### g(8) - Brass
- g(8)000: Trumpet
- g(8)001: Trombone
- g(8)002: Tuba
- g(8)003: Muted Trumpet
- g(8)004: French Horn
- g(8)005: Brass Section
- g(8)006: Synth Brass 1
- g(8)007: Synth Brass 2
- g(8)008-127: Additional variations

### g(9) - Reed/Pipe
- g(9)000: Soprano Sax
- g(9)001: Alto Sax
- g(9)002: Tenor Sax
- g(9)003: Baritone Sax
- g(9)004: Oboe
- g(9)005: English Horn
- g(9)006: Bassoon
- g(9)007: Clarinet
- g(9)008-127: Additional variations

### g(d) - Drum Kits
- g(d)000: Standard Kit
- g(d)001: Standard Kit 2
- g(d)008: Room Kit
- g(d)016: Power Kit
- g(d)024: Electronic Kit
- g(d)025: TR-808 Kit
- g(d)032: Jazz Kit
- g(d)040: Brush Kit
- g(d)048: Orchestra Kit
- g(d)056: SFX Kit
- g(d)127: CM-64/CM-32L

## Usage Notes

1. **Read-Only**: These banks cannot be edited. They are ROM banks stored in the Kronos firmware.

2. **Display Only**: PCG Tools displays these banks with program names for reference, but they are not stored in PCG files.

3. **Copy Operations**: You can copy programs from GM2 banks to user banks, but you cannot paste into GM2 banks.

4. **Naming Convention**: Programs without specific names are displayed with their bank and index (e.g., "g(1)008").

5. **Engine Type**: All GM2 programs show "GM2" as their engine type.

6. **Oscillator Mode**: 
   - g(1)-g(9): "Single" oscillator mode
   - g(d): "Drums" oscillator mode

## Testing

To verify GM2 banks are working correctly:

```bash
cd korg_pcg_tools
python3 test_gm2_banks.py test_files/soundcheck11242025.PCG
python3 test_gm_readonly.py test_files/soundcheck11242025.PCG
```

## References

- GM2 Specification: General MIDI Level 2
- Korg Kronos Parameter Guide
- PCG Tools Documentation: `GM_BANKS_IMPLEMENTATION.md`
