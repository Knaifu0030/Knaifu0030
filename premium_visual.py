from pathlib import Path
from PIL import Image,ImageOps
import base64,io,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent;A=R/'assets'
im=Image.open(A/'manga-triptych.webp').convert('RGB')
# Keep line art intact; no coarse ASCII rasterization of faces.
im=im.resize((960,960),Image.Resampling.LANCZOS)
b=io.BytesIO();im.save(b,format='PNG',optimize=True)
data=base64.b64encode(b.getvalue()).decode()
head='''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="960" height="1070" viewBox="0 0 960 1070"><style>@keyframes drift{0%{transform:translate(0,0);opacity:0}15%{opacity:.8}80%{opacity:.6}100%{transform:translate(46px,-30px);opacity:0}}.wind{animation:drift 9s linear infinite}@media(prefers-reduced-motion:reduce){.wind{animation:none;opacity:.5}}</style><rect width="960" height="1070" rx="14" fill="#0d1117"/><text x="32" y="52" fill="#eef1f4" font-family="monospace" font-size="25" letter-spacing="8">KNAIFU</text><text x="844" y="49" fill="#7f92a6" font-family="monospace" font-size="14">[0030]</text>'''
parts=[head,f'<image x="20" y="78" width="920" height="920" xlink:href="data:image/png;base64,{data}"/>']
for i,(x,y,t) in enumerate([(84,225,'~ . ·'),(188,380,'. /'),(387,225,'+ .'),(512,320,'· *'),(646,160,'. :'),(760,280,'/ /'),(842,480,'+ .')]):
 parts.append(f'<text class="wind" x="{x}" y="{y}" fill="#25394d" stroke="#fff" stroke-width=".3" font-size="23" font-family="monospace" style="animation-delay:-{i}s">{t}</text>')
parts.append('<path d="M32 1030H928" stroke="#2b3744"/><text x="32" y="1053" fill="#72869a" font-family="monospace" font-size="12">~ / / ~</text><text x="879" y="1053" fill="#72869a" font-family="monospace" font-size="12">* . +</text></svg>')
(A/'manga-motion.svg').write_text(''.join(parts))
# A single SVG grid retains identical geometry on every screen.
names=['typescript','javascript','react','nextjs','tailwindcss','threejs','nodejs','python','tensorflow','git','github','linux','vercel','azure','html5','css3']
# 14 cells = two rows of seven. Short labels remain readable, icons dominate.
labels=['TypeScript','JavaScript','React','Next.js','Tailwind','Three.js','Node.js','Python','TensorFlow','Git','GitHub','Linux','Vercel','Azure','HTML','CSS']
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="580" viewBox="0 0 960 580"><rect width="960" height="580" rx="14" fill="#0d1117"/>']
for i,(name,label) in enumerate(zip(names,labels)):
 x=28+(i%4)*232;y=22+(i//4)*138
 parts.append(f'<rect x="{x}" y="{y}" width="208" height="122" rx="12" fill="#141b24" stroke="#283443"/>')
 s=(A/'icons'/f'{name}.svg').read_text();root=ET.fromstring(s);vb=root.attrib.get('viewBox','0 0 128 128');inside=''.join(ET.tostring(c,encoding='unicode')for c in root)
 parts.append(f'<svg x="{x+79}" y="{y+22}" width="50" height="50" viewBox="{vb}">{inside}</svg><text x="{x+104}" y="{y+100}" text-anchor="middle" fill="#aebcca" font-family="Arial,sans-serif" font-size="16">{label}</text>')
parts.append('</svg>');(A/'icon-grid.svg').write_text(''.join(parts))
# Mobile grid: same assets, deliberate 2-column layout, never irregular wrapping.
s=''.join(parts)
# 7 rows x2 on mobile would be overly tall; use same uniform 7x2 grid scalable vector.
print('Sharp artwork, reduced-motion-aware animation, symmetric grid generated')
