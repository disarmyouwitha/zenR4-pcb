# Steno Squid

Steno Squid is the active hardware project, a compact QSPI flash accessory for the left expansion header of the Boardsource Wireless Corne SMT. The preferred arrangement connects all eight contacts directly. The existing Adafruit breakout supplies the proof of concept and a comparison circuit.

## Draft 0

Open [the native schematic](draft-0/steno-squid.kicad_sch) or [its SVG](draft-0/steno-squid.svg). KiCad 10.0.7 ERC reports zero violations. This result checks the proposed schematic connections. Connector dimensions, exact flash package and the host supply remain to be verified. Footprints are unassigned.

The first circuit contains W25Q128JV-family flash, 100 nF C1 across its supply, 10 kΩ R1 from CS# to that same switched supply, and an optional 1 µF C2 marked DNP pending rail/inrush review. J1 represents the host interface. Its power-output symbol pins express the assumed host supply, rather than measured rail capability.

## Eight-contact interface

| Host position | Published host signal | Proposed module net | Flash pad |
|---|---|---|---|
| 1 | P0.07 | CS# | 1 |
| 2 | P0.21 | IO0 | 5 |
| 3 | P0.12 | CLK | 6 |
| 4 | P0.23 | IO3 | 7 |
| 5 | Switched VCC | VCC | 8 |
| 6 | GND | GND | 4 |
| 7 | P0.19 | IO1 | 2 |
| 8 | P0.05 | IO2 | 3 |

The host contact assignments are fixed by the keyboard. Assigning CS/CLK/IO0–3 among its six GPIOs remains a design decision. This initial mapping preserves the handoff proposal for discussion. The four adjacent contacts that happen to match one Adafruit row impose no restriction on the custom module. IO2 and IO3 each retain a dedicated signal path.

Boardsource publishes the same contact order on both halves and identifies P0.31 as the VCC control. Its left matrix uses different GPIOs from these six expansion signals. The stock board definition enables SPI2 for a display on P0.23/P0.12 with P0.19 CS. The eventual left firmware must release those display resources and configure QSPI, while preserving the stock matrix. The right can retain its own display configuration. See the [manufacturer repository](https://github.com/boardsource/wireless-corne_zmk_config) and [expansion documentation](https://boardsource.xyz/blogs/guides/wireless-smt-corne-docs).

## Physical compatibility study

The first preference is a flat daughterboard with one matching eight-contact interface and outward-facing SMT components. Once its pitch and mating geometry are verified, compare direct soldered short pins against a low-profile removable header. A small soldered assembly may lower the stack, while a socket provides service access. Both require clearance around nearby components and solder joints. A rigid offset adapter is the fallback if the flash body or case obstructs the direct footprint.

The manufacturer pages and public open-files tree inspected on 2026-11-10 did not supply a dimensioned Wireless Corne expansion interface or its assembled host PCB CAD. The available Unicorne plate files establish plate geometry only. Pitch, hole diameter, pin-1 viewing face, available XY envelope, host antenna location and assembled Z clearance remain unresolved.

For a single straight row, the distance from the first to last contact centers is seven times the pitch. Until that distance is measured, even the connector can dominate the board length. This is the reason to postpone a numerical board outline and 3D fit claim.

The Adafruit four-pin mounting exercise is optional prototype work. The direct eight-contact design receives priority. [Adafruit breakout reference](https://learn.adafruit.com/adafruit-qspi-dip-breakout-boards/downloads)

## Package and BOM review

| Ref | Proposed item | Current selection status |
|---|---|---|
| U1 | W25Q128JV-family 128 Mbit / 16 MB NOR flash | Exact manufacturer ordering code and package drawing required |
| C1 | 100 nF ceramic, X7R, 0603 candidate | Choose voltage rating after rail verification, place next to U1 VCC/GND |
| R1 | 10 kΩ resistor, 1%, 0603 candidate | CS# pull-up to switched VCC |
| C2 | 1 µF ceramic, 0603 candidate | Optional DNP, confirm inrush and supply stability |
| J1 | Eight-contact mating interface | Pitch, drill, insertion direction and height pending |

Adafruit titles product 5634 with “W25Q128JVSSIQ”. That listing alone does not establish a narrower footprint. Winbond explicitly lists W25Q128JVSIQ as a 208-mil SOP-8, and marks that ordering code N, meaning not recommended for new design. Select a current manufacturer-supported ordering code and its actual package drawing before assigning the land pattern or ordering a batch. The bare chips already owned also need their exact suffix checked. [Adafruit product](https://www.adafruit.com/product/5634), [Winbond ordering-code details](https://www.winbond.com/hq/product/code-storage-flash/qspi-nor/w25q-jv/?__locale=en&partNo=W25Q128JVSIQ)

## Power and signal review

The switched-rail voltage, switch/regulator part, polarity, startup timing, discharge behavior and available current have not been established from a host schematic or measurement. W25Q128JVSIQ's specified supply range is 2.7–3.6 V. Measure the expansion rail both on battery and USB and check peak read/program/erase requirements for the selected flash against the host supply circuit. The manufacturer GPIO-control statement alone does not establish those electrical limits. [Winbond specification](https://www.winbond.com/hq/product/code-storage-flash/qspi-nor/w25q-jv/?__locale=en&partNo=W25Q128JVSIQ), [host expansion supply description](https://boardsource.xyz/blogs/guides/wireless-smt-corne-docs)

Route short clock/data paths over a continuous return plane on a two-layer board. Place C1 at the flash supply pins and keep its ground return short. Add test pads where they can be reached without long signal stubs. Confirm host antenna and metal-case clearance before locating copper art or the ground plane. Select the clock rate from the complete host/connector/flash timing and readback tests, including cold start and battery operation.

Firmware must establish safe flash startup, enable quad operation according to the chosen part, and finish outstanding writes before sleep. Before cutting the switched supply, put connected GPIOs into an appropriate low-power state to avoid powering the flash through its signal pins. On wake, restore supply, wait the specified startup interval and reinitialize the flash. Test shutdown current and power-cycle dictionary integrity.

## RGB and visual design

All six available GPIOs are assigned to flash. The first circuit therefore contains the flash and support passives. Independent programmable RGB would require an additional control path or an explicit bus-switching/control design with firmware support. A direct LED connection to a QSPI signal cannot provide independent status control.

Artwork studies can proceed after the board envelope is known. Candidate treatments are a white squid outline on the back, a tiny squid head with tentacles framing the flash, or a quiet name/revision with gold eye details. Decide exposed copper only after checking the host antenna, electrical clearances and touch access. Orientation marking and pin 1 have priority over decoration.

## Assembly strategy and remaining measurements

Use a two-layer board with SMT parts on one accessible face, and inspectable flash joints for the first prototype. Request assembled passives and flash once the BOM is finalized. Select the mating header after checking the delivered keyboard. A removable interface is attractive if its stack fits the plate/case. Soldered short pins remain an alternative for a lower stack.

From the delivered left PCB, record the following with a consistent top-view orientation, USB and seam identified.

1. All eight contact center coordinates, first-to-last span, adjacent pitch and whether they form one row.
2. Hole/drill diameter, pad diameter and existing connector details, if populated.
3. Header position relative to the PCB edge, USB and two fixed landmarks. Confirm which physical end is contact 1 using ground continuity and the manufacturer pinout.
4. Free component space on both faces, including the battery, power/reset controls, nearby components and host antenna.
5. Maximum assembled height with the actual Unicorne plate, switches and case. Include solder tails and insulation.
6. VCC-to-GND voltage with the expansion rail on and off, on battery and USB, followed by regulator/switch identification and load/sequence checks.

Draft 0 supplies the electrical proposal and compatibility investigation. Dimensioned PCB layout, routed copper, purchasable final BOM, 3D/front/back assembly previews and silkscreen variants follow the connector and package checks. Prior keyboard CAD is available in its existing directories. The project remains in the private repository.
