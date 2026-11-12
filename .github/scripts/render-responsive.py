"""Art-directed narrow-screen assets. Selected by README picture media queries."""
import base64
from notebook_art import ROOT, INK, PAPER, BLUE, YELLOW, MINT, PINK, PROJECTS, text, svg, star

def frame(height):
    return (f'<rect x="1" y="1" width="638" height="{height-2}" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M35 1V{height-1}" stroke="#e2b8b4"/>')

def save(name, height, title, desc, body):
    (ROOT / f'assets/{name}-mobile.svg').write_text(svg(640, height, title, desc, body))

motion='''<style>@keyframes drift{0%,100%{transform:translate(0,0) rotate(-4deg)}50%{transform:translate(-10px,-8px) rotate(5deg)}}
@keyframes dash{to{stroke-dashoffset:-60}}
.float{animation:drift 6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
.trail{animation:dash 10s linear infinite}
@media(prefers-reduced-motion:reduce){.float,.trail{animation:none}}</style>'''
body=motion+frame(440)
body+=text('a developer’s notebook', 62, 55, 32, 'hand', BLUE)
body+=text('SAKAR', 58, 165, 126, 'display', spacing=3)
body+=f'<path d="M61 263H542V283H61Z" fill="{MINT}"/>'
body+=text('KHADKA.', 58, 277, 126, 'display', spacing=3)
body+=text('Full Stack Engineer / Nepal', 63, 326, 27)
body+=text('Useful. Thoughtful. Shipped.', 63, 394, 32, 'hand', BLUE)
body+=star(561, 84, 62, YELLOW, 12)
body+=f'<g transform="translate(516 337) scale(.39)"><g class="float"><path d="m20 93 201-73-61 158-54-59-56 28 9-47Z" fill="{YELLOW}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/><path d="m59 100 162-80-115 99 54 59M106 119l-8 35-48-7" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/></g></g>'
save('notebook-cover',440,'Sakar Khadka — a developer’s notebook','Full Stack Engineer, Nepal. Useful. Thoughtful. Shipped.',body)

for name, number, title in [
 ('projects','01','SELECTED PAGES.'),('skills','02','THE WORKBENCH.'),
 ('activity','03','CODE IN MOTION.'),('opensource','04','OPEN BY DEFAULT.'),
 ('play','05','A LITTLE HAPPY CHAOS.')]:
    body=frame(90)+text(number,55,57,35,'display',BLUE)+text(title,116,60,43,'display')
    save('heading-'+name,90,title,title,body)

for slug,file,title,tagline,stack,color in PROJECTS:
    src=ROOT/'design/projects'/file
    mime='image/jpeg' if src.suffix=='.jpg' else 'image/webp'
    data=base64.b64encode(src.read_bytes()).decode()
    body=f'<rect x="1" y="1" width="398" height="368" rx="9" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    body+=f'<clipPath id="preview"><rect x="14" y="14" width="372" height="210" rx="4"/></clipPath><image href="data:{mime};base64,{data}" x="14" y="14" width="372" height="210" preserveAspectRatio="xMidYMid slice" clip-path="url(#preview)"/>'
    body+=f'<path d="M20 275H331V294H20Z" fill="{color}"/>'
    body+=text(title,20,287,43,'display')
    mobile_tag={'munal':'Wallets & remittance','xeno':'Gaming & subscriptions','merokarya':'Everyday digital tools','everest':'Spa & wellness'}[slug]
    body+=text(mobile_tag,20,324,24,'hand',BLUE)
    body+=f'<path d="M355 346 376 325m-20 0h20v20" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
    (ROOT/f'assets/projects/{slug}-mobile.svg').write_text(svg(400,370,title,mobile_tag,body))

from notebook_art import render_workbench
(ROOT / 'assets/workbench-mobile.svg').write_text(render_workbench(mobile=True))

body=frame(394)
for y,color,name,desc in [(20,YELLOW,'mero-nepali-utils','Dates, closer to home.'),(207,MINT,'@axcore/xicons','Little icons. Thoughtful details.')]:
    body+=f'<rect x="56" y="{y+4}" width="558" height="164" rx="4" fill="{INK}"/><rect x="52" y="{y}" width="558" height="164" rx="4" fill="{color}" stroke="{INK}" stroke-width="2"/>'
    body+=text(name,73,y+54,34)
    body+=text(desc,73,y+101,32,'hand',BLUE)
    body+=text('TypeScript / open source',73,y+140,21)
save('opensource',394,'Small tools, shared openly','mero-nepali-utils and @axcore/xicons',body)

body=motion+frame(290)
body+=text('Less overthinking.',60,58,32,'hand',BLUE)
body+=text('MORE MAKING.',57,111,53,'display')
body+=f'<path class="trail" d="M66 219C161 105 250 255 370 185S481 203 545 139" fill="none" stroke="{BLUE}" stroke-width="2" stroke-dasharray="5 8"/>'
body+=f'<g transform="translate(468 123) scale(.52)"><g class="float"><path d="m20 93 201-73-61 158-54-59-56 28 9-47Z" fill="{YELLOW}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/><path d="m59 100 162-80-115 99 54 59M106 119l-8 35-48-7" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/></g></g>'
body+=text('Take the kite for a spin.',60,260,26)
save('kite',290,'Less overthinking. More making.','Animated portfolio kite. Visit the playground.',body)

body=frame(210)+text('Have something good in mind?',58,48,28,'hand',BLUE)
body+=f'<path d="M58 89H493V111H58Z" fill="{MINT}"/>'
body+=text('LET’S MAKE IT REAL.',56,108,49,'display')
body+=f'<rect x="368" y="139" width="229" height="49" rx="3" fill="{YELLOW}" stroke="{INK}" stroke-width="2"/>'
body+=text('Say hello',390,172,28)
body+=f'<path d="M558 173 578 153m-20 0h20v20" fill="none" stroke="{INK}" stroke-width="2.5"/>'
save('notebook-footer',210,'Have something good in mind? Let’s make it real.','Say hello to Sakar.',body)
print('Rendered narrow-screen notebook artwork.')
