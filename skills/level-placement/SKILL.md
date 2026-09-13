---
name: level-placement
description: >-
  Place any system, product, vendor pitch, project or capability onto the eight-level
  interoperability scale (L1 Physical → L8 Purpose) shared by SGAM, RAMI 4.0, SCIAM and
  SFAM, and say what it would take to connect it to something in another architecture.
  Use this whenever someone asks which layer or level something sits on, how deep a
  system's usage actually goes, whether two systems can talk, what a vendor is really
  selling, where an initiative stops, or asks to compare things across smart grid, smart
  factory, smart city and smart farming architectures — including when they describe the
  problem in their own words ("we bought a platform, is it doing anything?", "can these
  two integrate?", "what layer is this?") without naming SGAM, RAMI or any level at all.
---

# Level placement

Four industry architecture models — SGAM (smart grid), RAMI 4.0 (smart factory),
SCIAM (smart city), SFAM (smart farming) — each stack their own layers, but those
layers land on one shared scale of eight concerns. Once a thing is placed on that
scale you can say what it actually does, what it only claims, and what a connection
to anything else would cost.

This skill is the placement method. It comes from PCC's Architecture City model
(`data/architecture-model.json`), which is a **workshop draft, not baselined** — see
*Honesty rules* at the end, they are not decoration.

## The scale

| | Level | Thai | The question it answers | Coupling |
|---|---|---|---|---|
| **L8** | Purpose | เจตนาธุรกิจ | Why does this exist? Whose P&L line, whose mandate? | A |
| **L7** | Capability | ความสามารถ | What named function can someone call? | D |
| **L6** | Cognition | ปัญญาประดิษฐ์ | What decides without a person in the loop? | D |
| **L5** | Semantics | ความหมายข้อมูล | Does the receiver understand what the data *means*? | C |
| **L4** | Exchange | การรับส่ง | Do bytes move? Protocol, transport, session. | B |
| **L3** | Trust | ความปลอดภัย | Who is it, and who says so? Identity, credential, authorisation. | E |
| **L2** | Digitization | แปลงเป็นดิจิทัล | Does the physical thing have a digital twin/record? | B |
| **L1** | Physical | สินทรัพย์กายภาพ | The thing you can touch. Serial number, location, failure mode. | A |

**L6 Cognition and L3 Trust are PCC extensions, not in the SGAM standard.** SGAM per
IEC SRD 63200:2021 has a five-layer baseline; PCC adds these two. L6 comes from
Leiva Vilaplana et al., Technical University of Denmark, 2022 — an academic proposal
the PCC team adopted, not a standard layer. Say so when it comes up; people assume
otherwise and then cite it as though IEC published it.

## Which layers each tower has

The gaps in this table are the whole point. A level a tower does not have is a level
it cannot meet a partner on.

| Level | SGAM (PCC) | RAMI 4.0 | SCIAM | SFAM |
|---|---|---|---|---|
| L8 Purpose | Business | Business | Business | Business |
| L7 Capability | Function | Functional | Function | Function |
| L6 Cognition | **Intelligence** | — | — | — |
| L5 Semantics | Information | Information | Information | Information |
| L4 Exchange | Communication | Communication | Communication | Communication |
| L3 Trust | **Cyber** | — | — | — |
| L2 Digitization | **—** | Integration | — | Integration |
| L1 Physical | Component | Asset | Component | Asset |

Two structural consequences you will hit constantly:

- **SGAM has no L2.** RAMI and SFAM both do. So RAMI↔SFAM can couple at L2 with PCC
  structurally unable to join that conversation. (Finding F1.)
- **Nothing else has L6 or L3.** A PCC agent or credential has no peer to dock onto,
  so it drops to the other tower's L7 or L4 asymmetrically. (Finding F2.)

**RAMI's third axis is Life Cycle, not Zone.** This is the most dangerous trap in the
four models — the others' third axis is a Zone (Market → Process). Comparing RAMI's
axis to a Zone directly produces an architecture that is wrong from the first slide and
stays undetected until it is half built. Never call it Zone. (Finding F3.)

## Placing something

Work bottom-up. People overwhelmingly place things too high, because vendors name
products after the level they wish they were at.

**The test for each level is what breaks when you remove it:**

- **L1** — Pull the plug. Does something physical stop? If nothing physical exists,
  it is not L1, however much hardware is in the diagram.
- **L2** — Is there a digital record of a physical thing that stays correct when the
  thing changes? A nameplate typed into a spreadsheet once is not L2. A register that
  tracks the asset's real state is.
- **L3** — Does it decide *who* something is, or what it may do? Not encryption in
  transit (that is L4 hygiene) — identity issuance, credential, authorisation.
- **L4** — Do bytes actually move between two parties, on a named protocol?
- **L5** — After the bytes arrive, does the receiver know what they mean without a
  human interpreting? A CSV both sides agree on is weak L5. A shared data model is L5.
- **L6** — Does something act without a person approving each act? A dashboard that a
  person reads and then decides is **not** L6 — that is L5 with a human at L7.
- **L7** — Is there a named function someone else can invoke and depend on?
- **L8** — Is there a stated business intent, owner and money attached?

**Most real things occupy a range, not a point.** Report the range. The useful output
is almost always the difference between:

- **reached** — levels where you could name what breaks if it were removed
- **claimed** — levels the marketing, the slide or the project charter asserts

That gap *is* the analysis. A platform that claims L5–L8 and reaches L1–L4 is a
network project wearing a data-platform name, and the budget was approved for the
wrong thing.

### Depth of usage

When the question is how far a system's *usage* has actually gone — as opposed to what
it is capable of — read it as the highest level where you can name a real consequence
of removal, and check the levels beneath it are continuous. **A level cannot be
genuinely reached when a level below it is empty.** Semantics with nothing exchanging
(L5 without L4) means a data model exists on paper. Cognition with no semantics
(L6 without L5) means the model is guessing on fields nobody agreed. Say where the
chain breaks; that break is where the next investment goes, and it is usually much
lower than anyone expects.

## Connecting two things

If the two sit in different towers, the level they meet on determines the coupling
type, and each type has its own cost. Colour in the source model encodes level only;
type is a dash pattern, not a colour.

| Type | Name | Levels | Risk | What it requires |
|---|---|---|---|---|
| **A** | Identity · ผูกที่ตัวตนเดียวกัน | L1, L8 | low | one identifier both sides accept |
| **B** | Contract · ผูกผ่านสัญญาอินเทอร์เฟซ | L2, L4 | medium | interface control document + conformance test |
| **C** | Translation · ผูกผ่านตารางแปลความหมาย | L5 | medium-high | one named source of truth, mapping retested each cycle |
| **D** | Orchestration · ผูกผ่าน use case/agent คร่อมสองตึก | L6, L7 | high | central registration, explicit decision rights, a stop button |
| **E** | Federated trust · ผูกผ่านการยอมรับตัวตนข้ามตึก | L3 | high | one-way only, named trust anchor, never mutual |

Type A is the most defensible. **Type D deserves the most scrutiny** — it is where an
agent quietly acquires authority over two systems with nobody owning the outcome.

If the two things land on **different** levels, the connection is asymmetric: one side
carries governance the other does not. Name who carries it. That is a real cost, and
in this model it falls entirely on PCC for every L6 and L3 coupling.

## Output

Answer in the language the question was asked in — Thai question, Thai answer, with
English technical terms inline, which is this project's convention.

Keep it to this shape. It is short on purpose: the value is in the placement and the
gap, not in prose around them.

```
## <thing> — placement

**Tower**   <SGAM | RAMI | SCIAM | SFAM | outside all four — say which and why>
**Reached** L<n>–L<m>  — <one line per level: what breaks if removed>
**Claimed** L<n>–L<m>  — <what the pitch/charter asserts>
**Gap**     <the difference, stated plainly>

**Chain check**  <continuous, or: breaks at L<n> because …>

**To connect to <other thing>**
  Meets at L<n> → type <X> <name>
  Requires: <the type's requirement, made concrete for this case>
  Asymmetric: <yes, and who carries the governance | no>

**Unresolved**  <what you could not determine, and who would know>
```

If the thing lands on L2, L3 or L6, flag it. Those are the structurally thin levels in
this model — L2 is missing from SGAM entirely, and L3 and L6 exist in SGAM alone — so
anything landing there is either a genuine differentiator or a coupling that cannot be
built yet. Both are worth the board's attention; neither is routine.

## Honesty rules

These exist because the underlying model is a workshop draft and it is easy to make it
sound settled. Breaking them produces confident architecture nobody owns.

- **Do not present the axis counts as verified.** SCIAM, SFAM and RAMI axis counts were
  read off published diagrams and still need confirmation from the topic 12–14 owners.
  SCIAM in particular is contested: one slide of its own source deck shows 5 layers,
  another shows 6. If a placement depends on that, say it depends on that.
- **Do not describe the couplings as standards-based.** They are proposals derived from
  PCC's business context.
- **Do not fill in what you cannot determine.** If the level is genuinely unclear from
  what you were given, write `unresolved` and name who would know. A plausible guess
  buried in a table outlives the person who guessed it. The gap is the finding.
- **Do not resolve an ambiguity by picking the tidiest reading.** Where a source
  contradicts itself, report both readings and what turns on the difference.
- **Distinguish measured from inferred.** If you placed something because someone said
  so, say who. If you placed it by reasoning from the tests above, say that instead.

## Worked example

> "We put in an IoT platform last year. Vendor says it gives us end-to-end visibility
> and AI-driven optimisation across the plant."

```
## IoT platform — placement

**Tower**   RAMI 4.0 (smart factory). Third axis is Life Cycle, not Zone.
**Reached** L1–L4
  L1  sensors on the line — removal stops the readings
  L2  asset register tracks machine state, stays current
  L4  MQTT to the historian — removal stops the data
**Claimed** L5–L7 ("end-to-end visibility", "AI-driven optimisation")
**Gap**     Two and a half levels. Bought as optimisation, running as telemetry.

**Chain check**  Breaks at L5. Tags are per-machine strings with no shared model, so
                 "AI-driven optimisation" at L6 would be inferring over fields nobody
                 has agreed. L6 cannot be genuinely reached while L5 is empty.

**To connect to the SGAM demand-response scheme**
  Meets at L4 → type B Contract
  Requires: an interface control document for the tag set, plus a conformance test
            that runs each release — not a one-off integration
  Asymmetric: no

**Unresolved**  Whether the vendor's "AI" module is doing anything today. Ask for the
                list of actions it has taken without human approval in the last quarter;
                an empty list settles it.
```
