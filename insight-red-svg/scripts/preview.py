import argparse,sys
from pathlib import Path
from validate import validate
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('folder',type=Path);a.add_argument('--out',type=Path,required=True);a.add_argument('--font',help='Installed preview-only fallback font');p=a.parse_args()
    if not validate(p.folder)['passed']:sys.exit('Static validation failed')
    try:import cairosvg
    except ImportError:sys.exit('Optional CairoSVG is not installed; use browser or other local renderer')
    p.out.mkdir(parents=True,exist_ok=True)
    for f in sorted(p.folder.glob('*.svg')):
        raw=f.read_text(encoding='utf-8')
        if p.font:
            import html
            raw=raw.replace('font-family="微软雅黑"','font-family="'+html.escape(p.font,quote=True)+'"')
        cairosvg.svg2png(bytestring=raw.encode(),write_to=str(p.out/(f.stem+'.png')))
    print('Rendered preview files. Visually inspect each; rendering alone is not acceptance. Preview font:',p.font or '微软雅黑 (system fallback possible)')
