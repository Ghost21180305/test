import sys,time; sys.path.insert(0,".")
from field import *
import cadquery as cq
from OCP.TColgp import TColgp_Array2OfPnt
from OCP.gp import gp_Pnt
from OCP.GeomAPI import GeomAPI_PointsToBSplineSurface
from OCP.GeomAbs import GeomAbs_C2
from OCP.Approx import Approx_IsoParametric
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCP.BRepFill import BRepFill
from OCP.TopExp import TopExp_Explorer, TopExp
from OCP.TopAbs import TopAbs_EDGE, TopAbs_VERTEX
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool
Z_TOP=27.0; Z_BASE=20.0
def body(R,rn):
    s=np.sqrt(0.5)*0.3
    w=(cq.Workplane("XZ").moveTo(0,0).lineTo(rn-0.3,0)
       .threePointArc((rn-0.3+s,0.3-s),(rn,0.3)).lineTo(rn,19.7)
       .threePointArc((rn+0.3-s,19.7+s),(rn+0.3,20.0)).lineTo(R-0.3,20.0)
       .threePointArc((R-0.3+s,20.3-s),(R,20.3)).lineTo(R,28.5).lineTo(0,28.5).close())
    return w.revolve(360,(0,0,0),(0,1,0))
def textured_block(R,a,Z,sub):
    k=30; Z=np.pad(Z,k,mode='reflect'); h=a[1]-a[0]; a=np.concatenate([a[0]-h*np.arange(k,0,-1),a,a[-1]+h*np.arange(1,k+1)])
    P=Z[::sub,::sub]; xs=a[::sub]; n=len(xs)
    arr=TColgp_Array2OfPnt(1,n,1,n)
    for i in range(n):
        for j in range(n): arr.SetValue(i+1,j+1,gp_Pnt(float(xs[i]),float(xs[j]),Z_TOP+float(P[j,i])))
    t=time.time(); g=GeomAPI_PointsToBSplineSurface(); g.Interpolate(arr,Approx_IsoParametric); srf=g.Surface(); print("  bspline",round(time.time()-t,1),"s")
    top=BRepBuilderAPI_MakeFace(srf,1e-6).Face()
    faces=[cq.Face(top)]; bot=[]; zb=-1.0
    ex=TopExp_Explorer(top,TopAbs_EDGE); edges=[]
    while ex.More(): edges.append(TopoDS.Edge_s(ex.Current())); ex.Next()
    for e in edges:
        v1=TopoDS.Vertex_s(TopExp.FirstVertex_s(e,True)); v2=TopoDS.Vertex_s(TopExp.LastVertex_s(e,True))
        p1,p2=BRep_Tool.Pnt_s(v1),BRep_Tool.Pnt_s(v2)
        q1,q2=cq.Vector(p1.X(),p1.Y(),zb),cq.Vector(p2.X(),p2.Y(),zb)
        E=lambda u,v:cq.Edge.makeLine(u,v)
        top_e=cq.Edge(e); bot_e=E(q1,q2)
        if (top_e.startPoint()-cq.Vector(p1.X(),p1.Y(),p1.Z())).Length>1e-6: top_e=cq.Edge(e.Reversed())
        faces.append(cq.Face.makeRuledSurface(top_e,bot_e)); bot.append(bot_e)
    faces.append(cq.Face.makeFromWires(cq.Wire.assembleEdges(bot)))
    sh=cq.Shell.makeShell(faces); return cq.Solid.makeSolid(sh)
def make(R,rn,path,sub=2):
    t0=time.time(); a,Z=field(R,sigma=3.0); blk=textured_block(R,a,Z,sub)
    kn=cq.Workplane("XY").add(body(R,rn)).intersect(cq.Workplane("XY").add(blk)).val()
    print(" valid",kn.isValid(),"vol",round(kn.Volume()),"bbox z",round(kn.BoundingBox().zmin,2),round(kn.BoundingBox().zmax,2),"faces",len(kn.Faces()),"t",round(time.time()-t0),"s")
    cq.exporters.export(cq.Workplane("XY").add(kn),path); return kn
if __name__=="__main__":
    import sys; make(float(sys.argv[1])/2,float(sys.argv[2])/2,sys.argv[3])
