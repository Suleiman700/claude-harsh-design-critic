<p align="center"><img src="docs/images/banner.png" alt="Harsh Design Critic: measures every pixel, marks every flaw, changes nothing until you approve" width="100%"></p>

# Harsh Design Critic — a Claude skill

> A brutal, publisher-grade design reviewer for games, apps and websites. It measures your screenshots, marks each issue on them, gives 2–3 fixes per problem with its pick, and changes nothing until you approve.

Most AI reviews say "looks clean, maybe tweak the colors". This skill acts like a senior reviewer who has seen a thousand games and a skeptical player looking for a reason to uninstall. It doesn't guess: it runs scripts on your screenshots and reports numbers.

**[What it can do](#what-it-can-do)** · **[Real-world tests](#real-world-tests)** · **[How a review looks](#how-a-review-looks)** · **[Install](#install)** · **[Use](#use)**

## What it can do

Every example below is a real finding from one of the [three test reviews](#real-world-tests).

| Capability | Example | What it found |
|---|---|---|
| **Measures sizes in a row** | <img src="docs/images/DT-022_settings-button-height.png" width="240" alt="Settings button vs pills"> | Settings button **109px** tall next to **70px** currency pills (Δ39px, 56%) |
| **Finds four sizes where there should be one** | <img src="examples/nova-survivor/design-review/screenshots/issues/DT-001_menu-button-widths.png" width="240" alt="Menu button widths"> | Menu buttons **861 / 599 / 1071 / 605px** wide, left edge jumps from 164 to 59 |
| **Checks if content is centered** | <img src="docs/images/DT-001_shop-price-overlay_row1.png" width="240" alt="Price off center"> | Price centered in a stray dark overlay, **28px** off the button center |
| **Spots titles centered on the wrong thing** | <img src="examples/word-wheel/design-review/screenshots/issues/DT-002_header-title-offset.png" width="240" alt="Title off center"> | Title centered between two buttons, **35px** left of the screen center |
| **Measures WCAG contrast** | <img src="examples/nova-survivor/design-review/screenshots/issues/DT-011_level-pips.png" width="240" alt="Level pips contrast"> | Level pips at **1.42:1** (needs 3:1); in another game, white on green at 2.09:1 |
| **Catches missing states** | <img src="examples/nova-survivor/design-review/screenshots/issues/DT-008_cant-afford.png" width="240" alt="Can't afford"> | Balance **50**, cheapest price **375**, every price still looks buyable |
| **Checks gaps and margins** | <img src="examples/nova-survivor/design-review/screenshots/issues/DT-002_grid-gaps.png" width="240" alt="Grid gaps"> | Column gap **7px** vs row gap **23px**; in another game, screen margins 3px vs 32px |
| **Finds mixed icon styles** | <img src="docs/images/DT-005_mixed-icons_pause.png" width="240" alt="Emoji icon"> | Home is an **OS emoji** next to white glyph icons; elsewhere, one outline coin among filled ones |
| **Finds clipping and overlapping text** | <img src="docs/images/DT-015_message-over-label.png" width="240" alt="Overlapping text"> | "No free room!" printed on top of "RECEPTION", so neither is readable |
| **Judges use of space** | <img src="examples/nova-survivor/design-review/screenshots/issues/DT-009_dead-space.png" width="240" alt="Dead space"> | **315px** empty under BACK while the list you came for is cut off |
| **Checks baselines across states** | <img src="examples/word-wheel/design-review/screenshots/issues/DT-006_level-digit-offset.png" width="240" alt="Digit offset"> | Level digits **7px** lower on locked tiles than on unlocked ones |
| **Flags translation risks** | <img src="examples/word-wheel/design-review/screenshots/issues/DT-007_nav-label-padding.png" width="240" alt="Label padding"> | "More games" has **12px** padding: Arabic or Hebrew won't fit |
| **Audits the palette** | <img src="examples/word-wheel/design-review/screenshots/screens/review-01_home_palette.png" width="240" alt="Palette"> | Real colors on screen as hex with share: 4 teals, 1 yellow, 1 cream |

### Perception tests

Blur, grayscale and three colorblind simulations in one sheet. They show problems a normal look misses.

<p align="center">
  <img src="examples/nova-survivor/design-review/screenshots/screens/review-01_main-menu_perception.png" width="45%" alt="Nova Survivor perception sheet">
  <img src="docs/images/perception-sheet.png" width="45%" alt="Block Wood perception sheet">
  <br><em>Left: in grayscale STORY is brighter than START, so the second option is the loudest button. Right: the green, purple and pink pieces turn into one gray.</em>
</p>

## Real-world tests

The skill has been run on three real mobile games. Each test has a full review, annotated screens and one cropped image per issue.

| # | Game | Genre | Screens | Score | 🔴 | 🟠 | 🟡 | Full review |
|---|---|---|---|---|---|---|---|---|
| 1 | Block Wood + hotel tycoon | Block puzzle + tycoon | 6 | **4/10** | 3 | 11 | 4 | [review](examples/sample-review/design-review/reviews/2026-10-26-review.md) · [tasks](examples/sample-review/design-review/DESIGN_TASKS.md) |
| 2 | Nova Survivor | Synthwave survivor shooter | 2 | **5/10** | 0 | 6 | 6 | [review](examples/nova-survivor/design-review/reviews/2026-10-26-review.md) |
| 3 | Word Wheel | Swipe-to-spell word puzzle | 4 | **6/10** | 0 | 3 | 5 | [review](examples/word-wheel/design-review/reviews/2026-10-26-review.md) |

Every box on the annotated screens is labeled with its task id, so you can find it in the review, and the cyan lines are measurements in pixels.

### Test 1 · Block Wood + hotel tycoon — 4/10

> "The board looks like a game. Everything around it looks like a prototype."

- Shop prices sit on stray dark stripes, 28px off center, and every buy button glows at 0 gems.
- Booster bar mixes OS emoji with white glyphs; cards hug the left edge (3px vs 32px).
- Hotel labels pile on top of each other and the receptionist's name is cut by the screen edge.

<p align="center">
  <img src="docs/images/shop-annotated.png" width="32%" alt="Shop screen, annotated">
  <img src="docs/images/pause-annotated.png" width="32%" alt="Pause menu, annotated">
  <img src="docs/images/booster-annotated.png" width="32%" alt="Gameplay booster bar, annotated">
</p>
<p align="center">
  <img src="docs/images/hotel-annotated.png" width="40%" alt="Hotel game HUD, annotated">
  <img src="docs/images/reception-annotated.png" width="55%" alt="Reception with overlapping labels, annotated">
</p>

### Test 2 · Nova Survivor — 5/10

> "Strong synthwave mood, but the menu is four different button systems and the shop sells things I can't afford without telling me."

- Menu buttons in four widths and five heights; grid column gap 7px vs row gap 23px.
- STORY uses the same yellow as the free-coin rewards, and out-shines START in grayscale.
- Shop: no can't-afford state, level pips at 1.42:1, 315px of dead space under BACK.

<p align="center">
  <img src="examples/nova-survivor/design-review/screenshots/screens/review-01_main-menu_annotated.png" width="40%" alt="Nova Survivor main menu, annotated">
  <img src="examples/nova-survivor/design-review/screenshots/screens/review-01_shop_annotated.png" width="40%" alt="Nova Survivor shop, annotated">
</p>

### Test 3 · Word Wheel — 6/10

> "Clean and calm, but locked, unearned and disabled all look the same faded teal."

- Gear and back buttons 151px tall with a 3D lip, next to flat 105px pills.
- Rewards you can still earn look disabled (2.77:1); locked day labels at 2.90:1.
- Screen titles 35px left of center; locked packs never say how to unlock them.
- What works: home layout margins equal to the pixel, one tight palette, primary action always in thumb reach.

<p align="center">
  <img src="examples/word-wheel/design-review/screenshots/screens/review-01_home_annotated.png" width="24%" alt="Word Wheel home, annotated">
  <img src="examples/word-wheel/design-review/screenshots/screens/review-01_daily-reward_annotated.png" width="24%" alt="Word Wheel daily reward, annotated">
  <img src="examples/word-wheel/design-review/screenshots/screens/review-01_challenges_annotated.png" width="24%" alt="Word Wheel challenges, annotated">
  <img src="examples/word-wheel/design-review/screenshots/screens/review-01_packs_annotated.png" width="24%" alt="Word Wheel packs, annotated">
</p>

The clean screenshots used in tests 2 and 3 are in [`tests/screenshots/`](tests/screenshots/), with the phone status bar and gesture bar removed.

## How a review looks

Every finding becomes a question with options and a pick:

```
Q4. 🟠 Settings button h=109 next to pills h=70 (Δ39px, 56%)  (DT-022)
- (a) One shared bar height: settings 70×70, icon 36px (effort S): small tap-target change
- (b) Keep sizes, align top edges (effort S): mismatch stays, just moves
- My pick: (a) because it removes the mismatch instead of moving it
```

Then it **stops**. You reply `approve all`, `approve Q1, Q4`, `Q1b, Q2a` or `approve quick wins`. After fixing, it re-captures the same screen, re-measures, and saves a before/after proof image. A fix that works on one screen size only is marked ⚠️ partial, not ✅.

Each review also has a skeptical player's take, a scorecard across 13 areas, a measurement table, and a coverage list of what it could not check.

## Features

- **Measured, not eyeballed.** Element boxes, content-vs-container centering, sibling heights, margins and WCAG contrast, computed from your screenshot.
- **Annotated screenshots.** Every box is labeled with its task id (`DT-018`), the same id used in the file names and the task list.
- **One cropped image per issue**, e.g. `screenshots/issues/DT-022_settings-button-height.png`, embedded under each question in the review.
- **Perception tests:** blur/squint, grayscale, deuteranopia, protanopia, tritanopia.
- **Market comparison** (asks permission once): 3–5 competitors, a comparison board, a ✅/➖/❌/⭐ feature matrix and an HTML report.
- **Game depth:** juice checklist, first-session flow, ads and economy judged retention-first, placement logic ("does a supply shelf belong in the lobby?").
- **Arabic / Hebrew / RTL checks:** mirroring, letter shaping, clipped diacritics, fallback fonts, overflow.
- **A living task board** (`DESIGN_TASKS.md`) with severity, effort, options, your choice, status and proof, plus a review log that calls out issues reported before and still broken.
- **UI tokens + lint:** `ui_lint.py` scans Godot and React Native code for emoji icons, mismatched row heights and off-token values.
- **Read-only until approved.** It never edits your project during a review.

## Install

**Claude Code**
```bash
git clone https://github.com/Suleiman700/claude-harsh-design-critic ~/.claude/skills/harsh-design-critic
pip install -r ~/.claude/skills/harsh-design-critic/requirements.txt
```
For one project only, clone into `<project>/.claude/skills/harsh-design-critic` instead.

**Claude app:** download this repo as a ZIP and upload it as a skill in the app's settings.

## Use

Attach a screenshot (or run it inside your project) and say:

- "review this screen"
- "harsh review of the shop"
- "critique / roast this UI"
- or `/harsh-design-critic <request>` in Claude Code

The first review in a project asks one short set of questions (audience, languages, monetization, competitor research, screenshots) and remembers the answers. Everything it writes goes to `docs/game-prompts/design-review/` in your project:

```
docs/game-prompts/design-review/
  REVIEW_LOG.md · DESIGN_TASKS.md · ui-tokens.json
  reviews/2026-10-26-review.md
  screenshots/screens/  review-01_shop_annotated.png …
  screenshots/issues/   DT-001_shop-price-overlay.png …
  screenshots/proof/    DT-001_before.png · DT-001_after.png · DT-001_proof.png
```

Later commands: `fix DT-007` · `next task` · `what's left` · `verify` · `research competitors` · `lint` · `store mode`.

## Known limits

- Numbers are in screenshot pixels. Converting to dp needs the device density, which a screenshot alone doesn't give.
- Color-based measurements depend on the colors picked for each element. Check the annotated image before trusting a number.
- There is no automated score yet for how many known issues a review catches. The screenshots in `tests/screenshots/` are the start of that test set.

## Works with mobile-game-specs

Pairs with [claude-mobile-game-specs](https://github.com/Suleiman700/claude-mobile-game-specs), a library of 28 mobile-game build specs. When a project follows those specs, the critic uses them as the rulebook: findings cite the spec ("floating label 4px from the edge; `04-hud-layout` requires 20px"), and option (a) is usually "apply the spec's default".

## What's inside

```
SKILL.md                     core: persona, rules, workflow
references/                  loaded only when a step needs them
  inspection-checklist.md    capture plan, measurement tables, precision defects, placement logic
  feel-flow-economy.md       juice, flow/FTUE, ads & economy, consumer criteria
  market-research.md         competitors, comparison board, gap table, HTML report
  tokens-devices-perception.md  tokens, device matrix, perception tests, lint, proof images
  screenshots.md             asking, capture, naming by task id, linking
  output-format.md           report layout, question blocks, approval prompt
  tasks-and-log.md           task board, statuses, fixing, review log
  house-standards.md         grading against mobile-game-specs
scripts/                     measure · annotate · issue_shots · palette · perception · compare · ui_lint
templates/ui-tokens.json     starter tokens
examples/sample-review/      test 1: Block Wood + hotel tycoon (report, task board, all images)
examples/nova-survivor/      test 2: Nova Survivor (menu + shop)
examples/word-wheel/         test 3: Word Wheel (home, reward, challenges, packs)
tests/screenshots/           clean phone screenshots used by tests 2 and 3
```

## License

[MIT](LICENSE) © 2026 Suleiman700
