window.addEventListener('load', function () {
  // Fail safe: if any library did not load, the page is already fully visible.
  if (!window.gsap || !window.ScrollTrigger) return;

  gsap.registerPlugin(ScrollTrigger);
  var hasSplit = !!window.SplitText;
  if (hasSplit) gsap.registerPlugin(SplitText);

  var mm = gsap.matchMedia();

  mm.add({
    motion: '(prefers-reduced-motion: no-preference)',
    fine:   '(pointer: fine)'
  }, function (ctx) {
    var motion = ctx.conditions.motion, fine = ctx.conditions.fine;
    if (!motion) return;

    /* ---- smooth scroll, deliberately light ---- */
    if (window.Lenis) {
      var lenis = new Lenis({ autoRaf: false, anchors: true, duration: 0.85, syncTouch: false });
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
      gsap.ticker.lagSmoothing(0);
    }

    /* ---- rail ---- */
    gsap.from('.rail > *', { y: 14, autoAlpha: 0, filter: 'blur(5px)', duration: .75, stagger: .07, ease: 'power2.out', delay: .15 });

    /* ---- headline: masked per-line rise ---- */
    if (hasSplit) {
      document.fonts.ready.then(function () {
        SplitText.create('.headline', {
          type: 'lines', mask: 'lines', autoSplit: true, aria: 'auto',
          onSplit: function (self) {
            return gsap.from(self.lines, { yPercent: 115, duration: .95, stagger: .09, ease: 'power3.out' });
          }
        });
      });
    }

    /* ---- generic block reveals ---- */
    gsap.utils.toArray('[data-reveal]').forEach(function (el) {
      gsap.from(el.children, {
        y: 26, autoAlpha: 0, filter: 'blur(7px)', duration: .8, stagger: .07, ease: 'power2.out',
        scrollTrigger: { trigger: el, start: 'top 88%', once: true }
      });
    });

    /* ---- pipelines draw themselves step by step ---- */
    gsap.utils.toArray('[data-pipe]').forEach(function (pipe) {
      var tl = gsap.timeline({ scrollTrigger: { trigger: pipe, start: 'top 82%', once: true } });
      tl.from(pipe.querySelector('.flow-line'), { scaleY: 0, duration: .75, ease: 'power2.out' })
        .from(pipe.querySelectorAll('.fnode'), { scale: 0, autoAlpha: 0, duration: .35, stagger: .1, ease: 'back.out(2.2)' }, '-=.55')
        .from(pipe.querySelectorAll('.fnum, .fbody'), { x: -12, autoAlpha: 0, duration: .45, stagger: .05, ease: 'power2.out' }, '-=.8')
        .from(pipe.querySelectorAll('.flow-note'), { autoAlpha: 0, duration: .4 }, '-=.25');
    });

    /* ---- stat tiles ---- */
    gsap.utils.toArray('[data-stats]').forEach(function (grid) {
      gsap.from(grid.querySelectorAll('.stat'), {
        autoAlpha: 0, y: 18, filter: 'blur(6px)', duration: .6, stagger: .07, ease: 'power2.out',
        scrollTrigger: { trigger: grid, start: 'top 88%', once: true }
      });
    });

    /* ---- count up on real numbers only ---- */
    gsap.utils.toArray('[data-count]').forEach(function (el) {
      var end = parseFloat(el.dataset.count),
          pre = el.dataset.prefix || '', suf = el.dataset.suffix || '',
          o = { v: 0 };
      gsap.to(o, {
        v: end, duration: 1.6, ease: 'power2.out', snap: { v: 1 },
        onUpdate: function () { el.innerHTML = pre + Math.round(o.v) + suf; },
        scrollTrigger: { trigger: el, start: 'top 92%', once: true }
      });
    });

    /* ---- magnetic buttons, precise pointers only ---- */
    if (fine) {
      document.querySelectorAll('.magnetic').forEach(function (b) {
        var xTo = gsap.quickTo(b, 'x', { duration: .45, ease: 'power3' }),
            yTo = gsap.quickTo(b, 'y', { duration: .45, ease: 'power3' });
        b.addEventListener('pointermove', function (e) {
          var r = b.getBoundingClientRect();
          xTo((e.clientX - r.left - r.width / 2) * .3);
          yTo((e.clientY - r.top - r.height / 2) * .45);
        });
        b.addEventListener('pointerleave', function () { xTo(0); yTo(0); });
      });

      /* ---- aurora drifts with the cursor, very slightly ---- */
      var aur = document.querySelector('.aurora');
      if (aur) {
        var ax = gsap.quickTo(aur, 'xPercent', { duration: 1.6, ease: 'power2' }),
            ay = gsap.quickTo(aur, 'yPercent', { duration: 1.6, ease: 'power2' });
        window.addEventListener('pointermove', function (e) {
          ax((e.clientX / window.innerWidth - .5) * 6);
          ay((e.clientY / window.innerHeight - .5) * 6);
        });
      }
    }


    /* ---- scroll-spy for the case-page nav ---- */
    var toc = document.querySelector('.toc');
    if (toc) {
      var links = [].slice.call(toc.querySelectorAll('a'));
      links.forEach(function (a) {
        var id = a.getAttribute('href').slice(1);
        var target = document.getElementById(id);
        if (!target) return;
        ScrollTrigger.create({
          trigger: target, start: 'top 45%', end: 'bottom 45%',
          onToggle: function (self) {
            if (self.isActive) {
              links.forEach(function (l) { l.classList.remove('on'); });
              a.classList.add('on');
            }
          }
        });
      });
    }

    /* ---- aurora slow drift, always on when motion allowed ---- */
    gsap.to('.aurora', {
      backgroundPosition: '100% 100%', duration: 26,
      ease: 'sine.inOut', repeat: -1, yoyo: true
    });
  });
});
