import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
STL="/home/user/test/HALFMOON_HANDLE/halfmoon_large_river_islands.stl"
d=np.fromfile(STL,dtype=[('n','<f4',3),('v','<f4',(3,3)),('a','<u2')],offset=84)
tri=d['v'].astype(float); n=d['n'].astype(float); nn=np.linalg.norm(n,axis=1); ok=nn>1e-9; tri,n=tri[ok],n[ok]/nn[ok,None]
Ld=np.array([-.4,.5,.8]); Ld/=np.linalg.norm(Ld); Lf=np.array([.5,-.3,.4]); Lf/=np.linalg.norm(Lf)
I=np.clip(n@Ld,0,1)*0.85+np.clip(n@Lf,0,1)*0.3
base=np.array([0.88,0.70,0.38])
def view(ax,az,el,title):
    a=np.radians(az); e=np.radians(el)
    R1=np.array([[np.cos(a),0,np.sin(a)],[0,1,0],[-np.sin(a),0,np.cos(a)]])
    R2=np.array([[1,0,0],[0,np.cos(e),-np.sin(e)],[0,np.sin(e),np.cos(e)]])
    M=R2@R1
    t=tri@M.T; nr=n@M.T
    cx=t.mean(1); face=nr[:,2]>-0.02
    o=np.argsort(cx[:,2]); o=o[face[o]]
    col=np.clip(base[None,:]*(0.25+0.9*I[:,None]),0,1)
    ax.set_facecolor("#e9e9ea")
    ax.add_collection(PolyCollection(t[o][:,:,:2],facecolors=col[o],edgecolors=col[o],linewidths=0.08))
    all_pts=t.reshape(-1,3)
    ax.set_xlim(all_pts[:,0].min()-5,all_pts[:,0].max()+5); ax.set_ylim(all_pts[:,1].min()-5,all_pts[:,1].max()+5)
    ax.set_aspect("equal"); ax.axis("off"); ax.set_title(title,fontsize=11)
fig,axs=plt.subplots(2,2,figsize=(14,10),facecolor="white")
view(axs[0,0], 0, 0,   "Front  (design dekhaay che)")
view(axs[0,1], 20, 25, "3D hero view")
view(axs[1,0], 90, 0,  "Side  (plate ni jadai, posts back par)")
view(axs[1,1], 180, 0, "Back  (posts batave che)")
fig.suptitle("Half Moon LARGE  152x76  with River Islands  (depth 0.4 mm)",fontsize=13,weight="bold")
fig.tight_layout(); fig.savefig("/home/user/test/HALFMOON_HANDLE/halfmoon_large_river_islands_preview.png",dpi=130); print("ok")
