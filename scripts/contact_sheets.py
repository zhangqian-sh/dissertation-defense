"""Create small contact sheets from browser screenshots for visual review."""
from pathlib import Path
import argparse
import subprocess
from PIL import Image, ImageOps, ImageDraw
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--pdf',action='store_true',help='Render and inspect the exported PDF instead of browser screenshots')
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]/'artifacts'
if args.pdf:
    (root/'pdf-pages').mkdir(exist_ok=True)
    subprocess.run(['pdftocairo','-png','-scale-to','600',str(root/'defense.pdf'),str(root/'pdf-pages'/'page')],check=True)
files=sorted((root/('pdf-pages' if args.pdf else 'slides')).glob('*.png'))
for start in range(0,len(files),12):
    canvas=Image.new('RGB',(1200,760),'#dce1df'); draw=ImageDraw.Draw(canvas)
    for i,p in enumerate(files[start:start+12]):
        image=Image.open(p).convert('RGB'); image.thumbnail((386,217))
        x=10+(i%3)*400;y=10+(i//3)*190
        image.thumbnail((386,165)); canvas.paste(image,(x,y+15));draw.text((x,y),p.stem,fill='#232727')
    canvas.save(root/f'{"pdf-" if args.pdf else ""}contact-{start//12+1}.png')
