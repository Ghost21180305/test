import sys; sys.path.insert(0,".")
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from hm_pair import half, full_field
R=76.0; GAP=3.0

a_full,Z_full,inside_full,Xf,Yf,rf=full_field()
res=a_full[1]-a_full[0]

def shade(Z,ins,exag=14):
    I=LightSource(315,40).hillshade(Z,vert_exag=exag,dx=res,dy=res); I=(I-I.min())/(I.max()-I.min()+1e-9)
    sh=np.ones(Z.shape+(4,))
    sh[...,:3]=np.clip(np.array([0.92,0.74,0.42])[None,None,:]*(0.30+0.80*I[...,None]),0,1)
    sh[~ins]=[0,0,0,0]
    return sh

aL,ZL,insL=half('LEFT'); aR,ZR,insR=half('RIGHT')
L_user=np.rot90(ZL,1); R_user=np.rot90(ZR,-1)
insL_u=np.rot90(insL,1); insR_u=np.rot90(insR,-1)

fig=plt.figure(figsize=(16,10),facecolor="white")

# Top: pair side by side
ax=fig.add_subplot(2,1,1); ax.set_facecolor("#f5f1e8")
Lsh=shade(L_user,insL_u); Rsh=shade(R_user,insR_u)
ax.imshow(Lsh,extent=[-R-GAP/2,R-GAP/2,-R,R],origin="lower")
ax.imshow(Rsh,extent=[-R+GAP/2,R+GAP/2,-R,R],origin="lower")
ax.plot([0,0],[-R,R],color="#555",lw=0.5,ls="--",alpha=0.6)
ax.annotate("3 mm gap",xy=(0,R+6),ha="center",fontsize=9,color="#555")
ax.text(-R*0.5-GAP/2,-R-10,"LEFT handle",ha="center",fontsize=11,weight="bold",color="#333")
ax.text(R*0.5+GAP/2,-R-10,"RIGHT handle",ha="center",fontsize=11,weight="bold",color="#333")
ax.set_xlim(-R-10,R+10); ax.set_ylim(-R-20,R+15); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("NEW: pair preview  -  channels center line par pass thai jay chhe",fontsize=13,weight="bold")

# Bottom left: individual LEFT
ax=fig.add_subplot(2,2,3); ax.set_facecolor("white")
Lsh2=Lsh.copy(); Lsh2[Lsh2[...,3]==0]=[0.95,0.94,0.92,1]
ax.imshow(Lsh2,extent=[-R,R,-R,R],origin="lower"); ax.set_xlim(-R-5,2); ax.set_ylim(-R-3,R+3); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("LEFT handle alone (flat edge daabi baju)",fontsize=11)

# Bottom right: individual RIGHT  
ax=fig.add_subplot(2,2,4); ax.set_facecolor("white")
Rsh2=Rsh.copy(); Rsh2[Rsh2[...,3]==0]=[0.95,0.94,0.92,1]
ax.imshow(Rsh2,extent=[-R,R,-R,R],origin="lower"); ax.set_xlim(-2,R+5); ax.set_ylim(-R-3,R+3); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("RIGHT handle alone (flat edge daabi baju from viewer, left on handle)",fontsize=11)

fig.suptitle("FIX: pattern flat edge sudhi reach kare che + bene handle same field thi sample thai chhe",fontsize=14,weight="bold",y=0.995)
fig.tight_layout(); fig.savefig("/home/user/test/HALFMOON_PAIR/FINAL_v2_LEFT_RIGHT.png",dpi=140); print("ok")
