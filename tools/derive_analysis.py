"""Add connection and cube analysis to the model.

Three buckets, kept apart on purpose:

  derived   computed from the model itself — recomputed by this script, never typed
  rule      a handful of authored rules applied across many items
  authored  needs a person; left empty with an owner slot and counted, never invented

12,350 values would be needed to fill every field of every cube and edge by hand.
The model currently holds 88 authored strings. Generating the rest would produce
text that reads like architecture and answers to nobody, which is the failure mode
CLAUDE.md names. So the gaps stay gaps, and the count of them is the deliverable.
"""
import collections
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / 'data' / 'architecture-model.json'
m = json.loads(P.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
C = m['couplings']
TOW = {t['id']: t for t in m['towers']}
pop = {k: v for k, v in m['sgamPopulation'].items() if not k.startswith('_')}

# ── response bands per aggregation zone, from docs/KNOWLEDGE.md §5 ──────────────
BAND = {
    'MKT': ('H6', 'ชั่วโมง – วัน'), 'CW': ('H6', 'ชั่วโมง – วัน'),
    'ENT': ('H5', 'นาที – ชั่วโมง'), 'MI': ('H5', 'นาที – ชั่วโมง'),
    'OPS': ('H4', 'วินาที'), 'OE': ('H4', 'วินาที'),
    'STA': ('H3', '10 – 100 ms'), 'PC': ('H3', '10 – 100 ms'),
    'FLD': ('H2', '3 – 20 ms'), 'SA': ('H2', '3 – 20 ms'),
    'PRO': ('H1', 'ต่ำกว่า 4 ms'), 'PO': ('H1', 'ต่ำกว่า 4 ms'),
}
for t in m['towers']:
    lifecycle = t['yAxis']['kind'] == 'lifecycle'
    for it in t['yAxis']['items']:
        while len(it) < 4:
            it.append('')
        # position 4 = the aggregation level and its response band. A life cycle axis
        # has neither: RAMI's third axis is not a zone and must never be given one.
        if len(it) == 4:
            it.append(None if lifecycle else {'level': BAND[it[0]][0], 'responseBand': BAND[it[0]][1]})
    t['yAxis']['bandsApply'] = not lifecycle
    if lifecycle:
        t['yAxis']['bandsNote'] = ('แกนนี้เป็น Life Cycle ไม่ใช่ Zone — เวลาตอบสนองตาม KNOWLEDGE §5 '
                                   'ใช้กับแกนนี้ไม่ได้ และห้ามใส่')

# ── connection analysis, per coupling ──────────────────────────────────────────
RISK_BASE = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 4}
RISK_WORD = {1: 'ต่ำ', 2: 'ปานกลาง', 3: 'ปานกลาง–สูง', 4: 'สูง', 5: 'สูงมาก', 6: 'สูงมาก'}
COST_DRIVERS = {
    'A': ['รหัสประจำตัวเดียวที่ทั้งสองฝ่ายยอมรับ', 'การกระทบยอดทะเบียนสินทรัพย์'],
    'B': ['interface control document', 'conformance test', 'การคุมเวอร์ชันของ gateway'],
    'C': ['ตาราง mapping', 'การทดสอบ mapping เป็นรอบ', 'การเฝ้าระวัง semantic drift'],
    'D': ['การลงทะเบียนส่วนกลาง', 'การกำหนด decision rights', 'ปุ่มหยุดและการเฝ้าระวัง agent'],
    'E': ['trust anchor', 'การจัดการวงจรชีวิตใบรับรอง', 'การตรวจสอบทางเดียว'],
}


def sgam_pop(ref):
    tw, ly, x, y = ref.split('.')
    if tw != 'SGAM':
        return None
    t = TOW['SGAM']
    xi = [i[0] for i in t['xAxis']['items']].index(x)
    yi = [i[0] for i in t['yAxis']['items']].index(y)
    return int(pop[ly][xi][yi])


def affected(i):
    """Which other couplings must be re-examined if this one's contract changes.
    D7 asks for blast radius across models; this is the structural stand-in that
    open question 4 says should later be replaced by measured dependency."""
    c = C[i]
    ends = {c['from'], c['to']}
    lay = {tuple(e.split('.')[:2]) for e in ends}
    out = []
    for j, d in enumerate(C):
        if j == i:
            continue
        de = {d['from'], d['to']}
        if ends & de or {tuple(e.split('.')[:2]) for e in de} & lay:
            out.append(d['id'])
    return out


for i, c in enumerate(C):
    score = RISK_BASE[c['type']] + (1 if c['flag'] == 'asymmetric' else 0) + (1 if c['flag'] == 'excluded' else 0)
    basis = [f"ชนิด {c['type']} ({m['couplingTypes'][c['type']]['riskTh']})"]
    if c['flag'] == 'asymmetric':
        basis.append('ไม่สมมาตร — ปลายทางอยู่คนละชั้น ภาระกำกับตกฝั่งเดียว')
    if c['flag'] == 'excluded':
        basis.append('PCC เข้าร่วมไม่ได้ — ไม่มีชั้นที่ตรงกัน')
    ends_pop = [p for p in (sgam_pop(c['from']), sgam_pop(c['to'])) if p is not None]
    aff = affected(i)
    c['analysis'] = collections.OrderedDict([
        ('risk', collections.OrderedDict([
            ('level', RISK_WORD[min(score, 6)]), ('score', score), ('of', 6),
            ('basis', ' · '.join(basis)), ('source', 'derived'),
        ])),
        ('impact', collections.OrderedDict([
            ('blastRadius', len(aff)),
            ('affects', aff),
            ('towers', sorted({c['from'].split('.')[0], c['to'].split('.')[0]})),
            ('sgamEndpointPopulation', ends_pop or None),
            ('basis', 'coupling อื่นที่แตะ cube เดียวกันหรือชั้นเดียวกันของตึกเดียวกัน'),
            ('caveat', 'ค่าเชิงโครงสร้างตามกฎ D7 — openQuestions ข้อ 4 ระบุว่าควรแทนด้วยค่าที่วัดจาก dependency จริง'),
            ('source', 'derived'),
        ])),
        ('functionality', collections.OrderedDict([
            ('provides', c['mechanism']),
            ('class', m['couplingTypes'][c['type']]['name']),
            ('direction', m['couplingTypes'][c['type']]['directionTh']),
            ('requires', m['couplingTypes'][c['type']]['requires']),
            ('standards', [s.strip() for s in c['standards'].split('·') if s.strip() and s.strip() != '—']),
            ('source', 'derived'),
        ])),
        ('budget', collections.OrderedDict([
            ('drivers', COST_DRIVERS[c['type']]),
            ('estimate', None), ('currency', None), ('period', None),
            ('owner', None), ('contractId', None),
            ('status', 'unassigned'),
            ('note', 'ตัวเลขงบไม่มีในมาตรฐานทั้งสามฉบับ — ต้องมาจาก PCC และผ่าน Architecture Review Board'),
            ('source', 'authored — ยังว่าง'),
        ])),
    ])

# ── in-tower connections: six rules, not 1,901 rows ────────────────────────────
m['inTowerConnections'] = collections.OrderedDict([
    ('_note', 'เส้นเชื่อมภายในตึกมี 1,901 เส้น จึงอธิบายด้วยกฎตามทิศทาง ไม่ใช่เขียนทีละเส้น '
              'แอปประกอบข้อความจากกฎเหล่านี้ตอน render'),
    ('rules', [
        collections.OrderedDict([
            ('direction', 'layer-up'), ('functionality', 'ชั้นบนกำหนดว่าชั้นนี้ต้องทำอะไร — cube นี้รับข้อกำหนดลงมา'),
            ('risk', 'ต่ำ'), ('riskWhy', 'อยู่ในตึกเดียวกัน เจ้าของเดียวกัน เปลี่ยนพร้อมกันได้'),
            ('impact', 'จำกัดอยู่ในคอลัมน์เดียวของตึกนี้'),
            ('budgetDriver', 'การทวนสอบว่าข้อกำหนดถูกส่งต่อครบ'),
        ]),
        collections.OrderedDict([
            ('direction', 'layer-down'), ('functionality', 'ส่งข้อกำหนดต่อให้ชั้นล่างไปทำให้เป็นจริงในระดับที่รูปธรรมกว่า'),
            ('risk', 'ต่ำ'), ('riskWhy', 'อยู่ในตึกเดียวกัน เจ้าของเดียวกัน'),
            ('impact', 'จำกัดอยู่ในคอลัมน์เดียวของตึกนี้'),
            ('budgetDriver', 'การทวนสอบว่าสิ่งที่สร้างตรงกับข้อกำหนด'),
        ]),
        collections.OrderedDict([
            ('direction', 'zone-up'), ('functionality', 'รวมศูนย์ขึ้นไป — ขอบเขตกว้างขึ้น รอบเวลายาวขึ้น (data + spatial aggregation)'),
            ('risk', 'ปานกลาง'), ('riskWhy', 'ข้ามขอบเขตเวลาตอบสนอง ต้องมี buffering และ backpressure'),
            ('impact', 'กระทบทุก cube ที่ป้อนข้อมูลขึ้นมา'),
            ('budgetDriver', 'ตัวรวมข้อมูล ความจุจัดเก็บ และการกระทบยอด'),
            ('basis', 'SG-CG/M490/K §426–438'),
        ]),
        collections.OrderedDict([
            ('direction', 'zone-down'), ('functionality', 'กระจายลงไป — ขอบเขตแคบลง ต้องตอบสนองเร็วขึ้น (functional separation)'),
            ('risk', 'ปานกลาง–สูง'), ('riskWhy', 'ข้อกำหนดเวลาตอบสนองเข้มขึ้นทุกขั้นที่ลง ฟังก์ชัน real-time ต้องอยู่ที่ field/station'),
            ('impact', 'กระทบทุก cube ที่รับคำสั่งลงไป'),
            ('budgetDriver', 'ช่องสัญญาณที่รับประกันเวลา และการทดสอบ latency'),
            ('basis', 'SG-CG/M490/K §432–438'),
        ]),
        collections.OrderedDict([
            ('direction', 'x-left'), ('functionality', 'ไหลย้อนกลับตามห่วงโซ่คุณค่าหรือลำดับชั้นของระบบ'),
            ('risk', 'ปานกลาง'), ('riskWhy', 'ข้าม domain — คนละเจ้าของกระบวนการ แม้อยู่ตึกเดียวกัน'),
            ('impact', 'จำกัดอยู่ในชั้นและ zone เดียวกัน'),
            ('budgetDriver', 'ข้อตกลงระหว่างหน่วยงานภายใน'),
        ]),
        collections.OrderedDict([
            ('direction', 'x-right'), ('functionality', 'ไหลต่อไปตามห่วงโซ่คุณค่าหรือลำดับชั้นของระบบ'),
            ('risk', 'ปานกลาง'), ('riskWhy', 'ข้าม domain — คนละเจ้าของกระบวนการ แม้อยู่ตึกเดียวกัน'),
            ('impact', 'จำกัดอยู่ในชั้นและ zone เดียวกัน'),
            ('budgetDriver', 'ข้อตกลงระหว่างหน่วยงานภายใน'),
        ]),
    ]),
])

# ── cube attributes: what is derived, what is still waiting for a person ───────
inscope = 0
for t in m['towers']:
    X = [i[0] for i in t['xAxis']['items']]
    Y = [i[0] for i in t['yAxis']['items']]
    for l in t['layers']:
        for xi in range(len(X)):
            for yi in range(len(Y)):
                v = int(pop[l[0]][xi][yi]) if t['id'] == 'SGAM' else 3
                if v > 0:
                    inscope += 1
banded = sum(len(t['layers']) * len(t['xAxis']['items']) * len(t['yAxis']['items'])
             for t in m['towers'] if t['yAxis']['kind'] != 'lifecycle')

m['cubeAttributes'] = collections.OrderedDict([
    ('_note', 'มุมมองต่อ cube ตามคำศัพท์ของ ISO/IEC/IEEE 42010 และ ArchiMate — ไม่ใช่คำของ SG-CG '
              'เอกสารมาตรฐานทั้งสามฉบับที่ใช้อ้างอิงในโปรเจกต์นี้ไม่ได้นิยามคำเหล่านี้ไว้'),
    ('derived', collections.OrderedDict([
        ('functionality', collections.OrderedDict([
            ('from', 'ชั้นของ cube — นิยามชั้นตามมาตรฐานและคำอธิบายสั้นของ PCC'),
            ('coverage', f'{inscope}/{inscope} cubes ในขอบเขต'),
        ])),
        ('nonFunctionality', collections.OrderedDict([
            ('from', 'zone ของ cube — ระดับ H1–H6 และเวลาตอบสนองตาม docs/KNOWLEDGE.md §5'),
            ('coverage', f'{banded}/798 cubes'),
            ('excluded', 'RAMI 4.0 — แกนที่สามเป็น Life Cycle ไม่ใช่ Zone จึงไม่มีเวลาตอบสนอง'),
        ])),
    ])),
    ('authored', collections.OrderedDict([
        ('_note', 'ต้องมีคนตัดสิน สร้างเองไม่ได้ ช่องว่างนี้คือ backlog ที่วัดได้ ไม่ใช่ความบกพร่องที่ซ่อนไว้'),
        ('fields', ['goal', 'concern', 'constraint', 'requiredResources']),
        ('filled', 0),
        ('of', inscope * 4),
        ('owner', None),
        ('nextStep', 'ต้องมี Layer Architect ต่อชั้น L1–L8 และ Model Owner ต่อตึกก่อน ตาม governance'),
    ])),
])

P.write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('derived values regenerated — now run tools/verify.py')
