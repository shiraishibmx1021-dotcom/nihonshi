import numpy as np, base64, io
from PIL import Image
C=np.load('calib.npy'); cx,cy=C[:3],C[3:]
SRC='basemap_japan.png'
def px(lon,lat): return (cx[0]*lon+cx[1]*lat+cx[2], cy[0]*lon+cy[1]*lat+cy[2])
def make(bbox,points,routes=(),outw=900,title=''):
    lon0,lon1,lat0,lat1=bbox
    xs=[px(lon0,lat0)[0],px(lon1,lat1)[0],px(lon0,lat1)[0],px(lon1,lat0)[0]]
    ys=[px(lon0,lat0)[1],px(lon1,lat1)[1],px(lon0,lat1)[1],px(lon1,lat0)[1]]
    L,R,T,B=int(min(xs)),int(max(xs)),int(min(ys)),int(max(ys))
    im=Image.open(SRC).convert('RGB').crop((L,T,R,B))
    s=outw/(R-L); im=im.resize((outw,int((B-T)*s)),Image.LANCZOS)
    buf=io.BytesIO(); im.save(buf,'JPEG',quality=72,optimize=True); b64=base64.b64encode(buf.getvalue()).decode()
    W,H=im.size
    def P(lon,lat):
        x,y=px(lon,lat); return ((x-L)*s,(y-T)*s)
    el=[f"<image href='data:image/jpeg;base64,{b64}' x='0' y='0' width='{W}' height='{H}'/>"]
    for (a,b,dash) in routes:
        x1,y1=P(*a); x2,y2=P(*b)
        el.append(f"<line x1='{x1:.0f}' y1='{y1:.0f}' x2='{x2:.0f}' y2='{y2:.0f}' style='stroke:#e07a5f;stroke-width:5;{'stroke-dasharray:12 8;' if dash else ''}' marker-end='url(#ah)'/>")
    for p in points:
        n,lon,lat,label,nx,ny=p[:6]; col=p[6] if len(p)>6 else '#f3d27a'
        x0,y0=P(lon,lat); x,y=x0+nx,y0+ny
        el.append(f"<circle cx='{x0:.0f}' cy='{y0:.0f}' r='6' style='fill:#e07a5f;stroke:#10141c;stroke-width:2;'/>")
        if nx or ny: el.append(f"<line x1='{x0:.0f}' y1='{y0:.0f}' x2='{x:.0f}' y2='{y:.0f}' style='stroke:#f3d27a;stroke-width:2;'/>")
        el.append(f"<circle cx='{x:.0f}' cy='{y:.0f}' r='19' style='fill:{col};stroke:#10141c;stroke-width:3;'/>")
        el.append(f"<text x='{x:.0f}' y='{y+8:.0f}' text-anchor='middle' style='font-size:23px;font-weight:800;fill:#10141c;'>{n}</text>")
    defs="<defs><marker id='ah' viewBox='0 0 10 10' refX='8' refY='5' markerWidth='5' markerHeight='5' orient='auto'><path d='M0,0 L10,5 L0,10 z' style='fill:#e07a5f;'/></marker></defs>"
    return f"<svg viewBox='0 0 {W} {H}' width='100%' role='img' aria-label='{title}'>{defs}{''.join(el)}</svg>"
