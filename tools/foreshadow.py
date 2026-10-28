import json,re
s=open('base37.html',encoding='utf-8').read()
m=re.search(r'const DEFAULT_PACKS = (\[[\s\S]*?\n\]);',s); packs=json.loads(m.group(1))
rd={}
for i in range(1,13):
    f='ruby.txt' if i==1 else f'ruby{i}.txt'
    for l in open(f,encoding='utf-8').read().strip().split('\n'):
        a,b=l.split(':'); rd[a]=b
for bad in ['三浦','藩','元','聖','講','西軍','東軍']: rd.pop(bad,None)
rd.update({"平重衡":"たいらのしげひら","南都焼打ち":"なんとやきうち","竹崎季長":"たけざきすえなが","平忠常の乱":"たいらのただつねのらん"})
keys=sorted(rd,key=len,reverse=True); pat=re.compile('|'.join(map(re.escape,keys)))
def rub(t):
    seen=set()
    def rep(mm):
        w=mm.group(0)
        if w in seen: return w
        seen.add(w); return f'<ruby>{w}<rt>{rd[w]}</rt></ruby>'
    o=[];inr=0
    for tok in re.split(r'(<[^>]+>)',t):
        if tok.startswith('<'):
            if tok.startswith('<ruby'): inr+=1
            elif tok.startswith('</ruby'): inr-=1
            o.append(tok);continue
        o.append(tok if inr else pat.sub(rep,tok))
    return ''.join(o)
def RB(t): return "<div class='recall'><span class='bx-tag'>ここで思い出そう</span>"+rub(re.sub(r'《([^》]+)》',r"<span class='kw'>\1</span>",t))+"</div>"
def L(pid,no): return [l for l in [p for p in packs if p['id']==pid][0]['lessons'] if l['no']==no][0]
def after_para(h,anchor,box):
    rx=''.join(re.escape(ch)+r'(?:<rt>[^<]*</rt>|<[^>]+>)*' for ch in anchor)
    mm=re.search(rx,h); assert mm,anchor
    e=h.find('</p>',mm.end())+4
    return h[:e]+box+h[e:]
def before_para(h,anchor,box):
    rx=''.join(re.escape(ch)+r'(?:<rt>[^<]*</rt>|<[^>]+>)*' for ch in anchor)
    mm=re.search(rx,h); assert mm,anchor
    st=h.rfind('<p>',0,mm.start())
    return h[:st]+box+h[st:]
# 1) 中世③L09：冒頭を伏線回収の「思い出そう」から
l=L('chusei3','09'); h=l['html']
first=h.find('</p>')+4
l['html']=RB("中世②の源平の争乱で、平氏の《平重衡》が奈良を攻め、東大寺や興福寺を焼き打ちにしたよね（《南都焼打ち》、1180年）。聖武天皇がつくらせたあの大仏殿も、燃えてしまった。……でも、東大寺は今も奈良に建っている。ということは、<b>誰かが建て直した</b>はずだ。その人こそが、ここで登場する重源だ。")+"<p>じつは、鎌倉時代の美術の新しい動きは、この<b>焼けた寺の建て直し</b>から始まった。</p>"+h[first:]
# 2) 中世③L05：竹崎季長の伏線回収
l=L('chusei3','05')
l['html']=RB("授業01で、肥後の御家人《竹崎季長》が、自分の手柄を認めてもらうために、わざわざ鎌倉まで出向いて恩賞を求めた、という話をしたよね。命がけで戦った御家人が、ほうびをもらうために遠い鎌倉まで行かなければならなかった。<b>なぜそこまでしないと、ほうびがもらえなかったのか</b>。その答えが、この授業だ。")+l['html']
# 3) 中世③L08：新古今と後鳥羽上皇
l=L('chusei3','08')
l['html']=before_para(l['html'],"後鳥羽上皇の命令で",RB("中世②の承久の乱で、後鳥羽上皇は「和歌の名人で、自分で刀まで打つ、なんでもできる人」だったと言ったよね。その<b>和歌の名人ぶり</b>が形になったのが、これから出てくる『新古今和歌集』だ。幕府を倒そうとして隠岐に流された上皇は、日本の和歌の歴史にも大きな名前を残している。"))
# 4) 中世③L07：建長寺
l=L('chusei3','07')
l['html']=before_para(l['html'],"幕府は臨済宗を大切にした",RB("中世②の最後で、5代執権の北条時頼が、禅宗の本格的なお寺<b>建長寺</b>を建て、鎌倉を武家の都として整えた、と言ったよね。なぜ執権がわざわざ禅寺を建てたのか。その理由が、ここでわかる。"))
# 5) 中世①L02：源頼信→頼義
l=L('chusei','02')
l['html']=RB("古代⑤の最後で、1028年に上総でおこった《平忠常の乱》を<b>源頼信</b>がしずめ、それが源氏が関東に進出するきっかけになった、と言ったよね。ここで東北に乗りこむ源頼義は、その<b>頼信の息子</b>だ。父が関東に足場をつくり、息子が東北へ。源氏はこうして、東国のリーダーへの道を一歩ずつ進んでいく。")+l['html']
# 6) 古代⑤L07：道真の怨霊
l=L('kodai5','07')
l['html']=before_para(l['html'],"そして平安の人たちが本気でこわがったのが",RB("授業02で、大宰府に飛ばされて死んだ菅原道真のあと、都で災いが続いて「道真のたたりだ！」と大騒ぎになり、北野天満宮が建てられた、という話をしたよね。<b>なぜ平安の人たちは、そこまで「たたり」をこわがったのか</b>。その背景にあるのが、これから説明する御霊信仰だ。"))
s=s[:m.start(1)]+json.dumps(packs,ensure_ascii=False,indent=1)+s[m.end(1):]
open('/mnt/user-data/outputs/nihonshi_38.html','w',encoding='utf-8').write(s); open('base38.html','w',encoding='utf-8').write(s)
sc=re.findall(r'<script>(.*?)</script>',s,re.S)[-1]; open('checku.js','w',encoding='utf-8').write(sc)
print('ok')
