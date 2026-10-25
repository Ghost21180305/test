RIVER ISLANDS KNOBS  D38.1 ane D40.1  (top side design)

Files (darek folder ma):
  KNOB_D..._RIVER_ISLANDS.step   3D model (H27, neck dia 9, top par design)
  RI381.nc / RI401.nc            G-code (ISO, mm)
  KNOB_D..._preview_*.png        preview images

TOOL     R1.5 ball nose, D3 shank, 8 flute length, 50 OAL, 4 flute
SPINDLE  S24000    FEED F200 (plunge F100)    Overrides 100%
WORK ZERO  X0 Y0 = knob center,  Z0 = top face of blank (D38.1 / D40.1, 27 mm high)
SAFE Z   +5 mm, travel between cuts +1 mm

PASSES in each NC file
  1  rough layer Z-0.2, stepover 0.6, stock 0.06
  2  rough layer Z-0.4, stepover 0.6, stock 0.06
  3  finish, stepover 0.15 (scallop about 0.002 mm), follows the surface

FEED TIME (feed path / F200, rapid ane Z lift alag)
  D38.1  about 22.5 min  (4502 mm)
  D40.1  about 24.5 min  (4890 mm)

NOTES
  - Max depth 0.5 mm. Pattern edge sudhi jay che, border nathi.
  - Tool change line nathi (manual load). Controller ni khabar nathi, etle simple ISO G-code che.
  - Neck dia 9 mm, fillets 0.3 mm assume karya che. Top edge par 0.3 fillet nathi.
  - Toolpath ma gouge check karyo che (ball footprint). Machine par pehla air-run ane scrap par try karo.
  - STEP: top surface smooth B-spline che, max error lagbhag 0.01 mm.
  - Feed time estimate che. Machine par check nathi karyu.
