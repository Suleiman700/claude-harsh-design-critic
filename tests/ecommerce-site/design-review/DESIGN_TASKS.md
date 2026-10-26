# Design Tasks — Kestrel store (landing, product page, checkout)
Updated: 2026-10-26 · Review #1 · Overall 3/10 (Landing 4 · Product 4 · Checkout 3)
Progress: [░░░░░░░░░░] 0/54 verified · 🔴 open: 4 · 🟠 open: 18 · awaiting your choice: 54

**Fix order:** DT-034, DT-035 (money) → DT-001, DT-015, DT-036 (mobile) → DT-052, DT-053 (shared header + tokens) before DT-005/009/027/050 → DT-039 before DT-040 → the rest by severity.

## 🔥 Release blockers (🔴)

### DT-001 · Landing has no mobile layout
- Status: TODO | Severity: 🔴 CRITICAL | Category: Mobile/Layout | Impact: High
- Screen: Landing (easy.html) | Where: easy.html:11-64 (no @media); :23 .hero padding; :45 .products; :52 .newsletter
- Found: Review #1 (2026-10-26) as Q1
- Screenshot: [DT-001_landing-no-mobile-layout.png](screenshots/issues/DT-001_landing-no-mobile-layout.png) · [DT-001_landing-no-mobile-layout_products.png](screenshots/issues/DT-001_landing-no-mobile-layout_products.png) · full screen: [review-01_landing_phone_annotated.png](screenshots/screens/review-01_landing_phone_annotated.png)
- Problem: No media queries. At 390px: document 667px wide (277px horizontal scroll); hero h1 starts at x=0 (no margin, `.hero` padding overrides `.container`); nav "Contact" cut at the right edge; 3rd feature card starts at x=370; product grid stays 4 columns, buttons 85px wide with "Add to cart" wrapping out of a 40px height; newsletter input at x=220–520, off-screen.
- Options:
  - (a) Add one `@media (max-width:760px)` block: hero 1 column, `.hero{padding:56px 32px}`→16px side padding, features 1 column, products 2 columns, newsletter stacked, nav links in a menu button (M): covers 90% of phones with one breakpoint
  - (b) Fluid grids: `repeat(auto-fit,minmax(240px,1fr))` for features/products, `flex-wrap` on newsletter and nav (S): fewer rules, less control at 360px
  - (c) Mobile-first rewrite of the landing CSS with 3 breakpoints (360/760/1024) (L): best result, most work
- My pick: (a) — half of US retail traffic is mobile; one breakpoint fixes every collision found at 390px
- Chosen: —
- Done when: At 390px: scrollWidth = 390, 16px side margins, no text outside its button.
- Proof: —

### DT-015 · Product page buy box off-screen on phones
- Status: TODO | Severity: 🔴 CRITICAL | Category: Mobile/Layout | Impact: High
- Screen: Product page (medium.html) | Where: medium.html:23, :45, :50 (no @media)
- Found: Review #1 (2026-10-26) as Q2
- Screenshot: [DT-015_pdp-buy-box-offscreen.png](screenshots/issues/DT-015_pdp-buy-box-offscreen.png) · full screen: [review-01_product_phone_annotated.png](screenshots/screens/review-01_product_phone_annotated.png)
- Problem: `.pdp{grid-template-columns:1fr 1fr; gap:64px}` has no breakpoint. At 390px the document is 650px wide; the gallery takes the viewport and the whole buy box sits to the right of it. Tabs wrap "Reviews (126)" onto two lines; the related rail shows 1.2 cards.
- Options:
  - (a) `@media (max-width:760px){.pdp{grid-template-columns:1fr;gap:24px}}` plus sizes 5→ wrap, buy row full width (S): minimal
  - (b) Mobile layout with a sticky bottom Add-to-cart bar (M): more code, better conversion
  - (c) Mobile-first rewrite of the PDP (L): most work
- My pick: (a) — one rule makes the page purchasable on phones
- Chosen: —
- Done when: At 390px: scrollWidth 390, Add to cart ≥ 44px tall and full width, visible without horizontal scroll.
- Proof: —

### DT-034 · Order math is wrong
- Status: TODO | Severity: 🔴 CRITICAL | Category: Data/Money | Impact: High
- Screen: Checkout (hard.html) | Where: hard.html:172-173, :177, :204 (hard-coded 88.99)
- Found: Review #1 (2026-10-26) as Q3
- Screenshot: [DT-034_order-math.png](screenshots/issues/DT-034_order-math.png) · full screen: [review-01_checkout_annotated.png](screenshots/screens/review-01_checkout_annotated.png)
- Problem: Line items do not add up to the subtotal, and both items cost more than the landing page lists them for (mugs $32.00 expected → $68.90; towel $18.00 → $19.99). Tax $7.12 and total $102.10 are computed from the wrong subtotal. A shopper who checks will abandon; charging this is a refund/chargeback issue.
- Options:
  - (a) Compute subtotal, tax and total from line items in one function; fix item prices to the catalog ($32.00, $18.00) (S): none
  - (b) Load the cart from the same product data the landing uses (M): needs a data source
  - (c) Add a server-side total check before payment (L): backend work
- My pick: (a) — removes every hard-coded money number on the page
- Chosen: —
- Done when: Subtotal = Σ line items; prices match landing/PDP.
- Proof: —

### DT-035 · Shipping charged despite the free-shipping promise
- Status: TODO | Severity: 🔴 CRITICAL | Category: Data/Trust | Impact: High
- Screen: Checkout (hard.html) | Where: hard.html:150, :178; easy.html:112; medium.html:148
- Found: Review #1 (2026-10-26) as Q4
- Screenshot: [DT-035_shipping-charged.png](screenshots/issues/DT-035_shipping-charged.png) · full screen: [review-01_checkout_annotated.png](screenshots/screens/review-01_checkout_annotated.png)
- Problem: The checkout breaks a promise made on both previous pages, at the moment of payment. No "free shipping applied" line exists.
- Options:
  - (a) Standard = $0.00 ("Free") when subtotal ≥ $60, Express stays $12.99 (S): none
  - (b) Change the landing promise to match the real policy (S): weaker offer
- My pick: (a) — keeps the promise that sells
- Chosen: —
- Done when: Subtotal ≥ $60 → Standard shows "Free" and total drops by $5.99.
- Proof: —

## ⚡ Quick wins (High impact + S pick)
DT-015 Product page buy box off-screen on phones · DT-034 Order math is wrong · DT-035 Shipping charged despite the free-shipping promise · DT-002 Hero 32px off the page grid · DT-003 Hero subtitle unreadable

## 📋 Now (🟠)

#### Landing (easy.html)

### DT-002 · Hero 32px off the page grid
- Status: TODO | Severity: 🟠 MAJOR | Category: Precision/A5 | Impact: High
- Screen: Landing (easy.html) | Where: easy.html:23 (.hero padding shorthand), :86
- Found: Review #1 (2026-10-26) as Q5
- Screenshot: [DT-002_hero-off-grid.png](screenshots/issues/DT-002_hero-off-grid.png) · full screen: [review-01_landing_annotated.png](screenshots/screens/review-01_landing_annotated.png)
- Problem: `.container.hero` uses `padding: 96px 0 80px`, which wipes the container's 32px side padding. Hero text left edge x=120 vs logo/sections x=152 (Δ32px); hero art right edge 1320 vs content edge 1288 (Δ32px). The hero is the one block that is wider than everything else.
- Options:
  - (a) Change to `padding-top:96px; padding-bottom:80px` (keep container side padding) (S): one-line fix, hero 64px narrower
  - (b) Wrap the hero grid in an inner div so `.container` keeps its padding (S): extra element
  - (c) Make the hero intentionally full-bleed with a background band (M): a design change, needs art
- My pick: (a) — restores one left edge for the whole page with a one-line change
- Chosen: —
- Done when: Hero text left = logo left = section left (152px at 1440).
- Proof: —

### DT-003 · Hero subtitle unreadable
- Status: TODO | Severity: 🟠 MAJOR | Category: Contrast | Impact: High
- Screen: Landing (easy.html) | Where: easy.html:25
- Found: Review #1 (2026-10-26) as Q6
- Screenshot: [DT-003_hero-subtitle-contrast.png](screenshots/issues/DT-003_hero-subtitle-contrast.png) · full screen: [review-01_landing_annotated.png](screenshots/screens/review-01_landing_annotated.png)
- Problem: The only sentence that explains what the store sells is `#A8A8A8` on `#FFFFFF` = 2.38:1 at 19px regular. It disappears in the blur test.
- Options:
  - (a) Use the existing body grey `#5F6368` (6.05:1) (S): none
  - (b) Use `#6B6B70` from the PDP (5.3:1) (S): one more grey
  - (c) Darken to `#1D1D1F` at 80% weight for a stronger hero (S): less hierarchy between h1 and p
- My pick: (a) — reuses a token already on the page
- Chosen: —
- Done when: Subtitle ≥ 4.5:1.
- Proof: —

### DT-004 · OS emoji among SVG icons
- Status: TODO | Severity: 🟠 MAJOR | Category: Icons/A4 | Impact: High
- Screen: Landing (easy.html) | Where: easy.html:111
- Found: Review #1 (2026-10-26) as Q7
- Screenshot: [DT-004_emoji-feature-icon.png](screenshots/issues/DT-004_emoji-feature-icon.png) · full screen: [review-01_landing_annotated.png](screenshots/screens/review-01_landing_annotated.png)
- Problem: Feature icons: shield = SVG stroke `#1F5F4A` 1.8px; returns = SVG; delivery = OS emoji 🚚 (full-color, renders differently on Windows/Android/iOS, cannot be themed).
- Options:
  - (a) Replace with a 24px truck line SVG, stroke `#1F5F4A`, width 1.8 (S): none
  - (b) Use one icon set (e.g. the same family for all three) (S): adds a dependency
  - (c) Drop icons from all three cards (S): less scannable
- My pick: (a) — matches the other two icons exactly
- Chosen: —
- Done when: All three feature icons are SVG with the same stroke and color.
- Proof: —

#### Product page (medium.html)

### DT-016 · "Save 20%" is wrong
- Status: TODO | Severity: 🟠 MAJOR | Category: Data/Pricing | Impact: High
- Screen: Product page (medium.html) | Where: medium.html:117-119
- Found: Review #1 (2026-10-26) as Q8
- Screenshot: [DT-016_discount-math.png](screenshots/issues/DT-016_discount-math.png) · full screen: [review-01_product_annotated.png](screenshots/screens/review-01_product_annotated.png)
- Problem: (89−74)/89 = 16.85%. Overstating a discount is a FTC/state pricing-law risk and a trust killer.
- Options:
  - (a) Badge "Save 17%" (or "Save $15") (S): none
  - (b) Set the price to $71.20 to make 20% true (S): margin change
  - (c) Compute the badge from the two prices in code (M): needs templating
- My pick: (c) — this bug class disappears for every product
- Chosen: —
- Done when: Badge = round((was−now)/was).
- Proof: —

### DT-017 · Five full stars for a 4.2 rating
- Status: TODO | Severity: 🟠 MAJOR | Category: Data | Impact: High
- Screen: Product page (medium.html) | Where: medium.html:115, :33
- Found: Review #1 (2026-10-26) as Q9
- Screenshot: [DT-017_stars-vs-rating.png](screenshots/issues/DT-017_stars-vs-rating.png) · full screen: [review-01_product_annotated.png](screenshots/screens/review-01_product_annotated.png)
- Problem: Static 5 full stars regardless of rating; a 4.2 should show 4 full + a partial star. Star color below 3:1 for graphics.
- Options:
  - (a) Render stars from the rating (4 full + 20% fill) and darken to `#B07D00` (3.4:1) (S): none
  - (b) Show one star + "4.2" (S): less visual
- My pick: (a) — accurate and readable
- Chosen: —
- Done when: Star fill matches rating; ≥3:1.
- Proof: —

### DT-018 · Three different review counts
- Status: TODO | Severity: 🟠 MAJOR | Category: Data | Impact: High
- Screen: Product page (medium.html) | Where: medium.html:115, :155, :171-172
- Found: Review #1 (2026-10-26) as Q10
- Screenshot: [DT-018_review-count-mismatch.png](screenshots/issues/DT-018_review-count-mismatch.png) · [DT-018_review-count-mismatch_tab.png](screenshots/issues/DT-018_review-count-mismatch_tab.png) · full screen: [review-01_product_annotated.png](screenshots/screens/review-01_product_annotated.png)
- Problem: Three numbers for one fact. The tab shows two reviews with no "load more", no star per review, no author or date.
- Options:
  - (a) Use one count from one source; show "Showing 2 of 128" + "Load more" (S): none
  - (b) Show only the count you can display (S): hides social proof
- My pick: (a) — consistent and honest
- Chosen: —
- Done when: One count everywhere; list says how many are shown.
- Proof: —

### DT-019 · Chalk swatch is invisible
- Status: TODO | Severity: 🟠 MAJOR | Category: States | Impact: High
- Screen: Product page (medium.html) | Where: medium.html:127, :43
- Found: Review #1 (2026-10-26) as Q11
- Screenshot: [DT-019_chalk-swatch-invisible.png](screenshots/issues/DT-019_chalk-swatch-invisible.png) · full screen: [review-01_product_states_annotated.png](screenshots/screens/review-01_product_states_annotated.png)
- Problem: `style="background:#ffffff; border-color:#fff"` makes the 4th swatch invisible: shoppers see 3 colors. Clicking the empty spot selects it, the label changes to "Chalk", and no swatch looks selected.
- Options:
  - (a) Remove the inline border-color so Chalk gets the default `#DDD` border; add an inner ring for light swatches (S): none
  - (b) Give light swatches a 1px `#8A8A8E` inset ring (S): extra rule
- My pick: (a) — removes the override that causes it
- Chosen: —
- Done when: Chalk visible (border ≥3:1 vs white) and selected state visible.
- Proof: —

### DT-020 · Swatch selected and focus states invisible
- Status: TODO | Severity: 🟠 MAJOR | Category: States/A11y | Impact: High
- Screen: Product page (medium.html) | Where: medium.html:42-43
- Found: Review #1 (2026-10-26) as Q12
- Screenshot: [DT-020_swatch-selected-state.png](screenshots/issues/DT-020_swatch-selected-state.png) · [DT-020_swatch-selected-state_focus.png](screenshots/issues/DT-020_swatch-selected-state_focus.png) · full screen: [review-01_product_annotated.png](screenshots/screens/review-01_product_annotated.png)
- Problem: Selected = 2px `#C8C8C8` (1.67:1 vs white), unselected = 2px `#DDD`. Nobody can tell which color is chosen except by reading the label. `outline:none` with no replacement: keyboard users get no focus indicator (WCAG 2.4.7).
- Options:
  - (a) Selected: `box-shadow:0 0 0 2px #fff, 0 0 0 4px #1C1C1E`; focus: `:focus-visible{outline:2px solid #1C1C1E; outline-offset:3px}` (S): none
  - (b) Selected: checkmark inside the swatch (M): needs per-color contrast
- My pick: (a) — same black as the selected size button
- Chosen: —
- Done when: Selected ring ≥3:1 vs page; visible focus ring.
- Proof: —

### DT-021 · Quantity goes negative
- Status: TODO | Severity: 🟠 MAJOR | Category: States/Logic | Impact: High
- Screen: Product page (medium.html) | Where: medium.html:190
- Found: Review #1 (2026-10-26) as Q13
- Screenshot: [DT-021_qty-negative.png](screenshots/issues/DT-021_qty-negative.png) · full screen: [review-01_product_states_annotated.png](screenshots/screens/review-01_product_states_annotated.png)
- Problem: `qty.value = Number(qty.value) - 1` with no clamp: 0 and negative quantities can be added to cart.
- Options:
  - (a) Clamp to 1–10 and disable − at 1 (`disabled` + 40% opacity) (S): none
  - (b) Replace with a select 1–10 (S): different control
- My pick: (a) — smallest change, standard pattern
- Chosen: —
- Done when: Minimum 1, − disabled at 1.
- Proof: —

### DT-022 · No cart or search on the product page
- Status: TODO | Severity: 🟠 MAJOR | Category: Navigation | Impact: High
- Screen: Product page (medium.html) | Where: medium.html:85-90
- Found: Review #1 (2026-10-26) as Q14
- Screenshot: [DT-022_pdp-no-cart.png](screenshots/issues/DT-022_pdp-no-cart.png) · full screen: [review-01_product_annotated.png](screenshots/screens/review-01_product_annotated.png)
- Problem: After "Add to cart" there is no cart icon, count or link anywhere on the page.
- Options:
  - (a) Reuse the landing header (search + cart with count) (S): none
  - (b) Add a cart drawer that opens on Add to cart (M): more code
- My pick: (a) — one shared header
- Chosen: —
- Done when: Cart icon with count visible on every page.
- Proof: —

#### Checkout (hard.html)

### DT-036 · Checkout form cards overflow the phone screen
- Status: TODO | Severity: 🟠 MAJOR | Category: Mobile/A2 | Impact: High
- Screen: Checkout (hard.html) | Where: hard.html:57, :81-89
- Found: Review #1 (2026-10-26) as Q15
- Screenshot: [DT-036_checkout-mobile-overflow.png](screenshots/issues/DT-036_checkout-mobile-overflow.png) · full screen: [review-01_checkout_phone_annotated.png](screenshots/screens/review-01_checkout_phone_annotated.png)
- Problem: `.card-num{min-width:340px}` + 21px card padding + border forces the form column wider than the viewport; every form card loses its right border and the page scrolls sideways.
- Options:
  - (a) Delete `min-width:340px` (inputs are already `width:100%`) (S): none
  - (b) Wrap it in `@media (min-width:761px)` (S): dead rule stays
- My pick: (a) — the rule does nothing useful on desktop either
- Chosen: —
- Done when: At 390px scrollWidth = 390; all cards 358px.
- Proof: —

### DT-037 · Expiry field cannot hold MM/YY
- Status: TODO | Severity: 🟠 MAJOR | Category: Forms | Impact: High
- Screen: Checkout (hard.html) | Where: hard.html:161
- Found: Review #1 (2026-10-26) as Q16
- Screenshot: [DT-037_expiry-maxlength.png](screenshots/issues/DT-037_expiry-maxlength.png) · full screen: [review-01_checkout_states_annotated.png](screenshots/screens/review-01_checkout_states_annotated.png)
- Problem: The format the field asks for does not fit. No auto-insert of "/".
- Options:
  - (a) `maxlength="5"`, `inputmode="numeric"`, auto-insert "/" after 2 digits (S): none
  - (b) Two selects (month, year) (M): slower to fill
- My pick: (a) — matches the placeholder and autofill
- Chosen: —
- Done when: "12/28" typed in full; autofill works.
- Proof: —

### DT-038 · Tab order CVC → Expiry, screen shows Expiry → CVC
- Status: TODO | Severity: 🟠 MAJOR | Category: Keyboard/A11y | Impact: High
- Screen: Checkout (hard.html) | Where: hard.html:55-56, :160-161
- Found: Review #1 (2026-10-26) as Q17
- Screenshot: [DT-038_cvc-expiry-tab-order.png](screenshots/issues/DT-038_cvc-expiry-tab-order.png) · full screen: [review-01_checkout_annotated.png](screenshots/screens/review-01_checkout_annotated.png)
- Problem: Keyboard and screen-reader order disagree with the visual order (WCAG 2.4.3); autofill users land in CVC first.
- Options:
  - (a) Swap the two `<div>`s in the HTML and delete the `order` rules (S): none
- My pick: (a)
- Chosen: —
- Done when: Tab: card number → expiry → CVC.
- Proof: —

### DT-039 · Weak email error state
- Status: TODO | Severity: 🟠 MAJOR | Category: Forms/States | Impact: High
- Screen: Checkout (hard.html) | Where: hard.html:42-43, :121-122, :196-198
- Found: Review #1 (2026-10-26) as Q18
- Screenshot: [DT-039_email-error-state.png](screenshots/issues/DT-039_email-error-state.png) · full screen: [review-01_checkout_states_annotated.png](screenshots/screens/review-01_checkout_states_annotated.png)
- Problem: The only validation on the page is low-contrast, has no field highlight, no icon, no `aria-invalid`/`aria-describedby`, causes layout shift, and skips the empty case.
- Options:
  - (a) Error color `#B91C1C` (6.5:1), red border + `aria-invalid`, error replaces the hint (no shift), validate empty on submit (S): none
  - (b) Inline validation on every field with one shared pattern (M): covers DT-040 too
- My pick: (b) — one pattern fixes this and the missing validation in DT-040
- Chosen: —
- Done when: Error ≥4.5:1, field border red, no layout shift.
- Proof: —

### DT-040 · Place order does nothing on an empty form
- Status: TODO | Severity: 🟠 MAJOR | Category: Forms/Flow | Impact: High
- Screen: Checkout (hard.html) | Where: hard.html:114, :182
- Found: Review #1 (2026-10-26) as Q19
- Screenshot: [DT-040_place-order-no-validation.png](screenshots/issues/DT-040_place-order-no-validation.png) · full screen: [review-01_checkout_annotated.png](screenshots/screens/review-01_checkout_annotated.png)
- Problem: No required-field errors, no scroll to the first error, no disabled/loading state. The shopper does not know what happened.
- Options:
  - (a) On submit: validate required fields, show errors (DT-039 style), focus the first invalid field; loading state on the button (S): none
  - (b) Remove `novalidate` and use native validation (S): inconsistent native bubbles
- My pick: (a) — consistent with the rest of the page
- Chosen: —
- Done when: Empty submit shows errors and focuses the first one.
- Proof: —

### DT-041 · No State field for a US address
- Status: TODO | Severity: 🟠 MAJOR | Category: Forms | Impact: High
- Screen: Checkout (hard.html) | Where: hard.html:134-144
- Found: Review #1 (2026-10-26) as Q20
- Screenshot: [DT-041_missing-state-field.png](screenshots/issues/DT-041_missing-state-field.png) · full screen: [review-01_checkout_annotated.png](screenshots/screens/review-01_checkout_annotated.png)
- Problem: US shipping and sales tax need the state; the 8% tax line cannot be correct without it.
- Options:
  - (a) Add State select (autocomplete `address-level1`) and "Apt, suite" line; relabel ZIP per country (S): none
  - (b) Address autocomplete service (M): external service needs approval
- My pick: (a)
- Chosen: —
- Done when: State required for US; label changes for CA/UK.
- Proof: —

### DT-042 · Place order hover fails contrast
- Status: TODO | Severity: 🟠 MAJOR | Category: Contrast/States | Impact: High
- Screen: Checkout (hard.html) | Where: hard.html:76
- Found: Review #1 (2026-10-26) as Q21
- Screenshot: [DT-042_place-order-hover.png](screenshots/issues/DT-042_place-order-hover.png) · full screen: [review-01_checkout_states_annotated.png](screenshots/screens/review-01_checkout_states_annotated.png)
- Problem: Hover makes the primary button lighter and harder to read at the most important click.
- Options:
  - (a) Hover `#1D4ED8` (darker, 6.7:1) (S): none
- My pick: (a)
- Chosen: —
- Done when: Hover ≥4.5:1.
- Proof: —

#### Cross-page

### DT-052 · Three brands, three primary colors
- Status: TODO | Severity: 🟠 MAJOR | Category: Consistency/A7 | Impact: High
- Screen: Cross-page | Where: easy.html:15, :28; medium.html:16, :54; hard.html:15, :75, :11
- Found: Review #1 (2026-10-26) as Q22
- Screenshot: [DT-052_brand-inconsistency.png](screenshots/issues/DT-052_brand-inconsistency.png) · full screen: [review-01_checkout_annotated.png](screenshots/screens/review-01_checkout_annotated.png)
- Problem: The three pages of one purchase flow look like three different stores: different store name, logo color and size (22px green vs 20px black), primary button color, header height and content width. A homeware landing leads to a jacket PDP from "Kestrel Outdoor" and a checkout from "Kestrel".
- Options:
  - (a) One shared header and token set: name "Kestrel", primary `#1F5F4A`, header 64px, container 1200px (M): touches all three files
  - (b) Keep sub-brands but share logo, header and primary (S): sub-brand names stay confusing
- My pick: (a) — a checkout that looks like another site is a classic phishing signal for shoppers
- Chosen: —
- Done when: Same logo, header, primary color and container on all pages.
- Proof: —

## 🗂 Next (🟡)

#### Landing (easy.html)

### DT-005 · Hero buttons 48px vs 40px
- Status: TODO | Severity: 🟡 MINOR | Category: Precision/A5 | Impact: Med
- Screen: Landing (easy.html) | Where: easy.html:27-29
- Found: Review #1 (2026-10-26) as Q23
- Screenshot: [DT-005_hero-button-heights.png](screenshots/issues/DT-005_hero-button-heights.png) · full screen: [review-01_landing_annotated.png](screenshots/screens/review-01_landing_annotated.png)
- Problem: `.btn-secondary` overrides height to 40px; the pair sits on one row with centers aligned but different heights.
- Options:
  - (a) Remove `height:40px` from `.btn-secondary` (S): none
  - (b) Keep 40px and make it a text link (S): weaker secondary
- My pick: (a) — paired buttons should share a height
- Chosen: —
- Done when: Both hero buttons 48px.
- Proof: —

### DT-006 · Third feature card has different padding
- Status: TODO | Severity: 🟡 MINOR | Category: Precision/A1 | Impact: Med
- Screen: Landing (easy.html) | Where: easy.html:39, :115
- Found: Review #1 (2026-10-26) as Q24
- Screenshot: [DT-006_feature-card-padding.png](screenshots/issues/DT-006_feature-card-padding.png) · full screen: [review-01_landing_annotated.png](screenshots/screens/review-01_landing_annotated.png)
- Problem: `.feature--compact` sets padding 20px. Icon top y=973 vs 985 in cards 1–2; content inset 21px vs 33px; title baseline 12px higher.
- Options:
  - (a) Delete the `feature--compact` class from the third card (S): none
  - (b) Delete the `.feature--compact` rule (S): none
- My pick: (a) — one-word fix, the three cards become identical
- Chosen: —
- Done when: All three cards padding 32px, icons at the same y.
- Proof: —

### DT-007 · Product grid row gap 8px vs column gap 24px
- Status: TODO | Severity: 🟡 MINOR | Category: Spacing | Impact: Med
- Screen: Landing (easy.html) | Where: easy.html:45
- Found: Review #1 (2026-10-26) as Q25
- Screenshot: [DT-007_product-grid-gaps.png](screenshots/issues/DT-007_product-grid-gaps.png) · full screen: [review-01_landing_annotated.png](screenshots/screens/review-01_landing_annotated.png)
- Problem: Rows of cards are separated by 8px, columns by 24px; the grid reads as vertical strips.
- Options:
  - (a) `gap: 24px` (S): none
  - (b) `gap: 32px 24px` for more air between rows (S): taller page
- My pick: (a) — one value, same as the features grid
- Chosen: —
- Done when: Row gap = column gap = 24px.
- Proof: —

### DT-008 · Long product name pushes price and button down
- Status: TODO | Severity: 🟡 MINOR | Category: Precision/A1 | Impact: Med
- Screen: Landing (easy.html) | Where: easy.html:46-50, :130
- Found: Review #1 (2026-10-26) as Q26
- Screenshot: [DT-008_product-card-button-drop.png](screenshots/issues/DT-008_product-card-button-drop.png) · full screen: [review-01_landing_annotated.png](screenshots/screens/review-01_landing_annotated.png)
- Problem: Cards are block flow. Card 2 title 48px tall vs 24px; its button y=1751.7 vs 1727.7 in the other three; row-1 cards 356px vs row-2 332px.
- Options:
  - (a) Make `.product` a flex column and give the button `margin-top:auto` (S): buttons align, empty space above them in short cards
  - (b) Clamp titles to 2 lines with a fixed 48px title block (S): every card 24px taller
  - (c) Shorten the name to "Stoneware Serving Bowl" (S): content fix only
- My pick: (a) — aligns buttons for any title length
- Chosen: —
- Done when: All buttons in a row share one y.
- Proof: —

### DT-009 · Newsletter button shorter than the input
- Status: TODO | Severity: 🟡 MINOR | Category: Precision/A5 | Impact: Med
- Screen: Landing (easy.html) | Where: easy.html:56-57
- Found: Review #1 (2026-10-26) as Q27
- Screenshot: [DT-009_newsletter-control-heights.png](screenshots/issues/DT-009_newsletter-control-heights.png) · full screen: [review-01_landing_annotated.png](screenshots/screens/review-01_landing_annotated.png)
- Problem: `.newsletter .btn{height:38px}` next to a 44px input; tops at y 2290.7 vs 2293.7.
- Options:
  - (a) Set the button to 44px (or both to 48px, the hero button height) (S): none
  - (b) Join input and button into one 48px field group (M): new component
- My pick: (a) — one control height per row
- Chosen: —
- Done when: Input and button same height.
- Proof: —

### DT-010 · Typo "Recieve"
- Status: TODO | Severity: 🟡 MINOR | Category: Copy | Impact: Med
- Screen: Landing (easy.html) | Where: easy.html:145
- Found: Review #1 (2026-10-26) as Q28
- Screenshot: [DT-010_typo-recieve.png](screenshots/issues/DT-010_typo-recieve.png) · full screen: [review-01_landing_annotated.png](screenshots/screens/review-01_landing_annotated.png)
- Problem: Spelling error in a conversion sentence.
- Options:
  - (a) "Receive 10% off your first order…" (S): none
  - (b) "Get 10% off your first order…" (S): none
- My pick: (b) — shorter and fixes the typo
- Chosen: —
- Done when: No typo.
- Proof: —

### DT-011 · "Contact" smaller than its siblings
- Status: TODO | Severity: 🟡 MINOR | Category: Typography | Impact: Med
- Screen: Landing (easy.html) | Where: easy.html:18
- Found: Review #1 (2026-10-26) as Q29
- Screenshot: [DT-011_nav-contact-size.png](screenshots/issues/DT-011_nav-contact-size.png) · full screen: [review-01_landing_annotated.png](screenshots/screens/review-01_landing_annotated.png)
- Problem: `.nav-links a.contact{font-size:14px}` makes one nav item smaller and its baseline 1px off.
- Options:
  - (a) Remove the `.contact` rule (S): none
  - (b) Move Contact to the footer (S): one less nav item
- My pick: (a) — consistent nav
- Chosen: —
- Done when: All nav links 16px.
- Proof: —

### DT-012 · Footer links are plain text; email input has no label
- Status: TODO | Severity: 🟡 MINOR | Category: Function/A11y | Impact: Med
- Screen: Landing (easy.html) | Where: easy.html:162-164, :148
- Found: Review #1 (2026-10-26) as Q30
- Screenshot: [DT-012_footer-dead-links.png](screenshots/issues/DT-012_footer-dead-links.png) · full screen: [review-01_landing_annotated.png](screenshots/screens/review-01_landing_annotated.png)
- Problem: Footer Shop/Help/Company items are not anchors: a shopper looking for Returns or Shipping cannot click them. The newsletter `<input>` has no `<label>`/`aria-label`; the placeholder disappears on typing.
- Options:
  - (a) Wrap each item in `<a href>`; add `aria-label="Email address"` (or a visually-hidden label) (S): none
  - (b) Add links only for Help items now (S): partial
- My pick: (a) — footer links are where shoppers look for policies
- Chosen: —
- Done when: Every footer item is a link; input has an accessible name.
- Proof: —

#### Product page (medium.html)

### DT-023 · Sold-out sizes barely differ from available ones
- Status: TODO | Severity: 🟡 MINOR | Category: States | Impact: Med
- Screen: Product page (medium.html) | Where: medium.html:48, :133, :136
- Found: Review #1 (2026-10-26) as Q31
- Screenshot: [DT-023_disabled-sizes.png](screenshots/issues/DT-023_disabled-sizes.png) · full screen: [review-01_product_annotated.png](screenshots/screens/review-01_product_annotated.png)
- Problem: Disabled sizes only differ by text color; no cue says why they cannot be picked or offers "notify me".
- Options:
  - (a) Diagonal strike + `#F4F4F5` fill + `aria-label="S, sold out"` (S): none
  - (b) Add "Notify me" when a sold-out size is tapped (M): backend
- My pick: (a) — standard retail pattern
- Chosen: —
- Done when: Sold-out sizes recognisable in grayscale.
- Proof: —

### DT-024 · Related rail clipped with no scroll control
- Status: TODO | Severity: 🟡 MINOR | Category: Layout/A2 | Impact: Med
- Screen: Product page (medium.html) | Where: medium.html:76-77, :182
- Found: Review #1 (2026-10-26) as Q32
- Screenshot: [DT-024_related-rail-clipped.png](screenshots/issues/DT-024_related-rail-clipped.png) · full screen: [review-01_product_annotated.png](screenshots/screens/review-01_product_annotated.png)
- Problem: No arrows, no scroll, no peek affordance; the 5th product (Wax Restoring Kit, the obvious add-on) can never be seen.
- Options:
  - (a) `overflow-x:auto; scroll-snap-type:x mandatory` + arrows (S): none
  - (b) Show 4 cards in a 4-column grid (S): drops one product
- My pick: (a) — keeps all 5
- Chosen: —
- Done when: All cards reachable; no card cut mid-text at rest.
- Proof: —

### DT-025 · Active tab underline floats 1px above the divider
- Status: TODO | Severity: 🟡 MINOR | Category: Precision | Impact: Med
- Screen: Product page (medium.html) | Where: medium.html:62
- Found: Review #1 (2026-10-26) as Q33
- Screenshot: [DT-025_tab-underline-gap.png](screenshots/issues/DT-025_tab-underline-gap.png) · full screen: [review-01_product_annotated.png](screenshots/screens/review-01_product_annotated.png)
- Problem: `.tab.active::after{bottom:1px}` leaves a 1px gap instead of sitting on the divider.
- Options:
  - (a) `bottom:-1px` so the underline covers the divider (S): none
- My pick: (a)
- Chosen: —
- Done when: Underline touches the divider.
- Proof: —

### DT-026 · Specs table zigzags and contradicts itself
- Status: TODO | Severity: 🟡 MINOR | Category: Data/Layout | Impact: Med
- Screen: Product page (medium.html) | Where: medium.html:70, :165-166
- Found: Review #1 (2026-10-26) as Q34
- Screenshot: [DT-026_specs-table.png](screenshots/issues/DT-026_specs-table.png) · full screen: [review-01_product_states_annotated.png](screenshots/screens/review-01_product_states_annotated.png)
- Problem: `.specs tr:nth-child(odd) td:last-child{text-align:right}` alternates value alignment. Unit spacing inconsistent. A packed weight cannot be lower than the item weight.
- Options:
  - (a) Remove the nth-child rule (all left); write "1.2 kg"; fix or remove packed weight (S): needs the real number
- My pick: (a)
- Chosen: —
- Done when: One alignment, one unit style, plausible data.
- Proof: —

### DT-027 · Three radii in the buy row
- Status: TODO | Severity: 🟡 MINOR | Category: Consistency | Impact: Med
- Screen: Product page (medium.html) | Where: medium.html:51, :54, :55
- Found: Review #1 (2026-10-26) as Q35
- Screenshot: [DT-027_buy-row-radii.png](screenshots/issues/DT-027_buy-row-radii.png) · full screen: [review-01_product_annotated.png](screenshots/screens/review-01_product_annotated.png)
- Problem: One row, two radii.
- Options:
  - (a) Add to cart radius 6 (or all 8 to match the landing) (S): none
- My pick: (a)
- Chosen: —
- Done when: One radius per row.
- Proof: —

### DT-028 · Third thumbnail 2px smaller
- Status: TODO | Severity: 🟡 MINOR | Category: Precision/A5 | Impact: Med
- Screen: Product page (medium.html) | Where: medium.html:29, :108
- Found: Review #1 (2026-10-26) as Q36
- Screenshot: [DT-028_thumb-size.png](screenshots/issues/DT-028_thumb-size.png) · full screen: [review-01_product_annotated.png](screenshots/screens/review-01_product_annotated.png)
- Problem: `.thumb--alt{width:70px;height:70px}`.
- Options:
  - (a) Remove `thumb--alt` (S): none
- My pick: (a)
- Chosen: —
- Done when: All thumbs 72px.
- Proof: —

### DT-029 · Thumbnails do nothing
- Status: TODO | Severity: 🟡 MINOR | Category: Interaction | Impact: Med
- Screen: Product page (medium.html) | Where: medium.html:27, :105-110, script :187-207
- Found: Review #1 (2026-10-26) as Q37
- Screenshot: [DT-029_thumbs-not-clickable.png](screenshots/issues/DT-029_thumbs-not-clickable.png) · full screen: [review-01_product_annotated.png](screenshots/screens/review-01_product_annotated.png)
- Problem: Clicking a thumbnail never changes the main image or the active border.
- Options:
  - (a) Add a click handler that swaps the main image and moves `.active`; make thumbs `<button>`s (S): none
- My pick: (a)
- Chosen: —
- Done when: Click and keyboard switch the main image.
- Proof: —

### DT-030 · "Colour" on a US store; color names don't match swatches
- Status: TODO | Severity: 🟡 MINOR | Category: Copy | Impact: Med
- Screen: Product page (medium.html) | Where: medium.html:122, :125-126
- Found: Review #1 (2026-10-26) as Q38
- Screenshot: [DT-030_colour-spelling.png](screenshots/issues/DT-030_colour-spelling.png) · full screen: [review-01_product_annotated.png](screenshots/screens/review-01_product_annotated.png)
- Problem: Spelling mismatch with the US market; two swatch names describe colors the swatches are not (unverified against real product photos).
- Options:
  - (a) "Color"; rename swatches "Charcoal"/"Brown" or recolor to real navy/tan (S): none
- My pick: (a)
- Chosen: —
- Done when: defect no longer measurable
- Proof: —

#### Checkout (hard.html)

### DT-043 · Phone is required but not marked
- Status: TODO | Severity: 🟡 MINOR | Category: Forms | Impact: Med
- Screen: Checkout (hard.html) | Where: hard.html:36, :124-127
- Found: Review #1 (2026-10-26) as Q39
- Screenshot: [DT-043_phone-required-mismatch.png](screenshots/issues/DT-043_phone-required-mismatch.png) · full screen: [review-01_checkout_annotated.png](screenshots/screens/review-01_checkout_annotated.png)
- Problem: Required/optional signal contradicts itself.
- Options:
  - (a) Make it optional: remove `required`, label "Phone (optional)" (S): none
  - (b) Keep required and add the asterisk (S): more friction
- My pick: (a) — less friction
- Chosen: —
- Done when: defect no longer measurable
- Proof: —

### DT-044 · City and ZIP inputs misaligned
- Status: TODO | Severity: 🟡 MINOR | Category: Precision/A5 | Impact: Med
- Screen: Checkout (hard.html) | Where: hard.html:35, :38
- Found: Review #1 (2026-10-26) as Q40
- Screenshot: [DT-044_city-zip-misaligned.png](screenshots/issues/DT-044_city-zip-misaligned.png) · full screen: [review-01_checkout_annotated.png](screenshots/screens/review-01_checkout_annotated.png)
- Problem: `.field--city label{margin-bottom:8px}` and `.field--zip input{height:43px}`.
- Options:
  - (a) Delete both one-off rules (S): none
- My pick: (a)
- Chosen: —
- Done when: Both inputs 44px, same top.
- Proof: —

### DT-045 · Stepper connectors 2px low
- Status: TODO | Severity: 🟡 MINOR | Category: Precision | Impact: Med
- Screen: Checkout (hard.html) | Where: hard.html:25
- Found: Review #1 (2026-10-26) as Q41
- Screenshot: [DT-045_stepper-line-low.png](screenshots/issues/DT-045_stepper-line-low.png) · full screen: [review-01_checkout_annotated.png](screenshots/screens/review-01_checkout_annotated.png)
- Problem: `.line{margin-top:17px}` for a 32px dot and 2px line; should be 15px.
- Options:
  - (a) `margin-top:15px` (S): none
- My pick: (a)
- Chosen: —
- Done when: Line centered on the dots.
- Proof: —

### DT-046 · Stepper says "Details", page already asks for payment
- Status: TODO | Severity: 🟡 MINOR | Category: Flow | Impact: Med
- Screen: Checkout (hard.html) | Where: hard.html:102-110, :155-164
- Found: Review #1 (2026-10-26) as Q42
- Screenshot: [DT-046_stepper-mismatch.png](screenshots/issues/DT-046_stepper-mismatch.png) · full screen: [review-01_checkout_annotated.png](screenshots/screens/review-01_checkout_annotated.png)
- Problem: The progress indicator lies about where the shopper is; "Review" (step 4) never appears either.
- Options:
  - (a) Steps: Cart · Checkout · Confirmation (S): none
  - (b) Split payment into a real step 3 (M): extra page
- My pick: (a)
- Chosen: —
- Done when: defect no longer measurable
- Proof: —

### DT-047 · Selecting a shipping option shifts the layout
- Status: TODO | Severity: 🟡 MINOR | Category: States | Impact: Med
- Screen: Checkout (hard.html) | Where: hard.html:46-47
- Found: Review #1 (2026-10-26) as Q43
- Screenshot: [DT-047_shipping-option-shift.png](screenshots/issues/DT-047_shipping-option-shift.png) · full screen: [review-01_checkout_states_annotated.png](screenshots/screens/review-01_checkout_states_annotated.png)
- Problem: Border width changes between states.
- Options:
  - (a) Keep 1px border and add `box-shadow:0 0 0 1px #2563EB` when selected (S): none
- My pick: (a)
- Chosen: —
- Done when: No movement when toggling.
- Proof: —

### DT-048 · Hints and legal text below 4.5:1
- Status: TODO | Severity: 🟡 MINOR | Category: Contrast | Impact: Med
- Screen: Checkout (hard.html) | Where: hard.html:41, :79
- Found: Review #1 (2026-10-26) as Q44
- Screenshot: [DT-048_hint-contrast.png](screenshots/issues/DT-048_hint-contrast.png) · full screen: [review-01_checkout_annotated.png](screenshots/screens/review-01_checkout_annotated.png)
- Problem: Small text below AA; legal text is also 11px.
- Options:
  - (a) Use `#5F6368` (6.05:1), legal 12px (S): none
- My pick: (a)
- Chosen: —
- Done when: defect no longer measurable
- Proof: —

### DT-049 · Line-item amounts not right-aligned
- Status: TODO | Severity: 🟡 MINOR | Category: Precision | Impact: Med
- Screen: Checkout (hard.html) | Where: hard.html:67
- Found: Review #1 (2026-10-26) as Q45
- Screenshot: [DT-049_amount-alignment.png](screenshots/issues/DT-049_amount-alignment.png) · full screen: [review-01_checkout_annotated.png](screenshots/screens/review-01_checkout_annotated.png)
- Problem: $19.99 ends at x=**1217**, $68.90 at **1219** (`.item:nth-child(2) .amt{padding-right:2px}`)
- Options:
  - (a) Delete the rule (S): none
- My pick: (a)
- Chosen: —
- Done when: defect no longer measurable
- Proof: —

### DT-050 · Promo row off the form system
- Status: TODO | Severity: 🟡 MINOR | Category: Consistency | Impact: Med
- Screen: Checkout (hard.html) | Where: hard.html:69-70
- Found: Review #1 (2026-10-26) as Q46
- Screenshot: [DT-050_promo-row.png](screenshots/issues/DT-050_promo-row.png) · full screen: [review-01_checkout_annotated.png](screenshots/screens/review-01_checkout_annotated.png)
- Problem: "Apply" text **13.3px** (button font not inherited) vs 15px; promo controls **40px** vs 44px fields
- Options:
  - (a) `font:inherit` on the button; height 44px (S): none
- My pick: (a)
- Chosen: —
- Done when: defect no longer measurable
- Proof: —

#### Cross-page

### DT-053 · Button and radius sprawl
- Status: TODO | Severity: 🟡 MINOR | Category: Tokens | Impact: Med
- Screen: Cross-page | Where: easy.html:27-29,50,57; medium.html:46,51,54,55; hard.html:37,70,75
- Found: Review #1 (2026-10-26) as Q47
- Screenshot: [DT-053_button-token-sprawl.png](screenshots/issues/DT-053_button-token-sprawl.png) · full screen: [review-01_product_annotated.png](screenshots/screens/review-01_product_annotated.png)
- Problem: No size scale; see ui-tokens.json for the proposed set.
- Options:
  - (a) Tokens: control height 44 (inputs, secondary) / 52 (primary CTA), radius 8 everywhere (S): none
- My pick: (a)
- Chosen: —
- Done when: defect no longer measurable
- Proof: —

### DT-054 · Input borders below 3:1
- Status: TODO | Severity: 🟡 MINOR | Category: Contrast | Impact: Med
- Screen: Cross-page | Where: hard.html:37; easy.html:56; medium.html:46,51
- Found: Review #1 (2026-10-26) as Q48
- Screenshot: [DT-054_input-border-contrast.png](screenshots/issues/DT-054_input-border-contrast.png) · full screen: [review-01_checkout_annotated.png](screenshots/screens/review-01_checkout_annotated.png)
- Problem: Empty inputs are hard to locate, especially on the `#FAFAFA` checkout background.
- Options:
  - (a) Border `#8A8F98` (3.25:1) on all inputs (S): heavier look
- My pick: (a)
- Chosen: —
- Done when: defect no longer measurable
- Proof: —

## 🔍 Later (⚪)

- DT-013 · Help column indented 12px: HELP column has `padding-left:12px`: heading at x=852 vs column x=840 · Fix: Remove `.footer-col--help` padding · `easy.html:63` · [DT-013_footer-help-indent.png](screenshots/issues/DT-013_footer-help-indent.png) · Status: TODO
- DT-014 · Nav links 16px right of center: Nav group center x=736 vs page center 720 (space-between with a 133px logo and 100px icon group) · Fix: Use a 3-column grid `1fr auto 1fr` for the header · `easy.html:14` · [DT-014_nav-off-center.png](screenshots/issues/DT-014_nav-off-center.png) · Status: TODO
- DT-031 · Breadcrumb separator spacing: "/" has **4px** before and **10px** after · Fix: `margin:0 8px` · `medium.html:20` · [DT-031_breadcrumb-spacing.png](screenshots/issues/DT-031_breadcrumb-spacing.png) · Status: TODO
- DT-032 · Two line-heights in one description: Paragraph 1 line-height **1.5**, paragraph 2 **1.65** (`p + p` rule) · Fix: Remove the `p + p` rule · `medium.html:66` · [DT-032_paragraph-line-height.png](screenshots/issues/DT-032_paragraph-line-height.png) · Status: TODO
- DT-033 · "Size guide" not styled as a link: Same grey `#6B6B70`, no underline: reads as a label · Fix: Underline it · `medium.html:40, :130` · [DT-033_size-guide-link.png](screenshots/issues/DT-033_size-guide-link.png) · Status: TODO
- DT-051 · Payment badges uneven: AMEX **39.3×24** (viewBox 36×22) vs 38×24; Mastercard tile `#F3F4F6` on white 1.1:1 (no edge) · Fix: Same viewBox 38×24 for all; 1px `#E5E7EB` border on the light tile · `hard.html:184-186` · [DT-051_payment-badges.png](screenshots/issues/DT-051_payment-badges.png) · Status: TODO

## 💡 Ideas from market research (IDEA-*)
— (research not allowed in this review)

## 🔁 Reopened / Regressed / Partial
—

## ✅ Verified
—

## 🚫 Won't fix
—
