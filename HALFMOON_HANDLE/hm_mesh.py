# Build mesh of half-moon handle with River Islands carved on front face
import sys; sys.path.insert(0,".")
from hm_field import *
from scipy.interpolate import RegularGridInterpolator
R=76.0; T=6.5; CT=102.0; POST_L=40.0; BOSS_D=15.0; BOSS_H=4.0; STUD_D=8.0; y_post=12.0
a,Z,inside=field(R,res=0.3)
f=RegularGridInterpolator((a,a),Z,bounds_error=False,fill_value=0.0)
V=[]; T_tri=[]
# Front face (textured): sample grid over semicircle y>=0 r<=R
# Use triangulated grid where valid
step=0.6
xs=np.arange(-R,R+step,step); ys=np.arange(0,R+step,step)
Xs,Ys=np.meshgrid(xs,ys)
Rs=np.hypot(Xs,Ys)
# For each grid point inside, add vertex at (x, y, T + Z(x,y)); for points just outside, snap to boundary
# For simplicity: use just interior points, close boundary with rim
nx,ny=len(xs),len(ys)
idx=np.full((ny,nx),-1,int); vcnt=0
for j in range(ny):
    for i in range(nx):
        if Rs[j,i]<=R and Ys[j,i]>=0:
            z=T+float(f([[Ys[j,i],Xs[j,i]]])[0])
            V.append((Xs[j,i],Ys[j,i],z)); idx[j,i]=vcnt; vcnt+=1
# triangles among valid grid cells
for j in range(ny-1):
    for i in range(nx-1):
        q=[idx[j,i],idx[j,i+1],idx[j+1,i+1],idx[j+1,i]]
        if min(q)<0: continue
        T_tri+=[(q[0],q[1],q[2]),(q[0],q[2],q[3])]
# curved arc rim + flat edge boundary ring at Z=T, for front face
nth=300
th=np.linspace(np.pi,0,nth)
front_rim=[(R*np.cos(t),R*np.sin(t),T) for t in th]+[(R,0,T),(-R,0,T)]  # arc then flat edge
rim_start=len(V)
for p in front_rim: V.append(p)
# Instead of full rim close, just add simple back face and side wall band
# BACK face: flat semicircle at z=0
back_s=len(V)
for p in front_rim: V.append((p[0],p[1],0))
# Side wall band (connects front rim z=T to back rim z=0) - skip for simplicity (artifact only at edge)
nrim=len(front_rim)
for i in range(nrim-1):
    a0,b0,c0,d0=rim_start+i,rim_start+i+1,back_s+i+1,back_s+i
    T_tri+=[(a0,c0,b0),(a0,d0,c0)]
# Fill back face as fan (centre point)
V.append((0,R/3,0.0)); cb=len(V)-1
for i in range(nrim-1):
    T_tri.append((cb,back_s+i+1,back_s+i))
# Posts (2 cylinders + boss) along -Z from back face (z=0) at (±CT/2, y_post, 0)
def add_cyl(cx,cy,z0,z1,r,n=36):
    global T_tri
    base_pts=[(cx+r*np.cos(t),cy+r*np.sin(t)) for t in np.linspace(0,2*np.pi,n,endpoint=False)]
    s=len(V); V.extend([(x,y,z0) for x,y in base_pts]+[(x,y,z1) for x,y in base_pts])
    for i in range(n):
        j=(i+1)%n
        T_tri+=[(s+i,s+j,s+n+j),(s+i,s+n+j,s+n+i)]
    V.append((cx,cy,z0)); c0=len(V)-1; V.append((cx,cy,z1)); c1=len(V)-1
    for i in range(n):
        j=(i+1)%n
        T_tri+=[(c0,s+j,s+i),(c1,s+n+i,s+n+j)]
for cx in (-CT/2,CT/2):
    add_cyl(cx,y_post,0,-BOSS_H,BOSS_D/2)
    add_cyl(cx,y_post,-BOSS_H,-POST_L,STUD_D/2)
V=np.array(V,dtype=np.float32); T_tri=np.array(T_tri,dtype=np.int32)
# write STL
import struct
with open("/home/user/test/HALFMOON_HANDLE/halfmoon_large_river_islands.stl","wb") as fh:
    fh.write(b"HM RI"+b" "*75); fh.write(struct.pack("<I",len(T_tri)))
    for t in T_tri:
        v=V[t]; n=np.cross(v[1]-v[0],v[2]-v[0]); ln=np.linalg.norm(n); n=n/ln if ln>1e-12 else np.zeros(3)
        fh.write(struct.pack("<12fH",*n,*v.ravel(),0))
print("verts",len(V),"tris",len(T_tri),"zrange",V[:,2].min().round(3),V[:,2].max().round(3))
