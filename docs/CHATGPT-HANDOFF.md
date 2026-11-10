# Draft-Corne C: current handoff

Private GitHub: https://github.com/disarmyouwitha/zenR4-pcb/tree/drafts/draft-corne

Read `projects/choc-corne-flash/draft-c/README.md`, `validation.json`, the matching native KiCad schematic/PCB pairs and `placement-preview.png`. The owner confirmed **nice!nanos on FRONT, components facing DOWN**, matching Typeractive. Battery J1 uses back-side solder pads instead of JST. Left flash/support and actual right five-pin nice!view interface are now implemented in the schematics and placement. Geometry is 42-key Typeractive-style Choc, reconstructed from its public model, not Zen geometry or original vendor CAD.

The earlier scope-only status below is superseded: a native Draft C now exists. It is a development draft, not fabrication-ready. Exact current ERC/DRC/parity/unconnected results and file hashes are in validation.json. Initial placement checks reported zero violations/parity issues, with all wiring still unrouted. Assembly height, antenna environment, exact purchased footprints, battery retention and final routing need review. Current working hardware/firmware is unchanged.

U1 carrier pad1/D1 is on the RIGHT in top view with USB up, pad13/B+ on the LEFT, on both halves. Right J2 front left→right: MOSI D2, SCK D3, switched3V3, GND, active-high CS D4. This differs from the physical Ultralight D0 CS because D0 is our matrix column.

Next conversation should focus on verifying the nano/display stack and completing/reviewing Draft C routing. Preserve our tested matrix/QSPI map below. RGB/art and integrated-chip/Zen replacement development are deferred. No order or working-device firmware changes are authorized by this handoff.

## Keep tested wiring

Both halves: ROW0 D8/P1.04; ROW1 D9/P1.06; ROW2 D21/P0.31; ROW3 D20/P0.29. Columns outside→seam: C0 D19/P0.02; C1 D18/P1.15; C2 D15/P1.13; C3 D14/P1.11; C4 D0/P0.08; C5 D1/P0.06. Col2row diodes, cathode toward row. Right firmware scans columns in reverse with offset 6.

Left flash: CS# D2/P0.17, CLK D4/P0.22, IO0 D5/P0.24, IO1 D6/P1.00, IO2 D7/P0.11, IO3 D3/P0.20; switched 3V3 and GND. P0.13 is controlled internally by nice!nano, not another carrier edge pad. Preserve tested rail/sleep policy. U2 W25Q128JVSIQ 208-mil SOIC is a candidate; local 100 nF and 10 kΩ CS bias require layout/part review.

The stock Corne/Typeractive D4–D7 matrix rows conflict with these QSPI signals. Copying the standard donor GPIO map unchanged will not work. Use the existing tested map instead; do not modify working firmware or flash the current hardware during PCB development.

Custom right nice!view: CS **D4/P0.22 active high**, MOSI D2/P0.17, SCK D3/P0.20; supply/GND. The existing Ultralight right uses a different matrix and D0 CS; custom overlays must not be flashed onto it. Mode-sync/reconnect behavior works on the hybrid prototype, while the custom-right overlays are compile checks, not new hardware evidence.


## Current validation and next steps

Native KiCad 10.0.7 ERC: 0 reported violations on each half. Native DRC: 0 reported violations and 0 schematic parity issues on each half, but **13 left / 20 right unconnected items remain**. These are not finished boards. Native configured ignored-check categories are retained in reports and validation.json. Independent netlist/PCB assertions verified our matrix, QSPI, right display pins, battery pads and module orientation.

Next: finish routing with the antenna keepout respected; physically verify the components-down nano stack, nice!view header height and solder access; confirm exact purchased socket, SOIC, reset/power footprints; select and retain a protected battery with strain relief; repeat ERC/DRC/parity and prototype. No Gerbers/order yet.

Generators under analysis-tools overwrite outputs. Do not regenerate the schematic after routing without rebuilding UUID-linked netlists/boards. Board regeneration also needs native socket-library normalization. Existing routing sessions are experiments, not original Typeractive copper.

Draft A in r4-layout/ and Draft B in projects/nano-independent/draft-b/ remain historical. Their prior checks do not validate C. Preserve ATTRIBUTION.md and LICENSES; repo stays private. No public release, fabrication or working-hardware changes were performed.
