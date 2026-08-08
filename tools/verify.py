#!/usr/bin/env python3
"""Check data/architecture-model.json against the invariants in CLAUDE.md.

The app reads this file at runtime, so it is the only copy — the old check that
compared the app's embedded literals against the JSON has nothing left to compare.
What matters now is that the model is internally consistent.

    python3 tools/verify.py

Exits non-zero on the first broken invariant.
"""
import json
import struct
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


    # 7 — derived analysis must still equal what the model would compute now, so a
    #     stale figure cannot sit in the file pretending to be current.
    RISK_BASE = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 4}
    for i, c in enumerate(m["couplings"]):
        a = c.get("analysis")
        check(bool(a), f"{c['id']}: no analysis block")
        if not a:
            continue
        for k in ("risk", "impact", "functionality", "budget"):
            check(k in a, f"{c['id']}: analysis missing {k}")
        want = RISK_BASE[c["type"]] + (1 if c["flag"] in ("asymmetric", "excluded") else 0)
        check(a["risk"]["score"] == want,
              f"{c['id']}: risk score {a['risk']['score']} but the model implies {want}")
        ends = {c["from"], c["to"]}
        lay = {tuple(e.split(".")[:2]) for e in ends}
        blast = [d["id"] for j, d in enumerate(m["couplings"]) if j != i
                 and (ends & {d["from"], d["to"]}
                      or {tuple(e.split(".")[:2]) for e in (d["from"], d["to"])} & lay)]
        check(a["impact"]["blastRadius"] == len(blast),
              f"{c['id']}: blast radius {a['impact']['blastRadius']} but recomputes to {len(blast)}")
        check(a["impact"]["affects"] == blast, f"{c['id']}: affects list is stale")

    # 8 — a zone axis carries response bands; a life cycle axis must not, because
    #     RAMI's third axis is not a zone (invariant 2).
    for t in m["towers"]:
        lifecycle = t["yAxis"]["kind"] == "lifecycle"
        check(t["yAxis"]["bandsApply"] != lifecycle, f"{t['id']}: bandsApply contradicts the axis kind")
        for it in t["yAxis"]["items"]:
            check(len(it) == 5, f"{t['id']}.{it[0]}: y-axis tuple should have 5 slots")
            if lifecycle:
                check(it[4] is None, f"{t['id']}.{it[0]}: a life cycle step must not carry a response band")
            else:
                check(isinstance(it[4], dict) and it[4].get("responseBand"),
                      f"{t['id']}.{it[0]}: zone has no response band")

    # 9 — the authored gap is counted honestly, not quietly filled. in_scope above is
    #     SGAM alone, since only SGAM has a population map; these fields apply to every
    #     in-scope cube in all four towers.
    in_scope_all = 0
    for t in m["towers"]:
        nx, ny = len(t["xAxis"]["items"]), len(t["yAxis"]["items"])
        for l in t["layers"]:
            for xi in range(nx):
                for yi in range(ny):
                    v = int(pop[l[0]][xi][yi]) if t["id"] == "SGAM" else 3
                    if v > 0:
                        in_scope_all += 1
    ca = m["cubeAttributes"]
    check(ca["authored"]["of"] == in_scope_all * len(ca["authored"]["fields"]),
          f"cubeAttributes.authored.of is {ca['authored']['of']}, "
          f"but {in_scope_all} in-scope cubes x {len(ca['authored']['fields'])} fields "
          f"= {in_scope_all * len(ca['authored']['fields'])}")
    unassigned = sum(1 for c in m["couplings"] if c["analysis"]["budget"]["status"] == "unassigned")
    print(f"  connection analysis: risk and blast radius recomputed for {len(m['couplings'])} couplings · "
          f"budget unassigned {unassigned}/{len(m['couplings'])}")
    print(f"  cube attributes: 2 derived · authored {ca['authored']['filled']}/{ca['authored']['of']} "
          f"({', '.join(ca['authored']['fields'])})")

    # 10 — the Smart Architecture team's reporting must point at things that
    #      exist, and must keep counting what it has not got rather than
    #      quietly covering the whole grid.
    sgam_layers = [l[0] for l in sgam["layers"]]
    sgam_domains = [i[0] for i in sgam["xAxis"]["items"]]
    sgam_zones = [i[0] for i in sgam["yAxis"]["items"]]

    ls = m["layerStandards"]["byLayer"]
    check(set(ls) == set(sgam_layers), f"layerStandards covers {sorted(ls)}, SGAM has {sorted(sgam_layers)}")
    for lay, blk in ls.items():
        check(bool(blk.get("view")), f"layerStandards.{lay}: no view statement")
        check(bool(blk["items"]), f"layerStandards.{lay}: no standards")
        for it in blk["items"]:
            check(it["scope"] in {"all"} | set(towers),
                  f"layerStandards.{lay}/{it['code']}: scope {it['scope']} is not a tower")

    reports = {r["domain"]: r for r in m["domainReports"]["reports"]}
    check(set(reports) == set(sgam_domains),
          f"domainReports covers {sorted(reports)}, SGAM domains are {sorted(sgam_domains)}")
    for d, r in reports.items():
        if r["status"] != "reported":
            check(r["ref"] is None, f"{d}: not reported but cites {r['ref']}")
            continue
        check(r["ref"] in {x["id"] for x in m["references"]}, f"{d}: cites unknown reference {r['ref']}")
        for z in r.get("byZone", []):
            check(z["zone"] in sgam_zones, f"{d}: byZone has unknown zone {z['zone']}")
        for l in r.get("byLayer", []):
            check(l["layer"] in sgam_layers, f"{d}: byLayer has unknown layer {l['layer']}")
        for lay, row in r.get("grid", {}).items():
            check(lay in sgam_layers, f"{d}: grid has unknown layer {lay}")
            check(set(row) == set(sgam_zones), f"{d}.{lay}: grid zones {sorted(row)} != {sorted(sgam_zones)}")
        for f in r.get("flows", []):
            for role in ("a", "b"):
                check(f[role] in sgam_zones, f"{d}: flow endpoint {f[role]} is not a zone")

    team = m["team"]
    check([x["layer"] for x in team["layerExperts"]] == sgam_layers,
          "team.layerExperts must list every SGAM layer, in order")
    check([x["domain"] for x in team["domainExperts"]] == sgam_domains,
          "team.domainExperts must list every SGAM domain, in order")
    for x in team["layerExperts"] + team["domainExperts"]:
        check(bool(x["owners"]) == (x["confidence"] == "measured"),
              f"team: {x.get('layer') or x['domain']} has owners but is not marked measured, or vice versa")
    unowned = [x["domain"] for x in team["domainExperts"] if not x["owners"]]
    check(set(unowned) == set(team["unresolved"]["candidates"]),
          f"team.unresolved.candidates {team['unresolved']['candidates']} "
          f"disagrees with the domains left without owners {unowned}")
    check(len(team["unresolved"]["groups"]) < len(unowned),
          "team.unresolved: as many owner groups as candidate domains — nothing would be left unowned, "
          "so the gap this records has gone away and the note should go with it")

    bs = m["boardReport"]
    check({t["tower"] for t in bs["towerStatus"]} == set(towers),
          "boardReport.towerStatus must cover every tower")
    check(sum(1 for t in bs["towerStatus"] if t["reporting"] == "active") >= 1,
          "boardReport: no architecture is reporting")
    for a in bs["asks"]:
        check(bool(a["owner"]) and bool(a["evidence"]), f"{a['id']}: an ask needs an owner and evidence")
    reported = sum(1 for r in m["domainReports"]["reports"] if r["status"] == "reported")
    print(f"  team: layer experts {sum(1 for x in team['layerExperts'] if x['owners'])}/{len(sgam_layers)} · "
          f"domain experts {sum(1 for x in team['domainExperts'] if x['owners'])}/{len(sgam_domains)} · "
          f"domain reports {reported}/{len(sgam_domains)} · "
          f"standards {sum(len(v['items']) for v in ls.values())} · asks {len(bs['asks'])}")

    # 11 — the vertical-axis reports and the Digital Twin overlay. Same rule as
    #      check 10: point at things that exist, and keep counting what is missing.
    lr = {r["layer"]: r for r in m["layerReports"]["reports"]}
    check(set(lr) == set(sgam_layers),
          f"layerReports covers {sorted(lr)}, SGAM has {sorted(sgam_layers)}")
    for lay, r in lr.items():
        check(bool(r["question"]), f"layerReports.{lay}: no question")
        if r["status"] != "reported":
            check(r["ref"] is None, f"layerReports.{lay}: not reported but cites {r['ref']}")
            continue
        check(r["ref"] in {x["id"] for x in m["references"]},
              f"layerReports.{lay}: cites unknown reference {r['ref']}")
        for z in r.get("byZone", []):
            check(z["zone"] in sgam_zones, f"layerReports.{lay}: unknown zone {z['zone']}")
        for d in r.get("byDomain", []):
            check(d["domain"] in sgam_domains, f"layerReports.{lay}: unknown domain {d['domain']}")

    # the Intelligence layer's own story has to stay internally consistent: every
    # case study must cite a gap type that is actually defined.
    intel = lr.get("INT", {})
    if intel.get("status") == "reported":
        types = {g["n"] for g in intel["gapTypes"]}
        for c in intel["cases"]:
            check(c["gapType"] in types, f"INT case {c['n']}: gap type {c['gapType']} is not defined")
        check([a["n"] for a in intel["autonomy"]] == sorted(a["n"] for a in intel["autonomy"]),
              "INT: autonomy levels must be listed in order")
        check(intel["valueChain"][-1] == "Business" and intel["valueChain"][0] == "Component",
              "INT: the value chain runs Component to Business")
        check("Intelligence" in intel["valueChain"], "INT: the decision layer is missing from its own value chain")

    dt = m["digitalTwin"]
    check(dt["ref"] in {x["id"] for x in m["references"]}, f"digitalTwin: unknown reference {dt['ref']}")
    check(set(dt["domains"]) == set(sgam_domains), "digitalTwin: domains must be SGAM's five")
    check(set(dt["layers"]) <= set(sgam_layers), "digitalTwin: layers must all exist on SGAM")
    for lay, row in dt["grid"].items():
        check(lay in dt["layers"], f"digitalTwin.grid has {lay}, not in its declared layers")
        check(set(row) == set(dt["domains"]), f"digitalTwin.{lay}: domains {sorted(row)} != {sorted(dt['domains'])}")
    check(set(dt["grid"]) == set(dt["layers"]), "digitalTwin: every declared layer needs a grid row")
    check(set(dt["capabilities"]["byDomain"]) == set(dt["domains"]),
          "digitalTwin.capabilities must cover every domain")
    # the overlay is drawn on the 5-layer baseline, so the two added layers are
    # absent — that absence is the finding and must stay counted, not quietly filled.
    missing = sorted(set(sgam_layers) - set(dt["layers"]))
    check(sorted(dt["missingLayers"]) == missing,
          f"digitalTwin.missingLayers says {sorted(dt['missingLayers'])} but the grid actually omits {missing}")

    # the demo video ships as a repository asset, so check the file the app points
    # at actually exists, is whole, and is H.264 — browsers will not play anything
    # else, and a silently broken asset would only show up in the meeting.
    vid = dt["video"]
    vpath = (ROOT / "app" / vid["src"]).resolve()
    check(vpath.is_file(), f"digitalTwin.video: {vid['src']} does not resolve to a file ({vpath})")
    if vpath.is_file():
        blob = vpath.read_bytes()
        # size first: an MP4's header survives truncation intact, so every other
        # check below still passes on a half-downloaded file.
        check(len(blob) == vid["bytes"],
              f"digitalTwin.video: file is {len(blob)} bytes but the model says {vid['bytes']} — truncated or replaced")
        check(blob[4:8] == b"ftyp", "digitalTwin.video: not an MP4 (no ftyp box)")
        check(b"avc1" in blob, "digitalTwin.video: no H.264 track — browsers will not play it")
        check(blob.find(b"moov") < blob.find(b"mdat"),
              "digitalTwin.video: moov sits after mdat, so it will not start until fully downloaded")
        i = blob.find(b"mvhd")
        ver = blob[i + 4]
        off = i + 8 + (16 if ver == 1 else 8)
        ts, dur = struct.unpack(">IQ" if ver == 1 else ">II", blob[off:off + (12 if ver == 1 else 8)])
        secs = round(dur / ts)
        check(secs == vid["seconds"],
              f"digitalTwin.video: file is {secs}s but the model says {vid['seconds']}s")
        print(f"  video: {vpath.name} · {len(blob)//1024//1024} MB · {secs}s · H.264 · streams progressively")

        # and the file has to actually reach the published site. The Pages workflow
        # copies a named list of paths into _site, so an asset can exist, pass every
        # check above, and still 404 in the browser because its directory was never
        # staged. That happened once; this is the guard.
        wf = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
        staged = next((l for l in wf.splitlines() if "_site/" in l and l.strip().startswith("cp ")), "")
        top = pathlib.PurePosixPath(vid["src"].replace("../", "")).parts[0]
        check(top in staged.split(),
              f"the Pages workflow does not stage {top}/ — {vid['src']} would 404 on the published site")

    nrep = sum(1 for r in lr.values() if r["status"] == "reported")
    print(f"  layer reports: {nrep}/{len(sgam_layers)} · digital twin: "
          f"{len(dt['layers'])} layers x {len(dt['domains'])} domains, "
          f"omits {', '.join(dt['missingLayers'])} · video {dt['video']['seconds']}s")

    # 12 — a concept that claims the tower's axes are confirmed has to actually
    #      agree with the tower. This is the check that would catch someone editing
    #      the geometry while leaving a deck's "confirmed" claim behind it.
    ac = {c["tower"]: c for c in m["architectureConcepts"]["concepts"]}
    check(set(ac) == set(towers) - {"SGAM"},
          f"architectureConcepts covers {sorted(ac)}, expected the three non-SGAM towers")
    ask_ids = {a["id"] for a in bs["asks"]}
    for tw, c in ac.items():
        t = towers[tw]
        check(c["ref"] in {x["id"] for x in m["references"]}, f"{tw} concept: unknown reference {c['ref']}")
        if c["axesConfirmed"]:
            counts = {a["axis"]: a["n"] for a in c["axes"]}
            for a in c["axes"]:
                check(len(a["items"]) == a["n"],
                      f"{tw} concept: axis {a['axis']} says {a['n']} but lists {len(a['items'])}")
            actual = sorted([len(t["layers"]), len(t["xAxis"]["items"]), len(t["yAxis"]["items"])])
            check(sorted(counts.values()) == actual,
                  f"{tw} concept claims axes {sorted(counts.values())} and calls them confirmed, "
                  f"but the tower is built as {actual}")
            product = 1
            for n in counts.values():
                product *= n
            check(product == t["cubes"],
                  f"{tw} concept's axes multiply to {product}, but the tower declares {t['cubes']} cubes")
        else:
            # unconfirmed means an open question must exist and be findable
            conflict = c.get("conflict") or c.get("instantiation")
            check(bool(conflict), f"{tw} concept: axes not confirmed but no conflict recorded")
            if conflict:
                check(conflict.get("ask") in ask_ids,
                      f"{tw} concept: cites {conflict.get('ask')}, which is not on the board's list")
    # an instantiation that redraws a domain axis must not silently become the tower
    sfam_inst = ac["SFAM"].get("instantiation")
    if sfam_inst:
        check(sfam_inst["ask"] in ask_ids, f"SFAM instantiation cites {sfam_inst['ask']}, not on the board's list")
        check(len(sfam_inst["domains"]) != len(towers["SFAM"]["xAxis"]["items"]),
              "SFAM instantiation now has the same number of domains as the tower — "
              "either it was folded in and should stop being called an instantiation, or a domain was lost")
    conf = [t for t, c in ac.items() if c["axesConfirmed"]]
    print(f"  concepts: {len(ac)} towers · axes confirmed {', '.join(sorted(conf)) or 'none'} · "
          f"open {', '.join(sorted(set(ac) - set(conf))) or 'none'}")

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
