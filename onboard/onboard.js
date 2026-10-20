/* Dialbridge setup form for custom clients (matviykorsunskiy.me/<client>/).
   One question per screen, grouped into a few named parts. A screen can depend on earlier answers (`when`), so
   a "yes" opens its follow-up questions and a "no" skips them. Answers are kept in this browser and saved to our
   API after every screen (a draft), then sent once from the review screen. The questions live in the client's own
   form.js as window.FORM; this file only knows how to show them. */
(function () {
  'use strict';
  var F = window.FORM;
  if (!F) return;
  var API = (F.api || 'https://dialbridge-booking-api.dialbridge-booking-api.workers.dev').replace(/\/+$/, '');
  // Local testing only: ?api=http://localhost:PORT (never another host, so a link can't send answers elsewhere).
  var testApi = /[?&]api=(http:\/\/localhost:\d{2,5})(?:&|$)/.exec(location.search);
  if (testApi) API = testApi[1];
  // The backup copy (n8n) is skipped in local tests unless ?backup=1.
  var BACKUP = F.backup && (!testApi || /[?&]backup=1\b/.test(location.search)) ? F.backup : '';
  var LS = 'dbx_form_' + F.form;
  var main = document.getElementById('fmain'), bar = document.getElementById('fbar'), partEl = document.getElementById('fpart'), backBtn = document.getElementById('fback');

  // ---------- state ----------
  function newKey() {
    var a = new Uint8Array(16); (window.crypto || window.msCrypto).getRandomValues(a);
    return 'f_' + Array.prototype.map.call(a, function (b) { return ('0' + b.toString(16)).slice(-2); }).join('');
  }
  function load() { try { var s = JSON.parse(localStorage.getItem(LS) || 'null'); if (s && s.key && s.a) return s; } catch (e) { } return null; }
  var S = load() || { key: newKey(), a: {}, cur: null, files: {}, sent: false };
  if (/[?&]reset\b/.test(location.search)) { S = { key: newKey(), a: {}, cur: null, files: {}, sent: false }; }
  function saveLocal() { try { localStorage.setItem(LS, JSON.stringify(S)); } catch (e) { } }

  // ---------- screens ----------
  var ALL = [];
  F.parts.forEach(function (p, pi) { p.screens.forEach(function (s) { s.part = pi; ALL.push(s); }); });
  function visible() { return ALL.filter(function (s) { return !s.when || s.when(S.a); }); }
  function byId(id) { for (var i = 0; i < ALL.length; i++) if (ALL[i].id === id) return ALL[i]; return null; }
  function current() {
    var v = visible(), s = S.cur && byId(S.cur);
    if (s && v.indexOf(s) > -1) return s;
    return v[0];
  }
  function go(s) { S.cur = s.id; saveLocal(); render(true); window.scrollTo(0, 0); }
  function next() {
    var v = visible(), i = v.indexOf(current());
    if (S.toReview) { S.toReview = false; var r = v.filter(function (x) { return x.type === 'review'; })[0]; if (r) return go(r); }
    if (i < v.length - 1) go(v[i + 1]);
  }
  function back() { var v = visible(), i = v.indexOf(current()); if (i > 0) { S.toReview = false; go(v[i - 1]); } }

  // ---------- helpers ----------
  function esc(s) { return String(s === undefined || s === null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function val(id, d) { return S.a[id] !== undefined ? S.a[id] : d; }
  var CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
  var BACK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg>';
  function money(n) { n = +n; return isFinite(n) ? '$' + n.toLocaleString('en-US') : ''; }
  function optList(s) { return typeof s.options === 'function' ? s.options(S.a) : s.options; }
  function title(s) { return typeof s.title === 'function' ? s.title(S.a) : s.title; }
  function sub(s) { return typeof s.sub === 'function' ? s.sub(S.a) : s.sub; }

  // ---------- render ----------
  function head(s) {
    return '<h1>' + esc(title(s)) + '</h1>' + (sub(s) ? '<p class="sub">' + sub(s) + '</p>' : '');
  }
  function actions(label, opts) {
    opts = opts || {};
    return '<div class="acts">' + (opts.noBack ? '<span></span>' : '<button class="btn ghost" type="button" data-back>' + BACK + 'Back</button>') +
      '<button class="btn" type="button" data-next' + (opts.disabled ? ' disabled' : '') + '>' + esc(label || 'Continue') + '</button></div>';
  }
  var R = {};
  R.intro = function (s) {
    return '<div class="q intro">' + (F.logo ? '<img class="logo" src="' + esc(F.logo) + '" alt="' + esc(F.business) + '">' : '') +
      '<h1>' + esc(title(s)) + '</h1><div class="sub">' + s.text + '</div>' +
      '<div class="acts start"><button class="btn" type="button" data-next>' + esc(S.cur && Object.keys(S.a).length ? 'Continue where I left off' : (s.button || 'Start')) + '</button></div>' +
      (s.fine ? '<p class="fine">' + s.fine + '</p>' : '') + '</div>';
  };
  R.fields = function (s) {
    return '<div class="q">' + head(s) + '<div class="fields">' + s.fields.map(function (f) {
      var v = val(f.id, typeof f.value === 'function' ? f.value(S.a) : f.value);
      var input = f.type === 'textarea'
        ? '<textarea class="in" rows="' + (f.rows || 4) + '" data-f="' + f.id + '" placeholder="' + esc(f.placeholder || '') + '">' + esc(v) + '</textarea>'
        : '<input class="in" data-f="' + f.id + '" type="' + (f.type || 'text') + '" value="' + esc(v) + '" placeholder="' + esc(f.placeholder || '') + '"' +
          (f.type === 'tel' ? ' inputmode="tel" autocomplete="tel"' : f.type === 'email' ? ' autocomplete="email"' : f.auto ? ' autocomplete="' + f.auto + '"' : '') + '>';
      return '<label class="field"><span>' + esc(f.label) + (f.optional ? ' <em>optional</em>' : '') + '</span>' + input + (f.hint ? '<small>' + esc(f.hint) + '</small>' : '') + '</label>';
    }).join('') + '</div><p class="err" id="ferr"></p>' + actions(s.button) + '</div>';
  };
  function optHtml(o, on, multi) {
    return '<button type="button" class="opt' + (multi ? ' multi' : '') + (on ? ' on' : '') + (o.wide ? ' wide' : '') + '" data-v="' + esc(o.v) + '">' +
      '<span class="ot">' + esc(o.label) + (o.hint ? '<small>' + esc(o.hint) + '</small>' : '') + '</span><span class="ck">' + CHECK + '</span></button>';
  }
  function otherHtml(s, show) {
    if (!s.other) return '';
    return '<div class="other' + (show ? ' on' : '') + '"><input class="in" data-other="' + s.id + '" placeholder="' + esc(s.other.placeholder || 'Tell us') + '" value="' + esc(val(s.id + '_other', '')) + '"></div>';
  }
  R.single = function (s) {
    var v = val(s.id, s.value);
    var opts = optList(s);
    return '<div class="q">' + head(s) + '<div class="opts' + (s.grid ? ' grid' : '') + '">' + opts.map(function (o) { return optHtml(o, v === o.v, false); }).join('') + '</div>' +
      otherHtml(s, s.other && v === s.other.v) + '<p class="err" id="ferr"></p>' + actions(s.button, { disabled: v === undefined }) + '</div>';
  };
  R.multi = function (s) {
    var v = val(s.id, s.value || []);
    var opts = optList(s);
    return '<div class="q">' + head(s) + '<div class="opts' + (s.grid ? ' grid' : '') + '">' + opts.map(function (o) { return optHtml(o, v.indexOf(o.v) > -1, true); }).join('') + '</div>' +
      otherHtml(s, s.other && v.indexOf(s.other.v) > -1) + '<p class="err" id="ferr"></p>' + actions(s.button, { disabled: !s.optional && !v.length }) + '</div>';
  };
  // Prices: one row per job they picked. Each row: how it's sold (fixed price / range then visit / free estimate)
  // and the numbers, filled in with the North Jersey typical prices we researched.
  var MODES = [['fixed', 'Fixed price'], ['range', 'Price range'], ['estimate', 'Free estimate']];
  function priceItems(s) { return (s.items(S.a) || []).map(function (id) { return F.catalog[id] ? Object.assign({ id: id }, F.catalog[id]) : null; }).filter(Boolean); }
  function priceVal(s, it) {
    var all = val(s.id, {}), v = all[it.id];
    return v || { mode: it.mode || 'range', low: it.low, high: it.high };
  }
  R.prices = function (s) {
    var items = priceItems(s);
    return '<div class="q">' + head(s) + '<div class="prs">' + items.map(function (it) {
      var v = priceVal(s, it);
      return '<div class="pr" data-item="' + esc(it.id) + '"><div class="pr-h"><b>' + esc(it.label) + '</b>' +
        '<small>' + esc(it.unit ? it.unit + ' · ' : '') + 'North NJ typical ' + money(it.low) + (it.high && it.high !== it.low ? ' to ' + money(it.high) : '') + '</small></div>' +
        '<div class="seg" role="radiogroup">' + MODES.map(function (m) { return '<button type="button" role="radio" aria-checked="' + (v.mode === m[0]) + '" class="' + (v.mode === m[0] ? 'on' : '') + '" data-m="' + m[0] + '">' + m[1] + '</button>'; }).join('') + '</div>' +
        '<div class="pr-in' + (v.mode === 'estimate' ? ' off' : '') + '">' +
          '<label><span>' + (v.mode === 'fixed' ? 'Price' : 'From') + '</span><i>$</i><input class="in" inputmode="numeric" data-lo value="' + esc(v.low) + '"></label>' +
          (v.mode === 'range' ? '<label><span>To</span><i>$</i><input class="in" inputmode="numeric" data-hi value="' + esc(v.high) + '"></label>' : '') +
        '</div>' + (it.note ? '<p class="pr-note">' + esc(it.note) + '</p>' : '') + '</div>';
    }).join('') + '</div>' + actions(s.button) + '</div>';
  };
  R.hours = function (s) {
    var v = val(s.id, s.value || { days: [1, 2, 3, 4, 5, 6], from: '08:00', to: '17:00' });
    var D = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], times = [];
    for (var h = 6; h <= 21; h++) { [0, 30].forEach(function (m) { var t = ('0' + h).slice(-2) + ':' + (m ? '30' : '00'); times.push(t); }); }
    function label(t) { var h = +t.slice(0, 2), m = t.slice(3); return (h % 12 || 12) + (m === '00' ? '' : ':' + m) + (h < 12 ? ' AM' : ' PM'); }
    function sel(k) { return '<select class="in" data-h="' + k + '">' + times.map(function (t) { return '<option value="' + t + '"' + (v[k] === t ? ' selected' : '') + '>' + label(t) + '</option>'; }).join('') + '</select>'; }
    var order = [1, 2, 3, 4, 5, 6, 0];
    return '<div class="q">' + head(s) + '<div class="days">' + order.map(function (d) { return '<button type="button" class="' + (v.days.indexOf(d) > -1 ? 'on' : '') + '" data-d="' + d + '">' + D[d] + '</button>'; }).join('') + '</div>' +
      '<div class="hrs"><label class="field"><span>From</span>' + sel('from') + '</label><label class="field"><span>To</span>' + sel('to') + '</label></div>' +
      '<p class="err" id="ferr"></p>' + actions(s.button) + '</div>';
  };
  // Files: resized here, then sent to the API (the draft is saved first so the file has a form to belong to).
  R.files = function (s) {
    var mine = (S.files[s.id] || []);
    var preset = s.preset && val(s.id + '_preset', true);
    return '<div class="q">' + head(s) +
      (s.preset ? '<button type="button" class="opt multi' + (preset ? ' on' : '') + '" data-preset><span class="ot">' + esc(s.preset.label) + (s.preset.img ? '<img class="preset" src="' + esc(s.preset.img) + '" alt="">' : '') + '</span><span class="ck">' + CHECK + '</span></button>' : '') +
      '<div class="thumbs">' + mine.map(function (f, i) { return '<figure><img src="' + esc(f.thumb) + '" alt=""><button type="button" aria-label="Remove" data-rm="' + i + '">×</button></figure>'; }).join('') +
      (mine.length < (s.max || 1) ? '<label class="add"><input type="file" accept="image/png,image/jpeg,image/webp" ' + ((s.max || 1) > 1 ? 'multiple' : '') + ' hidden data-file><span>+ ' + esc(s.addLabel || 'Add a photo') + '</span></label>' : '') + '</div>' +
      '<p class="err" id="ferr"></p>' + actions(s.button || (mine.length || preset ? 'Continue' : 'Skip for now')) + '</div>';
  };
  R.review = function (s) {
    var groups = summaryGroups();
    return '<div class="q">' + head(s) + '<div class="rev">' + groups.map(function (g) {
      return '<section><h2>' + esc(g.title) + '</h2>' + g.rows.map(function (r) {
        return '<div class="rv"><div><span>' + esc(r.q) + '</span><b>' + esc(r.a).replace(/\n/g, '<br>') + '</b></div><button type="button" class="link" data-edit="' + esc(r.id) + '">Edit</button></div>';
      }).join('') + '</section>';
    }).join('') + '</div><p class="err" id="ferr"></p>' + actions(s.button || 'Send my answers') + '</div>';
  };
  R.done = function (s) {
    var first = String(S.a[F.contact.name] || '').split(' ')[0];
    return '<div class="q done"><div class="ok">' + CHECK + '</div><h1>' + esc((first ? 'Thanks, ' + first + '. ' : 'Thanks. ') + (s.title || 'We got everything.')) + '</h1>' +
      '<div class="sub">' + s.text + '</div></div>';
  };

  // ---------- summary (review screen, and the text we email ourselves) ----------
  function answerText(s) {
    var v = S.a[s.id];
    if (s.type === 'fields') return s.fields.map(function (f) { var x = S.a[f.id]; return x ? (s.fields.length > 1 ? f.label + ': ' : '') + x : ''; }).filter(Boolean).join('\n');
    if (s.type === 'single') { var o = optList(s).filter(function (o) { return o.v === v; })[0]; return o ? o.label + (s.other && v === s.other.v && S.a[s.id + '_other'] ? ': ' + S.a[s.id + '_other'] : '') : ''; }
    if (s.type === 'multi') {
      v = v || [];
      return optList(s).filter(function (o) { return v.indexOf(o.v) > -1; }).map(function (o) { return o.label + (s.other && o.v === s.other.v && S.a[s.id + '_other'] ? ': ' + S.a[s.id + '_other'] : ''); }).join('\n');
    }
    if (s.type === 'prices') {
      return priceItems(s).map(function (it) {
        var p = priceVal(s, it);
        return it.label + ': ' + (p.mode === 'estimate' ? 'free estimate' : p.mode === 'fixed' ? money(p.low) + ' fixed' : money(p.low) + ' to ' + money(p.high));
      }).join('\n');
    }
    if (s.type === 'hours') {
      var h = v || { days: [1, 2, 3, 4, 5, 6], from: '08:00', to: '17:00' }, D = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
      var tl = function (t) { var hh = +t.slice(0, 2), mm = t.slice(3); return (hh % 12 || 12) + (mm === '00' ? '' : ':' + mm) + (hh < 12 ? ' AM' : ' PM'); };
      return [1, 2, 3, 4, 5, 6, 0].filter(function (d) { return h.days.indexOf(d) > -1; }).map(function (d) { return D[d]; }).join(', ') + ', ' + tl(h.from) + ' to ' + tl(h.to);
    }
    if (s.type === 'files') {
      var n = (S.files[s.id] || []).length, pre = s.preset && val(s.id + '_preset', true);
      return [pre ? s.preset.label : '', n ? n + ' uploaded' : ''].filter(Boolean).join(', ') || 'None';
    }
    return '';
  }
  function summaryGroups() {
    var v = visible(), groups = [];
    F.parts.forEach(function (p, pi) {
      var rows = v.filter(function (s) { return s.part === pi && ['intro', 'review', 'done'].indexOf(s.type) < 0; })
        .map(function (s) { return { id: s.id, q: s.short || title(s), a: answerText(s) || '(skipped)' }; });
      if (rows.length) groups.push({ title: p.title, rows: rows });
    });
    return groups;
  }
  function summaryText() {
    return summaryGroups().map(function (g) {
      return g.title.toUpperCase() + '\n' + g.rows.map(function (r) { return '- ' + r.q + '\n  ' + r.a.replace(/\n/g, '\n  '); }).join('\n');
    }).join('\n\n');
  }

  // ---------- saving ----------
  var saving = null, dirty = false;
  function body(extra) {
    var c = F.contact;
    return Object.assign({ key: S.key, form: F.form, business: S.a[c.business] || F.business, name: S.a[c.name] || '', phone: S.a[c.phone] || '', email: S.a[c.email] || '',
      answers: S.a, page: location.href.split('#')[0] }, extra || {});
  }
  function post(path, data) {
    return fetch(API + path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { j.status = r.status; return j; }); });
  }
  function saveDraft() {
    if (S.sent) return Promise.resolve();
    if (saving) { dirty = true; return saving; }
    saving = post('/v1/intake', body()).catch(function () { }).then(function () {
      saving = null; S.saved = true; saveLocal();
      if (dirty) { dirty = false; return saveDraft(); }
    });
    return saving;
  }

  // ---------- images ----------
  function resize(file, max, type) {
    return new Promise(function (ok, no) {
      var img = new Image(), url = URL.createObjectURL(file);
      img.onload = function () {
        var k = Math.min(1, max / Math.max(img.width, img.height)), w = Math.round(img.width * k), h = Math.round(img.height * k);
        var c = document.createElement('canvas'); c.width = w; c.height = h;
        var x = c.getContext('2d'); if (type === 'image/jpeg') { x.fillStyle = '#fff'; x.fillRect(0, 0, w, h); }
        x.drawImage(img, 0, 0, w, h); URL.revokeObjectURL(url);
        var d = c.toDataURL(type, 0.82);
        var t = document.createElement('canvas'), tk = Math.min(1, 240 / Math.max(w, h)); t.width = Math.round(w * tk); t.height = Math.round(h * tk);
        t.getContext('2d').drawImage(c, 0, 0, t.width, t.height);
        ok({ data: d, thumb: t.toDataURL('image/jpeg', 0.7) });
      };
      img.onerror = function () { URL.revokeObjectURL(url); no(new Error('image')); };
      img.src = url;
    });
  }
  function nextSlot() { var used = {}; Object.keys(S.files).forEach(function (k) { S.files[k].forEach(function (f) { used[f.n] = 1; }); }); for (var n = 1; n <= 12; n++) if (!used[n]) return n; return 0; }

  // ---------- events ----------
  function err(msg) { var e = document.getElementById('ferr'); if (e) e.textContent = msg || ''; }
  function collectFields(s) {
    var ok = true, msg = '';
    s.fields.forEach(function (f) {
      var el = main.querySelector('[data-f="' + f.id + '"]'), v = el.value.trim();
      S.a[f.id] = v;
      var bad = (!f.optional && !v) || (v && f.type === 'email' && !/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(v)) || (v && f.type === 'tel' && v.replace(/\D/g, '').length < 10);
      el.classList.toggle('bad', !!bad);
      if (bad && ok) { ok = false; msg = !v ? 'Please fill in ' + f.label.toLowerCase() + '.' : f.type === 'email' ? 'That email doesn’t look right.' : 'Please enter a 10-digit phone number.'; el.focus(); }
    });
    if (!ok) err(msg);
    return ok;
  }
  function collectPrices(s) {
    var all = Object.assign({}, val(s.id, {}));
    main.querySelectorAll('.pr').forEach(function (row) {
      var id = row.getAttribute('data-item'), it = F.catalog[id];
      var mode = (row.querySelector('.seg .on') || {}).getAttribute ? row.querySelector('.seg .on').getAttribute('data-m') : 'range';
      var lo = row.querySelector('[data-lo]'), hi = row.querySelector('[data-hi]');
      var p = { mode: mode, low: lo ? +String(lo.value).replace(/[^\d.]/g, '') || 0 : it.low, high: hi ? +String(hi.value).replace(/[^\d.]/g, '') || 0 : (mode === 'fixed' ? +String(lo.value).replace(/[^\d.]/g, '') || 0 : it.high) };
      if (p.mode === 'range' && p.high && p.low > p.high) { var t = p.low; p.low = p.high; p.high = t; }
      all[id] = p;
    });
    S.a[s.id] = all;
  }
  function collectOther(s) { var o = main.querySelector('[data-other]'); if (o) S.a[s.id + '_other'] = o.value.trim(); }

  function submit(btn) {
    var c = F.contact, missing = [c.name, c.phone, c.email].filter(function (k) { return !S.a[k]; });
    if (missing.length) { err('We still need your name, phone and email. Tap Edit next to "' + (byId(F.contact.screen) ? byId(F.contact.screen).short || title(byId(F.contact.screen)) : 'contact') + '".'); return; }
    btn.disabled = true; btn.textContent = 'Sending…';
    // Sent two ways at once: our API (saves it, emails info@ the answers, sends the owner a receipt) and a backup
    // n8n workflow (saves a copy in an n8n data table, emails info@ a short note). One of them landing is enough.
    var data = body({ submit: true, summary: summaryText() }), why = [];
    var toApi = (saving || Promise.resolve()).then(function () { return post('/v1/intake', data); })
      .then(function (j) { if (j.status >= 300) throw new Error((j.errors || []).join(', ') || 'api ' + j.status); return true; });
    var toBackup = BACKUP ? fetch(BACKUP, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
      .then(function (r) { if (!r.ok) throw new Error('backup ' + r.status); return true; }) : Promise.reject(new Error('no backup'));
    var settle = function (p) { return p.catch(function (e) { why.push(e.message); return false; }); };
    Promise.all([settle(toApi), settle(toBackup)]).then(function (r) {
      if (!r[0] && !r[1]) throw new Error(why.join('; '));
      S.sent = true; S.sentVia = r; saveLocal();
      var d = ALL.filter(function (x) { return x.type === 'done'; })[0]; if (d) { S.cur = d.id; saveLocal(); render(true); window.scrollTo(0, 0); }
    }).catch(function (e) {
      btn.disabled = false; btn.textContent = 'Send my answers';
      err('That didn’t go through (' + e.message + '). Check your connection and try again. Your answers are saved on this device.');
    });
  }

  main.addEventListener('click', function (e) {
    var s = current(), t = e.target.closest('button,label.add');
    if (!t) return;
    if (t.hasAttribute('data-back')) return back();
    if (t.hasAttribute('data-edit')) { S.toReview = true; return go(byId(t.getAttribute('data-edit'))); }
    if (t.classList.contains('opt') && t.hasAttribute('data-v')) {
      var v = t.getAttribute('data-v');
      if (s.type === 'single') {
        S.a[s.id] = v; saveLocal();
        main.querySelectorAll('.opt').forEach(function (b) { b.classList.toggle('on', b === t); });
        var nb = main.querySelector('[data-next]'); if (nb) nb.disabled = false;
        var oth = main.querySelector('.other');
        if (oth) { oth.classList.toggle('on', s.other && v === s.other.v); if (s.other && v === s.other.v) { oth.querySelector('input').focus(); return; } }
        if (!s.other || v !== s.other.v) { setTimeout(function () { if (current() === s) { collectOther(s); saveDraft(); next(); } }, 260); }
        return;
      }
      if (s.type === 'multi') {
        var arr = (S.a[s.id] || (s.value || []).slice()).slice(), i = arr.indexOf(v);
        if (i > -1) arr.splice(i, 1); else arr.push(v);
        if (s.only && arr.indexOf(s.only) > -1) arr = v === s.only ? [s.only] : arr.filter(function (x) { return x !== s.only; });
        S.a[s.id] = arr; saveLocal();
        main.querySelectorAll('.opt').forEach(function (b) { b.classList.toggle('on', arr.indexOf(b.getAttribute('data-v')) > -1); });
        var o2 = main.querySelector('.other'); if (o2) o2.classList.toggle('on', s.other && arr.indexOf(s.other.v) > -1);
        var nb2 = main.querySelector('[data-next]'); if (nb2) nb2.disabled = !s.optional && !arr.length;
        return;
      }
    }
    if (t.hasAttribute('data-preset')) { S.a[s.id + '_preset'] = !val(s.id + '_preset', true); saveLocal(); return render(); }
    if (t.hasAttribute('data-rm')) {
      var list = S.files[s.id] || [], f = list[+t.getAttribute('data-rm')];
      if (f) { list.splice(list.indexOf(f), 1); saveLocal(); post('/v1/intake/file', { key: S.key, n: f.n, remove: true }).catch(function () { }); }
      return render();
    }
    if (t.hasAttribute('data-m')) {
      collectPrices(s);
      var row = t.closest('.pr'), id = row.getAttribute('data-item'), cur = S.a[s.id][id], m = t.getAttribute('data-m');
      if (m === 'range' && (!cur.high || cur.high <= cur.low)) cur.high = F.catalog[id].high || cur.low;
      cur.mode = m; saveLocal();
      var y = window.scrollY; render(); window.scrollTo(0, y);
      return;
    }
    if (t.hasAttribute('data-d')) { var h = Object.assign({}, val(s.id, s.value || { days: [1, 2, 3, 4, 5, 6], from: '08:00', to: '17:00' })), d = +t.getAttribute('data-d'); h.days = h.days.slice(); var k = h.days.indexOf(d); if (k > -1) h.days.splice(k, 1); else h.days.push(d); S.a[s.id] = h; saveLocal(); t.classList.toggle('on'); return; }
    if (t.hasAttribute('data-next')) {
      err('');
      if (s.type === 'intro') { return next(); }
      if (s.type === 'fields' && !collectFields(s)) return;
      if (s.type === 'single' || s.type === 'multi') {
        collectOther(s);
        if (s.other && S.a[s.id + '_other'] === '' && (S.a[s.id] === s.other.v || (S.a[s.id] || []).indexOf && (S.a[s.id] || []).indexOf(s.other.v) > -1)) { err('Please fill in the box, or pick another answer.'); return; }
      }
      if (s.type === 'prices') collectPrices(s);
      if (s.type === 'hours') {
        var hv = val(s.id, s.value || { days: [1, 2, 3, 4, 5, 6], from: '08:00', to: '17:00' });
        hv = Object.assign({}, hv, { from: main.querySelector('[data-h="from"]').value, to: main.querySelector('[data-h="to"]').value });
        if (!hv.days.length) { err('Pick at least one day.'); return; }
        if (hv.to <= hv.from) { err('The end time has to be after the start time.'); return; }
        S.a[s.id] = hv;
      }
      if (s.type === 'files' && s.preset && S.a[s.id + '_preset'] === undefined) S.a[s.id + '_preset'] = true;
      if (s.type === 'review') return submit(t);
      saveLocal(); saveDraft(); next();
    }
  });
  main.addEventListener('change', function (e) {
    var s = current(), el = e.target;
    if (!el.hasAttribute('data-file')) return;
    var files = Array.prototype.slice.call(el.files || []).slice(0, (s.max || 1) - (S.files[s.id] || []).length);
    if (!files.length) return;
    err('Uploading…');
    var logo = s.slot === 'logo';
    saveDraft().then(function () {
      return files.reduce(function (p, file) {
        return p.then(function () {
          var n = nextSlot(); if (!n) throw new Error('That’s the most photos we can take here.');
          return resize(file, logo ? 800 : 1600, logo && file.type === 'image/png' ? 'image/png' : 'image/jpeg').then(function (r) {
            return post('/v1/intake/file', { key: S.key, n: n, slot: logo ? 'logo' : 'photo', name: file.name.slice(0, 100), data: r.data }).then(function (j) {
              if (j.status >= 300) throw new Error('That file didn’t upload. Try a JPG or PNG.');
              (S.files[s.id] = S.files[s.id] || []).push({ n: n, thumb: r.thumb, name: file.name });
              if (logo) S.a[s.id + '_preset'] = false;
              saveLocal();
            });
          });
        });
      }, Promise.resolve());
    }).then(function () { render(); }).catch(function (x) { render(); err(x.message && x.message.length > 8 ? x.message : 'That didn’t upload. Check your connection and try again.'); });
  });
  main.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && e.target.tagName === 'INPUT') { e.preventDefault(); var b = main.querySelector('[data-next]'); if (b && !b.disabled) b.click(); }
  });
  backBtn.addEventListener('click', back);

  // ---------- frame ----------
  function render(anim) {
    var s = current();
    if (S.sent && s.type !== 'done') { var d = ALL.filter(function (x) { return x.type === 'done'; })[0]; if (d) { S.cur = d.id; s = d; } }
    main.innerHTML = (R[s.type] || R.fields)(s);
    main.classList.toggle('anim', !!anim);
    var v = visible(), inPart = v.filter(function (x) { return x.part === s.part && x.type !== 'done'; }), i = inPart.indexOf(s);
    var p = F.parts[s.part];
    partEl.textContent = s.type === 'intro' || s.type === 'done' ? '' : 'Part ' + (s.part + 1) + ' of ' + F.parts.filter(function (pp) { return pp.count !== false; }).length + ': ' + p.title;
    bar.style.width = (s.type === 'done' ? 100 : Math.max(4, Math.round(((s.part + (i + 1) / Math.max(1, inPart.length)) / F.parts.length) * 100))) + '%';
    backBtn.style.visibility = v.indexOf(s) > 0 && s.type !== 'done' ? 'visible' : 'hidden';
    var first = main.querySelector('input.in:not([type=file]),textarea.in');
    if (first && anim && s.type === 'fields' && window.innerWidth > 700) first.focus();
  }
  render(false);
})();
