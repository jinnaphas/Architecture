#!/usr/bin/env python3
"""Check data/architecture-model.json against the invariants in CLAUDE.md.

The app reads this file at runtime, so it is the only copy — the old check that
compared the app's embedded literals against the JSON has nothing left to compare.
What matters now is that the model is internally consistent.

    python3 tools/verify.py

Exits non-zero on the first broken invariant.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODEL = ROOT / "data" / "architecture-model.json"


def main() -> int:
    m = json.loads(MODEL.read_text(encoding="utf-8"))
    towers = {t["id"]: t for t in m["towers"]}
    fail = []

    def check(ok, msg):
        if not ok:
            fail.append(msg)

    # 1 — cube counts. layers x domains x zones must equal the declared total.
    total = 0
    for t in m["towers"]:
        n = len(t["layers"]) * len(t["xAxis"]["items"]) * len(t["yAxis"]["items"])
        check(n == t["cubes"], f"{t['id']}: {n} cubes computed but {t['cubes']} declared")
        total += n
        print(f"  {t['id']:6} {len(t['layers'])}L x {len(t['xAxis']['items'])} x "
              f"{len(t['yAxis']['items'])} = {n}")
    check(total == 798, f"total cubes {total}, expected 798")
    check(total == m["meta"]["totalCubes"], "meta.totalCubes disagrees with the towers")

    # 2 — every coupling endpoint resolves to a real cube in a real tower.
    for c in m["couplings"]:
        for role in ("from", "to"):
            tw, layer, x, y = c[role].split(".")
            check(tw in towers, f"{c['id']} {role}: unknown tower {tw}")
            if tw not in towers:
                continue
            t = towers[tw]
            check(layer in {l[0] for l in t["layers"]}, f"{c['id']} {role}: no layer {layer} in {tw}")
            check(x in {i[0] for i in t["xAxis"]["items"]}, f"{c['id']} {role}: no {x} on {tw} x-axis")
            check(y in {i[0] for i in t["yAxis"]["items"]}, f"{c['id']} {role}: no {y} on {tw} y-axis")

    # 3 — coupling ids are unique and the count matches meta.
    ids = [c["id"] for c in m["couplings"]]
    check(len(ids) == len(set(ids)), "duplicate coupling ids")
    check(len(ids) == m["meta"]["namedCouplings"], "meta.namedCouplings disagrees with the list")

    # 4 — a coupling's type must match the level it sits on, except for the four
    #     deliberate asymmetries recorded in CLAUDE.md.
    level_of = {l[0]: l[2] for t in m["towers"] for l in t["layers"]}
    ASYMMETRIC = {"CPL-20", "CPL-21", "CPL-28", "CPL-29"}
    irregular = set()
    for c in m["couplings"]:
        a, b = c["from"].split(".")[1], c["to"].split(".")[1]
        la, lb = level_of[a], level_of[b]
        if la != lb or la not in m["couplingTypes"][c["type"]]["levels"]:
            irregular.add(c["id"])
            check(c["flag"] == "asymmetric",
                  f"{c['id']}: {la}->{lb} as type {c['type']} but not flagged asymmetric")
    check(irregular == ASYMMETRIC,
          f"irregular couplings {sorted(irregular)}, expected {sorted(ASYMMETRIC)}")

    # 5 — SGAM population map: shape, and the headline numbers PCC quotes.
    pop = {k: v for k, v in m["sgamPopulation"].items() if not k.startswith("_")}
    sgam = towers["SGAM"]
    check(set(pop) == {l[0] for l in sgam["layers"]}, "population layers do not match SGAM's layers")
    for layer, rows in pop.items():
        check(len(rows) == len(sgam["xAxis"]["items"]), f"population {layer}: wrong number of domains")
        for r in rows:
            check(len(r) == len(sgam["yAxis"]["items"]), f"population {layer}: wrong number of zones")
    cells = [int(d) for rows in pop.values() for r in rows for d in r]
    in_scope, core = sum(c > 0 for c in cells), sum(c == 3 for c in cells)
    seam_eligible = sum(int(d) > 0 for k in ("BUS", "CMP") for r in pop[k] for d in r)
    named = sum(1 for c in m["couplings"]
                if c["from"].startswith("SGAM.") and c["from"].split(".")[1] in ("BUS", "CMP"))
    check(in_scope == m["meta"]["sgamInScope"], f"SGAM in scope {in_scope}")
    check(core == m["meta"]["sgamCore"], f"SGAM core {core}")
    check(seam_eligible == m["meta"]["sgamSeamEligible"], f"SGAM seam-eligible {seam_eligible}")
    print(f"  SGAM population: {in_scope} in scope · {core} core · "
          f"{seam_eligible} seam-eligible · {named} named · {seam_eligible - named} unassigned")

    # 6 — every layer and shared level declares where it came from.
    for t in m["towers"]:
        for l in t["layers"]:
            check(len(l) == 6, f"{t['id']}.{l[0]}: layer tuple should have 6 slots, has {len(l)}")
            check(bool(l[4]), f"{t['id']}.{l[0]}: no source recorded")
            check(bool(l[5]), f"{t['id']}.{l[0]}: no short description for the UI")
        check(bool(t.get("note")), f"{t['id']}: no note")
    for lv in m["commonLevels"]:
        check(bool(lv.get("source")), f"{lv['id']}: no source recorded")

    print(f"  couplings: {len(ids)} · irregular: {sorted(irregular)} (all flagged)")
    if fail:
        print("\nFAILED:")
        for f in fail:
            print("  -", f)
        return 1
    print("\nmodel is consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
