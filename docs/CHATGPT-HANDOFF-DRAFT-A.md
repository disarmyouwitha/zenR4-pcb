> HISTORICAL: Draft A before the move to our own nice!nano case. Current scope and files: CHATGPT-HANDOFF.md.

# Zen R4 PCB — ChatGPT handoff

Snapshot: 2026-11-09. Repository: https://github.com/disarmyouwitha/zenR4-pcb (private). Current design: **DRAFT A nice!nano carrier**, two 21-key halves for a **42-key Corne-ish Zen V2 metal case**. The owner is designing their first PCB. Explain terms plainly and distinguish evidence, assumptions and remaining work.

## Start here

We now have **real routed custom KiCad schematics and PCBs**, not just a reverse-engineered Typeractive texture. Both halves passed KiCad 10.0.7 ERC, DRC, unconnected-item checks and schematic parity with **zero issues**. Pad/net membership checks also passed. Those checks establish represented connectivity and geometric rules; **the new PCBs have not been fabricated or hardware-tested**. This is not a production release.

The most useful discussion tomorrow is **physical layout and assembly review before ordering**, especially the controller's new USB opening and mounting stack. Do not start by changing matrix pins, reconstructing texture traces, or designing an integrated radio/charger.

If a private GitHub link cannot be opened in ChatGPT, use the attached `CHATGPT-HANDOFF.md` and PNG images, or unpack the upload bundle. The handoff is self-contained. Do not claim to have read a private repository that is inaccessible.

### Copy/paste conversation starter

> I'm making a replacement PCB for my 42-key Corne-ish Zen V2. Read this handoff and the attached diagrams. We have a routed nice!nano design with zero ERC/DRC/parity issues, but it is unbuilt. Help me review the USB opening, underside nano soldering/height, battery and switch access, and assembly choices before ordering. Keep the tested left matrix and left QSPI pinout, use that same matrix on the right, and distinguish hardware-tested behavior from compile checks and CAD assumptions. A cropped right nice!view is acceptable, but no display footprint exists yet. Start with the open mechanical/assembly decisions, not a redesign of the working pinout.

## 1. What the owner wants and what was decided

- Reuse the Zen V2 **metal shell**, 42 keys, Choc spacing, Zen thumb positions, Bluetooth between halves, preferably nice!nano v2 for this revision.
- The owner has a partially failed original Zen and limited vendor support. The working replacement prototype is a **handwired/custom Zen left running Javelin plus an existing Corne Ultralight right**. The Ultralight is a test platform, not the required pinout/layout for the custom right.
- **Both new halves use the tested LEFT matrix GPIOs.** Physical columns are C0 outside → C5 at the seam on each half. The right firmware reverses its scan-column list to preserve existing Corne key positions.
- **Left QSPI flash only.** Preserve the tested edge-pad wiring. No left display.
- **Right nice!view optional**, only after its actual mounting, solder access, clearance and useful visible area work. Cropped viewing is fine. Right display CS must move from the tested Ultralight's D0 to **D4/P0.22** to free D0 for the shared matrix. MOSI remains D2 and SCK D3.
- All nano connections must use its standard **edge holes/pads**, not underside test pads. The current carrier has 24 through-hole positions. Plan short trimmed through-pins/edge-hole joints, not a tall socket/header stack. It has not been proven possible to solder two flat boards together reliably without those joints.
- The user accepts modifying/reprinting the plastic base, removing a raised floor feature, and some metal filing. **Acceptance of slight filing did not establish acceptance or fit of this specific design's new USB opening.** See the USB decision below.
- The owner accepts a partially visible screen and might enlarge the metal window. Never reject a display just because every pixel cannot be seen. It still needs solder access, retention, insulation and no glass pressure.
- Do not change the working firmware or flash either current working half without an explicit request. None was changed/flashed during the PCB layout work.

## 2. Evidence ladder — do not blur these categories

| Evidence | What it establishes | What it does not establish |
|---|---|---|
| Owner's physical dry fit | Typeractive Choc sockets clear the Zen backplate; case closes after trimming circled PCB areas; nano appears to fit underneath with modified base | Our new outline, solder joints, USB location, flash height or all assembled components fit |
| Owner's measurements | Original PCB **1.65 mm**; metal viewing window **22.46 × 14.00 mm** | A display opening in the PCB; the original PCB has **battery opening only** |
| Darryl's archived Zen CAD | Registered grid/thumb/mount geometry and a reference case/base | Exact physical V2 shell geometry. Archive is early/V1 |
| Working hybrid hardware | Tested left matrix/QSPI, Javelin, split mode sync, Ultralight right display and reconnect behavior | New custom PCB or a new display CS pin on hardware |
| Custom-right firmware builds | Shared matrix overlay and future display overlay with CS D4 compile | Physical custom right matrix/display behavior |
| Final native KiCad checks | Zero ERC, DRC, unconnected and parity issues; matching pin memberships | Signal integrity, battery safety, antenna performance, solderability, case fit or fab yield |

The Typeractive main grid was the nearest starting reference, but its thumb cluster differs. Our replacement uses Zen thumb centers and mounting holes. The Ultralight is MX spaced; it is not a mechanical donor for this design. JonMuller's ChocSpacedV4 Gerbers and WLFKBD were research references; this is not a proven drop-in version of either.

## 3. Current files and authority

| Path | Role |
|---|---|
| `r4-layout/zen-r4-left.kicad_pro`, `zen-r4-right.kicad_pro` | Open these in KiCad 10 |
| `r4-layout/zen-r4-*.kicad_sch` and `*.kicad_pcb` | Authoritative current schematics/routed boards |
| `r4-layout/footprints/ZenR4.pretty`, `fp-lib-table`, `r4-review.kicad_sym`, `sym-lib-table` | Project-local libraries; keep relative paths |
| `r4-layout/checks/*-final-drc.json` | Final board rules + schematic parity |
| `r4-layout/checks/*-erc.json`, `net-membership-audit.json`, `validation.json` | Electrical checks and board/schematic SHA-256 snapshot |
| `r4-layout/checks/front-component-clearance.json` | Sampled archived-shell clearance, not physical V2 signoff |
| `r4-layout/geometry.json` | Case-coordinate centers, mounts, current/original perimeter and local additions |
| `r4-layout/mechanical/` | 1:1 SVG templates, bare-board fit STLs, modified base prototype STLs |
| `docs/images/`, `docs/schematics/` | Annotated discussion images and direct schematic exports |
| `zen-r4-review/` | Historical electrical/firmware context. Current handoff and routed files take precedence over stale “before layout” descriptions |
| `analysis-tools/` | Experimental generation/analysis scripts, not a safe one-command production rebuild |

Native checks can be rerun with `sh r4-layout/run-checks.sh` on this Mac. Override `KICAD_CLI` on other installations. No GitHub Actions check is implied. Read the final boards directly; `build_r4_pcb.py` overwrites placement/routing, and `r4_geometry.py` resets local perimeter edits. The historical `.dsn/.ses` files alone do **not** contain the final extra left routes; `checks/manual-routes.json` and `r4_finish.py` were part of completion. Directly committed KiCad files are authoritative.

## 4. Exact shared matrix — preserve this

21 keys per half, 4 rows × 6 possible columns, diode direction **col2row**. Drive column → switch → diode anode; stripe/cathode toward row. Three physical thumbs occupy **R3C3, R3C4, R3C5** on both halves. Both halves use the following assignments:

| Net | nice!nano label | nRF52840 GPIO | U1 edge-hole number in this project |
|---|---|---|---:|
| ROW0 | D8 | P1.04 | 11 |
| ROW1 | D9 | P1.06 | 12 |
| ROW2 | D21 | P0.31 | 17 |
| ROW3 | D20 | P0.29 | 18 |
| COL0, outside | D19 | P0.02 | 19 |
| COL1 | D18 | P1.15 | 20 |
| COL2 | D15 | P1.13 | 21 |
| COL3 | D14 | P1.11 | 22 |
| COL4 | D0 | P0.08 | 2 |
| COL5, seam | D1 | P0.06 | 1 |

The **right firmware** scans PCB columns in reverse: `[COL5, COL4, COL3, COL2, COL1, COL0]` = `[D1, D0, D14, D15, D18, D19]`, with global column offset 6. Its physical thumbs map to local scan cells R3C0–2 and global columns 6–8. Do not reverse rows or change the keymap to “fix” the physical naming.

Left switch references SW1–18 run through each row outside→seam; SW19–21 are thumbs C3→C5. Right SW1–18 run seam→outside and SW19–21 are thumbs C5→C3. Thus switch reference numbers on opposite sides do not imply identical named columns. Each switch connects to its same-numbered diode through an individual net (`Net-(D#-A)` in final native names).

### U1 footprint orientation — important

The symbol's 24 numbers are **our explicit convention**, not manufacturer MCU package numbers. Looking directly at the module's **component face** with USB at the top: numbers 1–12 go down the left edge and 13–24 down the right. The carrier mounts the module component face downward toward the plastic base. Consequently, **in a TOP view of the keyboard PCB, pad 1/D1 is on the RIGHT and pad 13/B+ is on the LEFT**, USB toward the rear. Looking at the underside reverses that. A mirrored-bank error was caught and corrected before final checks. Check a physical nano against the drawing before soldering.

| Pads 1–12, component-face left top→bottom | Pads 13–24, component-face right top→bottom |
|---|---|
| 1 D1 | 13 RAW/B+ (switched battery) |
| 2 D0 | 14 GND |
| 3 GND | 15 RESET_N |
| 4 GND | 16 switched VCC / 3V3_SW |
| 5 D2 | 17 D21 |
| 6 D3 | 18 D20 |
| 7 D4 | 19 D19 |
| 8 D5 | 20 D18 |
| 9 D6 | 21 D15 |
| 10 D7 | 22 D14 |
| 11 D8 | 23 D16, unused |
| 12 D9 | 24 D10, unused |

## 5. Left QSPI — unchanged tested pins

| Signal | Edge label | GPIO | U1 pad | Flash U2 SOIC pin |
|---|---|---|---:|---:|
| CS#, active low | D2 | P0.17 | 5 | 1 |
| CLK | D4 | P0.22 | 7 | 6 |
| IO0 | D5 | P0.24 | 8 | 5 |
| IO1 | D6 | P1.00 | 9 | 2 |
| IO2 | D7 | P0.11 | 10 | 3 |
| IO3 | D3 | P0.20 | 6 | 7 |
| Switched 3.3 V | VCC | module-controlled | 16 | 8 |
| GND | GND | common | 3/4/14 | 4 |

Candidate bare part: **W25Q128JVSIQ, 208-mil / 5.3 × 5.3 mm SOIC-8 body**, using the W25Q128JV pinout. Exact orderable part, package, supplier and assembly choice remain to be locked. Do not silently substitute a narrower 150-mil SOIC or the part on a breakout. Tested prototype returned JEDEC **EF 40 18**; the production candidate has not been tested on this PCB.

C1 = 100 nF between flash supply and GND. R1 = 10 kΩ CS# pull-up to flash supply. U2, C1 and R1 are **front side**; the nano is on the back. Flash placement was moved into the window area to avoid the archived metal lip. Current case coordinates: U2 center (-14.3, 17.5), C1 (-14.3, 22.0), R1 approximately (-14.3, 11.28), in mm.

**IO2 and IO3 are data lanes.** Do not strap them high. The tested hand-modified breakout had those lanes isolated from its original supply straps; that breakout modification is not a desired feature of the new bare-flash circuit.

P0.13 controls the switched rail **inside nice!nano v2**. There is no carrier wire/pad to P0.13. The tested left firmware owns that rail, disables generic external power control, keeps flash available during Bluetooth idle for Javelin/browser dictionary access, then coordinates flash sleep, high-impedance QSPI pins and rail-off at deep sleep. Wake restores power and verifies dictionaries. Preserve that behavior; a display policy must not unexpectedly cut left flash power.

## 6. Right display — reserved, absent from the PCB

| Future nice!view signal | nice!nano | GPIO | U1 pad |
|---|---|---|---:|
| CS, **active high** | D4 | P0.22 | 7 |
| MOSI | D2 | P0.17 | 5 |
| SCK | D3 | P0.20 | 6 |
| Supply | switched VCC | module rail | 16 |
| GND | GND | common | 3/4/14 |

The working Ultralight display uses **CS D0/P0.08**, MOSI D2 and SCK D3. D0 is needed for COL4 on our new right. The **custom-right candidate** moves CS to D4; it is compile-tested, not hardware-tested. The generic adapter's D1 CS default was wrong for the tested Ultralight. Do not conflate those three assignments.

Current right schematic has **no display footprint, connector or routes**. The relevant U1 pads are no-connect until a feasible mounting solution is designed. The left uses these GPIOs for QSPI on a separate MCU; that creates no cross-half conflict. Both halves can reuse identical matrix GPIO numbers because they are separate controllers.

Nice!view reference envelope is about 14 × 36 mm, roughly 2.9 mm overall, with a 1.0 mm carrier; refer to the official drawing before a new mechanical design. The physical metal window measured 22.46 × 14 mm. Cropping is accepted. The archived fixed-floor collision is historical: the user permits removing it and making a new base. Still resolve five-pad solder access, module/controller overlap, battery interaction, viewing orientation, electrical insulation, retention and glass pressure before adding a footprint.

## 7. Power, reset, parts and routing facts

- J1: **two battery-wire solder pads**, pin 1 BAT_RAW, pin 2 GND. It is not a JST connector with an assumed cable polarity.
- SW22: PCM12 SPDT. Common **pad 2 = BAT_RAW**, pad 3 = BAT_SW feeding nano RAW/B+, pad 1 unused. Pad numbering differs from the old generic two-pin review switch; the current schematic uses the corrected 2/3 numbering.
- SW23: TL3342 reset switch, pins 1 RESET_N and 2 GND (multiple same-numbered physical lands may exist).
- Battery charging, regulator, radio and USB are on nice!nano. This carrier does not recreate those circuits.
- Original PCB measured 1.65 mm; draft carrier nominal **1.6 mm**, not a proven exact stack-up. Thinner boards are an option, not a requirement.
- Two copper layers; minimum trace 0.20 mm, clearance 0.20 mm, copper-edge 0.25 mm; vias 0.60 mm / 0.30 mm drill. No ground fill was added. Left has 64 vias / 639 track segments, right 45 / 496 in the recorded final export. This is an initial routed prototype; QSPI return paths/routing quality and radio performance still need review.
- Five 4.4 mm mounting holes per half; battery opening 20.2 × 20.5 mm. Verify actual battery envelope/retention rather than assuming the opening proves fit.
- The innermost top-row switch on **each** half (physical R0C5) is rotated 180° for boss clearance. Check socket orientation and physical parts on assembly.
- Project-local `__NoSilk` variants keep standard KiCad pads and courtyards but remove crowded silkscreen. Hidden markings make a separate assembly drawing/polarity review especially useful before ordering.

## 8. Mechanical review — the real next gate

### USB: a specific new cut, not a signed-off small enlargement

The nano center is x=-14.3 mm on the left and x=+24.9 mm on the right in archived case coordinates, USB toward the rear. Archived original USB centers are roughly -38.51 and +53.52 mm. Thus this design's connector is offset **about 24.2 mm left / 28.6 mm right** from those archived ports. This placement needs a **new rear opening at the nano location**. The physical V2 port position might differ; it has not been quantitatively aligned to this draft.

Before cutting or ordering, decide whether to keep this placement and make the new opening, or rework controller placement / USB relocation. The owner prefers avoiding a custom USB/charger circuit. A remote connector/extension can itself take space and require module modification; do not present it as an already solved escape. Do not tell the owner their earlier dry fit proved this exact new opening works.

### Fit artifacts

- `r4-layout/mechanical/zen-r4-*-fit-1to1.svg`: print at **100% actual size**, disable fit-to-page, verify the **25 mm bar**. Top view; dashed nano body is on the opposite side. Mirror if checking from underside.
- `zen-r4-*-bare-pcb-fit-PROTOTYPE.stl`: watertight **1.6 mm** dummy boards, actual nominal drill pattern and battery opening, archived case coordinates. Check the new perimeter, thumb centers and bosses without paying for PCBs.
- `zen-r4-*-base-pocket-PROTOTYPE.stl`: provisional modified plastic bases. Local pocket floor z=-4.25 mm, exterior bottom z=-5.5 mm, floor thickness 1.25 mm, nano pocket open at the rear. They still need physical V2 perimeter/mount/USB/solder/battery checks. Power/reset access holes and battery restraint/insulation remain unfinished.
- Local socket-land perimeter additions are approximately **6.5 mm² left / 5.2 mm² right** beyond the archived outline. A rule check can allow them electrically while the metal shell still interferes. Fit-check them.
- Grid registration of the 18 main key centers is within about 0.10 mm against the archived case. That is not an assembled V2 fit claim.
- Sampled front-component envelopes: U2 and C1 lie in the archived open window; R1 has about **0.32 mm nominal headroom before solder allowance** using an assumed 0.65 mm component height. Check actual V2 and ordered part heights.
- Keep solder, component leads, metal-shell insulation, battery protection and lack of glass pressure in the stack. The nano's usable soldering method and exact height are not validated by a bare-body fit.

Do **not** ask again whether the original Typeractive sockets/nano generally fit: the owner already confirmed that. Ask only for a specific unresolved placement/clearance if its answer will change a decision. The original PCB has **no display cutout**, so do not request its “display cutout dimensions.”

## 9. Firmware and hardware bring-up context

Pinned tested application baseline: `cb3ccc8720a496fba8d877784345c6b120a0b999` in https://github.com/disarmyouwitha/zmk-javelin-steno . Manifest ZMK baseline was `4dd95d7840eb3d5a3f59bb29fbf1ab054715ef85`. These are the handoff's recorded baselines; do not assume the current remote main branch is unchanged.

Working hybrid checks included all 21 left switches and simultaneous chords, normal typing, Plover HID, onboard Javelin, both base dictionaries through QSPI, browser personal-dictionary editing, battery-powered flash-off deep sleep and wake. Left sends active mode over Bluetooth; the existing right nice!view follows Typing / SYM+NUM / Javelin / Plover HID and restores current mode after reboot/reconnect.

The custom right matrix overlay and the optional future D4-CS display overlay compiled. They are **not intended for the stock Ultralight right**. Do not flash the custom matrix onto that board. The current no-display PCB should use the custom right matrix/no-display build when eventually brought up. The left retains its tested matrix/QSPI includes.

After mechanical and assembly review, bring up one assembled pair in stages: inspect/continuity and resistance checks with power disconnected; verify polarity, no shorts and supplies; confirm module USB boot/reset and charging behavior; scan every switch and chords; run a **read-only JEDEC probe** before provisioning; verify fresh flash contents, mapped dictionary reads, Javelin and browser edits; verify Bluetooth split and sleep/wake. Only test display/mode rendering on a new display-capable revision if it is actually fitted. Battery/current checks must use the actual selected cell and module settings.

## 10. Ordered next steps and decisions for tomorrow

1. **Review the USB placement decision.** Use the top-view nano pin/orientation drawing and 1:1 templates. New rear notch versus a controller/USB placement revision is the largest unresolved shell decision.
2. **Print the fit artifacts.** Check our new thumb/perimeter/boss geometry, base seats and cable boot. Confirm vertical clearance using actual nano, intended trimmed-pin joint and insulation; do not force the metal case closed.
3. **Review assembly and battery.** Lock short-pin solder method, socket model/orientations, diode stripe, exact flash package and pin 1, power/reset parts and access, battery size/lead polarity/retention and insulation. A JLC-style assembly/stock check and BOM/CPL have not been prepared or quoted. Nice!nano/socket installation may remain manual.
4. **Review electrical layout quality.** Especially QSPI return paths, decoupling, antenna keepout/metal environment and power/charging assumptions. Re-run native ERC/DRC/parity after any change. Do not treat zero-rule-errors as a signal-integrity signoff.
5. **Decide display scope.** Keep Draft A without a display for the first pair, or create a mechanically proven right-display revision and route it with D4 CS / D2 MOSI / D3 SCK. The owner has not abandoned their display preference; current omission is a mounting gate.
6. **Freeze a reviewed prototype revision**, then create Gerbers, drills, BOM, assembly drawing and placement files as appropriate; review manufacturer previews and exact order options. **No released Gerbers, fabrication order or fully assembled-PCBA quote exists.** Do not order five pairs based only on today's rule checks.
7. **Bring up hardware** as described above and record measurements/failures. The integrated nRF52840 version can follow this proven signal architecture later.

Integrated candidate: **nRF52840-QIAA aQFN73**, same left-flash/right-display architecture and matrix signals as a starting point. Chip-specific power, RF/antenna, clocks, USB/ESD, LiPo charger, SWD, bootloader, enable polarity and board definition remain undesigned. QFN48 is not a drop-in for this map. We are not switching away from nice!nano in this draft.

## 11. Sharing and sources

This repo is private by default. Darryl's archived Zen files carry **CC Attribution–NonCommercial–NoDerivatives** as stated in their supplied license. Original attribution and KiCad library notices are retained. The project does not claim to be Typeractive's open-source PCB, and no blanket open-hardware license has been assigned to everything in the repository. Review third-party material before any future public release.

Primary references for further verification:

- Zen archive: https://www.thingiverse.com/thing:4698210
- nice!nano official pinout/schematic: https://nicekeyboards.com/docs/nice-nano/pinout-schematic/
- nice!view official pinout/dimensions: https://nicekeyboards.com/docs/nice-view/pinout-schematic/
- Winbond W25Q128JV candidate: https://www.winbond.com/hq/product/code-storage-flash/qspi-nor/w25q-jv/?__locale=zh&partNo=W25Q128JVSIQ
- Nordic nRF52840 package/reference design: https://docs.nordicsemi.com/r/bundle/ps_nrf52840/page/pin.html
- Earlier research: https://github.com/JonMuller/gerbers/tree/main/ChocSpacedV4 and https://github.com/WillACosta/wlfkbd/

The owner's original HEIC photos are not embedded in this upload packet. `zen-r4-review/PHOTO-REVIEW.md` records their interpretation and subsequent corrections. If discussing a photo, distinguish that written record from actually seeing the original.

## 12. Plain-language glossary

- **PCB:** the physical circuit board. A schematic describes what connects; the layout gives each part, hole and copper trace its physical location.
- **ERC:** electrical rules check on the schematic. It catches certain represented pin/connectivity problems.
- **DRC:** design rules check on the PCB. It checks copper spacing, drill rules, edges and similar constraints.
- **Schematic parity:** checks that the physical board's assigned parts/pads/nets agree with the schematic.
- **GPIO / D label:** a programmable processor pin. A nice!nano D label, the Nordic P-port number and our U1 pad number are three different names for a particular connection.
- **QSPI:** a serial memory bus using clock, chip select and four data lines. Here it connects the left controller to dictionary flash.
- **Active high / active low:** whether a signal selects a device at high voltage or low voltage. nice!view CS is active high; flash CS# is active low.
- **Via:** a plated small hole joining copper layers. An NPTH is an unplated mechanical hole. A module edge-hole joint is a separate assembly issue.
- **BOM / CPL:** bill of materials / component placement list for assembly. Gerbers describe board artwork; drill files describe holes. None alone establishes that a board fits the case.
