RIVER ISLANDS KNOBS  D38 ane D40  (top side design)

Files (darek folder ma):
  KNOB_D..._RIVER_ISLANDS.step   3D model (H27, neck dia 9, top par design)
  KNOB_D..._RIVER_ISLANDS.stl    mesh model (CAM / viewer mate, watertight)
  RI380.nc / RI400.nc            G-code (ISO, mm)
  KNOB_D..._preview_*.png        preview images

WHERE_TO_SET_ZERO_X0_Y0_Z0.png  X0 Y0 Z0 kyathi levu tenu image

TOOL     R1.5 ball nose, D3 shank, 8 flute length, 50 OAL, 4 flute
SPINDLE  S24000 full RPM    FEED F200 (plunge F100)    Overrides 100%
WORK ZERO  X0 Y0 = knob center,  Z0 = top face of blank (D38 / D40, 27 mm high)
SAFE Z   +5 mm, travel between cuts +1 mm

PROGRAM  ek j pass, direct full depth sudhi cutting (production mate)
  FINISH SINGLE PASS, stepover 0.15 mm, max depth 0.4 mm, scallop ~0.002 mm
  Pehla roughing nathi. R1.5 ball nose 0.4 mm depth par ekej var ma kaape che.

FEED TIME (feed path / F200, rapid ane Z lift alag)
  D38  about 19.3 min  (3868 mm)
  D40  about 20.9 min  (4174 mm)

NOTES
  - Max depth 0.4 mm. Pattern edge sudhi jay che, border nathi.
  - Tool change line nathi (manual load). Simple ISO G-code.
  - Neck dia 9 mm, fillets 0.3 mm assume karya che. Top edge par 0.3 fillet nathi.
  - Toolpath ma gouge check karyo che (ball footprint). Pehla air-run ane scrap par try karo.
  - STEP: top surface smooth B-spline che, max error lagbhag 0.01 mm.
  - Feed time estimate che. Machine par check nathi karyu.
  - "Full RPM" S24000 lidho che. Tamara spindle no actual max alag hoy to kaho.
