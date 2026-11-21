"""Build the portfolio page (design v3) from pubs.py. Run: python -I build.py <site_dir>"""
import html, sys, pathlib
from urllib.parse import quote, urlencode
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pubs import PUBS, REPOS

SITE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "E:/Claude/portfolio-site")
SCHOLAR = "https://scholar.google.com/citations?user=aulykMwAAAAJ"
GITHUB = "https://github.com/SamiulAlom"
LINKEDIN = "https://www.linkedin.com/in/md-samiul-alom-087124227/"
SITE_URL = "https://samiulalom.github.io/"
READ = "22 Nov 2026"
CITATIONS, H_INDEX = 67, 5
# Weekly refresh (refresh_scholar.py) writes data/scholar.json; when present it overrides the counts above.
_sj = pathlib.Path(__file__).resolve().parent.parent / "data" / "scholar.json"
if _sj.exists():
    import json as _json, datetime as _dt
    _d = _json.loads(_sj.read_text(encoding="utf-8"))
    READ = _dt.date.fromisoformat(_d["read"]).strftime("%d %b %Y").lstrip("0")
    CITATIONS, H_INDEX = _d["citations"], _d["h_index"]
    PUBS = [p[:7] + (_d["cites"].get(p[0], p[7]),) + p[8:] for p in PUBS]
THEMES = ("health", "vision", "nlp")
SHOW_CONF = 8          # conference papers visible before "Show all"
e = html.escape

for p in PUBS:  # guard the data that goes into attributes
    assert p[4] in ("j", "c") and p[5] in THEMES, p[0]

REPO_BY_TITLE = {t: r for r, _d, t in REPOS if t}
BY_TITLE = {p[0]: p for p in PUBS}


def link(p):
    title, doi = p[0], p[8]
    if doi:
        return "https://doi.org/" + quote(doi, safe="/")
    return "https://scholar.google.com/scholar?" + urlencode({"q": f'"{title}"'})


def gh(repo):
    return GITHUB + "/" + quote(repo, safe="")


def cites(n):
    if not n:
        return '<span class="cites" aria-hidden="true"></span>'
    word = "citation" if n == 1 else "citations"
    return f'<span class="cites mono"><b>{n}</b> {word}</span>'


def item(p, extra=False):
    title, auth, venue, year, kind, theme, first, n, doi, q = p
    ref = f"doi:{e(doi)}" if doi else "via Scholar"
    qtag = f'<span class="q">{e(q)}</span>' if q else ""
    mark = ('<span class="fa" aria-hidden="true">&#9632;</span><span class="vh">First author: </span>'
            if first else "")
    repo = REPO_BY_TITLE.get(title)
    code = f' <a class="codelink" href="{e(gh(repo))}" rel="noopener">code</a>' if repo else ""
    au = e(auth).replace("MS Alom", '<b class="me">MS Alom</b>')
    more = ' data-more="1"' if extra else ""
    return f'''<li class="pub" data-kind="{e(kind)}" data-theme="{e(theme)}" data-first="{int(first)}"{more}>
  <span class="yr">{year}</span>
  <div class="pb">
    <a class="pt" href="{e(link(p))}" rel="noopener">{mark}{e(title)}</a>
    <span class="pa">{au}</span>
    <span class="pv"><em>{e(venue)}</em>{qtag}<span class="ref">{ref}</span>{code}</span>
  </div>
  {cites(n)}
</li>'''


def plot():
    """Every paper as a dot: x = year, y = Scholar citations. Real data, read on READ."""
    x0, x1, y0, y1 = 44, 300, 206, 22
    years = [2023, 2024, 2025, 2026]
    ymax = 12
    X = lambda yr, k, m: x0 + (years.index(yr) + 0.5) * (x1 - x0) / 4 + (k - (m - 1) / 2) * 6.2
    Y = lambda c: y0 - c * (y0 - y1) / ymax
    dots = []
    for yr in years:
        group = sorted([p for p in PUBS if p[3] == yr], key=lambda p: (p[7], p[6]))
        by_c = {}
        for p in group:
            by_c.setdefault(p[7], []).append(p)
        for c, ps in by_c.items():
            per = 9
            for k, p in enumerate(ps):
                row, col = divmod(k, per)
                m = min(per, len(ps) - row * per)
                cx, cy = X(yr, col, m), Y(c) + row * 6.2
                cls = "dot f" if p[6] else "dot"
                dots.append(f'<circle class="{cls}" style="--d:{len(dots)}" cx="{cx:.1f}" cy="{cy:.1f}" r="2.6"><title>{e(p[0])} ({yr}, {c})</title></circle>')
    grid = "".join(f'<line class="gl" x1="{x0}" x2="{x1}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/><text x="{x0-8}" y="{Y(v)+3:.1f}" text-anchor="end">{v}</text>'
                   for v in (0, 4, 8, 12))
    xt = "".join(f'<text x="{x0 + (i + .5) * (x1 - x0) / 4:.1f}" y="{y0+30}" text-anchor="middle">{yr}</text>' for i, yr in enumerate(years))
    n_first = sum(p[6] for p in PUBS)
    return f'''<svg viewBox="0 0 320 246" role="img" aria-labelledby="plotcap">
      <g class="axes">{grid}{xt}<text x="{x0-8}" y="12" text-anchor="end">cites</text></g>
      <g>{"".join(dots)}</g>
    </svg>
    <figcaption id="plotcap" class="mono">Each dot is one of the {len(PUBS)} papers, by year and Google Scholar citations ({READ}). Filled: the {n_first} I led as first author.</figcaption>'''


def shot(img, title, text, alt, href=None, cls=""):
    more = f' <a class="codelink" href="{e(href)}" rel="noopener">code</a>' if href else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<figure{c}><div class="frame"><img src="assets/work/{img}.jpg" width="1280" height="635" loading="lazy" alt="{alt}"></div>'
            f'<figcaption><b>{title}</b><span>{text}{more}</span></figcaption></figure>')


journals = [p for p in PUBS if p[4] == "j"]
confs = sorted([p for p in PUBS if p[4] == "c"], key=lambda p: (-p[7], -p[3]))
n_first = sum(p[6] for p in PUBS)
n_doi = sum(1 for p in PUBS if p[8])
qs = [p[9] for p in journals if p[9]]
quart = " ".join(f'<span class="qp">{qs.count(q)}<small>{q}</small></span>' for q in ("Q1", "Q2", "Q3") if q in qs)

THEME_TEXT = {
    "health": ("Health", "Interpretable ensemble and federated models on clinical records: stroke, heart disease, suicide risk, thyroid cancer, kidney and liver disease."),
    "vision": ("Imaging", "CNNs and vision transformers for medical scans and skin disease, plant leaf disease, and historical coins."),
    "nlp": ("Language", "Transformer classifiers, mostly for Bangla: misogyny on YouTube, disaster news, suicide triggers in headlines, sentiment and lyrics."),
}
themes = ""
for i, key in enumerate(THEMES, 1):
    name, text = THEME_TEXT[key]
    n = sum(1 for p in PUBS if p[5] == key)
    top = sorted([p for p in PUBS if p[5] == key], key=lambda p: (-p[7], -p[3]))[:3]
    lis = "".join(f'<li><a href="{e(link(p))}" rel="noopener">{e(p[0])}</a><span class="mono">{p[3]}{" &middot; " + str(p[7]) + " cit." if p[7] else ""}</span></li>' for p in top)
    themes += f'''<article class="theme" id="t-{key}">
      <p class="tn mono">0{i} <span>{n} papers</span></p>
      <h3>{name}</h3>
      <p>{text}</p>
      <ul>{lis}</ul>
    </article>'''

repos = "".join(
    f'<li><a href="{e(gh(r))}" rel="noopener"><span class="slug">{e(r)}/</span></a><span class="rd">{e(d)}</span></li>'
    for r, d, _t in REPOS)

tomato = BY_TITLE["TomatoNet-R50: A ResNet50-Based Deep Learning Architecture for the Detection of Tomato Leaf Disease"]
suicide = BY_TITLE["An Explainable Triple-Layered Ensemble Model for Early Prediction of Suicide Risk Using Machine Learning"]

S, G, L = e(SCHOLAR), e(GITHUB), e(LINKEDIN)
profiles = f'<a href="{S}" rel="noopener">Google Scholar</a><a href="{G}" rel="noopener">GitHub</a><a href="{L}" rel="noopener">LinkedIn</a><a class="cvlink" href="assets/Md-Samiul-Alom-CV.pdf" download>CV (PDF)</a>'

import json
LDJSON = json.dumps({
    "@context": "https://schema.org", "@type": "Person", "name": "Md. Samiul Alom", "url": SITE_URL,
    "image": SITE_URL + "assets/share-card.png",
    "jobTitle": ["Adjunct Research Associate", "Software Engineer and Research Assistant"],
    "worksFor": [{"@type": "Organization", "name": "Miyan Research Institute"}, {"@type": "Organization", "name": "Brilliancy Research Limited"}],
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "International University of Business Agriculture and Technology (IUBAT)"},
    "address": {"@type": "PostalAddress", "addressLocality": "Dhaka", "addressCountry": "BD"},
    "knowsAbout": ["Explainable machine learning", "Medical image analysis", "Bangla natural language processing", "Federated learning", "Web development"],
    "sameAs": [SCHOLAR, GITHUB, LINKEDIN],
}, ensure_ascii=False).replace("</", "<\\/")

conf_items = "".join(item(p, extra=(i >= SHOW_CONF)) for i, p in enumerate(confs))

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Md. Samiul Alom</title>
<meta name="description" content="Md. Samiul Alom, researcher and software engineer in Dhaka. Explainable machine learning for health records, medical and plant images and Bangla text; {len(PUBS)} published papers; software in daily use.">
<meta property="og:title" content="Md. Samiul Alom">
<meta property="og:description" content="Explainable models, built into working software.">
<meta property="og:type" content="profile">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:image" content="{SITE_URL}assets/share-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Md. Samiul Alom: Explainable models, built into working software.">
<meta property="og:site_name" content="Md. Samiul Alom">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Md. Samiul Alom">
<meta name="twitter:description" content="Explainable models, built into working software. {len(PUBS)} papers on health records, medical and plant images and Bangla text.">
<meta name="twitter:image" content="{SITE_URL}assets/share-card.png">
<script type="application/ld+json">{LDJSON}</script>
<link rel="canonical" href="{SITE_URL}">
<meta name="theme-color" content="#15122A">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400;1,6..72,500&family=Schibsted+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<script>if(!matchMedia("(prefers-reduced-motion: reduce)").matches)document.documentElement.classList.add("anim")</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="hero" id="top">
  <div class="hero-in">
    <p class="kicker mono">Md. Samiul Alom &middot; Dhaka</p>
    <h1><span class="ln"><span>Explainable models,</span></span> <span class="ln"><span>built into <em>working</em> software.</span></span></h1>
    <p class="lede">I train machine-learning models for health records, medical and plant images, and Bangla text, and show what drives each prediction. I also build the web software a research company runs on every day.</p>
    <ul class="pills mono" aria-label="Jump to">
      <li><a href="#work">Projects</a></li><li><a href="#research">Research</a></li><li><a href="#publications">{len(PUBS)} papers</a></li>
    </ul>
    <p class="hero-links">{profiles}</p>
  </div>
  <figure class="hero-media live" id="live">
    <div class="chrome"><i aria-hidden="true"></i><i aria-hidden="true"></i><i aria-hidden="true"></i><span class="mono"><b class="pulse" aria-hidden="true"></b>explain() &middot; live</span>
      <div class="tabs mono" role="group" aria-label="Choose an example"><button type="button" aria-pressed="true">Health</button><button type="button" aria-pressed="false">Imaging</button><button type="button" aria-pressed="false">Language</button></div>
    </div>
    <div class="stage"></div>
    <figcaption class="mono">How my models explain a prediction. Illustration with generated example values, not real patient or study data.</figcaption>
  </figure>
</header>

<main id="main">

<section class="panel first" id="record" aria-labelledby="h-record">
  <div class="col">
    <h2 id="h-record" class="vh">Record</h2>
    <dl class="ledger">
      <div><dt>Citations</dt><dd>{CITATIONS}</dd></div>
      <div><dt>h-index</dt><dd>{H_INDEX}</dd></div>
      <div><dt>Published papers</dt><dd>{len(PUBS)}<span class="sub2 mono">{len(journals)} journal &middot; {len(confs)} conference &middot; {n_first} first-author</span></dd></div>
      <div><dt>Journal quartiles</dt><dd class="qd">{quart}</dd></div>
    </dl>
    <p class="src mono">Citations and h-index from Google Scholar, read {READ}. Quartiles: SJR, as shown on the Scholar profile.</p>
    <figure class="plot">{plot()}</figure>
  </div>
</section>

<section class="panel" id="about" aria-labelledby="h-about">
  <div class="col two">
    <h2 id="h-about">About</h2>
    <div>
      <p class="prose">I finished a B.Sc. in Computer Science and Engineering at IUBAT in January 2026 (CGPA 3.74/4.00). My thesis, an explainable three-layer ensemble for early suicide-risk prediction, was published in <em>Engineering Reports</em>. Since February 2026 I have been an Adjunct Research Associate at Miyan Research Institute, working with more than eight faculty members on experiments, model evaluation and manuscripts. In October 2026 I joined Brilliancy Research in Dhaka as a software engineer and research assistant.</p>
      <p class="prose">In my clinical, imaging and language work I pair each prediction with a feature-attribution view (SHAP or LIME) so the user can see which inputs drove it. I use ensembles, CNNs, vision transformers and federated learning, and I build the software around the models in React, TypeScript, Flask and Django.</p>
    </div>
  </div>
</section>

<section class="panel" id="research" aria-labelledby="h-research">
  <div class="col">
    <h2 id="h-research">Research</h2>
    <div class="themes">{themes}</div>
  </div>
</section>

<section class="band" id="paper-to-tool" aria-labelledby="h-ptt">
  <div class="col">
    <p class="eyebrow mono">From paper to tool</p>
    <h2 id="h-ptt">Two papers I turned into <em>something you can run.</em></h2>
    <div class="chains">
      <article class="chain">
        <ol class="steps mono"><li><span>01</span> Method</li><li><span>02</span> Proof</li><li><span>03</span> Tool</li></ol>
        <p><b>TomatoNet-R50</b>, a ResNet50 model for tomato leaf disease, published at <a href="{e(link(tomato))}" rel="noopener">IEEE QPAIN 2026</a>.</p>
        <p>It now runs inside <b>Krishi Sahayak</b>, a Bangla farming assistant: a farmer photographs a leaf and the app names the disease. <a href="{e(gh('agri_AI'))}" rel="noopener">Code</a></p>
        <div class="frame dark"><img src="assets/work/krishi-sahayak.jpg" width="1280" height="635" loading="lazy" alt="Krishi Sahayak home page with a plant photo banner and AI service cards."></div>
      </article>
      <article class="chain">
        <ol class="steps mono"><li><span>01</span> Method</li><li><span>02</span> Proof</li><li><span>03</span> Tool</li></ol>
        <p><b>A three-layer explainable ensemble</b> for early suicide-risk prediction, my thesis, published in <a href="{e(link(suicide))}" rel="noopener"><em>Engineering Reports</em></a> (Wiley, Q2).</p>
        <p>The full pipeline, including the SHAP and LIME explanations, is a public notebook with its data files. <a href="{e(gh('Suicide-prediction'))}" rel="noopener">Code</a></p>
        <div class="metric mono"><span>{suicide[7]}</span> citation &middot; first author &middot; doi:{e(suicide[8])}</div>
      </article>
    </div>
  </div>
</section>

<section class="panel" id="work" aria-labelledby="h-work">
  <div class="col">
    <h2 id="h-work">Projects</h2>
    <div class="job">
      <h3>Brilliancy Research Limited <span class="mono cnt">Software Engineer and Research Assistant &middot; Oct 2026&ndash;</span></h3>
      <p class="prose">I build and maintain the company&rsquo;s own software, used every day by staff and clients. React, TypeScript, Supabase and Cloudflare.</p>
      <div class="shots">
        {shot("research-desk", "Research Desk", "Managers assign tasks to research assistants, who post what they did each day; dashboards show who is on track. Shown with demo data.", "Research Desk dashboard: task counts, tasks by status, tasks waiting to be assigned and today&rsquo;s work updates.", cls="featured")}
        {shot("accounts", "Accounts and CRM", "Clients, quotes, invoices in Taka, bKash, Nagad and bank payments, and double-entry books with cash-flow reports. Shown with demo data; names blurred.", "Accounts dashboard: cash, money owed, invoices, profit, a six-month chart and a cash forecast. Names blurred.")}
        {shot("appointment", "Appointment booking", "Clients choose a service, a meeting type and a time; the booking goes into Google Calendar with an email confirmation.", "Booking page of the appointment system: consultation services with durations.")}
        {shot("classroom", "Brilliancy Classroom", "Portal for IELTS and research classes: admin and student sides, class tasks, grading, attendance and reminders.", "Sign-in screen of Brilliancy Classroom.")}
        {shot("attendance", "Attendance system", "Office check-in and check-out for staff, with weekly to yearly reports and CSV export.", "Sign-in screen of the employee attendance portal.")}
      </div>
    </div>
    <div class="job">
      <h3>Own projects</h3>
      <div class="shots">
        {shot("ielts", "IELTS 7.5 Lab", "IELTS Academic study app: English&ndash;Bangla vocabulary with spaced repetition, quizzes, reading, writing and speaking practice. Next.js and TypeScript.", "IELTS 7.5 Lab dashboard with study streak, words learned and today&rsquo;s plan.", cls="featured")}
        {shot("daymark", "Daymark", "Private workspace for research reading, IELTS practice, daily plans, a journal and focus timers. No account; data stays on the device.", "Daymark overview: focus goal, research items and today&rsquo;s plan.", "https://github.com/SamiulAlom/Daily_activity_track")}
        {shot("agroai", "Krishi-AI Sahakari", "Farming platform with crop-disease detection, an AI chatbot, a farmers&rsquo; forum and finance tools. Django.", "Krishi-AI Sahakari home page with a crop field banner and service cards.", "https://github.com/SamiulAlom/AgroAI_Project")}
      </div>
      <ul class="sys">
        <li><b>Book Shop</b> <span>Responsive bookshop front end. HTML and CSS.</span> <a href="https://samiulalom.github.io/Book_Shop/" rel="noopener">live demo</a></li>
        <li><b>Nisis quiz app</b> <span>Quiz application with React and Redux Toolkit.</span> <a href="https://github.com/SamiulAlom/ninish-project" rel="noopener">code</a></li>
        <li><b>Chat application</b> <span>Real-time chat web app. JavaScript.</span> <a href="https://github.com/SamiulAlom/Chat-Application" rel="noopener">code</a></li>
        <li><b>Library management</b> <span>Desktop library system. C#.</span> <a href="https://github.com/SamiulAlom/Library-management" rel="noopener">code</a></li>
      </ul>
    </div>
    <div class="job">
      <h3>Research code <span class="mono cnt">public on GitHub</span></h3>
      <p class="prose">Notebooks and code for eight published papers, also linked from their entries in the <a href="#publications">publication list</a>.</p>
      <ul class="dir mono">{repos}</ul>
    </div>
  </div>
</section>

<section class="panel" id="publications" aria-labelledby="h-pubs">
  <div class="col">
    <h2 id="h-pubs">Publications</h2>
    <p class="note mono"><span class="fa" aria-hidden="true">&#9632;</span> first author &middot; citations from Google Scholar, {READ} &middot; {n_doi} of {len(PUBS)} link to a DOI, the rest to Scholar</p>
    <div class="filters mono" role="group" aria-label="Filter publications" hidden>
      <button type="button" data-f="all" aria-pressed="true">All</button>
      <button type="button" data-f="first" aria-pressed="false">First author</button>
      <button type="button" data-f="health" aria-pressed="false">Health</button>
      <button type="button" data-f="vision" aria-pressed="false">Imaging</button>
      <button type="button" data-f="nlp" aria-pressed="false">Language</button>
    </div>
    <p class="status mono" role="status" aria-live="polite"></p>
    <h3 class="sub">Journal articles</h3>
    <ol class="biblio" id="jlist">{"".join(item(p) for p in journals)}</ol>
    <h3 class="sub">Conference papers <span class="mono cnt">most cited first</span></h3>
    <ol class="biblio" id="clist">{conf_items}</ol>
    <button type="button" class="more mono" id="showall" hidden>Show all {len(confs)} conference papers</button>
  </div>
</section>

<section class="panel" id="teaching" aria-labelledby="h-teach">
  <div class="col">
    <h2 id="h-teach">Teaching and service</h2>
    <ul class="cv">
      <li><span class="num mono">53<small>students</small></span><div><b>Student mentor</b>, Advanced Web Development and AI, IUBAT <span class="when mono">2024</span><br>A practical course; C/C++ mentoring in Fall 2024.</div></li>
      <li><span class="num mono">30<small>students</small></span><div><b>Student mentor</b>, Web Development and Design, IUBAT <span class="when mono">2023</span></div></li>
      <li><span class="num mono">350+<small>attendees</small></span><div><b>Seminar</b>, &ldquo;From Idea to Impact: A Complete Research Journey in AI, Publishing, and Innovation&rdquo;, IUBAT<br>Ninety minutes on research method and publishing, for students and faculty.</div></li>
      <li><span class="num mono">250+<small>students</small></span><div><b>Microsoft Learn Student Ambassador</b> (Beta) <span class="when mono">2023&ndash;2025</span><br>Four international online events on Azure, Git/GitHub, web hosting and Microsoft 365, and a 45-minute talk on international student opportunities.</div></li>
      <li><span class="num mono">2023&ndash;25</span><div><b>Postman Student Leader</b>, Postman</div></li>
      <li><span class="num mono">2024&ndash;25</span><div><b>Executive member</b>, Hult Prize at IUBAT; <b>academic mentor</b>, IUBAT IT Society</div></li>
      <li><span class="num mono">IEEE</span><div><b>Student chapter advisor</b>, IUBAT IEEE Computer Society; IEEE and IEEE Computer Society member</div></li>
    </ul>
  </div>
</section>

</main>

<footer class="foot" id="contact">
  <div class="col">
    <p class="eyebrow mono">Contact</p>
    <h2>Let&rsquo;s work on something <em>together.</em></h2>
    <p class="lead">Research collaboration, a software project or a question about my papers: message me on WhatsApp or send an email.</p>
    <div class="contact">
      <a class="btn wa" href="#contact" data-c="wa" rel="noopener">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.6.3-.2.2-.8.8-.8 2s.8 2.3 1 2.5c.1.2 1.7 2.6 4.1 3.6 1.5.7 2.1.7 2.9.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.3-.2Z"/></svg>
        <span><b>WhatsApp me</b><span>Opens a chat</span></span>
      </a>
      <a class="btn mail" href="#contact" data-c="mail">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.7" d="M3.5 6.5h17v11h-17z M3.5 7l8.5 6.5L20.5 7"/></svg>
        <span><b>Email me</b><span>Opens your mail app</span></span>
      </a>
    </div>
    <p class="hero-links">{profiles}</p>
    <p class="mono small">Dhaka, Bangladesh &middot; Figures checked {READ}</p>
  </div>
</footer>

<nav class="dock mono" aria-label="Sections">
  <a href="#about">About</a><a href="#research">Research</a><a href="#work">Projects</a><a href="#publications">Papers</a><a class="cta" href="#contact">Contact</a>
</nav>

<script src="assets/site.js" defer></script>
<script src="assets/live.js" defer></script>
</body>
</html>
'''
SITE.mkdir(parents=True, exist_ok=True)
(SITE / "index.html").write_text(page, encoding="utf-8")
print("wrote", SITE / "index.html", len(PUBS), "pubs,", n_doi, "with DOI")
