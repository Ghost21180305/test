# Realistic render of what LEFT and RIGHT handle will look like after machining
import sys; sys.path.insert(0,".")
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import LightSource
from hm_pair import full_field
R=76.0

# Use the actual field data to render the finished front face (with proper depth visualization)
a,Z,inside,Xf,Yf,rf=full_field()
res=a[1]-a[0]

# Three light setup for realistic brass look
def shade_brass(Z,ins,az=315,el=35,exag=18):
    ls=LightSource(azdeg=az,altdeg=el)
    I=ls.hillshade(Z,vert_exag=exag,dx=res,dy=res); I=(I-I.min())/(I.max()-I.min()+1e-9)
    # Specular highlight on the raised flats
    flat_mask=(Z>-0.05)&ins
    sh=np.ones(Z.shape+(4,))
    brass=np.array([0.92,0.74,0.42])
    sh[...,:3]=np.clip(brass[None,None,:]*(0.35+0.75*I[...,None]),0,1)
    # specular on islands
    sh[flat_mask,:3]=np.clip(sh[flat_mask,:3]*1.15+0.05,0,1)
    # dark channels get a touch darker
    deep_mask=(Z<-0.3)&ins
    sh[deep_mask,:3]*=0.85
    sh[~ins]=[0,0,0,0]  # transparent
    return sh

sh_full=shade_brass(Z,inside)
left_sh=sh_full.copy(); left_sh[Xf>0]=[0,0,0,0]
right_sh=sh_full.copy(); right_sh[Xf<0]=[0,0,0,0]
# Opaque backgrounds for the standalone previews
left_bg=left_sh.copy(); left_bg[left_bg[...,3]==0]=[0.96,0.95,0.93,1.0]
right_bg=right_sh.copy(); right_bg[right_bg[...,3]==0]=[0.96,0.95,0.93,1.0]

fig=plt.figure(figsize=(17,10),facecolor="white")

# LEFT handle finished (big)
ax=fig.add_subplot(2,2,1); ax.set_facecolor("white")
ax.imshow(left_bg,extent=[-R,R,-R,R],origin="lower")
ax.set_xlim(-R-5,2); ax.set_ylim(-R-5,R+5); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("LEFT handle  (machine ma thi nikdya pachi)",fontsize=13,weight="bold",color="#333")

# RIGHT handle finished
ax=fig.add_subplot(2,2,2); ax.set_facecolor("white")
ax.imshow(right_bg,extent=[-R,R,-R,R],origin="lower")
ax.set_xlim(-2,R+5); ax.set_ylim(-R-5,R+5); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("RIGHT handle  (machine ma thi nikdya pachi)",fontsize=13,weight="bold",color="#333")

# Both handles together - the final look when mounted on doors
ax=fig.add_subplot(2,1,2); ax.set_facecolor("#f8f6f0")
GAP=3.0
# Draw door hints
dw,dh=240,200
ax.add_patch(plt.Rectangle((-dw-GAP/2,-dh/2),dw,dh,fc="#c7a66e",ec="#6b522b",lw=2,alpha=0.5))
ax.add_patch(plt.Rectangle((GAP/2,-dh/2),dw,dh,fc="#c7a66e",ec="#6b522b",lw=2,alpha=0.5))
# Install handles with gap
ax.imshow(left_sh,extent=[-R-GAP/2,R-GAP/2,-R,R],origin="lower",zorder=5)
ax.imshow(right_sh,extent=[-R+GAP/2,R+GAP/2,-R,R],origin="lower",zorder=5)
# central gap line
ax.plot([0,0],[-dh/2,dh/2],color="#6b522b",lw=1.5,zorder=6)
ax.text(-dw/2-GAP/2,-dh/2-15,"LEFT door",ha="center",fontsize=11,color="#333",weight="bold")
ax.text(dw/2+GAP/2,-dh/2-15,"RIGHT door",ha="center",fontsize=11,color="#333",weight="bold")
ax.text(0,R+15,"doors closed  -  design flows across the 3 mm gap",ha="center",fontsize=11,color="#333",style="italic")
ax.set_xlim(-dw-GAP/2-15,dw+GAP/2+15); ax.set_ylim(-dh/2-30,dh/2+25); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("INSTALLED on double doors  (production result)",fontsize=14,weight="bold",color="#222")

fig.suptitle("MACHINE PROGRAM NU RESULT  -  LEFT ane RIGHT handle finished look",fontsize=15,weight="bold",y=0.995)
fig.tight_layout(); fig.savefig("/home/user/test/HALFMOON_PAIR/FINAL_RESULT_LEFT_RIGHT.png",dpi=150); print("ok")
