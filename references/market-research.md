# Market research (similar projects on the internet)

## Permission
- Stored in the project profile (REVIEW_LOG.md): `Market research: allowed (date)` or `declined (date)`.
- Never asked yet → ask once, together with any other missing profile fields: "Can I search the internet for similar games/apps and save their screenshots, descriptions, store info and reviews for comparison?"
- Declined → review without research; say comparisons are limited.
- **The user can ask any time** ("research competitors", "compare with other games", "find similar apps"): do it then, even if declined earlier, but don't change the stored permission unless they say so.

## Freshness
Research under ~30 days old in `market-research/` → reuse it, only search for what the current screen needs. Older or missing → full pass.

## Full pass
A consumer never judges a product alone; they judge it against what's already on their phone.

**Find them.** Start from what the project says it imitates (README "in the style of X", store text, genre words). Search `<genre> game/app`, `games like <X>`, `<X> alternatives`, and store "similar apps" lists. Pick 3–5: the market leader (top-grossing), 1–2 direct look-alikes, the one closest in idea and scope, and one fresh/indie take if it exists. Sources: web and image search, Google Play / App Store / Steam pages, review aggregators, Reddit, deconstruction articles, wikis, gameplay videos.

**Privacy:** only send generic search terms (genre, competitor names). Never send project code, internal names, user data or secrets.

**Evidence:** cite every claim with a URL. A fact from a single unofficial source is marked `(single source)`. Nothing from memory.

For each competitor write `market-research/competitors/<slug>/notes.md`:
```
# <Name>
- Developer · Store link · Downloads · Rating · Last update   (source URLs)
## Idea
Store description summarized in your own words · core loop · what happens in the first 2, 10 and 30 minutes ·
progression and depth (areas/levels/tiers, how long content lasts, endgame) · systems (upgrades, automation,
special customers, side activities, events, offline progress) · retention (daily quests, login rewards, goals,
collections) · what makes it unique
## Visual design
Art style · palette (hex, extracted with palette.py from saved screenshots) · HUD layout ·
booster/shop/menu design · icon style · how they handle the screens the user has
## Store and reception
Recurring praise and complaints from reviews, paraphrased, grouped by theme, rough frequency
## Monetization
Ad placements and frequency · rewarded offers · boosters and prices · shop structure · currencies · IAP packs
## Steal-worthy
Specific ideas to adapt (→ IDEA- tasks)
```
Save the icon and 3–6 representative screenshots next to it (private internal reference only; record each source URL; if downloads are blocked, store the image URLs instead). Paraphrase store text and reviews; don't paste long passages.

Update `market-research/INDEX.md`: competitor list, date, one line on why each was chosen, permission status.

## Comparison board
```
python scripts/compare.py market-research/comparison-board-<date>.png --title "Shop screen vs market" \
  --item "Yours=shot.png" --item "Block Blast=competitors/block-blast/shop.png" --item "Royal Match=competitors/royal-match/shop.png"
```
Crop competitor screenshots to the same element (booster bar, shop, top bar) when possible.

## Feature matrix and gap table (`market-research/gap-table.md`)
Feature matrix, using ✅ has it · ➖ weak · ❌ missing · ⭐ better than competitors:
| Feature / quality | This project | Competitor A | Competitor B | Notes |

Gap table:
| Area | Competitors do | You do | Gap | Steal-worthy idea | Q / Task |
Cover visual design, idea and mechanics, store and reception, monetization.

Then answer three questions bluntly:
1. **Table stakes missing**: what every competitor has and this one doesn't. Consumers leave over these → 🟠 or 🔴 Q blocks, area "Vs. competition".
2. **Where it can win**: competitors' top complaints this project can avoid (ad spam, bugs, grind). The cheapest way to stand out → a Q block, or an option inside one (e.g. "(b) rewarded ads only, never forced").
3. **Unique hook**: what this project does that none of them do. If nothing, say so; that is a finding too.

Copy mechanics only as ideas; never suggest copying assets, names or trademarked content.

## HTML report (`market-research/report-<date>.html`)
After every full pass: one self-contained page (images by relative path or embedded) with summary verdict on market position · a card per competitor (icon, screenshots, stats, idea, palette swatches, monetization, top praise/complaints, source links) · comparison board · gap table · steal-worthy ideas · differentiation suggestions · links to generated task ids. Tell the user where it is; offer to open or publish it.
