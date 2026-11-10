# Draft-Corne C: current handoff

Private GitHub: https://github.com/disarmyouwitha/zenR4-pcb/tree/drafts/draft-corne

Read `projects/choc-corne-flash/draft-c/README.md`, `validation.json`, the matching native KiCad schematic/PCB pairs and `placement-preview.png`. The owner confirmed **nice!nanos on FRONT, components facing DOWN**, matching Typeractive. Battery J1 uses back-side solder pads instead of JST. Left flash/support and actual right five-pin nice!view interface are now implemented in the schematics and placement. Geometry is 42-key Typeractive-style Choc, reconstructed from its public model, not Zen geometry or original vendor CAD.

Draft C is fully routed with filled ground planes on both layers. The right display header moved 1.8 mm toward the thumbs so its pads clear the carrier’s antenna keepout. The module and display stack, selected footprints and battery retention still need physical checks.

U1 carrier pad1/D1 is on the RIGHT in top view with USB up, pad13/B+ on the LEFT, on both halves. Right J2 front left→right: MOSI D2, SCK D3, switched3V3, GND, active-high CS D4. This differs from the physical Ultralight D0 CS because D0 is our matrix column.

Next conversation should focus on verifying the nano/display stack and reviewing the routed boards. Preserve our tested matrix/QSPI map below. RGB/art and integrated-chip/Zen replacement development are deferred. No order or working-device firmware changes are authorized by this handoff.

## Keep tested wiring

Both halves: ROW0 D8/P1.04; ROW1 D9/P1.06; ROW2 D21/P0.31; ROW3 D20/P0.29. Columns outside→seam: C0 D19/P0.02; C1 D18/P1.15; C2 D15/P1.13; C3 D14/P1.11; C4 D0/P0.08; C5 D1/P0.06. Col2row diodes, cathode toward row. Right firmware scans columns in reverse with offset 6.

Left flash: CS# D2/P0.17, CLK D4/P0.22, IO0 D5/P0.24, IO1 D6/P1.00, IO2 D7/P0.11, IO3 D3/P0.20; switched 3V3 and GND. P0.13 is controlled internally by nice!nano, not another carrier edge pad. Preserve tested rail/sleep policy. U2 W25Q128JVSIQ 208-mil SOIC is a candidate; local 100 nF and 10 kΩ CS bias require layout/part review.

The stock Corne/Typeractive D4–D7 matrix rows conflict with these QSPI signals. Copying the standard donor GPIO map unchanged will not work. Use the existing tested map instead; do not modify working firmware or flash the current hardware during PCB development.

Custom right nice!view: CS **D4/P0.22 active high**, MOSI D2/P0.17, SCK D3/P0.20; supply/GND. The existing Ultralight right uses a different matrix and D0 CS; custom overlays must not be flashed onto it. Mode-sync/reconnect behavior works on the hybrid prototype, while the custom-right overlays are compile checks, not new hardware evidence.


## Current validation and next steps

Native KiCad 10.0.7 reports zero ERC violations, DRC violations, schematic parity issues, and unrouted connections on both halves. See `validation.json` for file hashes and the configured ignored-check categories. Pad checks confirmed the tested matrix, QSPI, right display signals, battery pads, and module orientation.

Physically verify the nano/display stack, solder access, switch and flash footprints against the parts, and battery retention before fabrication.

Generators under analysis-tools overwrite outputs. Do not regenerate the schematic after routing without rebuilding UUID-linked netlists/boards. Board regeneration also needs native socket-library normalization. Existing routing sessions are experiments, not original Typeractive copper.

Draft A in r4-layout/ and Draft B in projects/nano-independent/draft-b/ remain historical. Their prior checks do not validate C. Preserve ATTRIBUTION.md and LICENSES; repo stays private. No public release, fabrication or working-hardware changes were performed.
