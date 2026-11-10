# Target: Choc Corne, left flash, right nice!view

The owner narrowed the goal: **a Typeractive-style Choc-spaced Corne with flash on the left and nice!view on the right**, similar in construction/function to the existing Corne Ultralight. The initial build has two changes of interest: Choc spacing and left flash. No Zen shell, Zen thumb geometry, Zen battery cutout or inherited port relief is a design constraint.

## Minimum hardware

| | Left | Right |
|---|---|---|
| Geometry | Typeractive-style 21-key Choc half | Matching Choc half |
| Controller | nice!nano v2, conventional accessible edge-hole mounting | nice!nano v2 |
| Extra device | Tested external QSPI flash | nice!view |
| Battery | Retain a real connection, power switch/reset and safe mounting | Retain battery/power/reset |
| Firmware | Existing tested matrix/QSPI architecture | Same tested matrix; D4 CS / D2 MOSI / D3 SCK display |

Keep RGB and artwork for a later revision. A simple plate/base enclosure can follow the assembled board; it must not dictate another electronics redesign now. No new custom USB, charger or integrated RF circuit is needed for this target.

## Why the existing pin map still matters

The standard Corne/Typeractive row assignments use D4–D7. Our tested left QSPI uses D4–D7 too. These cannot remain matrix rows and flash signals on the same controller. Use the existing tested custom matrix/QSPI map from `pin-plan.json`, rather than inventing another mapping or copying the donor netlist unchanged. Keeping the same matrix on both halves preserves the earlier owner preference. On the custom right that means CS D4 (active high), MOSI D2 and SCK D3, not the stock Ultralight's D0 CS.

Source: [Typeractive pinout documentation](https://docs.typeractive.xyz/build-guides/corne-wireless/troubleshooting), which links the [Corne row definition](https://github.com/zmkfirmware/zmk/blob/main/app/boards/shields/corne/corne.dtsi). Working firmware is not changed/flashed by this scope update.

## Left flash placement proposal

Omit the left display and its unused interface. The display-header / battery-JST electronics area is the first area to study for the bare flash and C1/R1. **The JST region is the preferred first candidate; no fit is asserted.** Relocate the battery connector or use explicitly polarized wire pads nearby, rather than deleting the battery connection.

Reference-model coordinates in the reconstruction's PCB XY frame: nano center approximately (143.51,47.60), display-header center (143.04,65.33), JST body center (144.06,69.86) mm. These are visualization-derived placements, not drill specifications. The nano body is roughly 18 × 34.2 mm, so the display-header area is close to its end; verify antenna clearance before putting flash/copper there. Account for module sockets, battery under the module, connector lead bend, reset/power and solder access.

The candidate 208-mil SOIC flash needs its full lead/land/courtyard envelope plus decoupling/bias, not just its 5.3 mm body. Confirm the actual selected W25Q128 package and pin 1. Keep the tested six signal assignments and switched flash rail; IO2/IO3 remain data lanes.

## Reference and implementation status

`reference/` contains the earlier editable reconstruction of the public Typeractive 3D model. It supplies the **right starting geometry**, including the Typeractive thumbs. Its copper is unrouted, its matrix is inferred, the display header is electrically unassigned, and battery/switch/reset support is incomplete. It is not Typeractive's released electrical CAD or a production donor netlist. Read its README before opening it as a manufacturing design.

Draft A and B are preserved as tested-wiring/layout research. Their Zen-derived outlines and positions are **not** the geometry for this target. Their zero-rule-error reports do not validate the reference boards or a future new layout.

Next implementation: verify and reuse Typeractive-style switch/module/mechanical geometry, apply our tested wiring, fit the left flash/battery arrangement and actual right nice!view interface, then route and run native ERC/DRC/parity. No new completed/routed PCB is claimed by this scope draft. Private visibility and source attribution stay unchanged.
