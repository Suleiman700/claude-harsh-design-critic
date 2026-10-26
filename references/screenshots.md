# Screenshots: asking, capturing, naming, linking

## Ask once per project
Add this to the one-time profile question (stored in REVIEW_LOG.md as `Screenshots: <choice>`):
"Should I review with screenshots? I'll save them under `docs/game-prompts/design-review/screenshots/`, one image per issue, named after its task id (e.g. `DT-007_settings-button-height.png`) and linked from the task file and the review."
- **Per-issue (recommended):** full annotated screens + one cropped image per issue + before/after proof.
- **Full screens only:** annotated full screens, no per-issue crops.
- **No images:** text and measurements only (still measured with scripts if screenshot files exist).
If the user only gave code and a live build can run safely, the same question covers capturing it: "Can I run the build and capture the screens myself?" Never capture without a yes. The user can change the choice any time ("stop saving screenshots", "save screenshots this time").

## Folder and names
```
docs/game-prompts/design-review/screenshots/
  screens/   review-03_shop.png                    capture (copy of the user's file, or taken from the build)
             review-03_shop_cant-afford.png        state suffix
             review-03_shop_tall-notch.png         device suffix (small · tall-notch · tablet · landscape)
             review-03_shop_ar.png                 language suffix (ar · he · en)
             review-03_shop_annotated.png          full screen, every box labeled with its task id (DT-018)
             review-03_shop_perception.png         blur / grayscale / colorblind sheet
             review-03_shop_palette.png            extracted colors
  issues/    DT-007_settings-button-height.png     one crop per task: red box + banner "DT-007 · MAJOR · title"
             DT-007_settings-button-height_r05.png same issue re-captured in review #5 (still broken / regressed)
  proof/     DT-007_before.png · DT-007_after.png · DT-007_proof.png (side by side, with measurements)
```
Rules:
- Review numbers are two digits (`review-03`). Slugs are short, lowercase, hyphenated, and describe the problem (`shop-price-overlay`, not `issue-1`).
- **The issue image name = the task id + slug, and never changes** once created. Re-captures add `_rNN`; the task links the newest one and keeps the older links under "History".
- `IDEA-` tasks may have an image too: the competitor screenshot that inspired it, named `IDEA-004_corner-count-badge.png` (copied from `market-research/competitors/`).
- User-provided screenshots are copied into `screens/` with this naming; the originals are never modified or moved.
- Never overwrite: if a name exists, add `-2`.

## Labels: always the task id
Every box on every image (full screens and crops) is labeled with the **task id** (`DT-018`), never a per-screen number like 1, 2, 3. The same id is in the file name, the task file and the review, so any box can be found in the .md files and any finding can be found on the image. Only the main box of an issue gets a label; the same issue elsewhere on the screen gets a thin unlabeled box (`"badge": false`). Boxes that point at correct elements for comparison are not drawn on full screens.

## Making the images
```
# full screen, numbered by Q
python scripts/annotate.py screens/review-03_shop.png spec.json screens/review-03_shop_annotated.png
# one crop per task (prints the markdown links to paste)
python scripts/issue_shots.py issues-spec.json docs/game-prompts/design-review/screenshots/issues
```
`issue_shots.py` spec: `source`, then per issue `id`, `slug`, `title`, `severity`, `box`, optional `extra_boxes` (same issue elsewhere on the screen), `measures`, `pad`. An issue spanning several screens gets one crop per screen: `DT-005_mixed-icons_shop.png`, `DT-005_mixed-icons_pause.png`.
Open every image before linking it; fix clipped labels or crops that miss the problem.

## Linking (relative paths, so they open from VS Code, GitHub or any markdown viewer)
In `design-review/DESIGN_TASKS.md`:
```
- Screenshot: [DT-007_settings-button-height.png](screenshots/issues/DT-007_settings-button-height.png) · full screen: [review-03_hud_annotated.png](screenshots/screens/review-03_hud_annotated.png) #2
- Proof: [DT-007_proof.png](screenshots/proof/DT-007_proof.png)
```
In `design-review/reviews/<date>-review.md` (one folder deeper, so `../`), under each Q block, show the crop inline:
```
**Q4. 🟠 Settings button h=109 next to pills h=70 (Δ39px, 56%)** (DT-007)
![DT-007](../screenshots/issues/DT-007_settings-button-height.png)
- (a) ...
```
The Findings table's Evidence column links the same crop. In chat, send the full annotated screens; the per-issue crops live in the files.
