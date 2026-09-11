#!/usr/bin/env python3
"""Generate the three case-study pages. Run: python gen.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from build_cases import HEAD, FOOT, flow, chips, stats, pending, nextprev


def P(*t):
    return '\n'.join('      <p>%s</p>' % x for x in t)


def prose(*t):
    return '      <div class="prose" data-reveal>\n' + P(*t) + '\n      </div>'


def sec(t):
    return '      <h2 class="sec" data-reveal>%s</h2>' % t


def pull(*t):
    return '      <div class="pull" data-reveal>\n' + P(*t) + '\n      </div>'


def bul(items):
    return ('      <ul class="bul" data-reveal>\n'
            + '\n'.join('        <li>%s</li>' % i for i in items) + '\n      </ul>')


# ===================================================== HEALTHCARE.COM
hc = HEAD.format(
    title='Healthcare.com &mdash; voice agents under compliance | Matviy Korsunskiy',
    desc='Three production voice agents inside a national health insurance marketplace, built where the agent is not allowed to improvise.',
    railrole='Case study', logo='healthcare-logo.png', client='Healthcare.com',
    meta='Contract voice engineering &nbsp;&middot;&nbsp; 2026, ongoing',
    url='https://www.healthcare.com', domain='healthcare.com')

hc += '\n'.join([
    pull('Most voice AI is a booking bot for a salon. This one sits inside health insurance, where an agent that says the wrong thing about coverage is not a bad customer experience, it is a compliance problem.'),
    sec('The constraint'),
    prose('Everything the agent says has to hold up against AI disclosure requirements and CMS marketing rules. It cannot improvise about plans, prices or eligibility, and it cannot imply a government affiliation. In a normal voice project the hard part is making the agent sound natural. Here the hard part is making it refuse cleanly, stay inside a scope, and hand off before it guesses.',
          'That changes the build. The interesting work is not the conversation, it is the boundary around the conversation.'),
    sec('What I built'),
    bul([
        '<b>A routing agent.</b> Works out what a caller actually needs and sends them down the right path. Built for high inbound volume.',
        '<b>A job loss intake line.</b> For people who just lost their health insurance along with their job. It qualifies the caller and warm transfers to a licensed human rather than trying to solve it, because that is not a call an agent should be closing.',
        '<b>A Medicare Advantage agent.</b> Runs inside that funnel, where the compliance bar is higher again.',
    ]),
    sec('The shape of it'),
    flow([('Inbound call', 'intent unknown', 0),
          ('Classify', 'what does this caller actually need', 0),
          ('Guardrails', 'disclosure, scope limits, nothing improvised', 1),
          ('Route', 'coverage, Medicare, or crisis path', 0),
          ('Warm transfer', 'handed to a licensed human', 0)],
         'The guardrail step is the whole job. Everything else is plumbing.'),
    sec('How I worked'),
    prose('I scoped all three by sitting with non-technical executives, mapped the use cases with senior stakeholders, built the flows, presented them back in plain language, and coordinated across product, engineering, compliance and operations to ship. Nobody handed me a spec.',
          'Compliance reviewed and approved agent behaviour and messaging before anything went live. On a project like this that review cycle is not overhead, it is the project.'),
    sec('Stack'),
    chips([('Retell AI', 'retell.svg', 1), ('VAPI', 'vapi.png', 0),
           ('n8n', 'n8n.png', 0), ('Claude', 'claude.png', 0)]),
    '''      <div class="gate" data-reveal>
        <div class="lbl">Where this stops</div>
        <p>My contract with Healthcare.com is specific about confidentiality, and their operational detail sits inside it: call volumes, internal product names, flows, performance data. So this page describes the shape of the problem and how I approached it, and stops there deliberately. Happy to talk through the approach and the reasoning on a call, within the same limits.</p>
      </div>''',
])
hc += FOOT.format(nextprev=nextprev([
    ('Case study', 'World of Luxury', '/work/world-of-luxury/'),
    ('Case study', 'Flock Bio', '/work/flock-bio/')]))


# ===================================================== WORLD OF LUXURY
wol = HEAD.format(
    title='World of Luxury &mdash; an inbound agent running eight months | Matviy Korsunskiy',
    desc='A production voice receptionist for a luxury watch dealer. 89% of calls arrive after hours. How I measure whether it is working.',
    railrole='Case study', logo='wol-logo.png', client='World of Luxury',
    meta='Luxury watches and jewelry, Aventura FL &nbsp;&middot;&nbsp; ~$500K/yr on Shopify &nbsp;&middot;&nbsp; 8-month retainer',
    url='https://worldofluxuryus.com', domain='worldofluxuryus.com')

wol += '\n'.join([
    pull('Building a voice agent is the easy part. Keeping one alive on someone&rsquo;s real phone line, month after month, is the part most people never reach.'),
    sec('The problem'),
    prose('The showroom is open Monday to Friday, ten to five. Their customers are not. People shop for a $40,000 watch at eleven at night and on Sunday afternoons, and every one of those calls used to land in a voicemail box nobody was going to action before Monday.',
          'For a dealer whose average inquiry is worth more than most people&rsquo;s cars, a missed call is not an inconvenience. It is the margin on a piece walking to whichever competitor picked up.'),
    sec('What I built'),
    prose('An inbound agent, Natalie, that answers every call. It takes consent for recording, works out what the caller wants, looks up live product and order data against Shopify, answers what it can, and captures a qualified lead with a callback commitment when it cannot.',
          'It never pretends to be human. When someone asks, it says it is virtual, and the call usually carries on.'),
    flow([('Inbound call', 'customer or prospect, usually after hours', 0),
          ('Consent + intent', 'recording consent, then what do they need', 0),
          ('Live lookup', 'product reference or order status against Shopify', 0),
          ('Resolve or capture', 'answer it, or take the lead with a callback window', 0),
          ('Weekly review', 'I listen to real calls and fix what broke', 1)],
         'The review loop is the part that matters. Without it this is a demo that degrades quietly.'),
    sec('What the data says'),
    prose('I coded every call in a recent sample by arrival time, intent, outcome and whether a lead was actually captured. Not call counts, which tell you nothing on their own, but what happened at the end of each one.'),
    stats([('89%', 'of calls arrive after hours', 1, ('89', '%')),
           ('72%', 'of real inquiries become leads', 0, ('72', '%')),
           ('8 mo', 'retained, still running', 0, None),
           ('$21&ndash;302K', 'range of pieces asked about', 0, None)]),
    prose('The 89% is what justifies the whole system. Nearly nine in ten calls land outside the hours anyone is there to answer them, and a large share of those are weekends.',
          'The 72% is measured against genuine inquiries only. I excluded wrong numbers, people trying to reach a different dealer, one caller chasing a Macy&rsquo;s order, and a couple who were abusive. Counting those would have flattered the number and taught me nothing.',
          'The value range is what callers actually asked about in that window: a Richard Mille at $302,500, a Jaeger-LeCoultre tourbillon at $41,000, a Corum at $21,000, plus Breguet, Patek Philippe and an Audemars Piguet Royal Oak Grande Complication. These are not $50 support calls.'),
    sec('What the review loop found'),
    prose('Reading transcripts is how you find the things no dashboard surfaces. Three real ones from the last pass:'),
    bul([
        '<b>A broken email domain.</b> The agent was reading the contact address out as &ldquo;world of luxurious dot com&rdquo;, and once as &ldquo;world of flux dot com&rdquo;. Every seller routed to email was handed an address that does not exist. A silent, total loss on an entire lead category.',
        '<b>Lead capture asked too late.</b> Several callers answered three or four product questions, then hung up the moment the agent asked for a first name. The ask was arriving cold at the end instead of being earned earlier in the call.',
        '<b>No recovery from a misheard name.</b> One caller&rsquo;s name came through as &ldquo;12&rdquo;. The agent had no path back and the call timed out, losing a $21,000 inquiry at the last step.',
    ]),
    pull('None of those show up in a success rate. You only find them by listening to calls that technically completed.'),
    sec('Stack'),
    chips([('Retell AI', 'retell.svg', 1), ('n8n', 'n8n.png', 0), ('Shopify', 'shopify.png', 0)]),
    sec('The build'),
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
    pull('The list was small and the wrong message would burn it. So the system spends its effort on targeting and enrichment instead of send volume.'),
    sec('The problem'),
    prose('Flock Bio sells pooled DNA libraries to a narrow technical audience: people running CRISPR screens, protein and enzyme engineering, MPRAs, CAR-T libraries. That is not a market you can spray.',
          'The usual outbound playbook is volume plus templating, and it fails here twice over. The addressable list is small enough that burning it has a real cost, and the buyers are technical enough that a generic message marks you immediately as someone who does not understand what they do.'),
    sec('The system'),
    flow([('Apify', 'source the raw list', 0),
          ('n8n', 'orchestration and sequencing logic', 0),
          ('Clay', 'enrich until the message can say something true', 1),
          ('LinkedIn', 'sequenced outreach, deliberately low volume', 0),
          ('Reply tracking', 'outcomes feed back into targeting', 0)],
         'Enrichment is the expensive step and the one that earns the reply rate.'),
    prose('Apify builds the raw prospect list. n8n orchestrates and handles sequencing. Clay enriches each prospect far enough that the opening line can reference something specific and accurate about their actual work rather than their job title. Replies are tracked back so targeting improves across the campaign instead of repeating.',
          'The design principle: one message that proves you read their work beats forty that prove you did not.'),
    sec('The result'),
    stats([('30%', 'reply rate, cold LinkedIn', 1, ('30', '%')),
           ('~10&times;', 'above channel benchmark', 0, None),
           ('3', 'tools, no volume play', 0, None)]),
    prose('Cold LinkedIn outreach benchmarks sit in the low single digits. A 30% reply rate on a technical B2B audience is an order of magnitude above that, and it came from targeting quality rather than send volume.'),
    sec('The numbers'),
    pending(['LinkedIn outreach metrics screenshot goes here',
             'save it into /shots/ and I will place it']),
    sec('Stack'),
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

Path('shots').mkdir(exist_ok=True)
(Path('shots') / '.gitkeep').write_text('', encoding='utf-8')
print('shots/ ready for screenshots')
