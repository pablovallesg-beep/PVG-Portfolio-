# Build scripts

Run from the repo root with Python 3 (no packages needed). Each script rewrites generated files; do not edit those by hand.

| Script | Reads | Writes |
|---|---|---|
| `build_fx.py` | `data/fiscal-raw/*.json` (Fiscal.ai pulls: statements, segments, estimates, consensus history, guidance) and `data/logos-raw/` | `<Folder>/fiscal.js` for every generic company and the generated logos |
| `build_content.py` | `research/<TICKER>.json` (earnings summaries, thesis and guidance history written from calls, releases and filings) | `<Folder>/content.js`, plus its `<script>` tag in `index.html` |
| `croplogos.py` | `data/logos-raw/` (Wikimedia Commons originals, public domain) | `<Folder>/logo-mark.svg` for the Mexican companies |

- `research/BRIEF.md` is the brief used to write the research files; reuse it to refresh a company or add a new one.
- `build_content.py` leaves out guidance steps the researcher inferred instead of reading (floors from wording, placeholders, own arithmetic).
- Prices and FX in `build_fx.py` (`CO`) are IBKR snapshots from Nov 10, 2026: update them when refreshing.
