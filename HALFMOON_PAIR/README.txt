HALF MOON PAIR  (LEFT + RIGHT)  with connecting River Islands design

Darek handle:
  Plate: half-moon 152 mm wide x 76 mm tall, 6.5 mm thick (same as original)
  Posts: 2 nos, back par, centers 102 mm apart, 40 mm long, boss 15 dia, stud 8 dia
  Design: River Islands, max depth 0.4 mm, aakha front face par

Bene handle begha mukta full circle 152 mm nu design bane che. Lower handle ne
upside-down mukvo pade (flat edge top), ane upper handle normal rakhvi (flat edge bottom).
Jyare dono flat edges mal thai jay tyare pattern ni channels ek baju thi biji baju vahavi jay.

Files:
  halfmoon_LEFT_river_islands.stl    LEFT handle (UPPER half of design)
  halfmoon_RIGHT_river_islands.stl   RIGHT handle (LOWER half of design, mounted upside-down)
  halfmoon_LEFT.nc                   LEFT handle G-code
  halfmoon_RIGHT.nc                  RIGHT handle G-code
  halfmoon_PLAIN.step                plain half-moon STEP (no design) for reference
  halfmoon_LEFT_preview.png          LEFT 3 views
  halfmoon_RIGHT_preview.png         RIGHT 3 views
  pair_DESIGN_FULL_CIRCLE.png        full circle design (bene handle begha)
  pair_LEFT_RIGHT_topview.png        darek handle alag top view

TOOL     R1.5 ball nose, D3 shank, 8 flute length, 50 OAL, 4 flute
SPINDLE  S24000 full RPM
FEED     F500 (plunge F180)
STEPOVER 0.5 mm  (scallop ~0.021 mm, brushed finish par ok, polished par thodi texture dekhay)
MAX DEPTH  0.4 mm, ek j pass

WORK ZERO  X0 = plate ni width center,  Y0 = flat edge (bottom),  Z0 = plate ni front face
SAFE Z   +5 mm,  cuts vache +1 mm

FEED TIME (per side, feed path / F500, rapid ane lift alag)
  LEFT handle   20.0 min feed  (9987 mm)   total ~24-25 min
  RIGHT handle  18.7 min feed  (9344 mm)   total ~22-23 min

NOTES
  - Target 20 min feed per side che. Rapid, Z lift, tool load, zero setting ni time alag.
  - Design pehla j F300 stepover 0.25 par 66 min hato. Have F500 + stepover 0.5 thi 20 min.
    Scallop 0.021 mm thai gayo, brushed brass par thek. Polished par light stepover texture dekhay.
  - Haju vadhu smooth finish joi e to F300 + stepover 0.25 par chaalavo (per handle ~40 min).
  - Haju vadhu fast joi e to F600 + stepover 0.6 par chaalavo (per handle ~14 min, visible scallop).
  - STEP file (full design valo) banavi nathi shakyo intersection ma kai error aavyo.
    Plain half-moon no STEP mukyo che. Design CAM ma STL mathi joi shako.
  - Pehla air-run ane scrap par try karo. Machine par chalavyu nathi.
