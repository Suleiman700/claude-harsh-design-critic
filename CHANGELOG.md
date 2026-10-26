# Changelog

## 1.1.0 — 2026-10-26
- **Output folder moved:** everything the skill writes now goes to `docs/harsh-design-critic/` (`design-review/`, `market-research/`) instead of `docs/game-prompts/`. Old reviews in `docs/game-prompts/` are read as history, and the skill asks once before moving them. `ui_lint.py` still finds `ui-tokens.json` in the old location.
- New blind test: `tests/ecommerce-site/`, three store pages with 42 planted defects. Found 42/42, plus 16 issues that weren't planted.
- All tests now live in `tests/<name>/` (each with a README holding every finding); `examples/` and `tests/screenshots/` were folded in. The main README keeps a short summary per test with a "Full test" link.

## 1.0.1 — 2026-10-26
- `annotate.py`: badges are placed outside their box first and never on another marked box, so they stop covering the text they point at. New `badge_xy` to pin a badge by hand.
- `issue_shots.py`: measurement labels that would overlap in the label strip are moved apart.
- Two more example reviews (Nova Survivor, Word Wheel) and clean test screenshots in `tests/screenshots/`.

## 1.0.0 — 2026-10-26
First published version.

- Brutal-but-professional review of games, apps and websites from screenshots, code or a live build.
- Measurement scripts (element boxes, centering, contrast), annotated screenshots labeled with task ids, one crop per issue.
- Perception tests (blur, grayscale, three colorblind simulations), palette extraction, before/after proof images.
- Question blocks with 2–3 options and a pick; approval commands; read-only until approved.
- Living task board and review log; UI tokens and `ui_lint.py` for Godot and React Native.
- Market research with comparison board, feature matrix and HTML report (asks permission once).
- Grades against the `mobile-game-specs` specs when a project uses them.
