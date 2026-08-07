# Z-SGAM-L · Architecture Knowledge Base

เอกสารความรู้สำหรับโครงการ Architecture City · PCC · v3 · workshop draft

---

## 1. บริบท

PCC จัด workshop ภายในเรื่อง SGAM มีผู้บรรยาย 17 หัวข้อ หัวข้อ 1–16 แบ่งกันอธิบายทีละชั้น
ทีละ domain และแต่ละสถาปัตยกรรม **หัวข้อที่ 17 คือสล็อตปิด** ที่ต้องพิสูจน์ว่าทั้งหมดเป็นระบบเดียวกัน
ภายใต้ชื่อ *Architecture Structure to be Architecture Resiliency Development*

**Architecture Resiliency ในที่นี้ไม่ใช่ Grid Resiliency**

| | Grid Resiliency | Architecture Resiliency |
|---|---|---|
| ทนต่ออะไร | ไฟดับ พายุ อุปกรณ์เสีย | การเปลี่ยนแปลงของเทคโนโลยี กฎเกณฑ์ ผู้ขาย คน |
| วัดด้วย | SAIDI, SAIFI, N-1 | Blast radius — เปลี่ยนหนึ่งอย่างกระทบกี่ cube |
| กลไก | Redundancy, restoration | Change locality — แยกส่วนให้ผลกระทบไม่ลาม |
| ล้มเหลวเมื่อ | ไฟไม่กลับมา | ต้องรื้อสถาปัตยกรรมใหม่ทั้งก้อน |

> จิ๊กซอว์ที่ดีคือจิ๊กซอว์ที่ถอดชิ้นเดียวออกมาเปลี่ยนได้ โดยไม่ต้องตัดภาพใหม่ทั้งแผ่น

---

## 2. สี่สถาปัตยกรรม

| ตึก | อุตสาหกรรม | Layers | แกน X | แกน Y | Cubes |
|---|---|---:|---|---|---:|
| **SGAM · PCC** | ไฟฟ้า / สมาร์ทกริด | 7 | 5 Domains | 6 Zones | **210** |
| RAMI 4.0 | การผลิต / โรงงาน | 6 | 7 Hierarchy levels | **4 Life cycle** | 168 |
| SCIAM | เมือง | 5 | 8 Domains | 6 Zones | 240 |
| SFAM | เกษตร | 6 | 5 Domains | 6 Zones | 180 |
| | | | | **รวม** | **798** |

SGAM ของ PCC = SGAM มาตรฐาน 5 ชั้น + **Intelligence** + **Cyber**

---

## 3. หลักการรวม — Federated ไม่ใช่ Unified

| แบบ | แนวคิด | ผล |
|---|---|---|
| Unified | ยุบสี่โมเดลเป็นหนึ่ง | **ล้มเหลว** — แกน Life Cycle ของ RAMI ไม่ใช่แกน Zone การยุบทำลายความหมาย |
| Parallel | ต่างคนต่างทำ | **ล้มเหลว** — ลงทุนซ้ำสี่รอบ |
| **Federated** | แกนร่วมเป็นมาตรฐานเดียว แต่ละโมเดลมีอธิปไตย เชื่อมเฉพาะจุดที่กำหนด | **ใช้ได้จริง** |

**กฎการ normalize:** ปรับแกน Z และ Y ให้เป็นบัญญัติร่วม — **ปล่อยแกน X ให้เป็นอิสระ**
เพราะ Domain คือเหตุผลที่แต่ละโมเดลมีอยู่ ถ้ายุบก็ไม่ต้องมีสี่โมเดล

---

## 4. แกน Z · แปดชั้นร่วม

| ชั้น | ความหมาย | SGAM มาตรฐาน | **SGAM · PCC** | RAMI 4.0 | SCIAM | SFAM | ชนิดการเชื่อม |
|---|---|---|---|---|---|---|:-:|
| L8 | Purpose | Business | Business | Business | Business | Business | A |
| L7 | Capability | Function | Function | Functional | Function | Function | D |
| L6 | Cognition | — | **Intelligence** | — | — | — | D |
| L5 | Semantics | Information | Information | Information | Information | Information | C |
| L4 | Exchange | Communication | Communication | Communication | Communication | Communication | B |
| L3 | Trust | — | **Cyber** | — | — | — | E |
| L2 | Digitization | — | **⚠ ไม่มี** | Integration | — | Integration | B |
| L1 | Physical | Component | Component | Asset | Component | Asset | A |

### 4.1 สามจุดที่เราเบี่ยงจากมาตรฐาน — ประกาศไว้ ไม่ใช่ซ่อนไว้

`SG-CG/M490/K` Table 3 กำหนด interoperability layer ของ SGAM ไว้ **5 ชั้น** ที่เพิ่มมาสองชั้นเป็นของ PCC เอง
รายละเอียดเต็มอยู่ใน `data/architecture-model.json` → `deviations`

| # | เบี่ยงตรงไหน | ราคาที่ต้องจ่าย |
|---|---|---|
| DEV-01 | เพิ่ม **L6 Intelligence** ซึ่งไม่มีใน SGAM มาตรฐาน | agent ต้อง dock ลง L7 ของตึกอื่นแบบไม่สมมาตร ภาระกำกับตกที่ PCC → F2 |
| **DEV-02** | เพิ่ม **L3 Cyber** เป็นชั้น — แต่ **§6.3 ของมาตรฐานถือว่า security เป็นข้อกำหนดที่พาดขวางทุกชั้น ไม่ใช่ชั้นแยก** | คนที่อ่าน SG-CG มาจะหาชั้นนี้ไม่เจอ และอาจเข้าใจผิดว่า security อยู่แค่ L3 ต้องอธิบายทุกครั้งที่นำเสนอ |
| DEV-03 | population map วัด **ความครบของเอกสาร** ส่วน §5.5 ของมาตรฐานวัด **ระดับ abstraction** | สองแกนคนละความหมายถูกยุบเป็นตัวเลขเดียว |

> DEV-02 สำคัญที่สุด — ไม่ใช่แค่ "เพิ่มชั้น" แต่เป็นการ**ตีความต่างจากมาตรฐาน** ต้องพูดให้ชัดในห้อง
> ก่อนที่จะมีคนถาม ไม่ใช่หลังจากนั้น

### 4.2 ขอบเขตที่ SGAM ประกาศว่าตัวเองไม่ทำ

`SG-CG/M490/K §383–391` — เก็บไว้ใน `scopeLimits` ข้อแรกคือเหตุผลของแอปนี้ทั้งแอป

> *SGAM ไม่จำเป็นต้องทำให้สถาปัตยกรรมของ domain เดียวหรือ zone เดียวดีขึ้น
> **แต่แสดงพลังเต็มที่ตอนโมเดล interaction ระหว่าง domain และ zone***

อีกสี่ข้อ: ไม่แทน requirements spec · ไม่แทน development spec · ไม่โมเดลฟิสิกส์ใน process zone
(harmonics, voltage sag) · ไม่แทนข้อกำหนดความปลอดภัยหรือเงื่อนไขการเดินระบบ

## 5. แกน Y · หกระดับร่วม

| ระดับ | SGAM / SCIAM | RAMI 4.0 | SFAM | เวลาตอบสนอง |
|---|---|---|---|---|
| H6 Ecosystem | Market | Connected world | Connected world | ชั่วโมง – วัน |
| H5 Enterprise | Enterprise | Enterprise | Management information | นาที – ชั่วโมง |
| H4 Operation | Operation | Work centre | Operation execution | วินาที |
| H3 Station | Station | Station | Production control | 10 – 100 ms |
| H2 Device | Field | Control device + Field device | Sensing & actuation | 3 – 20 ms |
| H1 Physical | Process | Product | Physical objects | ต่ำกว่า 4 ms |

RAMI ยุบสองระดับเป็นหนึ่งที่ H2 — ยอมรับได้ แต่ต้องบันทึกไว้

**⚠ แกน Life Cycle ของ RAMI ไม่ได้อยู่ในตารางนี้** เพราะเป็นแกนที่สี่ที่ SGAM ไม่มีเลย
และ **ไม่ใช่ Zachman Rows** ซึ่งเป็นระดับความละเอียดของคำอธิบาย ไม่ใช่วงจรชีวิตของของ

---

## 6. กับดักคำศัพท์ 3 อัน

| กับดัก | อาการ | ความจริง |
|---|---|---|
| คำเดียวกัน คนละความหมาย | "Station" อยู่ทั้ง SGAM และ RAMI | SGAM = สถานีไฟฟ้าย่อย · RAMI = สถานีการผลิต |
| คนละคำ ความหมายเดียวกัน | Component (SGAM, SCIAM) vs Asset (RAMI, SFAM) | ชั้นเดียวกัน ต่างแค่ธรรมเนียมวงการ |
| **แกนที่สามไม่เหมือนกัน** | RAMI ดูเหมือนมีสามแกนเหมือนตึกอื่น | แกนที่สามคือ Life Cycle **อันตรายที่สุด** ถ้าเทียบตรง ๆ |

---

## 7. ชนิดการเชื่อม A–E

**นี่คือฉบับแก้ไข** ฉบับแรกระบุว่า "คู่กันได้เฉพาะ L1 กับ L8" ซึ่งผิด
ชั้นกลางคู่กันได้จริง — IEC 61850 ↔ OPC UA gateway มีของจริง, CIM ↔ AAS mapping ก็มีคนทำ
ที่ถูกคือ **คู่ได้ทุกชั้น แต่คนละชนิดกัน และแต่ละชนิดมีต้นทุนกับความเสี่ยงต่างกัน**

| ชนิด | ชั้น | ความหมาย | ทิศทาง | เสี่ยง | ต้องมี | จำนวน |
|---|---|---|---|---|---|---:|
| **A** Identity | L1, L8 | อ้างถึงสิ่งเดียวกัน ไม่ต้องเปิดโครงสร้างภายใน | สองทาง | ต่ำ | รหัสประจำตัวเดียวที่ทั้งสองยอมรับ | 15 |
| **B** Contract | L2, L4 | คุยผ่าน gateway ที่มีสัญญาและเวอร์ชัน | สองทาง | ปานกลาง | ICD + conformance test | 4 |
| **C** Translation | L5 | แปล semantic มีการสูญเสียเสมอ | มีทิศทาง | ปานกลาง–สูง | source of truth ฝั่งเดียว + ทดสอบ mapping เป็นรอบ | 3 |
| **D** Orchestration | L6, L7 | use case หรือ agent คร่อมสองตึก | สองทาง | สูง | ลงทะเบียนส่วนกลาง + decision rights + ปุ่มหยุด | 6 |
| **E** Federated trust | L3 | ตัวตนข้ามตึก | ทางเดียว | สูง | trust anchor ชัดเจน ห้ามยอมรับกันไปกลับ | 2 |

**Hourglass ยังจริง แต่เป็นเรื่องต้นทุน ไม่ใช่ข้อห้าม** — คอขวดตรงกลางแคบเพราะแพงและเปราะ
ไม่ใช่เพราะทำไม่ได้ หลีกเลี่ยงเมื่อมีทางเลือก แต่ถ้าจำเป็นก็ทำได้ด้วยกลไกที่ถูกชนิด

---

## 8. กฎการออกแบบ D1–D7

| # | กฎ | เหตุผล |
|---|---|---|
| D1 | Normalize แกน Z และ Y — federate แกน X | Domain คือเหตุผลที่แต่ละโมเดลมีอยู่ |
| D2 | หนึ่ง cube หนึ่งโมเดล ห้ามถือสองสัญชาติ | ของสองฝ่าย = ไม่มีใครรับผิดชอบ |
| **D3** | **ทุกชั้นคู่กันได้ แต่ต้องใช้กลไกที่ถูกชนิด (A–E)** | *แก้จากฉบับแรก* |
| D4 | ทุกรอยต่อต้องมี contract artifact ที่มีชื่อ เลขที่ เจ้าของ | รอยต่อไม่มีเอกสาร = ไม่มีอยู่จริง |
| D5 | Lifecycle บังคับเฉพาะของที่ผลิต | ไม่แบกความซับซ้อนที่ไม่ได้ใช้ |
| D6 | Agent ข้ามโมเดลได้ แต่ต้องลงทะเบียนส่วนกลาง | agentic use case คร่อมโมเดลโดยธรรมชาติ |
| D7 | วัด blast radius ข้ามโมเดล | ความเปราะบางซ่อนที่รอยต่อเสมอ |

---

## 9. Population map ของ SGAM

3 = core (เอกสารครบ 6 คอลัมน์) · 2 = supporting · 1 = reference · 0 = out of scope
แถว = domain (GEN, TRA, DIS, DER, CUS) · หลัก = zone (MKT, ENT, OPS, STA, FLD, PRO)

```
BUS  221000 232000 332000 333000 333000
FUN  122110 233211 233321 333321 333121
INT  112210 123321 223321 333332 323121
INF  122210 233321 233321 333321 333121
COM  012221 123332 123332 223332 223132
CYB  022210 133321 133321 233332 233121
CMP  001222 012333 012333 012333 012133
```

| ตัวเลข | ค่า |
|---|---:|
| ในขอบเขต | 183 / 210 |
| Core | 79 |
| Seam-eligible (ชั้น BUS + CMP) | 39 |
| ระบุสัญญาแล้ว | 15 |
| **ช่องว่างที่ยังไม่มีเจ้าภาพ** | **24** |

**สังเกตแนวทแยง** — น้ำหนักไหลจากมุมซ้ายบน (Business × Market) ไปมุมขวาล่าง (Component × Process)
ถ้า population map ออกมาเป็นสี่เหลี่ยมทึบเต็มทุกช่อง แปลว่ากำลัง over-engineer

---

## 10. สี่ข้อค้นพบเชิงโครงสร้าง

**F1 · SGAM ของ PCC ขาดชั้น L2 Digitization** — RAMI และ SFAM มี ชั้นนี้คือชั้นที่แปลงของกายภาพ
เป็นของดิจิทัล PCC ผลิตอุปกรณ์เองจึงควรมี ผลคือมี coupling หนึ่งเส้น (RAMI ↔ SFAM ที่ L2)
ที่ **PCC เข้าร่วมไม่ได้** ทางเลือก: เพิ่มเป็นชั้นที่ 8 (จะได้ 240 cubes) หรือประกาศชัดว่าถูกดูดเข้า
Component layer แล้ว

**F2 · ชั้น L6 และ L3 ของ PCC ไม่มีคู่ให้เชื่อม** — อีกสามตึกไม่มีสองชั้นนี้ agent และ identity
ต้อง dock ลงมาที่ L7 หรือ L4 ของตึกปลายทางแบบไม่สมมาตร ผลคือ **ภาระการกำกับ agent
ตกอยู่ที่ PCC ฝ่ายเดียวทั้งหมด** — เป็นราคาของการเป็นตึกที่สูงที่สุดในเมือง ต้องตั้งงบ Agent Registrar ไว้

**F3 · แกนที่สามของ RAMI คือ Life Cycle** — กับดักที่อันตรายที่สุด ถ้าเทียบกับ Zone ตรง ๆ
จะได้สถาปัตยกรรมที่ผิดตั้งแต่ต้นและหาไม่เจอจนสร้างไปครึ่งทาง

**F4 · รอยต่อ SGAM ↔ SFAM ผ่านธุรกิจไผ่คือทรัพย์สินที่ยังไม่ได้ใช้** — ไผ่ → biochar → biomass
→ Generation domain และวนกลับผ่านโหลดชลประทาน คู่แข่งที่ทำสมาร์ทกริดอย่างเดียวไม่มีรอยต่อนี้
เป็นคำตอบที่เป็นรูปธรรมที่สุดว่า Ecosystem Capitalism หน้าตาเป็นอย่างไรสำหรับ PCC

---

## 11. Governance

| บทบาท | ใคร | อำนาจ |
|---|---|---|
| Architecture Review Board | ประธาน + Model Owner ทั้งสี่ | อนุมัติ coupling contract, ตัดสินข้อขัดแย้งข้ามตึก |
| Model Owner | หนึ่งคนต่อตึก | Baseline โมเดลของตัวเอง |
| Layer Architect | ตามชั้น L1–L8 | เนื้อหา cube ในชั้นนั้น |
| **Agent Registrar** | ส่วนกลาง | อนุมัติ agent ที่ข้ามตึกตามกฎ D6 — **บทบาทใหม่ที่ไม่มีในกรอบ EA ดั้งเดิม** |

ถ้าไม่ตั้งบทบาท Agent Registrar กฎ D6 จะกลายเป็นช่องโหว่ที่ทุกคนใช้เลี่ยง

---

## 12. การเดินตามอุปกรณ์ชิ้นเดียว — เครื่องมือสื่อสารที่ได้ผลที่สุด

ไดอะแกรมอธิบายโครงสร้างได้ แต่ไม่ทำให้คน *รู้สึก* ว่ามันเชื่อมกัน ใช้ RMU 22 kV ที่ PCC ผลิตเอง

| # | เกิดอะไร | สถาปัตยกรรม | พิกัด |
|---|---|---|---|
| 1 | ออกแบบ RMU | RAMI 4.0 | Type · Development |
| 2 | ผลิตที่โรงงาน PEM | RAMI 4.0 | Instance · Production |
| 3 | ได้ Digital Product Passport | **รอยต่อ 1** | RAMI Asset ↔ SGAM Component |
| 4 | ติดตั้งบน feeder 22 kV | SGAM | `CMP.DIS.FLD` |
| 5 | ส่งค่าวัดตาม IEC 61850 | SGAM | ไต่ COM → INF |
| 6 | Agent สับ feeder ใหม่ตอนไฟตก | SGAM | `INT.DIS.OPS` |
| 7 | Feeder จ่ายไฟให้อาคาร | **รอยต่อ 2** | SGAM Customer ↔ SCIAM Buildings |
| 8 | Feeder จ่ายไฟให้ปั๊มน้ำแปลงไผ่ | **รอยต่อ 3** | SGAM Customer ↔ SFAM Cultivation |
| 9 | ไผ่แปรเป็น biochar และ biomass | SFAM | Processing |
| 10 | Biomass เข้าโรงไฟฟ้า → **กลับข้อ 4** | **รอยต่อ 4** | SFAM Distribution ↔ SGAM Generation |

**วงจรปิดพอดี** — เริ่มที่โรงงาน จบที่แปลงไผ่ที่ป้อนไฟกลับเข้าโรงงาน

---

## 13. สิ่งที่ยังต้องยืนยันก่อน baseline

1. ตัวเลข layer / domain / zone ของ **SCIAM และ SFAM** อ่านจากไดอะแกรม ต้องให้เจ้าภาพหัวข้อ 12–14 ยืนยัน
   — ✅ **RAMI ปิดแล้ว** แกน Hierarchy Levels ตาม IEC 62264 แกน Life Cycle & Value Stream ตาม IEC 62890
   (ยืนยันจาก *RAMI 4.0 and OFFIS Tools*, Meister/OFFIS 2017 น.3)
2. Coupling ทั้ง 30 เส้นเป็นข้อเสนอจากบริบทธุรกิจ PCC ไม่ใช่มาตรฐาน — กลุ่ม A มั่นใจสุด กลุ่ม D ต้องตรวจสอบมากสุด
3. อีกสามตึกยังไม่มี population map ต้องมี Model Owner ก่อน
4. Blast radius ยังเป็นค่าประมาณเชิงโครงสร้าง ควรแทนด้วยค่าที่วัดจาก dependency จริง
5. ช่องว่าง 24 seam positions ที่ยังไม่มีเจ้าภาพ — เป็นวาระของ Architecture Review Board
6. แผน biomass power ของธุรกิจไผ่อยู่ระยะไหนแล้ว ก่อนใช้ F4 เป็นข้อเสนอเชิงกลยุทธ์

---

## 14. ไฟล์อื่นในชุดเดียวกัน

ผลิตไว้ก่อนหน้า ไม่ได้อยู่ใน repo นี้ แต่ใช้ข้อมูลชุดเดียวกัน

| ไฟล์ | ใช้ตอนไหน |
|---|---|
| `Z-SGAM-L_Cube_Explorer.html` | ทำงานจริง ไล่ดู 210 cube ทีละก้อน |
| `Z-SGAM-L_Federated_Explorer.html` | 3 แท็บ — cubes, federation, seam register |
| `Z-SGAM-L_Isometric_Designer.html` | SGAM ตึกเดียว + ดาวเทียมสามดวง |
| **`Architecture_City_v3.html`** | **สี่ตึกเต็ม — ตัวที่ deploy** |
