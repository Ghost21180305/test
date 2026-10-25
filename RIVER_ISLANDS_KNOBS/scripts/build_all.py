import sys,os,shutil; sys.path.insert(0,".")
OUT="/home/user/test/RIVER_ISLANDS_KNOBS"; os.makedirs(OUT,exist_ok=True)
import mkstep, mknc, previews
res={}
for D,rn,code in ((38.1,4.5,"381"),(40.1,4.5,"401")):
    sub=f"{OUT}/D{D}"; os.makedirs(sub,exist_ok=True)
    mkstep.make(D/2,rn,f"{sub}/KNOB_D{D}_RIVER_ISLANDS.step")
    res[D]=mknc.make_nc(D/2,f"D{D}",f"{sub}/RI{code}.nc")
    previews.make_previews(D,rn,sub,f"KNOB_D{D}")
import json; json.dump({str(k):[float(v[0]),v[1],v[2]] for k,v in res.items()},open("/tmp/nc_stats.json","w"))
print("ALL DONE")
