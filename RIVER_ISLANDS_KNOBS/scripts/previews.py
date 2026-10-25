import sys; sys.path.insert(0,".")
from field import *
from matplotlib.collections import PolyCollection
from matplotlib.colors import LightSource
from scipy.interpolate import RegularGridInterpolator
def mesh(R,rn,a,Z,dr=0.1,nth=1500):
    f=RegularGridInterpolator((a,a),Z,bounds_error=False,fill_value=0.0)
    th=np.linspace(0,2*np.pi,nth,endpoint=False); s=np.sqrt(.5)*.3
    P=[(0,0),(rn-.3,0)]+[(rn-.3+.3*np.sin(x),.3-.3*np.cos(x)) for x in np.linspace(0,np.pi/2,6)[1:]]+[(rn,19.7)]
    P+=[(rn+.3-.3*np.cos(x),19.7+.3*np.sin(x)) for x in np.linspace(0,np.pi/2,6)[1:]]+[(R-.3,20.0)]
    P+=[(R-.3+.3*np.sin(x),20.3-.3*np.cos(x)) for x in np.linspace(0,np.pi/2,6)[1:]]
    V=[(rr*np.cos(t),rr*np.sin(t),zz) for rr,zz in P for t in th]; nP=len(P); K=int(round(R/dr))
    for rr in np.linspace(0,R,K+1)[1:]:
        xs,ys=rr*np.cos(th),rr*np.sin(th); V+=list(zip(xs,ys,27.0+f(np.column_stack([ys,xs]))))
    V=np.array(V); T=[]
    def band(i0,i1,flip):
        for j in range(nth):
            j2=(j+1)%nth; A,B,C,D=i0*nth+j,i0*nth+j2,i1*nth+j2,i1*nth+j
            T.extend([(A,C,B),(A,D,C)] if flip else [(A,B,C),(A,C,D)])
    for i in range(nP-1): band(i,i+1,False)
    for k in range(K-1): band(nP+k,nP+k+1,True)
    band(nP-1,nP+K-1,False)
    for j in range(nth): T.append((nP*nth+j,nP*nth+(j+1)%nth,nP*nth+j))  # tiny centre ring, closes up visually
    return V,np.array(T)
def render3d(V,T,t_deg,path,title,D):
    tri=V[T]; n=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]); ln=np.linalg.norm(n,axis=1); ok=ln>1e-12; tri,n,ln=tri[ok],n[ok],ln[ok]; n/=ln[:,None]
    t=np.radians(t_deg); c=tri.mean(1); dep=c[:,1]*np.cos(t)-c[:,2]*np.sin(t)
    face=(-n[:,1]*np.cos(t)+n[:,2]*np.sin(t))>-0.05; o=np.argsort(-dep); o=o[face[o]]
    Ld=np.array([-.45,.45,.77]); Ld/=np.linalg.norm(Ld); Lf=np.array([.4,-.3,.4]); Lf/=np.linalg.norm(Lf)
    I=np.clip(n@Ld,0,1)*0.8+np.clip(n@Lf,0,1)*0.25
    base=np.array([0.86,0.66,0.34]); col=np.clip(base[None,:]*(0.30+0.85*I[:,None]),0,1)
    X=tri[:,:,0]; Vv=tri[:,:,1]*np.sin(t)+tri[:,:,2]*np.cos(t)
    fig,ax=plt.subplots(figsize=(9,7.2)); ax.set_facecolor("#e9e9ea"); fig.patch.set_facecolor("#e9e9ea")
    ax.add_collection(PolyCollection(np.stack([X,Vv],-1)[o],facecolors=col[o],edgecolors=col[o],linewidths=0.1))
    ax.set_xlim(-D*0.55,D*0.55); ax.set_ylim(-D*0.5-(10 if t_deg<0 else 0),D*0.5+27); ax.set_aspect("equal"); ax.axis("off"); ax.set_title(title,fontsize=12)
    fig.tight_layout(); fig.savefig(path,dpi=140); plt.close(fig)
def topview(R,a,Z,path,title):
    X,Y=np.meshgrid(a,a); r=np.hypot(X,Y)
    I=LightSource(315,40).hillshade(Z,vert_exag=10,dx=a[1]-a[0],dy=a[1]-a[0]); I=(I-I.min())/(I.max()-I.min()+1e-9)
    sh=np.ones(Z.shape+(4,)); sh[...,:3]=np.clip(np.array([0.88,0.68,0.36])[None,None,:]*(0.30+0.80*I[...,None]),0,1)
    sh[r>R]=[0.91,0.91,0.92,1.0]
    fig,ax=plt.subplots(figsize=(8,8)); ax.imshow(sh,extent=[-R,R,-R,R],origin="lower"); ax.axis("off"); ax.set_title(title,fontsize=12)
    ax.add_patch(plt.Circle((0,0),R,fill=False,ec="#333",lw=0.8)); fig.tight_layout(); fig.savefig(path,dpi=130); plt.close(fig)
def make_previews(D,rn,folder,tag):
    R=D/2; a,Z=field(R,sigma=3.0); Zm=np.where(np.hypot(*np.meshgrid(a,a))<=R,Z,0)
    topview(R,a,Zm,f"{folder}/{tag}_preview_top_view.png",f"Ø{D} mm  River Islands  (top view, max depth 0.5 mm)")
    V,T=mesh(R,rn,a,Z)
    render3d(V,T,38,f"{folder}/{tag}_preview_3D_top.png",f"Ø{D} x H27  River Islands  3D (true scale)",D)
    render3d(V,T,-34,f"{folder}/{tag}_preview_3D_underside.png",f"Ø{D} x H27  underside and neck Ø{2*rn:g}",D)
if __name__=="__main__":
    import os; os.makedirs("/tmp/pv",exist_ok=True); make_previews(38.1,4.5,"/tmp/pv","KNOB_D38.1")
