#!/usr/bin/env python3
"""Capture a web page at several widths and states, and dump every visible element's box and styles.

One command replaces hand-written browser scripts: full-page screenshots plus a JSON file with
boxes, font sizes, colors, radii, padding and the WCAG contrast of each text element, so findings
can be measured instead of eyeballed. Uses the installed Google Chrome / Chromium in headless mode.

Usage:
  python web_capture.py <page.html | http(s)://url> --out <dir> [--name home]
                        [--widths 1440,390] [--height 900] [--states states.json] [--no-full-page]

states.json (optional, each state is captured at every width; "default" is always captured):
[
  {"name": "invalid-email", "js": "const e=document.querySelector('#email'); e.value='abc'; e.dispatchEvent(new Event('blur'))"},
  {"name": "cta-hover", "pseudo": ["hover", ".place"]},        # applies the page's own :hover rules
  {"name": "swatch-focus", "pseudo": ["focus-visible", ".swatch"]},
  {"name": "qty-minus", "click": ["#minus", "#minus", "#minus"]}
]

Output in <dir>: <name>_<width>[_<state>].png and .json, plus <name>_index.json.
The JSON lists only elements visible in that state (closed tabs and hidden panels are absent: add a state).
Widths under 500px work too: headless Chrome won't open a window that narrow, so the page is
rendered inside a same-origin frame of the exact width.

Limits: pages that need their own origin (logins, API calls blocked by CORS) may render
incompletely from a URL; capture a running local build instead. With full-page capture the
viewport height equals the page height, so 100vh sections grow; use --no-full-page to check them.
"""
import argparse
import html
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.request

from PIL import Image

CHROME_CANDIDATES = [
    os.environ.get("CHROME", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
]
MIN_WINDOW = 500
NATIVE = []

# Runs inside the page: apply the state, then (measure pass only) write element data to the parent.
PAGE_JS = r"""
(function () {
  const STATE = __STATE__, MEASURE = __MEASURE__;
  function applyPseudo(kind, sel) {
    const cls = '__hdc-' + kind;
    for (const sheet of document.styleSheets) {
      let rules; try { rules = sheet.cssRules; } catch (e) { continue; }
      for (const r of Array.from(rules || [])) {
        if (r.selectorText && r.selectorText.includes(':' + kind)) {
          const s = r.selectorText.split(':' + kind).join('.' + cls);
          try { sheet.insertRule(s + '{' + r.style.cssText + '}', sheet.cssRules.length); } catch (e) {}
        }
      }
    }
    document.querySelectorAll(sel).forEach(el => el.classList.add(cls));
  }
  function parse(c) {
    const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number);
    return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1];
  }
  function hex(c) { return c ? '#' + c.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase() : null; }
  function lum(c) { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
                    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); }
  function over(top, base) { const a = top[3]; return [0, 1, 2].map(i => top[i] * a + base[i] * (1 - a)).concat([1]); }
  function backdrop(el) {
    const layers = []; let uncertain = false;
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') uncertain = true;
      const c = parse(cs.backgroundColor);
      if (c && c[3] > 0) { layers.push(c); if (c[3] >= 1) break; }
    }
    let bg = [255, 255, 255, 1];
    for (const l of layers.reverse()) bg = over(l, bg);
    return [bg, uncertain];
  }
  function directText(el) {
    let t = ''; for (const n of el.childNodes) if (n.nodeType === 3) t += n.textContent;
    return t.replace(/\s+/g, ' ').trim();
  }
  function measure() {
    const out = [], INTERACTIVE = /^(A|BUTTON|INPUT|SELECT|TEXTAREA|LABEL|IMG|SVG|VIDEO|CANVAS|H[1-6])$/;
    for (const el of document.body.querySelectorAll('*')) {
      if (out.length >= 800 || el.closest('svg') && el.tagName.toUpperCase() !== 'SVG') continue;
      const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
      if (r.width < 1 || r.height < 1 || cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) continue;
      const text = directText(el), bgc = parse(cs.backgroundColor);
      const boxed = (bgc && bgc[3] > 0) || parseFloat(cs.borderTopWidth) > 0 || parseFloat(cs.borderRadius) > 0;
      if (!text && !boxed && !INTERACTIVE.test(el.tagName.toUpperCase())) continue;
      const item = {
        tag: el.tagName.toLowerCase(), id: el.id || undefined,
        cls: (typeof el.className === 'string' && el.className.trim()) || undefined,
        text: text ? text.slice(0, 60) : undefined,
        box: [r.left + scrollX, r.top + scrollY, r.width, r.height].map(v => Math.round(v * 10) / 10),
        font: text ? [cs.fontSize, cs.fontWeight, cs.lineHeight, cs.fontFamily.split(',')[0].replace(/"/g, '')].join(' / ') : undefined,
        color: text ? hex(parse(cs.color)) : undefined,
        bg: bgc && bgc[3] > 0 ? hex(bgc) : undefined,
        border: parseFloat(cs.borderTopWidth) > 0 ? cs.borderTopWidth + ' ' + hex(parse(cs.borderTopColor)) : undefined,
        radius: parseFloat(cs.borderRadius) > 0 ? cs.borderRadius : undefined,
        padding: cs.padding !== '0px' ? cs.padding : undefined,
        opacity: +cs.opacity < 1 ? +cs.opacity : undefined,
        outline: cs.outlineStyle !== 'none' ? cs.outline : undefined,
        disabled: el.disabled || undefined,
      };
      if (text) {
        const fg = parse(cs.color), [bg, uncertain] = backdrop(el);
        if (fg) {
          const f = over(fg, bg), L1 = lum(f), L2 = lum(bg);
          item.contrast = Math.round((Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05) * 100) / 100;
          item.on = hex(bg) + (uncertain ? ' (over image/gradient: verify)' : '');
        }
      }
      out.push(JSON.parse(JSON.stringify(item)));
    }
    const d = document.documentElement;
    return { viewport: [innerWidth, innerHeight], page: [d.scrollWidth, d.scrollHeight],
             horizontal_overflow: d.scrollWidth > innerWidth, elements: out };
  }
  function run() {
    try {
      if (STATE.pseudo) applyPseudo(STATE.pseudo[0], STATE.pseudo[1]);
      for (const sel of STATE.click || []) { const el = document.querySelector(sel); if (el) el.click(); }
      if (STATE.js) (new Function(STATE.js))();
    } catch (e) { console.error('state failed', e); }
    if (MEASURE) setTimeout(() => {
      const box = parent.document.getElementById('__hdc_out');
      box.textContent = JSON.stringify(measure());
    }, 400);
  }
  if (document.readyState === 'complete') setTimeout(run, 50); else addEventListener('load', () => setTimeout(run, 50));
})();
"""


def find_chrome():
    for c in CHROME_CANDIDATES:
        if c and os.path.exists(c):
            return c
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        p = shutil.which(name)
        if p:
            return p
    sys.exit("Chrome/Chromium not found. Install it or set CHROME=/path/to/chrome")


def load_page(src):
    if src.startswith(("http://", "https://")):
        with urllib.request.urlopen(src) as r:
            return r.read().decode("utf-8", "replace"), src
    path = os.path.abspath(src)
    return open(path, encoding="utf-8", errors="replace").read(), "file://" + path


def build_wrapper(page_html, base_url, state, measure, width, height):
    script = PAGE_JS.replace("__STATE__", json.dumps(state)).replace("__MEASURE__", "true" if measure else "false")
    inject = f'<base href="{html.escape(base_url)}"><script>{script}</script>'
    low = page_html.lower()
    i = low.find("<head")
    if i >= 0:
        j = page_html.find(">", i) + 1
        page_html = page_html[:j] + inject + page_html[j:]
    else:
        page_html = inject + page_html
    return ("<!DOCTYPE html><html><head><style>html,body{margin:0;padding:0;overflow:hidden}"
            "iframe{border:0;display:block}</style></head><body>"
            f'<iframe width="{width}" height="{height}" srcdoc="{html.escape(page_html, quote=True)}"></iframe>'
            '<pre id="__hdc_out" style="display:none"></pre></body></html>')


def native_prefix():
    # An Intel Python under Rosetta would start Chrome translated too: about 6-10x slower per launch
    if sys.platform == "darwin" and platform.machine() == "x86_64":
        r = subprocess.run(["sysctl", "-n", "sysctl.proc_translated"], capture_output=True, text=True)
        if r.stdout.strip() == "1":
            return ["arch", "-arm64"]
    return []


def chrome(binary, args):
    base = NATIVE + [binary, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
            "--allow-file-access-from-files", "--virtual-time-budget=1500", "--no-first-run", "--no-default-browser-check"]
    return subprocess.run(base + args, capture_output=True, text=True, timeout=120)


def capture(binary, page_html, base_url, state, width, height, full_page, out_png, out_json, tmp):
    wrap = os.path.join(tmp, "measure.html")
    open(wrap, "w", encoding="utf-8").write(build_wrapper(page_html, base_url, state, True, width, height))
    res = chrome(binary, [f"--window-size={max(width, MIN_WINDOW)},{height}", "--dump-dom", "file://" + wrap])
    dom = res.stdout
    start = dom.find('id="__hdc_out"')
    data = None
    if start >= 0:
        raw = dom[dom.find(">", start) + 1:dom.find("</pre>", start)]
        try:
            data = json.loads(html.unescape(raw))
        except ValueError:
            data = None
    if not data:
        sys.exit(f"measurement failed at {width}px ({state.get('name')}); Chrome said: {res.stderr.strip()[:300]}")
    shot_h = min(data["page"][1], 16000) if full_page else height
    wrap = os.path.join(tmp, "shot.html")
    open(wrap, "w", encoding="utf-8").write(build_wrapper(page_html, base_url, state, False, width, shot_h))
    chrome(binary, [f"--window-size={max(width, MIN_WINDOW)},{shot_h}", f"--screenshot={out_png}", "file://" + wrap])
    Image.open(out_png).crop((0, 0, width, shot_h)).save(out_png)
    data.update({"width": width, "state": state.get("name", "default"), "screenshot": os.path.basename(out_png)})
    json.dump(data, open(out_json, "w"), indent=1)
    return data


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", help="local .html file or http(s) URL")
    ap.add_argument("--out", required=True, help="output folder for PNG + JSON")
    ap.add_argument("--name", default=None, help="file name prefix (default: page file name)")
    ap.add_argument("--widths", default="1440,390", help="comma-separated CSS widths (default 1440,390)")
    ap.add_argument("--height", type=int, default=900, help="viewport height (default 900)")
    ap.add_argument("--states", default=None, help="JSON file with states to force (see above)")
    ap.add_argument("--no-full-page", action="store_true", help="capture only the first viewport")
    a = ap.parse_args()

    binary = find_chrome()
    NATIVE[:] = native_prefix()
    page_html, base_url = load_page(a.src)
    name = a.name or os.path.splitext(os.path.basename(a.src.rstrip("/")))[0] or "page"
    states = [{"name": "default"}] + (json.load(open(a.states)) if a.states else [])
    os.makedirs(a.out, exist_ok=True)
    index = []
    with tempfile.TemporaryDirectory() as tmp:
        for w in [int(x) for x in a.widths.split(",")]:
            for st in states:
                suffix = "" if st["name"] == "default" else "_" + st["name"]
                stem = os.path.join(a.out, f"{name}_{w}{suffix}")
                d = capture(binary, page_html, base_url, st, w, a.height, not a.no_full_page,
                            stem + ".png", stem + ".json", tmp)
                low = [e for e in d["elements"] if e.get("contrast") and e["contrast"] < 4.5]
                index.append({"png": stem + ".png", "json": stem + ".json", "width": w, "state": st["name"],
                              "page": d["page"], "horizontal_overflow": d["horizontal_overflow"],
                              "elements": len(d["elements"]), "text_below_4.5": len(low)})
                print(f"{os.path.basename(stem)}: page {d['page'][0]}x{d['page'][1]}"
                      f"{'  HORIZONTAL OVERFLOW' if d['horizontal_overflow'] else ''}"
                      f"  elements {len(d['elements'])}  text <4.5:1: {len(low)}")
    json.dump(index, open(os.path.join(a.out, f"{name}_index.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
