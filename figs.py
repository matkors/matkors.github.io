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


def layer(name, title):
    """A sub-heading inside 'What I built'."""
    return ('      <div class="secnum" data-reveal>%s &nbsp;&middot;&nbsp; %s</div>'
            % (name, title))
