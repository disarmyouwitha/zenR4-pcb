# Primary source check — 2026-11-09

The draft component list is a **candidate architecture**, not a manufacturer-checked full schematic or stock/BOM approval. Datasheets and orderable package variants must be checked during detailed design.

- [Nordic nRF52840 reference circuitry](https://docs.nordicsemi.com/r/bundle/ps_nrf52840/page/ref_circuitry.html): use QIAA package support and reference RF/layout guidance with the actual stack-up.
- [Nordic compatible reference downloads](https://www.nordicsemi.com/products/nrf52840/compatible-downloads): QIAA 1.3 layout/BOM resources.
- [nice!nano pinout/schematic](https://nicekeyboards.com/docs/nice-nano/pinout-schematic/): module pin and switched-supply reference.
- [nice!view pinout/dimensions](https://nicekeyboards.com/docs/nice-view/pinout-schematic/): verify connector orientation and body during the new right design. Our CS is D4, not its generic adapter's D1 default.
- [Worldsemi V6 update](https://www.world-semi.com/web/index.php?classid=22&id=589&lanstr=en&topclassid=19): low-power changes and 3.3 V capability.
- [Manufacturer WS2812C-2020-V6 sheet hosted by LCSC](https://datasheet.lcsc.com/datasheet/pdf/8c7f104c99e52e4adb687ae84e594e95.pdf?productCode=C55109522): exact package/pins, timing, local decoupling and channel current. Do not substitute an older-generation sheet.
- [TI BQ25185](https://www.ti.com/product/BQ25185): candidate standalone power-path charger; evaluate exact low-current settings, chemistry and cell sensing.
- [TI TPS63900](https://www.ti.com/product/TPS63900): candidate regulated system rail; verify external settings/layout/startup.
- [TI TPS22917](https://www.ti.com/product/TPS22917): gate candidate; review suffix/polarity, discharge, leakage and reverse-current behavior.
- [TI SN74LVC1G125](https://www.ti.com/product/SN74LVC1G125): buffer candidate with partial-power-down support; maximum leakage still needs budget review.
- [TI TPD4EUSB30](https://www.ti.com/product/TPD4EUSB30): connector IO ESD candidate; separate VBUS/CC/shield/system-level evaluation is required.

Darryl's restricted archived geometry remains under `references/zen-original/`. These mechanical starter drafts and derived geometry are not cleared for public open-hardware redistribution by their presence in a private repo. Independently authored electronics/art should be separated from restricted reference/derived CAD before public release. Repository visibility/history are unchanged.
