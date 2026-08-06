# Architecture City

Isometric explorer for four industry architecture models — SGAM (PCC extended), RAMI 4.0,
SCIAM and SFAM — aligned on eight common concern levels, with 30 named cross-model couplings.

798 cubes · single HTML file · no build step · no runtime dependencies · works offline.

---

## Run

```bash
open app/index.html          # macOS
xdg-open app/index.html      # Linux
start app\index.html         # Windows
```

The repository root carries an `index.html` that redirects to `app/`, so a static host
pointed at the root lands on the explorer.

Or serve it, which you'll want once the app fetches the JSON:

```bash
python3 -m http.server 8080   # then http://localhost:8080/app/
```

Fonts load from Google Fonts. Offline, it falls back to system fonts — Thai still renders,
just less tidily. To make it fully self-contained, download Sarabun and IBM Plex Mono
into `app/fonts/` and swap the `<link>` for `@font-face`.

## Deploy

Static hosting, nothing to configure.

**GitHub Pages** is wired up in `.github/workflows/pages.yml`: it runs the coupling
verification below, then publishes the whole repository root on every push to `main`.
One manual step, once — *Settings → Pages → Source: **GitHub Actions***. After that the
site is at `https://<owner>.github.io/<repo>/`, and `/` redirects to `/app/`.

```bash
# Netlify / Cloudflare Pages
# publish directory: .   build command: (none)

# S3 + CloudFront
aws s3 sync . s3://YOUR-BUCKET/ --delete --exclude '.git/*' --exclude '.github/*'
```

---

## Controls

| | |
|---|---|
| Drag | rotate azimuth |
| Wheel | zoom |
| Click a node | cube detail — what it is, its cross-tower couplings, and why each of its six in-tower neighbours connects |
| Click a line | coupling detail — mechanism, rationale, both endpoints, direction, risk, standards |
| Click a tower name | isolate that tower |
| Tower buttons | multi-select; the shortcut chips jump to common pairs and triples |
| Level rows | isolate one of L1–L8 across all towers — this is how the missing floors become obvious |
| Coupling type rows | filter A–E |
| Theme | light (default) / dark |

Two entry paths into the same information: node-first or line-first. Both reach the same
detail, so pick whichever matches how the question was asked.

---

## Verify after editing the coupling list

Every coupling endpoint must resolve to a real cube in a real tower. Run this after any
change to `SEAMS` in `app/index.html` or to `couplings` in the JSON:

```bash
python3 - <<'EOF'
import re, json
html = open('app/index.html', encoding='utf-8').read()
blk = html[html.index('const SEAMS=['):html.index('/* ============ build')]
rows = re.findall(r'^\["([^"]+)","([^"]+)","([A-E])"', blk, re.M)
model = json.load(open('data/architecture-model.json', encoding='utf-8'))
T = {t['id']: (
        {l[0] for l in t['layers']},
        {x[0] for x in t['xAxis']['items']},
        {y[0] for y in t['yAxis']['items']})
     for t in model['towers']}
bad = []
for a, b, _ in rows:
    for ref in (a, b):
        tw, ly, xx, yy = ref.split('.')
        L, X, Y = T[tw]
        if ly not in L or xx not in X or yy not in Y:
            bad.append(ref)
print(f"couplings: {len(rows)}   invalid endpoints: {bad or 'none'}")
assert len(rows) == len(model['couplings']), "app and JSON are out of sync"
print("app and JSON agree")
EOF
```

Expected: `couplings: 30   invalid endpoints: none` and `app and JSON agree`.

---

## Layout

```
CLAUDE.md                      project context for Claude Code — read first
README.md
index.html                     redirect to app/ so the site root works
app/index.html                 the app
data/architecture-model.json   towers, levels, coupling types, couplings, population, findings
docs/KNOWLEDGE.md              the architecture reasoning behind all of it
.github/workflows/pages.yml    verify, then deploy to GitHub Pages
.nojekyll                      serve files as-is, no Jekyll processing
```

`data/architecture-model.json` was generated from `app/index.html`, so they agree as shipped.
The app still embeds its own copy. **Making the app read the JSON is the first refactor** —
until then, edit both or the verification above will fail.

---

## Status

Workshop draft for PCC topic 17. **Not baselined.** Axis counts for SCIAM, SFAM and RAMI were
read from published diagrams and need confirmation from the workshop's topic 12–14 owners.
The 30 couplings are proposals derived from PCC's business context, not standards.
See `docs/KNOWLEDGE.md` §13 for the full list of open items.
