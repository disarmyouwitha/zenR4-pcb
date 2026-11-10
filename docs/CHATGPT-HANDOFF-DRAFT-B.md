# Current ChatGPT handoff — Nano Independent, Draft B

Updated 2026-11-09. This supersedes the old single-Zen-case plan and the interrupted two-project proposal. The owner will ask Darryl about an original spare PCB for their Zen. **Integrated replacement development is set aside.** We are building our own nice!nano keyboard and new case, using the 42-key Choc Zen geometry as inspiration.

## Current actual revision

`projects/nano-independent/draft-b/` contains the current routed KiCad pair. `r4-layout/` remains the unchanged, electrically checked Draft A baseline, also preserved by Git tag `draft-a-baseline` at `bea6723`. Draft B has not been fabricated.

Requested and completed changes:

- Removed the old Zen USB reliefs from the rear outline. Each nice!nano supplies USB-C. Its connector position, cable boot, strain support and the new case's opening must be designed together.
- Fixed the thumb outline mismatch. An earlier right-side SW19 socket-land edge-clearance repair had added a small circle of PCB, producing the strange bump. Draft B blends that cap into a clean chamfer and mirrors both external outlines.
- Preserved every electrical item, switch center, battery cutout edge and schematic from Draft A. The native electrical-payload text hashes match. No pins, copper routes or module orientations were changed for this outline revision.

Both halves pass native KiCad ERC, DRC, unconnected and schematic parity checks with zero issues. This verifies represented rules/connectivity, not physical assembly, radio behavior or the new case. Mathematical outline geometry is mirrored; exported coordinates are rounded to micrometer-scale precision. The inherited switch grid itself has small archived-CAD left/right differences (under 0.10 mm on the main keys); no switch movement is claimed.

The old aluminum case no longer constrains solder joints, USB/reset placement, display height, viewing window, outline or mounts. Old mounting holes are retained starting references, not a final case scheme. Original user confirmations that Typeractive sockets and a nano generally fit are historical evidence; no repeat whole-Zen fit measurement is needed for our new case.

## Electrical decisions to preserve

21 keys per half; col2row diodes, stripe/cathode toward row. Physical columns are outside C0 → seam C5 on each side. Three thumbs are physical R3C3–5.

| Net | nano | GPIO | Project U1 pad |
|---|---|---|---:|
| ROW0 | D8 | P1.04 | 11 |
| ROW1 | D9 | P1.06 | 12 |
| ROW2 | D21 | P0.31 | 17 |
| ROW3 | D20 | P0.29 | 18 |
| COL0 | D19 | P0.02 | 19 |
| COL1 | D18 | P1.15 | 20 |
| COL2 | D15 | P1.13 | 21 |
| COL3 | D14 | P1.11 | 22 |
| COL4 | D0 | P0.08 | 2 |
| COL5 | D1 | P0.06 | 1 |

Right firmware scans `[COL5,COL4,COL3,COL2,COL1,COL0]`, global column offset 6. Do not reverse rows or change the keymap to fix physical naming. Socket packages are asymmetric; do not mirror complete pad patterns blindly.

Left QSPI: CS# D2/P0.17/U1-5 → U2-1; CLK D4/P0.22/U1-7 → U2-6; IO0 D5/P0.24/U1-8 → U2-5; IO1 D6/P1.00/U1-9 → U2-2; IO2 D7/P0.11/U1-10 → U2-3; IO3 D3/P0.20/U1-6 → U2-7. VCC is module switched 3V3 on U1-16 → U2-8, GND → U2-4. IO2/IO3 are data, not supply straps. Candidate flash W25Q128JVSIQ 208-mil SOIC; exact orderable part remains to be locked. C1=100 nF; R1=10 kΩ CS bias. P0.13 controls the flash rail inside the module; it is not a carrier edge connection.

The footprint numbers are our 24-edge-hole convention: component-face view, USB up, pads 1–12 left down, 13–24 right down. Because the nano mounts component-face down, in **carrier top view pad 1/D1 is RIGHT**, pad 13/RAW-B+ LEFT. Check the actual module and soldering method; a mirrored-bank error was already corrected in A.

## Target features — not yet implemented in B

- Optional left flash population: normal flash-free keyboard build with flash/support DNP; external-dictionary Javelin build with U2/C1/R1 fitted. A normal build must not require a successful QSPI probe. Inspect firmware build paths without changing/flashing working hardware.
- Right nice!view: **CS D4/P0.22 active high, MOSI D2/P0.17, SCK D3/P0.20**, supply/GND. Current B has no display footprint or connector. Its new case can provide proper viewing area, support, retention and height.
- Optional RGB status and squid artwork on either half. Proposed spare GPIOs D16/P0.10 data and D10/P0.09 enable require NFC-function and waveform-driver review. Gate RGB separately from flash/display; do not pulse the left flash supply for LED animation.
- The owner ordered WS2812C-2020-V6 (C55109522). Future LED footprint, supply tolerance, data isolation/back-power, bypass stuffing and leakage need actual schematic review. Shared feature/power calculations are proposals, not measured results or installed circuitry.
- The handed-off right RGB/display alternative-assembly preference remains the default; independent GPIO reservation leaves later combined assembly discussable without remapping the matrix.

The working hybrid keyboard is a handwired/custom Zen left plus existing Ultralight right. Its tested Javelin/QSPI/typing/Plover/Bluetooth mode-sync/display reconnect behavior is hardware evidence for that setup. Custom-right matrix and D4-CS display overlays were compile-tested, not hardware-tested. Do not flash those overlays onto the stock Ultralight. Working firmware is untouched.

## What to review next

1. Review Draft B's outline, then establish the new case's nano/display/battery stack and accessible service/USB/reset/power arrangement.
2. Choose module solder/socket method and case mounting/plug strain support. Build the case around actual component, solder and battery dimensions; old Zen base-pocket STLs are not the new case.
3. Add the actual right nice!view interface and optional independent RGB circuitry in a circuit revision; review exact package/pins, supply margin, leakage and optical/diffuser placement. Preserve the tested matrix/QSPI.
4. Review QSPI returns, decoupling, antenna clearance, flash-DNP firmware and assembly BOM before routing/fabrication. Repeat native rules/parity plus physical checks; then a small prototype build and measured bring-up.

No Gerber production release, hardware order, public release or original hardware modification is approved by this handoff.

## Files to use

- `projects/nano-independent/draft-b/README.md`, `layout-preview.png`, `thumb-before-after.png`.
- The `zen-r4-*.kicad_pro/.kicad_sch/.kicad_pcb` in that directory, with checks and new 1:1 SVG / bare-board STLs under `mechanical/`.
- `projects/shared/pin-contract.json`, `FEATURES.md`, `rgb-budget.json`, `SOURCES.md` for the future feature proposal and explicitly calculated estimates.
- `docs/CHATGPT-HANDOFF-DRAFT-A.md` is historical only. Old Zen-port/reset/no-integrated instructions there are superseded.

Darryl's CAD and derived geometry retain restrictive attribution/noncommercial/no-derivatives notices. The repository remains private. A new case identity does not automatically make inherited outline/CAD freely redistributable; independently authored electronics/art and restricted reference assets must be separated before public release.

Conversation starter: “Read this Nano Independent Draft B handoff and images. Help me design our own case and next nice!view/RGB circuit revision around the checked carrier. Keep matrix and QSPI pins, treat old Zen case restrictions as retired, and distinguish completed outline changes from planned circuits and hardware tests.”
