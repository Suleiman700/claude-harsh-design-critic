# Task board and review log

All paths in this file are relative to `docs/harsh-design-critic/` in the project root.

## DESIGN_TASKS.md (one living board, never one file per review)
Every Q block becomes a task (or updates an existing one). The task stores all options and the pick, so the choice survives between sessions.

### Task format
```
### DT-007 · Settings button taller than currency pills
- Status: TODO | Severity: 🟠 MAJOR | Category: Precision/A5 | Impact: High
- Screen: Main HUD | Where: ui/top_bar.tscn:42 (SettingsButton.custom_minimum_size)
- Found: Review #3 (2026-10-26) as Q2
- Screenshot: [DT-007_settings-button-height.png](screenshots/issues/DT-007_settings-button-height.png) · full screen: [review-03_hud_annotated.png](screenshots/screens/review-03_hud_annotated.png) #2
- Problem: pills 70px tall, settings 109px (Δ39px, 56%); tops misaligned by 17px.
- Options:
  - (a) one shared bar height: settings 70×70, icon 36px (S): small tap-target change
  - (b) keep sizes, align top edges (S): mismatch stays, just moves
  - (c) redesign the top bar as one framed strip (M): bigger change, best result
- My pick: (a) — removes the mismatch instead of moving it; one-constant change
- Chosen: — (filled when the user approves: "a (my pick)" or "c (user)")
- Done when: all top-bar items 70px ±2px and share a vertical center.
- Depends on: — | Reference: Royal Match top bar (market-research/competitors/royal-match)
- Proof: — (becomes [DT-007_proof.png](screenshots/proof/DT-007_proof.png) when verified)
- History: — (older captures, e.g. DT-007_settings-button-height_r02.png)
```
- Ids: `DT-` defects, `IDEA-` ideas/differentiators from research, `LINT-` lint findings not yet merged into a DT. Permanent, never reused. The review's Q numbers are per-review; the DT id is permanent. Always show both ("Q2 / DT-007").
- Statuses: `TODO` → `APPROVED` (option chosen) → `IN PROGRESS` → `DONE` (fix applied) → `VERIFIED` (re-measured, proof linked). Also `PARTIAL` (works at only some sizes/states/camera positions), `REOPENED` (claimed done, still broken), `REGRESSED` (was verified, broke again → raise severity one level), `WONTFIX` (user decided, reason recorded), `BLOCKED` (needs an asset or decision: say what), `FAILED` (fix attempted, didn't work; say why).
- Severity: 🔴 CRITICAL · 🟠 MAJOR · 🟡 MINOR · ⚪ NITPICK (definitions in `output-format.md`).
- Effort per option: S (<30 min) · M (a few hours) · L (a day+). Impact: High / Med / Low. A task counts as a quick win when it's High impact and its pick is S.
- Merge duplicates: one defect showing on several screens is one task listing all screens.

### Board layout (regenerate the header on every update)
```
# Design Tasks — <project>
Updated: YYYY-MM-DD · Review #N · Overall X/10
Progress: [██████░░░░] 12/20 verified · 🔴 open: 1 · 🟠 open: 4 · awaiting your choice: 6

## 🔥 Release blockers (🔴)
## ⚡ Quick wins (High impact + S pick, top 5 ids)
## 📋 Now (🟠) · 🗂 Next (🟡) · 🔍 Later (⚪, one line each)
## 💡 Ideas from market research (IDEA-*)
## 🔁 Reopened / Regressed / Partial
## ✅ Verified (id + title + option applied + review verified in + proof link)
## 🚫 Won't fix
```
Group by screen inside sections when there are many. Add a **Fix order** line respecting dependencies (component/token fixes before individual instances).

### Commands the user can say
Approving (from the review's Q blocks): `approve all` · `approve Q1, Q3` · `Q1b, Q2a` · `approve quick wins` · `approve all critical` · `more detail on Q<n>` · `won't fix Q<n> because …` · `skip`.
Later sessions (by task id): `fix DT-007` (uses the stored pick unless an option is named: `fix DT-007 c`) · `next task` (highest-priority unblocked) · `what's left` · `verify` (re-check all DONE/PARTIAL) · `research competitors` · `lint`.

### Fixing (only after approval)
1. Set the chosen option on each task (`Chosen:`) and status APPROVED. Work in severity order.
2. Before each fix, say in one line what will change. Anything destructive, irreversible, or touching production/shared infrastructure needs its own explicit approval, even under `approve all`.
3. IN PROGRESS → take a "before" capture (`screenshots/proof/<id>_before.png`) of the **same screen, state and size** as the original evidence → apply only that option → DONE.
4. Re-capture the same screen, state and size; re-measure against "Done when"; save `<id>_after.png`, build `<id>_proof.png` (`tokens-devices-perception.md`) and link it in the task.
5. VERIFIED (link proof) · PARTIAL (works only from one camera position, one screen size, or one language) · FAILED (say why) · or "not observed" if the state wasn't reached in this run. Never mark VERIFIED without seeing it.
6. Append a results table to that review's report under `## Fix results`, and update the board and scorecard:
```
| Q | Task | Option applied | Result | Proof |
|---|------|----------------|--------|-------|
| 1 | DT-001 | (a) | ✅ verified | [DT-001_proof.png](../screenshots/proof/DT-001_proof.png) |
| 2 | DT-007 | (c) | ⚠️ partial: tablet still 4px off | [DT-007_proof.png](../screenshots/proof/DT-007_proof.png) |
| 3 | DT-009 | — | ⏭ skipped | — |
| 4 | DT-011 | (b) | ❌ failed: theme override ignored | — |
```

## REVIEW_LOG.md
```
# Project profile
- This is supposed to be: <one line, "X for Y", from README/store text/config>
- Type/genre: ... | Audience: ... | Languages: ... | Monetization: ...
- Market research: allowed (2026-10-26) | Competitors: see market-research/INDEX.md
- Screenshots: per-issue (2026-10-26) | Folder: design-review/screenshots/
- Tokens: design-review/ui-tokens.json (confirmed 2026-10-26)

## Review #N — YYYY-MM-DD — <screen/feature/flow> — Overall X/10
Report: design-review/reviews/2026-10-26-review.md
Scorecard: Precision X | Visual X | Art X | Hierarchy X | Layout X | Feel X | Flow X | Placement X | L10n X | A11y X | Audience X | Monetization X | Market X
Coverage: <audited> | Not audited: <...>
New: DT-021..DT-030, IDEA-004 | Approved: DT-021a, DT-022c | Verified: DT-007 | Partial: DT-011 | Reopened: DT-012
```
