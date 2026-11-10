# Current scope — Choc Corne with LHS flash / RHS nice!view

Owner's latest goal: **Typeractive-style Choc-spaced Corne, nice!nano controllers, flash on left, nice!view on right.** Function/construction should be close to the owner's existing Corne Ultralight; Choc spacing and left flash are the central changes.

Read `projects/choc-corne-flash/README.md` and `pin-plan.json`. The new `reference/` folder contains the earlier editable **unrouted, inferred** Typeractive model reconstruction. It is a geometry reference, not original electrical source or a validated production board.

Retire Zen case, Zen thumbs, battery cutout, mount and port constraints from the active design. Drafts A/B remain historical checked work, not the new geometry. Integrated-chip work is set aside. RGB/artwork are deferred to keep the first build small. The active scope update has not produced another fully routed PCB.

## Keep tested wiring

Both halves: ROW0 D8/P1.04; ROW1 D9/P1.06; ROW2 D21/P0.31; ROW3 D20/P0.29. Columns outside→seam: C0 D19/P0.02; C1 D18/P1.15; C2 D15/P1.13; C3 D14/P1.11; C4 D0/P0.08; C5 D1/P0.06. Col2row diodes, cathode toward row. Right firmware scans columns in reverse with offset 6.

Left flash: CS# D2/P0.17, CLK D4/P0.22, IO0 D5/P0.24, IO1 D6/P1.00, IO2 D7/P0.11, IO3 D3/P0.20; switched 3V3 and GND. P0.13 is controlled internally by nice!nano, not another carrier edge pad. Preserve tested rail/sleep policy. U2 W25Q128JVSIQ 208-mil SOIC is a candidate; local 100 nF and 10 kΩ CS bias require layout/part review.

The stock Corne/Typeractive D4–D7 matrix rows conflict with these QSPI signals. Copying the standard donor GPIO map unchanged will not work. Use the existing tested map instead; do not modify working firmware or flash the current hardware during PCB development.

Custom right nice!view: CS **D4/P0.22 active high**, MOSI D2/P0.17, SCK D3/P0.20; supply/GND. The existing Ultralight right uses a different matrix and D0 CS; custom overlays must not be flashed onto it. Mode-sync/reconnect behavior works on the hybrid prototype, while the custom-right overlays are compile checks, not new hardware evidence.

## Placement to investigate first

No left screen. Put the bare flash/support in the former display/JST electronics region if the complete assembly fits. Start with the **JST region**, move the battery connector/wire pads nearby and retain a proper battery path. Verify nano antenna keepout, under-module battery, flash package/land/courtyard, socket stack, lead bends and reset/power access. Do not assume a small flash body proves the entire circuit fits.

The Typeractive model gives the starting geometry. Its approximate nano/display-header/JST centers are recorded in the project README, but it is not dimensionally certified production CAD. No placement is yet approved. A simple matching case/plate/base can be designed after the electronics stack is established.

## Preserve context

`r4-layout/` = unchanged Draft A; `projects/nano-independent/draft-b/` = historical outer-outline revision. Both passed checks for their specific files, not this new geometry. Do not continue adapting those Zen outlines and call it a Typeractive board. Source/license notices remain applicable; repo stays private. No order, production Gerbers, visibility change or working-hardware alteration is part of the scope update.
