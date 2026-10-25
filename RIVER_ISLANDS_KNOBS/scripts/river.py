SH=1.4
exec(open("nat.py").read().split("for R in (25,19):")[0].replace("Zm*6","Zm*SH"))
from scipy.ndimage import zoom
from scipy.ndimage import gaussian_filter
def curves(R):
    s=R/25; out=[]
    u=np.linspace(-1.15,1.15,400)
    out.append((np.column_stack([u*R,(0.50-0.42*u+0.20*np.sin(2.7*u+0.5))*R]),1.0))
    v=np.linspace(0,1,300)
    out.append((np.column_stack([(0.05+0.55*v+0.10*np.sin(5*v))*R,(0.05+1.05*v+0.10*np.sin(4*v+1))*R]),0.8))
    out.append((np.column_stack([(-0.35-0.05*v+0.16*np.sin(5*v+2))*R,(-0.15-0.95*v)*R]),0.75))
    out.append((np.column_stack([(0.55+0.5*v)*R,(-0.30-0.6*v+0.07*np.sin(6*v))*R]),0.6))
    return out,s
def build(R,fn=None,res=0.08):
    n=int(2*R/res)+1; a=np.linspace(-R,R,n); X,Y=np.meshgrid(a,a); r=np.hypot(X,Y)
    rng=np.random.default_rng(11); m=120
    f=gaussian_filter(rng.standard_normal((m,m)),9,mode='wrap'); f=zoom(f,n/m,order=3)[:n,:n]; f=(f-f.mean())/f.std()
    g=gaussian_filter(rng.standard_normal((m,m)),12,mode='wrap'); g=zoom(g,n/m,order=3)[:n,:n]; g=(g-g.mean())/g.std()
    gy,gx=np.gradient(f,res); gr=np.maximum(np.hypot(gx,gy),1e-3)
    d=np.abs(f-0.05)/gr; w=(1.1+0.6*np.clip(g,-1.5,1.5))*(R/25)+0.4
    sm=lambda x:x*x*(3-2*x)
    deep=0.4*sm(np.clip((w-d)/0.9,0,1))
    acc=0.2; xx=np.abs(d-(w+1.5)); az=np.where(xx<0.77,(np.sqrt(RB**2-xx**2)-(RB-acc)),0)*(d>w+0.8)
    bd=np.abs(r-(R-1.3)); bz=np.where(bd<0.77,(np.sqrt(RB**2-bd**2)-(RB-acc)),0)
    inside=r<=R-0.3
    Z=-np.maximum(deep*inside,az*inside)
    Acut=((deep*inside)>0.01).sum()*res*res; Adeep=((deep*inside)>0.2).sum()*res*res
    band=np.abs(d-(w+1.5))<0.2; Lacc=(band&inside&(d>w+0.8)).sum()*res*res/0.4
    L=Acut/0.15+Adeep/0.8+Lacc   # finish stepover 0.15 (scallop ~0.002 mm) + rough pass + accent lines
    return X,Y,r,Z,L
for R in (25,19):
    L=render(f"riverislands_D{2*R}",R,None,"Design 6 River Islands"); print(2*R,"approx path mm",round(L),"min @F200",round(L/200,1))
