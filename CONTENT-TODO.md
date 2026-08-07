# Content handover — what is real and what needs your sign-off

The redesign was built from six screenshots of the current site. The live site
(`lomanikayabeachresorts.com`) could not be fetched during the build — the network
policy on this session blocks it — so anything not visible in those screenshots was
either written fresh or inferred. **Read this file before the site goes live.**

Everything below is grouped by how confident you should be in it.

---

## 1. Confirmed from your current site — safe as-is

| Item | Value |
| --- | --- |
| Name | Lomanikaya Sunrise & Sunset Beach Resort |
| Location | Vatulele Island, Fiji — beside Lomanikaya Village |
| Phone (Fiji) | +679 927 2354 |
| Phone (USA) | +1 310 980 8276 |
| Retreat I | 13–22 November 2026 |
| Retreat II | 25 November – 4 December 2026 |
| Retreat III | 7–16 December 2026 |
| Retreat format | 10 days, all-inclusive, 100 places, entrepreneurs |
| Retreat content | Guest speakers, expert wealth, health and life coaches |
| People named | Ratu Ropate, Ratu Emori, Destini |
| Departure point | Boat launch at Korolevu |
| Also advertised | Employment enquiries welcome |

Two things worth knowing about the current site while you are here:

- **The third retreat is labelled "#2".** Your live page lists 11/25–12/04 as
  "Retreat #2" and 12/07–12/16 as "Retreat #2" as well. This build numbers them
  I, II and III. If the live numbering was deliberate, change it back in
  `index.html`.
- **"Korlevu" is spelled Korolevu** on the Coral Coast. Corrected here.

---

## 2. Needs a real value before launch — currently a placeholder

| Where | Placeholder | What to do |
| --- | --- | --- |
| `index.html` — form `data-mailto` | `info@lomanikayabeachresorts.com` | **Guessed.** Put your real address in, or the form will send enquiries into the void. |
| `index.html` — WhatsApp links (×2) | `https://wa.me/6799272354` | Assumed the Fiji number is WhatsApp-capable. Change or remove if not. |
| `index.html` — four `data-yt="REPLACE_ID_n"` | none | Paste each film's 11-character YouTube ID. Until then, clicking a film shows a note instead of playing. |
| `assets/img/logo-mark.svg` | generic gold sun-and-wave roundel | Replace with your actual gold emblem. Keep it small — the header is designed for a ~34px mark, deliberately, so the logo stops eating the whole first screen. |
| `assets/img/*.jpg` | generated gradient artwork | Replace with real photography — see §4. |
| Form endpoint | empty `data-endpoint` | Optional. Empty = the form opens the visitor's mail client pre-filled, which works on any static host. Add a Formspree/Netlify/CRM URL to capture submissions server-side instead. |

---

## 3. Written for you — check it is true before you publish

None of this came from your site. It reads well, but you are the one who knows
whether it is accurate.

- **"An hour by sea from the Coral Coast"** and **"thirty-three kilometres"** —
  used in the hero, the island section and the Getting Here steps. Verify the
  real crossing time and distance.
- **Masi (tapa) cloth and the sacred red prawns** — widely associated with
  Vatulele, and used in the island copy and the "Masi, by hand" experience card.
  Confirm that guests will actually be offered a masi demonstration.
- **The Getting Here steps** — Nadi (NAN) → Coral Coast drive → Korolevu launch →
  crossing. Inferred from your boat-launch film. Correct the route, and say who
  arranges the road transfer.
- **The "what all-inclusive means here" list** — six inclusions (transfer, bure,
  meals, programme, water activities, village events). Invented as a plausible
  set. Rewrite to match what is genuinely included.
- **Experience cards** — six of them, describing dawn/dusk, the boat loop, village
  music, the reef, masi and a shared dinner table. Grounded in your films and
  photos but embellished.
- **"Opening Nov 2026"** — inferred from the retreat dates being the first events.
- **No rates appear anywhere.** Deliberate: the site drives an enquiry rather than
  quoting a price nobody has confirmed. Add pricing when you have it — the retreat
  cards have room under `.retreat__meta`.

---

## 4. Photography

`assets/img/` currently holds generated gradient artwork — stylised sunrise,
sunset, lagoon, night and aerial scenes. They are illustrations, not fake photos
of the resort, so nothing on the page misrepresents the property.

To swap in real photos, **overwrite the files with the same names** and the site
picks them up with no code change:

| File | Used for | Ideal shot |
| --- | --- | --- |
| `hero-sunrise.jpg` | desktop hero (2400×1400) | wide, dark on the left third, light on the right |
| `hero-sunrise-portrait.jpg` | phone hero (1200×1700) | the same scene, vertical |
| `island-aerial.jpg` | island section, a film thumbnail | aerial of the beach and reef |
| `crossing.jpg` | Getting Here, experience card | the boat, open water |
| `night-village.jpg` | experience card, film thumbnail | the village music session at night |
| `lagoon-reef.jpg` | experience card | snorkelling, clear water |
| `sunset-lagoon.jpg` | experience card, film thumbnail | sunset from the beach |
| `retreat-dusk.jpg` | Claim Your Spot background, card | the long table / a group at dusk |
| `og-card.jpg` | link previews (1200×630) | your best single frame |

Keep them under ~400 KB each. The six photos in your current site's grid would
cover most of this list.

To regenerate the placeholder artwork after edits: `python3 tools/generate-placeholders.py`
(needs `pip install Pillow`). Delete `tools/` once real photos are in.

---

## 5. What was fixed from the old site

- The logo banner filled an entire phone screen before any content. It is now a
  34px mark in the header, and the first thing a visitor reads is what the place is.
- Nothing on the old page asked for a booking. Every screen now has a **Claim Your
  Spot** route: header, announcement ribbon, hero, each retreat card, a sticky
  mobile bar, and a real enquiry form.
- The retreats were buried below a video with no way to reserve a place. They are
  now the second section, with a live countdown to the first one.
- Four raw YouTube embeds loaded on page open. They are now click-to-play facades —
  nothing is requested from YouTube, and no tracking cookie is set, until a visitor
  actually presses play.
- No email address was shown despite the page saying "call or email".
- Added: page title, meta description, Open Graph/Twitter cards, `Resort` +
  `Event` structured data (so the three retreats can appear as events in search),
  a sitemap, a robots file and a styled 404 page.
- Added an employment route, since the old page mentioned hiring but gave it nowhere
  to go.
