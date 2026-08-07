# Lomanikaya Sunrise & Sunset Beach Resort

Website for Lomanikaya Sunrise & Sunset Beach Resort — Vatulele Island, Fiji.

A single static page. No framework, no build step, no dependencies: three files
do the work and any host that can serve a folder can serve this.

```
index.html                  the page
assets/css/site.css         one stylesheet
assets/js/site.js           ~4kb of vanilla JS, all of it optional
assets/img/                 artwork (placeholders — see CONTENT-TODO.md)
tools/generate-placeholders.py   regenerates the placeholder artwork
CONTENT-TODO.md             what is real, what is a placeholder — read this first
```

## Run it locally

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

That is the whole toolchain. Opening `index.html` directly works too, though the
form's mail hand-off behaves better over http.

## Deploying

Upload the repository contents to the web root. Nothing needs compiling.

If you host it somewhere that serves from a subdirectory, the paths are all
relative, so it will still work — but update the absolute URLs in the `<head>`
(`canonical`, `og:url`, `og:image`) and in `sitemap.xml`.

## Before it goes live

Read **[CONTENT-TODO.md](CONTENT-TODO.md)**. Four things must be replaced or the
site ships with placeholders:

1. The email address in the form's `data-mailto` (currently a guess).
2. The four `data-yt="REPLACE_ID_n"` YouTube video IDs.
3. The logo in `assets/img/logo-mark.svg`.
4. The photography in `assets/img/` — overwrite the files, keep the names.

## Notes for whoever edits this next

- **Content lives in `index.html`.** It is plain, commented HTML in reading order,
  so changing copy means editing the sentence, not hunting through components.
- **The retreat dates appear in three places** — the cards, the form's `<select>`,
  and the `Event` structured data at the bottom of `index.html`. Change all three.
- **Colours and type are CSS custom properties** at the top of `site.css`. The
  gold, the ink and the sand are each defined once.
- **Films never contact YouTube until clicked.** The thumbnail is a local image and
  the `<iframe>` is only built on click, so the page stays fast and sets no
  third-party cookie to visitors who never press play.
- **The form works with no backend.** Leave `data-endpoint` empty and it composes a
  pre-filled email; set it to a form endpoint and it POSTs instead, without
  reloading. Either way the visitor sees a confirmation.
- **Everything degrades.** With JavaScript disabled the page still reads, the menu
  is reachable, and the form still submits. The countdown simply stays hidden.
