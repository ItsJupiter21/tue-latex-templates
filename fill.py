"""Write the copier answers into the new project's .tex (run by copier, in the new folder).

Argument: the answers as JSON. Only the document-data lines at the top of the .tex
change; the rest stays the template's.
"""
import json
import re
import sys

a = json.loads(sys.argv[1])
kind = a['kind']


def get(key, default=''):
    return a.get(key, default) or default


def setline(text, cmd, value, opt=None):
    """Replace the argument of the first line starting with \\cmd, keeping its comment."""
    pattern = re.compile(r'^(\\' + cmd + r')(\[[^\]]*\])?\{.*?\}(\s*%.*)?$', re.M)
    arg = ('[' + opt + ']' if opt is not None else '')
    new, n = pattern.subn(lambda m: m.group(1) + (arg or (m.group(2) or ''))
                          + '{' + value.replace('\\', '\\\\') + '}' + (m.group(3) or ''),
                          text, count=1)
    if n != 1:
        sys.exit(f'fill.py: no \\{cmd} line found')
    return new


def block(text, cmd, rows):
    """\\cmd{% ... } spans several lines: replace it as a whole, one row per line."""
    pattern = re.compile(r'^\\' + cmd + r'\{%\n.*?^\}', re.M | re.S)
    body = '\\' + cmd + '{%\n' + ''.join(f'  {r}\n' for r in rows) + '}'
    new, n = pattern.subn(lambda m: body, text, count=1)
    if n != 1:
        sys.exit(f'fill.py: no \\{cmd} block found')
    return new


def items(s):
    return [x.strip() for x in s.split(',') if x.strip()]


f = {'cbl': 'main.tex', 'note': 'note.tex', 'thesis': 'thesis.tex',
     'slides': 'slides.tex', 'poster': 'poster.tex', 'cuecards': 'cuecards.tex'}[kind]
t = open(f).read()
title = get('title')

if kind == 'slides':
    t = setline(t, 'title', title)
    t = setline(t, 'subtitle', get('course'))
    t = setline(t, 'author', get('name'), opt=get('name'))
elif kind == 'note':
    t = setline(t, 'reporttitle', title)
    t = setline(t, 'reportsubtitle', get('name'))
    t = setline(t, 'reportauthors', get('name'))
    t = setline(t, 'reportversion', get('version'))
elif kind == 'thesis':
    t = setline(t, 'reporttype', get('thesis_type'))
    t = setline(t, 'reporttitle', title)
    t = setline(t, 'reportsubtitle', get('subtitle'))
    t = setline(t, 'reportauthors', get('name'))
    t = setline(t, 'reportstudentid', get('student_id'))
    t = setline(t, 'reportversion', get('version'))
    t = setline(t, 'reportgroup', get('group'))
    t = setline(t, 'reportdepartment', get('department'))
    t = block(t, 'reportsupervisor', [s + r'\\' for s in items(get('supervisor'))])
elif kind == 'poster':
    t = setline(t, 'reporttitle', title)
    t = setline(t, 'reportsubtitle', get('subtitle'))
    t = setline(t, 'reportauthors', get('authors'))
    t = setline(t, 'reportdepartment', get('department'))
elif kind == 'cuecards':
    t = setline(t, 'reporttitle', title)
    t = setline(t, 'reportauthors', get('name'))
else:  # cbl
    t = setline(t, 'reporttitle', title)
    t = setline(t, 'reportsubtitle', get('course'))
    t = setline(t, 'reportversion', get('version'))
    t = setline(t, 'reportgroup', get('group'))
    t = setline(t, 'reportsupervisor', get('supervisor'))
    rows = []
    for x in items(get('authors')):
        m = re.match(r'(.*?)\s+(\d{5,})$', x)
        rows.append((f'{m.group(1)} & {m.group(2)}' if m else f'{x} & ') + r' \\')
    t = block(t, 'reportauthors', rows)
accent = get('accent').lstrip('#').upper()
if accent:  # uncomment the \accentcolor line and set the color
    t, n = re.subn(r'^% (\\accentcolor)\{HTML\}\{[0-9A-Fa-f]{6}\}',
                   lambda m: m.group(1) + '{HTML}{' + accent + '}', t, count=1, flags=re.M)
    if n != 1:
        sys.exit('fill.py: no \\accentcolor line found')
font = get('font', 'modern')
if font != 'modern':  # \usepackage[font=noto]{tue...} / \usetheme[font=noto]{TUe}
    t, n = re.subn(r'^(\\use(?:package|theme))\{(tue\w+|TUe)\}',
                   lambda m: m.group(1) + f'[font={font}]{{' + m.group(2) + '}', t, count=1,
                   flags=re.M)
    if n != 1:
        sys.exit('fill.py: no \\usepackage{tue...} line found')
open(f, 'w').write(t)
