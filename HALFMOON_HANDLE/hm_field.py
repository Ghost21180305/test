# Half-moon river islands field: semicircle radius R, flat edge at y=0, pattern above (y>0)
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.spatial import cKDTree
RB=1.5; MAXD=0.4; HW=np.sqrt(2*RB*MAXD-MAXD*MAXD)
def field(R=76.0,res=0.3,sigma=3.0,seed=11):
    n=int(2*R/res)+1; a=np.linspace(-R,R,n); X,Y=np.meshgrid(a,a); r=np.hypot(X,Y)
    rng=np.random.default_rng(seed); m=180
    from scipy.ndimage import zoom
    f=gaussian_filter(rng.standard_normal((m,m)),9,mode='wrap'); f=zoom(f,n/m,order=3)[:n,:n]; f=(f-f.mean())/f.std()
    g=gaussian_filter(rng.standard_normal((m,m)),12,mode='wrap'); g=zoom(g,n/m,order=3)[:n,:n]; g=(g-g.mean())/g.std()
    gy,gx=np.gradient(f,res); gr=np.maximum(np.hypot(gx,gy),1e-3)
    d=np.abs(f-0.05)/gr
    w=(1.1+0.6*np.clip(g,-1.5,1.5))*(R/25)*0.42+0.5    # scale channel width down for larger handle
    sm=lambda x:x*x*(3-2*x)
    deep=MAXD*sm(np.clip((w-d)/0.9,0,1))
    acc=0.2; xx=np.abs(d-(w+1.5)); az=np.where(xx<np.sqrt(2*RB*acc-acc*acc),(np.sqrt(RB**2-xx**2)-(RB-acc)),0)*(d>w+0.8)
    inside=(r<=R)&(Y>=0.3)
    Z=-np.maximum(deep*inside,az*inside); Z=gaussian_filter(Z,sigma)
    Z[~inside]=0
    return a,Z,inside
