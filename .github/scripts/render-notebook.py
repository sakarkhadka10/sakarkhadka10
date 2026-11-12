"""Rebuild the GitHub notebook cover, footer, and skill badges."""
from notebook_art import ROOT, INK, PAPER, BLUE, YELLOW, MINT, PINK, text, svg, star

cover = f'''<defs><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
  <path d="M24 0H0V24" fill="none" stroke="{BLUE}" stroke-opacity=".10"/></pattern></defs>
<rect x="1" y="1" width="998" height="438" rx="12" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>
<path d="M45 1V439" stroke="#e2b8b4" stroke-width="1"/>
<path d="M46 380H970" stroke="{INK}" stroke-opacity=".22" stroke-dasharray="5 6"/>
'''
# A few subtle binding holes; the cover remains opaque and legible in both themes.
for y in [65, 130, 195, 260, 325, 390]:
    cover += f'<circle cx="22" cy="{y}" r="5" fill="#deddd6" stroke="{INK}" stroke-opacity=".18"/>'
cover += text('a developer’s notebook', 76, 63, 30, 'hand', BLUE)
cover += text('SAKAR', 72, 177, 130, 'display', spacing=4)
cover += f'<path d="M76 275Q300 266 559 277L556 291 77 292Z" fill="{MINT}"/>'
cover += text('KHADKA.', 72, 283, 130, 'display', spacing=4)
cover += text('Full Stack Engineer', 78, 333, 24)
cover += f'<circle cx="328" cy="325" r="3" fill="{BLUE}"/>'
cover += text('Nepal', 343, 333, 24)
cover += text('a few pages from my world', 78, 414, 26, 'hand', BLUE)
cover += text('CODE / COFFEE / CURIOSITY', 642, 411, 13, color=INK, spacing=1.4)
# A taped graph-paper note echoes the portfolio’s notebook and hard shadows.
cover += f'''<g transform="translate(654 93) rotate(5 135 125)">
  <rect x="7" y="9" width="260" height="243" rx="2" fill="{INK}"/>
  <rect width="260" height="243" rx="2" fill="#eef1fa" stroke="{INK}" stroke-width="2"/>
  <rect x="1" y="1" width="258" height="241" fill="url(#grid)"/>
  <path d="M83-13 175-10 170 19 80 16Z" fill="{YELLOW}" fill-opacity=".88" stroke="{INK}" stroke-width="1.4"/>
  <path d="m31 55-13 13 13 13m31-26 13 13-13 13m-13-31-9 36" fill="none" stroke="{BLUE}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
'''
cover += text('note to self:', 31, 117, 25, 'hand', BLUE)
cover += text('Useful.', 30, 154, 35, 'hand')
cover += text('Thoughtful.', 30, 188, 35, 'hand')
cover += text('Shipped.', 30, 222, 35, 'hand')
cover += '</g>'
cover += star(926, 89, 75, YELLOW, 15)
cover += star(609, 291, 38, PINK, -10)
# The portfolio’s paper plane, drawn as native paths.
cover += f'''<path d="M827 350q85 27 107-7" fill="none" stroke="{BLUE}" stroke-width="1.8" stroke-dasharray="4 5"/>
<g transform="translate(904 272) rotate(-10) scale(.29)">
  <path d="m20 93 201-73-61 158-54-59-56 28 9-47Z" fill="{PAPER}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
  <path d="m59 100 162-80-115 99 54 59M106 119l-8 35-48-7" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
</g>'''
(ROOT / 'assets/notebook-cover.svg').write_text(svg(1000, 440,
    'Sakar Khadka — a developer’s notebook',
    'Full Stack Engineer, Nepal. A paper notebook with a taped note: Useful. Thoughtful. Shipped.', cover))

footer = f'''<rect x="1" y="1" width="998" height="152" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>
<path d="M32 122H968" stroke="{INK}" stroke-opacity=".2" stroke-dasharray="5 6"/>
<path d="M48 79 478 75 481 100 47 104Z" fill="{MINT}"/>
'''
footer += text('Have something good in mind?', 45, 54, 24, 'hand', BLUE)
footer += text('Let’s make it real.', 44, 100, 44, 'display', spacing=1)
footer += f'''<g transform="translate(717 46) rotate(-3)">
<rect x="5" y="6" width="220" height="54" rx="3" fill="{INK}"/>
<rect width="220" height="54" rx="3" fill="{YELLOW}" stroke="{INK}" stroke-width="2"/>
'''
footer += text('Say hello', 24, 35, 24)
footer += f'<path d="M179 34 197 17m-17 0h17v17" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></g>'
footer += star(651, 74, 40, PINK, 12)
(ROOT / 'assets/notebook-footer.svg').write_text(svg(1000, 154,
    'Have something good in mind? Let’s make it real.',
    'A handwritten invitation on paper, with a yellow Say hello sticker.', footer))
print('Rendered notebook cover and footer.')

# Individual badges wrap naturally in GitHub’s sanitized README layout.


# Reuse the exact paper-plane geometry from the portfolio’s arcade kite.
MOTION = '''<style>
@keyframes drift{0%,100%{transform:translate(0,0) rotate(-4deg)}50%{transform:translate(-12px,-9px) rotate(5deg)}}
@keyframes turn{0%,100%{transform:rotate(-6deg)}50%{transform:rotate(9deg)}}
@keyframes dash{to{stroke-dashoffset:-60}}
.float{animation:drift 6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
.twinkle{animation:turn 8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
.trail{animation:dash 10s linear infinite}
@media(prefers-reduced-motion:reduce){.float,.twinkle,.trail{animation:none}}
</style>'''

def page_heading(number, title, note):
    body = f'<rect x="1" y="1" width="998" height="98" rx="9" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    body += f'<path d="M45 1V99" stroke="#e2b8b4"/>'
    body += f'<circle cx="22" cy="50" r="5" fill="#deddd6"/>'
    body += text(number, 65, 61, 35, 'display', BLUE)
    body += text(title, 133, 64, 44, 'display', spacing=1)
    body += text(note, 715, 60, 25, 'hand', BLUE)
    return body

for name, number, title, note in [
    ('projects', '01', 'SELECTED PAGES.', 'built to be used'),
    ('skills', '02', 'THE WORKBENCH.', 'tools of the trade'),
    ('activity', '03', 'CODE IN MOTION.', 'one day at a time'),
    ('opensource', '04', 'OPEN BY DEFAULT.', 'small tools, big care'),
    ('play', '05', 'A LITTLE HAPPY CHAOS.', 'keep being curious'),
]:
    (ROOT / f'assets/heading-{name}.svg').write_text(svg(1000, 100, title, note, page_heading(number, title, note)))

# Each project is one self-contained paper card. Embedded raster previews avoid
# network dependencies inside SVG images served by GitHub’s image proxy.
import base64
from notebook_art import PROJECTS as project_cards
for slug, file, title, tagline, stack, color in project_cards:
    src = ROOT / 'design/projects' / file
    mime = 'image/jpeg' if src.suffix == '.jpg' else 'image/webp'
    data = base64.b64encode(src.read_bytes()).decode()
    body = f'<rect x="1" y="1" width="598" height="478" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    body += f'<rect x="17" y="17" width="566" height="320" rx="5" fill="{color}"/>'
    body += f'<clipPath id="preview"><rect x="18" y="18" width="564" height="318" rx="4"/></clipPath>'
    body += f'<image href="data:{mime};base64,{data}" x="18" y="18" width="564" height="318" preserveAspectRatio="xMidYMid slice" clip-path="url(#preview)"/>'
    body += f'<path d="M24 383H355V400H24Z" fill="{color}"/>'
    body += text(title, 25, 394, 43, 'display', spacing=1)
    body += text(tagline, 26, 428, 25, 'hand', BLUE)
    body += text(stack, 26, 456, 16)
    body += f'<path d="M543 402 568 377m-24 0h24v24" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
    (ROOT / f'assets/projects/{slug}.svg').write_text(svg(600, 480, title, tagline + ' Built with ' + stack, body))

# Curated portfolio skills, shared with the narrow-screen renderer.
from notebook_art import render_workbench
(ROOT / 'assets/workbench.svg').write_text(render_workbench())

# Open source stays as two concise notebook index cards.
body = f'<rect x="1" y="1" width="998" height="220" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
for x, color, name, desc, command in [
    (25, YELLOW, 'mero-nepali-utils', 'Dates, closer to home.', 'npm i mero-nepali-utils'),
    (515, MINT, '@axcore/xicons', 'Little icons. Thoughtful details.', 'npm i @axcore/xicons'),
]:
    body += f'<rect x="{x+3}" y="26" width="457" height="171" rx="3" fill="{INK}"/>'
    body += f'<rect x="{x}" y="23" width="457" height="171" rx="3" fill="{color}" stroke="{INK}" stroke-width="1.5"/>'
    body += text(name, x+20, 75, 29)
    body += text(desc, x+20, 116, 28, 'hand', BLUE)
    body += text(command, x+20, 164, 19)
(ROOT / 'assets/opensource.svg').write_text(svg(1000, 222, 'Small tools, shared openly',
    'mero-nepali-utils: BS–AD date conversions. @axcore/xicons: TypeScript icons for React and Next.js.', body))

# A small breathing-space animation, linked to the actual portfolio playground.
body = MOTION + f'''<defs><pattern id="squares" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{BLUE}" stroke-opacity=".08"/></pattern></defs>
<rect x="1" y="1" width="998" height="218" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>
<rect x="2" y="2" width="996" height="216" rx="10" fill="url(#squares)"/>
<path class="trail" d="M58 171C195 52 230 194 375 119S579 181 716 95" fill="none" stroke="{BLUE}" stroke-width="2" stroke-dasharray="6 9"/>
<g transform="translate(705 23) rotate(8) scale(.56)"><g class="float">
<path d="m20 93 201-73-61 158-54-59-56 28 9-47Z" fill="{YELLOW}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
<path d="m59 100 162-80-115 99 54 59M106 119l-8 35-48-7" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>
</g></g>'''
body += text('Less overthinking.', 54, 67, 30, 'hand', BLUE)
body += text('MORE MAKING.', 51, 115, 52, 'display', spacing=2)
body += text('Take the kite for a spin in my portfolio.', 55, 188, 22)
body += '<g class="twinkle">' + star(909, 145, 60, PINK) + '</g>'
(ROOT / 'assets/kite.svg').write_text(svg(1000, 220, 'Less overthinking. More making.',
    'An animated paper kite follows a dotted flight path. Visit the portfolio playground.', body))
# Add gentle movement to the cover’s existing paper plane and star.
cover_path = ROOT / 'assets/notebook-cover.svg'
value = cover_path.read_text().replace('<defs>', MOTION+'<defs>', 1)
value = value.replace('<g transform="translate(904 272)', '<g class="float" transform="translate(904 272)')
# Keep geometry and animation on separate groups so CSS never overrides SVG placement.
value = value.replace('<g class="float" transform="translate(904 272) rotate(-10) scale(.29)">',
    '<g transform="translate(904 272) rotate(-10) scale(.29)"><g class="float">')
value = value.replace('</g></svg>', '</g></g></svg>')
cover_path.write_text(value)
print('Rendered notebook section pages, project cards, stack, open source, and animated kite.')

# Narrow-screen artwork is selected with native HTML picture sources.
import runpy
runpy.run_path(str(ROOT / ".github/scripts/render-responsive.py"))
