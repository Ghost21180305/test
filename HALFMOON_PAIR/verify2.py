import sys; sys.path.insert(0,".")
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from hm_pair import half
R=76.0; GAP=3.0
aL,ZL,insL=half('LEFT'); aR,ZR,insR=half('RIGHT')
L_user=np.rot90(ZL,1); R_user=np.rot90(ZR,-1)
insL_u=np.rot90(insL,1); insR_u=np.rot90(insR,-1)
res=aL[1]-aL[0]
def shade(Z,ins):
    I=LightSource(315,40).hillshade(Z,vert_exag=14,dx=res,dy=res); I=(I-I.min())/(I.max()-I.min()+1e-9)
    sh=np.ones(Z.shape+(4,)); sh[...,:3]=np.clip(np.array([0.92,0.74,0.42])[None,None,:]*(0.30+0.80*I[...,None]),0,1)
    sh[~ins]=[0,0,0,0]
    return sh
fig,axs=plt.subplots(1,2,figsize=(16,8),facecolor="white")
ax=axs[0]; Lsh=shade(L_user,insL_u); Rsh=shade(R_user,insR_u)
ax.imshow(Lsh,extent=[-R-GAP/2,R-GAP/2,-R,R],origin="lower")
ax.imshow(Rsh,extent=[-R+GAP/2,R+GAP/2,-R,R],origin="lower")
ax.set_facecolor("#f5f1e8")
ax.set_xlim(-R-10,R+10); ax.set_ylim(-R-5,R+5); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("Pair preview (NEW connecting River Islands)",fontsize=12,weight="bold")
# For comparison: show the full-circle design
from hm_pair import full_field
a,Z,inside,X,Y,r=full_field()
I=LightSource(315,40).hillshade(Z,vert_exag=14,dx=res,dy=res); I=(I-I.min())/(I.max()-I.min()+1e-9)
sh=np.ones(Z.shape+(4,)); sh[...,:3]=np.clip(np.array([0.92,0.74,0.42])[None,None,:]*(0.30+0.80*I[...,None]),0,1)
sh[~inside]=[1,1,1,1]
axs[1].imshow(sh,extent=[-R,R,-R,R],origin="lower"); axs[1].axvline(0,color="#d00",ls="--",lw=1)
axs[1].set_aspect("equal"); axs[1].axis("off")
axs[1].set_title("Full-circle source design  (lal line par cut thai chhe)",fontsize=12,weight="bold")
fig.tight_layout(); fig.savefig("/home/user/test/HALFMOON_PAIR/CONNECTED_preview.png",dpi=140); print("ok")
