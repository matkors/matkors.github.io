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
from figs import fig, figpair


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
    url='https://www.healthcare.com', domain='healthcare.com')

hc += '\n'.join([
    glance([('Role', 'Voice AI engineer, contract'),
            ('Period', 'May 2026 &ndash; present'),
            ('Built', 'Three inbound agents'),
            ('Status', 'In production')]),
    pull('Most voice AI is a booking bot for a salon. This one sits inside health insurance, where an agent that says the wrong thing about coverage is not a bad customer experience, it is a compliance problem.'),

    sec('01', 'The problem', 'Callers arrive without knowing what they need'),
    prose('Health insurance is a category where people call confused. They do not know which plan type applies to them, whether they qualify for a subsidy, or whether the thing they are worried about is even covered. A legacy phone menu asks them to self-select into a category they cannot yet identify, so they pick wrong, get routed wrong, and either hang up or waste a licensed agent&rsquo;s time.',
          'At high inbound volume that misrouting is expensive in both directions: callers who needed help do not get it, and expensive humans spend their day redirecting people.'),

    sec('02', 'The constraint', 'The agent is not allowed to improvise'),
    prose('Everything the agent says has to hold up against AI disclosure requirements and CMS marketing rules. It cannot improvise about plans, prices or eligibility, and it cannot imply a government affiliation.',
          'That inverts the usual build. In a normal voice project the hard part is making the agent sound natural and handle the long tail. Here the hard part is making it refuse cleanly, stay inside a defined scope, and hand off <em>before</em> it guesses. A model that is helpful in the general case is actively dangerous in this one.'),
    pull('The interesting work is not the conversation. It is the boundary around the conversation.'),

    sec('03', 'What I built', 'Three agents, one guardrail layer'),
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

    sec('04', 'The results', 'What I am able to share'),
    '''      <div class="gate" data-reveal>
        <div class="lbl">Confidentiality</div>
        <p>My contract with Healthcare.com is specific, and their operational detail sits inside it: call volumes, conversion and containment figures, internal product names, and the flows themselves. Publishing any of that would breach it, so this page stops at the shape of the problem and the approach. All three agents are built and in production. I am happy to talk through the reasoning on a call, within the same limits.</p>
      </div>''',

    sec('05', 'What it taught me', 'Compliance review is the project, not overhead'),
    prose('I scoped all three by sitting with non-technical executives, mapped use cases with senior stakeholders, built the flows, presented them back in plain language, and coordinated across product, engineering, compliance and operations to ship. Nobody handed me a spec.',
          'The thing I would tell anyone building in a regulated category: get compliance into the design conversation before you build, not after. Every hour spent agreeing what the agent may not say saves a week of rework, and it is the only way the thing actually ships rather than sitting in review.'),

    sec('&mdash;', 'Stack', 'What it runs on'),
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
    url='https://worldofluxuryus.com', domain='worldofluxuryus.com')

wol += '\n'.join([
    glance([('Role', 'Built it and run it'),
            ('Period', '8-month retainer'),
            ('Catalogue', '~5,000 live SKUs'),
            ('Match rate', '90&ndash;95%')]),
    pull('The voice was never the hard part. The hard part was matching a misheard watch name against five thousand products that change every day, fast enough that the caller does not notice the pause.'),

    sec('01', 'The problem', 'They had already tried a human'),
    prose('The showroom is open Monday to Friday, ten to five. Their customers are not. People shop for a $40,000 watch at eleven at night and on Sunday afternoons, and every one of those calls used to land in a voicemail box nobody was going to action before Monday.',
          'They had already tried the obvious fix and hired a virtual assistant to cover the gap. It did not work well enough. A VA who does not know the inventory cannot answer the question the caller actually has, which is almost always <em>do you have this specific piece and what does it cost</em>. Taking a message is not the same as answering.',
          'For a dealer whose average inquiry is worth more than most people&rsquo;s cars, a missed or badly handled call is not an inconvenience. It is the margin on a piece walking to whichever competitor picked up.'),

    sec('02', 'The constraint', 'Five thousand products, changing daily, matched from speech'),
    prose('The catalogue is roughly 5,000 products on Shopify and it moves every day as pieces sell and new stock lands. An agent working from a static export is wrong within 24 hours, and quoting a watch that sold last week is worse than not answering at all.',
          'So the agent had to hit live inventory mid-call, and fast. A lookup that takes eight seconds has already damaged the conversation.'),
    prose('Then the matching itself, which is where the real difficulty sat:'),
    bul([
        '<b>People mispronounce watch names constantly.</b> Jaeger-LeCoultre, Audemars Piguet, Breguet. Speech-to-text mangles them, and a mangled string matches nothing.',
        '<b>Model numbers are hostile to matching.</b> They mix digits, letters, dashes and symbols, capitalisation is inconsistent, and some carry a &ldquo;pre-owned&rdquo; marker while others do not.',
        '<b>Around a hundred products are near-duplicates,</b> separated only by price or one or two characters of reference. Exact match returns nothing. Loose match returns the wrong watch, confidently.',
        '<b>Callers ask about orders too,</b> so the agent has to work out which kind of lookup it is running before it runs one.',
    ]),

    sec('03', 'What I built', 'Six workflows in three layers'),
    prose('The agent is the visible part. Underneath it are six n8n workflows doing the work, split into a data layer that keeps a mirror of Shopify current, a lookup layer the agent calls mid-conversation, and a logging layer that turns every call into something the owner can act on.'),

    '''      <div class="secnum" data-reveal>Layer 1 &nbsp;&middot;&nbsp; Keeping 5,000 products current</div>''',
    prose('The obvious approach, an n8n Shopify node in a loop, broke immediately. It returns 50 records per call, which made a full catalogue pull slow, and running the loop hard enough to finish kept tripping limits and deactivating the workflow outright.',
          'I replaced it with a custom HTTP request against the Shopify Admin API, walking Shopify&rsquo;s <code>page_info</code> cursor and pulling roughly 250 records per iteration, about five times the throughput. The loop maintains its own state, checks for a next page, batches results, and <b>PATCHes into Airtable rather than creating</b>, so a product that changed price updates in place instead of duplicating. A Wait node paces the order sync so it never trips a rate limit. Products and orders both run on a schedule, current before the evening traffic starts.'),
    flow([('Set initial state', 'cursor empty, loop open', 0),
          ('Build request', 'next page_info cursor', 0),
          ('Shopify Admin API', '~250 records per call, not 50', 1),
          ('Parse + batch', 'shape for Airtable', 0),
          ('PATCH to Airtable', 'upsert, never duplicate', 0),
          ('Has more?', 'loop back or finish', 0)],
         'The n8n Shopify node capped at 50 per call and kept deactivating the workflow. This loop is the reason the rest works.'),
    fig('Fig 1', 'Product sync &mdash; the pagination loop', 'sync-products.png',
        'The loop that keeps the mirror current. <b>Build Request</b> assembles the next cursor, the HTTP node pulls a page from Shopify, results are parsed and batched, then <b>PATCHed</b> into Airtable so changed products update in place. <b>Has More Products?</b> feeds the arrow back round to Build Request until Shopify stops returning a cursor.'),
    fig('Fig 2', 'Order sync &mdash; same shape, paced', 'sync-orders.png',
        'Orders run the identical pattern with one addition: a <b>Wait</b> node between iterations. Without it the loop finishes faster and trips Shopify&rsquo;s rate limit, which is what was silently deactivating the workflow before.'),

    '''      <div class="secnum" data-reveal>Layer 2 &nbsp;&middot;&nbsp; Finding the right watch mid-call</div>''',
    prose('Three lookup workflows sit behind webhooks the agent calls as tools. Each one runs the same shape: pull the argument out of the tool call, normalise it, search Airtable, rank the candidates, format a response the agent can read aloud.'),
    figpair('product-page-annotated.png', 'A product page showing the three matchable fields',
            [('Product name',
              'Long, brand-heavy, and the thing callers mispronounce. Speech-to-text mangles Audemars Piguet reliably.'),
             ('Price',
              'The tiebreaker. When a name matches a cluster of near-identical pieces, price is what separates them.'),
             ('Model number',
              'Digits, letters, dots and a <code>Preowned-</code> prefix that only some products carry. Exact matching on this fails.')],
            'A real listing. These three fields are everything the agent has to work with, and every one of them is hostile to exact matching.'),
    bul([
        '<b>Product by name and price.</b> Extract and normalise, search, then fuzzy match and rank to a single best candidate, returned with description, price and details like water resistance.',
        '<b>Product by model number.</b> The reference is normalised on the way into Airtable to strip the inconsistencies that make exact matching fail, then fuzzy matched against. <b>90 to 95% correct across 5,000 SKUs.</b>',
        '<b>Order by number.</b> Orders resolve on a four-digit order number or a confirmation number, ranked the same way.',
    ]),
    prose('<b>The detail I am most pleased with:</b> if an order lookup misses, the workflow does not give up and tell the caller it cannot find them. It invokes a second, single-page sync workflow to pull the newest orders straight from Shopify, then answers. Someone who ordered an hour ago still gets a real answer, without running a full catalogue pull mid-conversation.'),
    flow([('Tool call from agent', 'raw argument, often messy', 0),
          ('Extract + normalise', 'strip case, dashes, pre-owned markers', 0),
          ('Airtable search', 'candidate set', 0),
          ('Fuzzy match + rank', 'best single result', 1),
          ('Not found?', 'trigger on-call sync, then retry', 0),
          ('Format response', 'phrased for speech', 0)],
         'Ranking rather than filtering is what makes the near-duplicate cluster survivable.'),
    fig('Fig 3', 'Product lookup by name and price', 'lookup-details.png',
        'Webhook in, <b>Extract &amp; Normalize</b> pulls the argument out of the tool call, Airtable returns a candidate set, then <b>Fuzzy Match &amp; Rank</b> reduces it to one before the response is formatted for speech.'),
    fig('Fig 4', 'Product lookup by model number', 'lookup-reference.png',
        'The same shape pointed at the reference field. The normalisation step is doing the heavy lifting here, stripping the case, punctuation and <code>Preowned-</code> inconsistencies that make a direct match return nothing.'),
    fig('Fig 5', 'Order lookup, with a live fallback', 'order-lookup.png',
        'Note the branch to <b>Run Order Sync</b>. If the order is not in Airtable yet, the workflow calls a single-page sync to pull the newest orders straight from Shopify and then answers, rather than telling the caller it cannot find them.'),
    prose('<b>Disambiguation instead of guessing.</b> When a model-number match returns more than one candidate, the agent does not pick. It asks for the price or the product name and narrows to one. Guessing confidently on a $40,000 watch is the worst available outcome.',
          '<b>A pronunciation dictionary.</b> None of the matching helps if the string leaving the agent is wrong. I built a dictionary of the brand and model vocabulary and gave it to the agent, so it spells names correctly on the way into the workflow instead of forwarding whatever the transcription heard.'),

    '''      <div class="secnum" data-reveal>Layer 3 &nbsp;&middot;&nbsp; Turning calls into something the owner uses</div>''',
    prose('Every completed call fires a webhook into a CRM workflow that formats timing and duration, then writes the call, the transcript, the recording and the caller into Airtable, <b>including a link to the exact product they asked about</b>. It looks the client up, creates them if they are new, and updates their record if they are not.',
          'A scheduled notifier then assembles the overnight activity and emails it out before the shop opens, so the owner starts the day with every after-hours lead, what they wanted, and the recording to listen to. That report is what turned this from a phone system into something they renewed.'),
    flow([('Call ends', 'webhook fires', 0),
          ('Format + enrich', 'duration, timing, product link', 0),
          ('Write to CRM', 'call data, transcript, recording', 0),
          ('Match client', 'create or update', 0),
          ('Morning digest', 'emailed before the shop opens', 1)],
         'The owner never opens a dashboard. The leads arrive in his inbox with recordings attached.'),
    fig('Fig 6', 'The morning digest', 'notifier.png',
        'A scheduled trigger pulls the overnight calls, checks client limits and usage, formats the summary and sends it by email before the shop opens. The <b>If</b> gate means a quiet night sends nothing rather than an empty report.'),

    prose('<b>The agent itself</b> started on VAPI and I later migrated it to Retell. Much of the work after that was prompt and voice engineering: tuning for latency so replies land fast enough to feel like conversation, and getting the tool-calling logic right so it knows when a question is about a product, when it is about an order, and when it is neither.'),

    sec('04', 'The results', 'Measured by hand, not from a dashboard'),
    prose('I went through every call in a recent sample and coded each one by arrival time, intent, outcome and whether a lead was actually captured. Call counts on their own tell you nothing. What matters is what happened at the end.'),
    stats([('89%', 'of calls arrive after hours', 1, ('89', '%')),
           ('90&ndash;95%', 'correct product from 5,000 SKUs', 0, None),
           ('8 mo', 'retained, still running', 0, None),
           ('$21&ndash;302K', 'range of pieces asked about', 0, None)]),
    prose('<b>89% is what justifies the system.</b> Nearly nine in ten calls land outside the hours anyone is there to answer them, and a large share are weekends. <b>72% of genuine inquiries</b> become a captured lead, measured after excluding wrong numbers, people trying to reach a different dealer, one caller chasing a Macy&rsquo;s order, and a couple who were abusive. Counting those would have flattered the number and taught me nothing.',
          '<b>The value range is what callers actually asked about</b> in that window: a Richard Mille at $302,500, a Jaeger-LeCoultre tourbillon at $41,000, a Corum at $21,000, plus Breguet, Patek Philippe and an Audemars Piguet Royal Oak Grande Complication. These are not $50 support calls.'),

    sec('05', 'What it taught me', 'The failures are invisible in the success rate'),
    prose('This agent was not good at the start. It got good because I listen to real calls every week and fix what broke. Three from the last pass, none of which show up in any success metric:'),
    bul([
        '<b>A broken email domain.</b> The agent was reading the contact address out as &ldquo;world of luxurious dot com&rdquo;, and once as &ldquo;world of flux dot com&rdquo;. Every seller routed to email was handed an address that does not exist. A silent, total loss on an entire lead category, and every one of those calls logged as successful.',
        '<b>Lead capture asked too late.</b> Several callers answered three or four product questions, then hung up the moment the agent asked for a first name. The ask was arriving cold at the end instead of being earned earlier in the call.',
        '<b>No recovery from a misheard name.</b> One caller&rsquo;s name came through as &ldquo;12&rdquo;. The agent had no path back, and the call timed out losing a $21,000 inquiry at the final step.',
    ]),
    pull('A voice agent is not a build, it is an operation. The version that shipped in month one and the version running now share a prompt and almost nothing else.'),

    sec('&mdash;', 'Stack', 'What it runs on'),
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
    url='https://flockbio.com', domain='flockbio.com')

fb += '\n'.join([
    glance([('Role', 'Built the system'),
            ('Channel', 'LinkedIn outbound'),
            ('Built', 'Enrichment pipeline'),
            ('Result', '30% reply rate')]),
    pull('The list was small and the wrong message would burn it. So the system spends its effort on targeting and enrichment instead of send volume.'),

    sec('01', 'The problem', 'A market too narrow to spray'),
    prose('Flock Bio sells high-throughput pooled DNA libraries to a specific technical audience: people running CRISPR screens, protein and enzyme engineering, promoter MPRAs, CAR-T libraries. The buyer is usually a scientist, not a procurement function.',
          'They needed pipeline, and the default answer in outbound is volume. That answer does not work here.'),

    sec('02', 'The constraint', 'You only get one pass at the list'),
    prose('Two things break the usual playbook at the same time. The addressable list is small enough that burning it has a real cost, so there is no version of this where you send ten thousand messages and accept a low hit rate. And the buyers are technical enough that a generic message marks you instantly as someone who does not understand what they do, which is disqualifying in a field where credibility is the product.',
          'So the constraint is that every message has to be worth receiving the first time, because there is no second list.'),
    pull('One message that proves you read their work beats forty that prove you did not.'),

    sec('03', 'What I built', 'A pipeline that spends its budget on enrichment'),
    prose('Apify builds the raw prospect list. n8n orchestrates the whole thing and handles sequencing. Clay enriches each prospect far enough that the opening line can reference something specific and accurate about their actual research rather than their job title. Replies are tracked back so targeting sharpens across the campaign instead of repeating.',
          'The deliberate trade: fewer sends, far more spent per prospect on knowing who they are before writing to them.'),
    flow([('Apify', 'source the raw list', 0),
          ('n8n', 'orchestration and sequencing logic', 0),
          ('Clay', 'enrich until the message can say something true', 1),
          ('LinkedIn', 'sequenced outreach, deliberately low volume', 0),
          ('Reply tracking', 'outcomes feed back into targeting', 0)],
         'Enrichment is the expensive step and the one that earns the reply rate.'),

    sec('04', 'The results', 'An order of magnitude above the channel'),
    stats([('30%', 'reply rate, cold LinkedIn', 1, ('30', '%')),
           ('~10&times;', 'above channel benchmark', 0, None),
           ('3', 'tools, no volume play', 0, None)]),
    prose('Cold LinkedIn outreach benchmarks sit in the low single digits. A 30% reply rate on a technical B2B audience is an order of magnitude above that, and it came from targeting quality rather than send volume.'),
    pending(['LinkedIn outreach metrics screenshot goes here',
             'save it into /shots/ and I will place it']),

    sec('05', 'What it taught me', 'Enrichment is cheaper than a burned list'),
    prose('The instinct in outbound is to treat send volume as the lever because it is the one that is easy to turn. On a narrow list that instinct is actively destructive: every generic message you send removes a prospect you cannot replace.',
          'Spending real money and compute per prospect felt expensive until you price the alternative, which is spending a finite list to learn nothing. That trade is the whole system, and it is the part that transfers to any market where the total number of real buyers is small.'),

    sec('&mdash;', 'Stack', 'What it runs on'),
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
