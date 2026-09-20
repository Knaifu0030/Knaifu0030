"""BLACK ICE: character-only render of the user-selected Climber panel."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageFilter
from html import escape
import random,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent;A=R/'assets/black-ice';A.mkdir(parents=True,exist_ok=True)
source=R/'source/climber-panel.jpg'
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
src=Image.open(source).convert('L')
def render(im,cols,out,animate=False):
 rows=round(im.height/im.width*cols*.59);g=ImageOps.autocontrast(im).resize((cols,rows),Image.Resampling.LANCZOS)
 edges=g.filter(ImageFilter.FIND_EDGES);ramp=' .,:;irsXA253hMHGS#9B&@';cw,ch=8,13
 w,h=cols*cw,rows*ch
 parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="#0d1117"/>']
 if animate:parts.append('<style>@keyframes air{0%,100%{opacity:.55}50%{opacity:1}}.air{animation:air 9s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.air{animation:none}}</style>')
 lines=[]
 for y in range(rows):
  buckets={};line=''
  for x in range(cols):
   v=(g.getpixel((x,y))/255)**.77
   c=ramp[min(len(ramp)-1,int(v*(len(ramp)-1)))];line+=c
   if c==' ':continue
   # Fine tonal separation preserves the figure while dark sky stays open.
   shade=[125,170,213,244][min(3,int(v*4))]
   key=(shade,animate and x<cols*.53 and y<rows*.6 and (x+3*y)%17==0)
   buckets.setdefault(key,[]).append((x,c))
  lines.append(line)
  for (shade,motion),chars in buckets.items():
   for x,c in chars:
    parts.append(f'<text x="{x*cw}" y="{y*ch+11}" font-family="monospace" font-size="13" fill="rgb({shade},{shade},{shade})"'+(' class="air"' if motion else '')+'>'+escape(c)+'</text>')
 parts.append('</svg>');(A/out).write_text(''.join(parts));(A/(Path(out).stem+'.txt')).write_text('\n'.join(lines))
render(src,180,'panel.svg',True);render(src,180,'panel-static.svg')
render(src.crop((330,0,1280,924)),105,'panel-mobile.svg',True);render(src.crop((330,0,1280,924)),105,'panel-mobile-static.svg')
render(src.crop((780,175,1210,660)),72,'detail-structure.svg')
render(src.crop((80,65,650,705)),72,'detail-sky.svg')
render(src.crop((0,20,780,220)),160,'ribbon.svg')
# Custom outlined ASCII wordmark, consistent glyph construction.
letters={'K':['#   #','#  # ','###  ','#  # ','#   #'],'N':['#   #','##  #','# # #','#  ##','#   #'],'A':[' ### ','#   #','#####','#   #','#   #'],'I':['#####','  #  ','  #  ','  #  ','#####'],'F':['#####','#    ','#### ','#    ','#    '],'U':['#   #','#   #','#   #','#   #',' ### ']}
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="170" viewBox="0 0 960 170"><style>@keyframes reveal{from{opacity:0}to{opacity:1}}.mark{animation:reveal 1.5s ease-out both}@media(prefers-reduced-motion:reduce){.mark{animation:none}}</style><rect width="960" height="170" fill="#0d1117"/>']
for row in range(5):
 line='   '.join(letters[c][row] for c in 'KNAIFU').replace('#','/')
 parts.append(f'<text class="mark" x="34" y="{33+row*22}" xml:space="preserve" font-family="monospace" font-size="23" letter-spacing="2" fill="#e1e5e8">{line}</text>')
parts.append('<text x="860" y="142" font-family="monospace" font-size="13" fill="#8293a0">0030</text><path d="M34 159H926" stroke="#35424d"/></svg>');(A/'signature.svg').write_text(''.join(parts))
# Borderless icons with only small row separators.
for name in ['tools-matrix.svg','tools-matrix-mobile.svg']:
 s=(R/'assets'/name).read_text();s=s.replace('</svg>','</svg>',1)
 pos=s.rfind('</svg>');s=s[:pos]+''.join(f'<path d="M50 {y}H910" stroke="#27313b"/>' for y in [126,238,350])+s[pos:]
 (A/name).write_text(s)
print('Character-only assets generated; original image is never embedded.')
