import sys,os; sys.path.insert(0,".")
OUT="/home/user/test/RIVER_ISLANDS_KNOBS"
import mkstep, mknc, previews
for D,rn,code in ((38.0,4.5,"380"),(40.0,4.5,"400")):
    sub=f"{OUT}/D{D}"; os.makedirs(sub,exist_ok=True)
    mkstep.make(D/2,rn,f"{sub}/KNOB_D{D}_RIVER_ISLANDS.step")
    mknc.make_nc(D/2,f"D{D}",f"{sub}/RI{code}.nc")
    previews.make_previews(D,rn,sub,f"KNOB_D{D}")
print("ALL DONE")
