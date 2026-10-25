import sys,time; sys.path.insert(0,".")
from pair_build import half, R, RB, SAFE, RET, APP, F_PLUNGE, tip_surface, rdp
import numpy as np
OUT="/home/user/test/HALFMOON_PAIR"
STEP=0.15; F_FIN=500
def gen(a,Z,insh,path,tag,flip):
    f=tip_surface(a,Z,insh); rows=[]; cs=np.arange(0.5,R,STEP); ds=0.08
    for n,c in enumerate(cs):
        L=np.sqrt(max(R*R-c*c,0))
        if L<1: continue
        s=np.linspace(-L,L,int(2*L/ds)+1); t=f(np.column_stack([np.full_like(s,c),s])); m=t<-0.01
        idx=np.flatnonzero(m)
        if len(idx)==0: continue
        br=np.flatnonzero(np.diff(idx)>1); starts=np.r_[idx[0],idx[br+1]]; ends=np.r_[idx[br],idx[-1]]
        rr=[]
        for a0,b0 in zip(starts,ends):
            a0=max(a0-1,0); b0=min(b0+1,len(s)-1); seg=rdp(np.column_stack([s[a0:b0+1],t[a0:b0+1]]),0.0005); rr.append(seg)
        if n%2: rr=[g[::-1] for g in rr[::-1]]
        rows.append((c,rr))
    Lp=0; nl=0; ln=0
    sgn = -1 if flip else 1
    note = "FLAT EDGE TOP, DESIGN -Y" if flip else "FLAT EDGE BOTTOM, DESIGN +Y"
    with open(path,"w") as fh:
        fh.write(f"%\n( HM {tag} SMOOTH  152x76  RIVER ISLANDS )\n( {note} )\n")
        fh.write(f"( R1.5 BALL NOSE  F{F_FIN}  STEPOVER {STEP}  SCALLOP ~0.002 mm )\n")
        fh.write(f"( MAX DEPTH 0.4  S24000 FULL RPM  X0 Y0 = FLAT EDGE CENTER )\n")
        fh.write("G21 G90 G94 G17 G40 G49 G80\nG54\nS24000 M3\n"+f"G0 Z{SAFE:.3f}\n")
        def w(s): nonlocal ln; fh.write(s+"\n"); ln+=1
        w(f"F{F_FIN}")
        for c,rr in rows:
            yc=sgn*c
            for g in rr:
                x0=g[0,0]
                w(f"G0 Z{RET:.3f}"); w(f"G0 X{x0:.3f} Y{yc:.3f}"); w(f"G0 Z{APP:.3f}")
                w(f"G1 Z{g[0,1]:.3f} F{F_PLUNGE}"); w(f"F{F_FIN}"); nl+=1
                px,pz=x0,g[0,1]
                for s,z in g[1:]:
                    Lp+=np.sqrt((s-px)**2+(z-pz)**2)
                    w(f"G1 X{s:.3f} Z{z:.3f}"); px,pz=s,z
                w(f"G0 Z{RET:.3f}")
        fh.write(f"G0 Z{SAFE:.3f}\nM5\nG0 X0 Y0\nM30\n%\n")
    return Lp,nl,ln
for side in ("LEFT","RIGHT"):
    a,Z,ins=half(side)
    for flip,suf in ((False,"_SMOOTH"),(True,"_SMOOTH_downside")):
        Lp,nl,ln=gen(a,Z,ins,f"{OUT}/halfmoon_{side}{suf}.nc",side,flip)
        print(f"{side}{suf}  lines {ln}  path {round(Lp)} mm = {round(Lp/F_FIN,1)} min feed")
