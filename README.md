# Indian Courts — Judgment Search (Supreme Court + all 25 High Courts)

A free, serverless search over **19 million+ case records** from the **Supreme Court of India
and all 25 High Courts**. Runs entirely in the browser as a static site — each court's SQLite/FTS5
index is queried directly over HTTP **range requests** (via
[sql.js-httpvfs](https://github.com/phiresky/sql.js-httpvfs)), so there is **no backend**.
Official judgment PDFs are served from the open-data buckets on click.

## How coverage is hosted
The full all-India index is ~5–7 GB, which exceeds a single GitHub Pages site's free quota.
So the data is **sharded across several `*.github.io` data repos** (`india-courts-data-N`).
Because every GitHub Pages project site for one account shares the **same origin**
(`https://<user>.github.io`), the search UI can byte-range-fetch any court's index from any of
those repos with **no CORS issues and no paid hosting** — and only the bytes each query needs are
transferred. A court's index loads on demand the first time you search it.

## Search
- Pick a **court**, then search by **party name**, **judge**, **case number / CNR**, or (Supreme
  Court) **citation** / **neutral citation**.
- FTS5 syntax: `"exact phrase"`, `AND`/`OR`/`NOT`, prefix `arbitrat*`.
- Filter by **year range**. Click **Official PDF** for the full judgment where available.

> Note: the index covers **case metadata** (parties, judges, dates, case numbers/citations), not
> the full body text. The full judgment is one click away via the official PDF.

## Data & license
- Sources: **[Indian Supreme Court Judgments](https://registry.opendata.aws/indian-supreme-court-judgments/)**
  and **[Indian High Court Judgments](https://registry.opendata.aws/indian-high-court-judgments/)**
  open datasets (Registry of Open Data on AWS), derived from the Supreme Court / High Courts / eCourts.
- Licensed **CC-BY-4.0**. This project redistributes only the open-licensed metadata and links to the
  official open-data PDFs; attribution is provided here and in the site footer.
- Research/discovery tool. **Verify against the official record before citing in court.**

## How it was built
- `retool/build_public_sc.py` — Supreme Court metadata → `data/index.db` (in this repo).
- `retool/build_hc_courts.py` — per-High-Court indexes from the HC open dataset (HTTP range +
  column projection; dedups orders → cases by CNR; reconstructs official PDF URLs).
- `retool/deploy_all_india.py` — chunks each court DB (10 MB pieces), bin-packs them into
  `india-courts-data-N` Pages repos under the 1 GB limit, and writes `courts.json`.
- `index.html` — the static search UI (court selector + lazy per-court loading; sql.js-httpvfs + FTS5 WASM).

## Run locally
```
python rangeserver.py 8901
# open http://127.0.0.1:8901/
```
