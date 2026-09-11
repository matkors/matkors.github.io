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
    title='World of Luxury &mdash; an inbound agent running eight months | Matviy Korsunskiy',
    desc='A production voice receptionist for a luxury watch dealer. 89% of calls arrive after hours. How I measure whether it is working.',
    railrole='Case study', logo='wol-logo.png', client='World of Luxury',
    meta='Luxury watches and jewelry, Aventura FL &nbsp;&middot;&nbsp; ~$500K/yr on Shopify',
    url='https://worldofluxuryus.com', domain='worldofluxuryus.com')

wol += '\n'.join([
    glance([('Role', 'Built and run it'),
            ('Period', '8-month retainer'),
            ('Built', 'Inbound voice agent'),
            ('Status', 'Live, reviewed weekly')]),
    pull('Building a voice agent is the easy part. Keeping one alive on someone&rsquo;s real phone line, month after month, is the part most people never reach.'),

    sec('01', 'The problem', 'Their customers call when the showroom is shut'),
    prose('The showroom is open Monday to Friday, ten to five. Their customers are not. People shop for a $40,000 watch at eleven at night and on Sunday afternoons, and every one of those calls used to land in a voicemail box nobody was going to action before Monday.',
          'For a dealer whose average inquiry is worth more than most people&rsquo;s cars, a missed call is not an inconvenience. It is the margin on a piece walking to whichever competitor picked up.'),

    sec('02', 'The constraint', 'It has to be honest and it has to be right'),
    prose('Three things made the obvious build wrong. It cannot pretend to be human, because these are high-trust purchases and getting caught faking it costs more than the call. It cannot invent product details, because quoting the wrong reference or price on a six-figure watch is a real problem, which means every answer has to come from live inventory rather than the model. And it has to take recording consent properly, on every call, before anything else happens.',
          'So the agent is deliberately narrow: it answers from data or it does not answer, and when it does not know, it captures the lead and commits to a callback window instead of guessing.'),

    sec('03', 'What I built', 'An agent that answers from live data'),
    prose('An inbound agent, Natalie, that answers every call. It takes consent for recording, works out what the caller wants, looks up live product and order data against Shopify, answers what it can, and captures a qualified lead with a callback commitment when it cannot.',
          'It never pretends to be human. When someone asks, it says it is virtual, and the call almost always carries on.'),
    flow([('Inbound call', 'customer or prospect, usually after hours', 0),
          ('Consent + intent', 'recording consent, then what do they need', 0),
          ('Live lookup', 'product reference or order status against Shopify', 0),
          ('Resolve or capture', 'answer it, or take the lead with a callback window', 0),
          ('Weekly review', 'I listen to real calls and fix what broke', 1)],
         'The review loop is the part that matters. Without it this is a demo that degrades quietly.'),

    sec('04', 'The results', 'Coded by hand, not pulled from a dashboard'),
    prose('I went through every call in a recent sample and coded each one by arrival time, intent, outcome, and whether a lead was actually captured. Call counts on their own tell you nothing. What matters is what happened at the end.'),
    stats([('89%', 'of calls arrive after hours', 1, ('89', '%')),
           ('72%', 'of real inquiries become leads', 0, ('72', '%')),
           ('8 mo', 'retained, still running', 0, None),
           ('$21&ndash;302K', 'range of pieces asked about', 0, None)]),
    prose('<b>89% is the number that justifies the system.</b> Nearly nine in ten calls land outside the hours anyone is there to answer them, and a large share of those are weekends.',
          '<b>72% is measured against genuine inquiries only.</b> I excluded wrong numbers, people trying to reach a different dealer, one caller chasing a Macy&rsquo;s order, and a couple who were abusive. Counting those would have flattered the number and taught me nothing.',
          '<b>The value range is what callers actually asked about</b> in that window: a Richard Mille at $302,500, a Jaeger-LeCoultre tourbillon at $41,000, a Corum at $21,000, plus Breguet, Patek Philippe and an Audemars Piguet Royal Oak Grande Complication. These are not $50 support calls.'),

    sec('05', 'What it taught me', 'The failures are invisible in the success rate'),
    prose('Reading transcripts is how you find the things no dashboard surfaces. Three real ones from the last pass:'),
    bul([
        '<b>A broken email domain.</b> The agent was reading the contact address out as &ldquo;world of luxurious dot com&rdquo;, and once as &ldquo;world of flux dot com&rdquo;. Every seller routed to email was handed an address that does not exist. A silent, total loss on an entire lead category, and every one of those calls was logged as successful.',
        '<b>Lead capture asked too late.</b> Several callers answered three or four product questions, then hung up the moment the agent asked for a first name. The ask was arriving cold at the end instead of being earned earlier in the call.',
        '<b>No recovery from a misheard name.</b> One caller&rsquo;s name came through as &ldquo;12&rdquo;. The agent had no path back, and the call timed out losing a $21,000 inquiry at the final step.',
    ]),
    pull('None of those show up in a success rate. You only find them by listening to calls that technically completed.'),

    sec('&mdash;', 'Stack', 'What it runs on'),
    chips([('Retell AI', 'retell.svg', 1), ('n8n', 'n8n.png', 0), ('Shopify', 'shopify.png', 0)]),
    pending(['n8n workflow screenshot goes here',
             'save it into /shots/ and I will place it']),
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
