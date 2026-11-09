# Physical V2 photo review and revised mechanical scope

User photos IMG_5225–5231 show the original Zen PCB marked v2.0, component/socket side, opposite display face, and plastic bottom plate. Photos are visual evidence, not calibrated metrology.

- Correction from the user: the original V2 PCB has a square battery opening only, **no display opening**. The earlier interpretation of IMG_5226 as showing a display cutout was incorrect. Any display recess/opening in our replacement PCB would be a new design feature.
- IMG_5225 and IMG_5227 show the socket/component side and the old radio module near the rear inside corner. A backside nice!nano candidate needs a placement/height check; photos do not prove its USB, component or solder clearance.
- IMG_5231 shows the molded plastic floor ribs and pockets. The user explicitly permits removing the raised feature and redesigning/reprinting the plastic bottom plate. The old fixed-floor collision is therefore no longer a design rejection.
- The user accepts cropping the nice!view to the metal window. No need to fit the complete active area through it; place the useful label in the visible region.
- A replacement bottom plate may have an outward pocket if necessary; keep screw seats, battery protection and antenna clearance in the mechanical design.

Current electrical plan: same tested left matrix on both custom halves, left QSPI unchanged, right optional display CS D4/P0.22 (active high), MOSI D2/P0.17, SCK D3/P0.20. Right column scan order is reversed in firmware to preserve physical Corne positions. Candidate firmware with and without display compiles; both review schematics pass ERC; actual custom right hardware is not tested. Display footprint is still pending actual positioning, solder access and height.

Historical pre-confirmation measurement requests are superseded by the user confirmations below. In particular, the original PCB has no display cutout. Use docs/CHATGPT-HANDOFF.md for current next steps.

The new PCB's switch locations will use the Zen geometry; the Ultralight is not the right-board layout constraint. Physical V2 measurements are used to check differences from the early public CAD rather than asking for a complete remeasurement.

## November 9 physical measurements and Typeractive dry fit

User reports:
- Original PCB thickness: **1.65 mm**. Thinner replacement is acceptable in principle, not selected.
- Confirmed metal viewing window: **22.46 × 14.00 mm**. This is not a PCB cutout dimension.
- Typeractive Choc board dry fit is encouraging, with thumb cluster mismatch.
- Updated user confirmation: the nice!nano fits underneath; the plastic backplate needs modification. No numeric module stack height supplied; use this as user-reported physical fit, not a metrology result.
- nice!view is tight; user may enlarge the metal window.

New photos inspected:
- IMG_5236: through top plate, the main-grid center holes appear close to the switch windows. Thumb holes visibly differ. This is not an all-switches installed/latched fit test.
- IMG_5235: underside/socket side with thumb-region screw bosses circled. Preserve the actual Zen boss coordinates and their keepouts; do not copy Typeractive mounting positions. The controller area visible here shows carrier pads; it does not establish clearance for an installed nice!nano, its solder, cable, and closed base.
- IMG_5233: bare nice!view held behind the metal plate, rear with labeled pads visible. This confirms a module is physically available for dry fit. Finger occludes parts; no complete depth evidence.
- IMG_5234: partial active screen visible through the metal opening. Cropped status remains acceptable; mechanical frame/glass clearance, retention and lack of pressure need checking independently of visible pixel area.

Resolved by subsequent user confirmation:
- 22.46 × 14.00 mm is the viewing window.
- The Typeractive Choc hotswap sockets fit the Zen backplate; the case closes with that PCB after trimming its red-circled PCB areas. Treat those reliefs as new-board perimeter/boss keepouts, preserving electrical clearances in our layout.
- The nice!nano fits underneath with a modified backplate. Do not repeatedly request the same dry-fit confirmation. Final manufactured stack still needs allowance for solder, insulation and cable access.
- If thinner PCB is considered, validate Choc switch/plate engagement, socket footprint and support height. Retain 1.65 mm as measured reference; nominal production thickness is still open.

ERC explanation: native schematic rules found no violations in the review sheets, but custom symbol pin types intentionally model many module contacts as passive. It verifies represented connectivity/rules only, not the correctness of the pin map, mechanical fit, radio/charger performance or physical hardware. Separate native netlist-vs-contract checks cover the proposed pin map.

Current mechanical direction: custom Choc PCB with Zen thumb positions and mounting-boss reliefs; backside nice!nano; modified/reprinted plastic base. Keep the measured 1.65 mm original PCB as reference rather than assuming a thinner carrier is required. Nice!view remains an optional placement study: cropped viewing is accepted, but its mounting, solder access, module/PCB overlap and absence of glass pressure are not signed off by the nano/socket fit results.
