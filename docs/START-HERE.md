# Use this with ChatGPT tomorrow

Upload **CHATGPT-HANDOFF.md** first. Add **01-layout-annotated.png**, **02-system-and-power.png** and **03-nano-top-view-pinmap.png** from `images/`. For a detailed schematic question, also attach `left-controller-detail.png`, `right-controller-detail.png` or either full schematic PNG.

The private GitHub URL may not be readable from another ChatGPT session. Uploading the files provides the actual context. The handoff document includes every critical pin assignment in text; diagrams supplement it.

Paste:

> Read the attached Zen R4 PCB handoff and images. This is my first PCB design. Help me review the unresolved USB opening, underside nano soldering and height, battery/switch access and optional cropped display before ordering. Preserve the tested matrix and left QSPI wiring. Separate physical tests, firmware compile checks, CAD assumptions and electrical rule checks. Let's begin with the next decisions rather than redesigning the processor or pinout.

The upload bundle includes the handoff, diagrams, exact schematic exports and a compact set of native KiCad files/checks. The full repository additionally contains mechanical fit STLs and source CAD.

Files marked PROTOTYPE are for fit studies. Current boards have not been fabricated. No Gerber order package is released.
