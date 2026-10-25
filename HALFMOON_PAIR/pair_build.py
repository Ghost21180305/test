# Build 2 handles: UPPER (left) ane LOWER (right). Each 152x76 half moon, flat edge bottom.
# Design = top half ane bottom half of a full-circle 152 mm River Islands pattern (begha thai jato continuous).
import sys,os; sys.path.insert(0,".")
from hm_pair import full_field
import numpy as np, struct
from scipy.ndimage import grey_dilation
from scipy.interpolate import RegularGridInterpolator
R=76.0; T=6.5; CT=102.0; POST_L=40.0; BOSS_D=15.0; BOSS_H=4.0; STUD_D=8.0; y_post=12.0
RB=1.5; SAFE=5.0; RET=1.0; APP=0.2; F_FIN=500; F_PLUNGE=180; STEP=0.5
OUT="/home/user/test/HALFMOON_PAIR"; os.makedirs(OUT,exist_ok=True)
a_full,Z_full,ins_full,Xf,Yf,rf=full_field()
res=a_full[1]-a_full[0]
# Handle local frame: flat edge at y=0, semicircle y>=0 (up to R=76).
# For UPPER (LEFT): local Y = world Y (take Y>0 slice directly)
# For LOWER (RIGHT): local Y = -world Y (flip so bottom-of-full becomes top-of-handle)
def half(side):
    if side=="LEFT":   # upper half of full circle
        mask=Yf>=0; Zh=Z_full*mask
    else:              # lower half, flipped vertically
        Z2=Z_full[::-1,:]; mask=(Yf[::-1,:]<=0); Zh=Z2*mask
    # Now Zh is defined on same grid, but valid only in upper half
    insh=mask & ins_full if side=="LEFT" else (Yf[::-1,:]<=0) & ins_full[::-1,:]
    return a_full,Zh,insh
# Mesh builder (reuses hm_mesh logic)
def build_mesh(a,Z,insh,path):
    f=RegularGridInterpolator((a,a),Z,bounds_error=False,fill_value=0.0)
    V=[]; T_tri=[]
    step=0.6; xs=np.arange(-R,R+step,step); ys=np.arange(0,R+step,step)
    Xs,Ys=np.meshgrid(xs,ys); nx,ny=len(xs),len(ys); idx=np.full((ny,nx),-1,int); vc=0
    Rs=np.hypot(Xs,Ys)
    for j in range(ny):
        for i in range(nx):
            if Rs[j,i]<=R and Ys[j,i]>=0:
                z=T+float(f([[Ys[j,i],Xs[j,i]]])[0]); V.append((Xs[j,i],Ys[j,i],z)); idx[j,i]=vc; vc+=1
    for j in range(ny-1):
        for i in range(nx-1):
            q=[idx[j,i],idx[j,i+1],idx[j+1,i+1],idx[j+1,i]]
            if min(q)<0: continue
            T_tri+=[(q[0],q[1],q[2]),(q[0],q[2],q[3])]
    nth=300; th=np.linspace(np.pi,0,nth)
    rim=[(R*np.cos(t),R*np.sin(t),T) for t in th]+[(R,0,T),(-R,0,T)]
    rs=len(V)
    for p in rim: V.append(p)
    bs=len(V)
    for p in rim: V.append((p[0],p[1],0))
    nr=len(rim)
    for i in range(nr-1):
        a0,b0,c0,d0=rs+i,rs+i+1,bs+i+1,bs+i
        T_tri+=[(a0,c0,b0),(a0,d0,c0)]
    V.append((0,R/3,0.0)); cb=len(V)-1
    for i in range(nr-1): T_tri.append((cb,bs+i+1,bs+i))
    def cyl(cx,cy,z0,z1,r,n=36):
        base=[(cx+r*np.cos(t),cy+r*np.sin(t)) for t in np.linspace(0,2*np.pi,n,endpoint=False)]
        s=len(V); V.extend([(x,y,z0) for x,y in base]+[(x,y,z1) for x,y in base])
        for i in range(n):
            j=(i+1)%n; T_tri.extend([(s+i,s+j,s+n+j),(s+i,s+n+j,s+n+i)])
        V.append((cx,cy,z0)); c0=len(V)-1; V.append((cx,cy,z1)); c1=len(V)-1
        for i in range(n):
            j=(i+1)%n; T_tri.extend([(c0,s+j,s+i),(c1,s+n+i,s+n+j)])
    for cx in (-CT/2,CT/2):
        cyl(cx,y_post,0,-BOSS_H,BOSS_D/2); cyl(cx,y_post,-BOSS_H,-POST_L,STUD_D/2)
    V=np.array(V,dtype=np.float32); T_tri=np.array(T_tri,dtype=np.int32)
    with open(path,"wb") as fh:
        fh.write(b"HM pair"+b" "*73); fh.write(struct.pack("<I",len(T_tri)))
        for t in T_tri:
            v=V[t]; n=np.cross(v[1]-v[0],v[2]-v[0]); ln=np.linalg.norm(n); n=n/ln if ln>1e-12 else np.zeros(3)
            fh.write(struct.pack("<12fH",*n,*v.ravel(),0))
    return len(T_tri)
# NC
def tip_surface(a,Z,insh):
    r=a[1]-a[0]; h=np.where(insh,Z,-10.0)
    k=int(np.ceil(RB/r)); o=np.arange(-k,k+1)*r; DX,DY=np.meshgrid(o,o); dd=np.hypot(DX,DY); foot=dd<=RB
    w=np.where(foot,RB-np.sqrt(np.maximum(RB**2-dd**2,0)),0.0)
    t=grey_dilation(h,footprint=foot,structure=-w)
    return RegularGridInterpolator((a,a),np.where(insh,t,0.0),bounds_error=False,fill_value=0.0)
def rdp(P,tol):
    k=np.zeros(len(P),bool); k[[0,-1]]=True; st=[(0,len(P)-1)]
    while st:
        i,j=st.pop()
        if j<=i+1: continue
        A,B=P[i],P[j]; dd=B-A; L=np.hypot(*dd)
        dist=np.abs(dd[0]*(P[i+1:j,1]-A[1])-dd[1]*(P[i+1:j,0]-A[0]))/L if L>0 else np.hypot(*(P[i+1:j]-A).T)
        kk=dist.argmax()
        if dist[kk]>tol: m=i+1+kk; k[m]=True; st+=[(i,m),(m,j)]
    return P[k]
def gen_nc(a,Z,insh,path,tag):
    f=tip_surface(a,Z,insh); rows=[]; cs=np.arange(0.5,R,STEP); ds=0.08
    for n,c in enumerate(cs):
        L=np.sqrt(max(R*R-c*c,0)); 
        if L<1: continue
        s=np.linspace(-L,L,int(2*L/ds)+1); t=f(np.column_stack([np.full_like(s,c),s])); m=t<-0.01
        idx=np.flatnonzero(m)
        if len(idx)==0: continue
        br=np.flatnonzero(np.diff(idx)>1); starts=np.r_[idx[0],idx[br+1]]; ends=np.r_[idx[br],idx[-1]]
        rr=[]
        for a0,b0 in zip(starts,ends):
            a0=max(a0-1,0); b0=min(b0+1,len(s)-1); seg=rdp(np.column_stack([s[a0:b0+1],t[a0:b0+1]]),0.0015); rr.append(seg)
        if n%2: rr=[g[::-1] for g in rr[::-1]]
        rows.append((c,rr))
    Lp=0; nl=0; ln=0
    with open(path,"w") as fh:
        fh.write(f"%\n( HALF MOON {tag}  152x76  RIVER ISLANDS - PAIR SET )\n( TOOL T1: R1.5 BALL NOSE  D3 SHANK  8 FL  50 OAL  4 FLUTE )\n")
        fh.write(f"( WORK ZERO: X0=CENTER WIDTH, Y0=FLAT EDGE, Z0=FRONT FACE )\n( MAX DEPTH 0.4  S24000 FULL RPM  F{F_FIN}  STEPOVER {STEP} )\n")
        fh.write("G21 G90 G94 G17 G40 G49 G80\nG54\n( T1 = R1.5 BALL NOSE, LOAD BEFORE START )\nS24000 M3\n"+f"G0 Z{SAFE:.3f}\n")
        def w(s): nonlocal ln; fh.write(s+"\n"); ln+=1
        w(f"F{F_FIN}")
        for c,rr in rows:
            for g in rr:
                x0,y0=g[0,0],c
                w(f"G0 Z{RET:.3f}"); w(f"G0 X{x0:.3f} Y{y0:.3f}"); w(f"G0 Z{APP:.3f}")
                w(f"G1 Z{g[0,1]:.3f} F{F_PLUNGE}"); w(f"F{F_FIN}"); nl+=1
                px,py,pz=x0,y0,g[0,1]
                for s,z in g[1:]:
                    x,y=s,c; Lp+=np.sqrt((x-px)**2+(y-py)**2+(z-pz)**2)
                    w(f"G1 X{x:.3f} Z{z:.3f}"); px,py,pz=x,y,z
                w(f"G0 Z{RET:.3f}")
        fh.write(f"G0 Z{SAFE:.3f}\nM5\nG0 X0 Y0\nM30\n%\n")
    return Lp,nl,ln
# Build both
import time
for side,fname in (("LEFT","halfmoon_LEFT"),("RIGHT","halfmoon_RIGHT")):
    a,Z,ins=half(side)
    stl=f"{OUT}/{fname}_river_islands.stl"; nc=f"{OUT}/{fname}.nc"
    t0=time.time(); nt=build_mesh(a,Z,ins,stl); 
    t1=time.time(); Lp,nl,ln=gen_nc(a,Z,ins,nc,side); t2=time.time()
    print(f"{side}: tris {nt} ({t1-t0:.0f}s)   NC lines {ln} path {round(Lp)} mm = {round(Lp/F_FIN,1)} min feed ({t2-t1:.0f}s)")
