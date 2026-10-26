#!/usr/bin/env python3
"""UI lint for Godot (.tscn/.gd) and React Native / web (.tsx/.jsx/.ts/.js) projects.

Catches the defect classes the harsh-design-critic keeps finding, before a build:
  E-EMOJI     OS emoji used in UI text (renders differently per device, can't be themed)
  E-SIBLING   siblings in the same row/container with mismatched heights
  W-TOKENS    sizes / radii / colors that are not in the project's ui-tokens.json
  W-SPRAWL    too many distinct font sizes, corner radii or colors (no system)
  I-OVERFLOW  Godot labels with no wrap / overrun / clip handling (clipping risk)
  I-WORLD     Godot Label3D / floating labels: verify on-screen clamping and overlap

Usage:
  python ui_lint.py <project_root> [--tokens docs/harsh-design-critic/design-review/ui-tokens.json]
                    [--out docs/harsh-design-critic/design-review/lint-report.md] [--strict]

Exit code 1 if any E-* finding (or any finding with --strict), so it can gate builds.
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict

EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U00002B00-\U00002BFF\U0001F900-\U0001F9FF️]"
)
SKIP_DIRS = {".git", "node_modules", ".godot", ".import", "build", "dist", "android", "ios",
             ".expo", "addons", "Pods", "vendor", ".next"}
CODE_EXT = (".tsx", ".jsx", ".ts", ".js")

findings = []


def add(code, path, line, msg):
    findings.append((code, path, line, msg))


def walk(root):
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            yield os.path.join(dp, fn)


# ---------------- Godot ----------------
NODE_RE = re.compile(r'^\[node name="([^"]+)" type="([^"]+)"(?: parent="([^"]*)")?')
PROP_RE = re.compile(r"^([\w/]+)\s*=\s*(.+)$")


def parse_tscn(path):
    nodes, cur, subres = [], None, []
    in_sub = None
    for i, raw in enumerate(open(path, encoding="utf-8", errors="ignore"), 1):
        line = raw.strip()
        m = NODE_RE.match(line)
        if m:
            cur = {"name": m.group(1), "type": m.group(2), "parent": m.group(3), "line": i, "props": {}}
            nodes.append(cur)
            in_sub = None
            continue
        if line.startswith("[sub_resource"):
            in_sub = {"line": i, "props": {}, "head": line}
            subres.append(in_sub)
            cur = None
            continue
        if line.startswith("["):
            cur, in_sub = None, None
            continue
        pm = PROP_RE.match(line)
        if pm:
            target = cur if cur else in_sub
            if target is not None:
                target["props"][pm.group(1)] = (pm.group(2), i)
    return nodes, subres


def node_path(n):
    if n["parent"] is None:
        return "."
    return n["name"] if n["parent"] == "." else n["parent"] + "/" + n["name"]


def vec_y(v):
    m = re.match(r"Vector2i?\(([-\d.]+),\s*([-\d.]+)\)", v)
    return float(m.group(2)) if m else None


def lint_godot_scene(path, tokens, stats):
    nodes, subres = parse_tscn(path)
    by_path = {node_path(n): n for n in nodes}
    children = defaultdict(list)
    for n in nodes:
        if n["parent"] is not None:
            children[n["parent"]].append(n)

    for n in nodes:
        for key in ("text", "tooltip_text", "placeholder_text"):
            if key in n["props"]:
                val, ln = n["props"][key]
                if EMOJI.search(val):
                    add("E-EMOJI", path, ln, f'{n["type"]} "{n["name"]}" uses emoji in {key}: {val[:40]} '
                        "-> replace with an icon from the project's icon set")
        if n["type"] == "Label" and "text" in n["props"]:
            p = n["props"]
            if not any(k in p for k in ("autowrap_mode", "text_overrun_behavior", "clip_text", "fit_content")):
                txt = p["text"][0]
                if len(txt) > 14:
                    add("I-OVERFLOW", path, n["line"], f'Label "{n["name"]}" has no wrap/overrun/clip; '
                        "longer translations (Arabic/Hebrew) may clip or overflow")
        if n["type"] == "Label3D":
            add("I-WORLD", path, n["line"], f'Label3D "{n["name"]}": verify it never overlaps transient '
                "messages and stays readable near screen edges")
        fs = n["props"].get("theme_override_font_sizes/font_size")
        if fs:
            stats["font_sizes"][fs[0]].append(f"{path}:{fs[1]}")

    # sibling height mismatch in row containers
    for parent, kids in children.items():
        pnode = by_path.get(parent) if parent != "." else next((n for n in nodes if n["parent"] is None), None)
        ptype = pnode["type"] if pnode else ""
        if ptype not in ("HBoxContainer", "HFlowContainer", "GridContainer"):
            continue
        hs = [(k, vec_y(k["props"]["custom_minimum_size"][0])) for k in kids if "custom_minimum_size" in k["props"]]
        hs = [(k, h) for k, h in hs if h]
        if len(hs) >= 2 and max(h for _, h in hs) - min(h for _, h in hs) > 4:
            desc = ", ".join(f'{k["name"]}={int(h)}' for k, h in hs)
            add("E-SIBLING", path, hs[0][0]["line"], f'Row "{parent}" children have mismatched heights ({desc}) '
                "-> use one height token for the whole row")

    for s in subres:
        for k, (v, ln) in s["props"].items():
            if k.startswith("corner_radius"):
                stats["radii"][v].append(f"{path}:{ln}")
            if k in ("bg_color", "border_color", "font_color"):
                m = re.match(r"Color\(([\d.]+),\s*([\d.]+),\s*([\d.]+)", v)
                if m:  # Godot Color(0..1) -> #RRGGBB so it can match ui-tokens.json
                    v = "#%02X%02X%02X" % tuple(round(float(c) * 255) for c in m.groups())
                stats["colors"][v].append(f"{path}:{ln}")


def lint_gd(path):
    for i, line in enumerate(open(path, encoding="utf-8", errors="ignore"), 1):
        if ".text" in line and EMOJI.search(line):
            add("E-EMOJI", path, i, f"emoji assigned to UI text: {line.strip()[:60]}")


# ---------------- React Native / web ----------------
JSX_TEXT = re.compile(r">([^<>{}]*)<")
STR_LIT = re.compile(r"(['\"`])((?:\\.|(?!\1).)*)\1")
STYLE_NUM = re.compile(r"\b(fontSize|borderRadius|height|minHeight)\s*:\s*(\d+(?:\.\d+)?)")
HEX = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")


def lint_code(path, stats):
    text = open(path, encoding="utf-8", errors="ignore").read()
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith(("//", "*", "import ")):
            continue
        for seg in JSX_TEXT.findall(line) + [m.group(2) for m in STR_LIT.finditer(line)]:
            if EMOJI.search(seg):
                add("E-EMOJI", path, i, f'emoji in UI string: "{seg.strip()[:40]}" -> use an icon component')
                break
        for k, v in STYLE_NUM.findall(line):
            key = {"fontSize": "font_sizes", "borderRadius": "radii"}.get(k)
            if key:
                stats[key][v].append(f"{path}:{i}")
        for h in HEX.findall(line):
            stats["colors"][h.upper()].append(f"{path}:{i}")


# ---------------- report ----------------
def check_tokens(stats, tokens):
    mapping = {"font_sizes": "fontSizes", "radii": "radii", "colors": "colors"}
    for key, tkey in mapping.items():
        allowed = {str(v).upper() for v in tokens.get(tkey, [])}
        if not allowed:
            continue
        for val, locs in stats[key].items():
            if str(val).upper().strip('"') not in allowed:
                add("W-TOKENS", locs[0], "", f"{tkey[:-1]} {val} not in ui-tokens.json (used {len(locs)}x)")


def check_sprawl(stats):
    limits = {"font_sizes": 6, "radii": 4, "colors": 14}
    for key, lim in limits.items():
        n = len(stats[key])
        if n > lim:
            vals = sorted(stats[key], key=lambda v: -len(stats[key][v]))[:12]
            add("W-SPRAWL", "(project)", "", f"{n} distinct {key.replace('_', ' ')} (limit {lim}): "
                + ", ".join(vals) + " -> consolidate into tokens")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--tokens", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()

    tok_path = a.tokens or os.path.join(a.root, "docs/harsh-design-critic/design-review/ui-tokens.json")
    if not a.tokens and not os.path.exists(tok_path):
        tok_path = os.path.join(a.root, "docs/game-prompts/design-review/ui-tokens.json")  # pre-1.1 location
    tokens = json.load(open(tok_path)) if os.path.exists(tok_path) else {}
    stats = {"font_sizes": defaultdict(list), "radii": defaultdict(list), "colors": defaultdict(list)}

    for p in walk(a.root):
        if p.endswith(".tscn"):
            lint_godot_scene(p, tokens, stats)
        elif p.endswith(".gd"):
            lint_gd(p)
        elif p.endswith(CODE_EXT) and "/test" not in p:
            lint_code(p, stats)

    if tokens:
        check_tokens(stats, tokens)
    check_sprawl(stats)

    order = {"E": 0, "W": 1, "I": 2}
    findings.sort(key=lambda f: (order[f[0][0]], f[0], f[1]))
    lines = ["# UI lint report", "",
             f"Errors: {sum(f[0][0] == 'E' for f in findings)} · Warnings: {sum(f[0][0] == 'W' for f in findings)}"
             f" · Info: {sum(f[0][0] == 'I' for f in findings)}"
             + ("" if tokens else " · (no ui-tokens.json found: token checks skipped)"), ""]
    for code, path, line, msg in findings:
        rel = os.path.relpath(path, a.root) if os.path.exists(path) else path
        lines.append(f"- **{code}** `{rel}{':' + str(line) if line else ''}` — {msg}")
    report = "\n".join(lines) + "\n"
    if a.out:
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        open(a.out, "w").write(report)
    print(report)
    bad = any(f[0][0] == "E" for f in findings) or (a.strict and findings)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
