import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from scipy.spatial import cKDTree, Voronoi
OUT="/home/user/test/knob_designs/"
RB=1.5; D=0.3; HW=np.sqrt(2*RB*D-D*D)
def prof(d):
    z=-(np.sqrt(np.maximum(RB**2-d**2,0))-(RB-D)); return np.where(d<HW,z,0.0)
def resample(P,step=0.1):
    P=np.asarray(P); seg=np.hypot(*np.diff(P,axis=0).T); n=np.maximum((seg/step).astype(int),1)
    return np.vstack([np.linspace(P[i],P[i+1],n[i],endpoint=False) for i in range(len(seg))]+[P[-1:]]),seg.sum()
def clip(P,Rmax):  # keep points inside Rmax
    return P[np.hypot(P[:,0],P[:,1])<=Rmax]
def leaf(R):
    a,b=0.72*R,0.88*R; lines=[]
    lines.append(np.column_stack([np.zeros(200),np.linspace(-R+2.5,0.86*b,200)]))
    y=-0.62*b
    while y<0.72*b:
        h=3.0
        for _ in range(30):
            ye=y+h; xe=0.86*a*np.sqrt(max(1-(ye/b)**2,0)); h=xe*0.95
        ye=y+h
        if xe>3:
            t=np.linspace(0,1,80)[:,None]; P0=np.array([0,y]);P2=np.array([xe,ye]);P1=np.array([xe*0.30,y+h*0.62])
            c=(1-t)**2*P0+2*(1-t)*t*P1+t**2*P2
            lines.append(c); m=c.copy(); m[:,0]*=-1; lines.append(m)
        y+=3.7
    return lines
def wood(R):
    g=np.linspace(-R,R,500); X,Y=np.meshgrid(g,g)
    s=R/25
    f=Y+2.2*s*np.sin(X/(5.5*s)+0.6)+5.5*s*np.exp(-(((X-0.22*R)**2+(Y+0.12*R)**2)/(2*(0.17*R)**2)))
    gy,gx=np.gradient(f,g,g); print("  wood min|grad|",round(np.hypot(gx,gy)[np.hypot(X,Y)<R-2].min(),2))
    lv=np.arange(-R-6,R+6,3.1); cs=plt.contour(X,Y,f,levels=lv); plt.close()
    L=[]
    for segs in cs.allsegs:
        for s_ in segs:
            if len(s_)>5: L.append(s_)
    return L
def pebbles(R):
    rng=np.random.default_rng(7); sp=6.4; P=[]
    for j in range(-8,9):
        for i in range(-8,9):
            p=np.array([i*sp+(j%2)*sp/2,j*sp*0.866])+rng.uniform(-1.3,1.3,2)
            if np.hypot(*p)<R+3.5: P.append(p)
    P=np.array(P)
    ring=R*1.8*np.array([[np.cos(t),np.sin(t)] for t in np.linspace(0,2*np.pi,40,endpoint=False)])
    for _ in range(3):
        V=Voronoi(np.vstack([P,ring])); newP=[]
        for i in range(len(P)):
            reg=V.regions[V.point_region[i]]
            newP.append(V.vertices[reg].mean(0) if -1 not in reg and reg else P[i])
        P=np.array(newP)
    V=Voronoi(np.vstack([P,ring])); L=[]
    for (i,j),rv in zip(V.ridge_points,V.ridge_vertices):
        if -1 in rv or max(i,j)>=len(P)+0 and min(i,j)>=len(P): continue
        a,b=V.vertices[rv[0]],V.vertices[rv[1]]; Rc=R-1.6
        dd=b-a; A=dd@dd; B=2*a@dd; C=a@a-Rc*Rc; disc=B*B-4*A*C
        if disc<=0: continue
        t0=max(0,(-B-np.sqrt(disc))/(2*A)); t1=min(1,(-B+np.sqrt(disc))/(2*A))
        if t1-t0>0.02: L.append(np.array([a+dd*t0,a+dd*t1]))
    th=np.linspace(0,2*np.pi,400); L.append(np.column_stack([(R-1.6)*np.cos(th),(R-1.6)*np.sin(th)]))
    return L
def build(R,fn,res=0.08):
    lines=fn(R); pts=[];Lt=0
    for l in lines:
        l=np.asarray(l); S,len_=resample(l); S=clip(S,R-1.6); pts.append(S); Lt+=len_ if fn is not wood else np.hypot(*np.diff(S,axis=0).T).sum()
    # outside clip lengths approximate
    pts=np.vstack(pts); tree=cKDTree(pts)
    n=int(2*R/res)+1; a=np.linspace(-R,R,n); X,Y=np.meshgrid(a,a); r=np.hypot(X,Y)
    d,_=tree.query(np.column_stack([X.ravel(),Y.ravel()]),distance_upper_bound=HW+0.01)
    Z=prof(d.reshape(X.shape)); Z=np.where(np.isfinite(d.reshape(X.shape)),Z,0.0)
    return X,Y,r,Z,Lt
def render(name,R,fn,title):
    X,Y,r,Z,L=build(R,fn); Zm=np.where(r<=R-0.3,Z,np.nan)
    fig=plt.figure(figsize=(13,6.2)); ax=fig.add_subplot(1,2,1)
    sh=LightSource(315,35).shade(np.nan_to_num(Zm*6),plt.cm.copper,vert_exag=1,dx=.08,dy=.08,blend_mode="soft"); sh[np.isnan(Zm)]=1
    ax.imshow(sh,extent=[-R,R,-R,R],origin="lower"); ax.set_title(f"{title} D{2*R} top view"); ax.axis("off")
    ax=fig.add_subplot(1,2,2); ex=6; t=np.radians(32)
    Zc=np.nan_to_num(Zm); m=r<=R-0.3
    gy,gx=np.gradient(Zc*ex,0.08); nx,ny=-gx,-gy; nn=np.sqrt(nx**2+ny**2+1); Ld=np.array([-.5,.5,.7]); Ld/=np.linalg.norm(Ld)
    I=(nx*Ld[0]+ny*Ld[1]+Ld[2])/nn; base=np.array([0.80,0.55,0.32])
    sel=m.copy()
    px,py,pz,pI=X[sel],Y[sel],ex*Zc[sel],I[sel]
    th=np.linspace(0,2*np.pi,1400); zz=np.arange(-6.0,0.001,0.12)
    TH,ZZ=np.meshgrid(th,zz); sx,sy,sz=(R-.3)*np.cos(TH).ravel(),(R-.3)*np.sin(TH).ravel(),ZZ.ravel()
    sI=np.clip(0.55+0.5*(-np.cos(TH)*0.5+np.sin(TH)*0.5).ravel(),0.2,1)*0.8
    ux=np.concatenate([px,sx]); uy=np.concatenate([py,sy]); uz=np.concatenate([pz,sz]); uI=np.concatenate([pI,sI])
    depth=uy*np.cos(t)-uz*np.sin(t); o=np.argsort(-depth)
    v=uy*np.sin(t)+uz*np.cos(t); col=np.clip(base[None,:]*(0.25+0.85*uI[:,None]),0,1)
    ax.scatter(ux[o],v[o],c=col[o],s=3.2,marker="s",linewidths=0); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(f"3D view, depth drawn {ex}x")
    fig.tight_layout(); fig.savefig(OUT+name+".png",dpi=110); plt.close(fig); return L
for R in (25,19):
    for nm,fn,t in (("leaf",leaf,"Design 3 Leaf"),("woodflow",wood,"Design 4 Wood Flow"),("pebbles",pebbles,"Design 5 River Pebbles")):
        L=render(f"{nm}_D{2*R}",R,fn,t); print(nm,2*R,"path mm",round(L),"min @F200",round(L/200,1))
