import sys; sys.path.insert(0,".")
from hm_field import *
import matplotlib, matplotlib.pyplot as plt
matplotlib.use("Agg")
from matplotlib.colors import LightSource
a,Z,inside=field()
X,Y=np.meshgrid(a,a); R=76
I=LightSource(315,40).hillshade(Z,vert_exag=12,dx=a[1]-a[0],dy=a[1]-a[0]); I=(I-I.min())/(I.max()-I.min()+1e-9)
sh=np.ones(Z.shape+(4,)); sh[...,:3]=np.clip(np.array([0.88,0.68,0.36])[None,None,:]*(0.30+0.80*I[...,None]),0,1)
sh[~inside]=[0.91,0.91,0.92,1.0]
fig,ax=plt.subplots(figsize=(12,7),facecolor="white"); ax.imshow(sh,extent=[-R,R,-R,R],origin="lower"); ax.set_xlim(-R-5,R+5); ax.set_ylim(-5,R+5); ax.set_aspect("equal"); ax.axis("off"); ax.set_title("Half Moon LARGE  152x76  River Islands on front face (depth 0.4 mm)",fontsize=12)
fig.tight_layout(); fig.savefig("/home/user/test/HALFMOON_HANDLE/halfmoon_large_RiverIslands_topview.png",dpi=140); print("ok")
