# Experimental tooling

Open the committed KiCad projects for design discussion. They contain the final reviewed layout. These scripts document how the draft was constructed; they are not an idempotent production build pipeline.

- `r4_geometry.py` recovers geometry from the five retained archived Zen STLs and **resets local outline edits**.
- `build_r4_pcb.py` creates placed boards and DSN inputs and **overwrites routing**. Uses KiCad's bundled Python/pcbnew plus wx; original development path is macOS KiCad 10.
- `r4_layout_schematic.py` expects the original baseline review schematics/library outside this curated snapshot. It is retained as provenance, not a standalone regeneration command.
- `r4_finish.py` imports DSN sessions, adds `checks/manual-routes.json`, applies final changes, normalizes net names/values/footprint identifiers and exports geometry. SES alone is not the final routing. It mutates both boards.
- `r4_complete_routes.py` requires a before-completion airwire report, not the zero-airwire final report. Do not run it against final boards.
- `r4_relieve_outline.py` uses placement errors to add local contour reliefs. Do not run it on final checks without understanding its inputs.
- `r4_base.py`, `r4_front_clearance.py`, `r4_artifacts.py` make prototype bases, sampled front-clearance evidence and fit/preview artifacts. The source geometry is early CAD; outputs do not certify physical V2 fit.
- `r4_board_audit.py` compares exported actual pad memberships with native schematic XML.
- `zen_r4_review.py` depends on historical ZMK build artifacts in a separate firmware workspace. It is provenance, not a portable build command.

Python scientific/mesh dependencies (NumPy, SciPy, Shapely, trimesh, manifold3d, mapbox-earcut, NetworkX, matplotlib, Pillow, kiutils) and local Java/Freerouting runtimes are not vendored. The `compare_geometry.load()` helper also references earlier decoded Typeractive meshes not included here; the STL helpers used for Zen geometry do not need those meshes. Several scripts retain development paths or the original local target-dependency arrangement. Port and review them before rebuilding.

For routine verification use `../r4-layout/run-checks.sh`; it calls the installed KiCad CLI directly. Documentation/image generation does not require rebuilding the boards.
