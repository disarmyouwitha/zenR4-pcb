# Typeractive Choc PCB reconstruction — revision 0.1

This is an editable reconstruction of both halves of the Typeractive Choc PCB from its public configurator model. It preserves the Typeractive geometry rather than adapting the thumb positions to the Zen. It is **an unrouted reference design**, not recovered original PCB source or a board ready for fabrication.

## Open these files

- `typeractive-model-left.kicad_pcb` and `typeractive-model-right.kicad_pcb`: editable, two-layer KiCad boards with recovered geometry and inferred switch-matrix net assignments.
- Matching `.kicad_sch` files: editable schematics of the inferred matrix, with embedded symbol definitions.
- `reconstruction-preview.png`: generated overview of both reconstructed boards. This is drawn from the generated board files, not a screenshot from KiCad.
- `left/right-model-mechanical.dxf`: outlines and hole circles in millimeters, for mechanical CAD.
- `switch-and-diode-placement.csv`, `component-placement.csv`, and `recovery-data.json`: placements and inference metadata.
- `left/right-inferred-matrix.net`: XML netlists, for independent review.
- `validation.json`: checks performed and their limits.

The PCB files embed their footprints, so external footprint libraries are not required to open and edit them. The schematic Footprint properties use the placeholder `Recovered:` library name. This library has not been packaged; assign verified production footprints or extract suitable libraries before creating a new board from the schematic or replacing footprints through library updates. Keep the existing embedded geometry when reviewing these boards.

## What was recovered, per half

- One closed board outline, simplified from the triangulated mesh with a 0.012 mm deviation threshold.
- All **145 circular holes**, including 21 switch center peg holes and their four supporting/socket holes, 24 controller holes, five display-header holes, and the remaining connector/alignment/mounting holes.
- **21 switch locations and rotations**, determined by matching the peg, supporting pin, and socket hole pattern.
- **21 diode body locations and orientations**, with the cathode end inferred from the modeled package stripe.
- Controller/header placement and component envelopes for battery connector, power switch, and reset button.
- Both front and back appearance textures. The copper routes are in these **1024 × 320 pixel images**, rather than separate copper geometry.

Hole diameters are fitted to polygonal mesh sections. These are visualization-model measurements, not drill-table specifications. Their small numerical roundoff does not imply micrometer accuracy in the original model or the physical PCB. Nominal hole sizes, plating, tolerances, and annuli require production verification.

## What was inferred

- The usual Corne 4-row × 6-column switch matrix, populated at 21 positions per half. The last row uses physical columns 3, 4, and 5.
- Col2row diode direction. Socket pad 1 is assigned to its column; pad 2 connects to diode anode. Diode cathodes connect to row nets. This is a proposed consistent circuit, not a traced proof of Typeractive's original pad numbering or routing.
- nice!nano v2 header functions and matrix GPIO assignments, based on primary documentation and the Corne definitions linked by Typeractive. The right-side logical header banks are mirrored based on the artwork; the physical controller orientation requires verification.
- Standard Choc hotswap SMD land locations/sizes. Only the socket and switch hole geometry is directly measured.
- SOD-123 diode lands: modeled body dimensions are consistent with that package. Exact diode part number is not recovered. Land sizes are taken from the KiCad SOD-123 footprint; its source/license is retained in `evidence/`.
- Through-hole annulus sizes. These are draft land patterns, not measurements of copper from the model.

`COL0` means the outermost column on each half. For the right half, the standard Corne firmware scans the physical column sequence in reverse. GPIO assignments on both reconstructed boards are COL0=P0.31, COL1=P0.29, COL2=P0.02, COL3=P1.15, COL4=P1.13, COL5=P1.11; ROW0=P0.22, ROW1=P0.24, ROW2=P1.00, ROW3=P0.11. This convention differs from a right-half firmware's inside-to-outside scan index.

## What remains unresolved

1. **Copper routing:** no copper tracks or zones have been generated. Every matrix connection is an unrouted net. The original traces, vias, pours, layer assignments, widths and clearances have not been recovered.
2. **Battery, power switch and reset circuitry:** only measured holes/envelopes are included. Battery polarity and usable switch/reset footprints are not established. Battery connector pads are unassigned. `BAT_SW`, `VCC`, `GND`, and `RESET` on U1 are labeled header nets, not completed support circuits.
3. **Display connections:** five measured header holes are included, with no assigned nets. Displays are not required for the user's intended replacement.
4. **Native validation:** no KiCad installation was available. Native DRC/ERC and actual loading/rendering in KiCad remain unverified. Parser checks do not replace those checks.
5. **Zen adaptation:** the reconstructed thumb positions still match Typeractive's model. They remain approximately 2.3–3.1 mm away from the downloaded early Zen case's centers. Controller height and the physical V2 case must also be resolved.

## Validation performed

- Both PCB and schematic files parsed and survived a serialize/reparse round trip using kiutils 1.4.8.
- Each PCB contains 58 footprints, 145 drilled holes, and zero copper tracks.
- Each schematic contains 43 symbols and 108 pin labels.
- Every modeled hole is represented once. File coordinate rounding introduces less than 0.00002 mm position error relative to the decoded/fitted model coordinates; the model itself is much less precise than this.
- Both outlines form a closed chain.
- PCB pad nets, XML netlist nodes, and schematic labels agree for the inferred circuit.
- Each of the 21 switch/diode intermediate nets contains exactly two nodes. Row/column fanouts match the populated 21-key matrix.

## Evidence and reproducibility

Public configurator: https://typeractive.xyz/pages/build#corne_choc

Main GLB: https://typeractive-customizer.pages.dev/corne/choc/meshopt.glb

Typeractive pinout documentation: https://docs.typeractive.xyz/build-guides/corne-wireless/troubleshooting

nice!nano v2 pinout: https://nicekeyboards.com/docs/nice-nano/pinout-schematic/

Upstream Corne definitions are copied into `evidence/` from the official ZMK repository. They establish the proposed matrix and GPIO convention, not the original copper topology.

Scripts are in `../analysis-tools/`. Run `reconstruct_typr.py`, `make_matrix_schematic.py`, `validate_reconstruction.py`, and `preview_reconstruction.py` in that order. They use the decoded GLB data in `../references/typeractive-choc-3d/`. Dependencies are NumPy, SciPy, Pillow and kiutils; the GLB decoder additionally uses the listed Node dependencies. PNG texture extraction is a direct read of embedded GLB image buffer views.

The next electrical work is to establish the battery/switch/reset land patterns and connections and route the inferred circuit. Before doing that for a Zen replacement, confirm the physical V2 case geometry and choose the controller mounting arrangement so routing does not have to be repeated.
