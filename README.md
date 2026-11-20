# governor-site

A working prototype of the updated Office of the Governor website (today's https://governor.ri.gov), built by the Helena Foulkes transition team. It is the reference for the vendor that implements the production site.

**This is not an official State of Rhode Island website.** Every page shows a prototype banner, has `noindex`, and `robots.txt` blocks all crawlers. Forms are mock only and send nothing.

- Test URL: https://helena-website.github.io/governor-site/
- Feedback: the #website thread in the transition Slack
- Handoff: Dec 1, 2026 vendor meeting

## Scope and phases

- **Scope:** governor.ri.gov only. The RI.gov portal and agency sites are out of scope.
- **Phase 1 (Day 1, Jan 5, 2027):** "Let's get to work." This prototype.
- **Phase 2 (Day 100):** a slightly different message plus improved hospitality. See [Phase 2 ideas](#phase-2-ideas).

## Pages

| Page | Path | Notes |
|---|---|---|
| Home | `/` | Hero ("Let's get to work"), How can we help you, Get involved |
| About | `/about/` | Governor bio, two photos (with Bill; at a park), office address |
| How can we help you | `/how-can-we-help/` | Call us box (8am-5pm weekdays), "Have a problem" form, state services quick links |
| Invite the Governor | `/how-can-we-help/invite-the-governor/` | Web form replacing today's downloadable PDF |
| News | `/news/` | "From the Office of the Governor": one list of press releases, executive orders and legislative transmittal messages, each tagged with its type |
| Samples | `/news/sample-press-release/`, `/news/sample-executive-order/`, `/news/sample-transmittal-message/` | Layout samples, placeholder text |
| Get Involved | `/get-involved/` | Three paths below |
| Share an idea | `/get-involved/share-an-idea/` | Modeled on the transition site's form |
| Be part of the team | `/get-involved/join-the-team/` | Open positions and general HR inquiries, with resume |
| Join a board or commission | `/get-involved/boards-and-commissions/` | Application with resume |

## Navigation changes from today's site

| Today | New |
|---|---|
| Home, About, Accomplishments, Budget, Newsroom, Constituent Services, Data Dashboards, Learn365RI, Contact | About, How can we help you, Get Involved, News |

- **Removed:** Accomplishments, Budget, Contact (folded into How can we help you), Data Dashboards, Learn365RI.
- **Header:** one blue row, like helenatransition.com: logo, menu (About, How can we help you, Get Involved, News), language picker. On phones the menu opens below the header.
- **Browser tab titles:** "Governor Helena Foulkes" on the home page, "<Page> | Governor Helena Foulkes" elsewhere (e.g. "How Can We Help You | Governor Helena Foulkes").
- **Footer:** office address and phone; Related sites (RI Jobs, RI.gov, State Agencies A-Z, APRA Request); Follow (Facebook, Instagram, X); accessibility and privacy policies link.

## Forms

All forms validate required fields, show an error summary that links to each field, and show a confirmation screen. In production, each needs a real back end.

| Form | Fields | Routes to |
|---|---|---|
| Have a problem | First/last name, email, phone, town, contact preference (email/phone), topic, message | Constituent Services Office. Today's contact form is an embedded IQ form (`iqconnect.lmhostediq.com`); production should feed IQ or replace it. |
| Invite the Governor | Host, event name, date, start time, address, town, attendance, role requested, open to public/press, description, contact name/phone/email, attachments | Governor's Scheduling Office, (401) 222-2080 |
| Share an idea | Name, email, organization, town, topic, idea, attachment | Governor's policy team (today: the transition's Ideas database in Notion) |
| Be part of the team | Name, email, phone, town, interest, position title, resume (required), note | Governor's Office HR inbox (hr@, address TBD) |
| Join a board or commission | Name, email, phone, town, boards of interest, why, resume (required) | Boards and Commissions Director |

The "Have a problem" topic list still includes "Citation or proclamation request", matching how today's site handles commemorative documents. The separate citations and preferred license plate boxes were removed in review (today's pages: governor.ri.gov/constituent-services).

## Design tokens

| Token | Value | Use |
|---|---|---|
| Blue | `#2253A5` | Header, hero, headings, links |
| Blue dark | `#1B4485` | Desktop nav bar, hover |
| Navy | `#040D40` | Body text, footer |
| Green | `#26B34C` | Primary button (navy text only: white on green fails contrast) |
| Lavender soft | `#EEF0F7` | Alternate section background |
| Gold | `#F2C230` / `#A87A00` | Logo stars on blue / on white |
| Headings | Barlow Semi Condensed 800 | Google Fonts |
| Body | Montserrat 400/500/700/800 | Google Fonts |

Square corners throughout. Contrast ratios are listed at the top of `assets/site.css`.

**Logo:** an original anchor-and-13-stars mark based on the Rhode Island flag's seal, drawn by `_build/logo.py`.
- `assets/logo-on-white.svg`: navy anchor, gold stars, blue HOPE ribbon
- `assets/logo-on-blue.svg`: white anchor, gold stars, white HOPE ribbon
- `assets/favicon.svg` (unused; the browser tab icon is `logo-on-white.svg`, transparent background)

## Translation

Same machine translation as today's site (Google Translate, which today's GTranslate widget wraps), behind a compact `<select>` in the header showing "Hello" in each language that defaults to English. Languages, in this order: English, Spanish, Portuguese, French, Haitian Creole, Chinese (Simplified), Italian, Arabic. Logic is in `assets/translate.js`: choosing a language sets Google's `googtrans` cookie and reloads; English clears it. Production should add human-reviewed Spanish for the top tasks.

## Accessibility

Target: ADA Title II / WCAG 2.1 AA, required for state websites by April 26, 2027.

Built in: semantic landmarks, skip link, visible focus, keyboard-operable menu (Esc closes it), labeled form fields with hints tied by `aria-describedby`, an error summary that takes focus, text contrast at or above 4.5:1, 48px touch targets, no horizontal scroll at 390px, and `prefers-reduced-motion` support.

Checked with axe-core (WCAG 2.0/2.1 A and AA plus best practices) on every page at 1280px and 390px: **0 violations** as of the first build. Still to check by hand in production: screen reader passes (VoiceOver, NVDA), 200% zoom and reflow on real devices, the GTranslate dropdown's own accessibility, and the PDFs linked from the site.

## Concierge features (round 6)

- **Life-moment services:** "Find state services" rows are named for what people need (e.g. "Losing a job, finding work, or getting hurt at work"), with the agency underneath and an icon.
- **A real person:** copy says a real person on the Constituent Services team reads every message and answers every call.
- **Open/closed indicator:** next to the phone number, computed in the browser from Eastern time (Mon to Fri, 8am to 5pm). State holidays are not handled yet; production should use the office's real holiday calendar.
- **"Need help?" band** above the footer on every page (phone, open/closed status, "Send us a message" link), plus a sticky "Need help?" button on phones.
- **Language picker** shows "Hello" in each language (Hola, Olá, Bonjour, Bonjou...); hover shows the language name.
- **Governor's letter:** the About bio is a first-person draft signed by the Governor (script font standing in for a real signature image). Needs her and the communications team's review.
- **Warm accents:** gold from the logo on icons, card tops and heading rules. Gold is decorative only (4.4:1 on blue is below AA for small text).

## Placeholders

Marked in yellow on the page: the bio update, social handles, response-time promise, open positions list, boards list, HR address, press contact and the three sample news items.

## Phase 2 ideas

- Track a request: a reference number and status for "Have a problem" submissions
- Publish response times and a monthly "what we heard, what we did"
- Resident account so people don't re-enter details
- Grounded AI assistant on state content, with clear AI disclosure
- Searchable list of boards and commissions with open seats

## Build

Plain HTML/CSS/JS, generated by a small Python script so the header and footer stay in one place.

```
python3 _build/logo.py    # only if the logo changes
python3 _build/build.py   # writes every page into the repo root
```

Edit page content in `_build/build.py`, styles in `assets/site.css`. GitHub Pages serves `main` from the repo root as plain files (`.nojekyll`). The hero photo is the transition site photo; the team will decide on a new one.
