# Z-SGAM-L Architecture City

Interactive isometric explorer for **Precise Corporation (PCC)** showing four industry
architecture models as separate towers on one shared height scale, with the couplings
between them.

Owner: Jinnaphas (Base) · Doc `PCC-EA-SGL-002` · v3 · **workshop draft, not baselined**

---

## What this is for

PCC is presenting topic 17 of an internal SGAM workshop: *"Architecture Structure to be
Architecture Resiliency Development"*. Sixteen speakers each cover one layer or domain;
topic 17 has to show how all of it connects. This app is the visual argument.

Read `docs/KNOWLEDGE.md` before changing anything conceptual. The design decisions in
there are not arbitrary — several were corrected after review and the reasoning matters.

---

## File map

```
CLAUDE.md                      ← you are here
README.md                      ← how to run and deploy
index.html                     ← redirect stub so the site root opens app/
app/index.html                 ← the whole app, single file, no build, no deps
data/architecture-model.json   ← the model · single source of truth · fetched at runtime
tools/verify.py                ← invariant checks (run after any model edit)
tools/derive_analysis.py       ← regenerates derived risk / impact / response bands
docs/KNOWLEDGE.md              ← the architecture knowledge base
.github/workflows/pages.yml    ← runs tools/verify.py, then deploys to Pages
```

`app/index.html` fetches `data/architecture-model.json` at startup, so the JSON is the
only copy of the data. The app must be served over http — `file://` blocks the fetch and
the app says so. Run `python3 tools/verify.py` after editing the model.

---

## Data model invariants — do not break these

1. **Eight common levels L1–L8.** Every tower places its own layers onto this shared
   scale. This is the entire point of the visual: missing floors must stay visible as gaps.
   `L6 Cognition` and `L3 Trust` exist only in SGAM. `L2 Digitization` is missing from SGAM.
2. **RAMI's third axis is Life Cycle, not Zone.** Never label it Zone, never let a UI
   control imply the four towers' Y axes are comparable. RAMI depth is 4, others are 6.
3. **Cube counts:** SGAM 210, RAMI 168, SCIAM 240, SFAM 180 → **798 total.**
4. **SGAM population:** 183 in scope, 79 core, 39 seam-eligible (BUS + CMP layers).
   Other towers have no population data — every node renders uniformly. Do not invent it.
5. **Coupling types A–E** each map to specific levels. A coupling's type must match the
   level it sits on, except the four deliberately asymmetric ones (see below).
6. **Coupling endpoints must resolve to real cubes.** `tools/verify.py` checks this and
   every other invariant on this list. Run it after any edit to the model.

## Deliberate irregularities — these are correct, do not "fix" them

- `CPL-20`, `CPL-21` — SGAM L6 agent docks onto the other tower's **L7**, because no other
  tower has an Intelligence layer. Rendered dashed.
- `CPL-28`, `CPL-29` — SGAM L3 trust flows down into the other tower's **L2 / L4**.
  Rendered dashed.
- `CPL-30` — RAMI ↔ SFAM at L2 with **no SGAM endpoint**. PCC is structurally excluded
  from this conversation. That is the finding, not a bug.

---

## Conventions

- Thai UI copy with English technical terms inline. Keep it that way.
- Fonts: Sarabun (body) + IBM Plex Mono (codes, IDs, numbers).
- Light theme is the default; dark is a toggle. Both must stay legible on a projector.
- Colour encodes **level** (L1–L8) for planes and nodes, **coupling type** (A–E) for lines.
  Never reuse a level colour for a coupling type.
- No labels rendered on nodes. Hover for tooltip, click for the panel. The reference tool
  this replaced was unreadable because it drew every label at once.
- Custom isometric projection in `proj()`. Azimuth rotates; elevation is fixed on purpose —
  free two-axis rotation loses the up/down reference during a live presentation.

---

## Known gaps worth building next

- Seam Contract Register export (CSV/XLSX): 39 eligible positions, 15 named contracts,
  24 unassigned — the gap is the agenda item for the Architecture Review Board.
- Population editor for the three non-SGAM towers.
- Print / PDF export at a fixed camera angle.
- Deep links (`?tower=SGAM,SFAM&coupling=CPL-16`) for jumping straight to a slide state.

## Three buckets, kept apart

Connection and cube attributes are split by where the value comes from, and the split is
enforced rather than described:

- **derived** — computed from the model. Coupling risk score, blast radius, zone response
  bands. `tools/verify.py` recomputes each one and fails if the stored value drifted.
- **rule** — a few authored rules applied across many items. The six in-tower directions
  carry risk and cost drivers this way; 1,901 edges, six rules.
- **authored** — needs a person. `goal`, `concern`, `constraint`, `requiredResources` per
  cube, and every coupling's budget. **0 of 3,084 filled.** Left empty on purpose and
  counted; filling them with generated text would produce architecture nobody owns.

Response bands come from the zone, so a life cycle axis must never carry one. RAMI is
excluded by construction, not by discipline — verify.py fails if a band appears there.

## The team's reporting — measured, or marked unresolved

`team`, `layerStandards`, `domainReports` and `boardReport` come from four decks the
Smart Architecture team produced (references R4–R7). They drive the **รายงานบอร์ด** mode,
the third view alongside 3D and 2D. Two rules hold that section together:

- **Ownership is measured, not inferred.** The layer owners were read by matching each
  name's text-box centre against the layer planes in the same slide's diagram — every one
  lands within 0.04 in, so `confidence: "measured"`. The domain owners are placed along
  the Domains arrow instead of under each domain, and only the two ends resolve. Those
  two are measured; the middle three are `"unresolved"` with the candidate list recorded.
  `verify.py` fails if a row claims owners without being marked measured, or vice versa.
- **The unresolved note has to stay true.** Two owner groups over three candidate domains
  means one domain has nobody. If that ever balances, the gap is gone and check 10 fails
  until the note goes too.

R4 slide 2 also corrects the tower's provenance: SGAM is **IEC SRD 63200:2021**, and its
baseline is **5 layers**. Intelligence (L6) and Cyber (L3) are additions the team proposed —
that is now what the layer `source` says, and it is ASK-5 on the board's list.

## Never do

- Do not present the numbers as verified. Axis counts for SCIAM, SFAM and RAMI were read
  off diagrams and still need confirmation from the workshop's topic 12–14 owners.
- Do not fill the authored cube attributes or coupling budgets with generated text. The
  gap is the finding; 12,350 plausible sentences would bury it.
- Do not describe the 30 couplings as standards-based. They are proposals derived from
  PCC's business context. Type A is the most defensible; type D needs the most scrutiny.
- Do not settle the three unresolved domain owners by picking whichever mapping looks
  tidiest. The deck genuinely does not say. Two groups over three domains means one
  domain has no owner, and finding out which is ASK-1 — a question for the team, not a
  gap to close with a plausible guess.
