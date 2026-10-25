RIVER ISLANDS KNOBS  D38 ane D40  (top side design)

Files (darek folder ma):
  KNOB_D..._RIVER_ISLANDS.step   3D model (H27, neck dia 9, top par design)
  KNOB_D..._RIVER_ISLANDS.stl    mesh model (CAM / viewer mate, watertight)
  RI380.nc / RI400.nc            G-code (ISO, mm)
  KNOB_D..._preview_*.png        preview images

WHERE_TO_SET_ZERO_X0_Y0_Z0.png  X0 Y0 Z0 kyathi levu tenu image

TOOL     R1.5 ball nose, D3 shank, 8 flute length, 50 OAL, 4 flute
SPINDLE  S24000 full RPM    FEED F300 (plunge F120)    Overrides 100%
WORK ZERO  X0 Y0 = knob center,  Z0 = top face of blank (D38 / D40, 27 mm high)
SAFE Z   +5 mm, travel between cuts +1 mm

PROGRAM  ek j pass, direct full depth sudhi cutting (production mate)
  FINISH SINGLE PASS, stepover 0.25 mm, max depth 0.4 mm, scallop ~0.005 mm
  Pehla roughing nathi. R1.5 ball nose 0.4 mm depth par ekej var ma kaape che.

FEED TIME (feed path / F300, rapid ane Z lift alag)
  D38  about 7.7 min feed  (2324 mm)   total ~11-12 min
  D40  about 8.3 min feed  (2505 mm)   total ~12-13 min
  BANNE together  about 24 min  (toolchange ane re-zero ma extra time)

NOTES
  - Max depth 0.4 mm. Pattern edge sudhi jay che, border nathi.
  - Stepover 0.25 mm par scallop ~0.005 mm, aankh thi nahi dekhay. Polished brass par thodo texture lage; satin / brushed finish par straight bhanju lage.
  - Tool change line nathi (manual load). Simple ISO G-code.
  - Neck dia 9 mm, fillets 0.3 mm assume karya che. Top edge par 0.3 fillet nathi.
  - Toolpath ma gouge check karyo che (ball footprint). Pehla air-run ane scrap par try karo.
  - STEP: top surface smooth B-spline che, max error lagbhag 0.01 mm.
  - Feed time estimate che. Machine par check nathi karyu.
  - "Full RPM" S24000 lidho che. Tamara spindle no actual max alag hoy to kaho.

JUO VADHU FAST JOI E to:
  - F400 karo, 25% ocho time (pan F300 par bhi edge chip thai shake che, aa thi vadhaare risky)
  - Stepover 0.3 karo, 20% ocho time pan scallop 0.0075 mm, polished finish par dekhay
