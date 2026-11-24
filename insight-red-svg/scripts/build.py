import argparse,json,re,sys
from pathlib import Path
from svg_core import SVG,wrap

def require(cond,msg):
    if not cond: raise ValueError(msg)
def notes(s,p):
    items=p.get('notes',[]); require(1<=len(items)<=4,'architecture/process require 1–4 notes')
    h=(472-(len(items)-1)*10)/len(items)
    for i,t in enumerate(items): s.card(820,142+i*(h+10),412,h,t['title'],t['body'])
def build_slide(s,p):
    typ=p['layout']; data=p['data']; s.conclusion(p['conclusion'])
    if typ in ('architecture','process'):
        s.text(48,135,p.get('section','技术机制'),16,'ink',True,maxw=748)
        s.text(820,135,p.get('notes_title','机制解读与启示'),16,'ink',True,maxw=412); notes(s,p)
        if typ=='architecture':
            layers=data['layers']; require(2<=len(layers)<=5,'architecture requires 2–5 layers')
            h=(472-(len(layers)-1)*16)/len(layers)
            for i,a in enumerate(layers):
                y=142+i*(h+16); s.rect(48,y,748,h,'panel','border',8)
                s.text(62,y+19,a['title'],14,'blue',True,maxw=720)
                nodes=a['nodes']; require(1<=len(nodes)<=4,'1–4 nodes per layer'); w=(720-(len(nodes)-1)*10)/len(nodes)
                for j,node in enumerate(nodes):
                    x=62+j*(w+10); s.rect(x,y+27,w,h-35,'white','border',4)
                    s.block(x+7,y+29,w-14,h-39,node,12,'ink',anchor='middle',center=True)
                if i<len(layers)-1 and data.get('ordered',False): s.arrow(422,y+h,422,y+h+15)
        else:
            steps=data['steps']; require(2<=len(steps)<=6,'process requires 2–6 steps'); h=(472-(len(steps)-1)*16)/len(steps)
            for i,a in enumerate(steps):
                y=142+i*(h+16); s.rect(48,y,748,h,'blue-tint','border',5); s.rect(60,y+12,36,30,'blue',rx=4)
                s.text(78,y+32,f'{i+1:02}',14,'white',True,'middle'); s.text(110,y+22,a['title'],14,'blue',True,maxw=670)
                s.block(110,y+28,670,h-34,a['body'],12)
                if i<len(steps)-1:s.arrow(422,y+h,422,y+h+15)
    elif typ in ('matrix','compare'):
        headers=data['headers']; rows=data['rows']; require(2<=len(headers)<=6 and 1<=len(rows)<=12,'matrix: 2–6 columns, 1–12 rows')
        weights=data.get('weights',[1]*len(headers)); require(len(weights)==len(headers) and all(x>0 for x in weights),'invalid weights'); ws=[1184*x/sum(weights) for x in weights]; xs=[48+sum(ws[:i]) for i in range(len(ws))]
        require(all(len(r)==len(headers) for r in rows),'row length differs from headers')
        s.rect(48,120,1184,34,'dark')
        for x,w,t in zip(xs,ws,headers):s.block(x+9,122,w-18,30,t,12,'white',True,center=True)
        heights=[max(31,max(len(wrap(t,12,w-18))*16.8+12 for t,w in zip(r,ws))) for r in rows]
        require(sum(heights)<=460,'matrix too tall; split pages')
        extra=(460-sum(heights))/len(heights); y=154
        for i,(r,h) in enumerate(zip(rows,heights)):
            h+=extra
            for j,(x,w,t) in enumerate(zip(xs,ws,r)):
                s.rect(x,y,w,h,'blue-tint' if j==0 else 'panel' if i%2==0 else 'white','border')
                s.block(x+9,y+4,w-18,h-8,t,12,'blue' if j==0 else 'ink',j==0,center=True)
            y+=h
    elif typ=='cards':
        cards=data['cards']; require(2<=len(cards)<=6,'cards: 2–6'); cols=2 if len(cards) in (2,4) else 3; rows=(len(cards)+cols-1)//cols
        h=(494-(rows-1)*18)/rows
        for i,a in enumerate(cards):
            row=i//cols; count=min(cols,len(cards)-row*cols); w=(1184-(count-1)*28)/count
            s.card(48+(i%cols)*(w+28),120+row*(h+18),w,h,a['title'],a['body'])
    else: raise ValueError(f'unknown layout: {typ}')
def check_deck(d):
    require(isinstance(d['label'],str) and d['label'].strip(),'label required'); require(d['slides'],'slides required')
    sources={x['id'] for x in d['sources']}; ev={x['id'] for x in d['evidence']}; require(len(sources)==len(d['sources']) and len(ev)==len(d['evidence']),'duplicate source/evidence ID'); require(all(re.fullmatch(r'S[1-9][0-9]*',i) for i in sources) and all(re.fullmatch(r'E[1-9][0-9]*',i) for i in ev),'source IDs S1…; evidence IDs E1…')
    for a in d['sources']: require(a.get('title') and a.get('locator'),'source title and locator required')
    for a in d['evidence']:
        require(a['kind'] in ('official','user','inference','recommendation') and a['statement'],'invalid evidence'); require(a['source_ids'] and set(a['source_ids'])<=sources,'unresolved source IDs')
        if a['kind']=='official': require(all(next(x for x in d['sources'] if x['id']==i).get('url','').startswith(('https://','http://')) for i in a['source_ids']),'official evidence needs source URL')
    ids=set()
    for p in d['slides']:
        require(re.fullmatch(r'[a-z0-9]+(?:[-_][a-z0-9]+)*',p['id']) and p['id'] not in ids,'invalid or duplicate slide id'); ids.add(p['id'])
        require(p['evidence_ids'] and set(p['evidence_ids'])<=ev,'unresolved evidence IDs')
        require(p.get('title') and p.get('conclusion'),'title and conclusion required')
def build(d,out):
    check_deck(d); require(not out.exists() or not any(out.iterdir()),'output directory must be empty')
    # Build all slides in memory before writing; layout error leaves output untouched.
    slides=[]; entries=[]
    for i,p in enumerate(d['slides']):
        num=d.get('start_page',1)+i; filename=p['id']+'.svg'
        evidence=' '.join('['+e+']' for e in p['evidence_ids']); sub=(p.get('subtitle','')+'  '+evidence).strip()
        s=SVG(p['title'],sub,num,d['label']); build_slide(s,p); slides.append((filename,s)); entries.append({'file':filename,'page':num,'title':p['title'],'evidence_ids':p['evidence_ids']})
    out.mkdir(parents=True,exist_ok=True)
    for f,s in slides:s.write(out/f)
    m={'label':d['label'],'sources':d['sources'],'evidence':d['evidence'],'limitations':d.get('limitations',[]),'slides':entries}
    (out/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
    def cell(x):return str(x).replace('|','\\|').replace('\n',' ')
    lines=['# 来源与 SVG 映射','','| 来源 | 定位 | SVG |','|---|---|---|']; em={e['id']:e for e in d['evidence']}
    for a in d['sources']:
        files=[p['file'] for p in entries if any(a['id'] in em[e]['source_ids'] for e in p['evidence_ids'])]; lines.append(f"| {cell(a['title'])} {cell(a.get('url',''))} | {cell(a['locator'])} | {', '.join(files)} |")
    lines+=['','## 证据登记']+[f"- {e['id']} ({e['kind']})：{e['statement']} — {', '.join(e['source_ids'])}" for e in d['evidence']]+['','## 限制']+['- '+x for x in d.get('limitations',[])]
    (out/'source-map.md').write_text('\n'.join(lines)+'\n',encoding='utf-8'); return len(slides)
if __name__=='__main__':
    a=argparse.ArgumentParser(); a.add_argument('deck',type=Path); a.add_argument('--out',required=True,type=Path); p=a.parse_args()
    try: print(f"Built {build(json.loads(p.deck.read_text(encoding='utf-8')),p.out)} SVG(s) in {p.out}")
    except (ValueError,KeyError,TypeError,OSError) as e: sys.exit(f'BUILD ERROR: {e}')
