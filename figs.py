#!/usr/bin/env python3
"""Figure helpers for the case-study pages."""


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
