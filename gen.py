#!/usr/bin/env python3
"""Generate the three case-study pages in the same system as the landing page.

Every page opens with the same summary the landing card shows (built,
tools, results) so a reader who clicked through gets the answer again
before deciding to read on. Then: the problem, what I built, the results,
what it taught me. Nothing else.

Run: python gen.py
"""
from pathlib import Path

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
    gsap.utils.toArray('section, .spec, .fig, .figpair').forEach(function (el) {
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
def spec(built, tools, results):
    """The same built / tools / results summary the landing card shows."""
    out = ['  <dl class="spec">',
           '    <div><dt>Built</dt><dd>%s</dd></div>' % built,
           '    <div><dt>Tools</dt><dd><div class="tools">%s</div></dd></div>'
           % ''.join('<span>%s</span>' % t for t in tools),
           '    <div><dt>Results</dt><dd><ul class="res">']
    out += ['      <li>%s</li>' % r for r in results]
    out += ['    </ul></dd></div>', '  </dl>']
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
    title='World of Luxury: matching 5,000 watches from a spoken sentence | Matviy Korsunskiy',
    desc='A production voice agent for a luxury watch dealer. Live Shopify catalog, fuzzy model-number matching at 90-95% across 5,000 products, 9 in 10 calls arriving after hours.',
    logo='wol-logo.png', client='World of Luxury',
    meta='Luxury watches and jewelry, Aventura FL &nbsp;&middot;&nbsp; ~$500K/yr on Shopify &nbsp;&middot;&nbsp; retained 8 months',
    url='https://worldofluxuryus.com',
    h1='Matching 5,000 watches from a spoken sentence')

wol += '\n'.join([
    spec('An inbound voice receptionist that answers every call, looks up live product and order data against Shopify, and writes a qualified lead into the CRM before it hangs up.',
         ['Retell AI', 'n8n', 'Airtable', 'Shopify'],
         ['<b>9 in 10 calls</b> arrive outside showroom hours, now captured',
          '<b>90&ndash;95%</b> correct product across 5,000 live products',
          '<b>8 months</b> live, maintained weekly']),

    sec('01', 'They had already tried a human'),
    lead('The showroom is open Monday to Friday, 10am to 5pm. Their customers are not.'),
    pts(['People shop for a <b>$40,000 watch at 11pm</b> and on Sunday afternoons. Those calls hit a voicemail box nobody would action before Monday.',
         'They hired a virtual assistant first. A VA who does not know the inventory cannot answer the only question that matters: <em>do you have this piece, and what does it cost</em>.',
         'The catalog moves daily as pieces sell and stock lands, so anything built on a static export is wrong within 24 hours.',
         '<b>Speech-to-text mangles the brand names.</b> Jaeger-LeCoultre, Audemars Piguet, Breguet. Model numbers mix digits, letters and symbols, and around 100 products are near-duplicates.']),
    endsec(),

    sec('02', '6 workflows in 3 layers'),
    lead('The agent is the visible part. Underneath it, 6 n8n workflows do the work.'),

    h3('Layer 1', 'Keeping 5,000 products current'),
    p('n8n&rsquo;s Shopify node returns 50 records per call, and looping it hard enough to finish a full pull kept tripping limits and deactivating the workflow. I replaced it with a custom HTTP request walking Shopify&rsquo;s <code>page_info</code> cursor at roughly 250 records per iteration: <b>5x the throughput</b>, stable enough to run unattended. It PATCHes into Airtable rather than creating, so a product that changed price updates in place instead of duplicating.'),
    fig('Fig 1', 'Product sync, the pagination loop', 'sync-products.png',
        '<b>Build Request</b> assembles the next cursor, the HTTP node pulls a page, results are parsed and batched, then upserted into Airtable. <b>Has More Products?</b> feeds the arrow back round until Shopify stops returning a cursor.'),
    fig('Fig 2', 'Order sync, same shape but paced', 'sync-orders.png',
        'Identical pattern with one addition: a <b>Wait</b> node between iterations. Without it the loop runs fast enough to trip Shopify&rsquo;s rate limit, which is what was silently killing the workflow before.'),

    h3('Layer 2', 'Finding the right watch mid-call'),
    p('3 lookup workflows sit behind webhooks the agent calls as tools. Each runs the same shape: extract the argument, normalize it, search Airtable, rank the candidates, format for speech.'),
    figpair('product-page-annotated.png', 'A product page showing the 3 matchable fields',
            [('Product name', 'Long and brand-heavy. This is what callers mispronounce and what speech-to-text mangles.'),
             ('Price', 'The tiebreaker. When a name hits a cluster of near-identical pieces, price separates them.'),
             ('Model number', 'Digits, letters, dots, and a <code>Preowned-</code> prefix only some products carry.')],
            'A real listing. These 3 fields are everything the agent has to work with.'),
    fig('Fig 3', 'Lookup by name and price', 'lookup-details.png',
        '<b>Extract &amp; Normalize</b> pulls the argument out of the tool call, Airtable returns candidates, then <b>Fuzzy Match &amp; Rank</b> reduces them to one.'),
    fig('Fig 4', 'Lookup by model number', 'lookup-reference.png',
        'Same shape pointed at the reference field. Normalization does the heavy lifting, stripping the case and punctuation that make a direct match return nothing. <b>90 to 95% correct across 5,000 products.</b>'),
    fig('Fig 5', 'Order lookup, with a live fallback', 'order-lookup.png',
        'Note the branch to <b>Run Order Sync</b>. If the order is not in Airtable yet, this calls a single-page sync to pull the newest orders from Shopify and then answers, rather than telling the caller it cannot find them.'),
    note('<b>It asks rather than guesses.</b> When a model-number match returns more than one candidate, the agent requests the price or product name and narrows to one. Guessing confidently on a $40,000 watch is the worst available outcome. A pronunciation dictionary fixes the input before any of the matching runs.'),

    h3('Layer 3', 'Turning calls into something the owner uses'),
    p('Every completed call writes the transcript, the recording and the caller into Airtable, <b>including a link to the exact product they asked about</b>. A scheduled notifier assembles the overnight activity and emails it before the shop opens. The owner never opens a dashboard.'),
    fig('Fig 6', 'The morning digest', 'notifier.png',
        'Scheduled trigger, pull the overnight calls, check client limits and usage, format and send. The <b>If</b> gate means a quiet night sends nothing rather than an empty report.'),
    endsec(),

    sec('03', 'Coded by hand, not pulled from a dashboard'),
    lead('I went through every call in a recent sample and coded each one by arrival time, intent, outcome, and whether a lead was actually captured.'),
    stats([('89%', 'of calls arrive after hours', 1),
           ('90&ndash;95%', 'correct product from 5,000', 0),
           ('72%', 'of genuine inquiries become a lead', 0),
           ('$21&ndash;302K', 'range of pieces asked about', 0)]),
    note('<b>72% is after excluding</b> wrong numbers, a caller chasing a Macy&rsquo;s order, and 2 who were abusive. Counting those would have flattered the number. The value range is what callers actually asked about: Richard Mille $302,500, Jaeger-LeCoultre tourbillon $41,000, Corum $21,000.'),
    endsec(),

    sec('04', 'The failures are invisible in the success rate'),
    lead('This agent was not good at the start. It got good because I listen to real calls every week and fix what broke.'),
    pts(['<b>A broken email domain.</b> The agent read the contact address as &ldquo;world of luxurious dot com&rdquo;. Every seller routed to email got an address that does not exist, and every one of those calls logged as successful.',
         '<b>Lead capture asked too late.</b> Callers answered 3 or 4 product questions, then hung up the moment the agent asked for a name.',
         '<b>No recovery from a misheard name.</b> One caller&rsquo;s name came through as &ldquo;12&rdquo;. The agent had no path back and the call timed out, losing a $21,000 inquiry at the final step.']),
    note('A voice agent is not a build, it is an operation. The version that shipped in month one and the version running now share a prompt and almost nothing else.'),
    endsec(),
])
wol += FOOT.replace('{chips}', chips([('Retell AI', 'retell.svg'), ('n8n', 'n8n.png'),
                                      ('Airtable', 'airtable.png'), ('Shopify', 'shopify.png')])) \
           .replace('{np}', np([('Flock Bio', '/work/flock-bio/'),
                                ('Healthcare.com', '/work/healthcare-com/')]))


# ================================================= FLOCK BIO
fb = HEAD.format(
    title='Flock Bio: a 42.6% reply rate on cold LinkedIn | Matviy Korsunskiy',
    desc='Outbound to a narrow technical audience, targeted by what people were talking about this week rather than by job title. Apify, Clay, n8n and HeyReach.',
    logo='flock-logo.png', client='Flock Bio',
    meta='High-throughput pooled DNA libraries &nbsp;&middot;&nbsp; LinkedIn outbound',
    url='https://flockbio.com',
    h1='Targeting the conversation, not the job title')

fb += '\n'.join([
    spec('A LinkedIn outbound pipeline that finds prospects by what they post about, then deduplicates by intent, enriches, scores and sequences them automatically.',
         ['Apify', 'n8n', 'Clay', 'HeyReach'],
         ['<b>42.6% reply rate</b> on cold LinkedIn, about 10x the channel benchmark',
          '<b>78.5%</b> connection acceptance',
          '<b>19 technical phrases</b> scraped and filtered weekly, unattended']),

    sec('01', 'The audience is too small to waste'),
    lead('No job title reliably identifies a scientist about to build a DNA library.'),
    pts(['Filtering by title and company returns thousands of people, almost none of whom have the problem this quarter.',
         'The addressable audience is small enough that burning it with generic outreach is unrecoverable. There is no second list.',
         'What someone posted about last week <b>does</b> separate them. It is the only signal available that tracks intent rather than description.']),
    endsec(),

    sec('02', 'Scrape the conversation, then work backwards'),
    lead('2 n8n workflows do the work, plus a third that exists only to catch failures.'),
    p('Apify scrapes LinkedIn every 3 days against 19 quoted phrases such as <code>"gene library"</code>, <code>"AAV cassette design"</code> and the rest, pulling the week&rsquo;s posts on those subjects. An LLM reads each one and keeps only genuine industry discussion, discarding recruiters, press releases and reposts.'),
    fig('Fig 1', 'Scrape, filter, enrich', 'flockbio-scraper.png',
        'Scheduled trigger into Apify, then the LLM filter, then everyone who engaged with a surviving post is pulled out, deduplicated by intent and pushed to Clay for enrichment and scoring.'),
    p('Approved leads flow from a Google Sheet into HeyReach every 3 days. An LLM first strips titles, suffixes and credentials from names, because <b>&ldquo;Hi Dr. Sarah Chen PhD&rdquo;</b> reads as automation to the person receiving it.'),
    fig('Fig 2', '2 tracks through HeyReach', 'flockbio-heyreach.png',
        'The person who wrote the post gets a different opener from the people who engaged with it. Both loop in small batches with a wait, because the platform limits are the real constraint on volume.'),
    fig('Fig 3', 'The error workflow', 'flockbio-error.png',
        'Three nodes, and the order of the middle 2 is the entire design. It deactivates the broken workflow <b>before</b> sending the alert email. Reverse them and a broken run keeps sending while the email sits unread.'),
    endsec(),

    sec('03', 'One month of an ongoing campaign'),
    stats([('42.6%', 'message reply rate', 1),
           ('78.5%', 'connection acceptance', 0),
           ('20', 'replies from 47 messages', 0),
           ('3 days', 'between sending runs', 0)]),
    note('<b>These figures cover one month</b> of a campaign that has run well past it: 65 connections sent, 51 accepted, 47 messages, 20 replies. Cold LinkedIn benchmarks sit in the low single digits. Replies turned into booked meetings, which is the number that actually matters to them.'),
    endsec(),

    sec('04', 'Intent beats firmographics'),
    lead('The instinct in outbound is to describe the buyer, then go and find people who match the description.'),
    p('On a narrow technical list that fails, because the description does not separate the person building a library this quarter from the ten thousand who are not. What someone posted about last week does. Targeting the conversation rather than the person is the single decision that produced the reply rate.'),
    endsec(),
])
fb += FOOT.replace('{chips}', chips([('Apify', 'apify.png'), ('n8n', 'n8n.png'),
                                     ('Clay', 'clay.png'), ('HeyReach', 'heyreach.png')])) \
          .replace('{np}', np([('World of Luxury', '/work/world-of-luxury/'),
                               ('Healthcare.com', '/work/healthcare-com/')]))


# ================================================= HEALTHCARE.COM
hc = HEAD.format(
    title='Healthcare.com: voice agents that are not allowed to improvise | Matviy Korsunskiy',
    desc='Three voice agents built for a national health insurance marketplace, where the agent is not allowed to improvise about coverage, price or eligibility.',
    logo='healthcare-logo.png', client='Healthcare.com',
    meta='National health insurance marketplace &nbsp;&middot;&nbsp; contract voice engineering &nbsp;&middot;&nbsp; 2026, ongoing',
    url='https://www.healthcare.com',
    h1='Voice agents that are not allowed to improvise')

hc += '\n'.join([
    spec('Three inbound voice agents: intent routing for high call volume, a loss-of-coverage intake line that warm transfers to a licensed human, and a Medicare Advantage agent.',
         ['Retell AI', 'VAPI', 'n8n', 'Claude'],
         ['Built to hold up against <b>CMS marketing rules</b> and AI disclosure requirements',
          'Scoped, designed and shipped across <b>product, engineering and compliance</b>',
          'Figures, flows and platform detail stay private under contract']),

    gate('Under contract',
         'Everything I build for Healthcare.com belongs to Healthcare.com, and their operational detail sits inside a confidentiality clause. No screenshots, no flows, no prompts, no numbers. What follows is the problem, the constraints, and my own method, which is mine to show. The other 2 case studies have the screenshots and the data.'),

    sec('01', 'Callers cannot classify themselves'),
    lead('Health insurance is a category where people call confused.'),
    pts(['They often cannot name the product they are calling about. They can only describe a situation: <em>I lost my job, my daughter ages off my plan in March, my doctor is not on the list any more.</em>',
         'A phone menu asks that person to self-select into a category they cannot yet identify, so they pick wrong and either hang up or waste a licensed agent&rsquo;s time.',
         '<b>The right answer is frequently a human.</b> A system optimized for containment will fight that.']),
    endsec(),

    sec('02', 'What the law requires before the agent is useful at all'),
    pts(['<b>Disclose that it is AI</b>, early enough to matter and clearly enough that a distressed caller registers it.',
         '<b>State it is not the government.</b> Nothing may imply endorsement by Medicare, CMS or any federal agency.',
         '<b>Carry the Medicare marketing disclaimer.</b> Third-party marketing of Medicare Advantage carries CMS-mandated wording about not offering every plan in the caller&rsquo;s area, plus the pointer to 1-800-MEDICARE.',
         '<b>Never assert an outcome it was not given.</b> No eligibility, no premium, no coverage decision. Not a hedged version either.']),
    p('That inverts the usual build. In a normal voice project the hard part is making the agent sound natural. Here the hard part is making it refuse cleanly, stay inside a defined scope, and hand off <em>before</em> it guesses.'),
    endsec(),

    sec('03', 'How an agent decides what it may say'),
    lead('My framework, not theirs, so I can show it in full.'),
    pts(['<b>Answer.</b> In scope, and the answer already exists in approved copy.',
         '<b>Answer with attached disclosure.</b> In scope, but regulation attaches specific words. The wording fires every time, not when the model judges it relevant.',
         '<b>Refuse and redirect.</b> Out of scope but adjacent. Say it cannot answer, say who can, offer the handoff.',
         '<b>Stop and transfer.</b> Anything touching eligibility, price or a coverage decision goes straight to a licensed human.']),
    note('Most teams ship an agent that treats the last rung as an error state. It is not an error, it is the product working. Designing it as a first-class path rather than a fallback is most of the job.'),
    endsec(),

    sec('04', 'Testing something that is not allowed to be wrong'),
    lead('The refusal path is the product, so it gets tested hardest.'),
    pts(['<b>Write the adversarial cases first.</b> &ldquo;So will my insulin be covered?&rdquo; in 6 phrasings, the polite ones and the desperate ones.',
         '<b>Treat every transfer as an assertion.</b> A handoff that dials into nothing is worse than no agent at all, and it only shows up if you test the receiving end.',
         '<b>Regression-test disclosures after any prompt change.</b> An edit that improves the greeting can stop required wording firing 3 turns later. That is a compliance event, not a bug.',
         '<b>Tune for silence.</b> A correct answer that arrives 2 seconds late loses the call anyway.']),
    endsec(),

    sec('05', 'Compliance is a design input, not a gate'),
    p('I scoped all 3 from scratch: sat with non-technical executives, mapped the use cases, designed the flows, presented them back in plain language, and coordinated across product, engineering, compliance and operations. Nobody handed me a spec.'),
    p('Every hour spent agreeing what the agent may <em>not</em> say saves a week of rework. Treating compliance as a design input at the start rather than a review at the end is the difference between an agent that reaches rollout and one that sits in review indefinitely.'),
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
