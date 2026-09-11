#!/usr/bin/env python3
"""Generate the three case-study pages on one consistent spine.

Every page runs the same structure:
  at a glance -> 01 The problem -> 02 The constraint -> 03 What I built
  -> 04 The results -> 05 What it taught me -> Stack
so a reader who has seen one knows exactly where to look on the next.
Run: python gen.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from build_cases import HEAD, FOOT, flow, chips, stats, pending, nextprev
from figs import fig, figpair, toc, sec_id, lead, layer, notes, nda, ladder, reqs, seealso


def P(*t):
    return '\n'.join('      <p>%s</p>' % x for x in t)


def prose(*t):
    return '      <div class="prose" data-reveal>\n' + P(*t) + '\n      </div>'


def sec(num, label, title):
    return ('      <div data-reveal>\n'
            '        <div class="secnum">%s &nbsp;&middot;&nbsp; %s</div>\n'
            '        <h2 class="sec">%s</h2>\n'
            '      </div>' % (num, label, title))


def pull(*t):
    return '      <div class="pull" data-reveal>\n' + P(*t) + '\n      </div>'


def bul(items):
    return ('      <ul class="bul" data-reveal>\n'
            + '\n'.join('        <li>%s</li>' % i for i in items) + '\n      </ul>')


def glance(items):
    out = ['      <div class="glance" data-reveal>']
    for label, value in items:
        out.append('        <div class="gi"><span class="l">%s</span>'
                   '<span class="v">%s</span></div>' % (label, value))
    out.append('      </div>')
    return '\n'.join(out)


# ===================================================== HEALTHCARE.COM
hc = HEAD.format(
    title='Healthcare.com &mdash; voice agents under compliance | Matviy Korsunskiy',
    desc='Three production voice agents inside a national health insurance marketplace, built where the agent is not allowed to improvise.',
    railrole='Case study', logo='healthcare-logo.png', client='Healthcare.com',
    meta='Contract voice engineering &nbsp;&middot;&nbsp; 2026, ongoing',
    url='https://www.healthcare.com', domain='healthcare.com',
    toc=toc([('problem', '01', 'The problem'),
             ('constraint', '02', 'The constraint'),
             ('built', '03', 'What I built'),
             ('ladder', '04', 'The decision ladder'),
             ('testing', '05', 'How you test it'),
             ('results', '06', 'How it is measured'),
             ('learned', '07', 'What it taught me')]))

hc += '\n'.join([
    glance([('Role', 'Voice AI engineer'),
            ('Period', 'May 2026 &ndash; present'),
            ('Built', 'Three inbound agents'),
            ('Status', 'In production')]),

    pull('Most voice AI is a booking bot for a salon. This one sits inside health insurance, where an agent that says the wrong thing about coverage is not a bad customer experience, it is a compliance problem.'),

    nda('I am under contract. I cannot show you this one.',
        'No screenshots, no flows, no prompts, no numbers. Everything I build for Healthcare.com belongs to Healthcare.com, and their operational detail sits inside a confidentiality clause.',
        'What is left is the problem, the constraints, and my own method. That part is mine to show.'),

    seealso('The other two case studies have the screenshots, the workflows and the numbers.',
            [('World of Luxury', 'Six live n8n workflows, real call data', '/work/world-of-luxury/'),
             ('Flock Bio', 'Full scraping and enrichment pipeline', '/work/flock-bio/')]),

    sec_id('01', 'The problem', 'Callers arrive without knowing what they need', 'problem'),
    lead('Health insurance is a category where people call confused.'),
    prose('They often cannot name the product they are calling about. They can only describe a situation: I lost my job, my daughter ages off my plan in March, my doctor is not on the list any more.',
          'A phone menu asks that person to self-select into a category they cannot yet identify. They pick wrong, get routed wrong, and either hang up or spend a licensed agent&rsquo;s time being redirected.'),
    bul([
        '<b>The right answer is frequently a human.</b> Not every call should be contained, and a system optimized for containment will fight that.',
        '<b>Timing is loaded.</b> Many of these calls come from someone who just lost coverage. The first fifteen seconds matter more than the routing logic.',
    ]),

    sec_id('02', 'The constraint', 'The agent is not allowed to improvise', 'constraint'),
    prose('In a normal voice project the hard part is making the agent sound natural and handle the long tail. Here the hard part is making it refuse cleanly, stay inside a defined scope, and hand off <em>before</em> it guesses. A model that is helpful in the general case is actively dangerous in this one.'),

    reqs([('Disclose that it is AI',
           'Early enough to matter, and clear enough that a distressed caller registers it.'),
          ('State it is not the government',
           'Nothing may imply endorsement by Medicare, CMS or any federal agency.'),
          ('Carry the Medicare marketing disclaimer',
           'Third-party marketing of Medicare Advantage carries CMS-mandated wording about not offering every plan available in the caller&rsquo;s area, plus the pointer to 1-800-MEDICARE.'),
          ('Handle recording and consent correctly',
           'Recording notice where required, and consent rules governing who may be called. The company determines the wording; I implement it exactly.'),
          ('Never assert an outcome it was not given',
           'No eligibility, no premium, no coverage decision. Not a hedged version either. It routes to someone licensed to say it.')],
         'What the law requires before the agent is useful at all'),

    sec_id('03', 'What I built', 'Three agents, one guardrail layer', 'built'),
    bul([
        '<b>A routing agent.</b> Works out what a caller needs from how they describe their situation rather than asking them to pick a menu option. Built for high inbound volume.',
        '<b>A job loss intake line.</b> Qualifies people who just lost their insurance along with their job, then warm transfers to a licensed human. Not a call an agent should be closing.',
        '<b>A Medicare Advantage agent.</b> Same build, strictest required wording.',
    ]),
    prose('I scoped all three from scratch: sat with non-technical executives, mapped the use cases, designed the flows, presented them back in plain language, and coordinated across product, engineering, compliance and operations to get them live. Nobody handed me a spec.'),

    sec_id('04', 'The decision ladder', 'How an agent decides what it may say', 'ladder'),
    lead('My framework, not theirs, so I can show it in full.'),
    ladder([
        ('Answer',
         'In scope, and the answer already exists in approved copy.', 0),
        ('Answer with attached disclosure',
         'In scope, but regulation attaches specific words to it. The wording fires every time, not when the model judges it relevant.', 0),
        ('Refuse and redirect',
         'Out of scope but adjacent. Say it cannot answer, say who can, offer the handoff. Never improvise a partial answer to be helpful.', 0),
        ('Stop and transfer',
         'Anything touching eligibility, price or a coverage decision. Straight to a licensed human.', 1),
    ],
    'Most teams ship an agent that treats the last rung as an error state. It is not an error, it is the product working. Designing it as a first-class path rather than a fallback is most of the job.'),

    sec_id('05', 'How you test it', 'Testing something that is not allowed to be wrong', 'testing'),
    lead('The refusal path is the product, so it gets tested hardest.'),
    bul([
        '<b>Write the adversarial cases first.</b> &ldquo;So will my insulin be covered?&rdquo; in six phrasings, the polite ones and the desperate ones. If the agent breaks, it breaks there.',
        '<b>Treat every transfer as an assertion.</b> A handoff that dials into nothing is worse than no agent at all, and it only shows up if you test the receiving end.',
        '<b>Regression-test disclosures after any prompt change.</b> An edit that improves the greeting can stop required wording firing three turns later. That is a compliance event, not a bug.',
        '<b>Tune for silence.</b> A correct answer that arrives two seconds late loses the call anyway.',
    ]),

    sec_id('06', 'How it is measured', 'The numbers I watch, and cannot publish', 'results'),
    bul([
        '<b>Transfer success rate.</b> Did the caller actually reach a human. The most important number and the one most often not instrumented.',
        '<b>Disclosure fire rate.</b> Binary. Either 100% or the system is broken.',
        '<b>Time to human</b> on the paths where speed matters.',
        '<b>Containment, read carefully.</b> Useful as a cost measure, dangerous as a goal. An agent that contains a call it should have escalated scores well and is doing the opposite of its job.',
        '<b>Where it refused.</b> Refusals cluster around gaps in approved copy, which makes them the backlog of what to write next.',
    ]),
    '''      <div class="gate" data-reveal>
        <div class="lbl">What sits behind this line</div>
        <p>Call volumes, conversion and containment figures, internal product names, platform configuration, the conversation flows themselves, and the commercial terms of my engagement. On a call I can go a layer deeper on reasoning and method, and no deeper on their data.</p>
      </div>''',

    sec_id('07', 'What it taught me', 'Compliance review is the project, not overhead', 'learned'),
    lead('Get compliance into the design conversation before you build, not after.'),
    prose('Every hour spent agreeing what the agent may not say saves a week of rework. In this category compliance is not a gate at the end of the process, it is a design input at the start, and treating it that way is the difference between three agents in production and three agents in a slide deck.'),

    '      <div class="secnum" data-reveal>&mdash; &nbsp;&middot;&nbsp; Stack</div>',
    chips([('Retell AI', 'retell.svg', 0), ('VAPI', 'vapi.png', 0),
           ('n8n', 'n8n.png', 0), ('Claude', 'claude.png', 0)]),
])
hc += FOOT.format(nextprev=nextprev([
    ('Case study', 'World of Luxury', '/work/world-of-luxury/'),
    ('Case study', 'Flock Bio', '/work/flock-bio/')]))


# ===================================================== WORLD OF LUXURY
wol = HEAD.format(
    title='World of Luxury &mdash; matching 5,000 watches from a spoken sentence | Matviy Korsunskiy',
    desc='A production voice agent for a luxury watch dealer: live Shopify catalogue, fuzzy model-number matching at 90-95% on 5,000 SKUs, and 89% of calls arriving after hours.',
    railrole='Case study', logo='wol-logo.png', client='World of Luxury',
    meta='Luxury watches and jewelry, Aventura FL &nbsp;&middot;&nbsp; ~$500K/yr on Shopify',
    url='https://worldofluxuryus.com', domain='worldofluxuryus.com',
    toc=toc([('problem', '01', 'The problem'),
             ('constraint', '02', 'The constraint'),
             ('built', '03', 'What I built'),
             ('results', '04', 'The results'),
             ('learned', '05', 'What it taught me')]))

wol += '\n'.join([
    glance([('Role', 'Built it and run it'),
            ('Period', '8-month retainer'),
            ('Catalogue', '~5,000 live SKUs'),
            ('Match rate', '90&ndash;95%')]),
    pull('The voice was never the hard part. The hard part was matching a misheard watch name against five thousand products that change every day, fast enough that the caller does not notice the pause.'),

    sec_id('01', 'The problem', 'They had already tried a human', 'problem'),
    lead('The showroom is open Monday to Friday, ten to five. Their customers are not.'),
    prose('People shop for a $40,000 watch at eleven at night and on Sunday afternoons. Those calls used to hit a voicemail box nobody was going to action before Monday.',
          'They tried the obvious fix first and hired a virtual assistant. It did not work.',
          'A VA who does not know the inventory cannot answer the only question that matters: <em>do you have this piece, and what does it cost</em>. Taking a message is not answering.'),

    sec_id('02', 'The constraint', 'Five thousand products, changing daily', 'constraint'),
    lead('The agent had to hit live inventory mid-call, and fast. A lookup that takes eight seconds has already damaged the conversation.'),
    prose('The catalogue moves every day as pieces sell and new stock lands, so anything working from a static export is wrong within 24 hours.',
          'Then the matching itself, which is where the real difficulty sat:'),
    bul([
        '<b>Speech-to-text mangles the brand names.</b> Jaeger-LeCoultre, Audemars Piguet, Breguet. A mangled string matches nothing.',
        '<b>Model numbers resist matching.</b> Mixed digits, letters and symbols, inconsistent capitalisation, and a pre-owned marker only some products carry.',
        '<b>Around a hundred products are near-duplicates.</b> Exact match returns nothing; loose match returns the wrong watch, confidently.',
        '<b>Callers ask about orders too,</b> so the agent has to pick which lookup to run.',
    ]),

    sec_id('03', 'What I built', 'Six workflows in three layers', 'built'),
    lead('The agent is the visible part. Underneath it, six n8n workflows do the work.'),

    layer('Layer 1', 'Keeping 5,000 products current'),
    prose('The obvious approach broke immediately. n8n&rsquo;s Shopify node returns 50 records per call, and looping it hard enough to finish a full pull kept tripping limits and deactivating the workflow.',
          'I replaced it with a custom HTTP request walking Shopify&rsquo;s <code>page_info</code> cursor at roughly 250 records per iteration. Five times the throughput, and stable enough to run unattended.',
          'It <b>PATCHes</b> into Airtable rather than creating, so a product that changed price updates in place instead of duplicating.'),
    fig('Fig 1', 'Product sync &mdash; the pagination loop', 'sync-products.png',
        '<b>Build Request</b> assembles the next cursor, the HTTP node pulls a page, results are parsed and batched, then upserted into Airtable. <b>Has More Products?</b> feeds the arrow back round until Shopify stops returning a cursor.'),
    fig('Fig 2', 'Order sync &mdash; same shape, paced', 'sync-orders.png',
        'Identical pattern with one addition: a <b>Wait</b> node between iterations. Without it the loop runs fast enough to trip Shopify&rsquo;s rate limit, which is what was silently killing the workflow before.'),

    layer('Layer 2', 'Finding the right watch mid-call'),
    prose('Three lookup workflows sit behind webhooks the agent calls as tools. Each runs the same shape: extract the argument, normalise it, search Airtable, rank the candidates, format for speech.'),
    figpair('product-page-annotated.png', 'A product page showing the three matchable fields',
            [('Product name',
              'Long and brand-heavy. This is what callers mispronounce and what speech-to-text mangles.'),
             ('Price',
              'The tiebreaker. When a name hits a cluster of near-identical pieces, price separates them.'),
             ('Model number',
              'Digits, letters, dots, and a <code>Preowned-</code> prefix only some products carry.')],
            'A real listing. These three fields are everything the agent has to work with.'),
    fig('Fig 3', 'Lookup by name and price', 'lookup-details.png',
        '<b>Extract &amp; Normalize</b> pulls the argument out of the tool call, Airtable returns candidates, then <b>Fuzzy Match &amp; Rank</b> reduces them to one.'),
    fig('Fig 4', 'Lookup by model number', 'lookup-reference.png',
        'Same shape pointed at the reference field. Normalisation does the heavy lifting here, stripping the case and punctuation that make a direct match return nothing. <b>90 to 95% correct across 5,000 SKUs.</b>'),
    fig('Fig 5', 'Order lookup, with a live fallback', 'order-lookup.png',
        'Note the branch to <b>Run Order Sync</b>. If the order is not in Airtable yet, this calls a single-page sync to pull the newest orders from Shopify and then answers, rather than telling the caller it cannot find them.'),
    prose('<b>It asks rather than guesses.</b> When a model-number match returns more than one candidate, the agent requests the price or product name and narrows to one. Guessing confidently on a $40,000 watch is the worst available outcome.',
          '<b>A pronunciation dictionary fixes the input.</b> None of the matching helps if the string leaving the agent is already wrong, so the agent holds the brand and model vocabulary and spells names correctly on the way into the workflow.'),

    layer('Layer 3', 'Turning calls into something the owner uses'),
    prose('Every completed call writes the transcript, the recording and the caller into Airtable, <b>including a link to the exact product they asked about</b>.',
          'A scheduled notifier assembles the overnight activity and emails it before the shop opens. The owner never opens a dashboard.'),
    fig('Fig 6', 'The morning digest', 'notifier.png',
        'Scheduled trigger, pull the overnight calls, check client limits and usage, format and send. The <b>If</b> gate means a quiet night sends nothing rather than an empty report.'),
    pull('That report is what turned this from a phone system into something they renewed.'),

    sec_id('04', 'The results', 'Coded by hand, not pulled from a dashboard', 'results'),
    lead('I went through every call in a recent sample and coded each one by arrival time, intent, outcome, and whether a lead was actually captured.'),
    stats([('89%', 'of calls arrive after hours', 1, ('89', '%')),
           ('90&ndash;95%', 'correct product from 5,000 SKUs', 0, None),
           ('8 mo', 'retained, still running', 0, None),
           ('$21&ndash;302K', 'range of pieces asked about', 0, None)]),
    notes(['<b>72% of genuine inquiries</b> become a captured lead, after excluding wrong numbers, a caller chasing a Macy&rsquo;s order, and two who were abusive. Counting those would have flattered the number.',
           '<b>The value range is what callers asked about:</b> Richard Mille $302,500, Jaeger-LeCoultre tourbillon $41,000, Corum $21,000, plus Breguet, Patek Philippe and an AP Royal Oak Grande Complication.']),

    sec_id('05', 'What it taught me', 'The failures are invisible in the success rate', 'learned'),
    lead('This agent was not good at the start. It got good because I listen to real calls every week and fix what broke.'),
    prose('Three from the last pass, none of which show up in any metric:'),
    bul([
        '<b>A broken email domain.</b> The agent was reading the contact address out as &ldquo;world of luxurious dot com&rdquo;. Every seller routed to email got an address that does not exist, and every one of those calls logged as successful.',
        '<b>Lead capture asked too late.</b> Callers answered three or four product questions, then hung up the moment the agent asked for a name. The ask arrived cold at the end instead of being earned earlier.',
        '<b>No recovery from a misheard name.</b> One caller&rsquo;s name came through as &ldquo;12&rdquo;. The agent had no path back and the call timed out, losing a $21,000 inquiry at the final step.',
    ]),
    pull('A voice agent is not a build, it is an operation. The version that shipped in month one and the version running now share a prompt and almost nothing else.'),

    '      <div class="secnum" data-reveal>&mdash; &nbsp;&middot;&nbsp; Stack</div>',
    chips([('Retell AI', 'retell.svg', 0), ('VAPI', 'vapi.png', 0),
           ('n8n', 'n8n.png', 0), ('Airtable', 'airtable.png', 0), ('Shopify', 'shopify.png', 0)]),
])
wol += FOOT.format(nextprev=nextprev([
    ('Case study', 'Flock Bio', '/work/flock-bio/'),
    ('Case study', 'Healthcare.com', '/work/healthcare-com/')]))


# ===================================================== FLOCK BIO
fb = HEAD.format(
    title='Flock Bio &mdash; a 42% reply rate on cold LinkedIn | Matviy Korsunskiy',
    desc='Outbound to a narrow technical audience, targeted by what they were talking about this week rather than by job title. Apify, Clay, n8n and HeyReach.',
    railrole='Case study', logo='flock-logo.png', client='Flock Bio',
    meta='High-throughput pooled DNA libraries &nbsp;&middot;&nbsp; LinkedIn outbound',
    url='https://flockbio.com', domain='flockbio.com',
    toc=toc([('problem', '01', 'The problem'),
             ('constraint', '02', 'The constraint'),
             ('built', '03', 'What I built'),
             ('results', '04', 'The results'),
             ('learned', '05', 'What it taught me')]))

fb += '\n'.join([
    glance([('Role', 'Built the system'),
            ('Channel', 'LinkedIn, via HeyReach'),
            ('Cadence', 'Runs every 3 days'),
            ('Reply rate', '42.6%')]),
    pull('They came to us with a list of keywords. That was the entire brief, and it turned out to be the right one.'),

    sec_id('01', 'The problem', 'You cannot find these buyers by job title', 'problem'),
    lead('There is no job title that reliably identifies a scientist about to build a DNA library.'),
    prose('Filtering LinkedIn by &ldquo;Scientist&rdquo; at biotech companies returns tens of thousands of people, almost none of whom are building one this quarter.',
          'What Flock Bio had instead was a list of the phrases their buyers actually use. That turned out to be a better signal than any firmographic filter.'),

    sec_id('02', 'The constraint', 'One pass at a small list', 'constraint'),
    lead('The addressable audience is small enough that burning it has a real cost. There is no version of this where you send ten thousand messages and accept a low hit rate.'),
    bul([
        '<b>The buyers are technical.</b> A generic message marks you as someone who does not understand the work, which is disqualifying in a field where credibility is the product.',
        '<b>LinkedIn punishes volume.</b> Connection limits and spam signals cap what you can send anyway.',
    ]),

    sec_id('03', 'What I built', 'Target the conversation, not the person', 'built'),
    lead('Rather than search for people who look right, the system finds posts about the right subject each week and harvests everyone who engaged with them.'),
    prose('Someone who comments on a post about directed evolution has self-selected far more precisely than any title filter can manage. Two n8n workflows do the work, plus a third that exists only to fail safely.'),

    layer('Workflow 1', 'Sourcing and qualification'),
    prose('An Apify scraper runs every three days against 19 quoted phrases &mdash; <code>"gene library"</code>, <code>"codon optimization"</code>, <code>"directed evolution"</code>, <code>"AAV cassette design"</code> and the rest &mdash; pulling the week&rsquo;s posts <b>along with their comments and reactions</b>.'),
    bul([
        '<b>Mechanical filter.</b> Keep posts by people, drop company pages.',
        '<b>Semantic filter.</b> An LLM judges whether each post is genuine industry discussion, rejecting personal stories and webinar pitches.',
        '<b>Re-join.</b> The model judges <em>posts</em>, but the leads are the <em>engagers</em>. A code step pulls back every comment and reaction attached to an approved post.',
        '<b>Dedupe by intent.</b> Post 3, comment 2, reaction 1, keyed by person and post. A commenter is warmer than a reactor, so only their highest-intent action survives.',
    ]),
    fig('Fig 1', 'Sourcing and qualification', 'flockbio-scraper.png',
        'Scrape, filter mechanically, then semantically, then re-attach the engagers and deduplicate them before the batch pushes into Clay.'),
    prose('Everything lands in Clay, where waterfall enrichment fills in company, size and position, and an LLM scores lead quality.'),
    pull('The scoring prompt was not written in a vacuum. We sent Flock Bio sample lists, they marked each lead good or not, and the criteria were rewritten against their answers until it matched what they actually wanted.'),

    layer('Workflow 2', 'Personalised outreach'),
    prose('Approved leads flow from a Google Sheet into HeyReach every three days. An LLM first strips titles, suffixes, emojis and pipes down to a clean first and last name, because &ldquo;Dr. WALLIS MARGRAFF, Ph.D.&rdquo; is not how you open a message.'),
    fig('Fig 2', 'Two tracks through HeyReach', 'flockbio-heyreach.png',
        'The split at <b>Engagement or Post Route</b> is where the personalisation lives. Post authors take the upper path, engagers the lower one. Both loop in small batches with a wait, then stamp the sheet.'),
    bul([
        '<b>Post authors</b> get a message referencing their own post.',
        '<b>Engagers</b> get one referencing the post they engaged with, which needs the original author&rsquo;s name in possessive form. A second LLM call formats it, so the opener reads <em>&ldquo;I saw you engaged with Jessica&rsquo;s post&rdquo;</em> rather than something assembled by string concatenation.',
    ]),
    prose('The sheet is then stamped with the date, the workflow ID and the execution ID, so nobody is contacted twice and every send traces back to the run that made it.'),

    layer('Workflow 3', 'Failing safely'),
    prose('When anything throws, the error workflow <b>deactivates the workflow first</b>, then emails.',
          'On a finite list that ordering is the point. A bug that keeps running burns prospects you cannot get back, so the system stops itself before anyone reads the alert.'),
    fig('Fig 3', 'The error workflow', 'flockbio-error.png',
        'Three nodes, and the order of the middle two is the entire design. Reverse them and a broken run keeps sending while the email sits unread.'),

    sec_id('04', 'The results', 'One month of the campaign, measured in HeyReach', 'results'),
    stats([('42.6%', 'message reply rate', 1, ('42', '.6%')),
           ('78.5%', 'connection acceptance', 0, ('78', '.5%')),
           ('20', 'replies from 47 messages', 0, ('20', '')),
           ('3 days', 'between sending runs', 0, None)]),
    notes(['<b>Figures are one month of an ongoing campaign:</b> 65 connections sent, 51 accepted, 47 messages, 20 replies. The system has run well past that window.',
           '<b>Cold LinkedIn benchmarks sit in the low single digits.</b> Replies turned into booked meetings, which is the number that actually matters to them.']),

    sec_id('05', 'What it taught me', 'Intent beats firmographics', 'learned'),
    lead('The instinct in outbound is to describe the buyer and go find people who match the description.'),
    prose('On a narrow technical list that fails, because the description does not separate the person building a library this quarter from the ten thousand who are not.',
          'What someone posted about last week does separate them. Targeting the conversation rather than the person is the single decision that produced the reply rate.'),

    '      <div class="secnum" data-reveal>&mdash; &nbsp;&middot;&nbsp; Stack</div>',
    chips([('Apify', 'apify.png', 0), ('n8n', 'n8n.png', 0),
           ('Clay', 'clay.png', 0), ('HeyReach', 'heyreach.png', 0)]),
])
fb += FOOT.format(nextprev=nextprev([
    ('Case study', 'World of Luxury', '/work/world-of-luxury/'),
    ('Case study', 'Healthcare.com', '/work/healthcare-com/')]))


for slug, html in (('healthcare-com', hc), ('world-of-luxury', wol), ('flock-bio', fb)):
    d = Path('work') / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / 'index.html').write_text(html, encoding='utf-8', newline='\n')
    print('work/%s/index.html  %s bytes' % (slug, format(len(html), ',')))
