# Images

Every `.jpg` in this folder is **generated placeholder artwork**, not a photograph
of the resort. They are stylised gradient scenes (sunrise, sunset, lagoon, night,
aerial) produced by `tools/generate-placeholders.py`, so the site looks finished
without pretending to show rooms or beaches that have not been photographed yet.

## Swapping in real photos

Overwrite a file with a real photo **using the same filename**. No code changes
needed anywhere.

| File | Size it is used at | What it should show |
| --- | --- | --- |
| `hero-sunrise.jpg` | 2400×1400, full-bleed desktop hero | Wide shot. Keep the left third darker or uncluttered — the headline sits there. |
| `hero-sunrise-portrait.jpg` | 1200×1700, phone hero | The same scene shot vertically. |
| `island-aerial.jpg` | 4:5 in the island section, 16:9 as a film thumbnail | Aerial or elevated view of the beach and reef. |
| `crossing.jpg` | 4:5 and 16:10 | The boat, the open water, the arrival. |
| `night-village.jpg` | 16:10 and 16:9 | The village music session; lantern or firelight. |
| `lagoon-reef.jpg` | 16:10 | Snorkelling, clear shallow water, coral. |
| `sunset-lagoon.jpg` | 16:10 and 16:9 | Sunset from the beach. |
| `retreat-dusk.jpg` | full-bleed background, 16:10 card | The long table, or a group at dusk. |
| `og-card.jpg` | 1200×630, link previews | One strong frame — this is what shows in messages and social posts. |

Because several files are used at more than one aspect ratio, avoid putting
anything essential right at the edges.

## Vector assets

- `logo-mark.svg` — **placeholder.** A generic gold sun-over-water roundel standing
  in for the resort's emblem. Replace it with the real logo; it renders at 34px in
  the header and 30px in the footer, so it needs to read at small sizes.
- `favicon.svg` — browser tab icon, same motif. Replace to match.

## Keeping the page fast

Aim for under ~400 KB per JPEG, ~250 KB for the ones used as cards. Resize to the
dimensions above before uploading rather than relying on the browser to scale a
6000px camera file down.
