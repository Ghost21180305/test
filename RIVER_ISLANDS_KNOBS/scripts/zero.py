import sys; sys.path.insert(0,".")
from previews import *
import matplotlib.patches as mp
R=19.05; a,Z=field(R,sigma=3.0); X,Y=np.meshgrid(a,a); r=np.hypot(X,Y)
I=LightSource(315,40).hillshade(Z,vert_exag=10,dx=a[1]-a[0],dy=a[1]-a[0]); I=(I-I.min())/(I.max()-I.min()+1e-9)
sh=np.ones(Z.shape+(4,)); sh[...,:3]=np.clip(np.array([0.88,0.68,0.36])[None,None,:]*(0.30+0.80*I[...,None]),0,1); sh[r>R]=[1,1,1,0]
fig=plt.figure(figsize=(13,7.2),facecolor="white")
ax=fig.add_axes([0.02,0.06,0.5,0.84]); ax.imshow(sh,extent=[-R,R,-R,R],origin="lower"); ax.set_xlim(-R-9,R+9); ax.set_ylim(-R-5,R+7); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("1) Upar thi jovo (top view):  X0 Y0 = knob nu center",fontsize=13)
ax.add_patch(plt.Circle((0,0),R,fill=False,ec="#222",lw=1.2))
ax.plot([-R-4,R+4],[0,0],color="#d00",lw=1.4,ls="--"); ax.plot([0,0],[-R-3,R+3],color="#d00",lw=1.4,ls="--")
ax.plot(0,0,marker="+",ms=26,mew=3,color="#d00"); ax.text(1.2,1.2,"X0 Y0",color="#d00",fontsize=16,weight="bold")
ax.annotate("",xy=(R+8,-R-3.5),xytext=(R-2,-R-3.5),arrowprops=dict(arrowstyle="->",lw=2.2,color="#06c")); ax.text(R+0.5,-R-1.6,"X +",color="#06c",fontsize=14)
ax.annotate("",xy=(-R-7.5,R+4),xytext=(-R-7.5,R-6),arrowprops=dict(arrowstyle="->",lw=2.2,color="#06c")); ax.text(-R-8.5,R-9,"Y +",color="#06c",fontsize=14)
for (x,y,t,ha) in ((-R,0,"X edge\ntouch 1","right"),(R,0,"X edge\ntouch 2","left"),(0,R,"Y edge touch 1","center"),(0,-R,"Y edge touch 2","center")):
    ax.plot(x,y,"o",color="#080",ms=9); dx=-1.2 if ha=="right" else 1.2 if ha=="left" else 0; dy=3 if ha=="center" and y>0 else -3.6 if ha=="center" else 0
    ax.text(x+dx,y+dy,t,color="#080",fontsize=11,ha=ha,va="center")
ax.text(0,-R-8.3,"Edge finder / indicator thi banne baju touch karo, pachi vachlo point = zero",ha="center",fontsize=11)
# side view
bx=fig.add_axes([0.55,0.06,0.43,0.84]); bx.set_aspect("equal"); bx.axis("off"); bx.set_title("2) Baju thi jovo (side view):  Z0 = upar ni sapati",fontsize=13)
rn=4.5
pts=[(-R,20),(-R,27),(R,27),(R,20),(rn,20),(rn,0),(-rn,0),(-rn,20)]
bx.add_patch(mp.Polygon(pts,closed=True,fc="#e3bd6e",ec="#222",lw=1.4)); bx.set_xlim(-R-4,R+4); bx.set_ylim(-4,48)
bx.plot([-R-3,R+3],[27,27],color="#d00",lw=2,ls="--"); bx.text(R+3.2,27,"Z0",color="#d00",fontsize=17,weight="bold",va="center")
bx.plot(0,27,marker="v",ms=11,color="#d00")
# ball nose tool touching top at centre: ball centre at z=27+1.5
bx.add_patch(mp.Circle((0,28.5),1.5,fc="#9aa4ad",ec="#222",lw=1.2)); bx.add_patch(mp.Rectangle((-1.5,28.5),3,16,fc="#9aa4ad",ec="#222",lw=1.2))
bx.annotate("R1.5 ball nose ni\nsauthi nichli tip\nZ0 par touch",xy=(0.0,27.1),xytext=(6,36),fontsize=12,arrowprops=dict(arrowstyle="->",lw=1.6))
bx.text(0,10,"neck (clamp)",ha="center",fontsize=11,color="#333"); bx.text(0,23.2,"top disc  (7 mm)",ha="center",fontsize=11,color="#333")
bx.text(0,-2.4,"Z0 touch: tool ne flat top face par (pattern ni bahar ni flat jagya par) touch karo",ha="center",fontsize=10.5)
fig.suptitle("Machine zero (G54) kyathi levu:  X0 Y0 Z0",fontsize=16,weight="bold",y=0.985)
fig.savefig("/home/user/test/RIVER_ISLANDS_KNOBS/WHERE_TO_SET_ZERO_X0_Y0_Z0.png",dpi=120); print("ok")
