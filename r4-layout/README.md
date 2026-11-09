# Zen R4 carrier — DRAFT A

Two custom 21-key Choc-spaced PCBs for the 42-key Zen. Open `zen-r4-left.kicad_pro` or `zen-r4-right.kicad_pro` in KiCad 10. The matching schematics, local symbols and local footprint library are included. `layout-preview.png` shows the actual routed geometry. This is a routed engineering prototype, not a released fabrication package.

## Implemented

- Same tested left matrix GPIOs on both halves; columns C0 outside through C5 at the seam. Zen thumb centers and five mounting holes per half, recovered from Darryl's archived geometry rather than Typeractive's thumb positions.
- Bottom-mounted nice!nano v2, all 24 edge-hole positions, component face toward the plastic base and USB toward the rear. In carrier top view D1/pad 1 is on the right. No underside module-pad wiring. Plan short through-pin solder joints with trimmed pins, not a tall header/socket stack; confirm solder access on the physical prototype.
- Left bare W25Q128 QSPI on the tested D2/D4/D5/D6/D7/D3 pins, switched VCC, 100 nF and 10 kΩ CS pull-up. U2 is on the **front** in the display-window region; controller, diodes, sockets and switches are on the back. Flash part is a candidate 208-mil SOIC W25Q128JVSIQ; do not substitute the narrower SOIC without changing footprint.
- Right display omitted. Cropping remains acceptable, but its carrier, solder access and glass clearance have not been solved. D4 CS active high, D2 MOSI and D3 SCK remain available; the earlier reviewed display overlay is retained in `../zen-r4-review/`.
- 1.6 mm nominal replacement against the original measured 1.65 mm; battery opening 20.2 × 20.5 mm; 4.4 mm mounting holes; two copper layers; minimum traces 0.20 mm, clearance 0.20 mm, copper-to-edge 0.25 mm, vias 0.60/0.30 mm. No ground pour has been added. The module includes its own radio/power/USB/charger circuitry. Front U2/C1 clear the archived window in a sampled envelope check; R1 has 0.32 mm sampled nominal headroom before solder allowance. These checks use early CAD and assumed part heights, not measured V2 clearance.
- Power SW22 is PCM12 with common pad 2 to battery, pad 3 to module RAW/B+, unused pad 1. Reset SW23 is TL3342. J1 is explicitly two soldered battery-wire pads, **not** a presumed JST pinout. Switch access through the new plastic base remains to be finalized.
- The innermost top-row socket on each half is rotated 180° to clear the adjacent boss. The remaining main keys and the three thumbs use their documented orientations. Check actual socket orientation when assembling.

## Checks and their limits

**Final native checks: zero ERC violations, zero DRC violations, zero unconnected items and zero schematic parity issues on each half.** `checks/*-final-drc.json` are the authoritative final KiCad reports, including schematic parity. `checks/*-erc.json` contain the schematic electrical checks. The separate net-membership audit compares all switch/diode pairs, module signals and flash wiring to KiCad's exported schematic XML. No rules are suppressed to hide routing errors. Local `__NoSilk` footprints retain standard KiCad pads/courtyards but remove crowded silkscreen graphics.

The working keyboard firmware has not been changed or flashed. Compile-tested custom right overlays and the pinned tested left wiring remain in the electrical review directory. The custom PCB still needs hardware bring-up and QSPI signal/power validation. A DRC pass does not establish case fit, radio performance, flash timing or assembly yield.

## Physical prototypes before ordering

`mechanical/zen-r4-*-fit-1to1.svg`: top-view paper templates. Print at 100% / actual size and verify the 25 mm calibration bar; disable “fit to page.” They show holes, outline, battery opening, switch bodies and a dashed nano body. For viewing the back, mirror the template or look through it.

`mechanical/zen-r4-*-bare-pcb-fit-PROTOTYPE.stl`: watertight 1.6 mm dummy boards with actual drill holes and battery opening, in the archived case coordinates. Use these to check this new outline, thumb locations and boss reliefs. The user’s successful Typeractive socket dry fit and underside nano fit are accepted; this check concerns the **new** geometry.

`mechanical/zen-r4-*-base-pocket-PROTOTYPE.stl`: modified archived plastic bases with ribs removed locally and deeper nano pockets. The pocket floor is z=-4.25 mm with a 1.25 mm floor; the new exterior reaches z=-5.5 mm. The rear pocket is open for USB access. These bases are provisional: check the physical V2 perimeter, mounting seats, USB cable boot, solder joints and battery protection. Reset/power access and the battery's final restraint/insulation are not finished.

Local socket-land reliefs added approximately 6.5 mm² (left) and 5.2 mm² (right) to the archived perimeter. They need the dummy-board fit check; do not assume they clear the metal simply because the 18 main switch centers register within 0.10 mm. Also confirm front-side flash headroom at the actual V2 window and module/base vertical clearance. No more whole-case measurements are needed to begin these checks.

**USB location needs specific review before cutting:** this layout centers the nano at archived-case x=-14.3 mm (left) / +24.9 mm (right). The archived original ports are centered about -38.51 / +53.52 mm, offsets of approximately 24.2 / 28.6 mm. The current placement therefore needs a new rear opening at the controller location. The physical V2 port position and acceptability of that cut must be checked with the fit template; the earlier general acceptance of slight filing is not a fit certification for this particular opening. Optional display-window filing remains accepted. The integrated nRF52840 version is a separate next design; this package uses nice!nano modules.

## Sources and regeneration

Darryl's original Zen models: https://www.thingiverse.com/thing:4698210 (early archived version; physical V2 evidence takes precedence). Derived base meshes are personal-use prototypes; preserve the source attribution and its original license restrictions. Custom electrical design is not presented as Typeractive source.

Generators live in `../analysis-tools/`: `r4_geometry.py`, `build_r4_pcb.py`, `r4_layout_schematic.py`, `r4_finish.py`, `r4_complete_routes.py`, `r4_base.py` and `r4_artifacts.py`. Geometry regeneration resets the local contour edits; rebuilding placement resets routing. Keep these reviewed boards and checks before regenerating. Routing used local Freerouting with telemetry disabled, 0.20 mm minimum routing, automatic neckdown disabled and extra edge/area clearance. The remaining left airwires were completed by local two-layer grid search and checked by native KiCad DRC.

No fabrication order has been placed. Gerbers are intentionally not packaged as released production files while the physical checks above remain open.
