import sys; sys.path.insert(0,".")
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
OUT="/home/user/test/HALFMOON_PAIR"
Ld=np.array([-.4,.5,.8]); Ld/=np.linalg.norm(Ld); Lf=np.array([.5,-.3,.4]); Lf/=np.linalg.norm(Lf)
base=np.array([0.88,0.70,0.38])
def render(stl,out,title):
    d=np.fromfile(stl,dtype=[('n','<f4',3),('v','<f4',(3,3)),('a','<u2')],offset=84)
    tri=d['v'].astype(float); n=d['n'].astype(float); nn=np.linalg.norm(n,axis=1); ok=nn>1e-9; tri,n=tri[ok],n[ok]/nn[ok,None]
    I=np.clip(n@Ld,0,1)*0.85+np.clip(n@Lf,0,1)*0.3
    def view(ax,az,el,t):
        a=np.radians(az); e=np.radians(el)
        R1=np.array([[np.cos(a),0,np.sin(a)],[0,1,0],[-np.sin(a),0,np.cos(a)]])
        R2=np.array([[1,0,0],[0,np.cos(e),-np.sin(e)],[0,np.sin(e),np.cos(e)]])
        M=R2@R1; tt=tri@M.T; nr=n@M.T
        cx=tt.mean(1); face=nr[:,2]>-0.02; o=np.argsort(cx[:,2]); o=o[face[o]]
        col=np.clip(base[None,:]*(0.25+0.9*I[:,None]),0,1); ax.set_facecolor("#e9e9ea")
        ax.add_collection(PolyCollection(tt[o][:,:,:2],facecolors=col[o],edgecolors=col[o],linewidths=0.08))
        p=tt.reshape(-1,3); ax.set_xlim(p[:,0].min()-5,p[:,0].max()+5); ax.set_ylim(p[:,1].min()-5,p[:,1].max()+5)
        ax.set_aspect("equal"); ax.axis("off"); ax.set_title(t,fontsize=11)
    fig,axs=plt.subplots(1,3,figsize=(16,6),facecolor="white")
    view(axs[0],0,0,"Front  (design)"); view(axs[1],20,25,"3D view"); view(axs[2],90,0,"Side profile")
    fig.suptitle(title,fontsize=13,weight="bold")
    fig.tight_layout(); fig.savefig(out,dpi=130); plt.close(fig)
render(f"{OUT}/halfmoon_LEFT_river_islands.stl",f"{OUT}/halfmoon_LEFT_preview.png","HALF MOON LEFT  152x76 + River Islands")
render(f"{OUT}/halfmoon_RIGHT_river_islands.stl",f"{OUT}/halfmoon_RIGHT_preview.png","HALF MOON RIGHT  152x76 + River Islands")
print("ok")
