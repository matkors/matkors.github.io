/* Click-to-enlarge for case-study figures.
   Deliberately independent of GSAP: if the animation libraries fail to load,
   the images must still open. Uses <dialog> so Escape and focus handling
   come from the platform rather than from us. */
(function () {
  var dlg = document.getElementById('lb');
  if (!dlg) return;

  var img = dlg.querySelector('img');
  var cap = dlg.querySelector('.lbcap');
  var closeBtn = dlg.querySelector('.lbclose');

  var frames = [].slice.call(document.querySelectorAll('.fig .frame'));
  if (!frames.length) return;

  frames.forEach(function (frame) {
    var source = frame.querySelector('img');
    if (!source) return;

    // affordance: a small badge that fades in on hover
    var cue = document.createElement('span');
    cue.className = 'zoomcue';
    cue.innerHTML = '<span aria-hidden="true">&#9906;</span> Click to enlarge';
    frame.appendChild(cue);

    frame.setAttribute('role', 'button');
    frame.setAttribute('tabindex', '0');
    frame.setAttribute('aria-label', 'Enlarge: ' + (source.alt || 'figure'));

    function open() {
      img.src = source.currentSrc || source.src;
      img.alt = source.alt || '';
      var figure = frame.closest('figure');
      var caption = figure && figure.querySelector('figcaption');
      if (caption) {
        cap.innerHTML = caption.innerHTML;
        cap.hidden = false;
      } else {
        cap.textContent = '';
        cap.hidden = true;
      }
      if (typeof dlg.showModal === 'function') dlg.showModal();
      else dlg.setAttribute('open', '');
      document.body.style.overflow = 'hidden';
    }

    frame.addEventListener('click', open);
    frame.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
    });
  });

  function close() {
    if (typeof dlg.close === 'function') dlg.close();
    else dlg.removeAttribute('open');
  }

  closeBtn.addEventListener('click', close);

  // clicking the backdrop closes; clicking the image itself must not
  dlg.addEventListener('click', function (e) {
    if (e.target === dlg) close();
  });

  dlg.addEventListener('close', function () {
    document.body.style.overflow = '';
    img.removeAttribute('src');
  });
})();
