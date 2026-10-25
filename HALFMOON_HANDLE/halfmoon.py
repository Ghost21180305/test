import cadquery as cq
# Half moon handle, LARGE
# Plate: semicircle R76, thickness 6.5
# Mounting posts: 2 nos, centers 102 apart, 40 long
# Post boss: 15 dia (reading side view), stud ~8 dia
# Flat edge of semicircle = bottom (horizontal), posts drop down from flat edge
R=76.0; T=6.5; CT=102.0; POST_L=40.0; BOSS_D=15.0; BOSS_H=4.0; STUD_D=8.0
# Plate stands vertical: X across, Y up (half-moon face in XY plane), posts stick back in -Z.
# Flat edge of semicircle = bottom. Plate thickness T in Z (+Z front, 0 back).
plate=cq.Workplane("XY").moveTo(-R,0).threePointArc((0,R),(R,0)).close().extrude(T)
# Post centers on back of plate: 102 mm apart, raised just above flat edge so the boss doesn't overhang
y_post=12.0
cx1,cx2=-CT/2,CT/2
# boss (short wider flange against the plate's back)
boss=cq.Workplane("XZ").workplane(offset=-y_post).pushPoints([(cx1,-BOSS_H/2),(cx2,-BOSS_H/2)]).circle(BOSS_D/2).extrude(-BOSS_H)
# this is getting messy, rebuild simpler: posts along -Z from plate's back face (Z=0)
plate=cq.Workplane("XY").moveTo(-R,0).threePointArc((0,R),(R,0)).close().extrude(T)
boss=cq.Workplane("XY").workplane(offset=0).pushPoints([(cx1,y_post),(cx2,y_post)]).circle(BOSS_D/2).extrude(-BOSS_H)
stud=cq.Workplane("XY").workplane(offset=-BOSS_H).pushPoints([(cx1,y_post),(cx2,y_post)]).circle(STUD_D/2).extrude(-(POST_L-BOSS_H))
# chamfer plate top edges a touch
asm=plate.union(boss).union(stud)
# M4 grub screw hole into side of boss (approx) — omit for cleanness
sh=asm.val()
print("valid",sh.isValid(),"vol",round(sh.Volume()),"bbox",sh.BoundingBox().xmin,sh.BoundingBox().xmax,sh.BoundingBox().ymin,sh.BoundingBox().ymax,sh.BoundingBox().zmin,sh.BoundingBox().zmax)
import os; os.makedirs("/home/user/test/HALFMOON_HANDLE",exist_ok=True)
cq.exporters.export(asm,"/home/user/test/HALFMOON_HANDLE/halfmoon_large.step")
cq.exporters.export(asm,"/home/user/test/HALFMOON_HANDLE/halfmoon_large.stl",tolerance=0.1,angularTolerance=0.2)
