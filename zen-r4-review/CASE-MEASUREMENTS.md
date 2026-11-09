# Case measurements from the six-column Zen archive

The print-ready STLs give us the window, stepped floor and rear connector cutouts. The case was sliced with its matching bottom plate in archive coordinates. These are **early/V1 CAD dimensions**, not measurements of the physical V2 shell. All distances are in millimeters.

| Feature | Archived dimensions |
| --- | --- |
| Right viewing throat | 14.82 wide × 22.28 long |
| Right pocket below the viewing ledge | 21.00 wide × 54.66 long (bounding box) |
| Gap behind nominal PCB, right viewing center | 0.459 |
| Gap behind nominal PCB, right pocket, selected points | 0.425 over a raised floor feature; 1.395, 1.995 and 2.835 elsewhere |
| Rear USB opening, left | 8.90 wide × 3.10 high |
| Rear USB opening, right | 8.90 wide × 3.12 high |
| USB sill below nominal PCB top, left / right | 3.30 / 3.37 |
| USB roof below nominal PCB top, left / right | 0.20 / 0.26 |

USB width is measured across the middle of each rounded slot, at z = 0 in the rear section y = 42.0. Height is at the slot's center. The lower sill is formed by the bottom plate in that section. Rounded corners and the wall bevel mean this is not a rectangular connector clearance gauge. The actual nice!nano and cable housing still need a placement check before filing.

A cropped screen is acceptable. **The raised bottom plate is now the limiting feature for a flat display fully behind the PCB.** To test this without assuming the nice!view is uniformly 2.9 mm thick, use its 14 × 36 mm board footprint and the larger lower pocket as a bounding rectangle. Every flat, long-axis-aligned placement wholly within those bounds includes x = 24.154, y = 15.0. The archived floor leaves only **0.425 mm** behind the nominal PCB at that point. The [nice!view dimension drawing](https://nicekeyboards.com/docs/nice-view/pinout-schematic/) shows a **1.0 mm** display carrier alone. This rules out that mounting arrangement in the archived case before adding the panel, components, solder, or insulation. It does not rule out nesting the display partly into a redesigned PCB opening or a differently shaped V2 floor.

**Superseded physical-check request:** The user has since confirmed socket/case closure after PCB trimming and underside nice!nano fit with a modified base. Do not request these again. The following was the earlier check: the floor about **9 mm toward the thumbs from the viewing-window center**, with the bottom plate installed, and the actual connector-to-case alignment once the controller is held at its intended height. There is no need to remeasure the whole case. The display remains omitted until a workable mounting position is confirmed.

[Raw measurement coordinates](case-measurements.json) · [Display overlay](right-display-fit.png)

**Current scope:** the V2 metal window measures 22.46 × 14.00 mm. Cropping is accepted and the plastic base is redesignable. The preceding fixed-floor bounds do not reject the current plan. See README.md for current decisions.
