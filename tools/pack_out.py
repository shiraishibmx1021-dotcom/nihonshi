import os
import json,re,zlib,base64,sys
src,out=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
m=re.search(r'const DEFAULT_PACKS = (\[[\s\S]*?\n\]);',s)
packs=json.loads(m.group(1))
raw=json.dumps(packs,ensure_ascii=False,separators=(',',':')).encode('utf-8')
comp=zlib.compress(raw,9)
b64=base64.b64encode(comp).decode()
pako=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'pako_inflate.min.js'),encoding='utf-8').read()
repl='const DEFAULT_PACKS = JSON.parse(pako.inflate(Uint8Array.from(atob("'+b64+'"),c=>c.charCodeAt(0)),{to:"string"}));'
t=s[:m.start()]+repl+s[m.end():]
# insert pako before the main app script (the one holding DEFAULT_PACKS)
i=t.rfind('<script>',0,m.start())
t=t[:i]+'<script>'+pako+'</script>\n'+t[i:]
open(out,'w',encoding='utf-8').write(t)
print('raw',len(raw),'b64',len(b64),'out',len(t.encode()))
