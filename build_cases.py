#!/usr/bin/env python3
"""Generate the three case-study pages from one template.

Each page shares the site stylesheet and the same GSAP setup as the index,
so a change to style.css propagates everywhere.
"""
from pathlib import Path

ROOT = Path(__file__).parent

HEAD = '''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<script>document.documentElement.classList.replace('no-js','js')</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300..700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<div class="aurora"></div>
<div class="grain"></div>

<div class="shell">
  <aside class="rail">
    <a class="back" href="/"><span class="ar">&larr;</span> Matviy Korsunskiy</a>
    <div class="role">{railrole}</div>
    <div class="avail"><span class="dot"></span>Available for contract</div>
    <nav>
      <a href="mailto:matviykorsunskiy@gmail.com">Email</a>
      <a href="https://www.linkedin.com/in/matviykorsunskiy">LinkedIn</a>
    </nav>
    <div class="tz">Eastern time<br>New Jersey, US</div>
  </aside>

  <main class="col">
    <div class="rv">
      <div class="case-hero">
        <div class="logo"><img src="/logos/{logo}" alt="{client}"></div>
        <div>
          <h1>{client}</h1>
          <div class="case-meta">{meta} &nbsp;·&nbsp; <a href="{url}" target="_blank" rel="noopener">{domain} &#8599;</a></div>
        </div>
      </div>
    </div>
'''

FOOT = '''
    <h2 class="sec">Other work</h2>
    <div class="nextprev" data-reveal>
{nextprev}
    </div>

    <footer>
      <div data-reveal>
        <p class="cta">If any of this is the shape of your problem, I&rsquo;d like to hear about it.</p>
        <div class="btns">
          <a class="btn solid magnetic" href="mailto:matviykorsunskiy@gmail.com">matviykorsunskiy@gmail.com</a>
          <a class="btn ghost magnetic" href="https://www.linkedin.com/in/matviykorsunskiy">LinkedIn</a>
        </div>
        <p class="disclaim">
          Client names and internal details omitted where I am under confidentiality.<br>
          Happy to go deeper on any of it on a call.
        </p>
      </div>
    </footer>
  </main>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.15.0/gsap.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.15.0/ScrollTrigger.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.15.0/SplitText.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.3.26/dist/lenis.min.js" defer></script>
<script src="/motion.js" defer></script>
</body>
</html>
'''


def flow(steps, note=None):
    out = ['      <div class="flow-wrap" data-pipe>', '        <ol class="flow">',
           '          <li class="flow-line"></li>']
    for i, (t, d, k) in enumerate(steps, 1):
        kc = ' key' if k else ''
        out.append(f'          <li class="fstep{kc}"><span class="fnode"></span>'
                   f'<span class="fnum">{i:02d}</span>'
                   f'<span class="fbody"><b>{t}</b><span>{d}</span></span></li>')
    out.append('        </ol>')
    if note:
        out.append(f'        <p class="flow-note">{note}</p>')
    out.append('      </div>')
    return '\n'.join(out)


def chips(items):
    out = ['      <div class="stack" data-reveal>']
    for label, img, wide in items:
        cls = ' class="wide"' if wide else ''
        out.append(f'        <span class="chip"><img src="/logos/tools/{img}" alt=""{cls}>{label}</span>')
    out.append('      </div>')
    return '\n'.join(out)


def stats(items):
    out = ['      <div class="stats" data-stats>']
    for v, k, hi, count in items:
        h = ' hi' if hi else ''
        c = f' data-count="{count[0]}" data-suffix="{count[1]}"' if count else ''
        out.append(f'        <div class="stat{h}"><span class="v"{c}>{v}</span><span class="k">{k}</span></div>')
    out.append('      </div>')
    return '\n'.join(out)


def pending(lines):
    body = '<br>'.join(lines)
    return f'      <div class="shot-pending">{body}</div>'


def nextprev(pairs):
    return '\n'.join(
        f'      <a class="npcard" href="{href}"><span class="l">{lbl}</span><span class="n">{name}</span></a>'
        for lbl, name, href in pairs)
