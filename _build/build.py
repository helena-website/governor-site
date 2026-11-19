#!/usr/bin/env python3
"""Build the governor.ri.gov prototype from one shared header and footer.

Run from the repo root:  python3 _build/build.py
Writes static HTML into the repo root. All links are relative, so the site works at any
address (GitHub Pages test URL now, a CMS later). GitHub Pages does not publish folders
that start with "_", so this script stays private to the repo.

Forms are mock only: they validate and show a confirmation screen, but send nothing.
Each form's routing is noted on the page and in the README.
"""
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "Governor Helena Foulkes"
OFFICE = {
    "addr": ["Office of the Governor", "82 Smith Street", "Providence, RI 02903"],
    "phone": "(401) 222-2080", "phone_href": "tel:+14012222080",
    "fax": "(401) 222-8096",
}
# Languages offered by the current governor.ri.gov (GTranslate). English is the default.
LANGS = ["en", "ar", "zh-CN", "zh-TW", "fr", "it", "pl", "pt", "es", "vi", "ht", "km"]

NAV = [("about/", "About"), ("how-can-we-help/", "How can we help you"), ("get-involved/", "Get Involved"), ("news/", "News")]

APRA = "https://governor.ri.gov/apra-request"


def page(path, title, body, desc="", forms=False, pre=None, out_file=None):
    depth = path.count("/")
    if pre is None:
        pre = "../" * depth
    home = pre or "./"
    nav = []
    for href, label in NAV:
        cur = ' aria-current="page"' if path.startswith(href) else ""
        nav.append(f'<li><a href="{pre}{href}"{cur}>{label}</a></li>')
    names = {"en": "English", "ar": "العربية", "zh-CN": "简体中文", "zh-TW": "繁體中文", "fr": "Français", "it": "Italiano",
             "pl": "Polski", "pt": "Português", "es": "Español", "vi": "Tiếng Việt", "ht": "Kreyòl ayisyen", "km": "ភាសាខ្មែរ"}
    short = {"zh-CN": "ZH", "zh-TW": "ZH-TW"}
    opts = "".join(f'<option value="{l}" lang="{l}" title="{names[l]}">{short.get(l, l.upper())}</option>' for l in LANGS)
    lang_select = (f'<label class="sr" for="lang-select">Translate this page</label>'
                   f'<select id="lang-select" class="lang-select notranslate" translate="no">{opts}</select>')
    nav_html = "\n          ".join(nav)
    full_title = SITE if not title else f"{title} | {SITE}"
    script = f'\n<script src="{pre}assets/forms.js" defer></script>' if forms else ""
    html = f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@600;800&family=Montserrat:wght@400;500;700;800&display=swap">
<link rel="icon" type="image/svg+xml" href="{pre}assets/logo-on-white.svg">
<link rel="stylesheet" href="{pre}assets/site.css">
<script src="{pre}assets/site.js" defer></script>{script}
<script src="{pre}assets/translate.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>

<section class="proto-banner" aria-label="Prototype notice">
  <div class="wrap"><strong>Prototype for review.</strong> Not an official State of Rhode Island website.</div>
</section>

<header class="top">
  <div class="wrap top-row">
    <a class="brand" href="{home}">
      <img src="{pre}assets/logo-on-blue.svg" alt="" width="52" height="54">
      <span class="brand-text"><span class="brand-name">Governor Helena Foulkes</span><span class="brand-sub">State of Rhode Island</span></span>
    </a>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul>
          {nav_html}
      </ul>
    </nav>
    <div class="top-tools">
      {lang_select}
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    </div>
  </div>
  <div id="google_translate_element" hidden></div>
</header>

<main id="main" tabindex="-1">
{body.replace("{pre}", pre).replace("{home}", home)}
</main>

<footer class="foot">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <img src="{pre}assets/logo-on-blue.svg" alt="" width="64" height="66">
      <p class="foot-office">{"<br>".join(OFFICE["addr"])}</p>
      <p>Phone: <a href="{OFFICE["phone_href"]}">{OFFICE["phone"]}</a><br>Fax: {OFFICE["fax"]}</p>
      <p><a class="foot-cta" href="{pre}how-can-we-help/">How can we help you?</a></p>
    </div>
    <div>
      <h2 class="foot-h">Related sites</h2>
      <ul>
        <li><a href="https://www.employri.org/">RI Jobs</a></li>
        <li><a href="https://www.ri.gov/">RI.gov</a></li>
        <li><a href="https://www.ri.gov/guide/">State Agencies (A-Z)</a></li>
        <li><a href="{APRA}">APRA Request</a></li>
      </ul>
    </div>
    <div>
      <h2 class="foot-h">Follow</h2>
      <ul class="social">
        <li>Facebook <span class="ph">handle TBD</span></li>
        <li>Instagram <span class="ph">handle TBD</span></li>
        <li>X <span class="ph">handle TBD</span></li>
      </ul>
    </div>
  </div>
  <div class="wrap foot-legal">
    <p><a href="https://www.ri.gov/policies/">Accessibility, data, and privacy policies</a></p>
  </div>
</footer>
</body>
</html>
"""
    out = ROOT / out_file if out_file else ROOT / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


# ---------- form helpers (static HTML, mock submit in assets/forms.js) ----------

def field(fid, label, kind="text", req=False, hint="", options=None, auto="", full=False, accept="", multiple=False):
    req_attr = " required" if req else ""
    star = ' <span class="req" aria-hidden="true">*</span><span class="sr">(required)</span>' if req else ' <span class="opt">(optional)</span>'
    hint_id = f"{fid}-hint" if hint else ""
    desc = f' aria-describedby="{hint_id}"' if hint else ""
    hint_html = f'<p class="hint" id="{hint_id}">{hint}</p>' if hint else ""
    auto_attr = f' autocomplete="{auto}"' if auto else ""
    cls = "field full" if full else "field"
    if kind in ("checks", "radios"):
        t = "checkbox" if kind == "checks" else "radio"
        items = "".join(
            f'<label class="choice" for="{fid}-{i}"><input type="{t}" id="{fid}-{i}" name="{fid}" value="{esc(o)}"{" required" if (req and t == "radio") else ""}> {esc(o)}</label>'
            for i, o in enumerate(options))
        data = ' data-req-group="1"' if (req and t == "checkbox") else ""
        return f'<fieldset class="{cls} group"{data}{desc}><legend>{label}{star}</legend>{hint_html}<div class="choices">{items}</div></fieldset>'
    if kind == "select":
        opts = '<option value="">Choose one</option>' + "".join(f"<option>{esc(o)}</option>" for o in options)
        ctl = f'<select id="{fid}" name="{fid}"{req_attr}{desc}>{opts}</select>'
    elif kind == "textarea":
        ctl = f'<textarea id="{fid}" name="{fid}" rows="6"{req_attr}{desc}></textarea>'
    elif kind == "file":
        acc = f' accept="{accept}"' if accept else ""
        mul = " multiple" if multiple else ""
        ctl = f'<input type="file" id="{fid}" name="{fid}"{acc}{mul}{req_attr}{desc}>'
    else:
        ctl = f'<input type="{kind}" id="{fid}" name="{fid}"{auto_attr}{req_attr}{desc}>'
    return f'<div class="{cls}"><label for="{fid}">{label}{star}</label>{hint_html}{ctl}</div>'


def form(fid, title, routes_to, fields, submit="Submit", intro=""):
    body = "\n".join(fields)
    return f"""<section class="form-wrap" aria-labelledby="{fid}-h">
  <h2 id="{fid}-h">{title}</h2>
  {f'<p class="lead-sm">{intro}</p>' if intro else ''}
  <p class="proto-note"><strong>Prototype:</strong> this form doesn't send anything. In production it routes to {routes_to}.</p>
  <p class="req-key"><span class="req" aria-hidden="true">*</span> Required</p>
  <form class="mock-form" id="{fid}" novalidate data-routes="{esc(routes_to)}">
    <div class="err-summary" role="alert" tabindex="-1" hidden></div>
    <div class="fields">
{body}
    </div>
    <button class="btn btn-blue" type="submit">{submit}</button>
  </form>
  <div class="confirm" id="{fid}-done" tabindex="-1" hidden>
    <h3>Thank you. We got it.</h3>
    <p>We'll review what you sent and get back to you. <span class="ph">Response-time promise TBD</span></p>
    <p class="proto-note">Prototype: nothing was sent. In production this goes to {routes_to}.</p>
  </div>
</section>"""


def contact_fields(prefix=""):
    return [
        field(prefix + "fname", "First name", req=True, auto="given-name"),
        field(prefix + "lname", "Last name", req=True, auto="family-name"),
        field(prefix + "email", "Email", "email", req=True, auto="email"),
        field(prefix + "phone", "Phone", "tel", auto="tel"),
        field(prefix + "town", "City or town", auto="address-level2"),
    ]


def card(href, title, text, cta="Start"):
    return f"""<a class="card" href="{href}"><h3>{title}</h3><p>{text}</p><span class="card-cta">{cta} <span aria-hidden="true">&rarr;</span></span></a>"""


# ---------- content ----------

AGENCY_LINKS = [
    ("Health", [("Department of Health", "https://health.ri.gov/"), ("Vital records", "https://health.ri.gov/records"),
                ("Facilities licensing", "https://health.ri.gov/licenses"), ("Professional licensing and boards", "https://healthri.mylicense.com/"),
                ("WIC / Women and Infants Nutrition", "https://health.ri.gov/programs/detail.php?pgm_id=36")]),
    ("Food, health coverage and family support (DHS)", [("Department of Human Services", "https://dhs.ri.gov/"),
                ("SNAP food assistance", "https://dhs.ri.gov/programs-and-services/supplemental-nutrition-assistance-program-snap"),
                ("Medicare / Medicaid", "https://dhs.ri.gov/programs-and-services/medicaid-medicare-programs"),
                ("Energy assistance", "https://dhs.ri.gov/programs-and-services/energy-assistance-programs"),
                ("Child care assistance (CCAP)", "https://dhs.ri.gov/programs-and-services/child-care"),
                ("RI Works", "https://dhs.ri.gov/programs-and-services/ri-works-program"),
                ("SSI / supplemental payments", "https://dhs.ri.gov/programs-and-services/ssi-state-supplemental-payment"),
                ("Family violence advocacy", "https://dhs.ri.gov/resources/family-violence-option-advocacy-program"),
                ("Long-term services and supports", "https://dhs.ri.gov/programs-and-services/long-term-services-and-supports")]),
    ("Jobs and unemployment (DLT)", [("Department of Labor and Training", "https://dlt.ri.gov/"),
                ("File an unemployment claim", "https://dltweb.dlt.ri.gov/uipua/"), ("Report unemployment fraud", "https://dlt.ri.gov/ui/reportfraud/"),
                ("Download a 1099-G", "https://dlt.ri.gov/1099/"), ("TDI / TCI", "https://dlt.ri.gov/tdi/"),
                ("Workers' compensation", "https://dlt.ri.gov/wc/"), ("Find a DLT form", "https://dlt.ri.gov/forms/")]),
    ("Driving and vehicles (DMV)", [("Division of Motor Vehicles", "https://dmv.ri.gov/"), ("Make a reservation", "https://dmv.ri.gov/make-a-reservation"),
                ("Driver's licenses", "https://dmv.ri.gov/licenses/"), ("Find a DMV form", "https://dmv.ri.gov/forms/"),
                ("License plates", "https://dmv.ri.gov/plates/overview/")]),
    ("Housing", [("Homeless resources", "http://www.rihomeless.org/"), ("Seeking shelter? RI CES", "https://www.cesri.info/"),
                ("RI Housing", "https://www.rihousing.com/"), ("Public housing authorities", "https://www.rihousing.com/public-housing-authorities/"),
                ("Renters' assistance", "https://www.rihousing.com/renters/"), ("Homeowners' assistance", "https://www.rihousing.com/hafri/"),
                ("Buying a home", "https://www.rihousing.com/buyers/"), ("Find a home", "https://www.housingsearchri.org/")]),
    ("Child support", [("Office of Child Support Services", "https://ocss.ri.gov/"), ("Apply for services", "https://ocss.ri.gov/apply-services")]),
    ("Older Rhode Islanders", [("Office of Healthy Aging", "https://oha.ri.gov/"), ("DigiAGE technology help", "https://oha.ri.gov/digiAGE"),
                ("Get help: 211", "https://www.unitedwayri.org/get-help/2-1-1/"), ("Alliance for Better Long Term Care", "http://alliancebltc.org/")]),
    ("Disability and rehabilitation", [("Office of Rehabilitation Services", "https://ors.ri.gov/"), ("ORS resources", "https://ors.ri.gov/resources/resource-links")]),
    ("Veterans", [("Office of Veterans Services", "http://www.vets.ri.gov/")]),
]

TOPICS = ["Health & Human Services", "Education & Workforce", "Economy", "Housing", "Public Safety & Justice",
          "Environment & Energy", "Infrastructure / Transportation", "Government Operations / Budget & Technology", "Other"]
PROBLEM_TOPICS = ["Food, health coverage or family support (DHS / SNAP)", "Unemployment or work (DLT)", "Driving or vehicles (DMV)",
                  "Housing", "Health (DOH)", "Child support", "Veterans", "Older Rhode Islanders", "Citation or proclamation request", "Something else"]

NEWS = [
    {"slug": "sample-press-release", "type": "Press Release", "date": "Jan 5, 2027", "title": "Sample press release: headline goes here",
     "summary": "Placeholder text. Shows how a press release looks on the new site.",
     "body": ['<span class="ph">Placeholder text.</span> This is a sample press release so reviewers can see the layout. It is not a real announcement.',
              "Releases open with a dateline and a short summary, then the full text. Each release can include a quote, links and contact details for the press office.",
              "For press inquiries, contact the Governor's Communications Office. <span class=\"ph\">Press contact TBD</span>"]},
    {"slug": "sample-executive-order", "type": "Executive Order", "date": "Jan 5, 2027", "title": "Sample executive order: title goes here",
     "summary": "Placeholder text. Shows how an executive order looks on the new site.",
     "body": ['<span class="ph">Placeholder text.</span> This is a sample executive order page so reviewers can see the layout. It is not a real order.',
              'Each order shows its number, title and date, a short plain-language summary, and a link to the signed PDF. <span class="ph">Order number and PDF TBD</span>']},
    {"slug": "sample-transmittal-message", "type": "Legislative Transmittal Message", "date": "Jan 5, 2027", "title": "Sample transmittal message: bill number and title",
     "summary": "Placeholder text. Shows how a legislative transmittal message looks on the new site.",
     "body": ['<span class="ph">Placeholder text.</span> This is a sample legislative transmittal message so reviewers can see the layout. It is not a real message.',
              "Each message names the bill, the Governor's action and the date, with a link to the signed letter. <span class=\"ph\">Bill and PDF TBD</span>"]},
]


def build():
    # ---- Home ----
    news_cards = "".join(
        f'<li class="news-row"><span class="news-type">{n["type"]}</span><a href="{{pre}}news/{n["slug"]}/">{n["title"]}</a><span class="news-date">{n["date"]}</span></li>'
        for n in NEWS)
    page("", "", f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <h1>Let's get to work.</h1>
      <p class="lead">Governor Helena Foulkes and her team are here to make state government work for every Rhode Islander. Tell us what you need, share an idea, or join us.</p>
      <div class="hero-ctas">
        <a class="btn btn-ghost" href="{{pre}}how-can-we-help/">How can we help you?</a>
        <a class="btn btn-ghost" href="{{pre}}get-involved/">Get involved</a>
      </div>
    </div>
    <figure class="hero-photo">
      <img src="{{pre}}assets/img/hero-placeholder.webp" alt="Governor Helena Foulkes" width="665" height="900">
    </figure>
  </div>
</section>

<section class="band" aria-labelledby="help-h">
  <div class="wrap">
    <h2 id="help-h">How can we help you?</h2>
    <p class="lead-sm">Have a problem, or want the Governor at your event? Start here.</p>
    <div class="cards">
      {card("{pre}how-can-we-help/#problem", "I have a problem", "Call or let us know what's going on and we'll get back to you.", "Get help")}
      {card("{pre}how-can-we-help/invite-the-governor/", "Invite the Governor", "Ask the Governor to attend or speak at your event.", "Request the Governor")}
      {card("{pre}how-can-we-help/#find-help", "Find state services", "Quick links to unemployment, SNAP, the DMV, housing help and more.", "See services")}
    </div>
  </div>
</section>

<section class="band band-lav" aria-labelledby="gi-h">
  <div class="wrap">
    <h2 id="gi-h">Get involved</h2>
    <p class="lead-sm">Rhode Island works better when more of us pitch in.</p>
    <div class="cards">
      {card("{pre}get-involved/share-an-idea/", "Share an idea", "What could the state fix or do better? Tell us.", "Share your idea")}
      {card("{pre}get-involved/join-the-team/", "Be part of the team", "Interested in a role in a state agency or the Governor's Office?", "Learn more")}
      {card("{pre}get-involved/boards-and-commissions/", "Join a board or commission", "Serve your community on one of the state's boards or commissions.", "Learn more")}
    </div>
  </div>
</section>

""", desc="Office of Governor Helena Foulkes. Let's get to work.")

    # ---- About ----
    page("about/", "About", """
<section class="page-head"><div class="wrap"><p class="eyebrow">About</p><h1>Governor Helena Foulkes</h1>
<p class="lead">Governor Helena Foulkes and her team are here to make state government work for every Rhode Islander.</p></div></section>
<section class="band"><div class="wrap about-grid">
  <div class="about-photos">
    <img src="{pre}assets/img/about-family.webp" alt="Governor Helena Foulkes with her husband, Bill" width="1000" height="620">
    <img src="{pre}assets/img/about-placeholder.webp" alt="Governor Foulkes talking with a family at a park" width="1000" height="667">
  </div>
  <div class="prose">
    <p>Governor Helena Foulkes is a lifelong Rhode Islander, wife of 36 years, mother of four, grandmother, and cancer survivor. She rose through the ranks of CVS over 25 years to become president of its retail division.</p>
    <p>As President of CVS Pharmacy, Helena worked to get consumers the lowest possible prescription drug prices. She removed tobacco products from the shelves, even though tobacco brought in $2 billion in revenue, because protecting people's health matters more than profits.</p>
    <p>Before taking office, Helena partnered with the mayor of Central Falls to improve its public schools, and fought homelessness and domestic violence as a board member and volunteer at nonprofits.</p>
    <p>As Governor, Helena is focused on making state government work for every Rhode Islander. <span class="ph">Bio to be updated</span></p>
    <h2>Office of the Governor</h2>
    <p>Office of the Governor<br>82 Smith Street<br>Providence, RI 02903<br>Phone: <a href="tel:+14012222080">(401) 222-2080</a></p>
  </div>
</div></section>
""", desc="About Governor Helena Foulkes.")

    # ---- How can we help ----
    groups = []
    for i, (name, links) in enumerate(AGENCY_LINKS):
        lis = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in links)
        groups.append(f'<details class="acc"><summary><h3>{name}</h3></summary><ul class="link-list">{lis}</ul></details>')
    problem = form("problem-form", "Tell us about your problem",
                   "the Governor's Constituent Services Office (today this form feeds the office's IQ case system)",
                   contact_fields() + [
                       field("method", "How should we reach you?", "radios", req=True, options=["Email", "Phone"]),
                       field("topic", "What is it about?", "select", req=True, options=PROBLEM_TOPICS),
                       field("message", "What's going on?", "textarea", req=True, full=True,
                             hint="Tell us what happened, which agency you've worked with, and any case or confirmation number. Please don't include your full Social Security number."),
                   ], submit="Send to the Governor's office",
                   intro="Tell us what's going on. We will look into it and get back to you.")
    page("how-can-we-help/", "How Can We Help You", f"""
<section class="page-head"><div class="wrap"><p class="eyebrow">Constituent services</p><h1>How can we help you?</h1>
<p class="lead">Our Constituent Services Office is here to serve all Rhode Islanders. Choose what you need below.</p></div></section>

<section class="band" aria-labelledby="choose-h"><div class="wrap">
  <h2 id="choose-h" class="sr">Choose what you need</h2>
  <div class="cards">
    {card("#problem", "I have a problem", "Call or let us know what's going on and we'll get back to you.", "Tell us")}
    {card("#find-help", "Find state services", "Quick links to the most-requested state services.", "See services")}
    {card("{pre}how-can-we-help/invite-the-governor/", "Invite the Governor", "Ask the Governor to attend or speak at your event.", "Request the Governor")}
  </div>
</div></section>

<section class="band band-lav" id="problem"><div class="wrap narrow">
  <div class="call-box">
    <h2>Call us</h2>
    <p>Call the Constituent Services at <a href="tel:+14012222080">(401) 222-2080</a>. We're available 8am-5pm Monday through Friday. We'll get back to you if we miss your call.</p>
  </div>
  {problem}
</div></section>

<section class="band" id="find-help" aria-labelledby="find-h"><div class="wrap narrow">
  <h2 id="find-h">Find state services</h2>
  <p class="lead-sm">Many questions are fastest to solve with the agency directly.</p>
  {"".join(groups)}
</div></section>

""", desc="Get help from the Governor's Constituent Services Office.", forms=True)

    invite = form("invite-form", "Event request", "the Governor's Scheduling Office",
                  [field("host", "Host or organization", req=True, full=True, auto="organization"),
                   field("ename", "Event name", req=True, full=True),
                   field("edate", "Event date", "date", req=True),
                   field("etime", "Start time", "time", req=True),
                   field("eaddr", "Event address", req=True, full=True, auto="street-address"),
                   field("etown", "City or town", req=True),
                   field("attend", "Expected attendance", "number"),
                   field("role", "What are you asking the Governor to do?", "checks", req=True, full=True,
                         options=["Speak", "Attend", "Meet and greet", "Video message"]),
                   field("open", "This event is", "checks", full=True, options=["Open to the public", "Open to press"]),
                   field("purpose", "Tell us about the event", "textarea", req=True, full=True,
                         hint="Purpose, audience, program and who else is speaking."),
                   field("cname", "Contact name", req=True, auto="name"),
                   field("cphone", "Contact phone", "tel", req=True, auto="tel"),
                   field("cemail", "Contact email", "email", req=True, full=True, auto="email"),
                   field("attach", "Attachments", "file", full=True, multiple=True, hint="Invitation, agenda or program, if you have them."),
                   ], submit="Send the invitation")
    page("how-can-we-help/invite-the-governor/", "Invite the Governor", f"""
<section class="page-head"><div class="wrap"><p class="eyebrow"><a href="{{pre}}how-can-we-help/">How can we help you</a></p><h1>Invite the Governor</h1>
<p class="lead">Ask Governor Foulkes to attend or speak at your event. Please send requests 4 to 6 weeks ahead, one request per event.</p></div></section>
<section class="band"><div class="wrap narrow">
  {invite}
  <div class="call-box"><h2>Questions?</h2><p>Call the Governor's Scheduling Office at <a href="tel:+14012222080">(401) 222-2080</a>.</p>
  <p>Please don't list the Governor on event materials until the Scheduling Office confirms and the Communications Office approves.</p></div>
</div></section>
""", desc="Invite Governor Foulkes to your event.", forms=True)

    # ---- News ----
    page("news/", "News", f"""
<section class="page-head"><div class="wrap"><p class="eyebrow">News</p><h1>From the Office of the Governor</h1>
<p class="lead">Press Releases, Executive Orders, and Legislative Transmittal Messages</p></div></section>
<section class="band"><div class="wrap">
  <h2 class="sr">Latest</h2>
  <ul class="news-rows">{news_cards}</ul>
</div></section>
""", desc="News from the Office of Governor Helena Foulkes.")
    for n in NEWS:
        paras = "".join(f"<p>{p}</p>" for p in n["body"])
        page(f'news/{n["slug"]}/', n["title"], f"""
<section class="page-head"><div class="wrap"><p class="eyebrow"><a href="{{pre}}news/">News</a> · {n["type"]}</p><h1>{n["title"]}</h1><p class="news-date">{n["date"]}</p></div></section>
<section class="band"><div class="wrap narrow prose">{paras}<p><a class="more" href="{{pre}}news/">All news</a></p></div></section>
""", desc=n["summary"])

    # ---- Get involved ----
    page("get-involved/", "Get Involved", f"""
<section class="page-head"><div class="wrap"><p class="eyebrow">Get involved</p><h1>Rhode Island works better when more of us pitch in.</h1>
<p class="lead">Share an idea, join the team, or serve on a board or commission.</p></div></section>
<section class="band" aria-labelledby="ways-h"><div class="wrap">
  <h2 id="ways-h" class="sr">Ways to get involved</h2>
  <div class="cards">
    {card("{pre}get-involved/share-an-idea/", "Share an idea", "What could the state fix or do better? Tell us the problem and your idea.", "Share your idea")}
    {card("{pre}get-involved/join-the-team/", "Be part of the team", "Interested in a role in a state agency or the Governor's Office?", "Learn more")}
    {card("{pre}get-involved/boards-and-commissions/", "Join a board or commission", "Serve your community on one of the state's boards or commissions.", "Learn more")}
  </div>
</div></section>
""", desc="Get involved with the Office of Governor Helena Foulkes.")

    idea = form("idea-form", "Share your idea", "the Governor's policy team (today the transition's Ideas database in Notion)",
                [field("name", "Name", req=True, auto="name"),
                 field("email", "Email", "email", req=True, auto="email"),
                 field("org", "Organization or business", hint="Leave blank if you're writing as an individual.", auto="organization"),
                 field("town", "City or town", auto="address-level2"),
                 field("topic", "Topic", "select", req=True, full=True, options=TOPICS),
                 field("idea", "Your idea", "textarea", req=True, full=True, hint="What's the problem, and what would you do about it? Specifics help."),
                 field("attach", "Attachment", "file", full=True, hint="PDF, Word or image, up to 10 MB."),
                 ], submit="Share my idea")
    page("get-involved/share-an-idea/", "Share an idea", f"""
<section class="page-head"><div class="wrap"><p class="eyebrow"><a href="{{pre}}get-involved/">Get involved</a></p><h1>Share an idea</h1>
<p class="lead">What could the state fix quickly? Tell us the problem and your idea to help Rhode Island work better for everyone.</p></div></section>
<section class="band"><div class="wrap narrow">{idea}</div></section>
""", desc="Share an idea with Governor Foulkes.", forms=True)

    team = form("team-form", "Tell us about yourself", "the Governor's Office HR inbox (hr@, address TBD)",
                contact_fields() + [
                    field("interest", "I'm interested in", "radios", req=True, full=True,
                          options=["A specific open position", "Working in the Governor's Office generally", "A role in a state agency", "A general HR question"]),
                    field("position", "Position title", full=True, hint="If you're applying for a specific opening."),
                    field("resume", "Resume or CV", "file", req=True, full=True, accept=".pdf,.doc,.docx", hint="PDF or Word."),
                    field("note", "Anything else we should know?", "textarea", full=True),
                ], submit="Send")
    page("get-involved/join-the-team/", "Be part of the team", f"""
<section class="page-head"><div class="wrap"><p class="eyebrow"><a href="{{pre}}get-involved/">Get involved</a></p><h1>Be part of the team</h1>
<p class="lead">Help make state government work for every Rhode Islander.</p></div></section>
<section class="band"><div class="wrap narrow">
  <h2>Open positions</h2>
  <p><span class="ph">Open positions list TBD</span> Current state job postings are on <a href="https://www.employri.org/">EmployRI</a>.</p>
  {team}
</div></section>
""", desc="Work in the Office of Governor Helena Foulkes.", forms=True)

    boards = form("boards-form", "Apply to serve", "the Boards and Commissions Director",
                  contact_fields() + [
                      field("which", "Which boards or commissions interest you?", "textarea", req=True, full=True,
                            hint="List any you know of, or the issues you care about. A searchable list of boards and openings is TBD."),
                      field("why", "Why do you want to serve?", "textarea", full=True, hint="Relevant experience and community ties."),
                      field("resume", "Resume or CV", "file", req=True, full=True, accept=".pdf,.doc,.docx", hint="PDF or Word."),
                  ], submit="Apply")
    page("get-involved/boards-and-commissions/", "Join a board or commission", f"""
<section class="page-head"><div class="wrap"><p class="eyebrow"><a href="{{pre}}get-involved/">Get involved</a></p><h1>Join a board or commission</h1>
<p class="lead">Rhode Island's boards and commissions shape decisions in every community. Tell us where you'd like to serve.</p></div></section>
<section class="band"><div class="wrap narrow">{boards}</div></section>
""", desc="Apply to serve on a Rhode Island board or commission.", forms=True)

    # ---- 404 (absolute links, since it can be served at any depth) ----
    page("404/", "Page not found", """
<section class="page-head"><div class="wrap"><h1>Page not found</h1>
<p class="lead">That page isn't here. Try the <a href="{home}">home page</a> or <a href="{pre}how-can-we-help/">How can we help you</a>.</p></div></section>
""", pre="/governor-site/", out_file="404.html")

if __name__ == "__main__":
    build()
