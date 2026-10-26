# UI lint report

Errors: 0 · Warnings: 0 · Info: 0 · (no ui-tokens.json found: token checks skipped)


## Manual CSS/HTML lint (ui_lint.py does not scan .html files)
Same rule classes, applied by hand to easy.html, medium.html, hard.html:

| Code | File:line | Finding | Task |
|---|---|---|---|
| E-EMOJI | easy.html:111 | 🚚 OS emoji used as a feature icon next to SVG icons | DT-004 |
| E-SIBLING | easy.html:27-29 | hero buttons 48px vs 40px in one row | DT-005 |
| E-SIBLING | easy.html:56-57 | newsletter input 44px vs button 38px | DT-009 |
| E-SIBLING | medium.html:29 | `.thumb--alt` 70px vs 72px siblings | DT-028 |
| E-SIBLING | hard.html:35,38 | City label gap 8 vs 6, ZIP input 43 vs 44 | DT-044 |
| E-SIBLING | hard.html:69-70 | promo controls 40px vs 44px fields | DT-050 |
| W-SPRAWL | all | button heights 38/40/44/48/52, radii 6/8/10/12/16/24, 3 primary colors, 7 text greys | DT-052, DT-053 |
| W-ONEOFF | easy.html:18, :39, :63 | one-off `.contact` 14px, `.feature--compact` padding, `.footer-col--help` indent | DT-011, DT-006, DT-013 |
| W-ONEOFF | medium.html:20, :66, :70 | asymmetric breadcrumb margin, `p + p` line-height, odd-row right align | DT-031, DT-032, DT-026 |
| W-ONEOFF | hard.html:36, :67 | phone label #616161, 2px padding on one amount | DT-043, DT-049 |
| W-A11Y | medium.html:42 | `outline:none` on swatches, no replacement | DT-020 |
| W-A11Y | hard.html:55-56 | CSS `order` changes visual order vs tab order | DT-038 |
| I-OVERFLOW | hard.html:57 | `min-width:340px` overflows 390px phones | DT-036 |
| I-OVERFLOW | easy.html, medium.html | no `@media` rules at all | DT-001, DT-015 |
