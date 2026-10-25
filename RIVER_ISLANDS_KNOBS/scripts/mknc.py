import sys; sys.path.insert(0,".")
from field import *
from scipy.ndimage import grey_dilation
from scipy.interpolate import RegularGridInterpolator
RB=1.5; SAFE=5.0; RET=1.0; APP=0.2
F_FIN=200; F_ROUGH=200; F_PLUNGE=100
def tip_surface(R,a,Z):
    res=a[1]-a[0]; X,Y=np.meshgrid(a,a); r=np.hypot(X,Y); h=np.where(r<=R,Z,-10.0)
    k=int(np.ceil(RB/res)); o=np.arange(-k,k+1)*res; DX,DY=np.meshgrid(o,o); d=np.hypot(DX,DY); foot=d<=RB
    w=np.where(foot,RB-np.sqrt(np.maximum(RB**2-d**2,0)),0.0)
    t=grey_dilation(h,footprint=foot,structure=-w)
    return RegularGridInterpolator((a,a),np.where(r<=R,t,0.0),bounds_error=False,fill_value=0.0)
def rdp(P,tol):
    keep=np.zeros(len(P),bool); keep[[0,-1]]=True; st=[(0,len(P)-1)]
    while st:
        i,j=st.pop()
        if j<=i+1: continue
        A,B=P[i],P[j]; d=B-A; L=np.hypot(*d)
        dist=np.abs(d[0]*(P[i+1:j,1]-A[1])-d[1]*(P[i+1:j,0]-A[0]))/L if L>0 else np.hypot(*(P[i+1:j]-A).T)
        k=dist.argmax()
        if dist[k]>tol: m=i+1+k; keep[m]=True; st+= [(i,m),(m,j)]
    return P[keep]
def runs(f,R,axis,step,zfun,cond,ds=0.05,tol=0.0015):
    out=[]; cs=np.arange(-R+step/2,R,step)
    for n,c in enumerate(cs):
        L=np.sqrt(max(R*R-c*c,0)); 
        if L<0.1: continue
        s=np.linspace(-L,L,int(2*L/ds)+1)
        pts=np.column_stack([s,np.full_like(s,c)]) if axis=='x' else np.column_stack([np.full_like(s,c),s])
        t=f(pts[:,::-1] if False else np.column_stack([pts[:,1],pts[:,0]]) if False else pts[:,[1,0]])   # interpolator axes are (y,x)
        z=zfun(t); m=cond(t)
        idx=np.flatnonzero(m)
        if len(idx)==0: continue
        br=np.flatnonzero(np.diff(idx)>1); starts=np.r_[idx[0],idx[br+1]]; ends=np.r_[idx[br],idx[-1]]
        rr=[]
        for a0,b0 in zip(starts,ends):
            a0=max(a0-1,0); b0=min(b0+1,len(s)-1)
            seg=rdp(np.column_stack([s[a0:b0+1],z[a0:b0+1]]),tol); rr.append(seg)
        if n%2: rr=[g[::-1] for g in rr[::-1]]
        out.append((c,rr))
    return out
def emit(fh,passes,title):
    st={'x':None,'y':None,'z':None}; length=0; nlift=0; lines=0
    def w(s):
        nonlocal lines; fh.write(s+"\n"); lines+=1
    for name,axis,rows,F in passes:
        w(f"( {name} )"); w(f"F{F}")
        for c,rr in rows:
            for g in rr:
                x0,y0=(g[0,0],c) if axis=='x' else (c,g[0,0])
                w(f"G0 Z{RET:.3f}") if st['z'] is not None and st['z']<RET-1e-6 else None
                w(f"G0 X{x0:.3f} Y{y0:.3f}")
                w(f"G0 Z{APP:.3f}"); w(f"G1 Z{g[0,1]:.3f} F{F_PLUNGE}"); w(f"F{F}"); nlift+=1; st['z']=g[0,1]
                px,py,pz=x0,y0,g[0,1]
                for s,z in g[1:]:
                    x,y=(s,c) if axis=='x' else (c,s)
                    length+=np.sqrt((x-px)**2+(y-py)**2+(z-pz)**2)
                    w(f"G1 "+(f"X{x:.3f} " if axis=='x' else f"Y{y:.3f} ")+f"Z{z:.3f}"); px,py,pz=x,y,z
                st['z']=pz
                w(f"G0 Z{RET:.3f}"); st['z']=RET
    return length,nlift,lines
def make_nc(R,tag,path):
    a,Z=field(R); f=tip_surface(R,a,Z)
    passes=[]
    prev=0.0
    for lay in (-0.2,-0.4):
        pv=prev
        rows=runs(f,R,'y',0.6,lambda t,l=lay:np.maximum(t+0.06,l),lambda t,pv=pv:(t+0.06)<pv-0.01)
        passes.append((f"ROUGH LAYER Z{lay}  STOCK 0.06  STEPOVER 0.6","y",rows,F_ROUGH)); prev=lay
    rows=runs(f,R,'x',0.15,lambda t:t,lambda t:t<-0.01)
    passes.append(("FINISH  STEPOVER 0.15  (SCALLOP 0.002)","x",rows,F_FIN))
    with open(path,"w") as fh:
        fh.write(f"%\n( RIVER ISLANDS KNOB TOP  D{2*R:.1f} )\n( TOOL T1: R1.5 BALL NOSE  D3 SHANK  8 FLUTE LEN  50 OAL  4 FLUTE )\n")
        fh.write("( WORK ZERO: XY = KNOB CENTER, Z = TOP FACE OF BLANK )\n( MAX DEPTH 0.5  SPINDLE S24000  FEED F200 )\n")
        fh.write("G21 G90 G94 G17 G40 G49 G80\nG54\nT1 M6\nS24000 M3\n"+f"G0 Z{SAFE:.3f}\n")
        # emit each pass, count
        tot=0;nl=0;ln=0;perpass=[]
        for p in passes:
            Lp,n,l=emit(fh,[p],p[0]); tot+=Lp; nl+=n; ln+=l; perpass.append((p[0],round(Lp),round(Lp/p[3],1)))
        fh.write(f"G0 Z{SAFE:.3f}\nM5\nG0 X0 Y0\nM30\n%\n")
    print(tag,"lines",ln,"feed path mm",round(tot),"feed min",round(tot/200,1),"runs/lifts",nl,perpass)
    return tot,nl,ln,perpass
if __name__=="__main__": make_nc(19.05,"D38.1","/tmp/test_381.nc")
