# Zen R4 project context

Read `docs/CHATGPT-HANDOFF.md` and `r4-layout/README.md` before design changes. `r4-layout/*.kicad_sch` and `*.kicad_pcb` are authoritative. Experimental generators can overwrite final placement/routing; do not run them just to inspect the project. Preserve tested matrix and QSPI assignments unless the user asks to change them. Keep physical evidence, CAD assumptions, compile checks and unbuilt-PCB rule checks distinct.

Both custom halves use the tested left matrix; right firmware reverses columns. Left has QSPI; right display footprint is absent pending mounting. User accepts cropped display and a modified plastic base. A new USB opening at the current controller position remains an unresolved specific decision. Do not repeat the user's already-confirmed general socket/nano dry-fit questions or invent an original PCB display opening.

Run native ERC, DRC and schematic parity after circuit/layout changes. Update checks, hash snapshot and exported images when the underlying design changes. No manufacturing order or firmware flashing is implied by a documentation/edit request. Preserve third-party attribution; repo initially private.
