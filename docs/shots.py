#!/usr/bin/env python3
"""Rebuild the template PDFs and render the README screenshots into docs/img/.

Run from anywhere: python3 docs/shots.py   (needs latexmk, pdftoppm, Pillow)
"""
import os
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / 'docs' / 'img'
DPI = 150          # render resolution; images are scaled down from this
GAP = 40           # space between pages, px
SHADOW = 18        # shadow blur radius, px


def build(folder, doc, env=None):
    subprocess.run(['latexmk', '-pdf', '-quiet', f'{doc}.tex'], cwd=ROOT / folder,
                   env=env, check=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    return ROOT / folder / f'{doc}.pdf'


def page(pdf, n, dpi=DPI):
    with tempfile.TemporaryDirectory() as t:
        subprocess.run(['pdftoppm', '-r', str(dpi), '-f', str(n), '-l', str(n),
                        '-png', '-singlefile', str(pdf), f'{t}/p'], check=True)
        return Image.open(f'{t}/p.png').convert('RGB')


def autocrop(im, margin=30):
    """Trim white space around the content, keep a margin."""
    bg = Image.new('RGB', im.size, 'white')
    x0, y0, x1, y1 = ImageChops.difference(im, bg).getbbox()
    return im.crop((max(x0 - margin, 0), max(y0 - margin, 0),
                    min(x1 + margin, im.width), min(y1 + margin, im.height)))


def height(im, h):
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


def width(im, w):
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


def sheet(rows, name):
    """rows: list of lists of images. Each page gets a hairline border and a
    soft shadow; the background is transparent (works in light and dark)."""
    pad = 2 * SHADOW
    W = max(sum(i.width for i in r) + GAP * (len(r) - 1) for r in rows) + 2 * pad
    H = sum(max(i.height for i in r) for r in rows) + GAP * (len(rows) - 1) + 2 * pad
    shadow = Image.new('L', (W, H), 0)
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    y = pad
    for r in rows:
        rw = sum(i.width for i in r) + GAP * (len(r) - 1)
        x = (W - rw) // 2
        for im in r:
            shadow.paste(90, (x + 4, y + 8, x + 4 + im.width, y + 8 + im.height))
            x += im.width + GAP
        y += max(i.height for i in r) + GAP
    shadow = shadow.filter(ImageFilter.GaussianBlur(SHADOW))
    out.putalpha(shadow)
    out = Image.composite(Image.new('RGBA', (W, H), (0, 0, 0, 255)), out, shadow)
    out.putalpha(shadow)
    y = pad
    for r in rows:
        rw = sum(i.width for i in r) + GAP * (len(r) - 1)
        x = (W - rw) // 2
        for im in r:
            framed = im.copy()
            Image.Image.paste(framed, (215, 215, 215),
                              (0, 0, framed.width, 1))
            Image.Image.paste(framed, (215, 215, 215),
                              (0, framed.height - 1, framed.width, framed.height))
            Image.Image.paste(framed, (215, 215, 215), (0, 0, 1, framed.height))
            Image.Image.paste(framed, (215, 215, 215),
                              (framed.width - 1, 0, framed.width, framed.height))
            out.paste(framed, (x, y))
            x += im.width + GAP
        y += max(i.height for i in r) + GAP
    out.save(IMG / f'{name}.png', optimize=True)
    print(f'{name}.png  {out.width}x{out.height}')


def main():
    IMG.mkdir(parents=True, exist_ok=True)
    cbl = build('cbl-report', 'main')
    note = build('cbl-report', 'note')
    thesis = build('thesis', 'thesis')
    slides = build('beamer', 'slides')
    poster = build('poster', 'poster')
    cards = build('cuecards', 'cuecards')
    env = dict(os.environ, TEXINPUTS=f'{ROOT}/common:{ROOT}/cbl-report:')
    style = build('docs', 'style', env)

    P = 700   # portrait page height in the sheets, px
    # Overview: the three covers and the poster, a slide and a cue card
    card_text = page(cards, 2)
    card_text = card_text.crop((0, 0, card_text.width, card_text.height // 2))
    side = (P - GAP) // 2
    s1 = width(page(slides, 1), round(side * 16 / 9))
    c1 = width(card_text, s1.width)
    sheet([[height(page(thesis, 1), P), height(page(cbl, 1), P),
            height(page(poster, 1), P)]], 'overview')
    sheet([[s1, height(c1, s1.height)]], 'overview-landscape')

    sheet([[height(page(cbl, n), P) for n in (1, 4, 5)]], 'cbl-report')
    sheet([[height(page(note, 1), P)]], 'note')
    sheet([[height(page(thesis, n), P) for n in (1, 2)],
           [height(page(thesis, n), P) for n in (4, 12)]], 'thesis')
    S = 450
    sheet([[height(page(slides, n), S) for n in (1, 4)],
           [height(page(slides, n), S) for n in (6, 8)]], 'slides')
    sheet([[height(page(poster, 1), 1100)]], 'poster')
    logo = page(cards, 1)
    logo = logo.crop((0, 0, logo.width, logo.height // 2))
    sheet([[height(logo, 420), height(card_text, 420)]], 'cuecards')
    sheet([[width(autocrop(page(style, 1, 200)), 1100)]], 'style')

    # Accent colors: the same CBL page in Scarlet and two secondary colors
    pages = [height(page(cbl, 4), P)]
    for hexcolor in ('003399', '00AC82'):   # CH&T-Blue, ESoE-Green (manual, institute colors)
        pdf = variant('cbl-report', 'main', lambda s: s.replace(
            '% \\accentcolor{HTML}{003399}', f'\\accentcolor{{HTML}}{{{hexcolor}}}', 1))
        pages.append(height(page(pdf, 4), P))
    sheet([pages], 'accent')

    # Fonts: mlmodern (default), Computer Modern, Noto Sans; report text and a slide
    cols = []
    for font, name in (('modern', 'mlmodern (default)'), ('cm', 'Computer Modern'),
                       ('noto', 'Noto Sans (TU/e LaTeX font)')):
        opt = '' if font == 'modern' else f'[font={font}]'
        rep = variant('cbl-report', 'main', lambda s: s.replace(
            '\\usepackage{tuereport}', f'\\usepackage{opt}{{tuereport}}', 1))
        sli = variant('beamer', 'slides', lambda s: s.replace(
            '\\usetheme{TUe}', f'\\usetheme{opt}{{TUe}}', 1))
        text = page(rep, 4, 200)
        text = text.crop((round(text.width * 0.09), round(text.height * 0.07),
                          round(text.width * 0.91), round(text.height * 0.47)))
        text = width(text, 620)
        slide = width(page(sli, 4, 200), 620)
        cols.append(labelled([text, slide], name))
    sheet([cols], 'fonts')


def variant(folder, doc, edit):
    """Build folder/doc.tex with edit() applied to its source, in a temporary copy
    (inputs linked, never the build files). Returns the PDF path."""
    t = Path(tempfile.mkdtemp())
    src = (ROOT / folder / f'{doc}.tex').read_text()
    (t / f'{doc}.tex').write_text(edit(src))
    for f in (ROOT / folder).iterdir():
        if f.suffix in ('.sty', '.bib') or f.name in ('figures', 'latexmkrc'):
            (t / f.name).symlink_to(f.resolve())
    subprocess.run(['latexmk', '-pdf', '-quiet', f'{doc}.tex'], cwd=t, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return t / f'{doc}.pdf'


def labelled(images, label):
    """Stack images on one white card with a label on top."""
    from PIL import ImageDraw, ImageFont
    try:
        font = ImageFont.truetype('/usr/share/fonts/google-noto/NotoSans-Bold.ttf', 26)
    except OSError:
        font = ImageFont.load_default()
    w = max(i.width for i in images)
    h = 60 + sum(i.height for i in images) + 20 * (len(images) - 1)
    card = Image.new('RGB', (w, h), 'white')
    ImageDraw.Draw(card).text((20, 16), label, fill=(200, 25, 25), font=font)
    y = 60
    for i in images:
        card.paste(i, (0, y))
        y += i.height + 20
    return card


if __name__ == '__main__':
    main()
