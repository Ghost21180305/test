import sys; sys.path.insert(0,".")
from hm_field import *
from scipy.ndimage import grey_dilation
from scipy.interpolate import RegularGridInterpolator
R=76.0; SAFE=5.0; RET=1.0; APP=0.2; F_FIN=300; F_PLUNGE=120
def tip_surface(a,Z,inside):
    res=a[1]-a[0]; h=np.where(inside,Z,-10.0)
    k=int(np.ceil(RB/res)); o=np.arange(-k,k+1)*res; DX,DY=np.meshgrid(o,o); d=np.hypot(DX,DY); foot=d<=RB
    w=np.where(foot,RB-np.sqrt(np.maximum(RB**2-d**2,0)),0.0)
    t=grey_dilation(h,footprint=foot,structure=-w)
    return RegularGridInterpolator((a,a),np.where(inside,t,0.0),bounds_error=False,fill_value=0.0)
def rdp(P,tol):
    keep=np.zeros(len(P),bool); keep[[0,-1]]=True; st=[(0,len(P)-1)]
    while st:
        i,j=st.pop()
        if j<=i+1: continue
        A,B=P[i],P[j]; dd=B-A; L=np.hypot(*dd)
        dist=np.abs(dd[0]*(P[i+1:j,1]-A[1])-dd[1]*(P[i+1:j,0]-A[0]))/L if L>0 else np.hypot(*(P[i+1:j]-A).T)
        k=dist.argmax()
        if dist[k]>tol: m=i+1+k; keep[m]=True; st+=[(i,m),(m,j)]
    return P[keep]
def runs(f,step,ds=0.08,tol=0.0015):
    out=[]; cs=np.arange(0.5,R,step)   # x-scan at y=c, c>=0.5 (above flat edge)
    for n,c in enumerate(cs):
        L=np.sqrt(max(R*R-c*c,0))
        if L<1: continue
        s=np.linspace(-L,L,int(2*L/ds)+1)
        t=f(np.column_stack([np.full_like(s,c),s]))
        m=t<-0.01
        idx=np.flatnonzero(m)
        if len(idx)==0: continue
        br=np.flatnonzero(np.diff(idx)>1); starts=np.r_[idx[0],idx[br+1]]; ends=np.r_[idx[br],idx[-1]]
        rr=[]
        for a0,b0 in zip(starts,ends):
            a0=max(a0-1,0); b0=min(b0+1,len(s)-1)
            seg=rdp(np.column_stack([s[a0:b0+1],t[a0:b0+1]]),tol); rr.append(seg)
        if n%2: rr=[g[::-1] for g in rr[::-1]]
        out.append((c,rr))
    return out
a,Z,inside=field(R)
f=tip_surface(a,Z,inside)
rows=runs(f,0.25)
# NC header: scanning y=c, varying X, so axis is X
def emit(fh,rows,F):
    length=0; nlift=0; lines=0
    def w(s):
        nonlocal lines; fh.write(s+"\n"); lines+=1
    w(f"F{F}")
    for c,rr in rows:
        for g in rr:
            x0,y0=g[0,0],c
            w(f"G0 Z{RET:.3f}")
            w(f"G0 X{x0:.3f} Y{y0:.3f}")
            w(f"G0 Z{APP:.3f}"); w(f"G1 Z{g[0,1]:.3f} F{F_PLUNGE}"); w(f"F{F}"); nlift+=1
            px,py,pz=x0,y0,g[0,1]
            for s,z in g[1:]:
                x,y=s,c
                length+=np.sqrt((x-px)**2+(y-py)**2+(z-pz)**2)
                w(f"G1 X{x:.3f} Z{z:.3f}"); px,py,pz=x,y,z
            w(f"G0 Z{RET:.3f}")
    return length,nlift,lines
with open("/home/user/test/HALFMOON_HANDLE/HM_LARGE_RI.nc","w") as fh:
    fh.write("%\n( HALF MOON HANDLE LARGE  152x76  RIVER ISLANDS DESIGN )\n")
    fh.write("( TOOL T1: R1.5 BALL NOSE  D3 SHANK  8 FLUTE LEN  50 OAL  4 FLUTE )\n")
    fh.write("( WORK ZERO: X0 = CENTER WIDTH, Y0 = FLAT EDGE, Z0 = FRONT FACE OF PLATE )\n")
    fh.write("( MAX DEPTH 0.4  SPINDLE S24000 FULL RPM  FEED F300 )\n")
    fh.write("G21 G90 G94 G17 G40 G49 G80\nG54\n( T1 = R1.5 BALL NOSE, LOAD BEFORE START )\nS24000 M3\n"+f"G0 Z{SAFE:.3f}\n")
    Lp,nl,ln=emit(fh,rows,F_FIN)
    fh.write(f"G0 Z{SAFE:.3f}\nM5\nG0 X0 Y0\nM30\n%\n")
print("lines",ln,"feed path mm",round(Lp),"feed min",round(Lp/F_FIN,1),"runs/lifts",nl)
