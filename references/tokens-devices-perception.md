# Design tokens, perception tests, device matrix, UI lint

## UI design tokens (`design-review/ui-tokens.json`)
The single source of truth for sizes, so "settings button taller than the pills" can't happen.
- No tokens file yet: build it from what the project **actually** uses. Code available → read theme/style files (Godot Theme/StyleBoxFlat resources and `custom_minimum_size`; React Native StyleSheet/theme files). Screenshots only → measure with `measure.py`. Start from `templates/ui-tokens.json`.
- Pick the dominant value for each role, propose consolidating outliers, and show the user the proposed tokens once ("Keep these tokens?"). Save after they confirm.
- Every review: compare every component against the tokens and flag violations as Precision/A5 defects with the token name ("settings 109px, token `heights.topBar` = 70").
- Keep a human-readable twin `design-review/ui-tokens.md` (table of roles, values, where used).

## Perception tests (every review with a screenshot file)
```
python scripts/perception.py screenshots/screens/review-03_shop.png screenshots/screens/review-03_shop_perception.png
```
- **Blur / squint**: is the primary action still the first thing you see? Do buttons dissolve into the background?
- **Grayscale**: do pieces, states and currencies still differ without color?
- **Deuteranopia / protanopia / tritanopia**: do any two pieces or states collapse into one color?
- **3-second first impression**: look at the original once, then state in one sentence what the screen is for and what to tap. If you can't, hierarchy is broken.
Send the sheet with the review when it shows a problem.

## Device matrix (live builds)
Screenshot every reviewed screen at:
| Profile | Viewport (CSS px) | Why |
|---|---|---|
| Small phone | 360×640 | cramped layouts, overflow |
| Tall phone + notch | 393×852 (19.5:9) | safe areas, top/bottom HUD |
| Tablet | 820×1180 | stretched layouts, dead space |
| Landscape phone | 852×393 | if the game supports rotation |
Godot web export / RN web: resize the browser viewport. Native-only builds: ask for screenshots or use the editor's resolution/aspect previews. Clipping, overlapping world labels and edge collisions mostly appear on the extremes. Note in the review which profiles were checked.

## Before/after proof (when fixing)
After each fix, re-screenshot the same screen at the same size and build a proof image:
```
python scripts/compare.py screenshots/proof/DT-022_proof.png --title "DT-022 settings height" \
  --item "Before=screenshots/proof/DT-022_before.png" --item "After=screenshots/proof/DT-022_after.png" --note "pills 70px · settings 70px (was 109px)"
```
Re-measure against the task's "Done when" line, then set VERIFIED (link the proof) or REOPENED.

## UI lint (code available)
```
python scripts/ui_lint.py <project_root> --out docs/game-prompts/design-review/lint-report.md
```
Catches: E-EMOJI (emoji in UI text), E-SIBLING (mismatched heights in a row container), W-TOKENS (values not in ui-tokens.json), W-SPRAWL (too many font sizes/radii/colors), I-OVERFLOW (Godot labels without wrap/overrun/clip), I-WORLD (Label3D to verify). Exit code 1 on errors.
- Turn each E-/W- finding into a task (or merge into an existing one).
- Offer once to add it as a pre-build step (Godot export script, npm `prebuild`, or a git pre-commit hook). Only add it if the user says yes.
