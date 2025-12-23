# Design Document

## Overview

This is a manual hardware verification test plan. Tests are performed by a human tester using PCG Tools GUI and a physical Korg Kronos synthesizer.

## Architecture

No code changes required. This is a verification-only spec.

## Test Workflow

1. Open PCG file in PCG Tools
2. Make specified edit
3. Save file
4. Copy to USB/SD card
5. Load on Kronos
6. Verify change appears correctly
7. Mark test as passed/failed

## Components and Interfaces

- **PCG Tools GUI**: `python3 -m pcg_tools.gui_qt`
- **Kronos Hardware**: Physical synthesizer
- **Transfer Medium**: USB drive or SD card mounted at `/Volumes/KEYBOARD/`

## Data Models

N/A - Manual testing only

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system.*

Property 1: File Integrity
*For any* PCG file edited by PCG Tools, loading on Kronos SHALL succeed without errors
**Validates: Requirements 1.1, 1.2**

Property 2: Edit Persistence  
*For any* edit made in PCG Tools and saved, the change SHALL be visible on Kronos after loading
**Validates: Requirements 2.1-2.3, 3.1-3.2, 4.1-4.4, 5.1-5.6**

## Error Handling

If a test fails:
1. Note the exact error message from Kronos
2. Note what was changed in PCG Tools
3. Try loading the original unmodified file to verify hardware works
4. Report the failure with details

## Testing Strategy

All tests are manual hardware verification tests. Each test follows the workflow above.
