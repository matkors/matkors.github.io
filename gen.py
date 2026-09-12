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
    h1='A voice agent that checks 5,000 live products')

wol += LF.join([

    sec('01', 'Why a human VA fails at this task'),
    pts(['The showroom is open Monday to Friday, 10am to 5pm. <b>9 in 10 calls arrive outside that window</b>, including $40,000 inquiries at 11pm and on Sundays. All of them hit a voicemail box nobody dealt with before Monday.',
         'They tried a virtual assistant first. Someone who cannot see the stock cannot answer the only question that matters: <em>do you have this piece, and what does it cost</em>.',
         'Stock changes every day, so a saved copy of the product list is out of date within 24 hours. Every answer has to come from live data.']),
    endsec(),

    sec('02', 'How it works'),
    h3('Layer 1', 'Keeping the product list up to date'),
    p('n8n&rsquo;s built-in Shopify node only pulls 50 products at a time. Looping it enough times to get through all 5,000 kept hitting Shopify&rsquo;s rate limit and switching the workflow off.',
      'I replaced it with a custom request that pages through Shopify <b>250 products at a time</b>, which is 5x faster and runs without me touching it.',
      'It updates the existing record rather than adding a new one, so a price change edits the product instead of duplicating it.'),
    fig('Fig 1', 'Pulling every product out of Shopify, page by page', 'sync-products.png',
        'The arrow from <b>Has More Products?</b> back to <b>Build Request</b> is the loop.'),
    fig('Fig 2', 'The same loop for orders, slowed down so Shopify does not block it', 'sync-orders.png',
        'The same loop with one addition: a <b>Wait</b> node between rounds. Without it the loop goes fast enough to hit Shopify&rsquo;s rate limit, which is what was quietly killing the workflow before.'),

    h3('Layer 2', 'Finding the right watch while the caller waits'),
    p('The agent can call 3 lookups in the middle of a conversation.',
      'Each one does the same thing: take what the caller said, clean it up, search the product list, rank the matches, and hand back the best one in a form the agent can read out loud.'),
    figpair('product-page-annotated.png', 'A product page showing the 3 matchable fields',
            [('Product name', 'Long and brand-heavy. This is what callers mispronounce and what speech-to-text mangles.'),
             ('Price', 'The tiebreaker. When a name hits a cluster of near-identical pieces, price separates them.'),
             ('Model number', 'Digits, letters, dots, and a <code>Preowned-</code> prefix only some products carry.')],
            'A real listing. These 3 fields are everything the agent has to match against.'),
    fig('Fig 3', 'Finding a watch by name and price', 'lookup-details.png',
        '<b>Extract &amp; Normalize</b> cleans up what the caller said, Airtable returns everything that might match, then <b>Fuzzy Match &amp; Rank</b> narrows it to one.'),
    fig('Fig 4', 'Finding a watch by model number', 'lookup-reference.png',
        'The same flow pointed at the model number instead. Most of the work is stripping out the capitals and punctuation that make an exact search return nothing. <b>90 to 95% correct across 5,000 products.</b>'),
    fig('Fig 5', 'Looking up an order, with a live check if it is missing', 'order-lookup.png',
        'Note the branch to <b>Run Order Sync</b>. If the order has not been saved yet, this fetches the newest orders straight from Shopify and then answers, instead of telling the caller it cannot find them.'),
    note('<b>It asks instead of guessing.</b> If a model number matches more than one watch, the agent asks for the price and narrows it down. A pronunciation list keeps the brand names spelled correctly on the way in.'),

    h3('Layer 3', 'Turning each call into a lead the owner sees'),
    p('Every finished call saves the transcript, the recording, the caller&rsquo;s details and <b>a link to the exact product they asked about</b>.',
      'A scheduled workflow gathers the overnight calls and emails them before the shop opens, because the owner was never going to log into a dashboard.'),
    fig('Fig 6', 'The email the owner gets before opening', 'notifier.png',
        'The <b>If</b> gate is the part that matters: a quiet night sends nothing rather than an empty report.'),
    endsec(),

    sec('03', 'The results, counted by hand'),
    lead('I listened to every call in a recent sample and tagged each one: when it came in, what they wanted, how it ended, and whether a lead was actually captured.'),
    stats([('89%', 'of calls arrive after hours', 1),
           ('90&ndash;95%', 'correct product from 5,000', 0),
           ('78%', 'of genuine inquiries become a lead', 0),
           ('$21&ndash;302K', 'range of pieces asked about', 0)]),
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
    h1='Finding leads by what they post, not their job title')

fb += LF.join([

    sec('01', 'Why searching by job title does not work'),
    pts(['No job title tells you who is about to build a DNA library. Searching by title and company returns thousands of people, and almost none of them have the problem right now.',
         'The audience is small enough that burning it with generic outreach cannot be undone. There is no second list.',
         '<b>What someone posted about last week does tell you.</b> It is the only signal available that shows what they are working on rather than what they are called.']),
    endsec(),

    sec('02', 'How it works'),
    fig('Fig 1', 'Finding the posts, then the people who engaged with them', 'flockbio-scraper.png',
        'Runs on a schedule into Apify, then the LLM throws out the posts that are not real discussion. Everyone who liked or commented on what is left gets pulled out, duplicates removed, and sent to Clay to be enriched and scored.'),
    p('Approved leads move from the Google Sheet into HeyReach every 3 days.',
      'An LLM cleans up the names first, stripping titles and credentials, because <b>&ldquo;Hi Dr. Sarah Chen PhD&rdquo;</b> instantly reads as automation.'),
    fig('Fig 2', 'Two different openers, depending on who they are', 'flockbio-heyreach.png',
        'The person who wrote the post gets a different first message from the people who engaged with it. Both send in small batches with a pause in between.'),
    fig('Fig 3', 'What happens when something breaks', 'flockbio-error.png',
        '3 nodes, and the order of the middle 2 is the whole point. It switches the broken workflow off <b>before</b> sending the alert email. The other way round, a broken run keeps messaging people while the email sits unread.'),
    endsec(),

    sec('03', 'Results'),
    stats([('42.6%', 'message reply rate', 1),
           ('78.5%', 'connection acceptance', 0),
           ('20', 'replies from 47 messages', 0),
           ('3 days', 'between sending runs', 0)]),
    note('<b>One month of an ongoing campaign:</b> 65 connection requests, 51 accepted, 47 messages, 20 replies. Those replies became booked meetings, which is the number that matters to them.'),
    endsec(),

])

fb += FOOT.replace('{chips}', chips([('Apify', 'apify.png'), ('n8n', 'n8n.png'),
                                     ('Clay', 'clay.png'), ('HeyReach', 'heyreach.png')])) \
          .replace('{np}', np([('World of Luxury', '/work/world-of-luxury/'),
                               ('Healthcare.com', '/work/healthcare-com/')]))


# ================================================= HEALTHCARE.COM
hc = HEAD.format(
    title='Healthcare.com: building voice agents inside a national health insurance company | Matviy Korsunskiy',
    desc='Three inbound voice agents scoped with the leadership team of a national health insurance marketplace, in a HIPAA-regulated environment where every flow clears compliance before launch.',
    logo='healthcare-logo.png', client='Healthcare.com',
    meta='National health insurance marketplace &nbsp;&middot;&nbsp; contract voice engineering &nbsp;&middot;&nbsp; 2026, ongoing',
    url='https://www.healthcare.com',
    h1='Building voice agents inside a national health insurance company')

hc += LF.join([

    gate('Under contract',
         'Everything I build for Healthcare.com belongs to them, and their operational detail sits inside a confidentiality clause. No screenshots, no flows, no prompts, no call volumes. What follows is how the work was run, and the method I brought to it.'),

    sec('01', 'Built with the leadership team, not from a spec'),
    lead('Nobody handed me a requirements document.'),
    pts(['I scoped all 3 agents from scratch, sitting with <b>non-technical executives and the leads of the teams</b> whose numbers the agents were going to move.',
         'Mapped the use cases with those stakeholders, designed the conversation flows, then presented them back in plain language so the people signing off could actually judge them.',
         'Coordinated the build across <b>product, engineering, marketing, compliance and operations</b>. Inside a company this size, getting those 5 groups to agree is most of the work.',
         'Every flow had to clear <b>compliance review</b> before it could go near production. In a <b>HIPAA-regulated</b> business that is a gate, not a formality.']),
    endsec(),

    sec('02', 'What the agent is not allowed to say'),
    lead('Everything the agent says has to survive a compliance review.'),
    pts(['<b>Disclose that it is AI</b>, early enough to matter and clearly enough that a distressed caller registers it.',
         '<b>State it is not the government.</b> Nothing may imply endorsement by Medicare, CMS or any federal agency.',
         '<b>Read the Medicare disclaimer.</b> Anyone marketing Medicare Advantage has to say specific wording set by CMS: that not every plan in the caller&rsquo;s area is on offer, plus the pointer to 1-800-MEDICARE.',
         '<b>Never state an answer it was not given.</b> Not whether someone qualifies, not what it costs, not whether something is covered, and no softened version of any of those.']),
    p('In most voice projects the hard part is making the agent sound natural. Here it is the opposite: making it stop cleanly, stay inside what it is allowed to discuss, and hand over <em>before</em> it guesses.',
      'Callers make that harder, because they describe a situation rather than a product. <em>I lost my job, my daughter ages off my plan in March.</em> A phone menu sends them to the wrong place before the agent ever gets a chance.'),
    endsec(),

    sec('03', 'How it decides what it can say'),
    lead('My framework, not theirs, so I can show it in full.'),
    pts(['<b>Answer.</b> In scope, and the answer already exists in approved copy.',
         '<b>Answer, with the required wording attached.</b> Allowed, but the law attaches specific words to it. Those words go out every single time, not when the model decides they are relevant.',
         '<b>Refuse and point elsewhere.</b> Close to what it covers, but not allowed. It says it cannot answer, says who can, and offers to transfer.',
         '<b>Stop and transfer.</b> Anything about whether someone qualifies, what it costs, or what is covered goes straight to a licensed human.']),
    note('Most teams build the last step as a failure case. It is not a failure, it is the agent working correctly. Designing the handoff as a real path rather than a fallback is most of the job.'),
    endsec(),

    sec('04', 'How I test it'),
    lead('The refusal path is the product, so it gets tested hardest.'),
    pts(['<b>Write the hard questions first.</b> &ldquo;So will my insulin be covered?&rdquo; asked 6 different ways, the polite ones and the desperate ones.',
         '<b>Test where the transfer lands.</b> A handoff that rings into nothing is worse than no agent at all, and you only catch it by calling the other end, not by checking that the agent tried.',
         '<b>Re-test the required wording after every prompt change.</b> An edit that improves the greeting can stop the legally required line firing 3 turns later. That is a compliance problem, not a bug.',
         '<b>Watch the delay.</b> A correct answer that arrives 2 seconds late loses the call anyway.']),
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
