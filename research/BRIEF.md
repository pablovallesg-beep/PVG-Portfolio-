# Research brief — PVG Portfolio Dashboard company content

You are filling the content of one company page in a personal equity-research dashboard (HTML, English text).
Today is Nov 10, 2026. Write in English, plain and factual. **Every number, quote and guide must come from a
primary source you actually read** (earnings call transcript, earnings release / shareholder letter, 10-Q/10-K/20-F/6-K,
investor presentation). Never invent or estimate a figure; if you cannot find something, leave it out. Quotes must be verbatim.

## Sources and tools
- Load tools with ToolSearch first. Useful ones:
  - Fiscal.ai: `mcp__claude_ai_Fiscal_ai__api_docs` (pass `functions` to get specific helper docs — the full doc is huge) and
    `mcp__claude_ai_Fiscal_ai__execute_code`. Helpers: `company_ir_events` (list calls), `company_ir_events_transcript`
    (call transcripts), `company_filings`, `company_earnings_summary`, `company_segments_and_kpis`.
    Keep execute_code outputs compact (slice text, extract what you need inside the sandbox).
  - Quartr: `mcp__claude_ai_Quartr__search_companies` → companyId, then `list_events`, `read_transcript`, `list_documents`,
    `read_document`, `search_documents`.
- The company's Fiscal.ai data already in the dashboard is in `C:\Users\pablo\Desktop\PVG Portfolio Dashboard\<Folder>\fiscal.js`
  (JSON after `] = `). Its `seg` rows are `[metricId, name, isKPI, format, isImportant, ...values]`; use those metricIds for charts.
- Example of the expected writing style: Amazon's `AMZN_EARN_DATA` in that folder's `index.html` (search for `const AMZN_EARN_DATA`; read only a slice).

## Output
Write ONE file: `C:\Users\pablo\AppData\Local\Temp\claude\20932b379416ecbf\63444a69-79ee-450f-8f83-a4567cad49b8\scratchpad\research\<TICKER>.json`
and validate it with `python -c "import json;json.load(open(r'<path>',encoding='utf-8'))"`. Write the file progressively
(e.g. after finishing earnings, then thesis, then guidance) so partial work survives. Money in **millions of the reporting
currency** unless the field is text; EPS in currency units. Quarter labels use the company's **fiscal** quarters: `Q3'26`; years `FY2026`.

```json
{
  "ticker": "META",
  "topics": ["Guidance & outlook", "...8-11 short topic names that fit this company..."],
  "earnings": {
    "quarters": {
      "Q3'26": {
        "date": "2026-10-22",
        "headline": "2-3 sentences: the main numbers vs guidance/consensus, what drove them, and the new guide.",
        "numbers": ["8-10 short lines: revenue, segments, margins, EPS, FCF, KPIs, each with YoY"],
        "points": [{"topic": "<one of topics>", "text": "2-3 sentences with numbers and who said it (CEO/CFO name)"}],
        "guidance": ["each guide given on that call/release, with the figure and period"],
        "qa": ["4-6 analyst questions: 'Analyst (Firm) asked about X; CFO said Y.'"]
      }
    },
    "next": {
      "nextReport": {"period": "Q4'26", "expected": "date if announced, else 'late January 2027 (not announced)'"},
      "targets": [{"metric": "Q4'26 revenue", "guide": "$x-yB (+a% to +b% YoY)", "src": "Q3'26 release & call"}],
      "watch": [{"topic": "<one of topics>", "text": "what to check next report and why"}],
      "openQuestions": ["questions analysts left open"]
    }
  },
  "thesis": {
    "summary": "4-6 sentences: what the business is, how it makes money, why it can compound, what the market debates.",
    "pillars": [{"title": "short", "text": "2-4 sentences", "evidence": [{"text": "fact with number", "src": "Q3'26 call"}]}],
    "segments": [{"name": "segment or business line", "text": "2-4 sentences",
                  "segIds": ["metricIds from fiscal.js seg rows to chart (revenue, operating income, KPIs) — only ids that exist"],
                  "themes": [{"theme": "short", "text": "1-2 sentences", "quote": "verbatim management quote", "calls": ["Q1'26", "Q3'26"]}]}],
    "risks": [{"text": "risk with specifics", "src": "10-K / call"}],
    "debates": [{"q": "bull/bear question", "bull": "...", "bear": "..."}]
  },
  "guidance": {
    "labels": {"<metricKey>": ["Label", "m|ps|pct", "unit e.g. US$M"]},
    "periods": {
      "FY2026": {"<metricKey>": {"steps": [{"d": "2026-01-29", "lo": 0, "hi": 0, "src": "URL or 'Q4'25 call'", "n": "note: exact wording, basis"}],
                                  "basis": "optional: GAAP / adjusted / constant currency"}},
      "Q4'26": {}
    }
  }
}
```

## Scope
- **Earnings**: the last 6 reported quarters (newest = the last quarter in fiscal.js), plus `next`.
- **Thesis**: 3-5 pillars, every main segment / business line, 4-6 risks, 3-4 debates. Use themes management repeats across calls.
- **Guidance history** (the important part — it is what Fiscal.ai lacks): every numeric guide the company gave, **each revision as
  its own step with the date it was given**, for FY2025, FY2026 and FY2027 (if given) and for each of the last 6 quarters
  (quarterly guides, given the prior quarter). Metric keys: use these when they fit — `revenue`, `gross_profit`, `gross_margin`
  (pct, e.g. 0.48 for 48%), `ebit`, `operating_margin`, `ebitda_adjusted`, `eps_gaap`, `eps_adjusted`, `net_income`,
  `free_cash_flow`, `capex`, `opex` — otherwise define your own key in `labels` (e.g. `gross_bookings`, `subscribers`, `mau`).
  `lo`/`hi` in millions (or the KPI's own unit, or a fraction for pct). Single number: lo = hi. "At least": hi = null and `"floor": 1`.
  Margin guides stay as margins (pct); do not convert them to amounts. Include the source link when you have one.
- Keep the whole file under ~150 KB. Quality over volume: correct, sourced, specific.

When done, reply with 3-5 lines: what you covered, the quarters, how many guidance steps, and anything you could not source.
