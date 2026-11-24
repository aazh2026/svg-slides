import argparse,json,sys,zipfile
from pathlib import Path
from validate import validate

def package(folder,out):
    r=validate(folder)
    if not r['passed']:raise ValueError('static validation failed; run validate.py')
    if out.exists():raise ValueError('archive already exists')
    m=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    with zipfile.ZipFile(out,'x',zipfile.ZIP_DEFLATED) as z:
        for name in [s['file'] for s in m['slides']]+['manifest.json','source-map.md']:z.write(folder/name,name)
        z.writestr('qa.json',json.dumps(r,ensure_ascii=False,indent=2))
    return len(m['slides'])
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('folder',type=Path);a.add_argument('--out',type=Path,required=True);p=a.parse_args()
    try:print(f'Packaged {package(p.folder,p.out)} SVG(s): {p.out}')
    except (ValueError,OSError) as e:sys.exit(str(e))
