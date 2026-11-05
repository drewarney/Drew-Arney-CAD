#!/usr/bin/env python3
"""Move the website's text in and out of one JSON file.

Every editable piece of text in index.html / work.html carries a
data-text="<id>" attribute; the rest (tagline, contact details, services)
lives in projects.js. This script keeps the editor artifact and the site
in step:

    python3 tools/site_text.py export content.json   # site  -> JSON
    python3 tools/site_text.py apply  content.json   # JSON  -> site

In the JSON, text is plain (no HTML entities); **double asterisks** mark
bold, which becomes <strong> on the page.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = [ROOT / "index.html", ROOT / "work.html"]
PROJECTS = ROOT / "projects.js"

# (section title, page label, [(id, label, multiline)])
SECTIONS = [
    ("Search & browser tab", "Both pages", [
        ("title_home", "Home page tab title", False),
        ("title_work", "Our Work page tab title", False),
        ("meta_description", "Search-engine description (shown under the link in Google)", True),
    ]),
    ("Business & contact details", "Both pages", [
        ("business_name", "Business name (next to the logo and in the footer copyright)", False),
        ("util_text", "Top strip", False),
        ("email", "Email address", False),
        ("phone", "Phone number (leave empty to hide it)", False),
        ("hours", "Hours", False),
        ("nav_quote", "Header button", False),
    ]),
    ("Main banner", "Home page", [
        ("hero_eyebrow", "Small label", False),
        ("hero_headline", "Headline", True),
        ("tagline", "Paragraph", True),
        ("hero_btn_primary", "First button", False),
        ("hero_btn_secondary", "Second button", False),
    ]),
    ("Facts strip", "Home page", [
        (f"fact{i}_{k}", f"Fact {i} {'heading' if k == 'title' else 'text'}", False)
        for i in range(1, 5) for k in ("title", "text")
    ]),
    ("Services", "Home page", [
        ("services_kicker", "Small label", False),
        ("services_heading", "Heading", False),
        ("services_intro", "Intro text", True),
    ] + [
        (f"svc{i}_{k}", f"Service {i} {'name' if k == 'title' else 'description'}", k == "body")
        for i in range(1, 9) for k in ("title", "body")
    ]),
    ("Your CAD box", "Home page", [
        ("cad_heading", "Heading", False),
        ("cad_text", "Text (**double asterisks** make text bold)", True),
    ]),
    ("How it works", "Home page", [
        ("process_heading", "Heading", False),
    ] + [
        (f"step{i}_{k}", f"Step {i} {'heading' if k == 'title' else 'text'}", k == "text")
        for i in range(1, 5) for k in ("title", "text")
    ]),
    ("About", "Home page", [
        ("about_kicker", "Small label", False),
        ("about_heading", "Heading", False),
        ("about_lead", "First paragraph", True),
        ("about_body", "Second paragraph", True),
        ("founder_heading", "Founder heading", False),
        ("founder_p1", "Founder paragraph 1", True),
        ("founder_p2", "Founder paragraph 2", True),
    ]),
    ("Industries", "Home page", [
        ("industries_kicker", "Small label", False),
        ("industries_heading", "Heading", False),
        ("industries_intro", "Intro text", True),
    ] + [(f"tile{i}", f"Industry {i}", False) for i in range(1, 7)]),
    ("Contact banner", "Home page", [
        ("cta_heading", "Heading", False),
        ("cta_text", "Text", True),
        ("cta_button", "Button", False),
    ]),
    ("Footer", "Both pages", [
        ("footer_blurb", "Blurb under the logo", True),
        ("footer_area_text", "Service area text", True),
        ("footer_location", "Location after the copyright", False),
        ("footer_note", "Bottom-right note", False),
    ]),
    ("Our Work page", "Our Work page", [
        ("work_eyebrow", "Small label", False),
        ("work_heading", "Heading", False),
        ("work_lede", "Intro text", True),
        ("work_empty_heading", "Coming-soon box heading", False),
        ("work_empty_text", "Coming-soon box text", True),
        ("work_empty_button", "Coming-soon box button", False),
    ]),
]

SITE_KEYS = {"email": "email", "phone": "phone", "hours": "hours", "tagline": "tagline"}


def to_plain(fragment):
    fragment = re.sub(r"</?strong>", "**", fragment)
    return html.unescape(fragment)


def to_html(text):
    out = html.escape(text, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)


def element_re(field_id):
    return re.compile(
        r'(<(\w+)\b[^>]*\bdata-text="' + re.escape(field_id) + r'"[^>]*>)(.*?)(</\2>)', re.S
    )


META_RE = re.compile(r'(<meta name="description" data-text="meta_description" content=")([^"]*)(")')


def js_string(key, src):
    m = re.search(r"\b" + key + r': "((?:[^"\\]|\\.)*)"', src)
    return json.loads('"' + m.group(1) + '"') if m else None


def read_site():
    pages = {p: p.read_text() for p in PAGES}
    js = PROJECTS.read_text()
    values = {}
    for sec_title, _, fields in SECTIONS:
        for fid, _, _ in fields:
            found = []
            if fid == "meta_description":
                found = [html.unescape(m.group(2)) for src in pages.values() for m in META_RE.finditer(src)]
            elif fid in SITE_KEYS:
                found = [js_string(SITE_KEYS[fid], js)]
            elif fid == "business_name":
                found = [js_string("name", js)]
                found += [to_plain(m.group(3)) for src in pages.values() for m in element_re(fid).finditer(src)]
            elif fid.startswith("svc"):
                i, kind = re.match(r"svc(\d)_(\w+)", fid).groups()
                block = re.search(r"export const SERVICES = \[(.*?)\];", js, re.S).group(1)
                items = re.findall(r'title: "((?:[^"\\]|\\.)*)",\s*body: "((?:[^"\\]|\\.)*)"', block)
                t, b = items[int(i) - 1]
                found = [json.loads('"' + (t if kind == "title" else b) + '"')]
            else:
                found = [to_plain(m.group(3)) for src in pages.values() for m in element_re(fid).finditer(src)]
            if not found or any(v != found[0] for v in found):
                sys.exit(f"{fid}: expected one consistent value, found {found!r}")
            values[fid] = found[0]
    return values


def export(path):
    values = read_site()
    data = {
        "site": "drewarneycad.com",
        "sections": [
            {
                "title": t,
                "page": page,
                "fields": [
                    {"id": fid, "label": label, "multiline": ml, "live": values[fid], "value": values[fid]}
                    for fid, label, ml in fields
                ],
            }
            for t, page, fields in SECTIONS
        ],
    }
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"exported {len(values)} fields to {path}")


def set_js_string(key, value, src, count=1):
    pattern = re.compile(r"(\b" + key + r': )"(?:[^"\\]|\\.)*"')
    new, n = pattern.subn(lambda m: m.group(1) + json.dumps(value, ensure_ascii=False), src, count=count)
    if n != 1:
        sys.exit(f"projects.js: could not set {key}")
    return new


def apply(path):
    data = json.loads(Path(path).read_text())
    new = {f["id"]: f["value"] for s in data["sections"] for f in s["fields"]}
    old = read_site()
    changed = {k: v for k, v in new.items() if k in old and old[k] != v}
    if not changed:
        print("no changes")
        return
    pages = {p: p.read_text() for p in PAGES}
    js = PROJECTS.read_text()
    for fid, value in changed.items():
        if fid == "meta_description":
            for p in pages:
                pages[p] = META_RE.sub(lambda m: m.group(1) + html.escape(value, quote=True) + m.group(3), pages[p])
            continue
        if fid in SITE_KEYS:
            site = re.search(r"export const SITE = \{.*?\};", js, re.S).group(0)
            js = js.replace(site, set_js_string(SITE_KEYS[fid], value, site))
            continue
        if fid.startswith("svc"):
            i, kind = re.match(r"svc(\d)_(\w+)", fid).groups()
            block = re.search(r"export const SERVICES = \[.*?\];", js, re.S).group(0)
            entries = re.findall(r"\{.*?\}", block, re.S)
            entry = entries[int(i) - 1]
            js = js.replace(block, block.replace(entry, set_js_string(kind, value, entry)))
            continue
        if fid == "business_name":
            site = re.search(r"export const SITE = \{.*?\};", js, re.S).group(0)
            js = js.replace(site, set_js_string("name", value, site))
        for p in pages:
            pages[p] = element_re(fid).sub(lambda m: m.group(1) + to_html(value) + m.group(4), pages[p])
    for p, src in pages.items():
        p.write_text(src)
    PROJECTS.write_text(js)
    after = read_site()
    bad = [k for k, v in changed.items() if after[k] != v]
    if bad:
        sys.exit(f"did not apply cleanly: {bad}")
    for k in changed:
        print(f"updated {k}")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("export", "apply"):
        sys.exit(__doc__)
    {"export": export, "apply": apply}[sys.argv[1]](sys.argv[2])
