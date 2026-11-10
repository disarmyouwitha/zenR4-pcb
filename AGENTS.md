# Active project: Nano Independent

Read `docs/CHATGPT-HANDOFF.md` and `projects/nano-independent/draft-b/README.md` first. The owner is pursuing an original spare Zen PCB; integrated Zen replacement development is set aside. Active scope is our nice!nano keyboard with a new case, inspired by Zen geometry.

`projects/nano-independent/draft-b/` contains current routed outline-revision boards and their checks. `r4-layout/` is immutable Draft A comparison data (also tag `draft-a-baseline`); do not overwrite it. Experimental generators can reset geometry or routing. Preserve tested matrix and left QSPI assignments unless requested. Right nice!view, optional RGB/art and flash-DNP firmware remain desired but unimplemented in B.

No original Zen shell/USB/reset/display-window constraints apply to the new case. The old USB reliefs were removed, and outer contours mirrored/blended without moving electrical objects. Do not mirror asymmetric physical socket footprints just to match copper images.

Run native ERC/DRC/parity after circuit/layout changes; distinguish rule checks from physical and hardware validation. Working firmware is untouched. Preserve attribution/restricted CAD and private visibility; no fabrication order, public release or history rewrite is implied.
