# Standards Review · ข้อเสนอการปรับปรุง Architecture City

ทบทวน Architecture City v3 เทียบกับเอกสารอ้างอิงสามฉบับ · workshop draft · ยังไม่ baseline

| # | เอกสาร | สถานะ |
|---|---|---|
| R1 | **SG-CG/M490/K_ SGAM User Manual v3.0** (CEN-CENELEC-ETSI, 11/2014) | มาตรฐาน — เป็นแหล่งอ้างอิงหลักของตึก SGAM |
| R2 | **RAMI 4.0 and OFFIS Tools for Editing and Visualization** (Meister, OFFIS, 04/2017) | สไลด์นำเสนอ — ยืนยันแกนของ RAMI |
| R3 | **How to Build a Digital Business Technology Platform** (Gartner G00743206, 03/2021) | บทวิเคราะห์เชิงบริหาร ไม่ใช่มาตรฐานสถาปัตยกรรม |

> **⚠ R3 มีข้อจำกัดลิขสิทธิ์** ระบุในไฟล์ว่า *"restricted to the personal use of .vainikka@cognite.com"*
> และ *"may not be reproduced or distributed in any form without Gartner's prior written permission"*
> แอปนี้ deploy ขึ้น GitHub Pages แบบสาธารณะ — **ห้ามฝังรูป ตาราง หรือข้อความจาก R3 ลงในแอป**
> ใช้ได้แค่เป็นกรอบความคิดที่เขียนใหม่ด้วยคำของเราเอง ตามที่ทำในข้อ S11–S12

---

## ส่วนที่ 1 · ข้อบกพร่องที่เจอในตัวโค้ดปัจจุบัน

ตรวจพบระหว่างรีวิว ไม่ใช่ข้อเสนอ — เป็นของที่พังอยู่จริง

### ✗ D-1 · `note` ของทั้งสี่ตึกเป็น dead data

`TOWERS[].note` เขียนไว้ครบทั้งสี่ตึก มีเนื้อหาดีมาก โดยเฉพาะของ RAMI ที่เตือนเรื่องแกนที่สาม

```js
note:"6 ชั้น × 7 hierarchy × 4 life cycle = 168 cubes · ตึกเดียวที่แกนที่สามเป็น
      Life Cycle ไม่ใช่ Zone อย่าเอาไปเทียบกับ Zone ของตึกอื่นตรง ๆ"
```

แต่ `grep '\.note' app/index.html` ไม่เจอการอ้างถึงเลยนอกจากใน literal — **ไม่เคยถูก render**
คำเตือนที่สำคัญที่สุดของโปรเจกต์ (F3 ใน KNOWLEDGE.md) จึงไม่เคยขึ้นจอ

**แก้:** แสดง `note` ในแผงรายละเอียดเมื่อคลิกชื่อตึก และติด badge ถาวรบนตึก RAMI

### ✗ D-2 · สีของ coupling type ชนกับสีของชั้น ผิด convention ที่เขียนไว้เอง

`CLAUDE.md` เขียนว่า *"Never reuse a level colour for a coupling type"*
แต่วัดระยะสี CIE76 ในธีมสว่างได้ผลนี้ (ΔE < 20 = แยกไม่ออกด้วยตา บนโปรเจกเตอร์ยิ่งแย่กว่า)

| coupling type | สีที่ใช้ | ชั้นที่ชนกัน | ΔE |
|---|---|---|---:|
| **D** Orchestration | `#5A3FBF` | L6 `#6A3DBF` | **4.6** |
| **C** Translation | `#B27400` | L5 `#A96A00` | **4.9** |
| **E** Federated trust | `#B23B1E` | L3 `#C0392B` | **7.4** |
| **B** Contract | `#0E7C6B` | L4 `#12795A` | **8.7** |
| **A** Identity | `#B0234A` | L8 `#C2185B` | **10.8** |

ไม่ใช่เรื่องบังเอิญ — แต่ละ type ถูกให้สีของ "ชั้นหลัก" ของตัวเอง (A→L8, B→L4, C→L5, D→L6, E→L3)
เป็นการทำ mnemonic ที่ตั้งใจ แต่**ขัดกับ convention ที่เขียนไว้เอง** และทำให้บนจอโปรเจกเตอร์
เส้น coupling type D กับ node ชั้น L6 กลายเป็นสีเดียวกัน

**ต้องเลือกหนึ่งอย่าง:**
- (ก) รักษา mnemonic ไว้ → **แก้ convention ใน CLAUDE.md** ให้ตรงกับของจริง แล้วแยกด้วย *รูปทรง* แทน
  (เส้นทึบ/ประ/หัวลูกศร) ไม่ใช่สี
- (ข) รักษา convention ไว้ → **เปลี่ยน palette ของ A–E** ให้ห่างจากสีชั้นอย่างน้อย ΔE 25

แนะนำ (ก) — mnemonic มีค่าจริงในการบรรยาย และเส้นกับจุดแยกกันด้วยรูปทรงอยู่แล้ว

### ✗ D-3 · โครงสร้าง x-axis ในแอปกับใน JSON ไม่ตรงกัน

JSON เก็บสามค่า `["GEN","Generation","ผลิตไฟฟ้า"]` แต่แอปเก็บสองค่า
และ SGAM ใช้ช่องที่ 2 เป็น**ภาษาไทย** ขณะที่ RAMI/SCIAM/SFAM ใช้เป็น**ภาษาอังกฤษ**

```js
SGAM  xs:[["GEN","ผลิตไฟฟ้า"], ...]      // [1] = ไทย
RAMI  xs:[["PRD","Product"], ...]         // [1] = อังกฤษ
```

ผลคือแผงรายละเอียดแสดงชื่อ domain ของ SGAM เป็นไทย แต่ของตึกอื่นเป็นอังกฤษ ไม่สม่ำเสมอ
และเสียชื่อทางการภาษาอังกฤษของ domain SGAM ไป ทั้งที่ R1 Table 1 กำหนดไว้ชัด

**แก้:** ใช้สามค่าให้เหมือน JSON ทุกตึก แล้วแสดง `อังกฤษ · ไทย` — ตรงกับ convention
"Thai UI copy with English technical terms inline"

---

## ส่วนที่ 2 · ข้อเสนอจากมาตรฐาน

### 🔴 S1 · เพิ่ม Use Case register — ช่องว่างที่ใหญ่ที่สุด

R2 หน้า 7 พูดตรง ๆ ว่า:

> *"3D Visualization of RAMI 4.0 Models is only the last step in the Requirements Engineering
> for Industrie 4.0. Especially, **Use Case Analysis and Modeling must be done beforehand**."*

นี่คือคำวิจารณ์ตรงตัวต่อสิ่งที่ Architecture City เป็นอยู่ตอนนี้ — เป็น visualization ที่ไม่มี
artifact ต้นน้ำรองรับ และ R1 ทั้งฉบับ (บทที่ 6 ทั้งบท) วางอยู่บนฐานว่า **use case คือหน่วยวิเคราะห์หลักของ SGAM**

ปัจจุบัน coupling มีแค่ `mechanism` + `rationale` ไม่มี use case object เลย ทั้งที่ CPL-16
อ้างถึง *"Cross-domain use case (IEC 62559)"* ในชื่อ mechanism ของตัวเอง

**เสนอ:** เพิ่ม `useCases[]` ใน JSON ตามเทมเพลต **IEC 62559-2** โดยใช้ classification ของ R1 §6.2.1

| ระดับ | ตาม R1 | ใช้กับอะไรใน PCC |
|---|---|---|
| Use case concept / HL-UC | บทบาทและความรับผิดชอบ ยังไม่มี business model | ระดับ "ทำไมต้องเชื่อมสองตึกนี้" |
| Business use case | กระบวนการธุรกิจ ไม่มีมุมเทคนิค → **BUS layer** | coupling type A ที่ L8 |
| System / device use case | ขอบเขตระบบ interaction กับ actor ภายนอก → **FUN layer** | coupling type D ทั้ง 6 เส้น |

พร้อม field ขั้นต่ำจาก R1 Table 5 (use case checklist): ชื่อเป็น *verb + description*,
domain(s) & zone(s), scope/boundary, actors ที่อยู่ชั้นเดียวกัน, relation to other use cases,
references (มาตรฐาน/กฎหมาย/grid code), information exchanged, requirements (QoS/privacy/security),
**threat & risk analysis**

### 🔴 S2 · coupling ขาด `owner` — ทั้งที่กฎ D4 บังคับไว้เอง

`KNOWLEDGE.md` D4 เขียนว่า *"ทุกรอยต่อต้องมี contract artifact ที่มีชื่อ เลขที่ เจ้าของ"*
แต่ schema ของ coupling มีแค่ `id / from / to / type / mechanism / rationale / standards / flag`
— **ไม่มีทั้งเลขที่สัญญาและเจ้าของ** กฎ D4 จึงบังคับใช้ไม่ได้เลยในทางเทคนิค

นี่คือสาเหตุที่ตัวเลข "15 named / 24 unassigned" อยู่แค่ในเอกสาร ตรวจสอบอัตโนมัติไม่ได้

**เสนอ:** เพิ่ม `contractId`, `owner`, `status` (draft / review / approved by ARB), `reviewDate`
แล้วเพิ่ม assertion ใน verification script ว่า coupling ที่ `status: approved` ต้องมี owner ครบ
→ ได้ Seam Contract Register ที่ export เป็น CSV/XLSX ได้ทันที (known gap ข้อ 2)

### 🟠 S3 · SG-CG ถือว่า security เป็น cross-cutting ไม่ใช่ชั้น — PCC เบี่ยงจากมาตรฐาน

R1 §6.3 (Figure 10–11) วาง security requirement **พาดขวางทุกชั้น** ไล่จาก
risk level → security level (SGIS) → functional requirement → mechanism → technical + procedural
ไม่ได้มีชั้น "Cyber" แยกใน SGAM มาตรฐาน

PCC เลือกเพิ่ม **CYB เป็นชั้น L3** ซึ่งเป็นการตัดสินใจที่มีเหตุผล แต่ **เบี่ยงจาก R1**
และ KNOWLEDGE.md ยังไม่ได้บันทึกว่านี่คือการเบี่ยง

**เสนอ:** บันทึกเป็น deviation ที่ประกาศชัด แบบเดียวกับที่ทำกับกับดัก RAMI life cycle
พร้อมเหตุผล และเพิ่มโหมด **security overlay** ที่ไฮไลต์ security requirement รายชั้น
แทนที่จะเห็นแค่พื้น L3 — จะได้ตอบได้ทั้งสองภาษาเวลาคนถามในห้อง

### 🟠 S4 · ประเภทเครือข่ายสื่อสาร A–N ของ R1 คือชุดข้อมูลสำเร็จรูปของชั้น COM

R1 §7.3.2 นิยามประเภทเครือข่าย 11 แบบ พร้อม **แผนที่ลงบนระนาบ SGAM** ให้แล้ว (Figure 16)

| | เครือข่าย | | เครือข่าย |
|---|---|---|---|
| A | Subscriber Access | F | Inter-substation |
| B | Neighborhood | G | Intra-Control/Data Centre |
| C | AMI backhaul | H | Backbone |
| D | Low-end intra-substation | L | Operation Backhaul |
| E | Intra-substation | M | Industrial Fieldbus |
| | | N | Home & Building integration bus |

ชั้น COM ตอนนี้เป็น cube เปล่า ๆ ทั้งที่มีข้อมูลมาตรฐานรออยู่ — และ **CPL-27 (Shared LPWAN backhaul)
คือประเภท (B) Neighborhood Network ตรงตัว** การผูกแบบนี้ทำให้ coupling มีที่ยืนตามมาตรฐาน
แทนที่จะเป็นข้อเสนอลอย ๆ

### 🟡 S5 · รายชื่อระบบ (R1 Table 7) ใช้เติมชั้น CMP ได้ทันที + เจอ pattern ที่แอปแสดงไม่ได้

R1 แบ่งระบบเป็นสามชนิด: domain-specific, function-specific (คร่อม domain),
และ **Administration systems** (asset management, clock reference, communication management,
**authentication authorization accounting**) ซึ่ง *"usually present in all the above"*

**Administration system พาดขวางทุก domain** — แอปตอนนี้วาดได้แค่ node ต่อ cube
แสดง pattern แบบพาดขวางไม่ได้เลย และสังเกตว่า **AAA system เกี่ยวโดยตรงกับชั้น L3 Trust ของ PCC**
ซึ่งช่วยหนุนเหตุผลของ S3

### 🟡 S6 · ชั้น BUS ควรผูกกับ Harmonized Role Model

R1 §7.2 (Figure 15) แม็ป HRM ลง SGAM และ Table 5 กำชับว่า
*"ensure that for business use cases the roles are based on the Conceptual Model or the
Harmonized Role Model to ensure EU-wide applicability"*

ตอนนี้ตาราง governance ใน KNOWLEDGE.md §11 เป็นบทบาท**ภายในองค์กร PCC** (ARB, Model Owner,
Layer Architect, Agent Registrar) ซึ่งคนละเรื่องกับ **market role** ตาม HRM
(Supplier, Aggregator, BRP, DSO, TSO…) — ควรมีทั้งสองชุด อย่าปนกัน

### 🟡 S7 · แยก "ระดับความละเอียด" ออกจาก "ความครบของเอกสาร"

R1 §5.5 นิยาม **SGAM analysis pattern** — แต่ละชั้นมีระดับ abstraction ของตัวเอง
ไล่จาก concept → ... → detailed (ถึงระดับ product บนชั้น component, business case บนชั้น business)

แต่ population map ของ PCC (3=core, 2=supporting, 1=reference, 0=out of scope) เป็นสเกล
**ความครบของเอกสาร** ไม่ใช่ระดับ abstraction — คนละแกนกันคนละความหมาย ตอนนี้ปนกันอยู่ในตัวเลขเดียว

**เสนอ:** แยกเป็นสองคุณสมบัติ `completeness` (ของเดิม) และ `abstractionLevel` (ตาม R1)
เพราะ cube หนึ่งอาจมีเอกสารครบแต่ยังอยู่ระดับ concept ก็ได้

### 🟢 S8 · ใส่นิยาม domain/zone ตาม R1 Table 1–2 โดยเฉพาะเส้นแบ่ง DER ↔ Customer Premises

R1 §412–418 วางกฎแบ่งที่คมมาก และเป็นจุดที่คนสับสนบ่อยที่สุด:

> **DER** = มีเป้าหมายธุรกิจหลักคือ**ป้อนเข้ากริด** (production / storage / ancillary services)
> **Customer Premises** = กระบวนการที่**ไม่ได้**มีเป้าหมายหลักป้อนเข้ากริด (ใช้กริดเป็นแหล่งพลังงาน)

ทั้งสอง domain มีการผลิตไฟได้เหมือนกัน — เส้นแบ่งอยู่ที่**เจตนาทางธุรกิจ ไม่ใช่เทคโนโลยี**
สำคัญกับ PCC โดยตรง เพราะ CPL-09 (agrivoltaic) อยู่ DER แต่ CPL-06 (EV) อยู่ Customer Premises

เช่นเดียวกับ zone: R1 §426–438 อธิบายว่า zone ประกอบด้วยสองแนวคิด — **aggregation**
(data + spatial) และ **functional separation** (real-time อยู่ field/station เสมอ)
`relWhy()` ตอนนี้อธิบายแค่ aggregation ขาด functional separation ไป

### 🟢 S9 · เอา "ขอบเขตที่ SGAM ไม่ทำ" ขึ้นจอ — เกราะกันคำถามในห้องประชุม

R1 §383–391 ระบุข้อจำกัดของตัวเองไว้ห้าข้อ ตรงไปตรงมา แปลได้ว่า

- SGAM ไม่ได้ทำให้สถาปัตยกรรมของ domain เดียวหรือ zone เดียวดีขึ้น
  **แต่แสดงพลังเต็มที่ตอนโมเดล interaction ข้าม domain และ zone**
- ช่วย derive system requirement แต่**ไม่แทน** requirement specification
- **ไม่แทน** development specification
- **ไม่โมเดล** ฟิสิกส์ของระบบไฟฟ้าใน process zone (harmonics, voltage sag)
- **ไม่แทน** ข้อกำหนดความปลอดภัยหรือเงื่อนไขการเดินระบบ

ข้อแรกคือ **thesis ของ Architecture City ทั้งแอปพูดโดยมาตรฐานเอง** — ควรยกมาอ้างตรง ๆ
ส่วนอีกสี่ข้อคือคำตอบสำเร็จรูปเวลาโดนถามว่า "ทำไมโมเดลนี้ไม่มีเรื่อง X"

### 🟢 S10 · อ้างที่มาของแกน RAMI ให้ชัดในแอป

R2 หน้า 3 ยืนยันแกนทั้งสามพร้อมมาตรฐานกำกับ — **ใช้ปิดข้อ 1 ใน KNOWLEDGE.md §13 ได้เลย**
(รายการที่ระบุว่า "อ่านจากไดอะแกรม ต้องให้เจ้าภาพยืนยัน") อย่างน้อยสำหรับ RAMI

| แกน | ที่มา |
|---|---|
| Hierarchy Levels (Product → Connected World) | **IEC 62264** |
| Life Cycle & Value Stream | **IEC 62890** |
| Layers | interoperability ICT layers |

ยังเหลือ SCIAM กับ SFAM ที่ต้องหาแหล่งอ้างอิงต่อ

### 🟢 S11 · กรอบ Sense → Decide → Act สำหรับ coupling type D

R3 เสนอว่า digital use case มีสามจังหวะ: รับรู้ → ตัดสินใจ → ลงมือ
วางทับชั้นของเราได้พอดี — **Sense** L1/L2/L4 · **Decide** L5/L6/L7 · **Act** L4/L1

เป็นวิธีเล่าที่ผู้บริหารเข้าใจใน 5 วินาที และเหมาะกับ coupling type D ทั้ง 6 เส้นที่เป็น
agent/use case คร่อมตึก โดยเฉพาะ CPL-16 (สั่งปั๊มชลประทานตามพยากรณ์ PV) ที่เดินครบสามจังหวะ

*(เขียนใหม่ด้วยคำของเราเอง ไม่คัดลอกจาก R3 — ดูข้อจำกัดลิขสิทธิ์ด้านบน)*

### 🟢 S12 · อธิบาย coupling type B ด้วยภาษา mediated API

R3 อธิบาย MASA ว่าแยก **outer API** (สำหรับผู้ใช้ภายนอก มี security + traffic management)
ออกจาก **inner API** (ของระบบเดิม) ซึ่งตรงกับนิยาม type B ของเราพอดี —
*"คุยผ่าน gateway ที่มีสัญญาและเวอร์ชัน ถอดเปลี่ยนได้"* เป็นคำอธิบายเสริมที่คนสาย IT คุ้นกว่า

### 🟢 S13 · Export ให้ round-trip กลับเข้าเครื่องมือมาตรฐานได้

R2 หน้า 8 แสดง toolchain ที่แลกเปลี่ยนผ่าน Word/HTML/XML, Visio XML, **UCMR**,
OpenDocument Spreadsheet และ "SGAM in Excel" — ทั้งหมดเชื่อมเข้า **RAMI Toolbox for Enterprise Architect**

ถ้า export ได้ตามรูปแบบเหล่านี้ Architecture City จะเลิกเป็นทางตัน กลายเป็นหน้าต่างบานหนึ่ง
ของ toolchain ที่มีอยู่แล้ว — และ R1 §9.5 ก็ปิดท้ายด้วยข้อเดียวกัน คือต้องเข้าถึง
use case repository และ mapping tool ได้สะดวก

---

## ส่วนที่ 3 · ข้อเสนอฝั่ง Interface

### 🔴 I1 · sidebar หายทั้งแผงที่จอแคบกว่า 1060px

```css
@media (max-width:1060px){ .body{grid-template-columns:1fr} .side{display:none} }
```

ต่ำกว่า 1060px **ปุ่มควบคุมทั้งหมดหายไป** — เลือกตึกไม่ได้ กรองชั้นไม่ได้ อ่านรายละเอียดไม่ได้
เหลือแค่ภาพ 3 มิติที่หมุนได้อย่างเดียว บนแท็บเล็ตหรือโปรเจกเตอร์อัตราส่วนแปลก ๆ แอปใช้งานไม่ได้จริง

**แก้:** ทำเป็น drawer ที่เลื่อนเข้าออกได้ อย่า `display:none`

### 🔴 I2 · เดินด้วยคีย์บอร์ดไม่ได้เลย และ screen reader มองไม่เห็น cube

`<svg role="img">` + aria-label ตายตัว หมายความว่า node ทั้ง 798 จุด**ไม่มีตัวตน**สำหรับ
assistive technology และคลิกได้อย่างเดียว กดคีย์บอร์ดไม่ได้

ที่น่าเสียดายคือ **โครงสร้างข้อมูลพร้อมอยู่แล้ว** — `nbrs()` คำนวณเพื่อนบ้านทั้งหกทิศ
(layer ↑↓, y ↑↓, x ←→) ไว้เรียบร้อย ผูกเข้ากับปุ่มลูกศรได้ตรง ๆ

**แก้:** `tabindex` + `role="button"` บน node, ลูกศร = เดินตาม `nbrs()`,
Enter = เปิดแผง, Esc = ยกเลิกการเลือก

### 🟠 I3 · ไม่มีช่องค้นหา

798 cube + 30 coupling แต่กระโดดไปที่อยู่ที่รู้อยู่แล้วไม่ได้ เช่น `CMP.DIS.FLD`
ที่ KNOWLEDGE.md §12 อ้างถึงในการเดินตาม RMU

R1 Table 6 ระบุ **"Search functions / Transparency"** เป็นคุณสมบัติที่ repository ต้องมี

**แก้:** command palette (`/` หรือ `Ctrl-K`) ค้นได้ทั้งที่อยู่ cube, ชื่อชั้น, รหัส CPL, และชื่อมาตรฐาน

### 🟠 I4 · โหมดเดินตาม RMU — ฟีเจอร์ที่คุ้มที่สุดสำหรับหัวข้อ 17

KNOWLEDGE.md §12 เขียนไว้เองว่าการเดินตามอุปกรณ์ชิ้นเดียวคือ
*"เครื่องมือสื่อสารที่ได้ผลที่สุด"* และวางไว้ครบ 10 ขั้น ปิดวงพอดี
(โรงงาน → feeder → อาคาร → แปลงไผ่ → biomass → กลับโรงไฟฟ้า)

แต่**ในแอปไม่มีอยู่เลย** ผู้บรรยายต้องคลิกเองทีละจุดสด ๆ หน้าห้อง

**แก้:** story mode 10 ขั้น แต่ละขั้นตั้ง state (มุมกล้อง, ตึกที่เปิด, ชั้น, coupling ที่ไฮไลต์)
พร้อมปุ่มถอยหน้า/ถอยหลัง — ทำให้บรรยายซ้ำได้เหมือนเดิมทุกครั้ง

### 🟠 I5 · ไม่มีโหมด "ช่องว่าง"

แอปแสดงสิ่งที่**มี** แต่ finding ของโปรเจกต์คือสิ่งที่**ขาด** — 39 ตำแหน่งที่มีสิทธิ์เป็นรอยต่อ
ระบุสัญญาแล้ว 15 เหลือ **24 ที่ยังไม่มีเจ้าภาพ** ซึ่งเป็นวาระของ ARB โดยตรง

**แก้:** โหมดที่วาด 39 ตำแหน่งนั้น โดย 15 ตำแหน่งทึบ 24 ตำแหน่งกลวง
= เอาวาระการประชุมขึ้นจอเป็นภาพเดียว

### 🟡 I6 · มาตรฐานเป็นข้อความล้วน กรองไม่ได้

`standards` เก็บเป็น string เดียว เช่น `"IEC 61850-8-1 · IEC 62541"` ตอบคำถาม
*"รอยต่อไหนบ้างที่ผูกกับ IEC 61850"* ไม่ได้ ทั้งที่ R1 §374 บอกว่าจุดประสงค์ข้อหนึ่งของ SGAM คือ
*"to identify standards and standardization gaps"*

**แก้:** เก็บเป็น array แล้วทำเป็น chip ที่กดกรองได้

### 🟡 I7 · ไม่มีคำอธิบายว่าขนาดจุดหมายถึงอะไร

รัศมี node เข้ารหัส population (core 4.3 / supporting 3.4 / reference 2.6) แต่ไม่มี legend
คนดูไม่มีทางรู้ และใช้กับตึก SGAM ตึกเดียว ตึกอื่นวาดเท่ากันหมด — ยิ่งต้องบอก

### 🟡 I8 · deep link

`?tower=SGAM,SFAM&coupling=CPL-16` ตาม known gap เดิม — R1 §9.5 ย้ำเรื่องการเข้าถึง
mapping tool ได้สะดวก และจำเป็นถ้าจะแปะ state ลงสไลด์หรือส่งให้เจ้าภาพหัวข้ออื่นดูจุดเดียวกัน

### 🟢 I9 · explode เป็นสวิตช์ ควรเป็นสไลเดอร์

ตอนนี้มีแค่ `1` กับ `1.7` — สไลเดอร์จะปรับระยะให้พอดีกับโปรเจกเตอร์แต่ละตัวได้

---

## ลำดับที่แนะนำ

| รอบ | ทำอะไร | เหตุผล |
|---|---|---|
| **0** | D-1, D-2, D-3 | ของพังอยู่จริง แก้ถูก ใช้เวลาน้อย |
| **1** | I1, I2, I7 | ใช้งานไม่ได้จริงบนจอแคบ และเข้าถึงไม่ได้ |
| **2** | I4 (story mode), I5 (gap mode) | คุ้มที่สุดต่อการบรรยายหัวข้อ 17 |
| **3** | S2 (owner/contract) → S1 (use case register) | ทำให้ D4 บังคับใช้ได้ แล้วต่อยอดเป็น use case |
| **4** | S3, S8, S9, S10 | เนื้อหาจากมาตรฐาน แก้ที่เอกสารเป็นหลัก |
| **5** | S4, S5, S6, S7 | ขยายโมเดล ต้องมี Model Owner ของแต่ละตึกก่อน |
| **6** | S13, I3, I6, I8, I9 | ต่อยอดเมื่อฐานนิ่ง |

---

## สิ่งที่ยังยืนยันไม่ได้จากเอกสารชุดนี้

- **SCIAM และ SFAM** ไม่มีเอกสารอ้างอิงในชุดนี้เลย ตัวเลข layer/domain/zone
  ยังเป็นของที่อ่านจากไดอะแกรม ตาม KNOWLEDGE.md §13 ข้อ 1 — **ยังต้องให้เจ้าภาพหัวข้อ 12–14 ยืนยัน**
- **coupling ทั้ง 30 เส้น** ยังเป็นข้อเสนอจากบริบทธุรกิจ PCC เอกสารชุดนี้ไม่ได้รับรอง
  สิ่งที่ทำได้คือผูกแต่ละเส้นเข้ากับ use case และประเภทเครือข่ายตามมาตรฐาน (S1, S4)
  เพื่อให้ตรวจสอบได้ — ไม่ใช่เพื่อให้อ้างว่าเป็นมาตรฐาน
- **R3 เป็นเอกสาร Gartner ที่มีลิขสิทธิ์จำกัด** ใช้เป็นกรอบความคิดได้ ห้ามคัดลอกลงแอปสาธารณะ
