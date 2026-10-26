# Inspection checklist

A glance at a screenshot says "looks fine". A consumer's eye says "something is off" without knowing why. Your job is to know why, with numbers. "Layout looks clean" is only allowed after the measurement table.

## Part 0 — Capture plan (before looking at anything)
One row per screen × state × size. With a live build, capture them all; with screenshots only, list what's missing under **Not audited**.

| Screen / state | Why | How to reach it |
|---|---|---|
| First launch / menu | first impression | fresh save |
| Main HUD in play | always on screen | play 10 s |
| Every panel, popup, dialog open | usually forgotten | tap each button |
| Extreme values: 0, 9,999,999, longest name, longest translation | layouts break here | debug values / language switch |
| Late-game state | different UI shows up | debug flags / seeded save |
| Error / disabled / loading / can't-afford | rarely designed | trigger them |

Sizes: target size plus the device matrix extremes (`tokens-devices-perception.md`). Autoplay bots and recordings only show the states they happen to reach; reach the rest deliberately or list them as not audited. Never skip silently.

**Zoom in.** Crop small regions (PIL, or `sips --cropOffset y x --cropToHeightWidth h w in.png --out crop.png` on macOS) and read the crops. Full-frame views hide 4–10px problems. Save and name captures per `screenshots.md` and cite them as evidence.

## Part A — Precision defect hunt (always first, element by element)
Go through **every** element on screen. Do not stop after the first few problems. Measure with `scripts/measure.py` instead of eyeballing, and report the numbers. For each component group (top-bar items, pills, buttons in one panel, list rows, tab icons) fill the measurement table:

| Screen | Group | Member | x | y | w | h | Flag |

Flag within a group when: heights (row) or widths (column) differ by > 2px or > 4% (unless clearly primary vs secondary) · top/bottom/center edges not aligned to the rule the group uses · unequal gaps (> 2px) · different radius, border, fill or shadow · different icon sizes or misaligned icon/text baselines · different inner padding. Groups that pass go on one "checked OK" line with their numbers.

Useful commands:
```
python scripts/measure.py pick shot.png 640,400                 # get exact colors first
python scripts/measure.py blobs shot.png --color "#5CCB32" --tol 40 --min 2000   # all green buttons
python scripts/measure.py fg shot.png --region 713,395,820,500 --bg "#306733" --tol 60  # content center vs container
python scripts/measure.py contrast "#FFFFFF" "#5CCB32"
```

### A1. Content misplaced inside its container
- Content (icon, text, price, number) centered/aligned in its own container, horizontally and vertically. Compare content center with container center (`fg`).
- Stray or misaligned inner layers: a darker/lighter inner rectangle, pressed-state overlay or highlight that doesn't fill the container, sits off-center or ignores the corner radius. Usually a leftover node, wrong anchor, or stuck pressed/disabled style. A price centered inside such a layer instead of the button is a classic.
- Icon + text pairs (gem + "15"): vertically centered on each other, same gap in every instance, centered as a group.
- Unbalanced empty space: content hugging one side of a pill/button with a large empty area on the other (report % empty).
- Repeated elements (shop rows, cards, list items): content at identical positions and identical sizes in every instance. Measure all rows, not one.

### A2. Clipping and edge collisions
- Anything cut by the screen edge, a panel edge, a mask, or the safe area (notch, rounded corners, home indicator, system bars).
- World-space / floating labels (name plates, price tags, "+$" popups, speech bubbles) drifting off-screen or under HUD elements. They must clamp to a screen margin or hide gracefully.
- HUD elements cutting through world labels or each other.
- Text clipped inside its own box: descenders, Arabic diacritics, text stroke.
- Edge margins ≥ ~16px (or safe-area inset) and **equal left and right**. Measure both.

### A3. Overlapping and colliding text
- Two texts drawn on top of each other (transient message spawning on a static label, two world labels sharing an anchor, tooltip over a title).
- Transient messages need their own lane/offset, a backing plate, or must hide the label underneath while shown.
- Text over busy backgrounds without a plate, outline or shadow.
- Labels overlapping characters, icons or tap targets.

### A4. Icon vs emoji mixing
- Classify every icon: OS emoji, flat single-color glyph, multicolor flat illustration, 3D/rendered. Any mix inside one screen or one component group is a defect (e.g. Home 🏠 emoji next to white Restart/Music/Sound glyphs).
- **OS emoji used as UI icons is a defect by itself**: renders differently per device/OS, can't be themed, looks unprofessional. Recommend one icon set styled to the theme.
- Within one style: same size, stroke weight, color, optical centering, padding.

### A5. Component dimension and alignment matching
- Same row/group → same height, baseline, vertical center (e.g. currency pills vs settings button). Report the mismatch in px.
- Siblings of one type (icon buttons, pills, cards, tabs) → same height, radius, padding, border weight, shadow depth, font size.
- Buttons that stretch to fill variable-height rows (shop button 134px in one row, 179px in the next) are a defect.
- Overlaps between stacked components (a header tab overlapping the button below it).
- Alignment lines: draw the content area's left edge, right edge and center line. Items 3–15px off a line others share are worse than clearly offset ("almost aligned" reads as a mistake).
- One spacing scale (e.g. 4/8/12/16/24/32). Flag one-off values, gaps bigger *inside* a group than *between* groups, and anything closer than ~8px to a neighbor or the screen edge.

### A6. Placement logic: does it belong there?
Size and alignment can be perfect while the *location* is wrong.
1. List each placed object, station and control and the area it sits in ("toilet paper shelf → lobby", "trash bin → lobby", "settings → bottom-left").
2. Ask: would it be there in real life, and in the leading competitors?
   - Games/sims: back-of-house items (supplies, storage, trash, laundry, staff rooms) don't sit in guest areas; reception sits by the entrance; guest areas look like guest areas.
   - Apps/web: destructive actions away from primary ones; settings/profile where the platform puts them; related controls grouped; primary action in thumb reach.
3. Flow cost: are stations used in sequence close together, or does the layout force pointless back-and-forth? Does an object block a path or hide behind another from the camera?
4. Each misplaced item is a finding: what, where it is, where it belongs, why (real-world logic, competitor reference, or flow cost). Typical options: move it · build the proper area (e.g. a utility room) · re-theme it so its current spot makes sense.

### A7. Cross-screen consistency
- The same component (button, panel, pill, header) looks the same on every screen: color, radius, font, height.
- The same action has the same icon and label everywhere. Close/back sits in the same corner on every panel.

Each defect: measured numbers + exact fix ("settings 70×70, center y 118", "remove overlay node / anchor full-rect").

## Part B — Screen checklist (every review)
1. **Visual language consistency**: materials (wood, glossy, flat, glass), frames, bevels, shadows, radii, outline weights. Flag anything that looks imported from another style.
2. **Art direction and palette**: run `python scripts/palette.py shot.png --out screenshots/screens/review-NN_<screen>_palette.png`. Flag too many hues, clashing saturations, muddy tones, colors with no role (background, surface, primary, currency/reward, danger). Mismatched free-asset packs (rendering, lighting, outline weight, resolution): say plainly if it reads as an asset-flip. Propose a tightened palette in hex; compare with competitor palettes when research exists.
3. **Hierarchy and contrast**: primary action loudest (confirm with the blur test). WCAG AA: 4.5:1 text, 3:1 large text/bold game text and UI components vs their background.
4. **Sizing and touch targets**: ≥ 44–48pt; sensible proportions.
5. **Semantics and affordance**: one visual treatment = one meaning (a pill must not mean "owned count" in one place and "price" in another).
6. **States**: normal, pressed, hover, focus, disabled, loading, empty, error, **can't-afford** (buy buttons fully active at 0 balance is a defect), out-of-stock, selected, cooldown, **toggle on/off** (music/sound). List missing ones.
7. **Typography**: one font family system, outline/stroke on game text, small-size legibility, number formatting (1,250 / 1.2K), truncation.
8. **Localization and RTL (always)**: Arabic, Hebrew, English. RTL mirroring (nav, progress, arrows, icon direction); Arabic shaping (joined letters); clipped diacritics; overflow in the longest language; fonts that match the style, no system fallback; numbers and mixed-direction strings. If only one language is visible, list what to verify in the others.
9. **Accessibility essentials**: grayscale + colorblind panels from `perception.py` (pieces/states must not collapse); minimum text size; primary actions in the bottom thumb zone; reduce-motion option if heavy shake/flashing.
10. **Audience fit** (profile): colors, symbols, imagery, tone suit the age and market. MENA/Israel: culturally inappropriate imagery, gambling-like visuals, RTL-first expectations.
11. **Web-specific**: breakpoints, layout shift, focus outlines, keyboard navigation, the 5-second above-the-fold test.
