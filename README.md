<p align="center"><img src="https://github.com/user-attachments/assets/f88b9380-9b08-47dd-bafa-18f29d460fcd" alt="Harsh Design Critic: reviews your game, app or website like a publisher; every flaw measured in pixels, marked and ranked" width="100%"></p>

<h1 align="center">Harsh Design Critic</h1>

<p align="center">
  <b>A Claude skill that reviews your game, app or website like a publisher who has seen it all.</b><br>
  Every flaw measured in pixels, marked on your screenshot, ranked, and paired with a fix.
</p>

<p align="center">
  <b>42/42</b> planted defects found · <b>0</b> false positives · <b>5</b> projects reviewed · <b>21</b> kinds of check
</p>

<p align="center">
  <a href="#-what-is-it">What is it</a> ·
  <a href="#-showcase">Showcase</a> ·
  <a href="#-features">Features</a> ·
  <a href="#-install">Install</a> ·
  <a href="#-use">Use</a>
</p>

---

## 🔍 What is it

Most AI reviews say *"looks clean, maybe tweak the colors."* This skill makes Claude act like a **senior reviewer who looks at hundreds of projects a day**, hunting the smallest things that make a product feel cheap, and a **skeptical player or shopper** looking for any reason to leave.

It doesn't guess. It measures your screenshots (or renders your web pages itself) and reports **numbers**: sizes, gaps, offsets, contrast. Each issue is marked on the screenshot and turned into a question with 2–3 fixes and a recommended pick.

**Why it's useful**

- 🎯 **Catches what you stopped seeing.** After weeks on a project, a 7px misalignment is invisible to you, and obvious to a new user.
- 📏 **Ends design arguments with numbers.** "Feels off" becomes "109px next to 70px, Δ39px".
- 🧭 **Tells you what to fix first.** Issues are ranked 🔴 / 🟠 / 🟡, with effort per fix.
- 🛡️ **Never touches your project without approval.** It reviews, proposes, then stops and waits for you.
- ✅ **Proves the fix worked.** After fixing, it re-captures, re-measures, and saves a before/after image.

---

## 🏆 Showcase

<details>
<summary><b>🧪 Real-world tests</b>: 4 games and 1 website, scored and annotated</summary>
<br>

The skill was run on four real mobile games and one website with planted defects. Each test has a full review, annotated screens and one cropped image per issue.

| Test | Screens | Score | 🔴 | 🟠 | 🟡 | Results |
|---|:-:|:-:|:-:|:-:|:-:|---|
| 🧩 Block puzzle + 🏨 hotel tycoon | 6 | **4/10** | 3 | 11 | 4 | [findings](tests/block-puzzle-hotel-tycoon/README.md) · [review](tests/block-puzzle-hotel-tycoon/design-review/reviews/2026-10-26-review.md) · [tasks](tests/block-puzzle-hotel-tycoon/design-review/DESIGN_TASKS.md) |
| 🚀 Synthwave survivor shooter | 2 | **5/10** | 0 | 6 | 6 | [findings](tests/nova-survivor/README.md) · [review](tests/nova-survivor/design-review/reviews/2026-10-26-review.md) |
| 🔤 Swipe-to-spell word puzzle | 4 | **6/10** | 0 | 3 | 5 | [findings](tests/word-wheel/README.md) · [review](tests/word-wheel/design-review/reviews/2026-10-26-review.md) |
| 🛒 E-commerce site, **blind test** | 3 pages | **3/10** | 4 | 18 | 26 | [results](tests/ecommerce-site/README.md) · [review](tests/ecommerce-site/design-review/reviews/2026-10-26-review.md) |

<table>
  <tr>
    <td align="center"><img src="docs/images/shop-annotated.png" width="200" alt="Puzzle shop, annotated"><br><sub>Puzzle shop · 4/10</sub></td>
    <td align="center"><img src="tests/nova-survivor/design-review/screenshots/screens/review-01_main-menu_annotated.png" width="200" alt="Survivor shooter main menu, annotated"><br><sub>Shooter menu · 5/10</sub></td>
    <td align="center"><img src="tests/word-wheel/design-review/screenshots/screens/review-01_home_annotated.png" width="200" alt="Word puzzle home, annotated"><br><sub>Word puzzle home · 6/10</sub></td>
  </tr>
</table>

Every box is labeled with its task id (`DT-018`), the same id used in the review; cyan lines are measurements in pixels.

</details>

<details>
<summary><b>🎯 The blind test</b>: 42 / 42 planted defects found</summary>
<br>

Three store pages (landing, product, checkout) were built with **42 hidden defects**, from easy to 1px-subtle. The answer key was kept where the skill couldn't read it.

> **Found all 42 planted defects**, plus **16 real problems nobody planted**, with no false positives.

| Page | Planted | Found | Extra found |
|---|:-:|:-:|:-:|
| Landing (easy) | 10 | **10** | 4 |
| Product (medium) | 15 | **15** | 5 |
| Checkout (hard) | 17 | **17** | 4 (+3 across pages) |

<p align="center"><img src="tests/ecommerce-site/design-review/screenshots/screens/review-01_checkout_annotated.png" width="420" alt="Checkout, annotated"></p>

<p align="center"><a href="tests/ecommerce-site/README.md">Results &amp; scorecard</a> · <a href="tests/ecommerce-site/ANSWER_KEY.md">Answer key</a> · <a href="tests/ecommerce-site/site/">Test pages</a></p>

</details>

### What it catches

Real findings from the tests above.

| | Example | What it found |
|---|---|---|
| **Mismatched sizes in a row** | <img src="docs/images/DT-022_settings-button-height.png" width="220" alt="Settings button vs pills"> | Settings button **109px** tall next to **70px** currency pills (Δ39px, 56%) |
| **Off-center content** | <img src="docs/images/DT-001_shop-price-overlay_row1.png" width="220" alt="Price off center"> | Price centered in a stray dark overlay, **28px** off the button center |
| **Low contrast** | <img src="tests/nova-survivor/design-review/screenshots/issues/DT-011_level-pips.png" width="220" alt="Level pips contrast"> | Level pips at **1.42:1** (WCAG needs 3:1) |
| **Wrong numbers** | <img src="tests/ecommerce-site/design-review/screenshots/issues/DT-016_discount-math.png" width="220" alt="Discount math"> | "Save 20%" badge on **$89 → $74**, which is **16.9%** off |
| **Hover, focus and error states** | <img src="tests/ecommerce-site/design-review/screenshots/issues/DT-042_place-order-hover.png" width="220" alt="Hover contrast"> | "Place order" is fine at rest (5.17:1) but drops to **2.54:1** on hover |
| **Phone layout** | <img src="tests/ecommerce-site/design-review/screenshots/issues/DT-036_checkout-mobile-overflow.png" width="220" alt="Mobile overflow"> | At **390px** the form cards run **8px** past the screen edge |

<details>
<summary><b>See all 21 kinds of check</b></summary>
<br>

**On screen: pixels, sizes, color**

| | Example | What it found |
|---|---|---|
| **Four sizes where there should be one** | <img src="tests/nova-survivor/design-review/screenshots/issues/DT-001_menu-button-widths.png" width="220" alt="Menu button widths"> | Menu buttons **861 / 599 / 1071 / 605px** wide, left edge jumps from 164 to 59 |
| **Centered on the wrong thing** | <img src="tests/word-wheel/design-review/screenshots/issues/DT-002_header-title-offset.png" width="220" alt="Title off center"> | Title centered between two buttons, **35px** left of the screen center |
| **Missing states** | <img src="tests/nova-survivor/design-review/screenshots/issues/DT-008_cant-afford.png" width="220" alt="Can't afford"> | Balance **50**, cheapest price **375**, every price still looks buyable |
| **Uneven gaps and margins** | <img src="tests/nova-survivor/design-review/screenshots/issues/DT-002_grid-gaps.png" width="220" alt="Grid gaps"> | Column gap **7px** vs row gap **23px** |
| **Mixed icon styles** | <img src="docs/images/DT-005_mixed-icons_pause.png" width="220" alt="Emoji icon"> | Home is an **OS emoji** next to white glyph icons |
| **Clipping and overlapping text** | <img src="docs/images/DT-015_message-over-label.png" width="220" alt="Overlapping text"> | "No free room!" printed on top of "RECEPTION" |
| **Wasted space** | <img src="tests/nova-survivor/design-review/screenshots/issues/DT-009_dead-space.png" width="220" alt="Dead space"> | **315px** empty under BACK while the list you came for is cut off |
| **Baselines across states** | <img src="tests/word-wheel/design-review/screenshots/issues/DT-006_level-digit-offset.png" width="220" alt="Digit offset"> | Level digits **7px** lower on locked tiles than on unlocked ones |
| **Translation risks** | <img src="tests/word-wheel/design-review/screenshots/issues/DT-007_nav-label-padding.png" width="220" alt="Label padding"> | "More games" has **12px** padding: Arabic or Hebrew won't fit |
| **Palette audit** | <img src="tests/word-wheel/design-review/screenshots/screens/review-01_home_palette.png" width="220" alt="Palette"> | Real colors on screen as hex with share: 4 teals, 1 yellow, 1 cream |

**Beyond pixels: what a real shopper runs into**

For websites, the skill renders the pages itself and forces each state (click, type, hover, keyboard focus) on a copy of the page.

| | Example | What it found |
|---|---|---|
| **Broken promises across pages** | <img src="tests/ecommerce-site/design-review/screenshots/issues/DT-035_shipping-charged.png" width="220" alt="Shipping charged"> | Checkout charges **$5.99** shipping; the landing page promised free delivery over $60 |
| **Keyboard order** | <img src="tests/ecommerce-site/design-review/screenshots/issues/DT-038_cvc-expiry-tab-order.png" width="220" alt="Tab order"> | Tab goes **CVC → Expiry** while the screen shows Expiry → CVC |
| **Form input limits** | <img src="tests/ecommerce-site/design-review/screenshots/issues/DT-037_expiry-maxlength.png" width="220" alt="Expiry maxlength"> | Placeholder asks for "MM/YY" (5 chars) but the field stops at **4**: "12/2" |
| **Values past their limits** | <img src="tests/ecommerce-site/design-review/screenshots/issues/DT-021_qty-negative.png" width="220" alt="Negative quantity"> | Three taps on minus: quantity **−2**, no lower limit |
| **Brand consistency** | <img src="tests/ecommerce-site/design-review/screenshots/issues/DT-052_brand-inconsistency.png" width="220" alt="Brand inconsistency"> | Three brand names, three primary colors, headers **72 / 64 / 64px** in one flow |

</details>

### How a review looks

Every finding becomes a question with options and a pick:

```
Q4. 🟠 Settings button h=109 next to pills h=70 (Δ39px, 56%)  (DT-022)
- (a) One shared bar height: settings 70×70, icon 36px (effort S): small tap-target change
- (b) Keep sizes, align top edges (effort S): mismatch stays, just moves
- My pick: (a) because it removes the mismatch instead of moving it
```

Then it **stops**. You reply `approve all`, `approve Q1, Q4`, `Q1b, Q2a` or `approve quick wins`.

---

## ✨ Features

<table>
<tr>
<td valign="top" width="50%">

**🔎 Review**
- Quick (top 10, one width) or Full (everything, phone + desktop)
- Measured sizes, centering, margins and WCAG contrast
- Consumer verdict, score out of 10, 13-area scorecard
- Perception tests: blur, grayscale, 3 color-blind modes
- Game depth: juice, first session, ads and economy, placement logic
- Arabic / Hebrew / RTL checks
- Competitor comparison with an HTML report (asks first)

</td>
<td valign="top" width="50%">

**🌐 Websites**
- `web_capture.py` renders any width, in hover, focus, error and click states
- Every element's box, font, colors and contrast saved to JSON
- Keyboard order, form limits, prices and promises across pages

</td>
</tr>
<tr>
<td valign="top">

**🖼️ Output**
- Annotated screenshots, every box labeled with its task id
- One cropped image per issue (optional)
- Living task board: severity, effort, your choice, status, proof
- Review log that flags issues still broken since last time

</td>
<td valign="top">

**🛠️ Fixing**
- Read-only until you approve
- Before/after proof image for each fix; ⚠️ partial if it works on one screen size only
- `ui_lint.py` for Godot, React Native and HTML/CSS: emoji icons, row heights, off-token values, missing focus outlines, no phone layout

</td>
</tr>
</table>

---

## 📦 Install

**Claude Code**
```bash
git clone --depth 1 https://github.com/Suleiman700/claude-harsh-design-critic ~/.claude/skills/harsh-design-critic
cd ~/.claude/skills/harsh-design-critic
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

- The scripts' packages (pillow, numpy, scipy) go into the skill's own `.venv`, so your system Python stays untouched; this also avoids the `externally-managed-environment` error on macOS/Homebrew Python. On Windows use `.venv\Scripts\pip`.
- For one project only, clone into `<project>/.claude/skills/harsh-design-critic` instead.
- The repo includes the test reviews and their screenshots (about 38 MB). To install only the skill, use the ZIP below.

**Claude app:** download this repo as a ZIP (**Code → Download ZIP**, about 50 KB, tests and images excluded) and upload it as a skill in the app's settings.

---

## 🚀 Use

Attach a screenshot (or run it inside your project) and say:

- *"review this screen"*
- *"harsh review of the shop"*
- *"critique / roast this UI"*
- `/harsh-design-critic <request>` in Claude Code
- `/harsh-design-critic quick <request>` for a fast top-10 pass

Every review starts with one short question, and nothing is captured until you answer:

1. **Quick or Full?** Quick: top 10 findings at one screen width. Full: every finding, phone + desktop, hover/focus/error states, perception and palette.
2. **Mark issues on screenshots?** Per-issue images, full screens only, or no images.

<details>
<summary><b>Quick vs Full: time and token cost</b></summary>
<br>

| Mode | Images | Measured cost per web page |
|---|---|---|
| Quick | full screens only | ~70k tokens · ~2.5 min (product page test: 14 of 15 planted issues found) |
| Full | per-issue | ~90k tokens · ~6.5 min (the [blind test](tests/ecommerce-site/README.md): 277k tokens, ~20 min for 3 pages, 42/42 found) |

Quick is mostly **faster** (about 2.7x); it saves about a quarter of the tokens, because most of the cost is reading the skill and the page. Numbers come from single runs; your page will differ.

</details>

"No images" is cheapest. Say it in the request to skip the question, e.g. `/harsh-design-critic quick, no images, review the checkout`.

Later commands: `fix DT-007` · `next task` · `what's left` · `verify` · `research competitors` · `lint` · `store mode`.

<details>
<summary><b>Where the output goes</b></summary>

The first review in a project also asks about audience, languages, monetization and competitor research once, and remembers the answers. Everything it writes goes to `docs/harsh-design-critic/` in your project:

```
docs/harsh-design-critic/
  market-research/    INDEX.md · competitors/ · gap-table.md (only when research is allowed)
  design-review/
    REVIEW_LOG.md · DESIGN_TASKS.md · ui-tokens.json
    reviews/2026-10-26-review.md
    screenshots/screens/  review-01_shop_annotated.png …
    screenshots/issues/   DT-001_shop-price-overlay.png …
    screenshots/proof/    DT-001_before.png · DT-001_after.png · DT-001_proof.png
```
</details>

---

## 🤝 Works with mobile-game-specs

Pairs with [claude-mobile-game-specs](https://github.com/Suleiman700/claude-mobile-game-specs), a library of 28 mobile-game build specs. When a project follows those specs, the critic uses them as the rulebook: findings cite the spec ("floating label 4px from the edge; `04-hud-layout` requires 20px"), and option (a) is usually "apply the spec's default".

## ⚠️ Known limits

- Numbers are in screenshot pixels. Converting to dp needs the device density, which a screenshot alone doesn't give.
- Color-based measurements depend on the colors picked for each element. Check the annotated image before trusting a number.
- There is no automated score yet for how many known issues a review catches. The screenshots in `tests/screenshots/` are the start of that test set.

<details>
<summary><b>What's inside the repo</b></summary>

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
scripts/                     measure · annotate · issue_shots · palette · perception · compare · ui_lint · web_capture
templates/ui-tokens.json     starter tokens
tests/                       one folder per test: README with every finding, review, task board, screenshots
  block-puzzle-hotel-tycoon/ test 1: block puzzle + hotel tycoon
  nova-survivor/             test 2: survivor shooter (menu + shop), input/ = clean phone screenshots
  word-wheel/                test 3: word puzzle (home, reward, challenges, packs), input/ = clean phone screenshots
  ecommerce-site/            test 4: blind test, 3 store pages with 42 planted defects + answer key
```
</details>

## License

[MIT](LICENSE) © 2026 Suleiman700
