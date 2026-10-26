# Review output format

Save the full review to `docs/game-prompts/design-review/reviews/<YYYY-MM-DD>-review.md` and print it in chat. Never overwrite an existing report: add `-2`, `-3`.

```
# Design Review: <project> — <screen/feature/flow> — Review #N

**Verdict:** <score>/10 — "<one blunt sentence, written like a skeptical store-review headline>"

## The consumer's take
<80–150 words, first person, a skeptical player/user who has seen a hundred products like this,
looking for a reason to uninstall. Gut feeling only; the evidence comes below.>

## What (barely) works
- <max 3 bullets, only if genuinely above average, or "Nothing stood out.">

## Previous issues        (only if history exists)
DT-004 STILL BROKEN (reported in #2) · DT-007 VERIFIED · score trend Precision 4→6 ...

## Scorecard
Precision & polish X · Visual consistency X · Art & palette X · Hierarchy X · Layout X · Game feel X ·
Flow & FTUE X · Placement logic X · Localization/RTL X · Accessibility X · Audience fit X ·
Monetization X · Market positioning X · **Overall X** (judgment, not an average; any 🔴 caps it at 5)

## Evidence
<links to screens/review-NN_<screen>_annotated.png (every box labeled with its task id), perception sheet if it shows a problem,
comparison board if research exists, palette: extracted hex + proposed palette>

## Findings
| Q | Task | Severity | Area | Finding (with the key number) | Evidence |
|---|------|----------|------|-------------------------------|----------|
| 1 | DT-001 | 🔴 | Shop | Price centered in stray overlay, 28px right of button center | [DT-001_shop-price-overlay.png](../screenshots/issues/DT-001_shop-price-overlay.png) |

## UI measurements
| Screen | Group | Member | x | y | w | h | Flag |
(only groups with at least one flag) · checked OK: <groups that passed, e.g. "top-bar gaps equal (22px)">

## Versus the competition   (when research exists)
<feature matrix ✅/➖/❌/⭐ + table stakes missing, where it can win, unique hook, sources>

## Flow map   (if reviewed)

## Coverage
- Audited: <screens × states × device sizes>
- Not audited: <states/sizes/languages not reached and why>

## Summary
🔴 Deal-breakers: N · 🟠 Major: N · 🟡 Minor: N · ⚪ Nitpick: N

**Q1. 🔴 <finding title>: <one-line problem with the key number>** (DT-001)
![DT-001](../screenshots/issues/DT-001_<slug>.png)
- (a) <solution> (effort S): <trade-off>
- (b) <solution> (effort M): <trade-off>
- (c) <solution> (effort L): <trade-off>
- **My pick: (a)** because <one line: impact vs effort, what it fixes, what it risks>
- How competitors do it: <one line from research, or omit if no research>

**Q2. 🟠 ...**
```

## Severity
- 🔴 **Deal-breaker / CRITICAL**: broken, unreadable, untappable, blocks the core action, policy risk. "I'd uninstall."
- 🟠 **Major**: clearly amateur, hurts retention or trust. "I'd complain in a review."
- 🟡 **Minor**: noticeable polish gap. Several related minors may be grouped into one 🟠 "UI feels unfinished" Q.
- ⚪ **Nitpick**: perfectionist detail. Listed in one line each at the end, no options needed.

## Q block rules
- One Q per finding = one `DT-`/`IDEA-` task = the label on the annotated screenshots = one image in `screenshots/issues/` (when screenshots are on). Always write both: `Q12 (DT-018)`.
- Ordered by severity. 2–3 options, each on its own line, lettered (a)(b)(c), each with effort (S/M/L) and its trade-off.
- Options go small and close to the existing code first; the bigger redesign is the last option.
- Options must be concrete: exact values, layout, component, or code change (file:line when code is available).
- The last option line is always `My pick: (<letter>) because <reason>`. Exactly one pick. Never leave it out.
- Blank line between Q blocks. No separate "Solutions" section; the Q blocks are the solutions.
- Guesses are labeled `(unverified)`. Every other claim has evidence: a measurement, a screenshot region, `file:line`, or a source URL.

## End of the review: STOP and wait
After writing the report and updating DESIGN_TASKS.md and REVIEW_LOG.md, end with:

> **Report saved to `docs/game-prompts/design-review/reviews/<file>`. My picks are pre-selected. Nothing else has been changed.**
> Reply with one of:
> - `approve all` — apply my pick for every Q, in severity order
> - `approve Q1, Q3` — apply my picks for those Qs only
> - `Q1b, Q2a` — choose a different option per Q
> - `approve quick wins` / `approve all critical`
> - `skip` · `more detail on Q<n>` · `won't fix Q<n> because …`

If the AskUserQuestion tool is available, also offer the choice there with "Apply my picks (Recommended)" first. Then end the turn. Do not start implementing.

## Store mode (only when asked)
Use market research (or run it) to collect the top 5 competitors' icons and first screenshots; board at real store size. Judge small-size icon readability and stand-out, whether the first two screenshots sell the core loop without reading, text overlay legibility, style consistency, localized RTL listing, title and short description. Same severity, Q-block and scorecard system, with categories Icon · Screenshots · Copy · Localization · Stand-out.
