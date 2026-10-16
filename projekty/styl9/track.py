"""usage: track.py VIDEO TREF X Y W H T0 T1 > kf.json
Track a rectangle (x,y,w,h at ref time) through [t0,t1] by SSD template search (half-res). Prints keyframes JSON."""
import json,subprocess,sys,numpy as np
src,tref,x,y,w,h,t0,t1=sys.argv[1],*map(float,sys.argv[2:9])
S=2
def frames(a,b):
    raw=subprocess.run(["ffmpeg","-v","error","-ss",str(a),"-i",src,"-t",str(b-a),"-vf",f"scale={1080//S}:{1920//S},format=gray","-f","rawvideo","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.uint8).reshape(-1,1920//S,1080//S).astype(np.float32)
ref=frames(tref,tref+0.04)[0]; X,Y,Ww,Hh=int(x/S),int(y/S),int(w/S),int(h/S)
tpl=ref[Y:Y+Hh,X:X+Ww]; tpl=tpl-tpl.mean()
F=frames(t0,t1); out=[]; cx,cy=X,Y
# start from ref position, search ±R px per frame around last position (forward from t0 assumes ref inside window)
k0=int(round((tref-t0)*30)); pos={k0:(X,Y)}
def search(f,px,py,R=14):
    best=None
    for dy in range(-R,R+1,1):
        for dx in range(-R,R+1,1):
            xx,yy=px+dx,py+dy
            if xx<0 or yy<0 or xx+Ww>f.shape[1] or yy+Hh>f.shape[0]: continue
            p=f[yy:yy+Hh,xx:xx+Ww]; p=p-p.mean(); s=((p-tpl)**2).mean()
            if best is None or s<best[0]: best=(s,xx,yy)
    return best
for k in list(range(k0+1,len(F)))+list(range(k0-1,-1,-1)):
    prev=pos.get(k-1) if k>k0 else pos.get(k+1)
    b=search(F[k],*prev); pos[k]=(b[1],b[2]) if b else prev
kf=[[round(t0+k/30,3),pos[k][0]*S,pos[k][1]*S] for k in sorted(pos) if k%3==0 or k==len(F)-1]
print(json.dumps(kf))
