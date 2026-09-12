#!/usr/bin/env python3
"""Generate the three case-study pages in the same system as the landing page.

Each page opens with the technical shape of the build, not the
built/tools/results summary from the landing card, which the reader has
already seen. Then: the constraints, how it works, the results, what
broke. Nothing narrative.

Run: python gen.py
"""
from pathlib import Path

LF = chr(10)

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
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
</head>
<body>

<div class="bar">
  <div class="wrap">
    <a class="back" href="/"><span class="ar">&larr;</span> Matviy Korsunskiy</a>
    <nav>
      <span class="here"><i></i>Available for contract</span>
      <a href="mailto:matviykorsunskiy@gmail.com">Email</a>
    </nav>
  </div>
</div>

<div class="wrap">
  <div class="hero">
    <a class="client" href="{url}" target="_blank" rel="noopener">
      <img src="/logos/{logo}" alt="">{client} <span class="ex">&#8599;</span>
    </a>
    <p class="cmeta">{meta}</p>
    <h1>{h1}</h1>
  </div>
'''

FOOT = '''
  <section>
    <p class="snum">Stack</p>
    <div class="stack">
{chips}
    </div>
  </section>

  <section>
    <p class="snum">More work</p>
    <div class="np">
{np}
    </div>
  </section>

  <div class="close">
    <h2>If any of this is the shape of your problem, <span class="q">I&rsquo;d like to hear about it.</span></h2>
    <div class="acts">
      <a class="btn solid" href="mailto:matviykorsunskiy@gmail.com">matviykorsunskiy@gmail.com</a>
      <a class="btn ghost" href="https://www.linkedin.com/in/matviykorsunskiy">LinkedIn</a>
    </div>
    <p class="fine">
      Eastern time, New Jersey, US<br>
      Client names and internal details omitted where I am under confidentiality.
    </p>
  </div>
</div>

<dialog class="lb" id="lb" aria-label="Enlarged image">
  <div class="lbinner">
    <button class="lbclose" type="button" aria-label="Close">&times;</button>
    <div class="lbscroll"><img alt=""></div>
    <p class="lbcap"></p>
  </div>
</dialog>

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.15.0/gsap.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.15.0/ScrollTrigger.min.js" defer></script>
<script src="/lightbox.js" defer></script>
<script>
window.addEventListener('load', function () {
  /* Without the libraries the page is already fully visible. */
  if (!window.gsap || !window.ScrollTrigger) return;
  gsap.registerPlugin(ScrollTrigger);
  gsap.matchMedia().add('(prefers-reduced-motion: no-preference)', function () {
    gsap.utils.toArray('section, .gate, .fig, .figpair').forEach(function (el) {
      gsap.from(el, {
        autoAlpha: 0, y: 26, duration: .7, ease: 'power2.out',
        scrollTrigger: { trigger: el, start: 'top 88%', once: true }
      });
    });
  });
});
</script>
</body>
</html>
'''


# ---------------------------------------------------------------- helpers
def system(rows):
    """The technical shape of the build.

    Deliberately NOT the built/tools/results summary from the landing
    card. Someone who clicked through has already read that, so repeating
    it spends the first screen of the page they came for on nothing.
    """
    out = ['  <dl class="spec">']
    for label, body in rows:
        out.append('    <div><dt>%s</dt><dd>%s</dd></div>' % (label, body))
    out.append('  </dl>')
    return '\n'.join(out)


def sec(num, title):
    return ('  <section>\n'
            '    <p class="snum">%s</p>\n'
            '    <h2>%s</h2>' % (num, title))


def endsec():
    return '  </section>'


def lead(t):
    return '    <p class="lead">%s</p>' % t


def p(*ts):
    return '\n'.join('    <p>%s</p>' % t for t in ts)


def pts(items):
    return ('    <ul class="pts">\n'
            + '\n'.join('      <li>%s</li>' % i for i in items)
            + '\n    </ul>')


def h3(name, title):
    return '    <h3><span>%s</span> &nbsp;%s</h3>' % (name, title)


def fig(num, label, src, caption):
    return ('    <figure class="fig">\n'
            '      <div class="figlabel"><b>%s</b> %s</div>\n'
            '      <div class="frame"><img src="/shots/%s" alt="%s" loading="lazy"></div>\n'
            '      <figcaption>%s</figcaption>\n'
            '    </figure>' % (num, label, src, label, caption))


def figpair(src, alt, items, caption):
    out = ['    <div class="figpair">',
           '      <figure class="fig" style="margin:0">',
           '        <div class="frame"><img src="/shots/%s" alt="%s" loading="lazy"></div>' % (src, alt),
           '        <figcaption>%s</figcaption>' % caption,
           '      </figure>',
           '      <ul class="legend">']
    for i, (t, b) in enumerate(items, 1):
        out.append('        <li><span class="n">%d</span><span><b>%s</b>%s</span></li>' % (i, t, b))
    out += ['      </ul>', '    </div>']
    return '\n'.join(out)


def stats(items):
    out = ['    <div class="stats">']
    for v, k, hi in items:
        out.append('      <div class="stat%s"><span class="v">%s</span><span class="k">%s</span></div>'
                   % (' hi' if hi else '', v, k))
    out.append('    </div>')
    return '\n'.join(out)


def note(t):
    return '    <p class="note">%s</p>' % t


def gate(label, t):
    return ('    <div class="gate">\n      <div class="lbl">%s</div>\n'
            '      <p>%s</p>\n    </div>' % (label, t))


def chips(items):
    return '\n'.join(
        '      <span class="chip"><img src="/logos/tools/%s" alt="">%s</span>' % (img, label)
        for label, img in items)


def np(pairs):
    return '\n'.join(
        '      <a class="npc" href="%s"><span class="l">Case study</span><span class="n">%s</span></a>'
        % (href, name) for name, href in pairs)


# ================================================= WORLD OF LUXURY
wol = HEAD.format(
    title='World of Luxury: a voice agent querying a live 5,000-product Shopify catalog | Matviy Korsunskiy',
    desc='Retell voice agent plus 6 n8n workflows. Cursor-paginated Shopify sync into Airtable, fuzzy product matching at 90-95%, CRM writeback on every call.',
    logo='wol-logo.png', client='World of Luxury',
    meta='Luxury watches and jewelry, Aventura FL &nbsp;&middot;&nbsp; ~$500K/yr on Shopify &nbsp;&middot;&nbsp; retained 8 months',
    url='https://worldofluxuryus.com',
    h1='Voice agent on a live 5,000-product catalog')

wol += LF.join([

    sec('01', 'Why a menu or a VA does not solve this'),
    pts(['The showroom is open Monday to Friday, 10am to 5pm. <b>9 in 10 calls arrive outside that window</b>, including $40,000 inquiries at 11pm and on Sundays. They were hitting a voicemail box nobody actioned before Monday.',
         'They hired a virtual assistant first. A VA without inventory access cannot answer the only question that matters: <em>do you have this piece, and what does it cost</em>.',
         'The catalog changes daily, so a static export is wrong within 24 hours. Any answer has to come from live data.',
         '<b>Speech-to-text mangles the brand names.</b> Jaeger-LeCoultre, Audemars Piguet, Breguet. Model numbers mix digits, letters and punctuation, carry a <code>Preowned-</code> prefix on some products only, and around 100 products are near-duplicates of each other.']),
    endsec(),

    sec('02', 'How it works'),
    lead('6 n8n workflows in 3 layers: keep the data current, answer the lookup, write the result back.'),

    h3('Layer 1', 'Catalog and order sync'),
    p('n8n&rsquo;s Shopify node returns 50 records per call, and looping it hard enough to finish a full pull kept tripping rate limits and deactivating the workflow. I replaced it with a custom HTTP request walking the <code>page_info</code> cursor at roughly 250 records per iteration: <b>5x the throughput</b>, stable unattended. It PATCHes into Airtable rather than creating, so a price change updates in place instead of duplicating the record.'),
    fig('Fig 1', 'Product sync, the pagination loop', 'sync-products.png',
        '<b>Build Request</b> assembles the next cursor, the HTTP node pulls a page, results are parsed and batched, then upserted into Airtable. <b>Has More Products?</b> feeds the arrow back round until Shopify stops returning a cursor.'),
    fig('Fig 2', 'Order sync, same shape but paced', 'sync-orders.png',
        'Identical pattern with one addition: a <b>Wait</b> node between iterations. Without it the loop trips Shopify&rsquo;s rate limit, which is what was silently killing the workflow before.'),

    h3('Layer 2', 'Lookup, ranking and disambiguation'),
    p('3 lookup workflows sit behind webhooks registered as agent tools. Each runs the same shape: extract the argument from the tool call, normalize it, query Airtable, rank the candidates, format the winner for speech.'),
    figpair('product-page-annotated.png', 'A product page showing the 3 matchable fields',
            [('Product name', 'Long and brand-heavy. This is what callers mispronounce and what speech-to-text mangles.'),
             ('Price', 'The tiebreaker. When a name hits a cluster of near-identical pieces, price separates them.'),
             ('Model number', 'Digits, letters, dots, and a <code>Preowned-</code> prefix only some products carry.')],
            'A real listing. These 3 fields are everything the agent has to match against.'),
    fig('Fig 3', 'Lookup by name and price', 'lookup-details.png',
        '<b>Extract &amp; Normalize</b> pulls the argument out of the tool call, Airtable returns candidates, then <b>Fuzzy Match &amp; Rank</b> reduces them to one.'),
    fig('Fig 4', 'Lookup by model number', 'lookup-reference.png',
        'Same shape pointed at the reference field. Normalization does the heavy lifting, stripping the case and punctuation that make a direct match return nothing. <b>90 to 95% correct across 5,000 products.</b>'),
    fig('Fig 5', 'Order lookup, with a live fallback', 'order-lookup.png',
        'Note the branch to <b>Run Order Sync</b>. If the order is not in Airtable yet, this calls a single-page sync to pull the newest orders from Shopify and then answers, instead of telling the caller it cannot find them.'),
    note('<b>Ambiguity resolves by asking, not guessing.</b> When a model-number match returns more than one candidate, the agent requests the price or product name and narrows to one. A pronunciation dictionary in the agent fixes brand and model strings before they ever reach the workflow, because none of the matching helps if the input is already wrong.'),

    h3('Layer 3', 'Writeback and reporting'),
    p('Every completed call writes transcript, recording, caller and <b>a link to the exact product asked about</b> into Airtable. A scheduled workflow assembles overnight activity and emails it before the shop opens, because the owner was never going to open a dashboard.'),
    fig('Fig 6', 'The morning digest', 'notifier.png',
        'Scheduled trigger, pull the overnight calls, check client limits and usage, format and send. The <b>If</b> gate means a quiet night sends nothing rather than an empty report.'),
    endsec(),

    sec('03', 'Results, coded by hand'),
    lead('I went through every call in a recent sample and coded each one by arrival time, intent, outcome, and whether a lead was actually captured.'),
    stats([('89%', 'of calls arrive after hours', 1),
           ('90&ndash;95%', 'correct product from 5,000', 0),
           ('72%', 'of genuine inquiries become a lead', 0),
           ('$21&ndash;302K', 'range of pieces asked about', 0)]),
    note('<b>72% is after excluding</b> wrong numbers, a caller chasing a Macy&rsquo;s order, and 2 who were abusive. Counting those would flatter the number. The value range is what callers actually asked about: Richard Mille $302,500, Jaeger-LeCoultre tourbillon $41,000, Corum $21,000.'),
    endsec(),

])

wol += FOOT.replace('{chips}', chips([('Retell AI', 'retell.svg'), ('n8n', 'n8n.png'),
                                      ('Airtable', 'airtable.png'), ('Shopify', 'shopify.png')])) \
           .replace('{np}', np([('Flock Bio', '/work/flock-bio/'),
                                ('Healthcare.com', '/work/healthcare-com/')]))


# ================================================= FLOCK BIO
fb = HEAD.format(
    title='Flock Bio: scraping LinkedIn post engagement into a scored outbound sequence | Matviy Korsunskiy',
    desc='Apify scrapes 19 technical phrases every 3 days, an LLM filters the posts, engagers are deduplicated by intent, enriched in Clay and sequenced in HeyReach. 42.6% reply rate.',
    logo='flock-logo.png', client='Flock Bio',
    meta='High-throughput pooled DNA libraries &nbsp;&middot;&nbsp; LinkedIn outbound',
    url='https://flockbio.com',
    h1='LinkedIn outbound targeted by post engagement')

fb += LF.join([

    sec('01', 'Why title-based targeting fails here'),
    pts(['No job title reliably identifies a scientist about to build a DNA library. Filtering by title and company returns thousands of people, almost none of whom have the problem this quarter.',
         'The addressable audience is small enough that burning it with generic outreach is unrecoverable. There is no second list.',
         '<b>What someone posted about last week does separate them.</b> It is the only available signal that tracks intent rather than description.']),
    endsec(),

    sec('02', 'How it works'),
    fig('Fig 1', 'Scrape, filter, enrich', 'flockbio-scraper.png',
        'Scheduled trigger into Apify, then the LLM filter, then everyone who engaged with a surviving post is pulled out, deduplicated by intent and pushed to Clay for enrichment and scoring.'),
    p('Approved leads flow from the Google Sheet into HeyReach every 3 days. An LLM strips titles, suffixes and credentials from names first, because <b>&ldquo;Hi Dr. Sarah Chen PhD&rdquo;</b> reads as automation to the person receiving it.'),
    fig('Fig 2', '2 tracks through HeyReach', 'flockbio-heyreach.png',
        'The author of the post and the people who engaged with it get different openers. Both loop in small batches with a wait between them.'),
    fig('Fig 3', 'The error workflow', 'flockbio-error.png',
        '3 nodes, and the order of the middle 2 is the entire design. It deactivates the broken workflow <b>before</b> sending the alert email. Reverse them and a broken run keeps sending while the email sits unread.'),
    endsec(),

    sec('03', 'Results'),
    stats([('42.6%', 'message reply rate', 1),
           ('78.5%', 'connection acceptance', 0),
           ('20', 'replies from 47 messages', 0),
           ('3 days', 'between sending runs', 0)]),
    note('<b>These figures cover one month</b> of a campaign that has run well past it: 65 connections sent, 51 accepted, 47 messages, 20 replies. Replies turned into booked meetings, which is the number that actually matters to them.'),
    endsec(),

])

fb += FOOT.replace('{chips}', chips([('Apify', 'apify.png'), ('n8n', 'n8n.png'),
                                     ('Clay', 'clay.png'), ('HeyReach', 'heyreach.png')])) \
          .replace('{np}', np([('World of Luxury', '/work/world-of-luxury/'),
                               ('Healthcare.com', '/work/healthcare-com/')]))


# ================================================= HEALTHCARE.COM
hc = HEAD.format(
    title='Healthcare.com: 3 inbound voice agents built under CMS marketing rules | Matviy Korsunskiy',
    desc='Intent routing, loss-of-coverage intake with warm transfer, and a Medicare Advantage line, built where the agent may not assert eligibility, price or coverage.',
    logo='healthcare-logo.png', client='Healthcare.com',
    meta='National health insurance marketplace &nbsp;&middot;&nbsp; contract voice engineering &nbsp;&middot;&nbsp; 2026, ongoing',
    url='https://www.healthcare.com',
    h1='3 voice agents under CMS marketing rules')

hc += LF.join([

    gate('Under contract',
         'Everything I build for Healthcare.com belongs to Healthcare.com, and their operational detail sits inside a confidentiality clause. No screenshots, no flows, no prompts, no numbers. What follows is the constraint set and my own method, which is mine to show. The other 2 case studies have the screenshots and the data.'),

    sec('01', 'The constraint set'),
    lead('Everything the agent says has to survive a compliance review, so the build inverts.'),
    pts(['<b>Disclose that it is AI</b>, early enough to matter and clearly enough that a distressed caller registers it.',
         '<b>State it is not the government.</b> Nothing may imply endorsement by Medicare, CMS or any federal agency.',
         '<b>Carry the Medicare marketing disclaimer.</b> Third-party marketing of Medicare Advantage requires CMS-mandated wording about not offering every plan in the caller&rsquo;s area, plus the pointer to 1-800-MEDICARE.',
         '<b>Never assert an outcome it was not given.</b> No eligibility, no premium, no coverage decision, and no hedged version of any of them.']),
    p('In a normal voice project the hard part is making the agent sound natural across a long tail. Here the hard part is making it refuse cleanly, stay inside a defined scope, and hand off <em>before</em> it guesses. Callers also cannot classify themselves: they describe a situation, not a product, so a menu routes them wrong before the agent gets a chance.'),
    endsec(),

    sec('02', 'The decision ladder'),
    lead('My framework, not theirs, so I can show it in full.'),
    pts(['<b>Answer.</b> In scope, and the answer already exists in approved copy.',
         '<b>Answer with attached disclosure.</b> In scope, but regulation attaches specific words. The wording fires every time, not when the model judges it relevant.',
         '<b>Refuse and redirect.</b> Out of scope but adjacent. Say it cannot answer, say who can, offer the handoff.',
         '<b>Stop and transfer.</b> Anything touching eligibility, price or a coverage decision goes straight to a licensed human.']),
    note('Most teams ship an agent that treats the last rung as an error state. It is not an error, it is the product working. Designing it as a first-class path rather than a fallback is most of the job.'),
    endsec(),

    sec('03', 'Testing something that is not allowed to be wrong'),
    lead('The refusal path is the product, so it gets tested hardest.'),
    pts(['<b>Adversarial cases first.</b> &ldquo;So will my insulin be covered?&rdquo; in 6 phrasings, the polite ones and the desperate ones.',
         '<b>Every transfer is an assertion.</b> A handoff that dials into nothing is worse than no agent at all, and it only shows up if you test the receiving end rather than the intent to transfer.',
         '<b>Regression-test disclosures after any prompt change.</b> An edit that improves the greeting can stop required wording firing 3 turns later. That is a compliance event, not a bug.',
         '<b>Tune for latency.</b> A correct answer that arrives 2 seconds late loses the call anyway.']),
    endsec(),

])

hc += FOOT.replace('{chips}', chips([('Retell AI', 'retell.svg'), ('VAPI', 'vapi.png'),
                                     ('n8n', 'n8n.png'), ('Claude', 'claude.png')])) \
          .replace('{np}', np([('World of Luxury', '/work/world-of-luxury/'),
                               ('Flock Bio', '/work/flock-bio/')]))


for slug, html in (('world-of-luxury', wol), ('flock-bio', fb), ('healthcare-com', hc)):
    d = Path('work') / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / 'index.html').write_text(html, encoding='utf-8', newline='\n')
    print('work/%s/index.html  %s bytes' % (slug, format(len(html), ',')))
