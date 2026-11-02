#!/usr/bin/env python3
"""Build the interactive HTML review report from report-data.json.

Usage:
  python html_report.py <design-review dir>            # reads report-data.json, writes REPORT.html
  python html_report.py <design-review dir> --check    # validate the JSON only

The JSON is the single source of truth for every review and finding: the skill writes it
during a review and updates it after every fix (status, chosen option, proof, result), then
re-runs this script. REPORT.html is fully regenerated each time; never edit it by hand.

The page is self-contained (data, CSS and JS inline) and links images relative to the
design-review folder, so it opens straight from the project with a double-click, offline.
The user's decisions and notes are kept in the browser (localStorage) and exported with
the "Copy decisions" button as lines the skill understands ("fix DT-012 c", ...).

report-data.json:
{
  "project": "Shop app",
  "updated": "2026-11-02",
  "reviews": [                                   # oldest first; shown in that order
    {
      "id": "02", "date": "2026-11-02", "title": "/checkout", "mode": "Full · desktop 1440",
      "score": 5, "verdict": "one blunt sentence", "consumer_take": "80-150 words",
      "strengths": ["..."], "scorecard": {"Precision & polish": 5, "Overall": 5},
      "report_md": "reviews/2026-11-02-review.md",
      "coverage": "Audited ... Not audited ...",
      "screens": [{"label": "Default", "image": "screenshots/screens/review-02_x_annotated.png"}],
      "findings": [
        {
          "q": 1, "id": "DT-012", "severity": "major",       # critical | major | minor | nitpick
          "area": "Page", "title": "short title", "finding": "the problem, with the key number",
          "where": "src/file.tsx:42", "image": "screenshots/...png", "box": [x1, y1, x2, y2],
          "screen": {"image": "screenshots/screens/review-02_x_annotated.png", "box": [x1, y1, x2, y2]},
                                   # with per-issue crops: where the issue sits on the full screen
          "also": [{"label": "Colorblind sheet", "image": "screenshots/...png"}],   # optional supporting images
          "options": [{"key": "a", "text": "...", "effort": "S"}],
          "pick": "a", "pick_reason": "...",
          "status": "TODO",        # TODO APPROVED IN PROGRESS DONE VERIFIED PARTIAL FAILED WONTFIX WITHDRAWN ...
          "chosen": "a", "result": "what happened", "proof": "screenshots/proof/DT-012_proof.png"
        }
      ]
    }
  ]
}
"""

import argparse
import html
import json
import os
import sys

REPO_URL = "https://github.com/Suleiman700/claude-harsh-design-critic"
SEVERITIES = ("critical", "major", "minor", "nitpick")
CLOSED = ("VERIFIED", "DONE", "WONTFIX", "WITHDRAWN")


def validate(data, base):
    problems = []
    if not isinstance(data.get("reviews"), list) or not data["reviews"]:
        problems.append("reviews: missing or empty")
        return problems
    seen = set()
    for r in data["reviews"]:
        rid = r.get("id", "?")
        for key in ("id", "date", "title", "findings"):
            if key not in r:
                problems.append(f"review {rid}: missing '{key}'")
        for f in r.get("findings", []):
            fid = f.get("id", "?")
            if fid in seen:
                problems.append(f"{fid}: duplicate id")
            seen.add(fid)
            if f.get("severity") not in SEVERITIES:
                problems.append(f"{fid}: severity must be one of {', '.join(SEVERITIES)}")
            for key in ("title", "finding", "status"):
                if not f.get(key):
                    problems.append(f"{fid}: missing '{key}'")
            for key in ("image", "proof"):
                path = f.get(key)
                if path and not os.path.exists(os.path.join(base, path)):
                    problems.append(f"{fid}: {key} not found: {path}")
            scr = f.get("screen")
            if scr is not None:
                if not os.path.exists(os.path.join(base, scr.get("image", ""))):
                    problems.append(f"{fid}: screen image not found: {scr.get('image')}")
                if not isinstance(scr.get("box"), list) or len(scr["box"]) != 4:
                    problems.append(f"{fid}: screen.box must be [x1, y1, x2, y2]")
            for extra in f.get("also", []):
                if not os.path.exists(os.path.join(base, extra.get("image", ""))):
                    problems.append(f"{fid}: also image not found: {extra.get('image')}")
            box = f.get("box")
            if box is not None and (not isinstance(box, list) or len(box) != 4):
                problems.append(f"{fid}: box must be [x1, y1, x2, y2]")
            keys = [o.get("key") for o in f.get("options", [])]
            if f.get("pick") and f["pick"] not in keys and "+" not in f["pick"]:
                problems.append(f"{fid}: pick '{f['pick']}' is not one of the options {keys}")
        for s in r.get("screens", []):
            if s.get("image") and not os.path.exists(os.path.join(base, s["image"])):
                problems.append(f"review {rid}: screen not found: {s['image']}")
    return problems


def build(data):
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    title = html.escape(f"Design review — {data.get('project', 'Project')}")
    return (TEMPLATE
            .replace("__TITLE__", title)
            .replace("__DATA__", payload)
            .replace("__REPO__", REPO_URL))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir", help="design-review folder containing report-data.json")
    ap.add_argument("--check", action="store_true", help="validate only, do not write REPORT.html")
    args = ap.parse_args()

    src = os.path.join(args.dir, "report-data.json")
    with open(src, encoding="utf-8") as fh:
        data = json.load(fh)
    problems = validate(data, args.dir)
    if problems:
        print("report-data.json problems:", *problems, sep="\n  - ", file=sys.stderr)
        sys.exit(1)
    if args.check:
        print("report-data.json OK")
        return
    out = os.path.join(args.dir, "REPORT.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(build(data))
    total = sum(len(r["findings"]) for r in data["reviews"])
    print(f"{out} ({len(data['reviews'])} reviews, {total} findings)")


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root {
  --bg: #f6f7f9; --card: #fff; --text: #111827; --muted: #5b6474; --line: #e5e7eb;
  --accent: #4338ca; --accent-soft: #eef2ff;
  --critical: #b91c1c; --critical-bg: #fee2e2;
  --major: #c2410c; --major-bg: #ffedd5;
  --minor: #a16207; --minor-bg: #fef9c3;
  --nitpick: #475569; --nitpick-bg: #f1f5f9;
  --ok: #15803d; --ok-bg: #dcfce7;
}
* { box-sizing: border-box; }
body { margin: 0; font: 15px/1.5 Inter, -apple-system, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); }
button, input, select, textarea { font: inherit; }
a { color: var(--accent); }
.top { position: sticky; top: 0; z-index: 5; background: rgba(255,255,255,.92); backdrop-filter: blur(8px); border-bottom: 1px solid var(--line); }
.top-inner { max-width: 1240px; margin: 0 auto; padding: 14px 24px; display: flex; gap: 16px; align-items: center; flex-wrap: wrap; }
.brand { font-weight: 700; font-size: 17px; margin-right: auto; }
.brand small { display: block; font-weight: 500; font-size: 12px; color: var(--muted); }
.stats { display: flex; gap: 8px; flex-wrap: wrap; }
.stat { padding: 4px 10px; border-radius: 999px; background: var(--nitpick-bg); font-size: 12.5px; font-weight: 600; color: var(--muted); }
.stat b { color: var(--text); }
.filters { display: flex; gap: 8px; flex-wrap: wrap; }
.filters select, .filters input { height: 34px; border: 1px solid var(--line); border-radius: 8px; padding: 0 10px; background: #fff; }
.filters input { width: 200px; }
main { max-width: 1240px; margin: 0 auto; padding: 24px 24px 120px; }
.toc { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }
.toc a { text-decoration: none; padding: 6px 12px; border-radius: 8px; background: #fff; border: 1px solid var(--line); color: var(--text); font-size: 13px; font-weight: 600; }
.toc a span { color: var(--muted); font-weight: 500; }
.divider { display: flex; align-items: center; gap: 14px; margin: 40px 0 16px; color: var(--muted); font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
.divider::before, .divider::after { content: ""; flex: 1; height: 1px; background: var(--line); }
.review { background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 24px; box-shadow: 0 1px 2px rgba(0,0,0,.03); }
.review { padding: 0; overflow: hidden; }
.review-toggle { width: 100%; display: grid; grid-template-columns: auto 1fr auto auto; gap: 16px; align-items: center; padding: 18px 24px; border: 0; background: none; cursor: pointer; text-align: left; color: inherit; }
.review-toggle:hover { background: #fafbff; }
.review-toggle .mini { width: 46px; height: 46px; border-radius: 12px; display: grid; place-items: center; background: var(--accent-soft); color: var(--accent); font-weight: 800; font-size: 18px; }
.review-toggle h2 { margin: 0; font-size: 19px; }
.review-toggle .sub { color: var(--muted); font-size: 13px; margin-top: 2px; }
.review-toggle .counts { display: flex; gap: 6px; flex-wrap: wrap; justify-content: flex-end; }
.chev { width: 34px; height: 34px; border-radius: 8px; display: grid; place-items: center; border: 1px solid var(--line); background: #fff; color: var(--muted); }
.chev svg { transition: transform .2s; }
.review.open .chev svg { transform: rotate(180deg); }
.review-toggle:hover .chev { color: var(--accent); border-color: var(--accent); }
.review-toggle:focus { outline: none; }
.review-toggle:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; border-radius: 16px; }
.review-body { display: none; padding: 0 24px 24px; border-top: 1px solid var(--line); }
.review.open .review-body { display: block; }
.review-head { display: grid; grid-template-columns: auto 1fr; gap: 20px; align-items: start; padding-top: 20px; }
.toc-row { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; margin-bottom: 20px; }
.toc-row .toc { margin: 0; margin-right: auto; }
.toc-actions { display: flex; gap: 8px; }
.toc-actions button { border: 1px solid var(--line); background: #fff; border-radius: 8px; height: 32px; padding: 0 12px; font-size: 13px; font-weight: 600; cursor: pointer; }
.to-top { position: fixed; right: 24px; bottom: 78px; z-index: 11; width: 44px; height: 44px; border-radius: 50%; border: 1px solid var(--line); background: #fff; box-shadow: 0 4px 14px rgba(0,0,0,.12); cursor: pointer; font-size: 18px; font-weight: 700; opacity: 0; pointer-events: none; transition: opacity .2s; }
.to-top.show { opacity: 1; pointer-events: auto; }
.score { width: 76px; height: 76px; border-radius: 18px; display: grid; place-items: center; background: var(--accent-soft); color: var(--accent); font-size: 28px; font-weight: 800; line-height: 1; }
.score small { display: block; font-size: 11px; font-weight: 600; color: var(--muted); text-align: center; }
.review h2 { margin: 0 0 4px; font-size: 22px; }
.meta { color: var(--muted); font-size: 13px; }
.verdict { margin: 10px 0 0; font-size: 16px; font-weight: 600; }
details.take { margin-top: 14px; }
details.take summary { cursor: pointer; color: var(--accent); font-weight: 600; font-size: 13px; }
details.take p { margin: 8px 0 0; color: #374151; }
.scorecard { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 14px; }
.chip { font-size: 12px; padding: 3px 9px; border-radius: 999px; background: var(--nitpick-bg); color: #374151; }
.chip b { margin-left: 4px; }
.screens { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 16px; }
.screens button { flex: 0 0 auto; border: 1px solid var(--line); background: #fff; border-radius: 10px; padding: 6px; cursor: pointer; text-align: left; }
.screens img { display: block; width: 150px; height: 90px; object-fit: cover; object-position: top; border-radius: 6px; }
.screens span { display: block; font-size: 12px; color: var(--muted); margin-top: 4px; }
table { width: 100%; border-collapse: collapse; margin-top: 20px; }
th { white-space: nowrap; text-align: left; font-size: 11.5px; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); padding: 10px 12px; border-bottom: 1px solid var(--line); }
td { padding: 12px; border-bottom: 1px solid var(--line); vertical-align: top; }
tr.issue { cursor: pointer; }
tr.issue:hover td { background: #fafbff; }
tr.issue.active td { background: var(--accent-soft); }
tr.issue.closed td { color: var(--muted); }
.id { font-family: ui-monospace, Menlo, monospace; font-size: 13px; white-space: nowrap; }
.sev { display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: .04em; padding: 2px 8px; border-radius: 6px; text-transform: uppercase; white-space: nowrap; }
.sev-critical { color: var(--critical); background: var(--critical-bg); }
.sev-major { color: var(--major); background: var(--major-bg); }
.sev-minor { color: var(--minor); background: var(--minor-bg); }
.sev-nitpick { color: var(--nitpick); background: var(--nitpick-bg); }
.status { font-size: 12px; font-weight: 600; white-space: nowrap; }
.status.closed { color: var(--ok); }
.decision { font-size: 12.5px; font-weight: 600; white-space: nowrap; color: var(--muted); }
.decision.set { color: var(--accent); }
.title-cell b { display: block; font-weight: 600; }
.title-cell span { font-size: 13px; color: var(--muted); }
.empty { padding: 24px; text-align: center; color: var(--muted); }
/* Detail drawer */
.scrim { position: fixed; inset: 0; background: rgba(17,24,39,.35); opacity: 0; pointer-events: none; transition: opacity .2s; z-index: 20; }
.scrim.open { opacity: 1; pointer-events: auto; }
.drawer { position: fixed; top: 0; right: 0; bottom: 0; width: min(760px, 100%); background: #fff; z-index: 21; transform: translateX(100%); visibility: hidden; transition: transform .25s ease, visibility .25s; display: flex; flex-direction: column; }
.drawer.open { transform: none; visibility: visible; box-shadow: -10px 0 30px rgba(0,0,0,.12); }
.drawer-head { padding: 18px 22px; border-bottom: 1px solid var(--line); display: flex; gap: 12px; align-items: start; }
.drawer-head { align-items: center; }
.issue-title { margin: 4px 0 0; font-size: 19px; line-height: 1.35; }
.drawer-head .nav { margin-left: auto; display: flex; gap: 6px; }
.icon-btn { border: 1px solid var(--line); background: #fff; border-radius: 8px; height: 34px; min-width: 34px; padding: 0 10px; cursor: pointer; font-weight: 600; }
.drawer-body { padding: 18px 22px 30px; overflow-y: auto; }
.viewer { position: relative; height: 340px; border-radius: 12px; overflow: hidden; background: #0f172a; }
.viewer.full { height: auto; max-height: 70vh; overflow: auto; background: #f1f5f9; }
.viewer img { position: absolute; top: 0; left: 0; transform-origin: 0 0; max-width: none; }
.viewer.full img { position: static; width: 100%; transform: none; }
.viewer .mark { position: absolute; border: 3px solid #ef233c; border-radius: 4px; pointer-events: none; box-shadow: 0 0 0 9999px rgba(15,23,42,.25); }
.viewer-bar { display: flex; gap: 8px; margin: 10px 0 18px; align-items: center; font-size: 13px; color: var(--muted); flex-wrap: wrap; }
.seg { display: inline-flex; border: 1px solid var(--line); border-radius: 9px; overflow: hidden; background: #fff; }
.seg button, .bar-btn { display: inline-flex; align-items: center; gap: 6px; height: 32px; padding: 0 12px; font-size: 13px; font-weight: 600; color: var(--muted); background: #fff; border: 0; cursor: pointer; text-decoration: none; }
.seg button + button { border-left: 1px solid var(--line); }
.seg button.on { background: var(--accent-soft); color: var(--accent); }
.seg button:not(.on):hover, .bar-btn:hover { color: var(--accent); }
.bar-btn { border: 1px solid var(--line); border-radius: 9px; height: 30px; font-size: 12.5px; }
.viewer-wrap { position: relative; }
.img-actions { position: absolute; top: 10px; right: 10px; z-index: 2; display: flex; gap: 8px; }
.img-open { width: 36px; height: 36px; border-radius: 50%; display: grid; place-items: center; background: rgba(255,255,255,.95); color: var(--text); box-shadow: 0 2px 8px rgba(0,0,0,.25); }
.img-open:hover { color: var(--accent); background: #fff; }
.img-open:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.ext { display: inline-flex; align-items: center; gap: 4px; }
.lightbox { position: fixed; inset: 0; z-index: 40; background: rgba(15,23,42,.88); display: none; flex-direction: column; }
.lightbox.open { display: flex; }
.lb-head { display: flex; gap: 12px; align-items: center; padding: 12px 20px; color: #fff; }
.lb-head b { margin-right: auto; }
.lb-head .hint { color: #cbd5e1; font-size: 13px; }
.lb-head a { color: #c7d2fe; }
.lb-head .icon-btn { background: #fff; }
.lb-zoom { border-color: #475569; background: transparent; }
.lb-zoom button { background: transparent; color: #cbd5e1; height: 30px; }
.lb-zoom button + button { border-left-color: #475569; }
.lb-zoom button.on { background: #fff; color: #111827; }
.lb-body { flex: 1; overflow: auto; padding: 0 20px 20px; }
.lb-stage { position: relative; margin: 0 auto; width: 100%; }
.lb-stage img { display: block; width: 100%; height: auto; border-radius: 8px; }
.lb-issues { display: flex; gap: 6px; flex-wrap: wrap; padding: 0 20px 12px; }
.lb-issues button { border: 1px solid #fde047; background: rgba(253,224,71,.12); color: #fef9c3; border-radius: 999px; padding: 4px 10px; font-size: 12.5px; font-weight: 600; cursor: pointer; }
.lb-issues button:hover, .lb-issues button.hl { background: #fde047; color: #111827; }
.hotspot { position: absolute; border: 2px dashed rgba(234,179,8,.95); border-radius: 6px; cursor: pointer; background: rgba(253,224,71,.06); padding: 0; }
.hotspot:hover, .hotspot:focus-visible { border-color: #fde047; background: rgba(253,224,71,.18); outline: none; }
.hotspot span { position: absolute; left: -2px; top: -24px; background: #fde047; color: #111827; font: 700 12px/1 ui-monospace, Menlo, monospace; padding: 5px 6px; border-radius: 5px; white-space: nowrap; opacity: 0; pointer-events: none; }
.hotspot:hover span, .hotspot:focus-visible span { opacity: 1; }
.section-label { font-size: 11.5px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); margin: 18px 0 6px; }
code { font-family: ui-monospace, Menlo, monospace; font-size: .9em; background: var(--nitpick-bg); padding: 1px 5px; border-radius: 4px; }
.where { font-family: ui-monospace, Menlo, monospace; font-size: 12.5px; background: var(--nitpick-bg); padding: 2px 6px; border-radius: 5px; }
.options { display: grid; gap: 8px; }
.option { display: flex; gap: 10px; align-items: flex-start; border: 1px solid var(--line); border-radius: 10px; padding: 10px 12px; }
.option b { margin-right: 6px; }
.option .text { flex: 1; }
.option .effort { font-size: 11.5px; font-weight: 700; color: var(--muted); }
.option input { margin: 3px 0 0; accent-color: var(--accent); }
label.option { cursor: pointer; transition: border-color .15s, background .15s; }
label.option:hover { border-color: #c7d2fe; background: #fafbff; }
label.option:has(input:checked), .option.chosen { border-color: var(--accent); background: var(--accent-soft); box-shadow: inset 0 0 0 1px var(--accent); }
.option.chosen::before { content: "✓"; color: var(--accent); font-weight: 800; }
.pick-tag { font-size: 11px; font-weight: 700; color: var(--accent); margin-left: 6px; }
.decide { display: flex; gap: 8px; flex-wrap: wrap; }
.decide label { display: inline-flex; align-items: center; gap: 6px; border: 1px solid var(--line); border-radius: 999px; padding: 6px 12px; cursor: pointer; font-size: 13.5px; font-weight: 600; }
.decide input { accent-color: var(--accent); }
.decide label:has(input:checked) { border-color: var(--accent); background: var(--accent-soft); color: var(--accent); }
textarea { width: 100%; min-height: 84px; margin-top: 8px; border: 1px solid var(--line); border-radius: 10px; padding: 10px 12px; resize: vertical; }
.result { border-radius: 10px; padding: 10px 12px; background: var(--ok-bg); color: #14532d; font-size: 14px; }
.result.neutral { background: var(--nitpick-bg); color: #334155; }
.proof { width: 100%; border-radius: 10px; border: 1px solid var(--line); margin-top: 8px; }
/* Copy bar */
.copybar { position: fixed; left: 0; right: 0; bottom: 0; z-index: 10; background: #111827; color: #fff; }
.copybar-inner { max-width: 1240px; margin: 0 auto; padding: 12px 24px; display: flex; gap: 12px; align-items: center; }
.copybar .count { margin-right: auto; font-size: 14px; }
.copybar button { border: 0; border-radius: 8px; height: 38px; padding: 0 16px; font-weight: 700; cursor: pointer; }
.copybar .primary { background: #fff; color: #111827; }
.copybar .ghost { background: transparent; color: #cbd5e1; border: 1px solid #374151; }
.toast { position: fixed; bottom: 70px; left: 50%; transform: translateX(-50%); background: #111827; color: #fff; padding: 8px 16px; border-radius: 8px; font-size: 13.5px; opacity: 0; transition: opacity .2s; z-index: 30; pointer-events: none; }
.toast.show { opacity: 1; }
footer { max-width: 1240px; margin: 40px auto 0; padding: 20px 24px 90px; color: var(--muted); font-size: 13px; border-top: 1px solid var(--line); display: flex; gap: 8px; flex-wrap: wrap; justify-content: space-between; }
@media (max-width: 760px) {
  .col-area, .col-status { display: none; }
  .filters input { width: 140px; }
}
</style>
</head>
<body>
<header class="top">
  <div class="top-inner">
    <div class="brand" id="brand"></div>
    <div class="stats" id="stats"></div>
    <div class="filters">
      <select id="f-sev" aria-label="Severity">
        <option value="">All severities</option>
        <option value="critical">Critical</option><option value="major">Major</option>
        <option value="minor">Minor</option><option value="nitpick">Nitpick</option>
      </select>
      <select id="f-status" aria-label="Status">
        <option value="">All statuses</option><option value="open">Open</option><option value="closed">Closed</option>
      </select>
      <input id="f-q" type="search" placeholder="Search issues" aria-label="Search issues">
    </div>
  </div>
</header>

<main>
  <div class="toc-row">
    <nav class="toc" id="toc"></nav>
    <div class="toc-actions"><button id="expand-all">Expand all</button><button id="collapse-all">Collapse all</button></div>
  </div>
  <div id="reviews"></div>
</main>

<footer>
  <span>Made with <a href="__REPO__" target="_blank" rel="noopener">Harsh Design Critic</a> by <b>Suleiman</b>.</span>
  <span><a href="__REPO__/blob/main/LICENSE" target="_blank" rel="noopener">MIT License</a> · © Suleiman</span>
</footer>

<div class="copybar">
  <div class="copybar-inner">
    <span class="count" id="count">No decisions yet. Open an issue to decide.</span>
    <button class="ghost" id="reset">Reset</button>
    <button class="primary" id="copy">Copy decisions</button>
  </div>
</div>

<div class="scrim" id="scrim"></div>
<aside class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer-head">
    <div id="d-kicker"></div>
    <div class="nav">
      <button class="icon-btn" id="prev" aria-label="Previous issue">‹</button>
      <button class="icon-btn" id="next" aria-label="Next issue">›</button>
      <button class="icon-btn" id="close" aria-label="Close">Close</button>
    </div>
  </div>
  <div class="drawer-body" id="d-body"></div>
</aside>
<div class="toast" id="toast"></div>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Screenshot">
  <div class="lb-head"><b id="lb-title"></b><span class="hint" id="lb-hint"></span><div class="seg lb-zoom" role="group" aria-label="Zoom"><button id="lb-fit" class="on" aria-pressed="true">Fit</button><button id="lb-actual" aria-pressed="false">Actual size</button></div><a class="ext" id="lb-ext" target="_blank" rel="noopener">Open image<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6"/><path d="M20 4l-9 9"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg></a><button class="icon-btn" id="lb-close">Close</button></div>
  <div class="lb-issues" id="lb-issues"></div>
  <div class="lb-body" id="lb-body"><div class="lb-stage" id="lb-stage"></div></div>
</div>
<button class="to-top" id="to-top" aria-label="Back to top" title="Back to top">↑</button>

<script type="application/json" id="data">__DATA__</script>
<script>
(() => {
  const DATA = JSON.parse(document.getElementById("data").textContent);
  const CLOSED = ["VERIFIED", "DONE", "WONTFIX", "WITHDRAWN"];
  const SEV_ORDER = { critical: 0, major: 1, minor: 2, nitpick: 3 };
  const STORE = "hdc:" + (DATA.project || "project");
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  // Escaped text with `inline code` rendered as code, for findings and options written in Markdown style.
  const rich = (s) => esc(s).replace(/`([^`]+)`/g, "<code>$1</code>");

  const findings = [];
  DATA.reviews.forEach((r) => r.findings.forEach((f) => findings.push({ ...f, review: r })));
  const isClosed = (f) => CLOSED.includes(String(f.status).toUpperCase());

  let decisions = {};
  try { decisions = JSON.parse(localStorage.getItem(STORE) || "{}"); } catch { decisions = {}; }
  const save = () => { localStorage.setItem(STORE, JSON.stringify(decisions)); renderCount(); };
  const decisionOf = (f) => decisions[f.id] || { choice: "leave", option: f.pick || "", note: "" };
  const decisionLabel = (d) => ({ leave: "Leave it", fix: "Fix" + (d.option ? ` (${d.option})` : ""), wontfix: "Won't fix", question: "Question" }[d.choice]);
  const isSet = (d) => d.choice !== "leave" || (d.note || "").trim();

  // Header
  const open = findings.filter((f) => !isClosed(f));
  $("brand").innerHTML = `${esc(DATA.project || "Design review")}<small>Updated ${esc(DATA.updated || "")} · ${DATA.reviews.length} review${DATA.reviews.length === 1 ? "" : "s"}</small>`;
  const bySev = (s) => open.filter((f) => f.severity === s).length;
  $("stats").innerHTML =
    `<span class="stat"><b>${open.length}</b> open</span>` +
    `<span class="stat"><b>${findings.length - open.length}</b> closed</span>` +
    ["critical", "major", "minor"].filter(bySev).map((s) => `<span class="stat sev-${s}"><b>${bySev(s)}</b> ${s}</span>`).join("");

  // Review sections, oldest first, each behind a divider
  $("toc").innerHTML = DATA.reviews.map((r) =>
    `<a href="#review-${esc(r.id)}">Review #${esc(r.id)} <span>${esc(r.title)}</span></a>`).join("");
  $("reviews").innerHTML = DATA.reviews.map((r) => `
    <div class="divider" id="review-${esc(r.id)}">Review #${esc(r.id)} · ${esc(r.date)}</div>
    <section class="review" data-rid="${esc(r.id)}">
      <button class="review-toggle" aria-expanded="false">
        <span class="mini">${esc(r.score ?? "–")}</span>
        <span><h2>${esc(r.title)}</h2><span class="sub">${esc(r.mode || "")}${r.verdict ? ` · “${esc(r.verdict)}”` : ""}</span></span>
        <span class="counts" data-counts="${esc(r.id)}"></span>
        <span class="chev" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
      </button>
      <div class="review-body">
      <div class="review-head">
        <div class="score">${esc(r.score ?? "–")}<small>/ 10</small></div>
        <div>
          <div class="meta">${esc(r.mode || "")}${r.report_md ? ` · <a href="${esc(r.report_md)}">Markdown report</a>` : ""}</div>
          ${r.verdict ? `<p class="verdict">“${esc(r.verdict)}”</p>` : ""}
          ${r.consumer_take ? `<details class="take"><summary>The consumer's take</summary><p>${esc(r.consumer_take)}</p></details>` : ""}
          ${r.strengths && r.strengths.length ? `<details class="take"><summary>What (barely) works</summary><p>${r.strengths.map(esc).join("<br>")}</p></details>` : ""}
          ${r.coverage ? `<details class="take"><summary>Coverage</summary><p>${esc(r.coverage)}</p></details>` : ""}
          ${r.scorecard ? `<div class="scorecard">${Object.entries(r.scorecard).map(([k, v]) => `<span class="chip">${esc(k)}<b>${esc(v)}</b></span>`).join("")}</div>` : ""}
          ${r.screens && r.screens.length ? `<div class="screens">${r.screens.map((s) => `<button data-screen="${esc(s.image)}"><img src="${esc(s.image)}" alt="" loading="lazy"><span>${esc(s.label)}</span></button>`).join("")}</div>` : ""}
        </div>
      </div>
      <table>
        <thead><tr><th>Issue</th><th>Severity</th><th>Finding</th><th class="col-area">Area</th><th class="col-status">Status</th><th>Your decision</th></tr></thead>
        <tbody data-review="${esc(r.id)}"></tbody>
      </table>
      </div>
    </section>`).join("");

  // Collapse state: every review starts collapsed; the open ones are remembered per browser.
  const OPEN_KEY = STORE + ":open";
  let openReviews = new Set();
  try { openReviews = new Set(JSON.parse(localStorage.getItem(OPEN_KEY) || "[]")); } catch { openReviews = new Set(); }
  function setOpen(rid, isOpen) {
    const sec = document.querySelector(`section.review[data-rid="${CSS.escape(rid)}"]`);
    if (!sec) return;
    sec.classList.toggle("open", isOpen);
    sec.querySelector(".review-toggle").setAttribute("aria-expanded", String(isOpen));
    isOpen ? openReviews.add(rid) : openReviews.delete(rid);
    localStorage.setItem(OPEN_KEY, JSON.stringify([...openReviews]));
  }
  DATA.reviews.forEach((r) => setOpen(r.id, openReviews.has(r.id)));
  document.querySelectorAll(".review-toggle").forEach((b) => b.addEventListener("click", () => {
    const rid = b.closest("section.review").dataset.rid;
    setOpen(rid, !openReviews.has(rid));
  }));
  document.querySelectorAll(".toc a").forEach((a) => a.addEventListener("click", () => setOpen(a.getAttribute("href").replace("#review-", ""), true)));
  $("expand-all").addEventListener("click", () => DATA.reviews.forEach((r) => setOpen(r.id, true)));
  $("collapse-all").addEventListener("click", () => DATA.reviews.forEach((r) => setOpen(r.id, false)));
  const toTop = $("to-top");
  window.addEventListener("scroll", () => toTop.classList.toggle("show", window.scrollY > 400), { passive: true });
  toTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

  function visible(f) {
    const sev = $("f-sev").value, st = $("f-status").value, q = $("f-q").value.trim().toLowerCase();
    if (sev && f.severity !== sev) return false;
    if (st === "open" && isClosed(f)) return false;
    if (st === "closed" && !isClosed(f)) return false;
    if (q && !`${f.id} ${f.title} ${f.finding} ${f.area} ${f.where}`.toLowerCase().includes(q)) return false;
    return true;
  }

  let shown = [];
  function renderTables() {
    shown = [];
    DATA.reviews.forEach((r) => {
      const body = document.querySelector(`tbody[data-review="${CSS.escape(r.id)}"]`);
      const rows = r.findings.map((f) => findings.find((x) => x.id === f.id))
        .filter(visible).sort((a, b) => SEV_ORDER[a.severity] - SEV_ORDER[b.severity] || (a.q || 0) - (b.q || 0));
      shown.push(...rows);
      const all = r.findings.map((f) => findings.find((x) => x.id === f.id));
      const openN = all.filter((f) => !isClosed(f)).length;
      const filtered = rows.length !== all.length ? `<span class="stat"><b>${rows.length}</b> shown</span>` : "";
      document.querySelector(`[data-counts="${CSS.escape(r.id)}"]`).innerHTML =
        `<span class="stat"><b>${openN}</b> open</span><span class="stat"><b>${all.length - openN}</b> closed</span>` + filtered;
      body.innerHTML = rows.length ? rows.map((f) => {
        const d = decisionOf(f);
        return `<tr class="issue${isClosed(f) ? " closed" : ""}" data-id="${esc(f.id)}" tabindex="0">
          <td class="id">${esc(f.id)}${f.q ? `<br><span class="meta">Q${esc(f.q)}</span>` : ""}</td>
          <td><span class="sev sev-${esc(f.severity)}">${esc(f.severity)}</span></td>
          <td class="title-cell"><b>${rich(f.title)}</b><span>${rich(f.finding)}</span></td>
          <td class="col-area">${esc(f.area || "")}</td>
          <td class="col-status"><span class="status${isClosed(f) ? " closed" : ""}">${esc(f.status)}</span></td>
          <td>${isClosed(f) ? `<span class="decision">—</span>` : `<span class="decision${isSet(d) ? " set" : ""}">${esc(decisionLabel(d))}${(d.note || "").trim() ? " · note" : ""}</span>`}</td>
        </tr>`;
      }).join("") : `<tr><td colspan="6" class="empty">No issues match the filters.</td></tr>`;
    });
    document.querySelectorAll("tr.issue").forEach((tr) => {
      tr.addEventListener("click", () => openIssue(tr.dataset.id));
      tr.addEventListener("keydown", (e) => { if (e.key === "Enter") openIssue(tr.dataset.id); });
    });
  }

  // Image viewer: zoom to the issue's box, or show the whole annotated screen.
  // `screenSrc`: the full annotated screen to open in the viewer (differs from `src` for crops).
  function viewer(src, box, full, screenSrc) {
    if (!src) return "";
    return `<div class="viewer-wrap"><div class="img-actions"><a class="img-open" href="${esc(screenSrc || src)}" data-lightbox="${esc(screenSrc || src)}" title="View ${screenSrc && screenSrc !== src ? "full screen" : "image"} (click the marked issues)" aria-label="View image"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg></a><a class="img-open" href="${esc(src)}" target="_blank" rel="noopener" title="Open image in a new tab" aria-label="Open image in a new tab"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6"/><path d="M20 4l-9 9"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg></a></div><div class="viewer${full ? " full" : ""}" id="viewer"><img src="${esc(src)}" alt="Annotated screenshot" id="v-img">${box && !full ? `<div class="mark" id="v-mark"></div>` : ""}</div></div>
      <div class="viewer-bar">${box ? `<div class="seg" role="group" aria-label="Image view"><button id="v-zoom" aria-pressed="${!full}"${!full ? ' class="on"' : ""}><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3M11 8v6M8 11h6"/></svg>Issue</button><button id="v-full" aria-pressed="${full}"${full ? ' class="on"' : ""}><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/></svg>Whole screen</button></div>` : ""}</div>`;
  }
  function fitViewer(box) {
    const v = $("viewer"), img = $("v-img");
    if (!v || !img || v.classList.contains("full")) return;
    const place = () => {
      const W = v.clientWidth, H = v.clientHeight, iw = img.naturalWidth, ih = img.naturalHeight;
      if (!box) { const s = Math.min(W / iw, H / ih); img.style.transform = `translate(${(W - iw * s) / 2}px, ${(H - ih * s) / 2}px) scale(${s})`; return; }
      const [x1, y1, x2, y2] = box, pad = 60;
      const s = Math.min(W / (x2 - x1 + pad * 2), H / (y2 - y1 + pad * 2), 2.5);
      const tx = W / 2 - ((x1 + x2) / 2) * s, ty = H / 2 - ((y1 + y2) / 2) * s;
      img.style.transform = `translate(${tx}px, ${ty}px) scale(${s})`;
      const m = $("v-mark");
      if (m) Object.assign(m.style, { left: `${tx + x1 * s - 4}px`, top: `${ty + y1 * s - 4}px`, width: `${(x2 - x1) * s + 8}px`, height: `${(y2 - y1) * s + 8}px` });
    };
    img.complete ? place() : img.addEventListener("load", place, { once: true });
  }

  let current = null, fullView = false;
  function openIssue(id, keepView) {
    const f = findings.find((x) => x.id === id);
    if (!f) return;
    current = f;
    if (!keepView) fullView = false;
    // Bring the issue's row into view behind the panel: expand its review, then center the row.
    setOpen(f.review.id, true);
    document.querySelectorAll("tr.issue").forEach((tr) => tr.classList.toggle("active", tr.dataset.id === id));
    const row = document.querySelector(`tr.issue[data-id="${CSS.escape(id)}"]`);
    if (row && !keepView) row.scrollIntoView({ block: "center", behavior: "smooth" });
    const d = decisionOf(f);
    $("d-kicker").innerHTML = `<span class="sev sev-${esc(f.severity)}">${esc(f.severity)}</span> <span class="id">${esc(f.id)}</span> <span class="meta">· Review #${esc(f.review.id)}${f.q ? ` · Q${esc(f.q)}` : ""} · ${esc(f.status)}</span>`;
    // Open issues: each option card is a radio; choosing one means "Fix it" with that option.
    // Closed issues: read-only cards, the applied option marked.
    const optBody = (o) => `<span class="text"><b>(${esc(o.key)})</b>${rich(o.text)}${o.key === f.pick ? `<span class="pick-tag">MY PICK</span>` : ""}</span>${o.effort ? `<span class="effort">${esc(o.effort)}</span>` : ""}`;
    const opts = (f.options || []).map((o) => isClosed(f)
      ? `<div class="option${o.key === f.chosen ? " chosen" : ""}">${optBody(o)}</div>`
      : `<label class="option"><input type="radio" name="opt" value="${esc(o.key)}"${d.choice === "fix" && (d.option || f.pick) === o.key ? " checked" : ""}>${optBody(o)}</label>`).join("");
    const closedBlock = isClosed(f) ? `
      <div class="section-label">Result</div>
      <div class="result${["WONTFIX", "WITHDRAWN"].includes(String(f.status).toUpperCase()) ? " neutral" : ""}">${esc(f.status)}${f.chosen ? ` · option (${esc(f.chosen)})` : ""}${f.result ? ` — ${esc(f.result)}` : ""}</div>
      ${f.proof ? `<img class="proof" src="${esc(f.proof)}" alt="Before and after proof">` : ""}` : "";
    const decideBlock = isClosed(f) ? "" : `
      <div class="section-label">Your decision</div>
      <div class="decide" id="decide">
        ${["leave", "fix", "wontfix", "question"].map((c) => `<label><input type="radio" name="choice" value="${c}"${d.choice === c ? " checked" : ""}>${{ leave: "Leave it", fix: "Fix it", wontfix: "Won't fix", question: "Ask a question" }[c]}</label>`).join("")}
      </div>
      <textarea id="note" placeholder="Note or question for this issue (optional)">${esc(d.note || "")}</textarea>`;
    $("d-body").innerHTML = `
      ${viewer(f.image, f.box, fullView, f.screen && f.screen.image)}
      ${(f.also || []).length ? `<div class="viewer-bar">See also ${f.also.map((a) => `<a class="bar-btn" href="${esc(a.image)}" data-lightbox="${esc(a.image)}" data-label="${esc(a.label || "")}">${esc(a.label || "image")}</a>`).join("")}</div>` : ""}
      <h3 class="issue-title" id="d-title">${rich(f.title)}</h3>
      <div class="section-label">Problem</div>
      <div>${rich(f.finding)}</div>
      ${f.where ? `<div class="section-label">Where</div><span class="where">${esc(f.where)}</span>` : ""}
      ${opts ? `<div class="section-label">Options${isClosed(f) ? "" : ` <span class="meta" style="text-transform:none;letter-spacing:0;font-weight:500">· pick one to fix it that way</span>`}</div><div class="options" id="options">${opts}</div>` : ""}
      ${f.pick_reason ? `<p class="meta">My pick (${esc(f.pick)}): ${rich(f.pick_reason)}</p>` : ""}
      ${closedBlock}${decideBlock}`;
    fitViewer(f.box);
    const setView = (full) => { if (fullView !== full) { fullView = full; openIssue(f.id, true); } };
    $("v-zoom") && $("v-zoom").addEventListener("click", () => setView(false));
    $("v-full") && $("v-full").addEventListener("click", () => setView(true));
    if (!isClosed(f)) {
      const optRadios = () => [...document.querySelectorAll('input[name="opt"]')];
      const update = () => {
        const choice = document.querySelector('input[name="choice"]:checked').value;
        const picked = optRadios().find((r) => r.checked);
        decisions[f.id] = { choice, option: choice === "fix" ? (picked ? picked.value : f.pick || "") : "", note: $("note").value };
        if (!isSet(decisions[f.id])) delete decisions[f.id];
        save(); renderTables();
        document.querySelectorAll("tr.issue").forEach((tr) => tr.classList.toggle("active", tr.dataset.id === f.id));
      };
      $("decide").addEventListener("change", () => {
        const choice = document.querySelector('input[name="choice"]:checked').value;
        if (choice !== "fix") optRadios().forEach((r) => (r.checked = false));
        else if (!optRadios().some((r) => r.checked)) { const p = optRadios().find((r) => r.value === f.pick) || optRadios()[0]; if (p) p.checked = true; }
        update();
      });
      $("options") && $("options").addEventListener("change", () => {
        document.querySelector('input[name="choice"][value="fix"]').checked = true;
        update();
      });
      $("note").addEventListener("input", update);
    }
    $("drawer").classList.add("open"); $("scrim").classList.add("open"); $("drawer").setAttribute("aria-hidden", "false");
    // Keep the open issue in the URL so a refresh (or a shared link) reopens it.
    history.replaceState(null, "", `#issue=${encodeURIComponent(f.id)}`);
  }
  function closeDrawer() {
    $("drawer").classList.remove("open"); $("scrim").classList.remove("open"); $("drawer").setAttribute("aria-hidden", "true");
    document.querySelectorAll("tr.issue.active").forEach((tr) => tr.classList.remove("active"));
    current = null;
    if (location.hash.startsWith("#issue=")) history.replaceState(null, "", location.pathname + location.search);
  }
  function step(dir) {
    if (!current) return;
    const i = shown.findIndex((f) => f.id === current.id);
    const next = shown[(i + dir + shown.length) % shown.length];
    if (next) openIssue(next.id);
  }
  $("close").addEventListener("click", closeDrawer);
  $("scrim").addEventListener("click", closeDrawer);
  $("prev").addEventListener("click", () => step(-1));
  $("next").addEventListener("click", () => step(1));
  document.addEventListener("keydown", (e) => {
    if (!current || ["TEXTAREA", "SELECT", "INPUT"].includes(document.activeElement.tagName)) return;
    if (e.key === "Escape") closeDrawer();
    if (e.key === "ArrowRight") step(1);
    if (e.key === "ArrowLeft") step(-1);
  });
  window.addEventListener("resize", () => current && fitViewer(current.box));

  // Screen thumbnails open the whole annotated screen in a new tab.
  document.querySelectorAll("[data-screen]").forEach((b) => b.addEventListener("click", () => openLightbox(b.dataset.screen, b.querySelector("span").textContent)));

  // Lightbox: the whole image with a clickable box for every issue marked on it.
  function openLightbox(src, label) {
    // An issue is clickable on this image when it is marked on it: its own image + box,
    // or (per-issue crops) the full screen it was cropped from.
    const spotBox = (f) => (f.image === src && f.box) ? f.box : (f.screen && f.screen.image === src ? f.screen.box : null);
    const spots = findings.filter(spotBox);
    $("lb-title").textContent = label || src.split("/").pop();
    $("lb-hint").textContent = spots.length ? `${spots.length} issue${spots.length === 1 ? "" : "s"} marked · click a dashed box or a name below` : "No issues are linked to boxes on this image";
    $("lb-issues").innerHTML = spots.map((f) => `<button data-id="${esc(f.id)}">${esc(f.id)} · ${esc(f.title)}</button>`).join("");
    $("lb-issues").querySelectorAll("button").forEach((b) => {
      b.addEventListener("click", () => { closeLightbox(); openIssue(b.dataset.id); });
      const spot = () => $("lb-stage").querySelector(`.hotspot[data-id="${CSS.escape(b.dataset.id)}"]`);
      b.addEventListener("mouseenter", () => { const h = spot(); if (h) { h.focus({ preventScroll: true }); h.scrollIntoView({ block: "nearest", inline: "nearest" }); } });
      b.addEventListener("mouseleave", () => { const h = spot(); if (h) h.blur(); });
    });
    $("lb-ext").href = src;
    $("lb-stage").innerHTML = `<img src="${esc(src)}" alt="${esc(label || "Screenshot")}" id="lb-img">` +
      spots.map((f) => `<button class="hotspot" data-id="${esc(f.id)}" title="${esc(f.id)} · ${esc(f.title)}"><span>${esc(f.id)} · ${esc(f.title)}</span></button>`).join("");
    const img = $("lb-img");
    const place = () => {
      const iw = img.naturalWidth, ih = img.naturalHeight, body = $("lb-body");
      // Fit: the whole image inside the window (width and height). Actual size: 1:1, scroll.
      const fitW = Math.min(iw, body.clientWidth - 40, (body.clientHeight - 20) * iw / ih);
      $("lb-stage").style.maxWidth = `${lbActual ? iw : Math.max(200, fitW)}px`;
      const s = img.clientWidth / iw;
      $("lb-stage").querySelectorAll(".hotspot").forEach((h) => {
        const [x1, y1, x2, y2] = spotBox(findings.find((f) => f.id === h.dataset.id));
        Object.assign(h.style, { left: `${x1 * s - 4}px`, top: `${y1 * s - 4}px`, width: `${(x2 - x1) * s + 8}px`, height: `${(y2 - y1) * s + 8}px` });
      });
    };
    $("lb-stage").querySelectorAll(".hotspot").forEach((h) => h.addEventListener("click", () => { closeLightbox(); openIssue(h.dataset.id); }));
    // Show the viewer first: placing boxes while it is hidden measures a 0px image
    // (always the case for an image already in the cache) and stacks them in a corner.
    $("lightbox").classList.add("open");
    $("lb-body").scrollTop = 0;
    lbActual = false; $("lb-fit").classList.add("on"); $("lb-actual").classList.remove("on");
    img.complete && img.naturalWidth ? requestAnimationFrame(place) : img.addEventListener("load", place, { once: true });
    window.__lbPlace = place;
  }
  let lbActual = false;
  const setZoom = (actual) => {
    lbActual = actual;
    $("lb-fit").classList.toggle("on", !actual); $("lb-fit").setAttribute("aria-pressed", String(!actual));
    $("lb-actual").classList.toggle("on", actual); $("lb-actual").setAttribute("aria-pressed", String(actual));
    window.__lbPlace && window.__lbPlace();
  };
  $("lb-fit").addEventListener("click", () => setZoom(false));
  $("lb-actual").addEventListener("click", () => setZoom(true));
  function closeLightbox() { $("lightbox").classList.remove("open"); window.__lbPlace = null; }
  $("lb-close").addEventListener("click", closeLightbox);
  $("lightbox").addEventListener("click", (e) => { if (e.target.classList.contains("lb-body")) closeLightbox(); });
  window.addEventListener("resize", () => window.__lbPlace && window.__lbPlace());
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && $("lightbox").classList.contains("open")) { e.stopImmediatePropagation(); closeLightbox(); } }, true);
  document.addEventListener("click", (e) => {
    const a = e.target.closest("[data-lightbox]");
    if (!a) return;
    e.preventDefault();
    openLightbox(a.dataset.lightbox, a.dataset.label || (current ? `${current.id} · ${current.title}` : ""));
  });

  // Copy: lines the skill already understands ("fix DT-012 c", "won't fix DT-019 because ...").
  function exportText() {
    const lines = [];
    findings.filter((f) => !isClosed(f) && decisions[f.id]).forEach((f) => {
      const d = decisionOf(f), note = (d.note || "").trim();
      const where = `${f.q ? `Q${f.q}, ` : ""}review #${f.review.id}: ${f.title}`;
      if (d.choice === "fix") {
        const key = d.option || f.pick || "";
        const opt = (f.options || []).find((o) => o.key === key);
        lines.push(`fix ${f.id} ${key}`.trim() + (opt ? ` (option ${key}: ${opt.text})` : "") + ` — ${where}` + (note ? ` — note: ${note}` : ""));
      }
      else if (d.choice === "wontfix") lines.push(`won't fix ${f.id} because ${note || "(no reason given)"} — ${where}`);
      else if (d.choice === "question") lines.push(`question ${f.id} — ${where} — ${note || "(write your question)"}`);
      else if (note) lines.push(`note ${f.id} — ${where} — ${note}`);
    });
    return lines.length
      ? `Design review decisions — ${DATA.project || ""}\n` + lines.map((l, i) => `${i + 1}. ${l}`).join("\n")
      : "";
  }
  function renderCount() {
    const ds = findings.filter((f) => !isClosed(f) && decisions[f.id]).map(decisionOf);
    const fix = ds.filter((d) => d.choice === "fix").length, other = ds.length - fix;
    $("count").textContent = ds.length ? `${fix} to fix · ${other} other decision${other === 1 ? "" : "s"} or note${other === 1 ? "" : "s"}` : "No decisions yet. Open an issue to decide.";
  }
  function toast(msg) { const t = $("toast"); t.textContent = msg; t.classList.add("show"); setTimeout(() => t.classList.remove("show"), 1800); }
  $("copy").addEventListener("click", async () => {
    const text = exportText();
    if (!text) return toast("Nothing to copy yet");
    try { await navigator.clipboard.writeText(text); }
    catch { const ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta); ta.select(); document.execCommand("copy"); ta.remove(); }
    toast("Copied — paste it to Claude");
  });
  $("reset").addEventListener("click", () => {
    if (!Object.keys(decisions).length || !confirm("Clear every decision and note on this page?")) return;
    decisions = {}; save(); renderTables(); if (current) openIssue(current.id, true);
  });

  ["f-sev", "f-status", "f-q"].forEach((id) => $(id).addEventListener("input", renderTables));
  renderTables(); renderCount();
  const fromUrl = () => {
    const m = location.hash.match(/^#issue=(.+)$/);
    if (m && findings.some((f) => f.id === decodeURIComponent(m[1]))) openIssue(decodeURIComponent(m[1]));
  };
  fromUrl();
  window.addEventListener("hashchange", fromUrl);
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
