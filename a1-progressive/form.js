/* A1 Progressive Construction: questions for their booking page setup (Oct 20, 2026).
   Prices are North Jersey typical prices from our research (Bergen, Passaic, Essex, 2025-2026), shown so the owner
   only changes what's off. mode: fixed = book online at that price, range = show a range then visit, estimate = free estimate. */
(function () {
  'use strict';
  function has(a, id, v) { return (a[id] || []).indexOf(v) > -1; }
  function is(a, id, v) { return a[id] === v; }
  var showPrices = function (a) { return a.price_style !== 'none'; };

  // ---------- every price line the widget can use ----------
  var C = {
    // Roofing: repairs
    leak_small: { label: 'One leak or a few shingles', unit: 'pipe boot, small spot', low: 350, high: 800 },
    leak_mid: { label: 'Leak at a chimney, wall, skylight or valley', low: 800, high: 2000 },
    leak_big: { label: 'Several leaks, a sagging spot or soft wood', low: 2300, high: 5500, mode: 'estimate' },
    shingle_few: { label: 'Missing shingles, one spot (wind)', low: 300, high: 650 },
    shingle_more: { label: 'Missing shingles, several spots', low: 650, high: 1400 },
    shingle_section: { label: 'Whole section torn off', low: 1400, high: 3500 },
    flash_chim_reseal: { label: 'Chimney flashing, reseal', low: 350, high: 800 },
    flash_chim_full: { label: 'Chimney flashing, all new', low: 900, high: 2000 },
    flash_wall: { label: 'Flashing along a wall or dormer', low: 500, high: 1200 },
    flash_sky: { label: 'Flashing around a skylight', low: 450, high: 1100 },
    tarp_day: { label: 'Emergency tarp, business hours', low: 300, high: 750 },
    tarp_night: { label: 'Emergency tarp, nights and weekends', low: 500, high: 1200 },
    insp_quote: { label: 'Roof inspection for a quote', low: 0, high: 0, mode: 'estimate', note: 'Most North Jersey roofers do this for free.' },
    insp_report: { label: 'Roof inspection with written photo report', unit: 'home sale, insurance', low: 249, high: 249, mode: 'fixed', note: 'Typical: $175 to $400.' },
    // Roofing: replacement
    rr_small: { label: 'New roof: small ranch, Cape or bungalow', unit: 'architectural shingle, tear-off', low: 9000, high: 15000 },
    rr_colonial: { label: 'New roof: 2-story colonial or split-level', unit: 'architectural shingle, tear-off', low: 12000, high: 19000 },
    rr_large: { label: 'New roof: large colonial, 4+ bedrooms', unit: 'architectural shingle, tear-off', low: 19000, high: 32000 },
    rr_layer: { label: 'Extra: second layer of shingles to remove', low: 1000, high: 3000 },
    rr_sheet: { label: 'Extra: rotted plywood', unit: 'per sheet', low: 95, high: 95, mode: 'fixed' },
    // Roofing: other
    flat_repair: { label: 'Flat roof: fix a leak or seam', low: 450, high: 1100 },
    flat_small: { label: 'Flat roof: replace a porch or dormer', unit: 'about 100 to 250 sq ft', low: 2200, high: 4500 },
    flat_mid: { label: 'Flat roof: replace a garage or addition', unit: 'about 250 to 600 sq ft', low: 3500, high: 7500 },
    flat_big: { label: 'Flat roof: replace a whole main roof', unit: 'about 600 to 1,200 sq ft', low: 7000, high: 14000 },
    sky_replace: { label: 'Replace a skylight', unit: 'same size opening', low: 1600, high: 3200 },
    sky_reroof: { label: 'Replace a skylight during a new roof', unit: 'each', low: 900, high: 2000 },
    ice_one: { label: 'Ice dam steaming, one area', unit: '2-hour minimum', low: 800, high: 1300 },
    ice_most: { label: 'Ice dam steaming, front or back', low: 1200, high: 2000 },
    ice_all: { label: 'Ice dam steaming, all sides', low: 1800, high: 3000 },

    // Chimney
    sw_fire: { label: 'Chimney sweep, wood fireplace', unit: 'one flue, with Level 1 check', low: 249, high: 249, mode: 'fixed', note: 'North Jersey runs $189 to $339. Fall specials go as low as $149.' },
    sw_stove: { label: 'Wood stove or insert cleaning', low: 299, high: 299, mode: 'fixed' },
    sw_furnace: { label: 'Oil or gas furnace flue only', low: 199, high: 199, mode: 'fixed' },
    sw_gas: { label: 'Gas fireplace or gas logs service', low: 179, high: 179, mode: 'fixed' },
    sw_extra: { label: 'Each extra flue, same visit', low: 125, high: 125, mode: 'fixed' },
    cr_heavy: { label: 'Heavy creosote, chemical treatment', unit: 'added to a sweep', low: 150, high: 300 },
    cr_glazed: { label: 'Glazed creosote removal', unit: 'per flue, may take 2 visits', low: 450, high: 950 },
    in_l1: { label: 'Level 1 inspection alone', unit: 'credited toward repairs', low: 149, high: 149, mode: 'fixed' },
    in_l2: { label: 'Level 2 camera inspection', unit: 'written report, home sales', low: 349, high: 349, mode: 'fixed', note: 'Recommended, not required, for NJ home sales.' },
    in_combo: { label: 'Sweep plus Level 2 camera inspection', low: 449, high: 449, mode: 'fixed' },
    in_leak: { label: 'Chimney leak check', unit: 'credited toward the repair', low: 199, high: 199, mode: 'fixed' },
    cap_ss: { label: 'Chimney cap, one flue, stainless', low: 299, high: 449 },
    cap_cu: { label: 'Chimney cap, one flue, copper', low: 499, high: 799 },
    cap_multi: { label: 'Chimney cap, 2+ flues or full top', low: 549, high: 1100 },
    crown_seal: { label: 'Crown: seal hairline cracks', low: 299, high: 599 },
    crown_new: { label: 'Crown: rebuild', low: 1200, high: 2500 },
    cf_reseal: { label: 'Chimney flashing, reseal', low: 300, high: 650 },
    cf_full: { label: 'Chimney flashing, new step and counter', low: 950, high: 1900 },
    cp_spots: { label: 'Chimney repointing, a few spots', low: 400, high: 900 },
    cp_most: { label: 'Chimney repointing, most joints above the roof', low: 1200, high: 2800 },
    cp_rebuild: { label: 'Rebuild above the roofline', low: 3500, high: 7500, mode: 'estimate' },
    ln_gas: { label: 'Stainless liner, gas furnace or water heater', low: 1500, high: 2800 },
    ln_oil: { label: 'Stainless liner, oil furnace', low: 1900, high: 3500 },
    ln_stove: { label: 'Stainless liner, wood stove or insert', low: 2800, high: 4800 },
    ln_fire: { label: 'Stainless liner, wood fireplace', low: 3500, high: 6000 },
    wp: { label: 'Chimney waterproofing', low: 399, high: 699 },
    dm_fix: { label: 'Fix or replace a stuck damper', low: 199, high: 449 },
    dm_top: { label: 'Top-sealing damper', low: 549, high: 899 },
    chase: { label: 'Metal chimney chase cover', unit: 'stainless, made to fit', low: 499, high: 899 },

    // Masonry
    br_few: { label: 'Brick repair, a few bricks', low: 450, high: 900 },
    br_yard: { label: 'Brick repair, about a square yard', low: 700, high: 1500 },
    br_big: { label: 'Brick repair, several areas', unit: '10 to 40 sq ft', low: 1500, high: 3500 },
    rp_patch: { label: 'Repointing, small patch', unit: 'under 10 sq ft', low: 350, high: 700 },
    rp_steps: { label: 'Repointing, front steps', low: 900, high: 2000 },
    rp_part: { label: 'Repointing, part of a wall', unit: '50 to 100 sq ft', low: 900, high: 2000 },
    rp_wall: { label: 'Repointing, one full wall, 1 story', low: 3000, high: 6500 },
    st_repair: { label: 'Step repair', unit: 'loose treads, cracks', low: 800, high: 2500 },
    st_brick_s: { label: 'New brick steps, 1 to 3 steps', low: 4000, high: 7500 },
    st_brick_l: { label: 'New brick steps, 4 to 6 steps', low: 6500, high: 12000 },
    st_conc_s: { label: 'New concrete steps, 1 to 3 steps', low: 2800, high: 5500 },
    st_conc_l: { label: 'New concrete steps, 4 to 6 steps', low: 4500, high: 8500 },
    st_stone_s: { label: 'New bluestone steps, 1 to 3 steps', low: 5500, high: 10000 },
    st_stone_l: { label: 'New bluestone steps, 4 to 6 steps', low: 8500, high: 16000 },
    st_rail: { label: 'New iron railing', low: 1500, high: 3000 },
    wk_repair: { label: 'Walkway repair', unit: 'reset sunken pavers, fix a crack', low: 600, high: 1800 },
    wk_pav_s: { label: 'Paver walkway, under 25 ft', low: 2500, high: 4500 },
    wk_pav_m: { label: 'Paver walkway, 25 to 50 ft', low: 4000, high: 7500 },
    wk_pav_l: { label: 'Paver walkway, over 50 ft', low: 7000, high: 12000 },
    wk_con_s: { label: 'Concrete walkway, under 25 ft', low: 1800, high: 3200 },
    wk_con_m: { label: 'Concrete walkway, 25 to 50 ft', low: 3000, high: 5500 },
    wk_con_l: { label: 'Concrete walkway, over 50 ft', low: 5000, high: 9000 },
    wk_blu_s: { label: 'Bluestone or brick walkway, under 25 ft', low: 3500, high: 6000 },
    wk_blu_m: { label: 'Bluestone or brick walkway, 25 to 50 ft', low: 5500, high: 10000 },
    wk_blu_l: { label: 'Bluestone or brick walkway, over 50 ft', low: 9500, high: 16000 },
    pt_pav_s: { label: 'Paver patio, small', unit: 'about 10 x 15 ft', low: 4000, high: 7000 },
    pt_pav_m: { label: 'Paver patio, medium', unit: 'about 15 x 20 ft', low: 7000, high: 12000 },
    pt_pav_l: { label: 'Paver patio, large', unit: 'about 20 x 25 ft', low: 11000, high: 19000 },
    pt_blu_s: { label: 'Bluestone patio, small', unit: 'about 10 x 15 ft', low: 5500, high: 9000 },
    pt_blu_m: { label: 'Bluestone patio, medium', unit: 'about 15 x 20 ft', low: 9500, high: 15500 },
    pt_blu_l: { label: 'Bluestone patio, large', unit: 'about 20 x 25 ft', low: 15000, high: 25000 },
    pt_con_s: { label: 'Concrete patio, small', unit: 'about 10 x 15 ft', low: 2000, high: 3800 },
    pt_con_m: { label: 'Concrete patio, medium', unit: 'about 15 x 20 ft', low: 3500, high: 6500 },
    pt_con_l: { label: 'Concrete patio, large', unit: 'about 20 x 25 ft', low: 5500, high: 10000 },
    rw_low_s: { label: 'Garden wall under 2 ft, up to 20 ft long', low: 2000, high: 3500 },
    rw_low_m: { label: 'Garden wall under 2 ft, 20 to 40 ft long', low: 3000, high: 6000 },
    rw_mid_s: { label: 'Retaining wall 2 to 4 ft, up to 20 ft long', low: 3000, high: 6000 },
    rw_mid_m: { label: 'Retaining wall 2 to 4 ft, 20 to 40 ft long', low: 5500, high: 11000 },
    rw_mid_l: { label: 'Retaining wall 2 to 4 ft, 40 to 60 ft long', low: 10000, high: 18000 },
    pg_spot: { label: 'Foundation parging, one spot', low: 450, high: 900 },
    pg_side: { label: 'Foundation parging, one side', low: 900, high: 2000 },
    pg_all: { label: 'Foundation parging, all around', low: 2500, high: 5000 },

    // Siding
    vs_1s: { label: 'Vinyl siding, 1-story under 1,500 sq ft', unit: 'tear-off, house wrap, trim', low: 9500, high: 14500 },
    vs_1l: { label: 'Vinyl siding, 1-story 1,500 to 2,500 sq ft', low: 13000, high: 20000 },
    vs_2s: { label: 'Vinyl siding, small colonial or Cape', unit: '2 stories, under 1,500 sq ft', low: 13000, high: 20000 },
    vs_2m: { label: 'Vinyl siding, typical colonial', unit: '2 stories, 1,500 to 2,500 sq ft', low: 17000, high: 27000 },
    vs_2l: { label: 'Vinyl siding, large 2-story', unit: 'over 2,500 sq ft', low: 25000, high: 38000 },
    hs_1s: { label: 'James Hardie, 1-story under 1,500 sq ft', low: 15000, high: 23000 },
    hs_1l: { label: 'James Hardie, 1-story 1,500 to 2,500 sq ft', low: 21000, high: 32000 },
    hs_2s: { label: 'James Hardie, 2-story under 1,500 sq ft', low: 20000, high: 30000 },
    hs_2m: { label: 'James Hardie, typical colonial', low: 27000, high: 40000 },
    sr_few: { label: 'Siding repair, 1 to 3 panels', low: 350, high: 700 },
    sr_section: { label: 'Siding repair, one section', unit: 'storm damage, up to 100 sq ft', low: 800, high: 2000 },
    sr_side: { label: 'Siding repair, a whole side', low: 2500, high: 5500 },
    sf_repair: { label: 'Soffit and fascia, repair one section', low: 600, high: 1400 },
    sf_all1: { label: 'Soffit and fascia, all new, 1-story', low: 2500, high: 5000 },
    sf_all2: { label: 'Soffit and fascia, all new, 2-story', low: 3500, high: 7000 },
    tc_s: { label: 'Aluminum trim capping, 1 to 5 windows', low: 900, high: 1800 },
    tc_m: { label: 'Aluminum trim capping, 6 to 12 windows', low: 1800, high: 3800 },
    tc_l: { label: 'Aluminum trim capping, 13 to 25 windows', low: 3500, high: 7000 },

    // Windows
    wn_one: { label: 'Vinyl window, 1 to 3 windows', unit: 'per window, double-hung, installed', low: 750, high: 1100 },
    wn_some: { label: 'Vinyl window, 4 to 9 windows', unit: 'per window', low: 650, high: 900 },
    wn_many: { label: 'Vinyl window, 10 or more', unit: 'per window', low: 550, high: 800, note: 'A 12 to 16 window colonial comes to about $9,000 to $14,000.' },
    wn_premium: { label: 'Premium brand window', unit: 'per window, Andersen, Pella, Harvey type', low: 950, high: 1250 },
    wn_casement: { label: 'Extra for casement or awning style', unit: 'per window', low: 150, high: 250 },
    wn_bay: { label: 'Bay window', low: 3200, high: 5500 },
    wn_bow: { label: 'Bow window', low: 4500, high: 8000 },
    wn_picture: { label: 'Picture window', low: 900, high: 2200 },
    wn_base: { label: 'Basement window, same size', low: 450, high: 750 },
    wn_egress: { label: 'Egress window', unit: 'cut, well, permit', low: 4000, high: 6500, mode: 'estimate' },
    wn_glass: { label: 'Foggy or broken glass replaced', unit: 'per window', low: 200, high: 450 },
    // Gutters
    gc_1: { label: 'Gutter cleaning, 1-story home', unit: 'with downspout flush', low: 199, high: 199, mode: 'fixed', note: 'North Jersey runs $175 to $250.' },
    gc_2: { label: 'Gutter cleaning, 2-story home', low: 299, high: 299, mode: 'fixed', note: 'North Jersey runs $250 to $375.' },
    gc_3: { label: 'Gutter cleaning, 3-story home', low: 449, high: 449, mode: 'fixed' },
    gs_1: { label: 'New seamless gutters, 1-story home', unit: '5-inch aluminum with downspouts', low: 1700, high: 2800 },
    gs_2: { label: 'New seamless gutters, 2-story home', unit: '5-inch aluminum with downspouts', low: 2000, high: 3200 },
    gs_6: { label: 'Extra for 6-inch gutters', unit: 'per foot', low: 2, high: 3 },
    gs_cu: { label: 'Copper gutters', unit: 'per foot', low: 30, high: 45 },
    gr_fix: { label: 'Gutter repair visit', unit: 'reseal, re-hang, re-pitch', low: 175, high: 400 },
    gr_section: { label: 'Replace a gutter section', low: 150, high: 400 },
    gr_down: { label: 'Downspout replaced or added', unit: 'each', low: 150, high: 350 },
    gg_guard: { label: 'Gutter guards, micro-mesh', unit: 'per foot, installed', low: 10, high: 16, note: 'About half of what LeafFilter charges ($30 to $42 a foot).' },
    yk_rubber: { label: 'Yankee gutter relining, rubber', unit: 'per foot', low: 20, high: 35, note: 'No one in North Jersey publishes this price. A whole house is about $3,000 to $5,000.' },
    yk_copper: { label: 'Yankee gutter relining, copper', unit: 'per foot', low: 60, high: 100 },
    yk_wood: { label: 'Yankee gutter wood rebuild', unit: 'per foot', low: 150, high: 200, mode: 'estimate' },
    yk_convert: { label: 'Yankee gutters converted to regular gutters', low: 2500, high: 6000 }
  };

  function opt(v, label, hint) { return { v: v, label: label, hint: hint }; }
  function prices(id, title, items, sub) {
    return { id: id, type: 'prices', title: title, short: title, sub: sub || 'Change anything that’s off. <b>Fixed price</b> books online at that price. <b>Price range</b> shows the range, then you confirm on site. <b>Free estimate</b> shows no price.',
      items: typeof items === 'function' ? items : function () { return items; } };
  }
  function jobsOf(trade, job) { return function (a) { return has(a, 'trades', trade) && has(a, 'jobs_' + trade, job) && showPrices(a); }; }

  window.FORM = {
    form: 'a1-progressive',
    backup: 'https://matkors.app.n8n.cloud/webhook/dialbridge-setup-form/submit-q7m2',
    business: 'A1 Progressive Construction',
    logo: 'logo.png',
    contact: { name: 'c_name', phone: 'c_phone', email: 'c_email', business: 'biz_name', screen: 'contact' },
    catalog: C,
    parts: [
      { title: 'About your business', screens: [
        { id: 'intro', type: 'intro', title: 'Let’s set up your booking page',
          text: '<p>Your page will let homeowners pick a job, see a price, and book a time with you, day or night.</p>' +
            '<p>This takes about 10 minutes. For every job you do, we filled in typical North Jersey prices, so you only change what’s off.</p>' +
            '<p>Your answers save as you go. You can stop and come back on this device.</p>',
          button: 'Start', fine: 'Prepared for A1 Progressive Construction by Dialbridge.' },
        { id: 'contact', type: 'fields', title: 'Who should we talk to?', short: 'Contact',
          fields: [
            { id: 'c_name', label: 'Your name', auto: 'name', placeholder: 'First and last name' },
            { id: 'c_phone', label: 'Your cell phone', type: 'tel', placeholder: '(201) 555-0123' },
            { id: 'c_email', label: 'Your email', type: 'email', placeholder: 'you@example.com' }
          ] },
        { id: 'biz', type: 'fields', title: 'How customers see your business', short: 'Business',
          fields: [
            { id: 'biz_name', label: 'Business name on the page', value: 'A1 Progressive Construction' },
            { id: 'biz_phone', label: 'Phone number customers call', type: 'tel', value: '(201) 421-5953' },
            { id: 'biz_license', label: 'NJ home improvement license number', optional: true, placeholder: '13VH...', hint: 'We show it on the page. Homeowners look for it.' }
          ] },
        { id: 'alerts', type: 'single', title: 'Where should new job alerts go?', short: 'Alerts', sub: 'We text this number the moment someone books or asks for a price.',
          options: [opt('p1', '(201) 421-5953'), opt('p2', '(201) 982-2232'), opt('both', 'Both numbers'), opt('other', 'Another number')],
          other: { v: 'other', placeholder: 'Phone number for alerts' } },
        { id: 'area', type: 'multi', title: 'Which counties do you work in?', short: 'Service area', grid: true,
          options: [opt('bergen', 'Bergen'), opt('passaic', 'Passaic'), opt('essex', 'Essex'), opt('hudson', 'Hudson'), opt('morris', 'Morris'), opt('other', 'Somewhere else')],
          other: { v: 'other', placeholder: 'Which counties or towns?' } },
        { id: 'area_skip', type: 'fields', title: 'Any towns you don’t go to?', short: 'Towns to skip', sub: 'People there will be told to call instead of booking.',
          fields: [{ id: 'area_skip_txt', label: 'Towns or ZIP codes', optional: true, type: 'textarea', rows: 3, placeholder: 'Leave empty if you cover all of it' }] },
        { id: 'logo', type: 'files', slot: 'logo', max: 1, title: 'Your logo', short: 'Logo',
          preset: { label: 'Use the logo from my website', img: 'logo.png' }, addLabel: 'Upload a different logo' },
        { id: 'photos', type: 'files', slot: 'photo', max: 8, title: 'Photos of your work', short: 'Photos',
          sub: 'Real jobs make the page look like you, not a template. Roofs, chimneys, patios, before and after. Up to 8.', addLabel: 'Add photos' }
      ] },

      { title: 'Your services and prices', screens: [
        { id: 'trades', type: 'multi', title: 'What do you want customers to book online?', short: 'Services', grid: true,
          options: [opt('roofing', 'Roofing'), opt('chimney', 'Chimney'), opt('masonry', 'Masonry'), opt('siding', 'Siding'), opt('windows', 'Windows'), opt('gutters', 'Gutters'), { v: 'commercial', label: 'Commercial buildings', wide: true }] },
        { id: 'price_style', type: 'single', title: 'How should prices show on your page?', short: 'Price display',
          sub: 'Homeowners leave their name and phone to see the price, so you get the lead even if they don’t book.',
          options: [opt('ranges', 'Show prices and ranges', 'Recommended. Pages with prices get more requests.'), opt('from', 'Show “starting at” prices only'), opt('none', 'No prices, free estimates only')] },

        // Roofing
        { id: 'jobs_roofing', type: 'multi', title: 'Which roofing jobs?', short: 'Roofing jobs', when: function (a) { return has(a, 'trades', 'roofing'); },
          options: [opt('repair', 'Leak and shingle repairs'), opt('flashing', 'Flashing repairs'), opt('emergency', 'Emergency tarping'), opt('inspection', 'Roof inspections'),
            opt('replace', 'Full roof replacement'), opt('flat', 'Flat roofs', 'Rubber, modified bitumen'), opt('skylight', 'Skylights'), opt('ice', 'Ice dam removal')] },
        prices('p_roof_repair', 'Roof repair prices', ['leak_small', 'leak_mid', 'leak_big', 'shingle_few', 'shingle_more', 'shingle_section']),
        prices('p_roof_flash', 'Flashing prices', function (a) { return (has(a, 'trades', 'chimney') ? [] : ['flash_chim_reseal', 'flash_chim_full']).concat(['flash_wall', 'flash_sky']); }),
        prices('p_roof_tarp', 'Emergency tarp prices', ['tarp_day', 'tarp_night']),
        prices('p_roof_insp', 'Roof inspection prices', ['insp_quote', 'insp_report']),
        prices('p_roof_replace', 'New roof prices', ['rr_small', 'rr_colonial', 'rr_large', 'rr_layer', 'rr_sheet'],
          'Customers pick their house type and see this range. Change anything that’s off.'),
        prices('p_roof_flat', 'Flat roof prices', ['flat_repair', 'flat_small', 'flat_mid', 'flat_big']),
        prices('p_roof_sky', 'Skylight prices', ['sky_replace', 'sky_reroof']),
        prices('p_roof_ice', 'Ice dam prices', ['ice_one', 'ice_most', 'ice_all']),
        { id: 'shingles', type: 'multi', title: 'Which shingle brands do you install?', short: 'Shingle brands', when: function (a) { return has(a, 'trades', 'roofing') && has(a, 'jobs_roofing', 'replace'); },
          options: [opt('gaf', 'GAF'), opt('oc', 'Owens Corning'), opt('ct', 'CertainTeed'), opt('atlas', 'Atlas'), opt('other', 'Something else')], other: { v: 'other', placeholder: 'Which brand?' } },
        { id: 'certified', type: 'multi', title: 'Are you certified by a shingle maker?', short: 'Certifications', sub: 'Certified roofers can offer longer warranties. We show the badge.',
          when: function (a) { return has(a, 'trades', 'roofing') && has(a, 'jobs_roofing', 'replace'); }, only: 'none',
          options: [opt('gaf', 'GAF Certified or Master Elite'), opt('oc', 'Owens Corning Preferred or Platinum'), opt('ct', 'CertainTeed ShingleMaster or SELECT'), opt('none', 'No')] },
        { id: 'emergency', type: 'single', title: 'When do you take emergency leak calls?', short: 'Emergency calls',
          when: function (a) { return has(a, 'trades', 'roofing') && has(a, 'jobs_roofing', 'emergency'); },
          options: [opt('247', 'Any time, 24/7'), opt('days', 'Same day, during business hours'), opt('next', 'Next day')] },
        { id: 'emergency_phone', type: 'fields', title: 'Which number should emergency calls go to?', short: 'Emergency number',
          when: function (a) { return has(a, 'trades', 'roofing') && has(a, 'jobs_roofing', 'emergency') && is(a, 'emergency', '247'); },
          fields: [{ id: 'emergency_phone_txt', label: 'After-hours phone', type: 'tel', value: function (a) { return a.biz_phone || '(201) 421-5953'; } }] },
        { id: 'insurance', type: 'single', title: 'Do you work with homeowners’ insurance claims?', short: 'Insurance claims',
          when: function (a) { return has(a, 'trades', 'roofing'); },
          options: [opt('full', 'Yes, we help with the whole claim', 'Photos, the adjuster visit, the paperwork'), opt('photos', 'Yes, we give photos and a written estimate'), opt('no', 'No')] },

        // Chimney
        { id: 'jobs_chimney', type: 'multi', title: 'Which chimney jobs?', short: 'Chimney jobs', when: function (a) { return has(a, 'trades', 'chimney'); },
          options: [opt('sweep', 'Sweeps and cleaning'), opt('inspect', 'Inspections', 'Level 1, Level 2 camera, leak checks'), opt('cap', 'Chimney caps'), opt('crown', 'Crown repair'),
            opt('flashing', 'Chimney flashing'), opt('repoint', 'Repointing and rebuilds'), opt('liner', 'Stainless liners'), opt('waterproof', 'Waterproofing'), opt('damper', 'Dampers'),
            opt('creosote', 'Heavy creosote removal'), opt('prefab', 'Metal (prefab) chimneys', 'Chase covers')] },
        prices('p_ch_sweep', 'Sweep prices', ['sw_fire', 'sw_stove', 'sw_furnace', 'sw_gas', 'sw_extra'],
          'Sweeps work best as a fixed price customers can book right away. Change anything that’s off.'),
        prices('p_ch_inspect', 'Inspection prices', ['in_l1', 'in_l2', 'in_combo', 'in_leak']),
        prices('p_ch_cap', 'Chimney cap prices', ['cap_ss', 'cap_cu', 'cap_multi']),
        prices('p_ch_crown', 'Crown prices', ['crown_seal', 'crown_new']),
        prices('p_ch_flashing', 'Chimney flashing prices', ['cf_reseal', 'cf_full']),
        prices('p_ch_repoint', 'Repointing and rebuild prices', ['cp_spots', 'cp_most', 'cp_rebuild']),
        prices('p_ch_liner', 'Liner prices', ['ln_gas', 'ln_oil', 'ln_stove', 'ln_fire'], 'Customers pick what the liner is for. Change anything that’s off.'),
        prices('p_ch_waterproof', 'Waterproofing price', ['wp']),
        prices('p_ch_damper', 'Damper prices', ['dm_fix', 'dm_top']),
        prices('p_ch_creosote', 'Creosote prices', ['cr_heavy', 'cr_glazed']),
        prices('p_ch_prefab', 'Metal chimney prices', ['chase']),
        { id: 'fall_special', type: 'single', title: 'Do you want to run a fall sweep special?', short: 'Fall special',
          sub: 'Other Bergen sweeps advertise $149 to $179 right now. A special on your page books the busy season early.',
          when: function (a) { return has(a, 'trades', 'chimney') && has(a, 'jobs_chimney', 'sweep'); },
          options: [opt('yes', 'Yes'), opt('no', 'No')] },
        { id: 'fall_special_d', type: 'fields', title: 'What’s the special?', short: 'Special details',
          when: function (a) { return has(a, 'trades', 'chimney') && has(a, 'jobs_chimney', 'sweep') && is(a, 'fall_special', 'yes'); },
          fields: [{ id: 'fall_special_txt', label: 'Offer', placeholder: 'Sweep + inspection $199 until Dec 31' }] },

        // Masonry
        { id: 'jobs_masonry', type: 'multi', title: 'Which masonry jobs?', short: 'Masonry jobs', when: function (a) { return has(a, 'trades', 'masonry'); },
          options: [opt('brick', 'Brick repair'), opt('repoint', 'Repointing'), opt('steps', 'Front steps'), opt('walk', 'Walkways'), opt('patio', 'Patios'), opt('wall', 'Retaining walls'), opt('parging', 'Foundation parging')] },
        prices('p_ms_brick', 'Brick repair prices', ['br_few', 'br_yard', 'br_big']),
        prices('p_ms_repoint', 'Repointing prices', ['rp_patch', 'rp_steps', 'rp_part', 'rp_wall']),
        { id: 'mat_steps', type: 'multi', title: 'What kind of steps do you build?', short: 'Step materials', when: function (a) { return has(a, 'trades', 'masonry') && has(a, 'jobs_masonry', 'steps'); },
          options: [opt('brick', 'Brick'), opt('concrete', 'Concrete'), opt('stone', 'Bluestone or stone'), opt('repair', 'Repairs only')] },
        prices('p_ms_steps', 'Step prices', function (a) {
          var m = a.mat_steps || [], out = ['st_repair'];
          if (m.indexOf('brick') > -1) out.push('st_brick_s', 'st_brick_l');
          if (m.indexOf('concrete') > -1) out.push('st_conc_s', 'st_conc_l');
          if (m.indexOf('stone') > -1) out.push('st_stone_s', 'st_stone_l');
          if (m.length && !(m.length === 1 && m[0] === 'repair')) out.push('st_rail');
          return out;
        }),
        { id: 'mat_walk', type: 'multi', title: 'What kind of walkways do you build?', short: 'Walkway materials', when: function (a) { return has(a, 'trades', 'masonry') && has(a, 'jobs_masonry', 'walk'); },
          options: [opt('pavers', 'Pavers'), opt('concrete', 'Concrete'), opt('stone', 'Bluestone or brick'), opt('repair', 'Repairs only')] },
        prices('p_ms_walk', 'Walkway prices', function (a) {
          var m = a.mat_walk || [], out = ['wk_repair'];
          if (m.indexOf('pavers') > -1) out.push('wk_pav_s', 'wk_pav_m', 'wk_pav_l');
          if (m.indexOf('concrete') > -1) out.push('wk_con_s', 'wk_con_m', 'wk_con_l');
          if (m.indexOf('stone') > -1) out.push('wk_blu_s', 'wk_blu_m', 'wk_blu_l');
          return out;
        }),
        { id: 'mat_patio', type: 'multi', title: 'What kind of patios do you build?', short: 'Patio materials', when: function (a) { return has(a, 'trades', 'masonry') && has(a, 'jobs_masonry', 'patio'); },
          options: [opt('pavers', 'Pavers'), opt('stone', 'Bluestone or natural stone'), opt('concrete', 'Poured concrete')] },
        prices('p_ms_patio', 'Patio prices', function (a) {
          var m = a.mat_patio || [], out = [];
          if (m.indexOf('pavers') > -1) out.push('pt_pav_s', 'pt_pav_m', 'pt_pav_l');
          if (m.indexOf('stone') > -1) out.push('pt_blu_s', 'pt_blu_m', 'pt_blu_l');
          if (m.indexOf('concrete') > -1) out.push('pt_con_s', 'pt_con_m', 'pt_con_l');
          return out;
        }, 'Customers pick the size and see this range. Patios over 600 sq ft go to a free estimate.'),
        prices('p_ms_wall', 'Retaining wall prices', ['rw_low_s', 'rw_low_m', 'rw_mid_s', 'rw_mid_m', 'rw_mid_l'],
          'Block walls. Walls over 4 ft need a permit and an engineer in NJ, so those go to a free estimate.'),
        prices('p_ms_parging', 'Parging prices', ['pg_spot', 'pg_side', 'pg_all']),
        { id: 'mason_min', type: 'fields', title: 'Do you have a minimum for small masonry jobs?', short: 'Masonry minimum',
          when: function (a) { return has(a, 'trades', 'masonry'); },
          fields: [{ id: 'mason_min_txt', label: 'Minimum job', optional: true, placeholder: '$450', hint: 'Most North Jersey masons start around $450.' }] },

        // Siding
        { id: 'jobs_siding', type: 'multi', title: 'Which siding jobs?', short: 'Siding jobs', when: function (a) { return has(a, 'trades', 'siding'); },
          options: [opt('vinyl', 'New vinyl siding'), opt('hardie', 'New James Hardie (fiber cement)'), opt('repair', 'Siding repairs'), opt('soffit', 'Soffit and fascia'), opt('trim', 'Aluminum trim capping')] },
        prices('p_sd_vinyl', 'Vinyl siding prices', ['vs_1s', 'vs_1l', 'vs_2s', 'vs_2m', 'vs_2l'], 'Customers pick their house and see this range. Change anything that’s off.'),
        prices('p_sd_hardie', 'James Hardie prices', ['hs_1s', 'hs_1l', 'hs_2s', 'hs_2m']),
        prices('p_sd_repair', 'Siding repair prices', ['sr_few', 'sr_section', 'sr_side']),
        prices('p_sd_soffit', 'Soffit and fascia prices', ['sf_repair', 'sf_all1', 'sf_all2']),
        prices('p_sd_trim', 'Trim capping prices', ['tc_s', 'tc_m', 'tc_l']),
        { id: 'asbestos', type: 'single', title: 'Do you take on houses with asbestos siding?', short: 'Asbestos siding',
          sub: 'Common on North Jersey homes built before 1980. We send these to a free estimate instead of showing a price.',
          when: function (a) { return has(a, 'trades', 'siding') && (has(a, 'jobs_siding', 'vinyl') || has(a, 'jobs_siding', 'hardie')); },
          options: [opt('yes', 'Yes, we handle removal'), opt('partner', 'Yes, with a removal partner'), opt('no', 'No')] },

        // Windows
        { id: 'jobs_windows', type: 'multi', title: 'Which window jobs?', short: 'Window jobs', when: function (a) { return has(a, 'trades', 'windows'); },
          options: [opt('replace', 'Replacement windows'), opt('special', 'Bay, bow and picture windows'), opt('basement', 'Basement and egress windows'), opt('glass', 'Foggy or broken glass'), opt('newcon', 'Windows for additions')] },
        prices('p_wn_replace', 'Replacement window prices', ['wn_one', 'wn_some', 'wn_many', 'wn_premium', 'wn_casement'], 'Per window, installed. Customers pick how many. Change anything that’s off.'),
        prices('p_wn_special', 'Special window prices', ['wn_bay', 'wn_bow', 'wn_picture']),
        prices('p_wn_basement', 'Basement window prices', ['wn_base', 'wn_egress']),
        prices('p_wn_glass', 'Glass repair price', ['wn_glass']),
        { id: 'win_brands', type: 'fields', title: 'Which window brands do you install?', short: 'Window brands', when: function (a) { return has(a, 'trades', 'windows'); },
          fields: [{ id: 'win_brands_txt', label: 'Brands', optional: true, placeholder: 'Andersen, Pella, Harvey, Simonton...' }] },

        // Gutters
        { id: 'jobs_gutters', type: 'multi', title: 'Which gutter jobs?', short: 'Gutter jobs', when: function (a) { return has(a, 'trades', 'gutters'); },
          options: [opt('clean', 'Gutter cleaning'), opt('new', 'New seamless gutters'), opt('repair', 'Repairs and downspouts'), opt('guards', 'Gutter guards'), opt('yankee', 'Yankee gutters', 'Built-in wood gutters on older homes')] },
        prices('p_gt_clean', 'Gutter cleaning prices', ['gc_1', 'gc_2', 'gc_3'], 'Cleaning works best as a fixed price customers can book right away.'),
        prices('p_gt_new', 'New gutter prices', ['gs_1', 'gs_2', 'gs_6', 'gs_cu']),
        prices('p_gt_repair', 'Gutter repair prices', ['gr_fix', 'gr_section', 'gr_down']),
        prices('p_gt_guards', 'Gutter guard price', ['gg_guard']),
        prices('p_gt_yankee', 'Yankee gutter prices', ['yk_rubber', 'yk_copper', 'yk_wood', 'yk_convert'], 'You refurbish Yankee gutters, and no one else in North Jersey shows a price for it. That makes it a strong thing to put on your page.'),

        // Commercial
        { id: 'commercial', type: 'multi', title: 'Which commercial jobs do you want requests for?', short: 'Commercial jobs', when: function (a) { return has(a, 'trades', 'commercial'); },
          sub: 'Commercial requests never show a price. They come to you as a call-back request.',
          options: [opt('roof', 'Roofing'), opt('siding', 'Siding'), opt('masonry', 'Masonry'), opt('windows', 'Windows'), opt('gutters', 'Gutters'), opt('maint', 'Ongoing maintenance')] },
        { id: 'commercial_min', type: 'fields', title: 'What commercial jobs are too small for you?', short: 'Commercial minimum', when: function (a) { return has(a, 'trades', 'commercial'); },
          fields: [{ id: 'commercial_min_txt', label: 'Smallest job you take', optional: true, placeholder: 'For example: under $5,000' }] },

        // Applies to every trade, with job-specific add-ons
        { id: 'p_hidden', type: 'fields', title: 'Anything you do that we didn’t list?', short: 'Other jobs',
          fields: [{ id: 'other_jobs', label: 'Other jobs and prices', optional: true, type: 'textarea', rows: 4, placeholder: 'For example: attic fans, $450 installed' }] }
      ] },

      { title: 'How booking works', screens: [
        { id: 'hours', type: 'hours', title: 'When can you do estimates and visits?', short: 'Visit hours', sub: 'Customers only see open times in these hours.' },
        { id: 'visit_len', type: 'single', title: 'How long is a typical estimate visit?', short: 'Visit length',
          options: [opt('30', '30 minutes'), opt('60', '1 hour'), opt('90', '1 hour 30 minutes'), opt('120', '2 hours')] },
        { id: 'per_day', type: 'single', title: 'How many visits can you do in a day?', short: 'Visits per day',
          options: [opt('2', 'Up to 2'), opt('4', 'Up to 4'), opt('6', 'Up to 6'), opt('any', 'No limit')] },
        { id: 'confirm', type: 'single', title: 'When someone picks a time, what should happen?', short: 'Booking',
          options: [opt('book', 'Book it right away', 'It goes on your calendar, they get a text'), opt('confirm', 'I confirm it first by text', 'They see “requested” until you reply')] },
        { id: 'financing', type: 'single', title: 'Do you offer financing?', short: 'Financing',
          options: [opt('yes', 'Yes'), opt('no', 'No')] },
        { id: 'financing_d', type: 'fields', title: 'Tell us about the financing', short: 'Financing details', when: function (a) { return is(a, 'financing', 'yes'); },
          sub: 'We show a line like “as low as $129 a month” next to big jobs.',
          fields: [
            { id: 'fin_company', label: 'Financing company', placeholder: 'GreenSky, Hearth, Service Finance...' },
            { id: 'fin_from', label: 'Smallest monthly payment you advertise', optional: true, placeholder: '$129 a month' },
            { id: 'fin_link', label: 'Link to apply', optional: true, placeholder: 'https://' }
          ] },
        { id: 'warranty', type: 'single', title: 'What warranty do you give on your work?', short: 'Warranty',
          options: [opt('1', '1 year'), opt('2', '2 years'), opt('5', '5 years'), opt('10', '10 years'), opt('life', 'Lifetime'), opt('varies', 'Depends on the job'), opt('other', 'Something else')],
          other: { v: 'other', placeholder: 'Describe it' } },
        { id: 'discounts', type: 'multi', title: 'Any discounts we should show?', short: 'Discounts', only: 'none',
          options: [opt('senior', 'Seniors'), opt('veteran', 'Veterans and military'), opt('first', 'First responders'), opt('other', 'Something else'), opt('none', 'No discounts')],
          other: { v: 'other', placeholder: 'What discount?' } },
        { id: 'discount_amt', type: 'fields', title: 'How much off?', short: 'Discount amount',
          when: function (a) { return (a.discounts || []).length && !has(a, 'discounts', 'none'); },
          fields: [{ id: 'discount_amt_txt', label: 'Discount', placeholder: '10% off, or $250 off jobs over $5,000' }] },
        { id: 'website', type: 'single', title: 'Who takes care of your website?', short: 'Website',
          sub: 'We add a “Book online” button to it. It’s one line of code.',
          options: [opt('me', 'I do'), opt('agency', 'A web person or company'), opt('us', 'Please do it for me'), opt('unsure', 'Not sure')] },
        { id: 'website_agency', type: 'fields', title: 'Who should we send the code to?', short: 'Web person', when: function (a) { return is(a, 'website', 'agency'); },
          fields: [{ id: 'web_contact', label: 'Their name and email', placeholder: 'Name, email' }] },
        { id: 'website_login', type: 'single', title: 'How should we get into your website?', short: 'Website access', when: function (a) { return is(a, 'website', 'us'); },
          sub: 'Your site runs on WordPress. Never send a password here.',
          options: [opt('invite', 'I’ll add you as a user', 'We’ll send the email to invite'), opt('call', 'Let’s do it on a quick call')] },
        { id: 'google', type: 'single', title: 'Should we add the booking link to your Google profile?', short: 'Google profile',
          sub: 'Your Google listing gets a “Book online” button. Most bookings start there.',
          options: [opt('yes', 'Yes'), opt('self', 'I’ll add it myself'), opt('no', 'No')] },
        { id: 'notes', type: 'fields', title: 'Anything else we should know?', short: 'Notes',
          fields: [{ id: 'notes_txt', label: 'Notes', optional: true, type: 'textarea', rows: 5, placeholder: 'Jobs you don’t want, busy seasons, how you like to talk to customers...' }] },
        { id: 'review', type: 'review', title: 'Check your answers', short: 'Review', sub: 'Tap Edit to change anything. Then send it to us.' },
        { id: 'done', type: 'done', title: 'We got everything.',
          text: '<p>We’ll build your booking page with your prices and send you a link to look at, usually within two business days.</p><p>Questions? Reply to the email we just sent you, or write to info@dialbridge.ai.</p>' }
      ] }
    ]
  };

  // Every price screen shows only when its job was picked and prices are on.
  var map = {
    p_roof_repair: ['roofing', 'repair'], p_roof_flash: ['roofing', 'flashing'], p_roof_tarp: ['roofing', 'emergency'], p_roof_insp: ['roofing', 'inspection'],
    p_roof_replace: ['roofing', 'replace'], p_roof_flat: ['roofing', 'flat'], p_roof_sky: ['roofing', 'skylight'], p_roof_ice: ['roofing', 'ice'],
    p_ch_sweep: ['chimney', 'sweep'], p_ch_inspect: ['chimney', 'inspect'], p_ch_cap: ['chimney', 'cap'], p_ch_crown: ['chimney', 'crown'], p_ch_flashing: ['chimney', 'flashing'],
    p_ch_repoint: ['chimney', 'repoint'], p_ch_liner: ['chimney', 'liner'], p_ch_waterproof: ['chimney', 'waterproof'], p_ch_damper: ['chimney', 'damper'],
    p_ch_creosote: ['chimney', 'creosote'], p_ch_prefab: ['chimney', 'prefab'],
    p_ms_brick: ['masonry', 'brick'], p_ms_repoint: ['masonry', 'repoint'], p_ms_steps: ['masonry', 'steps'], p_ms_walk: ['masonry', 'walk'], p_ms_patio: ['masonry', 'patio'],
    p_ms_wall: ['masonry', 'wall'], p_ms_parging: ['masonry', 'parging'],
    p_sd_vinyl: ['siding', 'vinyl'], p_sd_hardie: ['siding', 'hardie'], p_sd_repair: ['siding', 'repair'], p_sd_soffit: ['siding', 'soffit'], p_sd_trim: ['siding', 'trim'],
    p_wn_replace: ['windows', 'replace'], p_wn_special: ['windows', 'special'], p_wn_basement: ['windows', 'basement'], p_wn_glass: ['windows', 'glass'],
    p_gt_clean: ['gutters', 'clean'], p_gt_new: ['gutters', 'new'], p_gt_repair: ['gutters', 'repair'], p_gt_guards: ['gutters', 'guards'], p_gt_yankee: ['gutters', 'yankee']
  };
  window.FORM.parts[1].screens.forEach(function (s) {
    if (map[s.id]) {
      var w = jobsOf(map[s.id][0], map[s.id][1]), items = s.items;
      s.when = function (a) { return w(a) && items(a).length > 0; };
    }
  });
})();
