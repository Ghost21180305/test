# River Islands design with CONNECTION FIX: pattern reaches flat edge, both halves sample same field
import numpy as np
from scipy.ndimage import gaussian_filter, zoom
RB=1.5; MAXD=0.4; HW=np.sqrt(2*RB*MAXD-MAXD*MAXD)
def full_field(R=76.0,res=0.2,seed=11,scale=1.0,sigma=0.8):
    n=int(2*R/res)+1; a=np.linspace(-R,R,n); X,Y=np.meshgrid(a,a); r=np.hypot(X,Y)
    rng=np.random.default_rng(seed); m=180
    f=gaussian_filter(rng.standard_normal((m,m)),9,mode='wrap'); f=zoom(f,n/m,order=3)[:n,:n]; f=(f-f.mean())/f.std()
    g=gaussian_filter(rng.standard_normal((m,m)),12,mode='wrap'); g=zoom(g,n/m,order=3)[:n,:n]; g=(g-g.mean())/g.std()
    gy,gx=np.gradient(f,res); gr=np.maximum(np.hypot(gx,gy),1e-3)
    d=np.abs(f-0.05)/gr
    w=(1.1+0.6*np.clip(g,-1.5,1.5))*(R/25)*scale+0.5
    sm=lambda x:x*x*(3-2*x)
    deep=MAXD*sm(np.clip((w-d)/0.9,0,1))
    acc=0.2; xx=np.abs(d-(w+1.5)); az=np.where(xx<np.sqrt(2*RB*acc-acc*acc),(np.sqrt(RB**2-xx**2)-(RB-acc)),0)*(d>w+0.8)
    inside=r<=R-0.3
    Z=-np.maximum(deep*inside,az*inside)
    if sigma>0: Z=gaussian_filter(Z,sigma)
    Z[~inside]=0
    return a,Z,inside,X,Y,r
def half(side):
    a,Z,inside,X,Y,r=full_field()
    R=76.0; res=a[1]-a[0]; nh=int(2*R/res)+1; ah=np.linspace(-R,R,nh)
    Xh,Yh=np.meshgrid(ah,ah)
    if side=='LEFT':
        Xw,Yw=-Yh,Xh   # LEFT handle takes world x<=0 half
    else:
        Xw,Yw=Yh,-Xh   # RIGHT handle takes world x>=0 half
    i=((Xw+R)/res); j=((Yw+R)/res)
    i0=np.clip(i.astype(int),0,nh-2); j0=np.clip(j.astype(int),0,nh-2); fi=i-i0; fj=j-j0
    Zh=((1-fj)*(1-fi)*Z[j0,i0]+(1-fj)*fi*Z[j0,i0+1]+fj*(1-fi)*Z[j0+1,i0]+fj*fi*Z[j0+1,i0+1])
    # Pattern reaches ALL THE WAY to the flat edge (Yh>=0, no 0.5 strip)
    insh=(np.hypot(Xw,Yw)<=R-0.3) & (Yh>=0.0)
    Zh[~insh]=0
    return ah,Zh,insh
