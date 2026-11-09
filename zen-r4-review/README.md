# Zen R4 schematic review — shared matrix pinout

**Use the tested Zen left matrix pinout on both custom halves. Keep QSPI on the left; reserve D4/D2/D3 for the optional right display.** The Ultralight remains a prototype reference. The display footprint is pending a physical mounting solution, so it is absent from these schematics.

The working hardware is the handwired Zen R4 left and stock Corne Ultralight right. This review is for the new PCB. The working ZMK/Javelin split, including its mode sync and reconnect behavior, was not modified. The review is pinned to [application baseline cb3ccc8](https://github.com/disarmyouwitha/zmk-javelin-steno/tree/cb3ccc8720a496fba8d877784345c6b120a0b999) and its manifest ZMK revision `4dd95d7840eb3d5a3f59bb29fbf1ab054715ef85`. The older left-display/underside-pad proposal is outside this design.

## Current mechanical plan

Physical V2 checks now take precedence over deductions from the early archived case. The user confirms that the Typeractive Choc hotswap sockets fit the Zen backplate and the case closes after trimming the circled PCB areas. The nice!nano fits underneath with a modified plastic base. These dry-fit checks are accepted; they do not need to be repeated just to satisfy the previous notes.

- Original V2 PCB: **1.65 mm measured**. Keep this as the reference; choose a production nominal thickness after checking switch engagement and support. Thinner material is an option, not a requirement.
- V2 metal viewing window: **22.46 × 14.00 mm measured**.
- Original PCB has a battery opening only, **no display cutout**. Earlier photo interpretation was incorrect.
- Use the Typeractive main Choc grid as a reference, but place the thumbs at the Zen centers and provide clearance around the actual Zen mounting bosses. Do not reproduce the areas the user had to trim.
- Place the nice!nano on the socket/component side, soldered through edge contacts without headers or underside-pad wiring.
- Modify/reprint the plastic base to provide clearance and support. Preserve mounting seats and battery protection, and check antenna and USB cable clearance in final layout.
- Cropped right display is acceptable; useful content can occupy the visible region. A recessed carrier arrangement remains a placement task. Finalize screen position, five-pad solder access, module orientation, and lack of glass pressure before adding its optional footprint. Enlarging the window is an available user preference, not a prerequisite solely to display every pixel.

[Photo evidence](PHOTO-REVIEW.md) · [Archived measurements](CASE-MEASUREMENTS.md)

The archived V1 fixed-floor and full-screen visibility tests remain historical measurements, not current grounds to reject a cropped screen or a redesigned plastic base. No final display placement has yet been designed.

## Matrix GPIO contract

PCB columns are named **outside → seam on both halves**. Both halves use the same ten matrix GPIOs and the same physical thumb cells, R3C3–5. Each has 21 keys and col2row diodes, anode toward the switch and stripe/cathode toward the row.

| Net | Both halves: nice!nano edge / GPIO |
|---|---|
| R0 | D8 / P1.04 |
| R1 | D9 / P1.06 |
| R2 | D21 / P0.31 |
| R3 | D20 / P0.29 |
| C0 | D19 / P0.02 |
| C1 | D18 / P1.15 |
| C2 | D15 / P1.13 |
| C3 | D14 / P1.11 |
| C4 | D0 / P0.08 |
| C5 | D1 / P0.06 |

The right firmware scans from the seam out. It lists the same PCB columns in reverse: **C5, C4, C3, C2, C1, C0**, corresponding to **D1, D0, D14, D15, D18, D19**. This preserves the existing Corne key positions and split offset of six. Right PCB thumb nets C5, C4, C3 are local scan columns 0, 1, 2 and global columns 6, 7, 8. Do not reverse the row order or change the keymap.

**Custom right display:** move CS from the Ultralight’s D0 to **D4/P0.22, active high**. D0 stays on matrix C4. Keep **MOSI D2/P0.17** and **SCK D3/P0.20**. D2, D3 and D4 are available on the standard nice!nano edge because QSPI exists only on the left. These pins are marked no-connect until display mounting is confirmed. If fitted, use switched 3.3 V and GND and route all five connections through the PCB. Check backside orientation against the [official display pinout](https://nicekeyboards.com/docs/nice-view/pinout-schematic/). The adapter config specifies an unused MISO input internally; the display needs no MISO connection.

The 24 module symbol numbers are this project's explicit edge contact convention: component face toward viewer with USB at the top, bank 1–12 on the left top-to-bottom and 13–24 on the right top-to-bottom. Excludes the separate extra battery pair and all underside pads. See [official module v2 pinout](https://nicekeyboards.com/docs/nice-nano/pinout-schematic/). Verify orientation with the physical module when selecting the carrier footprint. No carrier footprint or traces are selected in this review.

## Left flash, unchanged at the module edge

| Flash net | nice!nano v2 edge | W25Q128JV SOIC pin | Integrated QIAA ball |
|---|---|---:|---|
| CS# | D2 / P0.17 | 1 | AD12 |
| CLK | D4 / P0.22 | 6 | AD18 |
| IO0 | D5 / P0.24 | 5 | AD20 |
| IO1 | D6 / P1.00 | 2 | AD22 |
| IO2 | D7 / P0.11 | 3 | T2 |
| IO3 | D3 / P0.20 | 7 | AD16 |
| VCC | Switched 3.3 V edge pad | 8 | Dedicated switched 3.3 V |
| GND | GND edge | 4 | Common ground |

P0.13 controls the switched VCC **inside** the v2 module; there is no carrier connection to P0.13. Keep the tested flash power sequencing and exclusive left firmware ownership. W25Q128JVSIQ (208-mil SOIC) is a **candidate** production part using the W25Q128JV pinout. Draft 100 nF decoupling and 10 kΩ CS# bias to the flash rail are schematic review choices, not claims about the handwired board. Validate exact orderable part, footprint, power-on timing and rail behavior with the selected module/parts. Route IO2 and IO3 as data; the hand-modified breakout's original rail straps are not part of this design. [Winbond part and datasheet](https://www.winbond.com/hq/product/code-storage-flash/qspi-nor/w25q-jv/?__locale=zh&partNo=W25Q128JVSIQ)

## Integrated starting point

Carry the same left QSPI and right-only optional display architecture forward. Use **nRF52840-QIAA aQFN73** as the candidate package, preserving both matrix GPIO maps. On the right reserve **AD18 (P0.22/CS), AD12 (P0.17/MOSI), AD16 (P0.20/SCK)** for a candidate SPIM0 write-only display bus, subject to the same mechanical gate. Keep left flash enable on **AD8/P0.13** as a candidate, using a switched regulated 3.3 V supply and an enable polarity matching the final hardware/overlay. Right and left reuse GPIO numbers on different chips; they do not share electrical nets. [Nordic package pin assignments](https://docs.nordicsemi.com/r/bundle/ps_nrf52840/page/pin.html) · [Nordic reference circuits](https://docs.nordicsemi.com/r/bundle/ps_nrf52840/page/ref_circuitry.html)

The [GPIO contract](gpio-contract.json) has the QIAA balls for every proposed signal. QFN48 is not a drop-in for this map. Exact package, power topology, radio/antenna, oscillator, USB/ESD, LiPo charging and sense, SWD, reset, flash partitions and PCB-specific board definition remain open. Lower component height alone does not resolve the same viewing throat. This is an integrated signal plan, not an integrated power or RF schematic.

## Review and verification

- Open `zen-r4-left-nano.kicad_pro` and `zen-r4-right-nano.kicad_pro` with the supplied symbol library and matching schematic. The SVG exports can be reviewed without KiCad.
- KiCad 10.0.7 ERC: **0 violations on each sheet**. Native netlists checked all 42 individual switch/diode pairs and the controller/flash net assignments. The right schematic contains no display footprint or flash. The electrical review sheets remain here; routed carriers and final PCB checks are in [r4-layout](../r4-layout/README.md).
- `zen-r4-right-matrix-review.overlay`: build for the custom right using `nice_nano//zmk` and `corne_right`, with the display disabled.
- `zen-r4-right-display-review.overlay`: future display build for the custom right only. Use it by itself as the extra overlay with `corne_right nice_view_adapter nice_view` and the baseline `right-nice-view.conf`. It includes the shared right matrix and sets CS to D4. Neither custom overlay is intended for the stock Ultralight.
- Both custom right firmware variants compile, including the baseline mode-sync display behavior with CS moved to D4. These are compile/net checks, not hardware tests.
- Left retains the pinned `corne_left.overlay` and its tested matrix/QSPI includes. No firmware was flashed.
- [Check results](checks/validation.json). Regenerate the measurements, schematics and checks with the three `analysis-tools/*zen_r4*review.py` / `zen_r4_display_fit.py` scripts in this project. These read the archived CAD, the pinned firmware build artifacts, and the installed KiCad symbol library.

## Routed carrier prototype

These files remain the electrical review baseline. The new [r4-layout projects](../r4-layout/README.md) include matched schematics, routed PCBs, custom footprints, physical fit templates and prototype bottom plates. The older `reconstruction/typeractive-model-*.kicad_pcb` files remain reverse-engineered references; do not send those to fabrication.

The carrier preserves the shared matrix and left QSPI wiring. Its right display remains omitted pending mounting. Read the layout README and final checks before using it: physical V2 fit, assembly and hardware validation remain open even after electrical checks pass.
