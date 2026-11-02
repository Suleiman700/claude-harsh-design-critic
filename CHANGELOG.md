# Changelog

## 1.3.0 — 2026-11-02
- **HTML report:** the start-of-review question now asks for the report format: Markdown, HTML or both. HTML writes `design-review/REPORT.html` in the project, built by the new `html_report.py` from `design-review/report-data.json`. Every review appears on one page behind its own divider, with an issue table per review. Clicking an issue opens its annotated screenshot zoomed to the marked box, with the problem, `file:line`, options and My pick.
- **Decide in the browser:** mark each issue Leave it, Fix it (with an option), Won't fix or Ask a question, add notes, and press **Copy decisions**. The copied lines (`fix DT-014 b — … — note: …`) paste straight back into Claude, which treats them as approvals, questions and won't-fix reasons.
- **Always in sync:** `report-data.json` is the single source for the page. Every review and every fix updates it along with the Markdown files, then regenerates `REPORT.html`.
- **Navigating the page:** reviews collapse and expand (all collapsed by default, remembered per browser), with Expand all / Collapse all and a back-to-top button. Opening an issue expands its review and scrolls its row into view; the URL keeps `#issue=DT-xxx`, so a refresh or a shared link reopens it.
- **Clickable screenshots:** the image viewer shows the whole annotated screen with a dashed box on every issue marked on it, plus a button per issue; clicking either opens that issue. Corner buttons open the viewer or the raw image in a new tab.
- **Options are the choice:** each option card is selectable (choosing one means "fix it that way"); "Fix it" alone takes My pick. Closed issues show the applied option, the result and the before/after proof.
- New optional `also` list per finding for supporting images (perception sheet, palette); an issue drawn on an annotated screen must point at that screen and its box so it stays clickable.
- Per-issue crops stay clickable too: a finding can carry `"screen": {"image", "box"}`, the full screen it was cropped from, so the viewer outlines it there and the crop's panel opens that full screen.

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
