import json, math, unicodedata, xml.etree.ElementTree as ET
from pathlib import Path
TOK=json.loads((Path(__file__).resolve().parents[1]/'assets/design-tokens.json').read_text())
C=TOK['colors']; FONT=TOK['font']; NS='http://www.w3.org/2000/svg'
ET.register_namespace('',NS)
def n(v): return f'{v:.3f}'.rstrip('0').rstrip('.') if isinstance(v,float) else str(v)
def width(s, size):
    return size*sum(1.03 if unicodedata.east_asian_width(c) in 'WF' else .65 if c.isupper() else .57 if c.isalnum() else .39 for c in s)
def wrap(s,size,maxw):
    # Prefer word boundaries for Latin tokens; split oversized tokens only as needed.
    import re
    lines=[]
    for paragraph in str(s).split('\n'):
        line=''
        for token in re.findall(r'[A-Za-z0-9_./:-]+|\s+|.',paragraph):
            if width(token,size)>maxw:
                parts=list(token)
            else: parts=[token]
            for p in parts:
                if line and width(line+p,size)>maxw:
                    lines.append(line.rstrip()); line=p.lstrip()
                else: line+=p
        lines.append(line.rstrip())
    return lines
class SVG:
    def __init__(self,title,subtitle,page,label):
        self.root=ET.Element('{'+NS+'}svg',{'width':'1280','height':'720','viewBox':'0 0 1280 720'})
        self.add('title').text=title
        self.rect(0,0,1280,720,'white')
        size=28 if width(title,28)<=1184 else 24
        self.text(48,64,title,size,'title',True,maxw=1184)
        if subtitle: self.text(48,86,subtitle,13.33,'secondary',maxw=1184)
        self.rect(48,98,1184,4,'title')
        self.text(48,700,str(page),9.33,'faint',maxw=150)
        self.text(1232,700,label,9.33,'faint',anchor='end',maxw=900)
    def add(self,tag,**attrs):
        return ET.SubElement(self.root,'{'+NS+'}'+tag,{k.replace('_','-'):n(v) for k,v in attrs.items() if v is not None})
    def rect(self,x,y,w,h,fill='white',stroke=None,rx=0):
        if min(w,h)<0: raise ValueError('negative rectangle')
        return self.add('rect',x=x,y=y,width=w,height=h,rx=rx,fill=C.get(fill,fill),stroke=C.get(stroke,stroke),stroke_width=1 if stroke else None)
    def text(self,x,y,s,size=12,color='ink',bold=False,anchor='start',maxw=None):
        if '\n' in str(s): raise ValueError('use multiline block')
        if maxw is not None and width(str(s),size)>maxw: raise ValueError(f'text too wide: {s!r} ({width(str(s),size):.0f} > {maxw:.0f})')
        t=self.add('text',x=x,y=y,font_family=FONT,font_size=size,font_weight=700 if bold else 400,fill=C.get(color,color),text_anchor=anchor); t.text=str(s); return t
    def block(self,x,y,w,h,s,size=12,color='ink',bold=False,anchor='start',center=False):
        ls=wrap(s,size,w); leading=size*1.4
        if len(ls)*leading>h+0.01: raise ValueError(f'text too tall: {s!r} ({len(ls)*leading:.1f} > {h:.1f})')
        top=y+(h-len(ls)*leading)/2 if center else y
        for i,l in enumerate(ls): self.text(x if anchor=='start' else x+w/2,top+size+i*leading,l,size,color,bold,anchor,maxw=w)
    def arrow(self,x1,y1,x2,y2,color='blue'):
        a=math.atan2(y2-y1,x2-x1); length=math.hypot(x2-x1,y2-y1)
        if length<7: raise ValueError('arrow too short')
        b=(x2-7*math.cos(a),y2-7*math.sin(a)); d=(4*math.sin(a),-4*math.cos(a))
        self.add('line',x1=x1,y1=y1,x2=b[0],y2=b[1],stroke=C[color],stroke_width=1.5)
        self.add('polygon',points=' '.join(f'{n(x)},{n(y)}' for x,y in [(x2,y2),(b[0]+d[0],b[1]+d[1]),(b[0]-d[0],b[1]-d[1])]),fill=C[color])
    def card(self,x,y,w,h,title,body,accent='title',fill='panel'):
        self.rect(x,y,w,h,fill,'border',8); self.rect(x,y,3.2,h,accent)
        ls=wrap(title,14,w-28); th=len(ls)*19.6
        self.block(x+14,y+10,w-28,th,title,14,accent,True)
        self.block(x+14,y+16+th,w-28,h-24-th,body,12,center=True)
    def conclusion(self,s):
        self.rect(48,628,1184,48,'red-tint-2',rx=4)
        self.block(62,633,1156,38,s,14,'title',True,center=True)
    def write(self,p):
        ET.indent(self.root,space='  '); ET.ElementTree(self.root).write(p,encoding='utf-8',xml_declaration=True)
