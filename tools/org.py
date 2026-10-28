import json
def esc(s): return s.replace('&','&amp;').replace('<','&lt;')
class C:
    def __init__(s,W=340): s.W=W; s.el=[]; s.H=0
    def box(s,cx,y,w,title,subs=(),kind='n',fs=13):
        h=22+len(subs)*14+ (6 if subs else 0)
        x=cx-w/2
        if kind=='lead': st="fill:var(--gold);stroke:none;"; tc="#1a140a"; sc="#3a2c12"
        elif kind=='dash': st="fill:var(--card);stroke:var(--gold);stroke-width:1.2;stroke-dasharray:4 3;"; tc="var(--ivory)"; sc="var(--ash)"
        else: st="fill:var(--card);stroke:var(--line);stroke-width:1.2;"; tc="var(--ivory)"; sc="var(--ash)"
        s.el.append(f"<rect x='{x:.1f}' y='{y}' width='{w}' height='{h}' rx='8' style='{st}'/>")
        s.el.append(f"<text x='{cx}' y='{y+16}' text-anchor='middle' style='fill:{tc};font-weight:700;font-size:{fs}px;font-family:var(--mincho);'>{esc(title)}</text>")
        for i,t in enumerate(subs):
            s.el.append(f"<text x='{cx}' y='{y+32+i*14}' text-anchor='middle' style='fill:{sc};font-size:10px;'>{esc(t)}</text>")
        s.H=max(s.H,y+h); return (cx,y,y+h,w)
    def label(s,x,y,t,anchor='middle',col='var(--gold)',fs=11):
        s.el.append(f"<text x='{x}' y='{y}' text-anchor='{anchor}' style='fill:{col};font-size:{fs}px;font-weight:700;'>{esc(t)}</text>")
    def line(s,x1,y1,x2,y2,dash=False,col='var(--gold)',w=1.3):
        d="stroke-dasharray:3 3;" if dash else ""
        s.el.append(f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' style='stroke:{col};stroke-width:{w};{d}'/>")
    def elbow(s,p,cs,dash=False):
        # p=(cx,y,bottom,w); cs=list of children
        my=(p[2]+min(c[1] for c in cs))/2
        s.line(p[0],p[2],p[0],my,dash)
        xs=[c[0] for c in cs]
        if len(cs)>1 or xs[0]!=p[0]: s.line(min(xs+[p[0]]),my,max(xs+[p[0]]),my,dash)
        for c in cs: s.line(c[0],my,c[0],c[1],dash)
    def vstack(s,parent_x,top,bottom_of_parent,boxes):
        pass
    def svg(s,label):
        return f"<svg viewBox='0 0 {s.W} {s.H+6}' width='100%' role='img' aria-label='{esc(label)}'>"+''.join(s.el)+"</svg>"

def chain_col(c,cx,y0,items,w,gap=10,kind='n'):
    out=[];y=y0
    for t,subs in items:
        b=c.box(cx,y,w,t,subs,kind); out.append(b); y=b[2]+gap
    # connect vertically with a side rail
    return out

def rail(c,header,boxes,side='left'):
    # vertical rail from header bottom along side, ticks to each box
    x=header[0]-header[3]/2+10 if side=='left' else header[0]
    xr=boxes[0][0]-boxes[0][3]/2-8
    c.line(header[0],header[2],header[0],header[2]+6)
    c.line(xr,header[2]+6,header[0],header[2]+6)
    last=(boxes[-1][1]+boxes[-1][2])/2
    c.line(xr,header[2]+6,xr,last)
    for b in boxes:
        my=(b[1]+b[2])/2; c.line(xr,my,b[0]-b[3]/2,my)

R={}
# A) 江戸幕府
c=C()
sh=c.box(170,4,96,'将軍',kind='lead',fs=14)
tai=c.box(250,52,110,'大老（臨時）',['重要事項のときだけ'],kind='dash',fs=12)
c.line(sh[0]+48,sh[1]+11,250,sh[1]+11,True); c.line(250,sh[1]+11,250,tai[1],True)
ji=c.box(70,52,118,'寺社奉行',['将軍直属・譜代大名'])
c.line(sh[0]-48,sh[1]+11,70,sh[1]+11); c.line(70,sh[1]+11,70,ji[1])
ro=c.box(110,124,110,'老中',['政務を統轄（常設）'],kind='lead')
wa=c.box(255,124,110,'若年寄',['老中を補佐'])
c.line(170,sh[2],170,112); c.line(110,112,255,112); c.line(110,112,110,ro[1]); c.line(255,112,255,wa[1])
items=[('大目付',['大名を監察']),('町奉行',['江戸の町・旗本から']),('勘定奉行',['財政・幕領・旗本から']),('京都所司代',['朝廷・西国大名の監視']),('大坂城代・遠国奉行',['重要都市・直轄地']),('郡代・代官',['幕領の支配（勘定奉行の下）'])]
bs=[];y=ro[2]+16
for t,s_ in items:
    b=c.box(125,y,150,t,s_,fs=12); bs.append(b); y=b[2]+7
c.line(ro[0],ro[2],ro[0],ro[2]+8); c.line(40,ro[2]+8,ro[0],ro[2]+8); c.line(40,ro[2]+8,40,(bs[-1][1]+bs[-1][2])/2)
for b in bs: c.line(40,(b[1]+b[2])/2,b[0]-75,(b[1]+b[2])/2)
me=c.box(270,wa[2]+16,104,'目付',['旗本・御家人を','監察'],fs=12)
c.line(255,wa[2],255,me[1]); 
hy=bs[-1][2]+18
hy_box=c.box(170,hy,300,'評定所',['老中・三奉行（寺社・町・勘定）らが合議'],kind='dash')
R['edo']=c.svg('江戸幕府の職制')

# B) 鎌倉幕府
c=C()
sh=c.box(170,4,150,'将軍（源頼朝）',kind='lead',fs=14)
c.label(85,58,'中央（鎌倉）'); c.label(255,58,'地方')
c.line(170,sh[2],170,38); c.line(85,38,255,38); c.line(85,38,85,46); c.line(255,38,255,46)
L=[];y=66
for t,s_ in [('侍所',['御家人の統制','別当＝和田義盛']),('政所（初め公文所）',['一般政務・財政','別当＝大江広元']),('問注所',['裁判','執事＝三善康信'])]:
    b=c.box(85,y,150,t,s_,fs=12); L.append(b); y=b[2]+8
Rr=[];y=66
for t,s_ in [('守護',['国ごとに1人','大犯三カ条']),('地頭',['荘園・公領ごと','年貢の徴収・土地管理']),('京都守護',['朝廷との交渉','西国御家人の統轄']),('鎮西奉行',['九州の御家人を統轄'])]:
    b=c.box(255,y,150,t,s_,fs=12); Rr.append(b); y=b[2]+8
R['kamakura']=c.svg('鎌倉幕府のしくみ')

# C) 執権時代
c=C()
sh=c.box(170,4,230,'将軍（摂家将軍・皇族将軍）',['実権はない'],kind='dash',fs=12)
sk=c.box(170,sh[2]+16,190,'執権・連署（北条氏）',['政治の実権を握る'],kind='lead')
c.line(170,sh[2],170,sk[1])
hj=c.box(95,sk[2]+20,150,'評定衆（1225・泰時）',['合議で政治・裁判'],fs=12)
hk=c.box(95,hj[2]+16,150,'引付衆（1249・時頼）',['御家人の所領の訴訟'],fs=12)
c.line(95,hj[2],95,hk[1])
s3=c.box(255,sk[2]+20,150,'侍所・政所・問注所',['頼朝以来の中央機関'],fs=12)
c.line(170,sk[2],170,sk[2]+10); c.line(95,sk[2]+10,255,sk[2]+10); c.line(95,sk[2]+10,95,hj[1]); c.line(255,sk[2]+10,255,s3[1])
c.label(255,s3[2]+20,'地方')
y=s3[2]+28; Lb=[]
for t,s_ in [('六波羅探題',['京都・朝廷の監視','（1221〜）']),('鎮西探題',['博多・九州（1293〜）']),('守護・地頭',['国ごと／荘園・公領ごと'])]:
    b=c.box(255,y,150,t,s_,fs=12); Lb.append(b); y=b[2]+8
R['shikken']=c.svg('執権時代の幕府のしくみ')

# D) 室町幕府
c=C()
sh=c.box(170,4,100,'将軍',kind='lead',fs=14)
kr=c.box(170,sh[2]+14,240,'管領',['将軍を補佐・三管領＝細川・斯波・畠山'],kind='lead')
c.line(170,sh[2],170,kr[1])
c.label(85,kr[2]+22,'中央（京都）'); c.label(255,kr[2]+22,'地方')
c.line(170,kr[2],170,kr[2]+8); c.line(85,kr[2]+8,255,kr[2]+8); c.line(85,kr[2]+8,85,kr[2]+12); c.line(255,kr[2]+8,255,kr[2]+12)
y=kr[2]+30
for t,s_ in [('侍所',['京都の警備・刑事裁判','所司＝四職（赤松・一色','山名・京極）']),('政所',['将軍家の家政・財政']),('問注所',['記録・訴訟文書']),('評定衆・引付衆',['鎌倉幕府から継承'])]:
    b=c.box(85,y,150,t,s_,fs=12); y=b[2]+8
y=kr[2]+30
kf=c.box(255,y,150,'鎌倉府',['東国（関東8か国＋伊豆・甲斐）'],fs=12)
kb=c.box(255,kf[2]+10,140,'鎌倉公方',['足利基氏の子孫'],fs=12)
kk=c.box(255,kb[2]+10,140,'関東管領',['上杉氏が世襲'],fs=12)
c.line(255,kf[2],255,kb[1]); c.line(255,kb[2],255,kk[1])
y=kk[2]+12
for t,s_ in [('九州探題',['九州']),('奥州探題・羽州探題',['東北']),('守護（守護代）',['国ごと・在京が原則'])]:
    b=c.box(255,y,150,t,s_,fs=12); y=b[2]+8
R['muromachi']=c.svg('室町幕府のしくみ')

# E) 寄進地系荘園
c=C()
def trap(y0,y1,topw,botw,fill):
    x0=170-topw/2;x1=170+topw/2;x2=170+botw/2;x3=170-botw/2
    c.el.append(f"<polygon points='{x0},{y0} {x1},{y0} {x2},{y1} {x3},{y1}' style='{fill}'/>")
trap(10,80,36,110,'fill:var(--gold);')
trap(84,154,114,188,'fill:var(--card);stroke:var(--line);stroke-width:1.2;')
trap(158,228,192,266,'fill:var(--card);stroke:var(--line);stroke-width:1.2;')
def t2(y,a,b_,dark=False):
    c.el.append(f"<text x='170' y='{y}' text-anchor='middle' style='fill:{'#1a140a' if dark else 'var(--ivory)'};font-weight:700;font-size:14px;font-family:var(--mincho);'>{a}</text>")
    c.el.append(f"<text x='170' y='{y+15}' text-anchor='middle' style='fill:{'#3a2c12' if dark else 'var(--ash)'};font-size:10px;'>{b_}</text>")
t2(52,'本家','摂関家・天皇家',True)
t2(118,'領家','貴族・大寺社')
t2(190,'開発領主 → 荘官','預所・下司として現地を管理')
def arr(x,lab,lab2):
    c.line(x,224,x,40)
    c.el.append(f"<polygon points='{x},{30} {x-5},{41} {x+5},{41}' style='fill:var(--gold);'/>")
    c.el.append(f"<text x='{x}' y='22' text-anchor='middle' style='fill:var(--gold);font-size:10.5px;font-weight:700;'>{lab}</text>")
    c.el.append(f"<text x='{x}' y='238' text-anchor='middle' style='fill:var(--gold);font-size:9.5px;'>{lab2}</text>")
arr(16,'寄進','（名義）')
arr(324,'年貢','（一部）')
c.el.append("<rect x='26' y='246' width='288' height='30' rx='8' style='fill:none;stroke:var(--line);stroke-dasharray:4 3;'/>")
c.el.append("<text x='170' y='266' text-anchor='middle' style='fill:var(--ash);font-size:11px;'>田堵などの農民が耕作し、年貢を納める</text>")
c.line(170,312,170,280,False,'#d9785c',2)
c.el.append("<circle cx='170' cy='296' r='9' style='fill:var(--bg,#121826);stroke:#d9785c;stroke-width:2;'/>")
c.line(164,290,176,302,False,'#d9785c',2); c.line(176,290,164,302,False,'#d9785c',2)
c.el.append("<rect x='70' y='312' width='200' height='44' rx='8' style='fill:var(--card);stroke:var(--line);'/>")
c.el.append("<text x='170' y='330' text-anchor='middle' style='fill:var(--ivory);font-weight:700;font-size:13px;font-family:var(--mincho);'>国衙（受領）</text>")
c.el.append("<text x='170' y='346' text-anchor='middle' style='fill:var(--ash);font-size:10px;'>官物・臨時雑役を取り立てたい</text>")
c.el.append("<text x='170' y='374' text-anchor='middle' style='fill:#d9785c;font-size:10.5px;font-weight:700;'>不輸（税の免除）・不入（検田使の立入り拒否）で入れない</text>")
c.H=380
R['kishin']=c.svg('寄進地系荘園のしくみ')
json.dump(R,open('orgs.json','w',encoding='utf-8'),ensure_ascii=False)
print({k:len(v) for k,v in R.items()})
