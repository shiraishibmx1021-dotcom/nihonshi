# 授業に入れる日本地図（ベクター）をつくる。
# 海岸線はアプリ本体の <g id='jpmap'>（vecmap.py で作った path）を <use> で使い回すので、
# 1枚の地図は点・線・文字だけになり、軽い。
#
#   from jmap import jmap
#   html = jmap('源平の争乱', (129.5,141,31,38),
#               points=[(1,'一の谷',135.10,34.65,0,-28), ...],   # (番号, 凡例, 経度, 緯度, 番号札のずらし x, y［画面px］)
#               routes=[([(lon,lat),...],'sea')],                  # 'road' 実線 / 'sea' 点線 / 'arrow' 矢印つき点線
#               areas=[('加賀',136.6,36.4)],                       # 地域名（うすい文字）
#               note='赤い点＝実際の場所')
#
# 凡例は HTML なので、ふりがな（<ruby>）や kw をそのまま書ける。
import numpy as np, os
_C=np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),'calib.npy')); _cx,_cy=_C[:3],_C[3:]
def px(lon,lat): return (_cx[0]*lon+_cx[1]*lat+_cx[2], _cy[0]*lon+_cy[1]*lat+_cy[2])

SCREEN=330   # スマホでの地図の幅（px）のめやす。文字や点の大きさをこれに合わせる

def _f(v): return f"{v:.1f}".rstrip('0').rstrip('.')

def jmap(title,bbox,points=(),routes=(),areas=(),note='',legend_cols=2,base='jp'):
    lon0,lon1,lat0,lat1=bbox
    xs,ys=zip(*[px(a,b) for a in (lon0,lon1) for b in (lat0,lat1)])
    X,Y,W,H=min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys)
    u=W/SCREEN                       # 画面1pxが地図の何単位か
    if base=='kinki':   # 近畿の拡大図：白地図の画像では粗すぎるので、海と湖を緯度経度から描く
        el=[f"<rect x='{_f(X)}' y='{_f(Y)}' width='{_f(W)}' height='{_f(H)}' style='fill:#263250;'/>"]
        for poly,fill in [(OSAKA_BAY,'#0F1626'),(AWAJI,'#263250'),(ISE_BAY,'#0F1626'),(ENSHU,'#0F1626'),(WAKASA,'#0F1626'),(BIWA,'#0F1626')]:
            d='M'+' L'.join(f"{_f(px(*p)[0])} {_f(px(*p)[1])}" for p in poly)+'Z'
            el.append(f"<path d='{d}' style='fill:{fill};stroke:#A88E4E;stroke-width:{_f(1*u)};stroke-linejoin:round;'/>")
    else:
        el=[f"<rect x='{_f(X)}' y='{_f(Y)}' width='{_f(W)}' height='{_f(H)}' style='fill:#0F1626;'/>",
            "<use href='#jpmap'/>"]
    for name,lon,lat in areas:
        x,y=px(lon,lat)
        el.append(f"<text x='{_f(x)}' y='{_f(y)}' text-anchor='middle' style='fill:#8E9AB8;font-size:{_f(11*u)}px;letter-spacing:.1em;'>{name}</text>")
    for pts,kind in routes:
        P=[px(*p) for p in pts]; d='M'+' L'.join(f"{_f(x)} {_f(y)}" for x,y in P)
        if kind=='road': st=f"stroke:#E07A5F;stroke-width:{_f(2.6*u)};"
        elif kind=='road2': st=f"stroke:#7FB3D5;stroke-width:{_f(2.6*u)};"
        elif kind=='sea': st=f"stroke:#7FB3D5;stroke-width:{_f(2.2*u)};stroke-dasharray:{_f(6*u)} {_f(4*u)};"
        else: st=f"stroke:#E07A5F;stroke-width:{_f(2.4*u)};stroke-dasharray:{_f(6*u)} {_f(4*u)};"
        mk=" marker-end='url(#jm-ah)'" if kind=='arrow' else ''
        el.append(f"<path d='{d}' style='fill:none;stroke-linejoin:round;stroke-linecap:round;{st}'{mk}/>")
    badges=[]
    for p in points:
        n,lab,lon,lat=p[:4]; dx,dy=(p[4],p[5]) if len(p)>5 else (0,0)
        x0,y0=px(lon,lat); x,y=x0+dx*u,y0+dy*u
        el.append(f"<circle cx='{_f(x0)}' cy='{_f(y0)}' r='{_f(3.2*u)}' style='fill:#E07A5F;stroke:#0F1626;stroke-width:{_f(1*u)};'/>")
        if dx or dy: el.append(f"<line x1='{_f(x0)}' y1='{_f(y0)}' x2='{_f(x)}' y2='{_f(y)}' style='stroke:#D4BD82;stroke-width:{_f(1*u)};'/>")
        badges.append(f"<circle cx='{_f(x)}' cy='{_f(y)}' r='{_f(8.5*u)}' style='fill:#D4BD82;stroke:#0F1626;stroke-width:{_f(1.4*u)};'/>"
                      f"<text x='{_f(x)}' y='{_f(y+3.8*u)}' text-anchor='middle' style='fill:#10141C;font-size:{_f(11*u)}px;font-weight:800;font-family:system-ui,sans-serif;'>{n}</text>")
    defs=(f"<defs><marker id='jm-ah' viewBox='0 0 10 10' refX='7' refY='5' markerWidth='4' markerHeight='4' orient='auto'>"
          "<path d='M0,0 L10,5 L0,10 z' style='fill:#E07A5F;'/></marker></defs>")
    svg=(f"<svg viewBox='{_f(X)} {_f(Y)} {_f(W)} {_f(H)}' width='100%' role='img' aria-label='{title}'>"
         +defs+''.join(el)+''.join(badges)+"</svg>")
    leg=''.join(f"<li><b>{p[0]}</b><span>{p[1]}</span></li>" for p in points)
    cap=f"地図 ── {title}"+(f"（{note}）" if note else '')
    return (f"<div class='viz jm'><div class='viz-cap'>{cap}</div><div class='mapwrap'>{svg}</div>"
            +(f"<ol class='jm-leg c{legend_cols}'>{leg}</ol>" if leg else '')+"</div>")

# アプリ本体に入れる、海岸線と琵琶湖の定義（source.html の <body> の直後に1回だけ置く）
BIWA=[(136.17,35.53),(136.22,35.47),(136.27,35.40),(136.26,35.33),(136.22,35.26),(136.15,35.18),(136.07,35.12),
      (135.98,35.06),(135.93,35.01),(135.90,34.98),(135.87,35.01),(135.89,35.07),(135.95,35.15),(136.00,35.27),
      (136.04,35.37),(136.09,35.46)]
# 近畿の拡大図に使う海（おおよその海岸線）
OSAKA_BAY=[(134.60,34.64),(134.99,34.645),(135.11,34.64),(135.19,34.68),(135.30,34.72),(135.40,34.70),(135.43,34.66),(135.47,34.61),
           (135.46,34.57),(135.42,34.52),(135.37,34.47),(135.30,34.40),(135.22,34.35),(135.15,34.32),(135.07,34.27),(135.05,33.9),(134.6,33.9)]
AWAJI=[(135.02,34.60),(134.95,34.53),(134.88,34.45),(134.80,34.38),(134.72,34.28),(134.68,34.20),(134.75,34.16),(134.85,34.20),
       (134.90,34.30),(134.93,34.38),(134.98,34.47),(135.03,34.56)]
ISE_BAY=[(136.85,35.08),(136.69,35.06),(136.63,34.96),(136.59,34.85),(136.53,34.72),(136.57,34.60),(136.72,34.50),(136.84,34.48),
         (137.01,34.58),(137.10,34.66),(137.25,34.72),(137.31,34.77),(137.22,34.82),(137.05,34.83),(136.95,34.89),(136.98,34.70),
         (136.88,34.75),(136.85,34.85),(136.87,34.98)]
ENSHU=[(136.88,34.40),(137.01,34.58),(137.30,34.62),(137.60,34.67),(137.90,34.69),(138.2,34.62),(138.2,34.0),(136.88,34.0)]
WAKASA=[(134.9,35.62),(135.20,35.55),(135.38,35.47),(135.55,35.49),(135.75,35.50),(135.95,35.60),(136.06,35.65),(136.02,35.75),
        (136.00,35.95),(136.10,36.3),(134.9,36.3)]

def symbol_html(path_d):
    b='M'+' L'.join(f"{_f(px(*p)[0])} {_f(px(*p)[1])}" for p in BIWA)+'Z'
    return ("<svg width='0' height='0' style='position:absolute;width:0;height:0;overflow:hidden' aria-hidden='true'><defs><g id='jpmap'>"
            f"<path d='{path_d}' style='fill:#263250;stroke:#A88E4E;stroke-width:1;vector-effect:non-scaling-stroke;stroke-linejoin:round;'/>"
            f"<path d='{b}' style='fill:#0F1626;stroke:#A88E4E;stroke-width:1;vector-effect:non-scaling-stroke;'/>"
            "</g></defs></svg>")
