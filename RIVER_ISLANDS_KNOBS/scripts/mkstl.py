import sys
import sys; sys.path.insert(0,'.')
from field import *
from scipy.interpolate import RegularGridInterpolator
OUT="/home/user/test/RIVER_ISLANDS_KNOBS/"
def arc(c,rad,a0,a1,n=8):
    t=np.radians(np.linspace(a0,a1,n)); return [(c[0]+rad*np.cos(x),c[1]+rad*np.sin(x)) for x in t]
def model(R,rn,dr=0.12,nth=1200):
    a,Z=field(R,sigma=3.0); f=RegularGridInterpolator((a,a),Z,bounds_error=False,fill_value=0.0)
    th=np.linspace(0,2*np.pi,nth,endpoint=False)
    # revolve profile (r,z) bottom to shoulder-top; matches the STEP outline (0.3 fillets)
    P=[(0,0),(rn-0.3,0)]+arc((rn-0.3,0.3),0.3,-90,0)[1:]+[(rn,19.7)]+arc((rn+0.3,19.7),0.3,180,90)[1:]+[(R-0.3,20.0)]+arc((R-0.3,20.3),0.3,-90,0)[1:]
    P=[p for i,p in enumerate(P) if i==0 or p!=P[i-1]]
    V=[];idx=lambda i,j:i*nth+j
    for (rr,zz) in P:
        for t in th: V.append((rr*np.cos(t),rr*np.sin(t),zz))
    nP=len(P); K=int(round(R/dr)); rk=np.linspace(0,R,K+1)[1:]
    for rr in rk:
        xs,ys=rr*np.cos(th),rr*np.sin(th); zs=27.0+f(np.column_stack([ys,xs]))
        V+=list(zip(xs,ys,zs))
    V=np.array(V); cb=len(V); V=np.vstack([V,[0,0,0]]); ct=len(V); V=np.vstack([V,[0,0,27.0+float(f([[0,0]])[0])]])
    T=[]; jn=lambda j:(j+1)%nth
    def band(i0,i1,flip=False):
        for j in range(nth):
            a,b,c,d=i0*nth+j,i0*nth+jn(j),i1*nth+jn(j),i1*nth+j
            if flip: T.append((a,c,b));T.append((a,d,c))
            else: T.append((a,b,c));T.append((a,c,d))
    for j in range(nth): T.append((cb,jn(j),j))      # bottom fan (faces -z)
    for i in range(nP-1): band(i,i+1)
    for k in range(K-1): band(nP+k,nP+k+1,True)
    # side wall: ring (R,20.3) -> top rim ring
    band(nP-1,nP+K-1)
    ring0=nP; 
    for j in range(nth): T.append((ct,ring0*nth+j,ring0*nth+jn(j)))  # top fan faces +z
    T=np.array(T)
    return V,T
def vol(V,T):
    a,b,c=V[T[:,0]],V[T[:,1]],V[T[:,2]]; return np.einsum('ij,ij->i',a,np.cross(b,c)).sum()/6
def write_stl(path,V,T):
    a,b,c=V[T[:,0]],V[T[:,1]],V[T[:,2]]; n=np.cross(b-a,c-a); n/=np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-12)
    rec=np.zeros(len(T),dtype=[('n','<f4',3),('v','<f4',(3,3)),('a','<u2')]); rec['n']=n; rec['v']=np.stack([a,b,c],1)
    with open(path,'wb') as fh: fh.write(b'Citadel River Islands knob'.ljust(80,b' ')); fh.write(np.uint32(len(T)).tobytes()); fh.write(rec.tobytes())
for D,rn in ((38.0,4.5),(40.0,4.5)):
    R=D/2; V,T=model(R,rn); v=vol(V,T)
    if v<0: T=T[:,[0,2,1]]; v=-v
    E=np.sort(np.concatenate([T[:,[0,1]],T[:,[1,2]],T[:,[2,0]]]),axis=1); u,cnt=np.unique(E,axis=0,return_counts=True)
    print(f"D{D}: tris {len(T)}, volume {v:.0f} mm3, bad edges {(cnt!=2).sum()}, zmax {V[:,2].max():.2f}")
    write_stl(OUT+f"D{D}/KNOB_D{D}_RIVER_ISLANDS.stl",V,T)
