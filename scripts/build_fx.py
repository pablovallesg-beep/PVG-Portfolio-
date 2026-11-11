"""Writes <Folder>/fiscal.js (Fiscal.ai standardized statements, segments / KPIs and estimates) for the generic
company shells of the PVG Portfolio Dashboard, and <Folder>/logo-mark.svg where the logo is generated here."""
import json, os, re, datetime

DASH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # the dashboard repo (scripts/ is inside it)
J = lambda f: json.load(open(os.path.join(DASH, 'data', 'fiscal-raw', f), encoding='utf-8'))

DATA = {c['k']: c for c in J('a.json') + J('b.json') + J('mx.json')}
EST = {c['k']: {**c, 'z': c['z']} for c in J('est.json')}
EST.update({c['k']: c for c in J('mx_est.json')})

# dashboard ticker: (Fiscal.ai key or None, folder, ADS ratio to convert per-share figures to one BMV share or None,
#                    IBKR last trade (price, change, change %, unix ts) captured Nov 10, 2026)
CO = {
    'NVDA': ('NASDAQ_NVDA', 'Nvda', None, (171.83, 2.94, 1.74, 1794362834)),
    'SPOT': ('NYSE_SPOT', 'Spot', None, (606.01, -0.21, -0.03, 1794344397)),
    'SE':   ('NYSE_SE', 'Se', None, (77.10, 0.30, 0.39, 1794361222)),
    'TBBB': ('NYSE_TBBB', 'Tbbb', None, (67.90, 0.07, 0.10, 1794344393)),
    'GOOGL': ('NASDAQ_GOOGL', 'Googl', None, (289.85, 2.47, 0.86, 1794362797)),
    'TSM':  ('NYSE_TSM', 'Tsm', None, (404.40, 7.92, 2.00, 1794362827)),
    'META': ('NASDAQ_META', 'Meta', None, (647.49, 6.10, 0.95, 1794362651)),
    'NFLX': ('NASDAQ_NFLX', 'Nflx', None, (63.11, -0.15, -0.24, 1794361045)),
    # Mexico: BMV listings priced in MXN; Fiscal.ai serves the US ADRs per ADS, converted here to one BMV share
    'AMXB':     ('NYSE_AMX', 'Amx', 20, (24.00, 0.10, 0.42, 1794344398)),         # 1 ADS = 20 Series B shares
    'BIMBOA':   (None, 'Bimbo', None, (70.10, 1.50, 2.19, 1794344396)),            # not covered by Fiscal.ai
    'WALMEX':   ('XMEX_WALMEX', 'Walmex', None, (54.45, -0.14, -0.26, 1794344396)),  # segments / KPIs only
    'ASURB':    ('NYSE_ASR', 'Asur', 10, (499.84, 5.61, 1.14, 1794344393)),       # 1 ADS = 10 Series B shares
    'FEMSAUBD': ('NYSE_FMX', 'Femsa', 10, (246.81, 4.48, 1.85, 1794344396)),      # 1 ADS = 10 BD units
    'OMAB':     ('NASDAQ_OMAB', 'Omab', 8, (256.00, 1.54, 0.61, 1794344396)),      # 1 ADS = 8 Series B shares
    'GMEXICOB': ('XMEX_GMEXICOB', 'Gmexico', None, (222.11, -1.46, -0.65, 1794344392)),  # segments / KPIs only
    'GFNORTEO': (None, 'Banorte', None, (210.49, 1.18, 0.56, 1794344397)),        # not covered by Fiscal.ai
    'GENTERA':  (None, 'Gentera', None, (37.72, 0.07, 0.19, 1794344396)),         # not covered by Fiscal.ai
}

# Fiscal.ai cells known to be wrong, left blank: (ticker, segment name, period type, fiscal year, fiscal quarter)
BAD = [('WALMEX', 'Central America Operating Income', 'A', 2025, None),   # repeats Mexico's 66,574
       ('WALMEX', 'Central America Operating Income', 'Q', 2025, 4)]      # derived from that annual figure

LOGO_SRC = {'NVDA': ('nvidia', '#76B900'), 'SPOT': ('spotify', '#1ED760'), 'GOOGL': ('google', '#4285F4'),
            'META': ('meta', '#0467DF'), 'NFLX': ('netflix', '#E50914')}
LOGO_TXT = {'SE': ('Sea', '#1F2A44'), 'TSM': ('tsmc', '#C8102E')}
# every other company keeps the logo file already in its folder (real logos from Wikimedia Commons)


def logo(tk):
    if tk in LOGO_SRC:
        name, col = LOGO_SRC[tk]
        svg = open(os.path.join(DASH, 'data', 'logos-raw', name + '.svg'), encoding='utf-8').read()
        d = re.search(r'<path d="([^"]+)"', svg).group(1)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="128" height="128">\n'
                f'  <!-- {name} mark (path from Simple Icons, CC0) -->\n  <path fill="{col}" d="{d}"/>\n</svg>\n')
    txt, col = LOGO_TXT[tk]
    fs = 11 if len(txt) <= 2 else 9 if len(txt) == 3 else 7.4
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="128" height="128">\n'
            f'  <!-- ticker badge (text mark, not the company logo) -->\n'
            f'  <text x="12" y="12" dominant-baseline="central" text-anchor="middle" font-family="Helvetica Neue,Arial,sans-serif" '
            f'font-weight="800" font-size="{fs}" letter-spacing="-0.3" fill="{col}">{txt}</text>\n</svg>\n')


def rows(rs, n, head):
    # drop rows with no value; per-share and share rows converted when an ADS ratio applies
    return [r for r in rs if any(v is not None for v in r[head:head + n])]


def conv_stmt(rs, ratio):
    if not ratio: return rs
    out = []
    for r in rs:
        f = r[3]
        k = 1 / ratio if f == 'ps' else ratio if f == 'sh' else 1
        out.append(r[:4] + [None if v is None else round(v * k, 6 if f == 'ps' else 2) for v in r[4:]])
    return out


def conv_est(e, ratio):
    if not ratio: return e
    m = {}
    for k, cells in e['m'].items():
        if k in ('eps_gaap', 'eps_adjusted', 'bvps'):
            cells = [None if c is None else [round(c[0] / ratio, 4)] + c[1:] for c in cells]
        m[k] = cells
    return {**e, 'm': m}


for tk, (key, folder, ratio, px) in CO.items():
    local = datetime.datetime.fromtimestamp(px[3], datetime.timezone.utc) - datetime.timedelta(hours=6)  # Mexico City
    c = DATA.get(key) if key else None
    D = {'key': key, 'cur': (c or {}).get('cur', 'MXN'), 'P': [], 'is': [], 'bs': [], 'cf': [], 'seg': [], 'groups': [],
         'pulled': 'Nov 10, 2026', 'adsRatio': ratio}
    last_sh = None
    if c:
        P = c['P']; n = len(P)
        D.update({'P': [[p['t'], p['e'], p['fy'], p['fq']] for p in P],
                  'is': conv_stmt(rows(c['is'], n, 4), ratio), 'bs': conv_stmt(rows(c['bs'], n, 4), ratio),
                  'cf': conv_stmt(rows(c['cf'], n, 4), ratio), 'seg': rows(c['seg'], n, 5), 'groups': c['groups']})
        for btk, name, t, fy, fq in BAD:
            if btk != tk: continue
            for r in D['seg']:
                if r[1] == name:
                    for i, pp in enumerate(P):
                        if pp['t'] == t and pp['fy'] == fy and (t == 'A' or pp['fq'] == fq): r[5 + i] = None
        sh = next((r for r in D['is'] if r[0] == 'shares_outstanding'), None)
        if sh:
            qi = [i for i, p in enumerate(P) if p['t'] == 'Q']
            last_sh = next((sh[4 + i] for i in reversed(qi) if sh[4 + i] is not None), None)
    D['mkt'] = {'price': px[0], 'chg': px[1], 'chgPct': px[2],
                'asOf': local.strftime('%b %d, %Y').replace(' 0', ' '), 'time': local.strftime('%H:%M'),
                'src': 'Interactive Brokers, last trade' + (' (BMV)' if tk in ('AMXB', 'BIMBOA', 'WALMEX', 'ASURB', 'FEMSAUBD', 'OMAB', 'GMEXICOB', 'GFNORTEO', 'GENTERA') else ''),
                'shares': last_sh, 'sharesSrc': 'shares outstanding at the end of the last reported quarter (Fiscal.ai)'}
    e = EST.get(key)
    if e:
        # Fiscal.ai's own estimates (company_estimates): cells [mean, source, confidence, basis];
        # source g = company guidance, ga = guidance moved by the beat record, gc = quarter from the FY guide,
        # m = Fiscal.ai model, ac = Fiscal.ai AI estimate. Money in millions; eps / bvps in units.
        D['est'] = conv_est({k: e[k] for k in ('cur', 'upd', 'basis', 'P', 'm')}, ratio)
        z = e['z']
        if ratio and 'eps' in z['m']:   # Zacks EPS is per ADS in US$
            z = {**z, 'm': {**z['m'], 'eps': [None if x is None else [round(x[0] / ratio, 4), x[1]] for x in z['m']['eps']]}}
        D['zacks'] = z   # Wall Street consensus (Zacks via Fiscal.ai): [mean, number of estimates]
    path = os.path.join(DASH, folder)
    os.makedirs(path, exist_ok=True)
    js = ('/* ' + tk + ' — Fiscal.ai standardized statements (income statement, balance sheet, cash flow), segments / KPIs and estimates.\n'
          '   Pulled Nov 10, 2026. Money in millions of the reporting currency, shares in millions, per-share in units'
          + (f' (per BMV share: Fiscal.ai ADS figures converted at 1 ADS = {ratio})' if ratio else '') + '.\n'
          '   Row: [id, name, isTotal, format, ...values in the order of P]; P: [type Q|A, period end, fiscal year, fiscal quarter].\n'
          '   Segments: [id, name, isKPI, format m|pct|n, isImportant, ...values]. est = Fiscal.ai estimates; zacks = analyst consensus.\n'
          '   Generated by build_fx.py — do not edit by hand. */\n'
          '(window.FISCAL = window.FISCAL || {})[' + json.dumps(tk) + '] = ' + json.dumps(D, separators=(',', ':')) + ';\n')
    open(os.path.join(path, 'fiscal.js'), 'w', encoding='utf-8', newline='\n').write(js)
    if tk in LOGO_SRC or tk in LOGO_TXT:
        open(os.path.join(path, 'logo-mark.svg'), 'w', encoding='utf-8', newline='\n').write(logo(tk))
    print(tk, folder, len(js), 'bytes', 'est' if e else 'no est', 'shares', last_sh)


# ---- Actual vs Estimates and Guidance Revisions (portfolio companies) ----
# Consensus: last Zacks snapshot before each report (EPS made split-consistent with today's share basis);
# actuals: Fiscal.ai adjusted metrics (US$ for companies that report in another currency, since Zacks is in US$);
# guidance: what Fiscal.ai captured (the pre-report guide of the last reported period and the current guides).
AVE_SRC = {c['k']: c for c in J('ave.json')}
AVE_TK = {'NVDA': 'NASDAQ_NVDA', 'SPOT': 'NYSE_SPOT', 'SE': 'NYSE_SE', 'TBBB': 'NYSE_TBBB', 'GOOGL': 'NASDAQ_GOOGL',
          'TSM': 'NYSE_TSM', 'META': 'NASDAQ_META', 'NFLX': 'NASDAQ_NFLX', 'UBER': 'NYSE_UBER'}
AVE_FOLDER = {**{tk: CO[tk][1] for tk in AVE_TK if tk in CO}, 'UBER': 'Uber'}
G_FOR = {'rev': ['revenue'], 'ebit': ['ebit', 'ebit_adjusted'], 'eps': ['eps_adjusted', 'eps_gaap'], 'ebitda': ['ebitda_adjusted']}


def ave_block(c):
    splits = []
    for s in c['splits']:
        if not s: continue
        r = json.loads(s['raw']) if s.get('raw') and s['raw'].endswith('}') else {}
        if r.get('splitType') == 'Stock Split' and r.get('exDate') and r.get('rate'):
            splits.append((r['exDate'], float(r['rate'])))
    adj = lambda d: 1.0 if not d else __import__('math').prod(rt for ex, rt in splits if ex > d)
    usd = c['cur'] == 'USD'
    G = {(g['l'], g['id']): g for g in c['G']}
    out = {'q': {}, 'y': {}}
    for lab, a in c['act'].items():
        cons = c['cons'].get(lab, {})
        row = {}
        for m in ('rev', 'ebit', 'eps', 'ebitda'):
            d = {}
            loc = a.get(m); us = a.get(m) if usd else a.get(m + 'U')
            g = next((G[(lab, gid)] for gid in G_FOR[m] if (lab, gid) in G and G[(lab, gid)]['act'] is not None), None)
            if g:
                pt = g['filed'] if g['filed'] is not None else g['mean']
                d.update(gLow=pt, gHigh=pt, act=g['act'], gid=g['id'], gsrc=g['src'])
            elif loc is not None:
                d['act'] = loc
            if m in cons:
                v = cons[m]['v']
                if m == 'eps': v = round(v / adj(cons[m]['a']), 4)
                d.update(est=v, n=cons[m]['n'])
            if us is not None: d['actC'] = us
            if d: row[m] = d
        out['q' if lab.startswith('Q') else 'y'][lab] = row
    G_out = [{k: g[k] for k in ('l', 't', 'id', 'src', 'mean', 'filed', 'act', 'asOf', 'iss', 'url', 'ex', 'ed') if g.get(k) not in (None, '')} for g in c['G']]
    return {'cur': c['cur'], 'zcur': c['zcur'], 'epsBasis': c['epsBasis'], **out, 'G': G_out}


for tk, key in AVE_TK.items():
    blk = ave_block(AVE_SRC[key])
    path = os.path.join(DASH, AVE_FOLDER[tk], 'fiscal.js')
    if tk == 'UBER':
        js = ('/* UBER — Fiscal.ai data for Actual vs Estimates and Guidance Revisions (the Uber model itself lives in index.html).\n'
              '   Generated by build_fx.py — do not edit by hand. */\n'
              '(window.FISCAL = window.FISCAL || {})["UBER"] = ' + json.dumps({'ave': blk, 'pulled': 'Nov 10, 2026'}, separators=(',', ':')) + ';\n')
        open(path, 'w', encoding='utf-8', newline='\n').write(js)
    else:
        s = open(path, encoding='utf-8').read()
        i = s.index('] = ') + 4; j = s.rstrip().rindex(';')
        D = json.loads(s[i:j]); D['ave'] = blk
        open(path, 'w', encoding='utf-8', newline='\n').write(s[:i] + json.dumps(D, separators=(',', ':')) + ';\n')
    nq = sum(1 for r in blk['q'].values() if 'est' in r.get('rev', {}))
    ng = sum(1 for p in list(blk['q'].values()) + list(blk['y'].values()) for d in p.values() if 'gLow' in d)
    print('ave', tk, 'quarters w/ consensus', nq, 'guided cells', ng, 'G', len(blk['G']))
