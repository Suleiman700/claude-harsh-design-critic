# Design Tasks — Sample run (Block Wood + hotel tycoon screenshots)
Updated: 2026-10-26 · Review #1 · Overall 4/10
Progress: [░░░░░░░░░░] 0/25 verified · CRITICAL open: 3 · MAJOR open: 11

> Sample generated from 6 screenshots, so no file:line yet. Every task links its own screenshot in `screenshots/issues/`, named after the task id. Run inside the project and these get exact locations.
> Market research not run (permission not asked yet in this sample), so "Reference" fields are empty.

## 🔥 Release blockers (CRITICAL)

### DT-001 · Shop buy buttons have a stray dark overlay; price is centered in it, not in the button
- Status: TODO | Severity: CRITICAL | Category: Precision/3.1 | Effort: S | Impact: High
- Screenshot: [DT-001_shop-price-overlay.png](screenshots/issues/DT-001_shop-price-overlay.png) · full screen: [review-01_shop_annotated.png](screenshots/screens/review-01_shop_annotated.png)
- Screen: Shop › Power-ups
- Problem: green button spans x 624–858 (center 741). A dark #306733 rectangle sits at x 708–820, so the gem + price center is at 769: **28px right of the button center**. The overlay is also inconsistent between rows (107px wide at x 713 in row 1, 112px at x 708 in rows 2–3). Reads as a stuck pressed state or leftover node.
- Fix: remove the overlay node (or anchor it full-rect with the button's corner radius if it is meant as a pressed state). Center the price group in the button.
- Done when: price group center within ±2px of button center in every row; no inner rectangle visible in normal state.

### DT-014 · World label "2nd Reception" clipped by the screen edge and cut by the Free $ button
- Status: TODO | Severity: CRITICAL | Category: Precision/3.2 | Effort: M | Impact: High
- Screenshot: [DT-014_world-label-clipped.png](screenshots/issues/DT-014_world-label-clipped.png) · full screen: [review-01_hotel-hud_annotated.png](screenshots/screens/review-01_hotel-hud_annotated.png)
- Screen: Hotel main view
- Problem: the name plate runs off the right edge ("Reception" cut) and the Free $ HUD button covers its top-left corner.
- Fix: clamp world-label screen positions to a 16px safe margin; hide or fade world labels when they intersect HUD rects; or move the plate under the station.
- Done when: no world label is clipped at any camera position on a 19.5:9 phone and a 4:3 tablet.

### DT-015 · "No free room!" drawn on top of the "RECEPTION" label: both unreadable
- Status: TODO | Severity: CRITICAL | Category: Precision/3.3 | Effort: S | Impact: High
- Screenshot: [DT-015_message-over-label.png](screenshots/issues/DT-015_message-over-label.png) · full screen: [review-01_reception_annotated.png](screenshots/screens/review-01_reception_annotated.png)
- Screen: Hotel reception
- Problem: transient warning spawns at the same anchor as the static station label.
- Fix: give transient messages their own lane (offset ~40px above the station label, with a dark plate), or hide the static label while the warning shows.
- Done when: the warning and the label never overlap; warning readable on any floor color.

## ⚡ Quick wins (High impact + S effort)
DT-001 · DT-022 · DT-004 · DT-002 · DT-015

## 📋 Now (MAJOR)

### DT-002 · Buy buttons look fully active with 0 gems
- Status: TODO | Severity: MAJOR | Category: States | Effort: S | Impact: High
- Screenshot: [DT-002_cant-afford-buttons.png](screenshots/issues/DT-002_cant-afford-buttons.png) · full screen: [review-01_shop_annotated.png](screenshots/screens/review-01_shop_annotated.png)
- Screen: Shop
- Problem: gem balance is 0, yet all three buttons (15/25/35) are bright green.
- Fix: can't-afford state: desaturated button + red price, tap opens the Gems tab or a rewarded-ad offer.
- Done when: every price above balance renders in the can't-afford state.

### DT-003 · Shop buy buttons stretch to card height (134px vs 179px)
- Status: TODO | Severity: MAJOR | Category: Precision/3.5 | Effort: S | Impact: Med
- Screenshot: [DT-003_shop-button-heights.png](screenshots/issues/DT-003_shop-button-heights.png) · full screen: [review-01_shop_annotated.png](screenshots/screens/review-01_shop_annotated.png)
- Screen: Shop
- Problem: row 1 button is 134px tall, rows 2–3 are 179px because the description wraps to two lines and the button fills the row.
- Fix: fixed button height (e.g. 96px), vertically centered in the card.
- Done when: all buy buttons measure the same height ±2px.

### DT-004 · Shop cards are asymmetric: 3px left margin vs 32px right
- Status: TODO | Severity: MAJOR | Category: Precision/3.2 | Effort: S | Impact: Med
- Screenshot: [DT-004_shop-card-margins.png](screenshots/issues/DT-004_shop-card-margins.png) · full screen: [review-01_shop_annotated.png](screenshots/screens/review-01_shop_annotated.png)
- Screen: Shop
- Problem: cards span x 3–910 on a 942px screen. Left edge nearly touches the screen; tabs bar and back button also hug the left edge.
- Fix: 16px (or safe-area) margin on both sides for cards, tabs and header.
- Done when: left and right margins equal ±2px on every row.

### DT-005 · Emoji and glyph icons mixed (shop, booster bar, pause menu)
- Status: TODO | Severity: MAJOR | Category: Precision/3.4 | Effort: M | Impact: High
- Screenshot: [DT-005_mixed-icons_booster.png](screenshots/issues/DT-005_mixed-icons_booster.png) · [DT-005_mixed-icons_pause.png](screenshots/issues/DT-005_mixed-icons_pause.png) · [DT-005_mixed-icons_shop.png](screenshots/issues/DT-005_mixed-icons_shop.png) · full screen: [review-01_pause_annotated.png](screenshots/screens/review-01_pause_annotated.png) · [review-01_booster-bar_annotated.png](screenshots/screens/review-01_booster-bar_annotated.png) · [review-01_shop_annotated.png](screenshots/screens/review-01_shop_annotated.png)
- Screens: Shop #4, Booster bar #2, Pause #1
- Problem: hammer and bomb are multicolor emoji-style art, swap and lightning are flat white glyphs; Home in the pause menu is an OS emoji 🏠 next to white glyphs.
- Fix: one icon set for all UI (white glyph with dark outline matches the current buttons). Replace every emoji.
- Done when: ui_lint.py reports 0 E-EMOJI and every icon in a group shares style and stroke.

### DT-007 · Booster buttons are flat blue on blue (2.11:1) and ignore the wood/gold theme
- Status: TODO | Severity: MAJOR | Category: Visual consistency | Effort: M | Impact: High
- Screenshot: [DT-007_booster-off-theme.png](screenshots/issues/DT-007_booster-off-theme.png) · full screen: [review-01_booster-bar_annotated.png](screenshots/screens/review-01_booster-bar_annotated.png)
- Screen: Gameplay
- Problem: #306AD9 buttons on #173A86 background, contrast 2.11:1. In the blur test they dissolve into the background. Board and tray are framed gold/wood; boosters have no frame or material.
- Fix: themed tray behind boosters (wood + gold frame like the piece tray) or gold outline + inner highlight + darker bottom lip on each button.
- Done when: boosters are still distinguishable in the blur test and share the board's material language.

### DT-008 · Same green pill means "owned count" (x1) and "price" (💎25)
- Status: TODO | Severity: MAJOR | Category: Semantics | Effort: S | Impact: Med
- Screenshot: [DT-008_pill-count-vs-price.png](screenshots/issues/DT-008_pill-count-vs-price.png) · full screen: [review-01_booster-bar_annotated.png](screenshots/screens/review-01_booster-bar_annotated.png)
- Screen: Gameplay booster bar
- Fix: corner count badge when owned; "+" or price only when empty.
- Done when: count and price use visually distinct treatments.

### DT-013 · Pieces differ only by hue: green, purple and pink collapse in grayscale
- Status: TODO | Severity: MAJOR | Category: Accessibility | Effort: M | Impact: Med
- Screenshot: [DT-013_pieces-grayscale.png](screenshots/issues/DT-013_pieces-grayscale.png) · full screen: [review-01_booster-bar_perception.png](screenshots/screens/review-01_booster-bar_perception.png)
- Screen: Gameplay
- Problem: all three piece colors become nearly the same gray.
- Fix: vary lightness more between piece colors and/or add a subtle per-color pattern or inner symbol (colorblind mode).
- Done when: pieces are distinguishable in the grayscale panel.

### DT-016 · "Receptionist" label clipped at the right screen edge
- Status: TODO | Severity: MAJOR | Category: Precision/3.2 | Effort: S | Impact: Med
- Screenshot: [DT-016_receptionist-label-clipped.png](screenshots/issues/DT-016_receptionist-label-clipped.png) · full screen: [review-01_reception_annotated.png](screenshots/screens/review-01_reception_annotated.png)
- Screen: Hotel reception
- Fix: same clamping as DT-014. Depends on: DT-014.

### DT-018 · "Resume" white on green fails contrast (2.09:1)
- Status: TODO | Severity: MAJOR | Category: Hierarchy/contrast | Effort: S | Impact: Med
- Screenshot: [DT-018_resume-contrast.png](screenshots/issues/DT-018_resume-contrast.png) · full screen: [review-01_pause_annotated.png](screenshots/screens/review-01_pause_annotated.png)
- Screen: Pause
- Fix: dark green text stroke/outline (3–4px, e.g. #1E6B12) or darker button green.
- Done when: text with outline passes 3:1 for large text.

### DT-021 · Music and Sound toggles show no on/off state
- Status: TODO | Severity: MAJOR | Category: States | Effort: S | Impact: Med
- Screenshot: [DT-021_toggle-no-state.png](screenshots/issues/DT-021_toggle-no-state.png) · full screen: [review-01_pause_annotated.png](screenshots/screens/review-01_pause_annotated.png)
- Screen: Pause
- Fix: slashed icon + dimmed button when off.
- Done when: both states visible and screenshot-verified.

### DT-022 · Settings button 109px tall next to 70px currency pills
- Status: TODO | Severity: MAJOR | Category: Precision/3.5 | Effort: S | Impact: High
- Screenshot: [DT-022_settings-button-height.png](screenshots/issues/DT-022_settings-button-height.png) · full screen: [review-01_topbar_annotated.png](screenshots/screens/review-01_topbar_annotated.png)
- Screen: Main top bar
- Problem: pills 70px (y 83–153); settings 96×109 (y 66–175). Tops misaligned by 17px, bottoms by 22px.
- Fix: settings 70×70, centered on the pills' vertical center (y 118).
- Done when: all top-bar items 70px ±2px and share center y.

## 🗂 Next (MINOR)

### DT-006 · Shop descriptions low contrast (#6B7BA8 on cream, 3.76:1)
- Status: TODO | Severity: MINOR | Category: Hierarchy/contrast | Effort: S | Impact: Med
- Screenshot: [DT-006_shop-description-contrast.png](screenshots/issues/DT-006_shop-description-contrast.png) · full screen: [review-01_shop_annotated.png](screenshots/screens/review-01_shop_annotated.png)
- Fix: darken to ~#4A5578 (passes 4.5:1).

### DT-010 · Tray pieces unevenly distributed
- Status: TODO | Severity: MINOR | Category: Precision/3.1 | Effort: S | Impact: Low
- Screenshot: [DT-010_tray-piece-spacing.png](screenshots/issues/DT-010_tray-piece-spacing.png) · full screen: [review-01_booster-bar_annotated.png](screenshots/screens/review-01_booster-bar_annotated.png)
- Fix: center each piece in a third of the tray.

### DT-011 · Booster bar ~500px wide under a ~900px tray (200px dead each side)
- Status: TODO | Severity: MINOR | Category: Layout | Effort: S | Impact: Med
- Screenshot: [DT-011_booster-bar-width.png](screenshots/issues/DT-011_booster-bar-width.png) · full screen: [review-01_booster-bar_annotated.png](screenshots/screens/review-01_booster-bar_annotated.png)
- Fix: match bar width to tray, or enlarge buttons.

### DT-019 · "Paused" header overlaps the Resume button by 15px
- Status: TODO | Severity: MINOR | Category: Precision/3.5 | Effort: S | Impact: Low
- Screenshot: [DT-019_header-overlaps-resume.png](screenshots/issues/DT-019_header-overlaps-resume.png) · full screen: [review-01_pause_annotated.png](screenshots/screens/review-01_pause_annotated.png)
- Fix: push Resume down 24px or shrink the header tab.

### DT-020 · Pause labels low contrast (#C3D1EE on #2A5CC4, 3.99:1)
- Status: TODO | Severity: MINOR | Category: Hierarchy/contrast | Effort: S | Impact: Low
- Screenshot: [DT-020_pause-label-contrast.png](screenshots/issues/DT-020_pause-label-contrast.png) · full screen: [review-01_pause_annotated.png](screenshots/screens/review-01_pause_annotated.png)
- Fix: white labels or a darker panel.

### DT-023 · Currency pills 50–59% empty
- Status: TODO | Severity: MINOR | Category: Precision/3.1 | Effort: S | Impact: Low
- Screenshot: [DT-023_pill-dead-space.png](screenshots/issues/DT-023_pill-dead-space.png) · full screen: [review-01_topbar_annotated.png](screenshots/screens/review-01_topbar_annotated.png)
- Problem: coin pill content ends at x 264 of 459 (195px empty); gem pill 233px empty.
- Fix: shrink pills to content + padding, or move "+" to the right end.

### DT-024 · "+" button position moves with the number width
- Status: TODO | Severity: MINOR | Category: Precision/3.5 | Effort: S | Impact: Low
- Screenshot: [DT-024_plus-position.png](screenshots/issues/DT-024_plus-position.png) · full screen: [review-01_topbar_annotated.png](screenshots/screens/review-01_topbar_annotated.png)
- Problem: "+" sits 147px from pill start in the coin pill, 111px in the gem pill.
- Fix: anchor "+" to the pill's right edge in both. Depends on: DT-023.

### DT-017 · Partially visible panel cut off at the right edge (reception screenshot)
- Status: TODO | Severity: MINOR | Category: Precision/3.2 | Effort: S | Impact: Low
- Screenshot: [DT-017_cut-off-side-panel.png](screenshots/issues/DT-017_cut-off-side-panel.png) · full screen: [review-01_reception_annotated.png](screenshots/screens/review-01_reception_annotated.png)
- Note: may be a debug panel. Verify on device.

## 🔍 Later (NITPICK)
- **DT-009** · Grey ghost blobs left of the booster bar (leftover shadow) — booster #4 · [DT-009_ghost-blob.png](screenshots/issues/DT-009_ghost-blob.png)
- **DT-012** · Tray frame has a cream bottom lip, board frame doesn't — booster #6 · [DT-012_tray-lip.png](screenshots/issues/DT-012_tray-lip.png)
- **DT-025** · Coin is a letter "C" glyph, gem is a stylized gem: icons from two styles — topbar #3 · [DT-025_currency-icon-styles.png](screenshots/issues/DT-025_currency-icon-styles.png)

## 💡 Ideas from market research
(Empty: run "research competitors" inside the project.)

## 🔁 Reopened / Regressed
## ✅ Verified
## 🚫 Won't fix
