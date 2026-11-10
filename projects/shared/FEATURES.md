> Active project: Nano Independent. Integrated-Zen references below are earlier proposal context; that development is set aside. Draft B implements outline changes only.

# Shared features — proposal, not a new validated circuit

## Preserve signals and make flash optional

`pin-contract.json` preserves all ten tested matrix GPIOs on both halves, six left QSPI signals and the right D4/D2/D3 display reservation. Original working hardware and firmware remain untouched. Integrated package balls are candidates inherited from the earlier mapping; verify them against the chosen package/reference before schematic lock.

Flash population is optional on the **left** of either project. Javelin assembly fits U2, local decoupling and CS bias. Standard assembly leaves flash/support DNP and selects a firmware build that does not require external QSPI initialization, dictionary partitions or a successful JEDEC probe. Host Plover is separate from onboard external-dictionary Javelin. The internal test dictionary path is a development option to inspect, not automatically the desired standard release. No runtime auto-detection is required.

Both halves reuse matrix pin numbers because they contain separate processors. Right scan columns remain reversed; physical thumb cells stay R3C3–5 in the shared outside-to-seam naming.

## RGB electrical proposal

Use the ordered **WS2812C-2020-V6 / C55109522**, conventional DI pin 3 → DO pin 1 chaining, GND pin 2 and VDD pin 4. Preserve exact V6 footprint orientation; a generic WS2812B 2020 land pattern is not accepted without a drawing comparison. Each populated pixel gets local 100 nF decoupling; add a suitably sized local bulk capacitor after inrush review. These are draft choices based on the manufacturer sheet, not completed schematic parts.

Candidate data = P0.10 (nano D16/pad 23), enable = P0.09 (nano D10/pad 24). NFC functionality must be disabled and the ZMK/Zephyr waveform implementation/timing checked; allocating a GPIO does not establish an available SPI/PWM driver. Those pins were spare in Draft A. Integrated firmware gets its own board definition and enable polarity mapping.

Proposed domain: `suitable RGB source → separate hardware gate → RGB_VDD → pixels + power-off-tolerant buffer`. MCU DATA enters the buffer; series damping and a defined low state go at the LED input. Buffer output loses drive when RGB_VDD is off. A **TPS22917** gate and **SN74LVC1G125** Ioff-capable buffer are functional candidates, not final package/leakage selections. Check maximum leakage, powered-off input behavior, startup and low-current alternatives before BOM lock. Ioff support is not zero leakage.

Flash and RGB are separate switched domains. On nano-left, do not use P0.13/module VCC as the per-breath LED switch: flash must remain available according to its existing policy. Reserve the same independence for right display. An enable pulldown keeps the RGB gate off through reset; coordinate data low/high-impedance and buffer state so no MCU signal back-powers an off pixel.

**Supply-margin decision remains open.** Worldsemi's V6 material supports operation down to 3.3 V; a nominal nano 3.3 V rail can be below that under tolerance/drop. Either validate the actual intended module/pixels across operating conditions or design an independently gated regulated RGB source with margin. Do not use unqualified raw LiPo across the entire discharge range. The Zen draft's 3.3 V system rail has the same lower-bound question. A separate converter's shutdown/backfeed, leakage and efficiency must enter the budget.

## One or three LEDs

Default populate the first LED only, with later positions DNP. Three pixels use a contiguous populated chain. A populated pixel downstream of an empty position needs a **documented DIN→DOUT bypass jumper** at every skipped position. Bypass must be open whenever its pixel is installed. One-versus-three stuffing is an assembly option, not an automatic reconnect circuit.

Zen default optics are backside RGB into a translucent plastic-base diffuser. A top-window variant would need a real optical path; a standard upward-emitting package on the underside cannot illuminate through solid PCB. Nano Independent can put LEDs/diffusers where its new case allows.

## Event behavior

Track a stable mode/layer state separate from key scans. On an actual meaningful change, queue one short breath, then send black, put the data path in its safe state and power the RGB domain down. On boot/reconnect, adopt the current synchronized state without repeatedly pulsing an unchanged mode. Coalesce rapid transitions; never let stale animations backlog into seconds of light.

Proposed palette: Javelin purple, host Plover cyan, SYM+NUM amber, ordinary typing off. USB-powered continuous/richer lighting is an explicit optional policy, not battery default. Initial study: 0.5 s breath, peak per-active-channel code 8/255, two active channels. Verify perceptual/gamma behavior and minimum useful visible brightness on actual pixels/diffuser.

The existing mode-sync mechanism is the starting point; neither project has implemented new RGB firmware. Right nice!view default and right RGB-only remain alternative assemblies in this draft. Pins are reserved independently so concurrent right features can be reviewed later without remapping matrix signals.

## Power estimates

`rgb-budget.json` and CSV use a transparent model: 0.2 mA controller overhead **while powered**, 5 mA/channel full scale, PWM duty proportional to the selected code, and a breath with half its peak mean LED brightness. They do not equate the vendor's ≤1 µA standby statement with active controller current.

At 200 half-second transitions/day, estimated RGB-domain charge is **0.0099 mAh/day for one pixel**, **0.0297 mAh/day for three**. This excludes converter inefficiency, enable/settling overhead, gate/buffer leakage and all keyboard/flash/radio/display loads. It is not battery life or a current measurement. Continuous powered-control overhead alone in this conservative model is 4.8 / 14.4 mAh per day for one / three pixels. Characterize actual black/standby/active states; do not promise those model values as measured behavior.

## Squid artwork study

Three vector concepts are supplied under `docs/two-projects/artwork-concepts.svg`: fine white-silk squid, masked tentacle pattern, and selective gold-accent concept. These are review drawings, **not actual copper/solder-mask geometry**. No decorative copper is yet added to either PCB.

Zen: front window artwork, back-mounted electronics/RGB and no screens. Nano Independent: a new case can expose left flash and right screen or RGB as selected. Keep all conductive art away from shell, antenna, switch pads, mounting holes and signal return paths; never use tentacle-shaped signal detours as decoration. Final silk/mask/ENIG dimensions follow the selected fabricator and assembly tolerances.
