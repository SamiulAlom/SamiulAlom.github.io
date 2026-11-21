"""Build the portfolio page from pubs.py. Run: python -I build.py <site_dir>"""
import html, sys, pathlib
from urllib.parse import quote, urlencode
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pubs import PUBS, REPOS

SITE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "E:/Claude/portfolio-site")
SCHOLAR = "https://scholar.google.com/citations?user=aulykMwAAAAJ"
GITHUB = "https://github.com/SamiulAlom"
LINKEDIN = "https://www.linkedin.com/in/md-samiul-alom-087124227/"
READ = "22 Nov 2026"
THEMES = ("health", "vision", "nlp")
e = html.escape

for p in PUBS:  # guard the data that goes into attributes
    assert p[4] in ("j", "c") and p[5] in THEMES, p[0]

REPO_BY_TITLE = {t: r for r, _d, t in REPOS if t}


def link(p):
    title, doi = p[0], p[8]
    if doi:
        return "https://doi.org/" + quote(doi, safe="/")
    return "https://scholar.google.com/scholar?" + urlencode({"q": f'"{title}"'})


def cites(n):
    if not n:
        return '<span class="cites" aria-hidden="true"></span>'
    word = "citation" if n == 1 else "citations"
    return f'<span class="cites mono"><b>{n}</b> {word}</span>'


def item(p):
    title, auth, venue, year, kind, theme, first, n, doi, q = p
    ref = f"doi:{e(doi)}" if doi else "via Scholar"
    qtag = f'<span class="q">{e(q)}</span>' if q else ""
    mark = ('<span class="fa" aria-hidden="true">&#9632;</span><span class="vh">First author: </span>'
            if first else "")
    repo = REPO_BY_TITLE.get(title)
    code = (f' <a class="codelink" href="{e(GITHUB + "/" + quote(repo, safe=""))}" rel="noopener">code</a>'
            if repo else "")
    au = e(auth).replace("MS Alom", '<b class="me">MS Alom</b>')
    return f'''<li class="pub" data-kind="{e(kind)}" data-theme="{e(theme)}" data-first="{int(first)}">
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
        # papers with the same citation count are spread sideways so none hides another
        by_c = {}
        for p in group:
            by_c.setdefault(p[7], []).append(p)
        for c, ps in by_c.items():
            per = 9  # dots per row; papers with equal citations wrap onto extra rows below the value line
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
    <figcaption id="plotcap" class="mono">All {len(PUBS)} papers by year and Google Scholar citations, read {READ}. Filled dots: the {n_first} I led as first author. Papers with equal counts sit side by side; uncited ones stack under the zero line.</figcaption>'''


def shot(img, title, text, alt, href=None):
    more = f' <a class="codelink" href="{e(href)}" rel="noopener">code</a>' if href else ""
    return (f'<figure><img src="assets/work/{img}.jpg" width="1280" height="635" loading="lazy" alt="{alt}">'
            f'<figcaption><b>{title}.</b> {text}{more}</figcaption></figure>')


journals = [p for p in PUBS if p[4] == "j"]
confs = sorted([p for p in PUBS if p[4] == "c"], key=lambda p: (-p[3], -p[7]))
n_first = sum(p[6] for p in PUBS)
n_doi = sum(1 for p in PUBS if p[8])
qs = [p[9] for p in journals if p[9]]
quart = " ".join(f'{qs.count(q)} <small>{q}</small>' for q in ("Q1", "Q2", "Q3") if q in qs)

theme_html = {}
for key in THEMES:
    rows = sorted([p for p in PUBS if p[5] == key], key=lambda p: -p[7])[:4]
    theme_html[key] = "".join(f'<li><a href="{e(link(p))}" rel="noopener">{e(p[0])}</a> <span class="mono">{p[3]}</span></li>' for p in rows)
    theme_html[key + "_n"] = sum(1 for p in PUBS if p[5] == key)

repos = "".join(
    f'<li><a href="{e(GITHUB + "/" + quote(r, safe=""))}" rel="noopener"><span class="slug">{e(r)}/</span></a><span class="rd">{e(d)}</span></li>'
    for r, d, _t in REPOS)

S, G, L = e(SCHOLAR), e(GITHUB), e(LINKEDIN)
profiles = f'<a href="{S}" rel="noopener">Google Scholar</a><a href="{G}" rel="noopener">GitHub</a><a href="{L}" rel="noopener">LinkedIn</a>'

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Md. Samiul Alom</title>
<meta name="description" content="Md. Samiul Alom, researcher and software engineer in Dhaka. Explainable machine learning for clinical prediction, medical imaging and Bangla text; {len(PUBS)} published papers.">
<meta property="og:title" content="Md. Samiul Alom">
<meta property="og:description" content="Explainable machine learning for clinical prediction, medical imaging and Bangla text.">
<meta property="og:type" content="profile">
<meta property="og:url" content="https://samiulalom.github.io/">
<link rel="canonical" href="https://samiulalom.github.io/">
<meta name="theme-color" content="#15122A">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400;1,6..72,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<script>if(!matchMedia("(prefers-reduced-motion: reduce)").matches)document.documentElement.classList.add("anim")</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="hero" id="top">
  <div class="hero-in">
    <p class="kicker mono">Md. Samiul Alom <span>Dhaka</span></p>
    <h1><span class="ln"><span>Machine learning</span></span> <span class="ln"><span>you can <em>check</em>.</span></span></h1>
    <p class="lede">I build interpretable models for clinical prediction, medical imaging and Bangla text, and the software that puts tools in people&rsquo;s hands. Adjunct Research Associate at Miyan Research Institute; Software Engineer and Research Assistant at Brilliancy Research.</p>
    <ul class="pills mono" aria-label="Research areas">
      <li><a href="#t-health">Health</a></li><li><a href="#t-vision">Imaging</a></li><li><a href="#t-nlp">Language</a></li><li><a href="#work">Projects</a></li>
    </ul>
    <p class="hero-links">{profiles}</p>
  </div>
  <figure class="plot">
    {plot()}
  </figure>
</header>

<main id="main">

<section class="panel first" id="record" aria-labelledby="h-record">
  <div class="col">
    <h2 id="h-record" class="vh">Record</h2>
    <dl class="ledger">
      <div><dt>Citations</dt><dd>67 <span class="src mono">Google Scholar, read {READ}</span></dd></div>
      <div><dt>h-index</dt><dd>5 <span class="src mono">Google Scholar, read {READ}</span></dd></div>
      <div><dt>Published papers</dt><dd>{len(PUBS)} <span class="src mono">{len(journals)} journal, {len(confs)} conference; {n_first} as first author</span></dd></div>
      <div><dt>Journal quartiles</dt><dd class="qd">{quart} <span class="src mono">SJR quartiles shown on the Scholar profile, read {READ}</span></dd></div>
    </dl>
  </div>
</section>

<section class="panel" id="about" aria-labelledby="h-about">
  <div class="col">
    <h2 id="h-about">About</h2>
    <p class="prose">I finished a B.Sc. in Computer Science and Engineering at IUBAT in January 2026 (CGPA 3.74/4.00). My thesis, an explainable three-layer ensemble for early suicide-risk prediction, was published in <em>Engineering Reports</em>. Since February 2026 I have been an Adjunct Research Associate at Miyan Research Institute, working with more than eight faculty members on experiments, model evaluation and manuscripts. In October 2026 I joined Brilliancy Research in Dhaka as a software engineer and research assistant.</p>
    <p class="prose">Across clinical records, scans and Bangla text, I want a model&rsquo;s prediction to come with a reason the user can check. I use ensembles, CNNs, vision transformers and federated learning, with SHAP, LIME and Grad-CAM to show what drives each decision. My current work is on calibration, uncertainty and domain shift in medical imaging.</p>
  </div>
</section>

<section class="panel" id="research" aria-labelledby="h-research">
  <div class="col">
    <h2 id="h-research">Research</h2>
    <div class="theme" id="t-health">
      <h3>Health <span class="mono cnt">{theme_html["health_n"]} papers</span></h3>
      <p>Interpretable ensemble and federated models on clinical records (stroke, heart disease, suicide risk, thyroid cancer recurrence, kidney and liver disease), and one blockchain system against counterfeit medicines.</p>
      <ul>{theme_html["health"]}</ul>
    </div>
    <div class="theme" id="t-vision">
      <h3>Imaging <span class="mono cnt">{theme_html["vision_n"]} papers</span></h3>
      <p>CNNs, vision transformers and encoder-decoder networks for medical scans, skin disease, plant leaf disease and historical coins.</p>
      <ul>{theme_html["vision"]}</ul>
    </div>
    <div class="theme" id="t-nlp">
      <h3>Language <span class="mono cnt">{theme_html["nlp_n"]} papers</span></h3>
      <p>Transformer classifiers, mostly for Bangla: misogyny on YouTube, disaster news, suicide triggers in headlines, sentiment and song lyrics; also app reviews and data-breach stories.</p>
      <ul>{theme_html["nlp"]}</ul>
    </div>
  </div>
</section>

<section class="panel" id="publications" aria-labelledby="h-pubs">
  <div class="col">
    <h2 id="h-pubs">Publications</h2>
    <p class="note mono"><span class="fa" aria-hidden="true">&#9632;</span> first author &middot; citation counts from Google Scholar, {READ} &middot; {n_doi} of {len(PUBS)} link to a DOI, the rest to Scholar</p>
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
    <h3 class="sub">Conference papers</h3>
    <ol class="biblio dense" id="clist">{"".join(item(p) for p in confs)}</ol>
  </div>
</section>

<section class="panel" id="work" aria-labelledby="h-work">
  <div class="col">
    <h2 id="h-work">Projects</h2>
    <p class="prose">Software I have designed and built, for my employer, for other students and for myself.</p>

    <div class="job">
      <h3>Brilliancy Research Limited <span class="mono cnt">Software Engineer and Research Assistant &middot; Oct 2026&ndash;</span></h3>
      <p class="prose">I build and maintain the company&rsquo;s own software, used every day by staff and clients. React, TypeScript, Supabase and Cloudflare.</p>
      <div class="shots">
        {shot("appointment", "Appointment booking", "Clients choose a service, a meeting type and a time; the booking goes into Google Calendar and both sides get an email confirmation.", "Booking page of the appointment system: consultation services with durations and the steps to choose a meeting.")}
        {shot("research-desk", "Research Desk", "Managers assign tasks to research assistants, who post what they did each day; dashboards show who is on track.", "Research Desk dashboard: task counts, tasks by status, tasks waiting to be assigned and today&rsquo;s work updates.")}
        {shot("accounts", "Accounts and CRM", "Clients, quotes, invoices in Taka, bKash, Nagad and bank payments, and double-entry books with cash-flow reports.", "Accounts dashboard: cash, money owed, invoices, profit, a six-month chart and a cash forecast.")}
        {shot("classroom", "Brilliancy Classroom", "A portal for IELTS and research classes, with admin and student sides, class tasks, grading, attendance and reminder emails.", "Sign-in screen of Brilliancy Classroom.")}
        {shot("attendance", "Attendance system", "Office check-in and check-out for staff, with weekly to yearly reports and CSV export.", "Sign-in screen of the employee attendance portal.")}
      </div>
    </div>

    <div class="job">
      <h3>Own projects</h3>
      <div class="shots">
        {shot("ielts", "IELTS 7.5 Lab", "An IELTS Academic study app: English&ndash;Bangla vocabulary with spaced repetition, quizzes, reading, writing and speaking practice, and progress tracking. Next.js and TypeScript.", "IELTS 7.5 Lab dashboard with study streak, words learned, words due for review and today&rsquo;s study plan.")}
        {shot("daymark", "Daymark", "A private workspace for research reading, IELTS practice, daily plans, a journal and focus timers. Runs in the browser with no account; data never leaves the device.", "Daymark overview: focus goal, research items, IELTS practice minutes and today&rsquo;s plan.", "https://github.com/SamiulAlom/Daily_activity_track")}
        {shot("krishi-sahayak", "Krishi Sahayak", "A Bangla farming assistant: farmers photograph a leaf and the TomatoNet-R50 model from my QPAIN 2026 paper names the disease; a chatbot answers follow-up questions. Flask.", "Krishi Sahayak home page in Bangla with a plant photo banner and AI service cards.", "https://github.com/SamiulAlom/agri_AI")}
        {shot("agroai", "Krishi-AI Sahakari", "A Bangla farming platform with crop-disease detection, an AI chatbot, a farmers&rsquo; forum and finance tools. Django.", "Krishi-AI Sahakari home page in Bangla with a crop field banner and service cards.", "https://github.com/SamiulAlom/AgroAI_Project")}
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
      <p class="prose">Notebooks and data behind published papers. Links also sit next to each paper above.</p>
      <ul class="dir mono">{repos}</ul>
    </div>
  </div>
</section>

<section class="panel" id="teaching" aria-labelledby="h-teach">
  <div class="col">
    <h2 id="h-teach">Teaching and service</h2>
    <ul class="cv">
      <li><span class="num mono">53<small>students</small></span><div><b>Web development mentor</b>, Advanced Web Development and AI, IUBAT <span class="when mono">2024</span><br>A practical course; C/C++ mentoring in Fall 2024.</div></li>
      <li><span class="num mono">30<small>students</small></span><div><b>Web development mentor</b>, Web Development and Design, IUBAT <span class="when mono">2023</span></div></li>
      <li><span class="num mono">350+<small>attendees</small></span><div><b>Seminar</b>, &ldquo;From Idea to Impact: A Complete Research Journey in AI, Publishing, and Innovation&rdquo;, IUBAT<br>Ninety minutes on research method and publishing, for students and faculty.</div></li>
      <li><span class="num mono">250+<small>students</small></span><div><b>Microsoft Learn Student Ambassador</b> (Beta) <span class="when mono">2023&ndash;2025</span><br>Four international online events on Azure, Git/GitHub, web hosting and Microsoft 365, and a 45-minute talk on international student opportunities.</div></li>
      <li><span class="num mono">2023&ndash;25</span><div><b>Postman Student Leader</b>, Postman</div></li>
      <li><span class="num mono">2024&ndash;25</span><div><b>Executive member</b>, Hult Prize at IUBAT; <b>academic mentor</b>, IUBAT IT Society</div></li>
      <li><span class="num mono">IEEE</span><div><b>Advisor</b>, IUBAT IEEE Computer Society; IEEE and IEEE Computer Society member</div></li>
    </ul>
  </div>
</section>

</main>

<footer class="foot" id="contact">
  <div class="foot-in">
    <h2>Profiles</h2>
    <p class="hero-links">{profiles}</p>
    <p class="mono small">Dhaka, Bangladesh &middot; Figures checked {READ}</p>
  </div>
</footer>

<nav class="dock mono" aria-label="Sections">
  <a href="#about">About</a><a href="#research">Research</a><a href="#publications">Papers</a><a href="#work">Projects</a><a href="#teaching">Teaching</a>
</nav>

<script src="assets/site.js" defer></script>
</body>
</html>
'''
SITE.mkdir(parents=True, exist_ok=True)
(SITE / "index.html").write_text(page, encoding="utf-8")
print("wrote", SITE / "index.html", len(PUBS), "pubs,", n_doi, "with DOI;", quart)
