# Review output format

Save the full review to `docs/harsh-design-critic/design-review/reviews/<YYYY-MM-DD>-review.md` and print it in chat. Never overwrite an existing report: add `-2`, `-3`.

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
Websites and apps without game mechanics use: Precision & polish · Visual consistency · Hierarchy · Layout & responsive · Content & data accuracy ·
Forms & states · Accessibility · Trust & conversion · Localization/RTL · **Overall**

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

> **Report saved to `docs/harsh-design-critic/design-review/reviews/<file>`. My picks are pre-selected. Nothing else has been changed.**
> Reply with one of:
> - `approve all` — apply my pick for every Q, in severity order
> - `approve Q1, Q3` — apply my picks for those Qs only
> - `Q1b, Q2a` — choose a different option per Q
> - `approve quick wins` / `approve all critical`
> - `skip` · `more detail on Q<n>` · `won't fix Q<n> because …`

If the AskUserQuestion tool is available, also offer the choice there with "Apply my picks (Recommended)" first. Then end the turn. Do not start implementing.

With HTML or Both, also add one line before the reply options: "Open `docs/harsh-design-critic/design-review/REPORT.html` to go through the issues, mark each one and copy your decisions back here."

## HTML report (when the user chose HTML or Both)
`design-review/report-data.json` is the single source for the page; `scripts/html_report.py <design-review dir>` turns it into `design-review/REPORT.html` (self-contained, opens offline with a double-click, images linked relative to `design-review/`). Never edit `REPORT.html` by hand; regenerate it.

One file per project, every review in it, **oldest first** (the page shows them in that order, each behind a "Review #NN · date" divider). Append a new review; never drop old ones, since they hold the history of what was fixed.
```
{ "project": "<name>", "updated": "YYYY-MM-DD",
  "reviews": [ { "id": "02", "date": "YYYY-MM-DD", "title": "<screen/feature>", "mode": "Full · desktop 1440",
      "score": 5, "verdict": "<one sentence>", "consumer_take": "<the paragraph>", "strengths": ["..."],
      "scorecard": {"Precision & polish": 5, "Overall": 5}, "report_md": "reviews/<file>.md",
      "coverage": "<audited / not audited>",
      "screens": [{"label": "Default", "image": "screenshots/screens/review-02_<screen>_annotated.png"}],
      "findings": [ { "q": 1, "id": "DT-012", "severity": "major", "area": "Page",
          "title": "<short>", "finding": "<problem with the key number>", "where": "src/x.tsx:42",
          "image": "<the issue crop, or the annotated full screen it is marked on>", "box": [x1, y1, x2, y2],
          "screen": {"image": "screenshots/screens/<...>_annotated.png", "box": [x1, y1, x2, y2]},   (per-issue crops)
          "also": [{"label": "Colorblind sheet", "image": "screenshots/screens/<...>_perception.png"}],
          "options": [{"key": "a", "text": "<option>", "effort": "S"}], "pick": "a", "pick_reason": "<why>",
          "status": "TODO", "chosen": null, "result": null, "proof": null } ] } ] }
```
- `severity`: critical · major · minor · nitpick. `status`: the task board status (TODO, APPROVED, DONE, VERIFIED, PARTIAL, FAILED, WONTFIX, WITHDRAWN, ...). VERIFIED, DONE, WONTFIX and WITHDRAWN count as closed.
- `box` is the issue's box in **image pixels**, the same one given to `annotate.py`/`issue_shots.py`. The page zooms to it; without a box it shows the whole image.
- **Per-issue crops:** point `image` at the crop (no `box`) **and** add `"screen": {"image": "<the annotated full screen>", "box": [x1, y1, x2, y2]}` with the same box given to `issue_shots.py`. Without `screen`, the issue can't be clicked on the full screen in the image viewer.
- If the issue is drawn on an annotated full screen, `image` **must** be that screen and `box` its box there: that is what makes it clickable on the screen in the page. Supporting evidence (a perception sheet, a palette, another state) goes in the optional `"also": [{"label": "...", "image": "..."}]` list, never in place of the screen.
- Every finding of the review goes in, nitpicks too (with one option if the Markdown lists it in one line).
- Paths are relative to `design-review/`. `html_report.py` refuses missing images, duplicate ids, unknown severities and a `pick` that isn't one of the options; fix the JSON and re-run.
- The footer credits the skill and its license; leave it in.

## Quick report (Quick mode)
Same file name and folder. Keep: Verdict, The consumer's take (max 80 words), Scorecard (short), Findings table with the **top 10** ranked by severity, then "Also seen" (one line each, no Q block), then Q blocks for 🔴 and 🟠 only, then the STOP prompt. Evidence column: the annotated full screen (if images were chosen) plus `file:line` or the measurement; no per-issue crops in Quick. Skip UI measurements tables, competition, flow map and the long coverage list; one line instead: "Quick review: <width>, default state; not checked: other widths, states, perception, market." End with: "Want the full review? It covers every finding, phone + desktop and all states."

## Store mode (only when asked)
Use market research (or run it) to collect the top 5 competitors' icons and first screenshots; board at real store size. Judge small-size icon readability and stand-out, whether the first two screenshots sell the core loop without reading, text overlay legibility, style consistency, localized RTL listing, title and short description. Same severity, Q-block and scorecard system, with categories Icon · Screenshots · Copy · Localization · Stand-out.
