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
from figs import fig, figpair, toc, sec_id, lead, layer


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
             ('results', '04', 'The results'),
             ('learned', '05', 'What it taught me')]))

hc += '\n'.join([
    glance([('Role', 'Voice AI engineer, contract'),
            ('Period', 'May 2026 &ndash; present'),
            ('Built', 'Three inbound agents'),
            ('Status', 'In production')]),
    pull('Most voice AI is a booking bot for a salon. This one sits inside health insurance, where an agent that says the wrong thing about coverage is not a bad customer experience, it is a compliance problem.'),

    sec_id('01', 'The problem', 'Callers arrive without knowing what they need', 'problem'),
    prose('Health insurance is a category where people call confused. They do not know which plan type applies to them, whether they qualify for a subsidy, or whether the thing they are worried about is even covered. A legacy phone menu asks them to self-select into a category they cannot yet identify, so they pick wrong, get routed wrong, and either hang up or waste a licensed agent&rsquo;s time.',
          'At high inbound volume that misrouting is expensive in both directions: callers who needed help do not get it, and expensive humans spend their day redirecting people.'),

    sec_id('02', 'The constraint', 'The agent is not allowed to improvise', 'constraint'),
    prose('Everything the agent says has to hold up against AI disclosure requirements and CMS marketing rules. It cannot improvise about plans, prices or eligibility, and it cannot imply a government affiliation.',
          'That inverts the usual build. In a normal voice project the hard part is making the agent sound natural and handle the long tail. Here the hard part is making it refuse cleanly, stay inside a defined scope, and hand off <em>before</em> it guesses. A model that is helpful in the general case is actively dangerous in this one.'),
    pull('The interesting work is not the conversation. It is the boundary around the conversation.'),

    sec_id('03', 'What I built', 'Three agents, one guardrail layer', 'built'),
    bul([
        '<b>A routing agent.</b> Works out what a caller actually needs from how they describe their situation, rather than asking them to pick a menu option, and sends them down the right path. Built for high inbound volume.',
        '<b>A job loss intake line.</b> For people who just lost their health insurance along with their job. It qualifies the caller and warm transfers to a licensed human rather than trying to solve it, because that is not a call an agent should be closing.',
        '<b>A Medicare Advantage agent.</b> Runs inside that funnel, where the compliance bar is higher again.',
    ]),
    flow([('Inbound call', 'intent unknown', 0),
          ('Classify', 'what does this caller actually need', 0),
          ('Guardrails', 'disclosure, scope limits, nothing improvised', 1),
          ('Route', 'coverage, Medicare, or crisis path', 0),
          ('Warm transfer', 'handed to a licensed human', 0)],
         'The guardrail step is the whole job. Everything else is plumbing.'),

    sec_id('04', 'The results', 'What I am able to share', 'results'),
    '''      <div class="gate" data-reveal>
        <div class="lbl">Confidentiality</div>
        <p>My contract with Healthcare.com is specific, and their operational detail sits inside it: call volumes, conversion and containment figures, internal product names, and the flows themselves. Publishing any of that would breach it, so this page stops at the shape of the problem and the approach. All three agents are built and in production. I am happy to talk through the reasoning on a call, within the same limits.</p>
      </div>''',

    sec_id('05', 'What it taught me', 'Compliance review is the project, not overhead', 'learned'),
    prose('I scoped all three by sitting with non-technical executives, mapped use cases with senior stakeholders, built the flows, presented them back in plain language, and coordinated across product, engineering, compliance and operations to ship. Nobody handed me a spec.',
          'The thing I would tell anyone building in a regulated category: get compliance into the design conversation before you build, not after. Every hour spent agreeing what the agent may not say saves a week of rework, and it is the only way the thing actually ships rather than sitting in review.'),

    '      <div class="secnum" data-reveal>&mdash; &nbsp;&middot;&nbsp; Stack</div>',
    chips([('Retell AI', 'retell.svg', 1), ('VAPI', 'vapi.png', 0),
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
        '<b>People mispronounce watch names.</b> Jaeger-LeCoultre, Audemars Piguet, Breguet. Speech-to-text mangles them, and a mangled string matches nothing.',
        '<b>Model numbers resist matching.</b> Digits, letters, dashes and symbols, inconsistent capitalisation, and a &ldquo;pre-owned&rdquo; marker that only some products carry.',
        '<b>Around a hundred products are near-duplicates,</b> separated by price or two characters of reference. Exact match returns nothing. Loose match returns the wrong watch, confidently.',
        '<b>Callers ask about orders too,</b> so the agent has to decide which kind of lookup it is running before it runs one.',
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
    prose('Nearly nine in ten calls land outside the hours anyone is there to answer them, and a large share are weekends.',
          '<b>72% of genuine inquiries</b> become a captured lead. That figure excludes wrong numbers, people trying to reach a different dealer, one caller chasing a Macy&rsquo;s order, and a couple who were abusive. Counting those would have flattered the number and taught me nothing.',
          'The value range is what callers actually asked about: a Richard Mille at $302,500, a Jaeger-LeCoultre tourbillon at $41,000, a Corum at $21,000, plus Breguet, Patek Philippe and an Audemars Piguet Royal Oak Grande Complication.'),

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
    chips([('Retell AI', 'retell.svg', 1), ('VAPI', 'vapi.png', 0),
           ('n8n', 'n8n.png', 0), ('Airtable', 'airtable.png', 0), ('Shopify', 'shopify.png', 0)]),
])
wol += FOOT.format(nextprev=nextprev([
    ('Case study', 'Healthcare.com', '/work/healthcare-com/'),
    ('Case study', 'Flock Bio', '/work/flock-bio/')]))


# ===================================================== FLOCK BIO
fb = HEAD.format(
    title='Flock Bio &mdash; a LinkedIn pipeline at ten times benchmark | Matviy Korsunskiy',
    desc='Outbound to a narrow technical audience where volume does not work. Apify, n8n and Clay, at a 30% reply rate.',
    railrole='Case study', logo='flock-logo.png', client='Flock Bio',
    meta='High-throughput pooled DNA libraries &nbsp;&middot;&nbsp; lead generation',
    url='https://flockbio.com', domain='flockbio.com',
    toc=toc([('problem', '01', 'The problem'),
             ('constraint', '02', 'The constraint'),
             ('built', '03', 'What I built'),
             ('results', '04', 'The results'),
             ('learned', '05', 'What it taught me')]))

fb += '\n'.join([
    glance([('Role', 'Built the system'),
            ('Channel', 'LinkedIn outbound'),
            ('Built', 'Enrichment pipeline'),
            ('Result', '30% reply rate')]),
    pull('The list was small and the wrong message would burn it. So the system spends its effort on targeting and enrichment instead of send volume.'),

    sec_id('01', 'The problem', 'A market too narrow to spray', 'problem'),
    prose('Flock Bio sells high-throughput pooled DNA libraries to a specific technical audience: people running CRISPR screens, protein and enzyme engineering, promoter MPRAs, CAR-T libraries. The buyer is usually a scientist, not a procurement function.',
          'They needed pipeline, and the default answer in outbound is volume. That answer does not work here.'),

    sec_id('02', 'The constraint', 'You only get one pass at the list', 'constraint'),
    prose('Two things break the usual playbook at the same time. The addressable list is small enough that burning it has a real cost, so there is no version of this where you send ten thousand messages and accept a low hit rate. And the buyers are technical enough that a generic message marks you instantly as someone who does not understand what they do, which is disqualifying in a field where credibility is the product.',
          'So the constraint is that every message has to be worth receiving the first time, because there is no second list.'),
    pull('One message that proves you read their work beats forty that prove you did not.'),

    sec_id('03', 'What I built', 'A pipeline that spends its budget on enrichment', 'built'),
    prose('Apify builds the raw prospect list. n8n orchestrates the whole thing and handles sequencing. Clay enriches each prospect far enough that the opening line can reference something specific and accurate about their actual research rather than their job title. Replies are tracked back so targeting sharpens across the campaign instead of repeating.',
          'The deliberate trade: fewer sends, far more spent per prospect on knowing who they are before writing to them.'),
    flow([('Apify', 'source the raw list', 0),
          ('n8n', 'orchestration and sequencing logic', 0),
          ('Clay', 'enrich until the message can say something true', 1),
          ('LinkedIn', 'sequenced outreach, deliberately low volume', 0),
          ('Reply tracking', 'outcomes feed back into targeting', 0)],
         'Enrichment is the expensive step and the one that earns the reply rate.'),

    sec_id('04', 'The results', 'An order of magnitude above the channel', 'results'),
    stats([('30%', 'reply rate, cold LinkedIn', 1, ('30', '%')),
           ('~10&times;', 'above channel benchmark', 0, None),
           ('3', 'tools, no volume play', 0, None)]),
    prose('Cold LinkedIn outreach benchmarks sit in the low single digits. A 30% reply rate on a technical B2B audience is an order of magnitude above that, and it came from targeting quality rather than send volume.'),
    pending(['LinkedIn outreach metrics screenshot goes here',
             'save it into /shots/ and I will place it']),

    sec_id('05', 'What it taught me', 'Enrichment is cheaper than a burned list', 'learned'),
    prose('The instinct in outbound is to treat send volume as the lever because it is the one that is easy to turn. On a narrow list that instinct is actively destructive: every generic message you send removes a prospect you cannot replace.',
          'Spending real money and compute per prospect felt expensive until you price the alternative, which is spending a finite list to learn nothing. That trade is the whole system, and it is the part that transfers to any market where the total number of real buyers is small.'),

    '      <div class="secnum" data-reveal>&mdash; &nbsp;&middot;&nbsp; Stack</div>',
    chips([('Apify', 'apify.png', 0), ('n8n', 'n8n.png', 0),
           ('Clay', 'clay.png', 0), ('LinkedIn', 'linkedin.png', 0)]),
])
fb += FOOT.format(nextprev=nextprev([
    ('Case study', 'Healthcare.com', '/work/healthcare-com/'),
    ('Case study', 'World of Luxury', '/work/world-of-luxury/')]))


for slug, html in (('healthcare-com', hc), ('world-of-luxury', wol), ('flock-bio', fb)):
    d = Path('work') / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / 'index.html').write_text(html, encoding='utf-8', newline='\n')
    print('work/%s/index.html  %s bytes' % (slug, format(len(html), ',')))
