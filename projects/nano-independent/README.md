# Nano Independent

Our own nice!nano keyboard and case, using the Zen's 42-key Choc geometry as inspiration. The original metal shell no longer sets the USB opening, controller/solder height, perimeter, display envelope or new-case mounts. Integrated Zen repair work is set aside while the owner asks Darryl about an original spare PCB.

## Current revision

**[Draft B](draft-b/README.md)** is a real routed carrier revision:

- Removed the old rear USB reliefs. USB-C comes from each nice!nano, and the new case will put its opening around that connector.
- Replaced the unmatched right thumb-pad clearance bubble with a continuous chamfer and made both external outlines exact mirrors.
- Preserved all electrical objects and switch centers from checked Draft A. Native ERC, DRC, unconnected and schematic parity checks pass.

The original grid registration has small left/right differences (under 0.10 mm on the main keys); this revision makes the **outline** symmetric without moving footprints or copper. A later canonical-grid change would be a separate electrical/layout revision.

## Continuing design direction

Keep the same tested matrix on both halves, reversed right firmware scan order, optional left QSPI, and a target right nice!view interface (CS D4 active high, MOSI D2, SCK D3). Optional RGB/status pulses and squid artwork remain desired on both halves. These new display/RGB footprints/circuits and artwork are **not yet implemented** in Draft B. See `../shared/FEATURES.md` and `pin-contract.json` for the proposal.

Case design can now provide proper nano solder/socket access, connector strain support, battery retention/insulation, a display pod/bezel, serviceable reset/power and antenna clearance. The old Zen base-pocket files are historical prototypes, not the new case. Existing board mounting holes remain starting references; the new case's mount scheme is still open.

Original working keyboard firmware is untouched. Drafts are private, with restricted reference CAD clearly attributed. No fabrication order or public-release change is implied.
