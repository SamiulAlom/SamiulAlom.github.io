// Publication filters and "show all", the dock, the current-section mark, and scroll-in effects.
// The page works fully without this file (all papers show, nothing is hidden).
(function () {
  var clist = document.getElementById('clist');
  var showall = document.getElementById('showall');
  if (clist && showall && clist.querySelector('[data-more]')) {
    clist.classList.add('collapsed');
    showall.hidden = false;
    showall.addEventListener('click', function () {
      clist.classList.remove('collapsed');
      showall.hidden = true;
      var first = clist.querySelector('[data-more] a');
      if (first) first.focus({ preventScroll: true });
    });
  }

  var bar = document.querySelector('.filters');
  if (bar) {
    bar.hidden = false;
    var pubs = document.querySelectorAll('.pub');
    var status = document.querySelector('.status');
    var heads = document.querySelectorAll('#publications .sub');
    bar.addEventListener('click', function (ev) {
      var btn = ev.target.closest('button');
      if (!btn) return;
      var f = btn.getAttribute('data-f');
      bar.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
      if (f !== 'all' && clist) { clist.classList.remove('collapsed'); if (showall) showall.hidden = true; }
      var shown = 0;
      pubs.forEach(function (li) {
        var ok = f === 'all' || (f === 'first' ? li.dataset.first === '1' : li.dataset.theme === f);
        li.hidden = !ok;
        li.classList.remove('flash');
        if (ok) {
          li.style.setProperty('--i', Math.min(shown, 20));
          void li.offsetWidth; // restart the settle animation
          li.classList.add('flash');
          shown++;
        }
      });
      heads.forEach(function (h) {
        var list = h.nextElementSibling;
        var empty = !list.querySelector('.pub:not([hidden])');
        h.hidden = empty;
        list.hidden = empty;
      });
      status.textContent = f === 'all' ? '' : (shown ? shown + (shown === 1 ? ' paper' : ' papers') + ' shown' : 'No papers match this filter.');
    });
  }

  // Scroll-in: rules draw and the citation dots appear (CSS only acts on this when html.anim is set)
  var watch = document.querySelectorAll('.job, .ledger, .plot');
  if ('IntersectionObserver' in window) {
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); ro.unobserve(en.target); }
      });
    }, { threshold: 0.15 });
    watch.forEach(function (r) { ro.observe(r); });
  } else {
    watch.forEach(function (r) { r.classList.add('in'); });
  }

  var dock = document.querySelector('.dock');
  if (!dock) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hero = document.querySelector('.hero');
  var last = window.scrollY;
  function place() {
    var y = window.scrollY, past = !hero || y > hero.offsetHeight * 0.6;
    var down = y > last + 5, up = y < last - 5;
    if (!past) dock.classList.add('away');
    else if (reduce || up) dock.classList.remove('away');
    else if (down) dock.classList.add('away');
    if (down || up || !past) last = y;
  }
  dock.classList.add('away');
  window.addEventListener('scroll', place, { passive: true });
  place();

  var links = dock.querySelectorAll('a');
  var ids = ['about', 'research', 'work', 'publications', 'teaching', 'contact'];
  var secs = ids.map(function (id) { return document.getElementById(id); }).filter(Boolean);
  var ticking = false;
  function mark() {
    ticking = false;
    var mid = window.innerHeight / 2, cur = null;
    secs.forEach(function (s) {
      var r = s.getBoundingClientRect();
      if (r.top <= mid && r.bottom > mid) cur = s.id;
    });
    links.forEach(function (a) {
      if (cur && a.getAttribute('href') === '#' + cur) a.setAttribute('aria-current', 'location');
      else a.removeAttribute('aria-current');
    });
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(mark); } }, { passive: true });
  window.addEventListener('resize', mark);
  mark();
})();

// Contact buttons: the number and address are put together only when someone clicks,
// so they never appear on the page or in its source as plain text.
(function () {
  var parts = {
    wa: ['https://wa.me/', '880', '1931', '112881'],
    mail: ['mailto:', 'samiulalom090', '@', 'gmail.com']
  };
  document.querySelectorAll('[data-c]').forEach(function (a) {
    a.addEventListener('click', function (ev) {
      var p = parts[a.getAttribute('data-c')];
      if (!p) return;
      ev.preventDefault();
      var url = p.join('');
      if (a.getAttribute('data-c') === 'wa') window.open(url, '_blank', 'noopener');
      else window.location.href = url;
    });
  });
})();
