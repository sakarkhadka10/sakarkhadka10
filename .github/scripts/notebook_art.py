"""Build self-contained GitHub-safe SVGs; typography is outlined, never fetched."""
from pathlib import Path
from html import escape
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[2]
FONTS = ROOT / 'design/fonts'
INK, PAPER, BLUE = '#191919', '#f8f7f2', '#2855e8'
YELLOW, MINT, PINK = '#f6c945', '#a9e3d0', '#ff4f91'
fonts = {name: TTFont(FONTS / file) for name, file in {
    'display': 'jersey-10-latin.woff2', 'sans': 'space-grotesk-latin.woff2',
    'hand': 'caveat.ttf',
}.items()}


def text(value, x, y, size, font='sans', color=INK, spacing=0):
    face = fonts[font]
    glyphs = face.getGlyphSet()
    cmap = face.getBestCmap()
    scale = size / face['head'].unitsPerEm
    paths, advance = [], 0
    for char in value:
        name = cmap.get(ord(char))
        if name is None:
            raise ValueError(f'Unsupported character {char!r} in {font}')
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(pen)
        commands = pen.getCommands()
        if commands:
            paths.append(f'<path transform="translate({advance:.2f} 0)" d="{commands}"/>')
        advance += glyphs[name].width + spacing / scale
    return (f'<g aria-label="{escape(value, quote=True)}" fill="{color}" '
            f'transform="translate({x} {y}) scale({scale:.6f} {-scale:.6f})">'
            + ''.join(paths) + '</g>')


def svg(width, height, title, description, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>'
            + body + '</svg>\n')


def star(x, y, size, color=YELLOW, rotation=0):
    return f'''<path transform="translate({x} {y}) rotate({rotation}) scale({size / 100})"
    d="M0-50 13-19 43-25 25 0 43 25 13 19 0 50-13 19-43 25-25 0-43-25-13-19Z"
    fill="{color}" stroke="{INK}" stroke-width="2.8" stroke-linejoin="round"/>'''



# Keep the toolbox focused on the primary stack, in portfolio category order.
SKILL_GROUPS = [
    ('Frontend', BLUE, [
        ('typescript', 'TypeScript', '#3178c6'), ('react', 'React', '#087ea4'),
        ('nextdotjs', 'Next.js', '#191919'), ('tailwindcss', 'Tailwind CSS', '#087ea4'),
    ]),
    ('Backend', YELLOW, [
        ('nodedotjs', 'Node.js', '#43853d'), ('nestjs', 'NestJS', '#e0234e'),
    ]),
    ('Data & ORM', MINT, [
        ('postgresql', 'PostgreSQL', '#4169e1'), ('drizzle', 'Drizzle', '#4f661d'),
        ('redis', 'Redis', '#d82c20'),
    ]),
    ('Cloud & tools', PINK, [
        ('docker', 'Docker', '#1d63ed'), ('cloudflare', 'Cloudflare', '#be4b00'),
        ('git', 'Git', '#f05032'),
    ]),
]
SKILLS = [skill for _, _, group in SKILL_GROUPS for skill in group]


def centered_text(value, center, y, size):
    face = fonts['sans']
    glyphs = face.getGlyphSet()
    cmap = face.getBestCmap()
    width = sum(glyphs[cmap[ord(char)]].width for char in value)
    width *= size / face['head'].unitsPerEm
    return text(value, center - width / 2, y, size)


def render_workbench(mobile=False):
    """One curated stack and one renderer keep both responsive layouts in sync."""
    import xml.etree.ElementTree as ET
    width, height = (640, 658) if mobile else (1000, 438)
    body = f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    body += f'<path d="M35 1V{height-1}" stroke="#e2b8b4"/>'
    for index, (category, accent, group) in enumerate(SKILL_GROUPS):
        top = 13 + index * (160 if mobile else 104)
        if index:
            body += f'<path d="M50 {top-3}H{width-20}" stroke="{INK}" stroke-opacity=".16"/>'
        body += f'<rect x="54" y="{top+12}" width="5" height="23" rx="2" fill="{accent}"/>'
        body += text(category, 72, top+33 if mobile else top+51, 27 if mobile else 25)
        for column, (slug, label, color) in enumerate(group):
            center = (106 + column*140) if mobile else (342 + column*176)
            y = top + (55 if mobile else 10)
            icon = ET.parse(ROOT / f'design/icons/{slug}.svg').getroot()
            paths = ''.join(f'<path d="{el.attrib["d"]}"/>' for el in icon.iter() if el.tag.endswith('path'))
            size = 53 if mobile else 47
            # Logos retain recognizable brand colors against the warm paper.
            body += f'<g transform="translate({center-size/2} {y}) scale({size/24})" fill="{color}">{paths}</g>'
            body += centered_text(label, center, y+size+29, 23 if mobile else 20)
    description = '; '.join(category + ': ' + ', '.join(skill[1] for skill in group)
                            for category, _, group in SKILL_GROUPS)
    return svg(width, height, 'Core skills — the workbench', description, body)


PROJECTS = [
    ('munal', 'munal.webp', 'MUNAL ONLINE', 'Money moves. Simply.', 'Next.js / Expo / NestJS', YELLOW),
    ('xeno', 'xeno.webp', 'XENONEPAL', 'Good game. Great experience.', 'Next.js / NestJS / PostgreSQL', '#ffdeeb'),
    ('merokarya', 'merokarya.webp', 'MEROKARYA', 'A little less busywork.', 'Next.js / NestJS / Prisma', MINT),
    ('everest', 'everest.jpg', 'THE EVEREST', 'The art of slowing down.', 'Next.js / NestJS / Tailwind', '#e5ebfa'),
]
