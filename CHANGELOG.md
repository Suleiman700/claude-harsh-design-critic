# Changelog

## 1.2.0 — 2026-10-26
- **Ask before starting:** every review now starts with one question, Quick or Full, and whether to mark issues on screenshots, with a warning that marking costs extra credits and time. Nothing is captured before the answer. Skip it by saying it in the request (`quick, no images`).
- **Quick mode** (`/harsh-design-critic quick …`): top 10 findings, one width, default state, short report with Q blocks for Critical/Major only.
- **`web_capture.py`:** full-page captures at any width (true 390px via a same-origin frame) and in forced states (`:hover`/`:focus` rules, clicks, scripts), plus per-element JSON (box, font, colors, radius, padding, WCAG contrast). Starts Chrome natively on Apple silicon when Python runs under Rosetta (~4x faster).
- Website scorecard (Content & data accuracy, Forms & states, Trust & conversion…) instead of game categories.

## 1.1.0 — 2026-10-26
- **Output folder moved:** everything the skill writes now goes to `docs/harsh-design-critic/` (`design-review/`, `market-research/`) instead of `docs/game-prompts/`. Old reviews in `docs/game-prompts/` are read as history, and the skill asks once before moving them. `ui_lint.py` still finds `ui-tokens.json` in the old location.
- `ui_lint.py` now scans HTML/CSS: emoji in page text, token sprawl, removed focus outlines with no replacement (`E-FOCUS`), pages with no `@media` rule (`W-MOBILE`), fixed widths wider than a phone.
- Install uses a `.venv` inside the skill folder (fixes `externally-managed-environment` on Homebrew Python); the skill runs its scripts with `.venv/bin/python` when it exists.
- The ZIP download (for the Claude app) leaves out `tests/` and `docs/images/`: about 50 KB instead of 38 MB.
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
