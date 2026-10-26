# Answer key: planted issues for harsh-design-critic test

Kept outside the project folder so the critic can't read it. Score = issues found / planted, minus false positives on the "clean controls".

## easy.html: landing page (10 planted)
| ID | Component | Planted issue | Proof |
|---|---|---|---|
| E1 | Nav | "Contact" link is 14px; the other links are 16px | `.nav-links a.contact` |
| E2 | Hero CTAs | Primary button is 48px tall, secondary is 40px, side by side | `.btn-secondary { height: 40px }` |
| E3 | Hero subtitle | `#a8a8a8` on white ≈ 2.4:1, fails WCAG AA (4.5:1) | `.hero p` |
| E4 | Feature cards | Third card has 20px padding vs 32px: icon/title/text start 12px higher and further left | `.feature--compact` |
| E5 | Mixed icons | 🚚 OS emoji next to two stroke SVG icons | 2nd feature card |
| E6 | Product grid | Column gap 24px vs row gap 8px | `.products { gap: 8px 24px }` |
| E7 | Product cards | Long title wraps, so that card's price/button sit 24px lower than its neighbours (not bottom-aligned) | Card 2, no flex column |
| E8 | Newsletter | Input 44px vs button 38px; placeholder-only field, no label | `.newsletter .btn` |
| E9 | Newsletter copy | Typo "Recieve" | newsletter `<p>` |
| E10 | Footer | "Help" column is indented 12px; headings don't line up | `.footer-col--help` |

Clean controls (should NOT be flagged as broken): header icon buttons, hero headline, section titles/subtitles spacing.

## medium.html: product page (15 planted)
| ID | Component | Planted issue | Proof |
|---|---|---|---|
| M1 | Breadcrumb | Separator spacing 4px left / 10px right | `.crumbs .sep` |
| M2 | Thumbnails | Third thumb is 70px, the others 72px (also not active-bordered) | `.thumb--alt` |
| M3 | Price badge | "Save 20%" but $89 → $74 is 16.9% | price row |
| M4 | Rating | 5 full stars shown for a 4.2 rating | `.stars` |
| M5 | Review count | "128 reviews" vs tab "Reviews (126)"; tab only shows 2 reviews | rating vs tab |
| M6 | Swatches | "Chalk" white swatch has a white border on white: invisible | 4th swatch |
| M7 | Swatches | Selected state `#c8c8c8` vs unselected `#ddd` is nearly the same | `.swatch.selected` |
| M8 | Swatches | `outline: none`, so no keyboard focus indicator | `.swatch` |
| M9 | Sizes | Out-of-stock sizes only at 0.85 opacity, no strike/label | `.size:disabled` |
| M10 | Quantity | Minus goes to 0 and negative numbers | JS `minus` |
| M11 | Add to cart | Radius 10px; every other control is 6px | `.add` |
| M12 | Tabs | Active underline sits 1px above the divider (floats) | `bottom: 1px` |
| M13 | Description | 2nd paragraph line-height 1.65 vs 1.5 | `.panel p + p` |
| M14 | Specs table | Value alignment alternates right/left by row; units "1.2kg" vs "800 g" | `.specs tr:nth-child(odd)` |
| M15 | Related rail | 4th card clipped by 16px with no arrows/scroll affordance; 5th card unreachable | `.rail { overflow: hidden }` |

Clean controls: gallery main image, header nav, buy-row heights (52px all), ship note.

## hard.html: checkout (17 planted)
| ID | Component | Planted issue | Proof |
|---|---|---|---|
| H1 | Stepper | Connector lines are 2px below the circle centre (line centre 18px vs circle centre 16px) | `.line { margin-top: 17px }` |
| H2 | Phone label | Label grey `#616161` vs `#5f6368` everywhere else (palette drift) | `.field--phone label` |
| H3 | Phone field | Required in code, but no asterisk | `#phone required` |
| H4 | City label | Label→input gap 8px vs 6px, so the City input sits 2px lower than ZIP | `.field--city label` |
| H5 | ZIP input | 43px tall vs 44px | `.field--zip input` |
| H6 | Hint text | `#8a8f98` on white ≈ 3.3:1 at 12px, fails AA | `.hint` |
| H7 | Email error | `#e57373` ≈ 2.9:1, colour-only, appears between input and hint and pushes layout (blur with "abc") | `.error` |
| H8 | Shipping options | Selected card border 2px vs 1px, so content shifts 1px when switching | `.ship-opt.selected` |
| H9 | Payment row | DOM order CVC→Expiry, visual order Expiry→CVC: Tab order is reversed | `order:` on pay-row |
| H10 | Expiry | Placeholder "MM/YY" (5 chars) but `maxlength="4"`: can't type the shown format | `#exp` |
| H11 | Order math | Line items $68.90 + $19.99 = $88.89 but subtotal says $88.99 | summary |
| H12 | Price column | Tea-towel price has 2px right padding: right edges don't line up | `.item:nth-child(2) .amt` |
| H13 | Promo button | Missing `font: inherit`, so "Apply" renders at the browser default 13.33px vs 15px | `.promo button` |
| H14 | Place order hover | Hover goes lighter `#60a5fa`: white text drops to ≈ 2.5:1 | `.place:hover` |
| H15 | Trust badges | AMEX uses a cropped viewBox, so it renders ~3% larger than VISA/MC | 3rd svg |
| H16 | Legal text | 11px grey `#8a8f98`, below readable size and contrast | `.legal` |
| H17 | Mobile ≤760px | Card number `min-width: 340px` + stepper (4×72 + 3×32 = 384px) overflow a 390px screen: horizontal scroll | media query |

Clean controls: header "Secure checkout", card containers, Place-order default state, totals arithmetic (88.99 + 5.99 + 7.12 = 102.10 is correct given the shown subtotal; Express recalculates correctly).

## Result (blind run, 2026-10-26)
42 / 42 found. Note: the hero was listed as a clean control, but the review correctly found it 32px off the page grid (DT-002): `.hero` padding overrides `.container` padding. That was an accidental bug, not a false positive.
