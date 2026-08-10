# Figures for the executive summary

Drop image files here with the **exact names below**. The executive summary picks them
up automatically — no code change, no rebuild. Until a file exists, the app shows a
placeholder in its place naming the path, so nothing breaks and nothing is silently missing.

| filename | where it appears | what it should show |
|---|---|---|
| `core-competency.png` | under **ฐาน — สมรรถนะหลัก**, beneath the three criteria | the core-competency and sustainable-advantage report (the capability table, the three imitation tests, the moat) |
| `revenue-target.png` | under **ปลายทาง — โครงสร้างรายได้**, beneath the bars | the revenue mix / target picture |

## How to add one

Either drag the file into `assets/exec/` on github.com and commit, or:

```bash
git add assets/exec/core-competency.png
git commit -m "Add the core competency figure"
git push
```

## Notes

- `.png`, `.jpg` and `.webp` all work. If you use a different extension, change the
  `src` in `executive.foundation.figure` / `executive.revenue.figure` in
  `data/architecture-model.json` to match.
- Keep each file under about 600 KB. These ship to every visitor, and the repository
  already carries a 22 MB video.
- Wide, legible screenshots work best — they render at up to 900px across and scale down
  on a phone.
- `tools/verify.py` checks that this directory is staged by the Pages workflow, so a file
  dropped here really does reach the published site rather than 404ing.
