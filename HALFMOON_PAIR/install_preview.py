import sys; sys.path.insert(0,".")
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import matplotlib.patches as mp
from matplotlib.colors import LightSource
from hm_pair import full_field
R=76.0; GAP=3.0
a,Z,inside,Xf,Yf,rf=full_field()
res=a[1]-a[0]
I=LightSource(315,40).hillshade(Z,vert_exag=12,dx=res,dy=res); I=(I-I.min())/(I.max()-I.min()+1e-9)
sh=np.ones(Z.shape+(4,))
# Golden brass colour for handles
sh[...,:3]=np.clip(np.array([0.90,0.72,0.40])[None,None,:]*(0.28+0.80*I[...,None]),0,1)
sh[...,3]=inside.astype(float)
left=sh.copy(); left[Xf>0,3]=0
right=sh.copy(); right[Xf<0,3]=0

fig=plt.figure(figsize=(18,10),facecolor="white")

# ===== MAIN INSTALLED VIEW =====
ax=fig.add_subplot(1,2,1); ax.set_facecolor("#efe8d7")
# Door panels: a typical cabinet door 200x240
dw,dh=200,240
door_fc="#cdb37d"; door_ec="#7d6435"
# wood grain hatching
ax.add_patch(mp.Rectangle((-dw-GAP/2,-dh/2),dw,dh,fc=door_fc,ec=door_ec,lw=2))
ax.add_patch(mp.Rectangle((GAP/2,-dh/2),dw,dh,fc=door_fc,ec=door_ec,lw=2))
# subtle inset bevel on each door
for sx in (-1,1):
    ax.add_patch(mp.Rectangle((sx*GAP/2 + (-dw if sx<0 else 0)+10,-dh/2+10),dw-20,dh-20,fc="none",ec="#8e7645",lw=0.8,ls=":"))
# Place handles: LEFT handle is in world x<=0 range -R to 0; shift so flat edge is at -GAP/2
ax.imshow(left,extent=[-R-GAP/2,R-GAP/2,-R,R],origin="lower",zorder=5)
ax.imshow(right,extent=[-R+GAP/2,R+GAP/2,-R,R],origin="lower",zorder=5)
# gap line
ax.plot([0,0],[-dh/2,dh/2],color="#7d6435",lw=1.5,zorder=6)
# post hole marks (small circles indicating screw positions on back - visible through if transparent, but here just hint)
# door labels
ax.text(-dw/2-GAP/2,-dh/2-14,"LEFT door",ha="center",fontsize=12,color="#333",weight="bold")
ax.text(dw/2+GAP/2,-dh/2-14,"RIGHT door",ha="center",fontsize=12,color="#333",weight="bold")
# gap dim
ax.annotate("",xy=(12,R+22),xytext=(-12,R+22),arrowprops=dict(arrowstyle="<->",lw=1,color="#444"))
ax.text(0,R+28,f"door gap {GAP:.1f} mm",ha="center",fontsize=10,color="#333")
# full-handle width dim
ax.annotate("",xy=(R-GAP/2,-R-20),xytext=(-R-GAP/2,-R-20),arrowprops=dict(arrowstyle="<->",lw=1,color="#333"))
ax.text(0,-R-28,f"{2*R+GAP:.0f} mm total (handles + gap)",ha="center",fontsize=10,color="#333")
ax.set_xlim(-dw-GAP/2-30,dw+GAP/2+30); ax.set_ylim(-dh/2-45,dh/2+25); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("CLOSED DOUBLE DOORS  (coordinated pair, design flows across the gap)",fontsize=13,weight="bold")

# ===== HANDLES ALONE (zoom) =====
ax=fig.add_subplot(2,2,2); ax.set_facecolor("#f3f0ea")
ax.imshow(left,extent=[-R-GAP/2,R-GAP/2,-R,R],origin="lower")
ax.imshow(right,extent=[-R+GAP/2,R+GAP/2,-R,R],origin="lower")
# center ref line
ax.plot([0,0],[-R-5,R+5],color="#555",lw=0.8,ls="--")
# post mark hints (on back, shown as dashed circles)
for yy in (-51,51):
    for sx in (-1,1):
        ax.add_patch(mp.Circle((sx*(45+GAP/2),yy),4,fc="none",ec="#555",ls="--",lw=0.6))
ax.text(0,R+10,"3 mm door gap",ha="center",fontsize=10,color="#444")
ax.text(-R*0.5-GAP/2,-R-15,"LEFT handle",ha="center",fontsize=11,weight="bold",color="#333")
ax.text(R*0.5+GAP/2,-R-15,"RIGHT handle",ha="center",fontsize=11,weight="bold",color="#333")
ax.set_xlim(-R-12,R+12); ax.set_ylim(-R-25,R+22); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("ZOOMED pair  (dashed = post locations on back)",fontsize=11)

# ===== DIM/INFO PANEL =====
ax2=fig.add_subplot(2,2,4); ax2.axis("off")
txt=f"""ASSUMPTIONS (badlvu hoy to kaho):
   Door gap:               3 mm (standard cabinet)
   Handle orientation:     flat edge VERTICAL, facing door gap

EK HANDLE DIMENSIONS:
   Width (flat edge -> arc apex):   76 mm
   Height (along flat edge):       152 mm   
   Thickness:                     6.5 mm
   Posts: 2 nos, back par, 102 mm vertically apart
           40 mm long, 15 dia boss, 8 dia stud

INSTALLATION:
   LEFT handle:  flat edge on jamni baju (facing right door)
   RIGHT handle: flat edge on daabi baju (facing left door)
   Doors closed thatan: handles mal thai jay ane
   design ni channels gap ni aarpar jati dekhay chhe.
   Door khulvamaa 3 mm clearance che, physical contact nathi.

MANUFACTURING (production ready):
   R1.5 ball nose, S40000 full RPM, F500
   Max depth 0.4 mm, single pass, stepover 0.5 (fast)
   Alternative SMOOTH files (stepover 0.15) pan available.
   Program complete thatan Z home + XY home par jay che.

CURRENT FILES ALREADY MATCH THIS PAIR:
   halfmoon_LEFT_*  = full-circle design no left half
   halfmoon_RIGHT_* = full-circle design no right half
   Darek handle alag CNC par chaalavay. Mounting pachi connect thai jay."""
ax2.text(0,0.98,txt,fontsize=10,family="monospace",va="top",ha="left")

fig.suptitle("DOUBLE DOOR PAIR  River Islands  (coordinated LEFT + RIGHT)",fontsize=15,weight="bold",y=0.995)
fig.tight_layout(); fig.savefig("/home/user/test/HALFMOON_PAIR/INSTALLED_double_doors.png",dpi=140); print("ok")
