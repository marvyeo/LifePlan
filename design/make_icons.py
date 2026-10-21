"""Life Plan ecosystem icon set: one style for every app.
Dark tile, single line-art glyph in the app's accent colour, same stroke weight and safe zone.
Run: python3 make_icons.py <outdir>  -> <outdir>/<app>/icon-192.png, icon-512.png, + preview.png
"""
import sys, os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 2048                      # draw size, downsampled later
BG = (16, 21, 27)
W = int(S * 0.055)            # stroke width (same for every glyph)

APPS = {
    'lifeplan':        ('Life Plan',         '#7C9CFF'),
    'tvworld':         ('TV World',          '#A78BFA'),
    'financialplanner':('Financial Planner', '#4FB0E8'),
    'comicstracker':   ('ComicsTracker',     '#F2B84B'),
    'mccinventory':    ('MCC Inventory',     '#3FC1A5'),
    'chorewheel':      ('ChoreWheel',        '#E58FD0'),
    'foodguide':       ('Makan Map',         '#FF8A5B'),
    'vacationguru':    ('VacationGuru',      '#5BC0EB'),
    'novelreader':     ('NovelReader',       '#F07167'),
}

def P(x, y): return (x * S, y * S)
def hexrgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def line(d, pts, c, w=W, caps=True):
    d.line([P(*p) for p in pts], fill=c, width=w, joint='curve')
    if not caps: return
    r = w / 2
    for p in (pts[0], pts[-1]):
        x, y = P(*p); d.ellipse([x - r, y - r, x + r, y + r], fill=c)

def rrect(d, box, rad, c, w=W, fill=None):
    d.rounded_rectangle([*P(box[0], box[1]), *P(box[2], box[3])], radius=rad * S, outline=c, width=w, fill=fill)

def circle(d, cx, cy, r, c, w=W, fill=None):
    d.ellipse([*P(cx - r, cy - r), *P(cx + r, cy + r)], outline=None if fill and w == 0 else c, width=w, fill=fill)

# ---------- glyphs (all within roughly 0.25..0.75) ----------
def g_lifeplan(d, c):
    rrect(d, (0.25, 0.30, 0.75, 0.74), 0.07, c)
    line(d, [(0.26, 0.42), (0.74, 0.42)], c, caps=False)
    line(d, [(0.36, 0.25), (0.36, 0.33)], c); line(d, [(0.64, 0.25), (0.64, 0.33)], c)
    line(d, [(0.39, 0.585), (0.47, 0.655), (0.62, 0.51)], c)

def g_tvworld(d, c):
    rrect(d, (0.23, 0.29, 0.77, 0.67), 0.07, c)
    d.polygon([P(0.455, 0.40), P(0.455, 0.56), P(0.585, 0.48)], fill=c)
    line(d, [(0.40, 0.76), (0.60, 0.76)], c)

def g_financialplanner(d, c):
    rrect(d, (0.22, 0.32, 0.78, 0.70), 0.06, c)
    line(d, [(0.23, 0.43), (0.77, 0.43)], c, caps=False)
    rrect(d, (0.30, 0.52, 0.42, 0.61), 0.02, c, w=int(W * 0.8))
    line(d, [(0.55, 0.60), (0.68, 0.60)], c)

def g_comicstracker(d, c):
    # speech bubble with a lightning bolt
    d.rounded_rectangle([*P(0.22, 0.27), *P(0.78, 0.65)], radius=0.12 * S, outline=c, width=W)
    d.polygon([P(0.36, 0.62), P(0.33, 0.78), P(0.48, 0.64)], fill=c)
    d.polygon([P(0.53, 0.32), P(0.42, 0.48), P(0.50, 0.48), P(0.46, 0.60), P(0.59, 0.43), P(0.51, 0.43), P(0.55, 0.32)], fill=c)

def g_mccinventory(d, c):
    # isometric box
    top = [(0.50, 0.24), (0.75, 0.36), (0.50, 0.48), (0.25, 0.36), (0.50, 0.24)]
    line(d, top, c)
    line(d, [(0.25, 0.36), (0.25, 0.64), (0.50, 0.77), (0.75, 0.64), (0.75, 0.36)], c)
    line(d, [(0.50, 0.48), (0.50, 0.77)], c)
    line(d, [(0.375, 0.30), (0.625, 0.42)], c, w=int(W * 0.7))

def g_chorewheel(d, c):
    circle(d, 0.5, 0.5, 0.25, c)
    circle(d, 0.5, 0.5, 0.06, c, w=0, fill=c)
    for i in range(6):
        a = math.radians(i * 60 - 90)
        line(d, [(0.5 + 0.095 * math.cos(a), 0.5 + 0.095 * math.sin(a)), (0.5 + 0.215 * math.cos(a), 0.5 + 0.215 * math.sin(a))], c, w=int(W * 0.8))

def g_foodguide(d, c):
    # bowl + chopsticks + steam
    d.chord([*P(0.22, 0.30), *P(0.78, 0.82)], start=0, end=180, outline=c, width=W)
    line(d, [(0.22, 0.56), (0.78, 0.56)], c)
    line(d, [(0.40, 0.76), (0.60, 0.76)], c)
    line(d, [(0.52, 0.47), (0.76, 0.22)], c, w=int(W * 0.8)); line(d, [(0.58, 0.49), (0.80, 0.27)], c, w=int(W * 0.8))
    pts = [(0.36 + 0.025 * math.sin(t / 10 * 2 * math.pi), 0.45 - 0.19 * t / 20) for t in range(21)]
    line(d, pts, c, w=int(W * 0.7))

def g_vacationguru(d, c):
    # paper plane
    line(d, [(0.22, 0.47), (0.78, 0.25), (0.62, 0.76), (0.49, 0.56), (0.22, 0.47)], c)
    line(d, [(0.49, 0.56), (0.78, 0.25)], c)
    line(d, [(0.49, 0.56), (0.47, 0.70)], c)

def g_novelreader(d, c):
    # open book
    line(d, [(0.50, 0.34), (0.40, 0.29), (0.22, 0.29), (0.22, 0.70), (0.40, 0.70), (0.50, 0.75), (0.60, 0.70), (0.78, 0.70), (0.78, 0.29), (0.60, 0.29), (0.50, 0.34)], c)
    line(d, [(0.50, 0.34), (0.50, 0.75)], c)
    line(d, [(0.30, 0.42), (0.42, 0.42)], c, w=int(W * 0.6)); line(d, [(0.30, 0.52), (0.42, 0.52)], c, w=int(W * 0.6))
    line(d, [(0.58, 0.42), (0.70, 0.42)], c, w=int(W * 0.6)); line(d, [(0.58, 0.52), (0.70, 0.52)], c, w=int(W * 0.6))

GLYPHS = {k: globals()['g_' + k] for k in APPS}

def make(app):
    _, col = APPS[app]
    rgb = hexrgb(col)
    im = Image.new('RGB', (S, S), BG)
    # soft accent halo behind the glyph
    halo = Image.new('RGB', (S, S), BG); hd = ImageDraw.Draw(halo)
    hd.ellipse([*P(0.18, 0.18), *P(0.82, 0.82)], fill=tuple(int(BG[i] + (rgb[i] - BG[i]) * 0.16) for i in range(3)))
    halo = halo.filter(ImageFilter.GaussianBlur(S * 0.06))
    im.paste(halo)
    d = ImageDraw.Draw(im)
    GLYPHS[app](d, rgb)
    return im

def main(out):
    os.makedirs(out, exist_ok=True)
    tiles = []
    for app in APPS:
        im = make(app)
        os.makedirs(f'{out}/{app}', exist_ok=True)
        for size in (192, 512):
            im.resize((size, size), Image.LANCZOS).save(f'{out}/{app}/icon-{size}.png')
        im.resize((180, 180), Image.LANCZOS).save(f'{out}/{app}/apple-touch-icon.png')
        tiles.append((app, im.resize((220, 220), Image.LANCZOS)))
    # preview sheet: icons with iOS-style rounded mask + labels, 3 per row
    cols, cell_w, cell_h = 3, 300, 300
    rows = math.ceil(len(tiles) / cols)
    sheet = Image.new('RGB', (cols * cell_w, rows * cell_h + 20), (236, 239, 243))
    sd = ImageDraw.Draw(sheet)
    try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
    except Exception: font = ImageFont.load_default()
    mask = Image.new('L', (220, 220), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, 219, 219], radius=50, fill=255)
    for i, (app, t) in enumerate(tiles):
        x, y = (i % cols) * cell_w + 40, (i // cols) * cell_h + 25
        sheet.paste(t, (x, y), mask)
        name = APPS[app][0]
        tw = sd.textlength(name, font=font)
        sd.text((x + 110 - tw / 2, y + 232), name, fill=(40, 46, 54), font=font)
    sheet.save(f'{out}/preview.png')

if __name__ == '__main__':
    main(sys.argv[1])
