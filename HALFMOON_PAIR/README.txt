HALF MOON PAIR  (LEFT + RIGHT) for DOUBLE DOORS
=================================================
Coordinated River Islands design - design flows across the door gap when both doors are closed.

ASSUMPTIONS (badlvu hoy to kaho):
  Door gap:            3 mm (standard cabinet)
  Each handle shape:   half-moon 152 wide x 76 tall (as per original drawing)
  Mounting:            flat edge VERTICAL on each handle, facing the door gap
                       (handle is rotated 90 degrees from the machining orientation
                        before installation)

EK HANDLE PHYSICAL DIMENSIONS
  Across (flat edge -> arc apex):  76 mm   -- goes across the door width
  Along flat edge:                152 mm   -- vertical, parallel to door gap
  Thickness:                      6.5 mm
  Posts: 2 nos on back, 102 mm apart along flat edge direction
         40 mm long, boss 15 dia, stud 8 dia

PAIR CONCEPT
  Design = full-circle River Islands pattern (152 mm dia)
  Vacche thi vertical split karelo:
    LEFT handle  = pattern no left half  -> left door par mounted
    RIGHT handle = pattern no right half -> right door par mounted
  Doors closed thatan bene handle mal thai jay (3 mm gap) ane
  design ni channels gap ni aarpar jati visually dekhay chhe.
  Doors khulvamaa 3 mm clearance che, physical contact nathi.

INSTALLATION ORIENTATION
  LEFT door  -> LEFT handle,  flat edge jamni baju (right side of handle)
  RIGHT door -> RIGHT handle, flat edge daabi baju (left side of handle)
  Both arcs extend outward (away from gap)
  Posts drill holes:  per handle 2 holes, 102 mm vertically apart,
                      centered 51 mm from flat edge (into door)

MACHINING ORIENTATION  (vice ma mukta time)
  Blank ne machine ma mukta time: flat edge NICHE (Y=0), arc UPAR (+Y)
  OR _downside.nc files vaparo to: flat edge UPAR (Y=0), arc NICHE (-Y)
  Machine thai pachi install karva maate 90 deg rotate karo.

FILES
  INSTALLED_double_doors.png                     - installation preview
  halfmoon_LEFT_river_islands.stl                - LEFT handle 3D mesh
  halfmoon_RIGHT_river_islands.stl               - RIGHT handle 3D mesh
  halfmoon_LEFT.nc / halfmoon_RIGHT.nc           - fast NC (flat edge niche)
  halfmoon_LEFT_downside.nc / halfmoon_RIGHT_downside.nc  - fast NC (flat edge upar)
  halfmoon_LEFT_SMOOTH.nc / halfmoon_RIGHT_SMOOTH.nc      - smooth NC (step 0.15)
  halfmoon_LEFT_SMOOTH_downside.nc / halfmoon_RIGHT_SMOOTH_downside.nc
  halfmoon_PLAIN.step                            - plain half-moon STEP
  WHERE_TO_SET_ZERO.png / WHERE_TO_SET_ZERO_downside.png  - setup guides
  halfmoon_LEFT_preview.png / halfmoon_RIGHT_preview.png  - individual previews
  pair_DESIGN_FULL_CIRCLE.png                    - full circle view
  pair_LEFT_RIGHT_topview.png                    - top-view both halves

TOOL / SPEEDS
  Tool:     R1.5 ball nose, D3 shank, 8 flute length, 50 OAL, 4 flute
  Spindle:  S40000 (max RPM)
  Feed:    F500  (plunge F180)   OR  F500 stepover 0.15 (SMOOTH)
  Max depth: 0.4 mm, single pass

FEED TIME (per side; rapid + lift + setup extra)
  Fast variant  (stepover 0.5):   LEFT ~20 min   RIGHT ~19 min
  Smooth variant (stepover 0.15): LEFT ~66 min   RIGHT ~62 min

WORK ZERO
  X0 Y0 = flat edge ni vacche (midpoint of flat edge)
  Z0    = plate ni front face
  Safe Z = +5 mm,  travel between cuts = +1 mm

END OF PROGRAM
  Z lift -> spindle stop -> G28 Z home -> G28 X Y home -> M30

NOTES
  - Pehla air-run karo ane scrap par try karo.
  - Design brass par polished thai pachi, pattern lagbhag reflect kare.
  - 3 mm door gap assumption chhe. Tamara door no actual gap alag hoy
    (jem ke 1.5 mm ke 5 mm) to kaho - handle positioning ferfari daish.
  - Design pattern koi khaas seed par banavo joi e to seed badalvu possible
    (hamnavi aa seed 11 che).
