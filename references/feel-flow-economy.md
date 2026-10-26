# Game feel, flow, ads and economy

## Game feel and juice (games: heavy weight)
For every player action (tap, drag, drop, place, merge, clear, combo, win, lose, reward, purchase). Screenshots: judge the static evidence, list what must be verified live. Live builds: judge timing and easing directly.
- **Input response** within ~100ms: press scale 0.9–0.95, highlight, lift on drag.
- **Motion**: squash/stretch, overshoot/bounce on settle, easing (never linear).
- **Placement**: snap, landing impact, ghost/preview of where the piece lands.
- **Effects**: particles scaled to event importance; screen shake only for big moments.
- **Sound**: distinct cue per action, rising pitch on combos.
- **Haptics**: light on tap, strong on big events.
- **Escalation**: a 5x combo must feel far bigger than a 1x. Flat feedback = MAJOR.
- **Rewards**: coins flying to the counter, ticking counters, buildup and payoff.
- **Fail state**: fair, readable reason; fast retry.
Compare speed, size and frequency with competitors (gameplay videos from research).

## Flow review (when input covers more than one screen)
Games: launch → FTUE → first win → rewards → shop → next-session hook. Apps/sites: launch → core task → success → return.
- Taps from launch to core gameplay/task, vs competitors.
- Friction: unskippable screens, early permission prompts, walls of text, dead ends, stacked modals.
- FTUE: mechanic understood in ~30s without reading; first win quick and satisfying.
- Session hooks: daily rewards, visible progress, reason to return. Present, well-designed, not annoying.
- Output a numbered flow map with friction points marked. One screen only → list flows you couldn't judge.

## Ads and economy (retention-first)
Revenue that drives uninstalls is a loss.
- **Interstitials**: never during active play; natural breaks only; frequency vs competitors (not every level from level 1).
- **Rewarded ads**: clear offer ("Watch ad → +50 coins"), worthwhile reward, opt-in, at the moment of need (continue on fail, double reward, can't-afford tap).
- **Banners**: never over gameplay or next to tap targets. Accidental-click placement risks AdMob policy strikes.
- **Economy**: clear soft vs hard currency roles; prices meaningful against earn rate (not instant, not a grind wall); clear owned/affordable state; a path from the HUD "+" to get more currency. Compare prices and booster sets with competitors.
- **Dark patterns**: fake close buttons, misleading offers, pressure timers. Flag them.

## Consumer criteria beyond the UI (whenever the project or a build is available)
Judge as a skeptical player/user looking for a reason to quit. Skip what doesn't apply.
- **First 60 seconds**: is it clear what to do and why to care?
- **Core loop / core value**: fun or useful, or tedious and shallow?
- **Polish**: placeholder art or text, typos, janky animation, missing sound.
- **Stability and performance**: crashes, errors in logs, slow loads, frame drops, failing tests (run them read-only if safe).
- **Content and depth**: still playing/using it after a day? A week? How long does the content last, is there an endgame?
- **Trust and safety**: permissions, data handling, anything that feels shady.
- **Value vs. competitors**: why this over the obvious alternative?

## Idea and positioning (when research exists)
- Core loop and mechanics: what you have that they lack; table stakes they all have that you lack.
- Differentiation: a clear reason to pick this over the leader? If not, say so and suggest 1–3 concrete differentiators.
- Competitor complaints you can solve (from their reviews).
- Steal-worthy ideas: features, UI patterns, juice moments to adapt (never copy assets). Each becomes an `IDEA-` task.
