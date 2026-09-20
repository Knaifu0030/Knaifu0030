"""Original character-built mountain. No raster or generated art embedded."""
from pathlib import Path
from html import escape
import random, math,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent;A=R/'assets';rng=random.Random(31)
W,H=104,42;grid=[[' ']*W for _ in range(H)]
def put(x,y,c):
 if 0<=x<W and 0<=y<H:grid[y][x]=c
# Main summit contour: left snow face; sharply hatched shadow face.
peak=59
for y in range(5,40):
 t=y-5;left=peak-int(t*1.33);right=peak+int(t*.94)
 put(left,y,'/');put(right,y,'\\')
 ridge=peak-int(t*.26)
 if t:put(ridge,y,'\\')
 for x in range(left+1,right):
  if x>ridge:
   if (x+y)%3==0:put(x,y,'/')
   elif (x-y)%7==0:put(x,y,':')
  elif t>3 and (x+2*y)%13==0:put(x,y,'/')
  elif t>8 and (2*x-y)%31==0:put(x,y,'.')
# Glacial ledges give authored directional structure, not luminance noise.
for y,x,length in [(16,49,8),(21,42,10),(27,33,12),(33,26,14)]:
 for j in range(length):put(x+j,y,'_' if j<length-2 else '/')
# Foreground ridge, visually distinct from central face.
for y in range(29,42):
 left=24-(y-29)*2;right=24+(y-29)*3
 put(left,y,'/');put(right,y,'\\')
 for x in range(max(0,left+1),min(W,right)):
  if x<27 and (x+y)%4==0:put(x,y,'/')
# Tiny, deliberately authored climber and ice axe on the near ridge.
for dy,line in enumerate(['  O  /',' /|_/ ',' / \\  ']):
 for dx,c in enumerate(line):
  if c!=' ':put(22+dx,25+dy,c)
# Distant ridge, fainter in SVG by row color.
for y in range(22,39):
 x=91-(y-22);put(x,y,'/');put(91+(y-22)//2,y,'\\')
rows=[''.join(r).rstrip() for r in grid]
(A/'summit.txt').write_text('\n'.join(rows)+'\n')
def svg(mobile=False,static=False):
 width=960;height=590;parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>Knaifu — ASCII summit</title><desc>Character-built mountain, climber, drifting snow. Original composition inspired by The Climber.</desc><rect width="960" height="590" fill="#0d1117"/><text x="32" y="41" font-family="monospace" font-size="18" letter-spacing="5" fill="#dce4ec">KNAIFU</text><text x="840" y="40" font-family="monospace" font-size="12" fill="#8c9ba9">0030</text>']
 if not static:parts.append('<style>@keyframes snow{0%{transform:translate(0,0);opacity:0}15%{opacity:.6}85%{opacity:.6}100%{transform:translate(-32px,46px);opacity:0}}@keyframes cloud{0%,100%{transform:translateX(0)}50%{transform:translateX(16px)}}.snow{animation:snow 12s linear infinite}.cloud{animation:cloud 24s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.snow,.cloud{animation:none}}</style>')
 for i,line in enumerate(rows):parts.append(f'<text x="35" y="{97+i*10.8:.1f}" xml:space="preserve" font-family="monospace" font-size="14" textLength="{len(line)*8.5}" lengthAdjust="spacingAndGlyphs" fill="#c6cfd6">{escape(line)}</text>')
 parts.append('<g class="cloud" fill="#61707f" font-family="monospace" font-size="15"><text x="125" y="170">.  . ___ . .</text><text x="160" y="184">_ _ .      . _</text><text x="652" y="137">. _ __ .</text></g>')
 for i in range(19):
  x=rng.randint(80,870);y=rng.randint(95,330)
  parts.append(f'<text class="snow" x="{x}" y="{y}" font-family="monospace" font-size="13" fill="#97aabb" style="animation-delay:-{i*.71:.2f}s">{[".","+","."][i%3]}</text>')
 parts.append('<path d="M32 559H928" stroke="#25313d"/><text x="32" y="578" font-family="monospace" font-size="11" fill="#758695">/\\</text><text x="880" y="578" font-family="monospace" font-size="11" fill="#758695">. /</text></svg>');return ''.join(parts)
(A/'summit.svg').write_text(svg());(A/'summit-static.svg').write_text(svg(static=True))
# Borderless 4 x 4 icon matrix; geometry itself enforces symmetry.
names=['typescript','javascript','react','nextjs','tailwindcss','threejs','nodejs','python','tensorflow','git','github','linux','vercel','azure','html5','css3']
labels=['TypeScript','JavaScript','React','Next.js','Tailwind','Three.js','Node.js','Python','TensorFlow','Git','GitHub','Linux','Vercel','Azure','HTML','CSS']
def icons(mobile=False):
 parts=['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="470" viewBox="0 0 960 470"><rect width="960" height="470" fill="#0d1117"/>']
 for i,(name,label) in enumerate(zip(names,labels)):
  x=120+(i%4)*240;y=25+(i//4)*112;root=ET.fromstring((A/'icons'/f'{name}.svg').read_text());inside=''.join(ET.tostring(c,encoding='unicode') for c in root);vb=root.attrib.get('viewBox','0 0 128 128');size=54 if name not in ['linux','python','tailwindcss'] else 60
  parts.append(f'<svg x="{x-size/2}" y="{y}" width="{size}" height="{size}" viewBox="{vb}">{inside}</svg><text x="{x}" y="{y+83}" text-anchor="middle" font-family="monospace" font-size="{21 if mobile else 15}" fill="#a4b0bc">{label}</text>')
 parts.append('</svg>');return ''.join(parts)
(A/'tools-matrix.svg').write_text(icons());(A/'tools-matrix-mobile.svg').write_text(icons(True))
print('Built true ASCII summit and borderless icon matrix')
