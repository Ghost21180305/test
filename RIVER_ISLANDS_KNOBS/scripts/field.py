# shared height field for the River Islands knob top. Z = cut depth below the top face (<=0), mm
src=open("/tmp/claude-0/-home-user-test/e3ae2854-ac2e-5151-82d4-ce8e0cd4b20b/scratchpad/river.py").read()
src=src[:src.rindex("for R in (25,19):")].replace("inside=r<=R-0.3","inside=r<=1e9")
exec(src)
def field(R,sub=5):
    m=int(2*R/0.25); n=sub*m+1; res=2*R/(sub*m)*0.99999
    X,Y,r,Z,L=build(R,None,res); assert Z.shape==(n,n),(Z.shape,n)
    return np.linspace(-R,R,n),Z
_field_raw=field
def field(R,sub=5,sigma=3.0):
    a,Z=_field_raw(R,sub); return a,gaussian_filter(Z,sigma)
