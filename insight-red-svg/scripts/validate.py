import argparse,json,re,sys,math,xml.etree.ElementTree as ET
from pathlib import Path
from svg_core import C,FONT,NS,width
ALLOWED={'svg','title','desc','g','rect','text','tspan','line','path','polygon','polyline','circle','ellipse'}
ATTR={'width','height','viewBox','x','y','rx','ry','cx','cy','r','x1','y1','x2','y2','d','points','fill','stroke','stroke-width','stroke-dasharray','stroke-linecap','stroke-linejoin','font-family','font-size','font-weight','text-anchor','opacity','fill-opacity','stroke-opacity','id','dx','dy'}
def inspect(p):
    errors=[]; warnings=[]
    def err(s):errors.append(s)
    try:
        raw=p.read_text(encoding='utf-8');
        if re.search(r'<!DOCTYPE|<!ENTITY|<\?xml-stylesheet',raw,re.I): raise ValueError('forbidden document declaration')
        root=ET.fromstring(raw)
        if root.tag!='{'+NS+'}svg' or [root.get(k) for k in ('width','height','viewBox')]!=['1280','720','0 0 1280 720']:err('invalid canvas')
        texts=[]; rects=[]
        def number(e,k,default=0):
            val=float(e.get(k,default))
            if not math.isfinite(val): raise ValueError('non-finite geometry')
            return val
        def bounds(x,y,w,h):
            if w<0 or h<0 or x<-.02 or y<-.02 or x+w>1280.02 or y+h>720.02:err(f'out of canvas: {x},{y},{w},{h}')
        for e in root.iter():
            tag=e.tag.split('}')[-1]
            if e.tag!='{'+NS+'}'+tag or tag not in ALLOWED:err('forbidden element: '+tag)
            for k,v in e.attrib.items():
                if k not in ATTR or re.search(r'url\s*\(|var\s*\(|javascript:',v,re.I):err('forbidden attribute: '+k)
                if k in ('fill','stroke') and v.lower() not in {*C.values(),'none'}:err('undeclared color: '+v)
            if tag=='rect':
                x,y,w,h=(number(e,k) for k in ('x','y','width','height')); bounds(x,y,w,h); rects.append((x,y,w,h,e.get('fill')))
            elif tag=='line':
                x,y,x2,y2=(number(e,k) for k in ('x1','y1','x2','y2'));bounds(min(x,x2),min(y,y2),abs(x2-x),abs(y2-y))
            elif tag in ('polygon','polyline'):
                pts=[float(t) for t in re.split(r'[ ,\s]+',e.get('points','').strip()) if t];
                if len(pts)<4 or len(pts)%2 or not all(map(math.isfinite,pts)):err('invalid points')
                else: bounds(min(pts[::2]),min(pts[1::2]),max(pts[::2])-min(pts[::2]),max(pts[1::2])-min(pts[1::2]))
            elif tag in ('circle','ellipse'):
                x,y=number(e,'cx'),number(e,'cy'); rx,ry=(number(e,'r'),)*2 if tag=='circle' else (number(e,'rx'),number(e,'ry'));bounds(x-rx,y-ry,2*rx,2*ry)
            elif tag=='path':warnings.append('custom path bounds/relationships require visual review')
            elif tag=='tspan':warnings.append('tspan layout requires visual review')
            elif tag=='text':
                x,y,size=number(e,'x'),number(e,'y'),number(e,'font-size'); content=''.join(e.itertext()); texts.append((x,y,size,e.get('fill'),e.get('text-anchor','start'),content))
                if e.get('font-family')!=FONT:err('font must be '+FONT)
                if size<9.33:err('font below minimum: '+content[:40])
                w=width(content,size); anchor=e.get('text-anchor','start'); left=x-w if anchor=='end' else x-w/2 if anchor=='middle' else x
                if not list(e):bounds(left,y-size,w,size*1.2)
                if 118<=y<=676 and not list(e) and (left<47.9 or left+w>1232.1):err('content text outside margins: '+content[:40])
        if (0,0,1280,720,C['white']) not in rects:err('white background missing')
        if (48,98,1184,4,C['title']) not in rects:err('red rule missing')
        if not any(x==48 and y==64 and sz in (24,28) and col==C['title'] for x,y,sz,col,_,_ in texts):err('title missing')
        if not all(any(x==xx and y==700 and sz==9.33 and col==C['faint'] and an==aa for x,y,sz,col,an,_ in texts) for xx,aa in [(48,'start'),(1232,'end')]):err('footer missing')
        if not any(640<=y<=676 and sz>=14 and col==C['title'] for _,y,sz,col,_,_ in texts):err('bottom conclusion missing')
    except (OSError,ValueError,ET.ParseError) as e:err(str(e))
    return {'file':p.name,'errors':errors,'warnings':sorted(set(warnings))}
def validate(folder):
    results=[inspect(p) for p in sorted(folder.glob('*.svg'))]; issues=[]
    try:
        m=json.loads((folder/'manifest.json').read_text(encoding='utf-8')); files=[s['file'] for s in m['slides']]; actual=[r['file'] for r in results]
        if sorted(files)!=actual or not actual:issues.append('manifest/files mismatch or no SVGs')
        sources={s['id'] for s in m['sources']}; evidence={e['id']:e for e in m['evidence']}
        if len(sources)!=len(m['sources']) or len(evidence)!=len(m['evidence']):issues.append('duplicate IDs')
        for e in evidence.values():
            if not e['source_ids'] or not set(e['source_ids'])<=sources:issues.append('unresolved source: '+e['id'])
        for s in m['slides']:
            if not s['evidence_ids'] or not set(s['evidence_ids'])<=evidence.keys():issues.append('unresolved evidence: '+s['file'])
        if not (folder/'source-map.md').is_file():issues.append('source-map missing')
    except (OSError,ValueError,KeyError,TypeError) as e:issues.append(str(e))
    return {'passed':not issues and all(not r['errors'] for r in results),'scope':'static XML/style/approximate text bounds/source mapping; not visual or factual validation','manifest_errors':issues,'slides':results}
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('folder',type=Path);a.add_argument('--report',type=Path);p=a.parse_args();r=validate(p.folder);out=json.dumps(r,ensure_ascii=False,indent=2);print(out)
    if p.report:p.report.write_text(out+'\n',encoding='utf-8')
    sys.exit(0 if r['passed'] else 1)
