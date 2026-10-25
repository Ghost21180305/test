import sys; sys.path.insert(0,".")
from hm_pair import *
import matplotlib, matplotlib.pyplot as plt
matplotlib.use("Agg")
from matplotlib.colors import LightSource
R=76
a,Z,inside,X,Y,r=full_field()
res=a[1]-a[0]
def shade(Zm,insm):
    I=LightSource(315,40).hillshade(Zm,vert_exag=12,dx=res,dy=res); I=(I-I.min())/(I.max()-I.min()+1e-9)
    sh=np.ones(Zm.shape+(4,)); sh[...,:3]=np.clip(np.array([0.88,0.68,0.36])[None,None,:]*(0.30+0.80*I[...,None]),0,1)
    sh[~insm]=[0.91,0.91,0.92,1.0]; return sh
# Joined: full circle
fig,ax=plt.subplots(figsize=(10,10),facecolor="white")
sh=shade(Z,inside); ax.imshow(sh,extent=[-R,R,-R,R],origin="lower")
ax.axvline(0,color='#d00',ls='--',lw=2); ax.text(-R*0.5,R+3,"LEFT handle",ha='center',color='#d00',fontsize=13,weight='bold'); ax.text(R*0.5,R+3,"RIGHT handle",ha='center',color='#d00',fontsize=13,weight='bold')
ax.set_aspect("equal"); ax.axis("off"); ax.set_title("Full design.  Lal line = jyare bene handle begha thai (flat edges together)",fontsize=12)
fig.tight_layout(); fig.savefig("/home/user/test/HALFMOON_HANDLE/pair_JOINED.png",dpi=140)
# Separate: left and right halves shown independently
fig,axs=plt.subplots(1,2,figsize=(14,7),facecolor="white")
Zl=Z.copy(); insl=inside.copy(); insl[:,X[0]>0]=False; Zl[~insl]=0
Zr=Z.copy(); insr=inside.copy(); insr[:,X[0]<0]=False; Zr[~insr]=0
for ax,Zm,insm,t in ((axs[0],Zl,insl,"LEFT handle  (flat edge jamni baju, right)"),(axs[1],Zr,insr,"RIGHT handle  (flat edge daabi baju, left)")):
    ax.imshow(shade(Zm,insm),extent=[-R,R,-R,R],origin="lower"); ax.set_aspect("equal"); ax.axis("off"); ax.set_title(t,fontsize=12)
fig.suptitle("Darek handle alag.  Begha mukta full design bane che.",fontsize=13,weight="bold")
fig.tight_layout(); fig.savefig("/home/user/test/HALFMOON_HANDLE/pair_LEFT_RIGHT_separate.png",dpi=140); print("ok")
