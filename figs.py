#!/usr/bin/env python3
"""Figure, nav and text helpers for the case-study pages."""


def fig(num, label, src, caption):
    """One framed screenshot with a numbered label chip and a caption."""
    return (
        '      <figure class="fig" data-reveal>\n'
        '        <div class="figlabel"><b>%s</b> %s</div>\n'
        '        <div class="frame"><img src="/shots/%s" alt="%s" loading="lazy"></div>\n'
        '        <figcaption>%s</figcaption>\n'
        '      </figure>' % (num, label, src, label, caption)
    )


def figpair(src, alt, items, caption=None):
    """A screenshot beside a numbered legend that matches badges drawn on it."""
    out = [
        '      <div class="figpair" data-reveal>',
        '        <figure class="fig" style="margin:0">',
        '          <div class="frame"><img src="/shots/%s" alt="%s" loading="lazy"></div>' % (src, alt),
    ]
    if caption:
        out.append('          <figcaption>%s</figcaption>' % caption)
    out.append('        </figure>')
    out.append('        <ul class="legend">')
    for i, (title, body) in enumerate(items, 1):
        out.append('          <li><span class="n">%d</span><span><b>%s</b>%s</span></li>'
                   % (i, title, body))
    out.append('        </ul>')
    out.append('      </div>')
    return '\n'.join(out)


def toc(items):
    """In-page nav for the sticky rail. items = [(anchor, num, label), ...]"""
    out = ['    <nav class="toc">']
    for anchor, num, label in items:
        out.append('      <a href="#%s"><span class="tn">%s</span>%s</a>' % (anchor, num, label))
    out.append('    </nav>')
    return '\n'.join(out)


def sec_id(num, label, title, anchor):
    """Numbered section heading the rail nav can target."""
    return ('      <div data-reveal id="%s">\n'
            '        <div class="secnum">%s &nbsp;&middot;&nbsp; %s</div>\n'
            '        <h2 class="sec">%s</h2>\n'
            '      </div>' % (anchor, num, label, title))


def lead(text):
    """An opening sentence set slightly larger than body copy."""
    return '      <p class="lead" data-reveal>%s</p>' % text


def notes(items):
    """Compact supporting notes under a stats block. Not paragraphs."""
    lines = ['      <ul class="notes" data-reveal>']
    lines += ['        <li>%s</li>' % i for i in items]
    lines.append('      </ul>')
    return '\n'.join(lines)


def layer(name, title):
    """A sub-heading inside 'What I built'."""
    return ('      <div class="secnum" data-reveal>%s &nbsp;&middot;&nbsp; %s</div>'
            % (name, title))


def nda(headline, body, sub=None):
    """The confidentiality notice, stated loudly and early.

    Deliberately not buried at the bottom: a reader should hit the limit
    before they go looking for screenshots that are never coming.
    """
    out = ['      <div class="nda" data-reveal>',
           '        <div class="lbl">Under contract</div>',
           '        <p class="ndah">%s</p>' % headline,
           '        <p class="ndab">%s</p>' % body]
    if sub:
        out.append('        <p class="ndas">%s</p>' % sub)
    out.append('      </div>')
    return '\n'.join(out)


def ladder(rungs, note=None):
    """The escalation ladder: my own framework, not client work product."""
    out = ['      <div class="ladderlabel"><b>Framework</b> How a regulated agent decides what it may say</div>',
           '      <ol class="ladder" data-reveal>']
    for i, (title, body, stop) in enumerate(rungs, 1):
        cls = ' stop' if stop else ''
        out.append('        <li class="rung%s"><span class="rn">%02d</span>'
                   '<span class="rb"><b>%s</b><span>%s</span></span></li>' % (cls, i, title, body))
    out.append('      </ol>')
    if note:
        out.append('      <p class="laddernote" data-reveal>%s</p>' % note)
    return '\n'.join(out)


def reqs(items, label):
    """A numbered list of externally imposed requirements."""
    out = ['      <div class="reqbox" data-reveal>',
           '        <div class="lbl">%s</div>' % label,
           '        <ol class="reqlist">']
    for title, body in items:
        out.append('          <li><b>%s</b><span>%s</span></li>' % (title, body))
    out += ['        </ol>', '      </div>']
    return '\n'.join(out)


def seealso(intro, items):
    """Point at the pages that can show the work, from the page that cannot."""
    out = ['      <div class="seealso" data-reveal>',
           '        <div class="lbl">Want the technical detail?</div>',
           '        <p>%s</p>' % intro,
           '        <div class="salinks">']
    for name, sub, href in items:
        out.append('          <a href="%s"><span class="sn">%s</span>'
                   '<span class="ss">%s</span><span class="sa">&rarr;</span></a>'
                   % (href, name, sub))
    out += ['        </div>', '      </div>']
    return '\n'.join(out)
