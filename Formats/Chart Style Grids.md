# Summit Dashboard Style Guide — Charts, Tables, Type & Color

Visual formats used in the LLY dashboard (v1–v17). This covers **how things look and behave**: typography, color, number formatting, chart patterns, table patterns and the card layout ("chart on top, table below"). It deliberately does **not** cover which tabs or sections a dashboard should have.

Stack: single self-contained HTML file · Chart.js 4.4.1 (`https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js`) · Figtree from Google Fonts. No other libraries.

---

## 1. Typography

**Font:** `Figtree` (weights 300 / 400 / 500 / 600 / 700), fallback `system-ui, -apple-system, 'Segoe UI', sans-serif`.

```html
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

| Element | Size | Weight | Color | Notes |
|---|---|---|---|---|
| Topbar price / headline value | 18px | 700 | `--text-primary` | −0.5px tracking, tabular nums |
| Topbar ticker | 15px | 700 | `--text-primary` | |
| Stat value (when stat cards are used) | 20px | 700 | `--text-primary` | −0.5px tracking, line-height 1 |
| Card title | 13px | 600 | `--text-primary` | Unit goes after it in `card-sub`: "Revenue by product **(US$B)**" |
| Card sub / unit label | 11px | 400 | `--text-tertiary` | Updates when the chart mode changes |
| Body / table cell | 13px | 400 | `--text-primary` | |
| Prose inside cards | 13px | 400 | `--text-secondary` | line-height 1.6; `<strong>` in `--text-primary` |
| Table header | 11px | 600 | `--text-tertiary` | UPPERCASE, 0.06em tracking |
| Control label ("VIEW", "RANGE") | 11px | 600 | `--text-tertiary` | UPPERCASE, 0.06em tracking |
| Group-header row in tables | 10.5px | 700 | `--text-tertiary` | UPPERCASE, 0.07em tracking, `--main-bg` fill |
| Sub-rows (YoY, % of revenue) | 11px | 400–600 | see §3 | Italic for growth |
| Source note | 10px | 400 | `--text-tertiary` | Italic, `--main-bg` band at card bottom |
| Chart ticks / legend | 11px | 400 | ticks `#9AACBE`, legend `#6B7A8D` | |

**Rule:** all numbers use `font-variant-numeric: tabular-nums` so digits stack in columns.

---

## 2. Color

### 2.1 Core tokens (light)

```css
:root{
  --sidebar-bg:#141C2B;  --sidebar-hover:#1E2D44; --sidebar-active:#243346;
  --sidebar-text:#8899AA;
  --main-bg:#F3F5F8;     --card-bg:#FFFFFF;       --border:#E4E8EE;
  --text-primary:#141C2B; --text-secondary:#6B7A8D; --text-tertiary:#9AACBE;
  --accent:#2E75B6;      --accent-light:#EBF4FF;
  --positive:#00C49A;    --positive-bg:rgba(0,196,154,0.10);
  --negative:#F05252;    --negative-bg:rgba(240,82,82,0.10);
  --neutral-color:#8899AA; --neutral-bg:rgba(107,122,141,0.08);
  --warning:#ED7D31;     --warning-bg:rgba(237,125,49,0.10);
  --chart-grid:#EDF0F5;  --series-1:#141C2B;
  --radius:10px; --radius-sm:6px;
  --shadow:0 1px 3px rgba(0,0,0,0.06),0 1px 2px rgba(0,0,0,0.04);
}
```

### 2.2 Dark-mode overrides

```css
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --main-bg:#0F1520; --card-bg:#172031; --border:#253248;
    --text-primary:#E8EDF4; --text-secondary:#A3B1C2; --text-tertiary:#71829A;
    --accent-light:rgba(46,117,182,0.16); --chart-grid:#223047; --series-1:#C9D6E6;
  }
}
:root[data-theme="dark"]{ /* same values */ }
```

`--series-1` flips from navy to light grey-blue so the primary series stays visible on dark backgrounds. Read it in JS with `getComputedStyle(document.documentElement).getPropertyValue('--series-1')`.

### 2.3 Series palette (categorical)

Use in this order. Red and green are **never** used for categories (reserved for +/−).

| # | Hex | Typical use |
|---|---|---|
| 1 | `--series-1` (#141C2B) | Primary / largest series (e.g. Mounjaro, U.S., P/E) |
| 2 | `#2E75B6` | Second series (Zepbound, EV/EBITDA) |
| 3 | `#5B9BD5` | Third / related to #2 (Foundayo, International) |
| 4 | `#70AD47` | Fourth (Retatrutide, Immunology) |
| 5 | `#ED7D31` | Fifth (Verzenio, Oncology) — also used for growth lines on dual-axis charts |
| 6 | `#833C00` | Sixth (Trulicity) |
| 7 | `#7030A0` | Seventh (Neuroscience) |
| 8 | `#A9D18E` | Small secondary slices (Canada & Japan) |
| — | `#B8C4D2` | "All other" / residual — always last, always grey |
| — | `#6B7A8D` dashed | Totals overlaid on a breakdown ("Total revenue", "Total change") |

### 2.4 Semantic usage

| Meaning | Color |
|---|---|
| Positive change, beat, cheap vs history | `--positive` #00C49A |
| Negative change, miss, rich vs history | `--negative` #F05252 |
| Caution / flag / "check" | `--warning` #ED7D31 |
| Neutral / no change (|x| < 0.05) | `--text-tertiary` |
| Common-size (% of total) values | `--accent` #2E75B6 |
| Forecast / consensus zone | `rgba(46,117,182,0.035–0.08)` tint |

### 2.5 Company colors (competitive charts)

Lilly `#2E75B6` · Novo `#ED7D31` · Amgen `#7030A0` · Roche `#70AD47` · BI/Zealand `#833C00` · Innovent `#5B9BD5` · Others `#8899AA`.

---

## 3. Number formatting (by data type, not location)

| Type | Format | Example |
|---|---|---|
| Currency, table | US$M, thousands separator, no decimals | `22,974` |
| Currency, chart axis/tooltip | US$B, 1 decimal | `$23.0B` |
| Negative currency | Parentheses | `(7,841)` |
| Per share | `$` + 2 decimals | `$36.58` |
| Growth % | Sign + 1 decimal, **italic**, green/red | *+47.7%* / *−9.3%* |
| Growth near zero (|x| < 0.05) | Neutral grey, no sign color | *0.0%* |
| Growth in $ | Sign + `$` + 1 decimal B | `+$9.6B` |
| Margin / share | 1 decimal + `%`, no sign | `85.8%` |
| Common size | 1 decimal `%`, in `--accent` blue | `43.7%` |
| Moves in % metrics | percentage points | `+1.5 pp` |
| Multiples | 1 decimal + `x` | `26.3x` |
| Z-score | Sign + 2 decimals + `σ` | `−1.24σ` |
| Missing value | En dash in `--text-tertiary` | `–` |
| Not meaningful (e.g. PEG with negative growth) | `n/m` in `--text-tertiary` | `n/m` |
| Dates (axis) | `Mon 'YY` | `Sep 26` |
| Dates (tooltip / detail) | `Mon D, YYYY` | `Sep 25, 2026` |

**Data-quality markers inside tables**

| Marker | Meaning |
|---|---|
| Dashed underline | Derived from a disclosed growth rate |
| Dotted underline | Rounded or partial in the source |
| `Check` badge (warning) | Value looks inconsistent in the source |

---

## 4. Card anatomy — "chart on top, table below"

Every analytical block is one card with this vertical order:

```
┌──────────────────────────────────────────────────────────────┐
│ Card title (unit)                       LABEL [seg|seg] LABEL [..] │  ← header: title left, controls right
├──────────────────────────────────────────────────────────────┤
│ [chip] [chip] [chip]   hint text                             │  ← optional legend chips (show/hide series)
│                                                              │
│                         CHART                                │  ← card-body, fixed-height container
│                                                              │
│ ●━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━●                         │  ← optional date slider
│ Sep 17, 2021                               Sep 25, 2026      │
├──────────────────────────────────────────────────────────────┤
│ TABLE (same data as the chart, filtered to what is visible)  │  ← flush to card edges
├──────────────────────────────────────────────────────────────┤
│ Source note (10px italic)                                    │  ← always last
└──────────────────────────────────────────────────────────────┘
   Insight box (only one per view, at the bottom of the view)
```

Rules:
- **Unit lives in the title** and changes with the mode: `(US$B)` → `(% YoY)` → `(US$B added YoY)` → `(% of Lilly revenue)`.
- **Controls sit top-right of the card they control.** Every control has an uppercase label beside it.
- **The table under a chart shows the same lines the chart draws.** Toggling a series off removes it from both.
- **Source note is mandatory** whenever values are derived, estimated or third-party.
- Card: white, 1px `--border`, radius 10px, `--shadow`. Header padding `14px 20px 12px`, body `16px 20px`. Cards stack with `gap:16px`.
- Two-up layout: `grid-template-columns: repeat(2, minmax(0,1fr))`; a wide card spans both (`span-2`). Collapse to one column under 820px.

### Chart container heights

| Class | Height | Use |
|---|---|---|
| `.short` | 220px | Small supporting charts |
| default | 300px | Standard |
| `.tall` | 340px | Main chart of a view, stacked bars with many series |
| custom | 420px | Scatter with many category lanes |

---

## 5. Chart patterns

### 5.1 Universal defaults (apply to every chart)

```js
{
  responsive:true, maintainAspectRatio:false,
  interaction:{ mode:'index', intersect:false },
  plugins:{
    legend:{ labels:{ font:{family:'Figtree',size:11}, color:'#6B7A8D',
             usePointStyle:true, pointStyleWidth:18, boxHeight:3 } },
    tooltip:{ backgroundColor:'#141C2B', titleFont:{family:'Figtree',size:11},
              bodyFont:{family:'Figtree',size:12}, padding:10, cornerRadius:8 }
  },
  scales:{
    x:{ grid:{color:'#EDF0F5', drawTicks:false}, border:{display:false},
        ticks:{font:{family:'Figtree',size:11}, color:'#9AACBE', maxRotation:0} },
    y:{ grid:{color:'#EDF0F5', drawTicks:false}, border:{display:false},
        ticks:{font:{family:'Figtree',size:11}, color:'#9AACBE'} }
  }
}
```

Every tooltip label is formatted by data type (§3). Axis tick callbacks carry the unit (`$20B`, `25%`, `26x`).

### 5.2 Which chart for which question

| Question | Pattern | Details |
|---|---|---|
| Level and mix over time | **Stacked bar** | One stack; residual "All other" in grey on top |
| Share of total | **100% stacked bar** ("Common size") | y-axis fixed 0–100% |
| How fast is each line growing | **Multi-line, % YoY** | One line per series + dashed grey total; clip y to a sane range (e.g. −40% to +200%) |
| Who contributes to growth | **Stacked bar of $ added** + dashed grey line for total change | Bars can go negative |
| Level + margin/share on one chart | **Bar + line, dual axis** | Bars on left axis (US$), line on right axis (%), line in `#ED7D31` or `--series-1` |
| Estimates changing over time | **Step line** (`stepped:'before'`) on a linear date axis | Solid = nearer year, dashed `[5,4]` = further year, same color per product |
| Multiple vs its own history | **Line + ±1σ band + dashed mean** | Band and mean computed over the visible window |
| Sign-encoded values (FCF, net debt) | **Bar colored by sign** | Green ≥ 0, red < 0 |
| Positioning / landscape | **Scatter on category lanes** | x = metric, y = category lane; shape = stage; color = company |
| Two-variable sensitivity | **Heatmap table** (not a chart) | See §6.6 |
| Pie charts | **Never** | Use stacked or 100% stacked bars |

### 5.3 Reading-mode controls (the standard toggle set)

Placed in the card header, left to right:

```
VIEW  [US$B | Growth | Common size]   GROWTH [% | $ added]   RANGE [2020–29 | 2023–29 | 2025–29]
```

- `GROWTH` sub-toggle is only visible when View = Growth.
- Growth base: prior period of the **same series**.
- Changing any toggle re-renders the chart **and** updates the unit in the title.

### 5.4 Actual vs forecast

- **Forecast zone plugin:** light blue rectangle (`rgba(46,117,182,0.06)`) from the first estimate period to the right edge, with a small "Consensus" label (10px, 600, `#2E75B6`) top-left of the zone.
- **Forecast bars** use the same color at ~45–55% alpha.
- **Year labels:** `2025A` for actuals, `2026E` for estimates; guidance years `2026G`.

### 5.5 Event markers on time series

Custom plugin, drawn after datasets:
- Earnings dates: dashed vertical `rgba(237,125,49,0.7)`, `[4,3]`, label at top (`Q2'26`, 10px 600, orange).
- Other events (approvals, trial readouts): dotted vertical `rgba(112,173,71,0.8)`, `[1,3]`, label near the bottom, stacked 13px apart if several.

### 5.6 ±1σ band (historical multiples)

```js
// beforeDatasetsDraw: for each visible series
ctx.fillStyle = seriesBand;            // e.g. rgba(20,28,43,0.07) or rgba(46,117,182,0.09)
ctx.fillRect(left, y(mean+sd), width, y(mean-sd) - y(mean+sd));
ctx.strokeStyle = seriesLine;          // same hue, ~0.5 alpha
ctx.setLineDash([5,4]);                // dashed mean line
```

Line series: 2px, `pointRadius:0`, `pointHoverRadius:4`, `tension:0.1`, `animation:false` (so the slider feels instant).

### 5.7 Scatter on lanes

- y-axis = category index, `reverse:true`, tick callback returns the lane name.
- Point shape encodes stage: `circle` = marketed, `rectRot` (diamond) = filed / Phase 3, `triangle` = Phase 2.
- Point radius 8; selected point radius 10 with a 2.5px `--text-primary` border.
- Labels drawn by a plugin (10.5px 600, `--text-secondary`) to the right of each point; if two points in a lane are < 3.2 units apart, alternate the label below the point.
- Click a point → detail panel to the right of the chart.

### 5.8 Interaction

| Interaction | Behavior |
|---|---|
| Legend click | Hides series (Chart.js default) |
| Legend chips (custom) | Pill buttons, `on` = full opacity + `--main-bg`; `off` = 0.55 opacity. At least one must stay on |
| Vertical drag on chart | Pans the y-axis |
| Double-click on chart | Resets axis / window |
| Dual-range date slider | One rail, two handles, accent band between them, start/end dates shown below in 10.5px 600 uppercase-tracked text |
| Range presets | `1Y / 3Y / 5Y / 10Y`; moving the slider manually clears the active preset |

Y-axis drag helper:

```js
function addYAxisDrag(chart, el){
  let drag=false, y0=0, r={};
  el.addEventListener('mousedown', e=>{ drag=true; y0=e.clientY; r={min:chart.scales.y.min,max:chart.scales.y.max}; });
  document.addEventListener('mousemove', e=>{ if(!drag) return;
    const h=chart.chartArea.bottom-chart.chartArea.top, s=((e.clientY-y0)/h)*(r.max-r.min);
    chart.options.scales.y.min=r.min+s; chart.options.scales.y.max=r.max+s; chart.update('none'); });
  document.addEventListener('mouseup', ()=>{ drag=false; });
  el.addEventListener('dblclick', ()=>{ delete chart.options.scales.y.min; delete chart.options.scales.y.max; chart.update(); });
}
```

---

## 6. Table patterns

### 6.1 Base rules

- First column left-aligned, 600 weight. All other columns right-aligned. Headers align with their column.
- Cell padding `9px 14px`, row border `1px --border`, hover row `--main-bg`.
- Wide tables scroll horizontally inside `.tbl-wrap { overflow-x:auto }`; never let the page scroll sideways.

```css
.metrics-table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}
.metrics-table th{padding:8px 14px;text-align:right;font-size:11px;font-weight:600;
  color:var(--text-tertiary);text-transform:uppercase;letter-spacing:.06em;
  background:var(--main-bg);border-bottom:1px solid var(--border);white-space:nowrap}
.metrics-table th:first-child{text-align:left}
.metrics-table td{padding:9px 14px;text-align:right;font-size:13px;border-bottom:1px solid var(--border)}
.metrics-table td:first-child{text-align:left;font-weight:600}
```

### 6.2 Row types

| Row | Style |
|---|---|
| Line item | Default |
| Subtotal / total (Revenue, Gross profit, EBITDA, EPS) | 700 weight, `--accent-light` background |
| Sub-row: YoY growth | Indented 28px, label 500 `--text-secondary`, values italic 11px green/red |
| Sub-row: % of revenue (common size) | Indented, values in `--accent` blue |
| Sub-row: margin | Indented, plain `%` |
| Group header ("FRANCHISE", "GEOGRAPHY") | Full-width row, 10.5px uppercase tertiary, `--main-bg` fill |
| Residual ("All other", "Unallocated") | Italic label |
| Inactive series (toggled off in chart) | Row at 45% opacity |

Sub-row visibility is controlled by chips or a segmented control in the card header: `ROWS [YoY | Common size | Both]`.

### 6.3 Period columns

- Forecast columns: header `rgba(46,117,182,0.08)` background with `--accent` text; cells `rgba(46,117,182,0.035)`.
- Summary columns on the right (CAGR, LTM, latest YoY): `rgba(46,117,182,0.05)` background with a 1px left border.
- Year-range toggle in the header: `YEARS [2020–29 | 2023–29]`.

### 6.4 Expandable rows (drill-down)

- Parent row shows a caret `▸` (rotates 90° and turns accent when open) and a small count ("11 lines").
- Child rows: `--main-bg` background, 12.5px, indented 34px, with a second line in 10.5px showing share-of-parent and YoY.
- Parent rows are focusable and toggle on Enter/Space.

### 6.5 Statistics table (historical multiples)

Columns: Current (bold) · Mean · Median · −1 s.d. · +1 s.d. · Low (date) · High (date) · vs. mean · Z-score · Percentile · Price at mean. Percentile is green below the mean and red above. All values are recomputed for the selected window.

### 6.6 Sensitivity heatmap

- Rows = input flex (e.g. EPS −15%…+15%), columns = multiple (20x…28x); base row highlighted.
- Cell background = distance from current price: green above, red below, alpha = `min(|Δ|/0.35, 1) × 0.55`.
- Cell text stays 600 weight and fully legible; tooltip shows % vs current.

---

## 7. Components

| Component | Spec |
|---|---|
| **Segmented control** (`period-btns`) | `--main-bg` track, 1px border, radius 6px, 3px padding; buttons 12px 500; active = white, 600, `--shadow` |
| **Chip** | Pill, 1px border, 12px 600, 14×3px colored key line (or 10px dot); `on`/`off` states as in §5.8 |
| **Badge** | Pill, 3px 8px padding, 11px 600; background = `*-bg` token, text = solid token. Variants: positive, negative, neutral, warning, accent |
| **Insight box** | `--accent-light` background, 3px `--accent` left border, 12.5px `--text-secondary`, leading `<strong>` sentence in `--text-primary`. Warning variant uses `--warning-bg` / `--warning`. One per view, at the bottom |
| **Source note** | 10px italic `--text-tertiary`, `--main-bg` band, 1px top border, last element of the card |
| **Accordion** | Header button: caret ▸ + title + 11px meta ("9 lines · Q1'25–Q2'26"); caret rotates when open |
| **Detail panel** (click target) | `--main-bg`, 1px border, radius 10px; title 15px 700 with a 4px colored left bar; key–value rows with 1px dividers, value right-aligned 600 |
| **Timeline / Gantt** | 130px label column; bars 10px high, radius 3px; extensions hatched (`repeating-linear-gradient(45deg, rgba(255,255,255,.55) 0 3px, transparent 3px 6px)`); event dots 14px with 2px card-colored ring; dashed vertical "Today" line |
| **Status tiles** | 5px colored top border = status; 10px uppercase code, 13.5px 700 name, 11.5px 600 status text in the status color; selected tile gets a 2px outline in the same color |

---

## 8. Do / Don't

**Do**
- Style every number by its data type (§3), wherever it appears.
- Put the unit in the card title and update it with the mode.
- Keep chart and table in the same card, showing the same lines.
- Grey out residuals, dash totals, tint forecasts.
- Add a source note to anything derived or third-party.

**Don't**
- Use pie charts.
- Use red/green for categories.
- Show raw `null`/`NaN` — use `–` or `n/m`.
- Color a rounding artifact (|x| < 0.05) as a gain or loss.
- Rely on placeholder text instead of a visible control label.
