// Live hero illustration: a model explaining its predictions in real time.
// Five scenes: health records, leaf images, news text, federated training and a software request.
// Values are generated examples for illustration, never real patient or study data.
(function () {
  var host = document.getElementById('live');
  if (!host) return;
  var NS = 'http://www.w3.org/2000/svg';
  var W = 520, H = 340;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var C = { ink: '#F6F2EA', mut: '#B5AFCB', dim: '#3A3460', up: '#E8A33D', down: '#7F8CFF', hot: '#E2553B', node: '#2A2550' };

  function el(tag, attrs, parent) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }
  function txt(x, y, s, attrs, parent) {
    var a = { x: x, y: y, fill: C.mut, 'font-size': 11, 'font-family': 'IBM Plex Mono, monospace' };
    for (var k in attrs) a[k] = attrs[k];
    var t = el('text', a, parent); t.textContent = s; return t;
  }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function ease(t) { return t < 0 ? 0 : t > 1 ? 1 : 1 - Math.pow(1 - t, 3); }
  function rnd(a, b) { return a + Math.random() * (b - a); }

  var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Animated illustration: a model makes a prediction and shows which inputs drove it.' }, host.querySelector('.stage'));
  var scenes = [], current = 0, sceneStart = 0, running = true, visible = true;
  var tabs = host.querySelectorAll('.tabs button');

  /* ---------- shared: horizontal probability bars ---------- */
  function classBars(g, x, y, labels, w) {
    var rows = labels.map(function (l, i) {
      var yy = y + i * 30;
      txt(x, yy, l, { fill: C.ink }, g);
      el('rect', { x: x, y: yy + 6, width: w, height: 6, rx: 3, fill: C.dim }, g);
      var bar = el('rect', { x: x, y: yy + 6, width: 0, height: 6, rx: 3, fill: C.up }, g);
      var val = txt(x + w, yy, '0%', { 'text-anchor': 'end' }, g);
      return { bar: bar, val: val, from: 0, to: 0 };
    });
    return {
      set: function (probs) { rows.forEach(function (r, i) { r.from = r.cur || 0; r.to = probs[i]; }); },
      draw: function (t) {
        var best = 0;
        rows.forEach(function (r, i) { if (r.to > rows[best].to) best = i; });
        rows.forEach(function (r, i) {
          r.cur = lerp(r.from, r.to, ease(t));
          r.bar.setAttribute('width', (r.cur * w).toFixed(1));
          r.bar.setAttribute('fill', i === best ? C.up : '#6E668F');
          r.val.textContent = Math.round(r.cur * 100) + '%';
          r.val.setAttribute('fill', i === best ? C.ink : C.mut);
        });
      }
    };
  }

  /* ---------- scene 1: health record -> ensemble -> risk + SHAP ---------- */
  (function () {
    var g = el('g', {}, svg);
    var feats = [
      { k: 'age', unit: 'y', lo: 30, hi: 85, mean: 55, w: 0.045 },
      { k: 'glucose', unit: '', lo: 70, hi: 240, mean: 110, w: 0.012 },
      { k: 'BMI', unit: '', lo: 18, hi: 40, mean: 27, w: 0.05 },
      { k: 'hypertension', unit: '', lo: 0, hi: 1, mean: 0.3, w: 0.9, bin: true },
      { k: 'heart disease', unit: '', lo: 0, hi: 1, mean: 0.15, w: 1.1, bin: true },
      { k: 'smoking', unit: '', lo: 0, hi: 1, mean: 0.25, w: 0.6, bin: true }
    ];
    txt(18, 26, 'PATIENT RECORD', { 'font-size': 9, 'letter-spacing': 1.5 }, g);
    var rows = feats.map(function (f, i) {
      var y = 52 + i * 34;
      el('rect', { x: 16, y: y - 15, width: 150, height: 24, rx: 6, fill: C.node }, g);
      txt(26, y + 1, f.k, { fill: C.ink }, g);
      var v = txt(158, y + 1, '', { 'text-anchor': 'end', fill: C.up }, g);
      return { v: v, y: y };
    });
    var models = [{ n: 'XGB', y: 92 }, { n: 'RF', y: 152 }, { n: 'GB', y: 212 }];
    var paths = [];
    models.forEach(function (m) {
      rows.forEach(function (r) {
        var d = 'M168 ' + r.y + ' C215 ' + r.y + ' 215 ' + m.y + ' 252 ' + m.y;
        el('path', { d: d, fill: 'none', stroke: C.dim, 'stroke-width': 0.6, opacity: 0.6 }, g);
        paths.push({ d: d, row: rows.indexOf(r), m: m });
      });
      el('path', { d: 'M276 ' + m.y + ' C305 ' + m.y + ' 305 152 330 152', fill: 'none', stroke: C.dim, 'stroke-width': 1 }, g);
    });
    models.forEach(function (m) {
      el('circle', { cx: 264, cy: m.y, r: 13, fill: C.node, stroke: '#5A5282' }, g);
      txt(264, m.y + 4, m.n, { 'text-anchor': 'middle', fill: C.ink, 'font-size': 9 }, g);
    });
    el('rect', { x: 330, y: 136, width: 62, height: 32, rx: 8, fill: C.node, stroke: C.up }, g);
    txt(361, 156, 'ensemble', { 'text-anchor': 'middle', fill: C.ink, 'font-size': 9.5 }, g);
    el('path', { d: 'M392 152 L412 152', stroke: C.up, 'stroke-width': 1.2 }, g);
    // risk gauge
    var cx = 462, cy = 152, R = 40, circ = 2 * Math.PI * R;
    el('circle', { cx: cx, cy: cy, r: R, fill: 'none', stroke: C.dim, 'stroke-width': 7 }, g);
    var arc = el('circle', { cx: cx, cy: cy, r: R, fill: 'none', stroke: C.up, 'stroke-width': 7, 'stroke-linecap': 'round',
      'stroke-dasharray': circ, 'stroke-dashoffset': circ, transform: 'rotate(-90 ' + cx + ' ' + cy + ')' }, g);
    var pct = txt(cx, cy + 6, '0%', { 'text-anchor': 'middle', fill: C.ink, 'font-size': 18, 'font-family': 'Schibsted Grotesk, sans-serif', 'font-weight': 600 }, g);
    txt(cx, cy + 58, 'stroke risk', { 'text-anchor': 'middle', 'font-size': 10 }, g);
    // SHAP bars
    txt(200, 262, 'WHY: SHAP contribution per feature', { 'font-size': 9, 'letter-spacing': 1.2 }, g);
    var axis = 330;
    el('line', { x1: axis, x2: axis, y1: 270, y2: 334, stroke: '#5A5282' }, g);
    var shap = feats.map(function (f, i) {
      var y = 272 + i * 10.5;
      txt(axis - 92, y + 7, f.k, { 'font-size': 8.5, 'text-anchor': 'end', fill: C.mut, x: 236 }, g);
      return { bar: el('rect', { x: axis, y: y, width: 0, height: 7, rx: 2, fill: C.up }, g), from: 0, to: 0 };
    });
    var dots = [];
    for (var i = 0; i < 26; i++) dots.push({ c: el('circle', { r: 2.2, fill: C.up, opacity: 0 }, g), p: null, t0: 0, dur: 0 });
    var probe = el('path', { d: '', fill: 'none' }, g);
    var risk = 0, riskFrom = 0, vals = [];

    function newPatient() {
      vals = feats.map(function (f) { return f.bin ? (Math.random() < f.mean + 0.15 ? 1 : 0) : Math.round(rnd(f.lo, f.hi)); });
      var z = -1.2, contrib = feats.map(function (f, i) { var c = f.w * (vals[i] - f.mean); z += c; return c; });
      riskFrom = risk; risk = 1 / (1 + Math.exp(-z));
      var m = Math.max.apply(null, contrib.map(Math.abs)) || 1;
      shap.forEach(function (s, i) { s.from = s.cur || 0; s.to = contrib[i] / m; });
      rows.forEach(function (r, i) { var f = feats[i]; r.v.textContent = f.bin ? (vals[i] ? 'yes' : 'no') : vals[i] + f.unit; });
      dots.forEach(function (d, k) { d.p = paths[Math.floor(Math.random() * paths.length)]; d.t0 = k * 45; d.dur = rnd(700, 1100); d.sign = shap[d.p.row].to >= 0; });
    }
    scenes.push({
      g: g, name: 'Health', period: 4200,
      start: newPatient,
      tick: function (t, tAll) {
        dots.forEach(function (d) {
          var u = (t - d.t0) / d.dur;
          if (u < 0 || u > 1) { d.c.setAttribute('opacity', 0); return; }
          probe.setAttribute('d', d.p.d);
          var L = probe.getTotalLength(), pt = probe.getPointAtLength(L * ease(u));
          d.c.setAttribute('cx', pt.x); d.c.setAttribute('cy', pt.y);
          d.c.setAttribute('fill', d.sign ? C.up : C.down);
          d.c.setAttribute('opacity', (1 - Math.abs(u - .5) * 1.4).toFixed(2));
        });
        var k = ease((t - 900) / 900);
        var r = lerp(riskFrom, risk, k);
        arc.setAttribute('stroke-dashoffset', (circ * (1 - r)).toFixed(1));
        arc.setAttribute('stroke', r > .5 ? C.hot : C.up);
        pct.textContent = Math.round(r * 100) + '%';
        var ks = ease((t - 1500) / 800);
        shap.forEach(function (s) {
          s.cur = lerp(s.from, s.to, ks);
          var w = Math.abs(s.cur) * 88;
          s.bar.setAttribute('x', s.cur >= 0 ? axis : axis - w);
          s.bar.setAttribute('width', w.toFixed(1));
          s.bar.setAttribute('fill', s.cur >= 0 ? C.up : C.down);
        });
      }
    });
  })();

  /* ---------- scene 2: leaf image -> scan -> heat map + class ---------- */
  (function () {
    var g = el('g', {}, svg);
    txt(18, 26, 'LEAF IMAGE', { 'font-size': 9, 'letter-spacing': 1.5 }, g);
    var N = 16, S = 14, ox = 30, oy = 46;
    var cells = [];
    for (var r = 0; r < N; r++) for (var c = 0; c < N; c++) {
      var dx = (c - 7.5) / 7.5, dy = (r - 7.5) / 7.5;
      var leaf = (dx * dx) / 0.55 + (dy + dx * 0.25) * (dy + dx * 0.25) / 1.05 < 1;
      if (!leaf) continue;
      cells.push({ r: r, c: c, rect: el('rect', { x: ox + c * S, y: oy + r * S, width: S - 1.5, height: S - 1.5, rx: 2, fill: '#2F6B45' }, g), heat: 0 });
    }
    el('line', { x1: ox + 2, y1: oy + N * S - 2, x2: ox + N * S - 6, y2: oy + 6, stroke: '#7FB08E', 'stroke-width': 1.2, opacity: .6 }, g);
    var scan = el('rect', { x: ox - 4, y: oy, width: N * S + 8, height: 2, fill: C.up, opacity: 0 }, g);
    txt(ox, oy + N * S + 26, 'heat map over the spots the model relied on', { 'font-size': 9 }, g);
    txt(300, 70, 'PREDICTION', { 'font-size': 9, 'letter-spacing': 1.5 }, g);
    var bars = classBars(g, 300, 100, ['early blight', 'late blight', 'leaf mold', 'healthy'], 196);
    var conf = txt(300, 250, '', { 'font-size': 10 }, g);
    var spots = [];
    function newLeaf() {
      spots = [];
      var k = Math.floor(rnd(2, 4));
      for (var i = 0; i < k; i++) spots.push({ r: rnd(3, 12), c: rnd(4, 11), s: rnd(1.2, 2.2) });
      cells.forEach(function (cl) {
        var h = 0;
        spots.forEach(function (sp) { var d = Math.hypot(cl.r - sp.r, cl.c - sp.c); h = Math.max(h, Math.exp(-(d * d) / (2 * sp.s * sp.s))); });
        cl.heat = h;
        cl.rect.setAttribute('fill', h > .55 ? '#6B5A2A' : (Math.random() < .08 ? '#2A5E3D' : '#2F6B45'));
      });
      var p = [rnd(.55, .88), 0, 0, 0];
      p[1] = rnd(.04, (1 - p[0]) * .7); p[2] = rnd(0, 1 - p[0] - p[1]); p[3] = Math.max(0, 1 - p[0] - p[1] - p[2]);
      var order = [0, 1, 2]; var top = order[Math.floor(Math.random() * 3)]; var tmp = p[0]; p[0] = p[top]; p[top] = tmp;
      bars.set(p);
      conf.textContent = '';
      newLeaf.top = top; newLeaf.p = p;
    }
    scenes.push({
      g: g, name: 'Imaging', period: 4600,
      start: newLeaf,
      tick: function (t) {
        var u = (t - 200) / 1500;
        scan.setAttribute('opacity', u > 0 && u < 1 ? .9 : 0);
        var sy = oy + ease(u) * N * S;
        scan.setAttribute('y', sy);
        cells.forEach(function (cl) {
          var shown = oy + cl.r * S < sy;
          var a = shown ? cl.heat : 0;
          cl.rect.setAttribute('stroke', a > .25 ? (a > .7 ? C.hot : C.up) : 'none');
          cl.rect.setAttribute('stroke-width', a > .25 ? 1.6 : 0);
          cl.rect.setAttribute('opacity', shown || u <= 0 ? 1 : .55);
        });
        bars.draw((t - 1600) / 900);
        if (t > 2500 && !conf.textContent) conf.textContent = 'confidence ' + Math.round(newLeaf.p[newLeaf.top] * 100) + '% · TomatoNet-style CNN';
      }
    });
  })();

  /* ---------- scene 3: headline -> token attention -> category ---------- */
  (function () {
    var g = el('g', {}, svg);
    txt(18, 26, 'NEWS HEADLINE', { 'font-size': 9, 'letter-spacing': 1.5 }, g);
    var heads = [
      { w: ['Flash', 'floods', 'cut', 'off', 'villages', 'in', 'Sylhet', 'after', 'heavy', 'rain'], a: [.3, .95, .5, .2, .55, .05, .4, .1, .6, .8], p: [.86, .06, .05, .03] },
      { w: ['Parliament', 'passes', 'new', 'budget', 'amid', 'opposition', 'walkout'], a: [.85, .5, .1, .7, .15, .9, .6], p: [.04, .88, .05, .03] },
      { w: ['Garment', 'exports', 'rise', 'for', 'third', 'straight', 'month'], a: [.7, .95, .6, .05, .2, .3, .35], p: [.03, .07, .85, .05] },
      { w: ['Cyclone', 'warning', 'issued', 'for', 'coastal', 'districts'], a: [.95, .8, .3, .05, .6, .45], p: [.9, .04, .03, .03] }
    ];
    var line = el('g', {}, g);
    txt(18, 150, 'WHY: words the model weighted most', { 'font-size': 9, 'letter-spacing': 1.2 }, g);
    var bars = classBars(g, 330, 200, ['disaster', 'politics', 'business', 'sport'], 166);
    txt(330, 176, 'CATEGORY', { 'font-size': 9, 'letter-spacing': 1.5 }, g);
    var rank = el('g', {}, g);
    var toks = [], hi = 0, ranked = [];
    function newHead() {
      hi = (hi + 1) % heads.length;
      while (line.firstChild) line.removeChild(line.firstChild);
      toks = [];
      var x = 18, y = 64, h = heads[hi];
      h.w.forEach(function (w, i) {
        var t = txt(x + 6, y, w, { fill: C.ink, 'font-size': 14, 'font-family': 'Schibsted Grotesk, sans-serif', opacity: 0 }, line);
        var wd = w.length * 7.6 + 12;
        if (x + wd > 500) { x = 18; y += 40; t.setAttribute('x', x + 6); t.setAttribute('y', y); }
        var bg = el('rect', { x: x, y: y - 16, width: wd, height: 24, rx: 5, fill: C.up, opacity: 0 }, line);
        line.insertBefore(bg, t);
        var bar = el('rect', { x: x + 4, y: y + 12, width: 0, height: 3, rx: 1.5, fill: C.up }, line);
        toks.push({ t: t, bg: bg, bar: bar, a: h.a[i], wd: wd });
        x += wd + 6;
      });
      bars.set(h.p);
      while (rank.firstChild) rank.removeChild(rank.firstChild);
      ranked = toks.slice().sort(function (p, q) { return q.a - p.a; }).slice(0, 5).map(function (k, i) {
        var y = 182 + i * 28;
        txt(18, y, k.t.textContent, { fill: C.ink, 'font-size': 11 }, rank);
        el('rect', { x: 112, y: y - 8, width: 120, height: 6, rx: 3, fill: C.dim }, rank);
        return { bar: el('rect', { x: 112, y: y - 8, width: 0, height: 6, rx: 3, fill: k.a > .75 ? C.hot : C.up }, rank),
                 val: txt(240, y, '', { 'font-size': 10 }, rank), a: k.a };
      });
    }
    scenes.push({
      g: g, name: 'Language', period: 4400,
      start: newHead,
      tick: function (t) {
        toks.forEach(function (k, i) {
          var u = ease((t - i * 110) / 300);
          k.t.setAttribute('opacity', u.toFixed(2));
          var v = ease((t - 1200 - i * 60) / 500) * k.a;
          k.bg.setAttribute('opacity', (v * .45).toFixed(2));
          k.bar.setAttribute('width', ((k.wd - 8) * v).toFixed(1));
          k.bar.setAttribute('fill', k.a > .75 ? C.hot : C.up);
        });
        var kr = ease((t - 1600) / 800);
        ranked.forEach(function (r) { r.bar.setAttribute('width', (120 * r.a * kr).toFixed(1)); r.val.textContent = (r.a * kr).toFixed(2); });
        bars.draw((t - 1900) / 900);
      }
    });
  })();

  /* ---------- scene 4: federated training (hospitals keep their data) ---------- */
  (function () {
    var g = el('g', {}, svg);
    txt(18, 26, 'FEDERATED TRAINING', { 'font-size': 9, 'letter-spacing': 1.5 }, g);
    var server = { x: 410, y: 118 };
    var probe = el('path', { d: '', fill: 'none' }, g);
    var sites = ['Hospital A', 'Hospital B', 'Hospital C'].map(function (n, i) {
      var y = 62 + i * 70;
      el('rect', { x: 16, y: y - 22, width: 150, height: 52, rx: 8, fill: C.node }, g);
      txt(28, y - 4, n, { fill: C.ink }, g);
      for (var k = 0; k < 9; k++) el('circle', { cx: 32 + k * 9, cy: y + 12, r: 2.4, fill: '#6E668F' }, g);
      el('rect', { x: 124, y: y + 8, width: 32, height: 6, rx: 3, fill: C.dim }, g);
      var bar = el('rect', { x: 124, y: y + 8, width: 0, height: 6, rx: 3, fill: C.up }, g);
      var d = 'M166 ' + y + ' C260 ' + y + ' 300 ' + server.y + ' ' + (server.x - 30) + ' ' + server.y;
      el('path', { d: d, fill: 'none', stroke: C.dim, 'stroke-width': 1, 'stroke-dasharray': '3 4' }, g);
      return { y: y, bar: bar, d: d, up: el('rect', { width: 8, height: 8, rx: 2, fill: C.up, opacity: 0 }, g),
               down: el('circle', { r: 4, fill: C.down, opacity: 0 }, g) };
    });
    txt(18, 266, 'raw records stay', { 'font-size': 9 }, g); txt(18, 280, 'at each hospital', { 'font-size': 9 }, g);
    txt(236, 60, 'model updates only', { 'font-size': 9 }, g);
    var ring = el('circle', { cx: server.x, cy: server.y, r: 30, fill: C.node, stroke: C.up, 'stroke-width': 1.4 }, g);
    var pulse = el('circle', { cx: server.x, cy: server.y, r: 30, fill: 'none', stroke: C.up, opacity: 0 }, g);
    txt(server.x, server.y - 2, 'global', { 'text-anchor': 'middle', fill: C.ink, 'font-size': 10 }, g);
    txt(server.x, server.y + 11, 'model', { 'text-anchor': 'middle', fill: C.ink, 'font-size': 10 }, g);
    var rlab = txt(server.x, server.y + 50, 'round 0', { 'text-anchor': 'middle', 'font-size': 10 }, g);
    var cx0 = 236, cx1 = 500, cy0 = 330, cy1 = 256;
    txt(220, 242, 'GLOBAL AUC BY ROUND (EXAMPLE)', { 'font-size': 9, 'letter-spacing': 1.2 }, g);
    el('line', { x1: cx0, x2: cx1, y1: cy0, y2: cy0, stroke: '#5A5282' }, g);
    [0.7, 0.8, 0.9].forEach(function (v) { var yy = cy0 - (v - 0.6) / 0.35 * (cy0 - cy1); el('line', { x1: cx0, x2: cx1, y1: yy, y2: yy, stroke: C.dim, 'stroke-dasharray': '2 4' }, g); txt(cx0 - 6, yy + 3, v.toFixed(1), { 'text-anchor': 'end', 'font-size': 8 }, g); });
    var line = el('polyline', { points: '', fill: 'none', stroke: C.up, 'stroke-width': 1.8 }, g);
    var marks = []; for (var m = 0; m < 8; m++) marks.push(el('circle', { r: 2.6, fill: C.up, opacity: 0 }, g));
    var head = el('circle', { r: 3.5, fill: C.up, opacity: 0 }, g);
    var auc = txt(cx1, 242, '', { 'text-anchor': 'end', fill: C.ink, 'font-size': 10 }, g);
    var round = 0, hist = [0.66], ROUNDS = 8, speed = [1, 1, 1];
    function pt(i, v) { return [cx0 + (cx1 - cx0) * i / (ROUNDS - 1), cy0 - (v - 0.6) / 0.35 * (cy0 - cy1)]; }
    function nextRound() {
      if (round >= ROUNDS - 1) { round = 0; hist = [0.66]; }
      round++;
      speed = sites.map(function () { return rnd(0.6, 1); });
      hist.push(0.66 + 0.24 * (1 - Math.exp(-round / 2.6)) + rnd(-0.012, 0.012));
      rlab.textContent = 'round ' + round + ' of ' + (ROUNDS - 1);
    }
    function along(node, d, u, isCircle) {
      if (u <= 0 || u >= 1) { node.setAttribute('opacity', 0); return; }
      probe.setAttribute('d', d);
      var L = probe.getTotalLength(), q = probe.getPointAtLength(L * ease(u));
      if (isCircle) { node.setAttribute('cx', q.x); node.setAttribute('cy', q.y); }
      else { node.setAttribute('x', q.x - 4); node.setAttribute('y', q.y - 4); }
      node.setAttribute('opacity', 1);
    }
    scenes.push({
      g: g, name: 'Federated', period: 4000,
      start: nextRound,
      tick: function (t) {
        sites.forEach(function (s, i) {
          s.bar.setAttribute('width', (32 * ease(t / (1000 * speed[i]))).toFixed(1));
          along(s.up, s.d, (t - 1000 - i * 120) / 900, false);
          along(s.down, s.d, 1 - (t - 2700 - i * 80) / 900, true);
        });
        var pu = (t - 1950) / 600, on = pu > 0 && pu < 1;
        pulse.setAttribute('opacity', on ? (1 - pu).toFixed(2) : 0);
        pulse.setAttribute('r', (30 + Math.max(0, Math.min(1, pu)) * 22).toFixed(1));
        ring.setAttribute('stroke', on ? C.hot : C.up);
        var k = ease((t - 2000) / 700), pts = [];
        hist.forEach(function (v, i) {
          var a = pt(i, v);
          if (i === hist.length - 1 && i > 0) { var b = pt(i - 1, hist[i - 1]); a = [lerp(b[0], a[0], k), lerp(b[1], a[1], k)]; }
          pts.push(a[0].toFixed(1) + ',' + a[1].toFixed(1));
        });
        line.setAttribute('points', pts.join(' '));
        marks.forEach(function (mk, i) { if (i < pts.length - 1) { var q = pts[i].split(','); mk.setAttribute('cx', q[0]); mk.setAttribute('cy', q[1]); mk.setAttribute('opacity', 1); } else mk.setAttribute('opacity', 0); });
        var last = pts[pts.length - 1].split(',');
        head.setAttribute('cx', last[0]); head.setAttribute('cy', last[1]); head.setAttribute('opacity', 1);
        var n = hist.length;
        auc.textContent = (n > 1 ? lerp(hist[n - 2], hist[n - 1], k) : hist[0]).toFixed(3);
      }
    });
  })();

  /* ---------- scene 5: software: one request through the stack ---------- */
  (function () {
    var g = el('g', {}, svg);
    txt(18, 26, 'API ENDPOINT', { 'font-size': 9, 'letter-spacing': 1.5 }, g);
    el('rect', { x: 14, y: 38, width: 270, height: 196, rx: 8, fill: '#100E22', stroke: C.dim }, g);
    var code = [
      [['@app.post', C.up], ['("/predict")', C.ink]],
      [['def ', C.down], ['predict', C.ink], ['():', C.mut]],
      [['  img = ', C.ink], ['read', C.up], ['(request.files["leaf"])', C.mut]],
      [['  p = ', C.ink], ['model', C.up], ['(img)', C.mut]],
      [['  return ', C.down], ['{"disease": top(p),', C.ink]],
      [['          "why": ', C.ink], ['gradcam', C.up], ['(img)}', C.mut]]
    ];
    var lines = code.map(function (parts, i) {
      var y = 66 + i * 28;
      var hl = el('rect', { x: 18, y: y - 15, width: 262, height: 21, rx: 3, fill: C.up, opacity: 0 }, g);
      txt(26, y, String(i + 1), { 'font-size': 9, fill: '#5A5282' }, g);
      var t = el('text', { x: 42, y: y, 'font-size': 10.5, 'font-family': 'IBM Plex Mono, monospace' }, g);
      t.style.whiteSpace = 'pre';
      var n = 0;
      var spans = parts.map(function (pp) { n += pp[0].length; return { s: el('tspan', { fill: pp[1] }, t), txt: pp[0] }; });
      return { spans: spans, n: n, hl: hl };
    });
    var total = lines.reduce(function (a, l) { return a + l.n; }, 0), typed = false;
    function typeTo(left) {
      lines.forEach(function (l) {
        l.spans.forEach(function (sp) {
          sp.s.textContent = sp.txt.slice(0, Math.max(0, Math.min(sp.txt.length, left)));
          left -= sp.txt.length;
        });
      });
    }
    var layers = [['React app', 'browser'], ['API', 'Flask'], ['Model', 'CNN + Grad-CAM'], ['Database', 'Supabase']];
    var boxes = layers.map(function (L, i) {
      var y = 46 + i * 50;
      if (i) el('line', { x1: 411, x2: 411, y1: y - 14, y2: y, stroke: C.dim }, g);
      var r = el('rect', { x: 318, y: y, width: 186, height: 36, rx: 8, fill: C.node, stroke: '#5A5282' }, g);
      txt(332, y + 22, L[0], { fill: C.ink, 'font-size': 11.5, 'font-family': 'Schibsted Grotesk, sans-serif' }, g);
      txt(494, y + 22, L[1], { 'text-anchor': 'end', 'font-size': 9.5 }, g);
      return { r: r, y: y + 18 };
    });
    var req = el('circle', { cx: 307, r: 5, fill: C.up, opacity: 0 }, g);
    var status = txt(318, 270, '', { fill: C.ink, 'font-size': 11 }, g);
    var log = txt(18, 266, '', { 'font-size': 10 }, g);
    var log2 = txt(18, 288, '', { 'font-size': 10, fill: C.ink }, g);
    txt(18, 326, 'how my apps serve a model: request in, answer and explanation out', { 'font-size': 9 }, g);
    var res = {}, results = ['early blight', 'late blight', 'leaf mold', 'healthy'];
    function newRequest() {
      res = { ms: Math.round(rnd(48, 140)), cls: results[Math.floor(Math.random() * results.length)], p: Math.round(rnd(82, 97)) };
      status.textContent = ''; log.textContent = ''; log2.textContent = '';
    }
    scenes.push({
      g: g, name: 'Software', period: 4400,
      start: newRequest,
      tick: function (t) {
        var off = 0;
        if (!typed) { typeTo(Math.floor(total * Math.min(1, t / 1500))); if (t >= 1500) typed = true; off = 1500; }
        else typeTo(total);
        var u = t - off, y = null, active = -1;
        if (u > 0 && u < 1400) { var a = ease(u / 1400); y = lerp(boxes[0].y, boxes[3].y, a); active = Math.min(3, Math.floor(a * 3.999)); }
        else if (u >= 1400 && u < 2400) { var b = ease((u - 1400) / 1000); y = lerp(boxes[3].y, boxes[0].y, b); active = 3 - Math.min(3, Math.floor(b * 3.999)); }
        req.setAttribute('opacity', y === null ? 0 : 1);
        if (y !== null) { req.setAttribute('cy', y.toFixed(1)); req.setAttribute('fill', u < 1400 ? C.up : C.down); }
        boxes.forEach(function (bx, i) { bx.r.setAttribute('stroke', i === active ? C.up : '#5A5282'); });
        var hl = active === 0 ? 0 : active === 1 ? 2 : active === 2 ? (u < 1400 ? 3 : 5) : active === 3 ? 4 : -1;
        lines.forEach(function (l, i) { l.hl.setAttribute('opacity', i === hl ? 0.16 : 0); });
        if (u > 0 && !log.textContent) log.textContent = 'POST /predict  leaf.jpg';
        if (u > 2400 && !status.textContent) {
          status.textContent = '200 OK · ' + res.ms + ' ms';
          log2.textContent = '→ ' + res.cls + ' ' + res.p + '% + heat map';
        }
      }
    });
  })();

  /* ---------- scene control ---------- */
  var cycles = 0, picked = false;
  function show(i, now) {
    current = i; sceneStart = now; cycles = 0;
    scenes.forEach(function (s, k) { s.g.style.display = k === i ? '' : 'none'; });
    tabs.forEach(function (b, k) { b.setAttribute('aria-pressed', String(k === i)); });
    scenes[i].start();
  }
  tabs.forEach(function (b, k) {
    b.addEventListener('click', function () { picked = true; show(k, performance.now()); if (reduce) scenes[k].tick(99999, 0); });
  });

  if (reduce) { show(0, 0); scenes[0].tick(99999, 0); return; }

  var last = performance.now();
  show(0, last);
  function frame(now) {
    if (running && visible) {
      var s = scenes[current], t = now - sceneStart;
      if (t > s.period) {
        cycles++;
        if (cycles >= 2 && !picked) { show((current + 1) % scenes.length, now); }
        else { sceneStart = now; s.start(); }
      } else s.tick(t, now);
    } else sceneStart += now - last; // freeze the clock while hidden
    last = now;
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (en) { visible = en[0].isIntersecting; }).observe(host);
  }
  document.addEventListener('visibilitychange', function () { running = !document.hidden; });
})();
