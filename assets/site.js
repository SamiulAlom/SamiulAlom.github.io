// Publication filters, the dock that hides on scroll down, and the current-section mark.
// The page works fully without this file.
(function () {
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

  // Draw section rules when they scroll into view (CSS only acts on this when html.anim is set)
  var rules = document.querySelectorAll('.theme, .job, .ledger');
  if ('IntersectionObserver' in window) {
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); ro.unobserve(en.target); }
      });
    }, { threshold: 0, rootMargin: '0px 0px -12% 0px' });
    rules.forEach(function (r) { ro.observe(r); });
  } else {
    rules.forEach(function (r) { r.classList.add('in'); });
  }

  var dock = document.querySelector('.dock');
  if (!dock) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // The dock stays out of the way over the hero, then hides while reading down and returns on scroll up.
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

  // Mark the section that crosses the middle of the viewport; clear the mark above the first section.
  var links = dock.querySelectorAll('a');
  var ids = ['about', 'research', 'publications', 'work', 'teaching'];
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
