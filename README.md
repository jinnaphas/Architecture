# Architecture City

Isometric explorer for four industry architecture models — SGAM (PCC extended), RAMI 4.0,
SCIAM and SFAM — aligned on eight common concern levels, with 30 named cross-model couplings.

798 cubes · one HTML file plus one JSON model · no build step · no runtime dependencies.

---

## Run

```bash
python3 -m http.server 8080     # then http://localhost:8080/app/
```

The app fetches `data/architecture-model.json` at startup, so it has to be served over
http. Opening `app/index.html` straight off disk gives a `file://` origin where the
browser blocks the fetch; the app detects that and tells you what to run.

The repository root carries an `index.html` that redirects to `app/`, so a static host
pointed at the root lands on the explorer.

Fonts load from Google Fonts. Offline, it falls back to system fonts — Thai still renders,
just less tidily. To make it fully self-contained, download Sarabun and IBM Plex Mono
into `app/fonts/` and swap the `<link>` for `@font-face`.

## Deploy

Static hosting, nothing to configure.

**GitHub Pages** is wired up in `.github/workflows/pages.yml`: it runs the model
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
| Mode | **3D** isometric · **2D ผังตึก** — four towers as columns, the eight levels as rows · **รายงานบอร์ด** — the Smart Architecture team's report · **สรุปผู้บริหาร** — a one-screen executive summary, Thai or English |
| Layout (3D) | **ตาราง 2×2**, or **เรียงแถว + hub** — the towers on one line with the shared level scale standing between them, each level's guide becoming a spoke out to every tower |
| Drag | rotate azimuth (3D only) |
| Wheel | zoom |
| Click a node | cube detail — what it is, its cross-tower couplings, and why each of its six in-tower neighbours connects |
| Click a line | coupling detail — mechanism, rationale, both endpoints, direction, risk, standards |
| Click a tower name | isolate that tower |
| Tower buttons | multi-select; the shortcut chips jump to common pairs and triples |
| Level rows | isolate one of L1–L8 across all towers — this is how the missing floors become obvious |
| Coupling type rows | filter A–E · the swatch shows each type's dash pattern |
| Theme | light (default) / dark |

Both modes carry the **Z backbone**: the shared level scale as a thing you can see rather
than a set of faint guide lines. In 2D it is a column on the left whose chip is solid when
all four towers carry that level and dashed when they do not; in the row layout it stands
in the middle of the towers with spokes running out to each. Shape carries that
distinction because colour is already spoken for by the level itself.

In 2D a level a tower does not have is drawn as a dashed ghost rather than left absent,
and couplings between matching levels are horizontal — so the only sloped lines on
screen are the four that dock onto a different level. That is finding F2, drawn rather
than explained. Clicking a block opens that layer; clicking a line opens the couplings
it bundles.

Colour carries one meaning only: the level. A coupling line is drawn in the colour of the
level it sits on, and its **type is a dash pattern** — A solid, B long dash, C dotted,
D dash-dot, E short dash. The five type colours this replaced measured 4.6–10.8 ΔE from the
level colours beside them, close enough to read as the same hue on a projector.

Two entry paths into the same information: node-first or line-first. Both reach the same
detail, so pick whichever matches how the question was asked.

**On a phone** the side panel becomes a bottom sheet: parked off-screen until you tap a cube,
a coupling or a block, then it slides up over the drawing with that detail and a close button.
Selecting fewer towers does not raise it — only tapping a thing does. The toolbar collapses to
one row that scrolls sideways with **Mode** at the start, which takes 55px instead of the 223px
it used to spend wrapping over four rows, and every button is at least 40px tall for a finger.

**รายงานบอร์ด** is the third mode and the only one that is not a drawing. It reports what
the Smart Architecture team has actually delivered per architecture: which towers have a
team reporting against them, the three of five SGAM domains that have filed a report, who
owns each interoperability layer and each domain, the 52 standards the team has mapped
onto the seven layers, and the five things it is asking the board to decide. Every number
on the page is recomputed from the model when it renders — none of them are typed in — so
the page cannot drift from the data the other two modes draw.

Coverage is shown as coverage: a domain with no owner gets a highlighted row and a `ยังไม่ระบุ`
pill rather than being left off the table, and the footer states the authored gap in full.

It also carries the **Seam Contract Register** and a CSV export of it: all 39 eligible
positions on SGAM's BUS and CMP layers, 15 with a named coupling and 24 without, one row
each with layer, domain, zone, scope, response band, coupling, type, partner, risk and
blast radius already filled in — and owner, contract id and budget left deliberately blank
for whoever takes them. CSV rather than XLSX because the project has no build step and no
dependencies; a UTF-8 BOM makes Excel open the Thai columns correctly.

**สรุปผู้บริหาร** is the fourth mode and the one to open in the meeting: the thesis in a
sentence, nine headline numbers, the four reference diagrams side by side, the shared scale
showing which towers carry which level, both structural findings, and the open decisions —
on one scrolling screen. A **ไทย / EN** toggle appears only in this mode and switches every
string, including the diagram captions and the board's asks. The other three modes stay Thai,
which is the convention for the working views.

It opens on the **foundation**: the three tests of a core competency that resists
imitation — complexity, organisational diffuseness, well-developed interfaces — each
scored against a figure this repository already computes. Complexity is the mapped
structure; diffuseness is ownership actually named by layer and by domain; interfaces are
seams with a contract behind them. Two of the three fall short today, and the cards say so
rather than rounding up: that is where the moat is thin, and it is the same gap the board
report counts. It closes on the **destination** — the targeted revenue mix, six streams
summing to 100%, with the 55% tied to contracts and assets marked apart from the 45% won
project by project. Both were supplied as pictures and are rebuilt as data, so they follow
the theme, switch language with everything else, and cannot disagree with the model.

Both sections carry a **figure slot** the owner fills without touching code: drop
`core-competency.png` or `revenue-target.png` into `assets/exec/` on GitHub and it appears.
Until then the slot renders a panel naming the exact path, so a missing figure is visible
and actionable rather than a broken icon or an empty box. `verify.py` checks that the
directory is staged for Pages — otherwise a file dropped there would 404 the way the demo
video once did — and that any file which *is* present is a real PNG, JPEG or WebP.

`verify.py` enforces the bilingual rule structurally: it walks the executive block and fails
if any leaf carrying `th` is missing `en` or vice versa, so a half-translated summary cannot
ship. Each tower's diagram also records how many layers, domains and zones it depicts, and
that is checked against the tower itself — a five-layer figure filed under a seven-layer
tower is exactly the sort of thing that survives a slide review and misleads a board.

**Concept รายสถาปัตยกรรม** covers the three non-SGAM towers — what each model is, who
wrote it, and whether its axes are confirmed. RAMI and SFAM are; SCIAM is not, and the
section says why rather than picking a reading. `verify.py` checks that a concept marked
confirmed multiplies out to that tower's actual cube count, so the claim cannot outlive
an edit to the geometry.

The same mode carries the **vertical axis** — one expandable section per interoperability
layer, four of seven reported: Business and Function through a single substation, Intelligence
with its gap taxonomy and autonomy ladder, Communication by domain and by zone. Cyber,
Information and Component are listed as not reported rather than left out.

**Digital Twin** sits below it: the 5 × 5 matrix, the capabilities row, and a 106-second
demo video served from `assets/`. That matrix is drawn on the five-layer baseline, so it has
no Intelligence or Cyber row — `verify.py` recomputes which layers the grid omits and fails
if the model's own list of them disagrees.

---

## Verify after editing the model

`data/architecture-model.json` is the only copy of the data — the app reads it at
runtime. Run this after any change to it:

```bash
python3 tools/verify.py
```

Derived values — a coupling's risk score, its blast radius, and a zone's response band —
are regenerated by `tools/derive_analysis.py` and then **re-checked** by `verify.py`, which
recomputes them and fails if the stored figure has drifted. A stale number cannot sit in
the file pretending to be current.

It checks the invariants from `CLAUDE.md`: cube counts per tower and the 798 total,
every coupling endpoint resolving to a real cube, unique coupling ids, coupling type
matching the level it sits on with exactly the four documented asymmetries flagged,
the SGAM population map's shape and its 183 / 79 / 39 headline numbers, and that every
layer and shared level records where it came from. The Pages workflow runs the same
script before deploying.

It also checks the team's reporting: every layer with a standards list is a real SGAM
layer and all seven are covered, every domain report cites a reference that exists and
names only real zones and layers, the team tables list every layer and domain in order,
and — the one that matters — `team.unresolved` must keep describing a genuine gap. If the
number of owner groups ever equals the number of candidate domains, no domain is left
unowned, and `verify.py` fails until the stale note is removed.

The demo video is checked as a file, not just as a path: byte length first — an MP4's header
survives truncation, so every other check still passes on a half-copied file — then the `ftyp`
box, an H.264 track, `moov` ahead of `mdat` so it starts before it has fully downloaded, and
a duration matching what the model claims.

---

## Layout

```
CLAUDE.md                      project context for Claude Code — read first
README.md
index.html                     redirect to app/ so the site root works
app/index.html                 the app
data/architecture-model.json   the model — the app fetches this at runtime
assets/digital-twin-demo.mp4   the Digital Twin walkthrough played in the board mode
assets/arch/*.jpg              the reference diagram for each of the four towers
tools/verify.py                invariant checks, also run by CI
tools/derive_analysis.py       regenerates the derived risk, impact and response bands
docs/KNOWLEDGE.md              the architecture reasoning behind all of it
.github/workflows/pages.yml    verify, then deploy to GitHub Pages
.nojekyll                      serve files as-is, no Jekyll processing
```

The app fetches the JSON at runtime, so the data lives in exactly one place. Editing the
model means editing that file and running `tools/verify.py`.

---

## Status

Workshop draft for PCC topic 17. **Not baselined.** Axis counts for SCIAM, SFAM and RAMI were
read from published diagrams and need confirmation from the workshop's topic 12–14 owners.
The 30 couplings are proposals derived from PCC's business context, not standards.
See `docs/KNOWLEDGE.md` §13 for the full list of open items.
