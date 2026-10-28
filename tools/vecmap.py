# 白地図画像（basemap_japan.png）から海岸線を取り出して、SVG の path にする。
# 出力 basemap_path.txt は、アプリ本体の <symbol id='jpmap'> にそのまま入れる。
# 座標は basemap_japan.png のピクセル座標（mapkit.py の px(lon,lat) と同じ）。
import numpy as np
from PIL import Image

def load_mask(src='basemap_japan.png'):
    a=np.asarray(Image.open(src).convert('RGB')).astype(int)
    m=(a.sum(2)>100).astype(float)          # 陸地と海岸線（金）＝1、海＝0
    # 少しぼかして、ギザギザを消す（0.5 の等高線を取る）
    k=np.array([1,4,6,4,1],float); k/=k.sum()
    for ax in (0,1):
        m=np.apply_along_axis(lambda r: np.convolve(r,k,mode='same'),ax,m)
    return m

def contours(f,lv=0.5):
    H,W=f.shape
    a=f[:-1,:-1];b=f[:-1,1:];c=f[1:,1:];d=f[1:,:-1]   # 左上・右上・右下・左下
    idx=((a>lv)*8+(b>lv)*4+(c>lv)*2+(d>lv)*1)
    ys,xs=np.nonzero((idx>0)&(idx<15))
    def it(p,q): return 0.5 if q==p else (lv-p)/(q-p)
    segs=[]
    for y,x in zip(ys,xs):
        A,B,C,D=a[y,x],b[y,x],c[y,x],d[y,x]; i=idx[y,x]
        T=(x+it(A,B),y); R=(x+1,y+it(B,C)); Bt=(x+it(D,C),y+1); L=(x,y+it(A,D))
        e={1:[(L,Bt)],2:[(Bt,R)],3:[(L,R)],4:[(T,R)],5:[(L,T),(Bt,R)],6:[(T,Bt)],7:[(L,T)],
           8:[(L,T)],9:[(T,Bt)],10:[(L,Bt),(T,R)],11:[(T,R)],12:[(L,R)],13:[(Bt,R)],14:[(L,Bt)]}[i]
        segs+=e
    # 線分をつないで輪にする
    key=lambda p:(round(p[0],4),round(p[1],4))
    adj={}
    for s in segs:
        for u,v in ((s[0],s[1]),(s[1],s[0])): adj.setdefault(key(u),[]).append(key(v))
    seen=set(); rings=[]
    for st in list(adj):
        if st in seen: continue
        ring=[st]; seen.add(st); cur=st
        while True:
            nx=[n for n in adj[cur] if n not in seen]
            if not nx: break
            cur=nx[0]; seen.add(cur); ring.append(cur)
        if len(ring)>4: rings.append(ring)
    return rings

def dp(pts,eps):
    pts=np.array(pts); n=len(pts)
    # 輪なので、いちばん遠い2点で2本に切ってから単純化する
    j0=int(np.argmax(np.hypot(*(pts-pts[0]).T)))
    keep={0,j0,n-1}; st=[(0,j0),(j0,n-1)]
    while st:
        i,j=st.pop()
        if j<=i+1: continue
        p,q=pts[i],pts[j]; d=q-p; L=np.hypot(*d); v=pts[i+1:j]-p
        dist=np.abs(d[0]*v[:,1]-d[1]*v[:,0])/L if L>1e-9 else np.hypot(v[:,0],v[:,1])
        k=int(np.argmax(dist))
        if dist[k]>eps: k+=i+1; keep.add(k); st+=[(i,k),(k,j)]
    return pts[sorted(keep)]

def area(r):
    x,y=r[:,0],r[:,1]; return 0.5*abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

if __name__=='__main__':
    f=load_mask(); rings=contours(f)
    out=[]
    for r in rings:
        s=dp(r,0.45)
        if len(s)<4 or area(s)<6: continue
        out.append('M'+' '.join(f'{x:.1f} {y:.1f}' for x,y in s)+'Z')
    d=''.join(out)
    d=d.replace('.0 ',' ').replace('.0Z','Z')
    open('basemap_path.txt','w').write(d)
    print('rings',len(out),'chars',len(d))
