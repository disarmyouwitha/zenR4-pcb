#!/bin/sh
set -eu
KICAD_CLI="${KICAD_CLI:-/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli}"
cd "$(dirname "$0")"
for half in left right; do
 "$KICAD_CLI" sch erc --format json --exit-code-violations -o "checks/$half-erc.json" "zen-r4-$half.kicad_sch"
 "$KICAD_CLI" pcb drc --schematic-parity --exit-code-violations --format json -o "checks/$half-final-drc.json" "zen-r4-$half.kicad_pcb"
done
