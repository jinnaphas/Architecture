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
data/architecture-model.json   ← machine-readable model (source of truth for content)
docs/KNOWLEDGE.md              ← the architecture knowledge base
.github/workflows/pages.yml    ← runs the README verification, then deploys to Pages
```

`app/index.html` currently embeds its own copy of the data as JS literals.
`data/architecture-model.json` was generated **from** that file, so the two agree today.
**First refactor should be to make the app fetch the JSON** so there is one source of truth.

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
6. **Coupling endpoints must resolve to real cubes.** There is a check for this in README.
   Run it after any edit to the coupling list.

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

- Fetch `data/architecture-model.json` instead of embedding data (highest value).
- Seam Contract Register export (CSV/XLSX): 39 eligible positions, 15 named contracts,
  24 unassigned — the gap is the agenda item for the Architecture Review Board.
- Population editor for the three non-SGAM towers.
- Print / PDF export at a fixed camera angle.
- Deep links (`?tower=SGAM,SFAM&coupling=CPL-16`) for jumping straight to a slide state.

## Never do

- Do not present the numbers as verified. Axis counts for SCIAM, SFAM and RAMI were read
  off diagrams and still need confirmation from the workshop's topic 12–14 owners.
- Do not describe the 30 couplings as standards-based. They are proposals derived from
  PCC's business context. Type A is the most defensible; type D needs the most scrutiny.
