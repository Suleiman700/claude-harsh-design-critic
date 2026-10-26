# Test 1 · Block puzzle game + hotel tycoon game — 4/10

> "The board looks like a game. Everything around it looks like a prototype."

25 issues across 6 screens from two games. Click an ID to see its close-up.

## Block puzzle
**Shop**

<p align="center"><img src="../../docs/images/shop-annotated.png" width="260" alt="Puzzle shop, annotated"></p>

| ID | Level | Issue |
|---|---|---|
| [DT&#8209;001](design-review/screenshots/issues/DT-001_shop-price-overlay.png) | 🔴&nbsp;Critical | Price centered inside a stray dark overlay, **28px** right of the button center; overlay 107px wide in one row, 112px in the others |
| [DT&#8209;002](design-review/screenshots/issues/DT-002_cant-afford-buttons.png) | 🟠&nbsp;Major | Every buy button looks active while the player has **0 gems**: no can't-afford state |
| [DT&#8209;003](design-review/screenshots/issues/DT-003_shop-button-heights.png) | 🟠&nbsp;Major | Buy buttons **134px** tall in row 1, **179px** in rows 2–3: they stretch with the card |
| [DT&#8209;004](design-review/screenshots/issues/DT-004_shop-card-margins.png) | 🟠&nbsp;Major | Cards **3px** from the left edge, **32px** from the right |
| [DT&#8209;005](design-review/screenshots/issues/DT-005_mixed-icons_shop.png) | 🟠&nbsp;Major | Hammer and bomb are emoji-style art, swap is a flat glyph: mixed icon styles |
| [DT&#8209;006](design-review/screenshots/issues/DT-006_shop-description-contrast.png) | 🟡&nbsp;Minor | Descriptions `#6B7BA8` on cream: **3.76:1**, below 4.5:1 |
**Gameplay and booster bar**

<p align="center"><img src="../../docs/images/booster-annotated.png" width="260" alt="Puzzle gameplay booster bar, annotated"></p>

| ID | Level | Issue |
|---|---|---|
| [DT&#8209;007](design-review/screenshots/issues/DT-007_booster-off-theme.png) | 🟠&nbsp;Major | Boosters flat blue on a blue background (**2.11:1**), ignore the wood-and-gold theme |
| [DT&#8209;005](design-review/screenshots/issues/DT-005_mixed-icons_booster.png) | 🟠&nbsp;Major | Booster icons mix emoji (hammer, bomb) with white glyphs (swap, lightning) |
| [DT&#8209;008](design-review/screenshots/issues/DT-008_pill-count-vs-price.png) | 🟠&nbsp;Major | The same green pill means "owned count" (x1) and "price" (💎25) |
| [DT&#8209;013](design-review/screenshots/issues/DT-013_pieces-grayscale.png) | 🟠&nbsp;Major | Green, purple and pink pieces turn into one gray (see the perception sheet above) |
| [DT&#8209;010](design-review/screenshots/issues/DT-010_tray-piece-spacing.png) | 🟡&nbsp;Minor | Tray pieces unevenly spaced across the tray |
| [DT&#8209;011](design-review/screenshots/issues/DT-011_booster-bar-width.png) | 🟡&nbsp;Minor | Booster bar ~500px wide under a ~900px tray: ~200px dead space each side |
| [DT&#8209;009](design-review/screenshots/issues/DT-009_ghost-blob.png) | ⚪&nbsp;Nitpick | Grey ghost blobs left of the booster bar |
| [DT&#8209;012](design-review/screenshots/issues/DT-012_tray-lip.png) | ⚪&nbsp;Nitpick | Tray frame has a cream bottom lip, the board frame doesn't |
**Pause menu**

<p align="center"><img src="../../docs/images/pause-annotated.png" width="260" alt="Puzzle pause menu, annotated"></p>

| ID | Level | Issue |
|---|---|---|
| [DT&#8209;018](design-review/screenshots/issues/DT-018_resume-contrast.png) | 🟠&nbsp;Major | White "Resume" on green: **2.09:1** |
| [DT&#8209;021](design-review/screenshots/issues/DT-021_toggle-no-state.png) | 🟠&nbsp;Major | Music and Sound toggles show no on/off state |
| [DT&#8209;005](design-review/screenshots/issues/DT-005_mixed-icons_pause.png) | 🟠&nbsp;Major | Home is an OS emoji 🏠 next to white glyph icons |
| [DT&#8209;019](design-review/screenshots/issues/DT-019_header-overlaps-resume.png) | 🟡&nbsp;Minor | "Paused" header overlaps the Resume button by **15px** |
| [DT&#8209;020](design-review/screenshots/issues/DT-020_pause-label-contrast.png) | 🟡&nbsp;Minor | Button labels `#C3D1EE` on blue: **3.99:1** |
**Top bar**

<p align="center"><img src="../../docs/images/topbar-annotated.png" width="560" alt="Puzzle top bar, annotated"></p>

| ID | Level | Issue |
|---|---|---|
| [DT&#8209;022](design-review/screenshots/issues/DT-022_settings-button-height.png) | 🟠&nbsp;Major | Settings button **109px** tall next to **70px** currency pills (Δ39px, 56%) |
| [DT&#8209;023](design-review/screenshots/issues/DT-023_pill-dead-space.png) | 🟡&nbsp;Minor | Currency pills 50–59% empty |
| [DT&#8209;024](design-review/screenshots/issues/DT-024_plus-position.png) | 🟡&nbsp;Minor | "+" moves with the number: **147px** vs **111px** from the pill edge |
| [DT&#8209;025](design-review/screenshots/issues/DT-025_currency-icon-styles.png) | ⚪&nbsp;Nitpick | Coin is a letter "C" glyph, gem is a stylized icon: two icon styles |

## Hotel tycoon

**HUD**

<p align="center"><img src="../../docs/images/hotel-annotated.png" width="340" alt="Tycoon HUD, annotated"></p>

| ID | Level | Issue |
|---|---|---|
| [DT&#8209;014](design-review/screenshots/issues/DT-014_world-label-clipped.png) | 🔴&nbsp;Critical | "2nd Reception" name plate clipped by the screen edge and covered by the Free $ button |
**Reception**

<p align="center"><img src="../../docs/images/reception-annotated.png" width="420" alt="Tycoon reception, annotated"></p>

| ID | Level | Issue |
|---|---|---|
| [DT&#8209;015](design-review/screenshots/issues/DT-015_message-over-label.png) | 🔴&nbsp;Critical | "No free room!" printed on top of "RECEPTION": neither is readable |
| [DT&#8209;016](design-review/screenshots/issues/DT-016_receptionist-label-clipped.png) | 🟠&nbsp;Major | "Receptionist" label clipped at the right edge |
| [DT&#8209;017](design-review/screenshots/issues/DT-017_cut-off-side-panel.png) | 🟡&nbsp;Minor | A side panel cut off at the right edge |

## Files
- [Full review](design-review/reviews/2026-10-26-review.md)
- [Task board](design-review/DESIGN_TASKS.md)
- [Annotated screens](design-review/screenshots/screens/) · [one crop per issue](design-review/screenshots/issues/)
