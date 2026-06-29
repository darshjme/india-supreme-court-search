# Supreme Court of India — Judgment Search

A free, serverless full-text search over **43,495 Supreme Court of India judgments (1950–2026)**.
Runs entirely in the browser as a static site — the SQLite/FTS5 index is queried directly over
HTTP range requests (via [sql.js-httpvfs](https://github.com/phiresky/sql.js-httpvfs)), so there
is **no backend**. Official judgment PDFs are served from the open-data bucket on click.

## Live site
Hosted on GitHub Pages (see repository settings → Pages).

## Search
- By **party name**, **judge**, **citation** (e.g. `[2024] 10 S.C.R. 108`), or **neutral citation** (e.g. `2024 INSC 735`).
- FTS5 syntax: `"exact phrase"`, `AND`/`OR`/`NOT`, prefix `arbitrat*`.
- Filter by **year range**. Click **Official PDF** for the full judgment.

> Note: the index covers **case metadata** (parties, judges, citations, dates), not the full body
> text, so doctrine searches like "basic structure" match only where those words appear in a title.
> The full judgment is one click away via the official PDF.

## Data & license
- Source: **[Indian Supreme Court Judgments](https://registry.opendata.aws/indian-supreme-court-judgments/)**
  open dataset (Registry of Open Data on AWS), derived from the Supreme Court of India / eCourts.
- Licensed **CC-BY-4.0**. This project redistributes only the open-licensed metadata and links to the
  official open-data PDFs; attribution is provided here and in the site footer.
- This is a research/discovery tool. **Verify against the official record before citing in court.**

## How it was built
- `retool/build_public_sc.py` — downloads the per-year metadata Parquet from the open-data bucket and
  builds a SQLite + FTS5 index (`data/index.db`).
- `index.html` — the static search UI (sql.js-httpvfs + FTS5 WASM).
- `rangeserver.py` — local dev server with HTTP Range support (GitHub Pages supports ranges natively).

## Run locally
```
python rangeserver.py 8901
# open http://127.0.0.1:8901/
```
