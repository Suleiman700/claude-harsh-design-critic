# House standards (mobile-game-specs)

When the project follows the `mobile-game-specs` library, review against **its** rules, not just general taste. A finding that breaks the user's own spec is stronger evidence than any opinion.

## Find the standards (first match wins, per file)
1. The game repo's `docs/game-prompts/NN-*.md` (project copies override the library).
2. The installed `mobile-game-specs` skill's copy of the same file.
3. `docs/game-prompts/project-decisions.md`: values the user confirmed for this game (e.g. "interstitial every 8 purchases"). These beat the spec's defaults.

None found → review with the general checklists only, and don't mention the library.

## Load only the specs for what you're reviewing
| Reviewing | Specs |
|---|---|
| Any screen | 01 design language · 02 buttons & badges · 26 accessibility |
| Popups, pause, rewards, reveal | 03 popups |
| Game screen / HUD, floating world labels | 04 HUD layout · 07 touch controls |
| Coins, prices, purchases | 05 money feedback · 28 upgrades & unlocks |
| Juice / live build feel | 06 feel, sound & haptics |
| Splash, main menu, settings | 08 · 09 · 10 |
| Ads, rate prompt, notifications, offers | 11 · 12 · 13 · 19, plus 03 "Ask budget" |
| Daily reward, goals, gifts, welcome back | 15 retention |
| Tutorial / first session | 23 tutorial · 07 |
| Arabic / Hebrew / long languages | 21 localization & RTL |
| Back button, pause/resume | 24 Android lifecycle |

## How it changes the review
- **Tokens:** the `01` palette tokens and type scale are the project's tokens. Use them instead of `templates/ui-tokens.json`, and mirror them into `ui-tokens.json` for `ui_lint.py`. Any color, size or radius not in `01` (or project-decisions) is a token violation.
- **Measurements:** compare against the spec's numbers: e.g. `04` floating label margin `20` px, `02` badge offset `x = width − 32, y = −14`, button heights `100 / 88–96`, popup width `620`, touch area `88×88`.
- **Rules and "Done when":** each unmet rule or checklist item that the input lets you check is a finding. Unverifiable ones go under Coverage → Not audited, never assumed passed.
- **Spec beats generic advice.** If the spec says one thing and the critic's general checklist another (ad cadence, badge style, palette), the spec wins. Disagree with the spec only as a separate, clearly labeled ⚪ or 🟡 Q block ("Spec challenge"), never by grading the project against your own preference.
- **Citing:** name the spec and rule in the finding: "Floating label 4px from the edge; `04-hud-layout` requires 20px (DT-014)". In the Findings table, Area can be the spec number.
- **Options:** option (a) is usually "apply the spec's default" (small, already agreed). Bigger redesigns come after it.
- **Decisions:** if the user picks an option that changes a spec value for this game, offer once to record it in `project-decisions.md`. Write it only on yes. That file belongs to the builder skill; the critic never edits the spec files themselves.
