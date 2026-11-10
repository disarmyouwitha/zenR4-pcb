# Active scope: Choc Corne + flash

Read `docs/CHATGPT-HANDOFF.md` and `projects/choc-corne-flash/README.md` first. Latest goal: Typeractive-style 42-key Choc Corne, nice!nano, left QSPI flash, right nice!view. Keep this first build small; RGB/artwork and integrated SoC work are deferred. No Zen shell, Zen-specific thumb/cutout/mount geometry or elaborate case adaptation in the active design.

`projects/choc-corne-flash/reference/` is an inferred/unrouted Typeractive model reconstruction, not released original PCB CAD. Use geometry as reference and production-verify footprints/support circuits. Standard donor matrix rows conflict with tested QSPI: preserve the existing tested custom matrix/QSPI plan and right D4-CS display reservation unless the user changes it.

Draft A (`r4-layout/`) and B are historical preserved work; their rule checks do not validate a new design. Working firmware/hardware are unchanged. No fabrication order, public release, visibility change or history rewrite is implied. Keep attribution and private repository settings.

Active implementation is `projects/choc-corne-flash/draft-c/`. Read its README and validation.json. Both nanos FRONT/components DOWN (owner confirmed), J1 wire pads BACK, left QSPI/right actual J2 nice!view. Do not mirror the right module pin banks. Generators overwrite placements/routing; do not rerun casually. Native socket-library normalization is required after board regeneration. Routing is incomplete unless the current native report explicitly proves otherwise.
