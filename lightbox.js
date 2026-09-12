/* Click-to-enlarge for case-study figures.

   Deliberately independent of GSAP: if the animation libraries fail to
   load, the images must still open. Uses <dialog> so Escape and focus
   handling come from the platform rather than from us.

   On touch the image opens fitted to the screen, so you see the whole
   workflow first. Tapping it switches to a readable size you can drag
   around. Opening straight into the zoomed view showed about a tenth of
   a 1800px-wide diagram, which is worse than not zooming at all. */
(function () {
  var dlg = document.getElementById('lb');
  if (!dlg) return;

  var coarse = !!(window.matchMedia && window.matchMedia('(pointer: coarse)').matches);
  var scroller = dlg.querySelector('.lbscroll');
  var img = dlg.querySelector('img');
  var cap = dlg.querySelector('.lbcap');
  var closeBtn = dlg.querySelector('.lbclose');
  var capHTML = '';

  var frames = [].slice.call(document.querySelectorAll('.fig .frame'));
  if (!frames.length) return;

  frames.forEach(function (frame) {
    var source = frame.querySelector('img');
    if (!source) return;

    var cue = document.createElement('span');
    cue.className = 'zoomcue';
    cue.innerHTML = '<span aria-hidden="true">&#9906;</span> '
                  + (coarse ? 'Tap to enlarge' : 'Click to enlarge');
    frame.appendChild(cue);

    frame.setAttribute('role', 'button');
    frame.setAttribute('tabindex', '0');
    frame.setAttribute('aria-label', 'Enlarge: ' + (source.alt || 'figure'));

    function open() {
      img.src = source.currentSrc || source.src;
      img.alt = source.alt || '';

      var figure = frame.closest('figure');
      var caption = figure && figure.querySelector('figcaption');
      capHTML = caption ? caption.innerHTML : '';

      dlg.classList.remove('zoomed');
      if (typeof dlg.showModal === 'function') dlg.showModal();
      else dlg.setAttribute('open', '');
      document.body.style.overflow = 'hidden';
      paint();
    }

    frame.addEventListener('click', open);
    frame.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
    });
  });

  /* the caption doubles as the instruction, so it only ever says one thing */
  function paint() {
    var hint = '';
    if (coarse) {
      hint = dlg.classList.contains('zoomed')
        ? 'Drag to explore &middot; tap image to fit'
        : 'Tap image to zoom in';
    }
    cap.innerHTML = hint
      ? '<span class="lbhint">' + hint + '</span>' + (capHTML ? ' ' + capHTML : '')
      : capHTML;
    cap.hidden = !cap.innerHTML;
  }

  if (coarse) {
    img.addEventListener('click', function (e) {
      e.stopPropagation();
      dlg.classList.toggle('zoomed');
      if (scroller) scroller.scrollLeft = 0;
      paint();
    });
  }

  function close() {
    if (typeof dlg.close === 'function') dlg.close();
    else dlg.removeAttribute('open');
  }

  closeBtn.addEventListener('click', close);

  /* clicking the backdrop closes; clicking the image itself must not */
  dlg.addEventListener('click', function (e) {
    if (e.target === dlg || e.target === dlg.firstElementChild) close();
  });

  dlg.addEventListener('close', function () {
    document.body.style.overflow = '';
    dlg.classList.remove('zoomed');
    img.removeAttribute('src');
  });
})();
