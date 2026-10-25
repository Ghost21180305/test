import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
OUT="/home/user/test/knob_designs/"
R_BALL=1.5; DEPTH=0.3; HW=np.sqrt(2*R_BALL*DEPTH-DEPTH**2)  # groove half width 0.9
def prof(d):
    z=-(np.sqrt(np.maximum(R_BALL**2-d**2,0))-(R_BALL-DEPTH))
    return np.where(d<HW,z,0.0)
def grid(R,res=0.08):
    n=int(2*R/res)+1; a=np.linspace(-R,R,n); X,Y=np.meshgrid(a,a); return X,Y,np.hypot(X,Y)
def rings(R):
    X,Y,r=grid(R); Z=np.zeros_like(r); pitch=2.6; L=0; rk=3.0; ks=[]
    while rk<=R-1.2: ks.append(rk); rk+=pitch
    for k in ks: Z=np.minimum(Z,prof(np.abs(r-k))); L+=2*np.pi*k
    return X,Y,r,Z,L,len(ks)
def sunburst(R):
    X,Y,r=grid(R); Z=np.zeros_like(r)
    N=int(round(R/19*24/4)*4)  # 24 for D38, 32 for D50
    r0=N*2.4/(2*np.pi); r1=R-3.4; L=0
    th=np.arctan2(Y,X)
    for i in range(N):
        a=2*np.pi*i/N; t=np.clip(X*np.cos(a)+Y*np.sin(a),r0,r1)
        d=np.hypot(X-t*np.cos(a),Y-t*np.sin(a)); Z=np.minimum(Z,prof(d)); L+=r1-r0
    rr=R-1.5; Z=np.minimum(Z,prof(np.abs(r-rr))); L+=2*np.pi*rr
    return X,Y,r,Z,L,N
def render(name,R,fn,title):
    X,Y,r,Z,L,n=fn(R); Z=np.where(r<=R-0.3,Z,np.nan)
    fig=plt.figure(figsize=(13,6.2))
    ax=fig.add_subplot(1,2,1)
    ls=LightSource(azdeg=315,altdeg=35)
    sh=ls.shade(np.nan_to_num(Z*6),plt.cm.copper,vert_exag=1,dx=0.08,dy=0.08,blend_mode="soft")
    sh[np.isnan(Z)]=1
    ax.imshow(sh,extent=[-R,R,-R,R],origin="lower"); ax.set_title(f"{title} D{int(2*R)} top view"); ax.axis("off")
    ax=fig.add_subplot(1,2,2,projection="3d")
    s=3; ex=5
    k=np.minimum(1,(R-0.3)/np.maximum(r,1e-9)); Xc=X*k; Yc=Y*k; Zc=np.nan_to_num(Z)
    ax.plot_surface(Xc[::s,::s],Yc[::s,::s],ex*Zc[::s,::s],facecolors=plt.cm.copper(0.55+0*Zc[::s,::s]),
        lightsource=LightSource(315,30),shade=True,linewidth=0,antialiased=False,rstride=1,cstride=1)
    ax.set_box_aspect((1,1,0.18)); ax.view_init(38,-60); ax.axis("off")
    ax.set_title(f"3D view, depth drawn {ex}x")
    fig.tight_layout(); fig.savefig(OUT+name+".png",dpi=110); plt.close(fig)
    return L,n
for R in (25,19):
    for nm,fn,t in (("ripple",rings,"Design 1 Ripple Rings"),("sunburst",sunburst,"Design 2 Sunburst")):
        L,n=render(f"{nm}_D{2*R}",R,fn,t)
        print(nm,2*R,"count",n,"path mm",round(L),"feed min @F200",round(L/200,1))
