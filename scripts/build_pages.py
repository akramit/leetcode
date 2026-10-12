#!/usr/bin/env python3
"""Build static GitHub Pages site from README.md and reading shelf."""

import html
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
READING_SHELF = ROOT / "content" / "reading-shelf.md"
OUT = ROOT / "site"

INLINE_MD = re.compile(r"\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*")
READING_LINK = re.compile(r"^\*\s+\[([^\]]+)\]\(([^)]+)\)\s*$")


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def normalize_url(url: str) -> str:
    url = url.strip()
    if url.startswith("https://www.google.com/search?q="):
        return unquote(url.removeprefix("https://www.google.com/search?q="))
    return url


def parse_readme(text: str) -> tuple[str, list[str], list[dict]]:
    lines = text.splitlines()
    intro: list[str] = []
    sections: list[dict] = []
    current: dict | None = None
    i = 0

    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        i = 1
    else:
        title = "LeetCode"

    while i < len(lines) and not lines[i].startswith("## "):
        if lines[i].strip():
            intro.append(lines[i])
        i += 1

    item_re = re.compile(
        r"^- \[[ xX]\] \[(.+?)\]\((https://leetcode\.com/problems/[^/]+/)\)"
    )

    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            if current:
                sections.append(current)
            current = {"title": line[3:].strip(), "items": []}
        elif current and (m := item_re.match(line)):
            name, url = m.group(1), m.group(2)
            slug = url.rstrip("/").split("/")[-1]
            current["items"].append({"name": name, "url": url, "slug": slug})
        i += 1

    if current:
        sections.append(current)

    return title, intro, sections


def parse_reading_shelf(text: str) -> tuple[str, str, list[dict]]:
    lines = text.splitlines()
    title = "Reading Shelf"
    intro: list[str] = []
    sections: list[dict] = []
    current: dict | None = None
    i = 0

    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        i = 1

    while i < len(lines):
        line = lines[i]
        if line.startswith("### "):
            if current:
                sections.append(current)
            current = {"title": line[4:].strip(), "links": []}
        elif line.startswith("## "):
            pass
        elif current and (m := READING_LINK.match(line)):
            current["links"].append(
                {"name": m.group(1), "url": normalize_url(m.group(2))}
            )
        elif not line.startswith("#") and line.strip() and current is None:
            intro.append(line.strip())
        i += 1

    if current:
        sections.append(current)

    return title, " ".join(intro), sections


def render_inline_markdown(text: str) -> str:
    parts: list[str] = []
    last = 0
    for m in INLINE_MD.finditer(text):
        parts.append(html.escape(text[last : m.start()]))
        if m.group(3) is not None:
            parts.append(f"<strong>{html.escape(m.group(3))}</strong>")
        else:
            parts.append(
                f'<a href="{html.escape(normalize_url(m.group(2)), quote=True)}" '
                f'target="_blank" rel="noopener">{html.escape(m.group(1))}</a>'
            )
        last = m.end()
    parts.append(html.escape(text[last:]))
    return "".join(parts)


def intro_for_site(intro: list[str]) -> list[str]:
    skip_prefixes = ("Progress:", "**Site:**")
    return [line for line in intro if not line.startswith(skip_prefixes)]


def build_practice_panel(title: str, intro: list[str], sections: list[dict]) -> str:
    intro_html = "\n".join(
        f"<p>{render_inline_markdown(p)}</p>" for p in intro_for_site(intro)
    )
    jump_nav = " ".join(
        f'<a href="#{slugify(s["title"])}">{html.escape(s["title"])}</a>'
        for s in sections
    )
    sections_html = []
    for sec in sections:
        sid = slugify(sec["title"])
        items = []
        for it in sec["items"]:
            items.append(
                f"""<li>
  <label>
    <input type="checkbox" data-slug="{html.escape(it['slug'], quote=True)}" />
    <a href="{html.escape(it['url'], quote=True)}" target="_blank" rel="noopener">{html.escape(it['name'])}</a>
  </label>
</li>"""
            )
        sections_html.append(
            f"""<section id="{sid}">
  <h2>{html.escape(sec['title'])} <span class="count" data-section="{html.escape(sid, quote=True)}"></span></h2>
  <ul class="problems">{''.join(items)}</ul>
</section>"""
        )

    return f"""
    <div class="panel panel-practice" id="panel-practice" role="tabpanel" aria-labelledby="tab-practice">
      <header class="panel-head">
        <h1>{html.escape(title)}</h1>
        <p class="progress" id="progress">0 / 75 solved</p>
        <div class="intro">{intro_html}</div>
      </header>
      <nav class="jump-nav" aria-label="Problem categories">{jump_nav}</nav>
      {''.join(sections_html)}
      <footer class="panel-foot">Progress is saved in this browser only.</footer>
    </div>"""


def build_reading_panel(
    title: str, intro: str, sections: list[dict]
) -> str:
    toc = "".join(
        f'<a href="#{slugify(s["title"])}">{html.escape(s["title"])}</a>'
        for s in sections
    )
    body = []
    for sec in sections:
        sid = slugify(sec["title"])
        links = "".join(
            f'<li><a href="{html.escape(l["url"], quote=True)}" target="_blank" rel="noopener">'
            f"{html.escape(l['name'])}</a></li>"
            for l in sec["links"]
        )
        body.append(
            f"""<article class="shelf-section" id="{sid}">
  <h2>{html.escape(sec['title'])}</h2>
  <ul class="shelf-links">{links}</ul>
</article>"""
        )

    intro_p = f"<p>{html.escape(intro)}</p>" if intro else ""
    return f"""
    <div class="panel panel-reading" id="panel-reading" role="tabpanel" aria-labelledby="tab-reading" hidden>
      <header class="shelf-hero">
        <h1>{html.escape(title)}</h1>
        {intro_p}
      </header>
      <nav class="shelf-toc" aria-label="Reading sections">{toc}</nav>
      <div class="shelf-body">{''.join(body)}</div>
    </div>"""


def build_html(
    practice_title: str,
    intro: list[str],
    sections: list[dict],
    reading_title: str,
    reading_intro: str,
    reading_sections: list[dict],
) -> str:
    practice = build_practice_panel(practice_title, intro, sections)
    reading = build_reading_panel(reading_title, reading_intro, reading_sections)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(practice_title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,700;1,9..144,500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --ink: #12161c;
      --practice-bg: #12161c;
      --practice-surface: #1a222d;
      --practice-text: #e8edf4;
      --practice-muted: #8a9bb0;
      --practice-accent: #5eb3ff;
      --practice-border: #2a3544;
      --reading-bg: #1c1814;
      --reading-paper: #f3ebe0;
      --reading-ink: #2a2218;
      --reading-muted: #6b5d4f;
      --reading-accent: #b86b2c;
      --reading-rule: #d9cbb8;
      --font-display: "Fraunces", Georgia, serif;
      --font-body: "IBM Plex Sans", system-ui, sans-serif;
      --measure: 38rem;
    }}

    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}

    @media (prefers-reduced-motion: reduce) {{
      html {{ scroll-behavior: auto; }}
    }}

    body {{
      margin: 0;
      font-family: var(--font-body);
      font-size: 1rem;
      line-height: 1.55;
      color: var(--practice-text);
      background: var(--practice-bg);
    }}

    body.theme-reading {{
      color: var(--reading-ink);
      background: var(--reading-bg);
    }}

    .site-bar {{
      position: sticky;
      top: 0;
      z-index: 10;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      padding: 0.65rem 1.25rem;
      border-bottom: 1px solid var(--practice-border);
      background: color-mix(in srgb, var(--practice-bg) 92%, transparent);
      backdrop-filter: blur(8px);
    }}

    body.theme-reading .site-bar {{
      border-color: #3d342c;
      background: color-mix(in srgb, var(--reading-bg) 90%, transparent);
    }}

    .site-mark {{
      font-family: var(--font-display);
      font-size: 1.05rem;
      font-weight: 500;
      letter-spacing: -0.02em;
      color: var(--practice-muted);
    }}

    body.theme-reading .site-mark {{ color: #a89888; }}

    .tabs {{
      display: flex;
      gap: 0.35rem;
    }}

    .tabs button {{
      font: inherit;
      font-size: 0.9rem;
      font-weight: 500;
      padding: 0.45rem 0.85rem;
      border: 1px solid transparent;
      border-radius: 999px;
      background: transparent;
      color: var(--practice-muted);
      cursor: pointer;
      transition: color 0.15s, background 0.15s, border-color 0.15s;
    }}

    .tabs button:hover {{
      color: var(--practice-text);
      background: var(--practice-surface);
    }}

    .tabs button[aria-selected="true"] {{
      color: var(--practice-text);
      background: var(--practice-surface);
      border-color: var(--practice-border);
    }}

    body.theme-reading .tabs button {{
      color: #a89888;
    }}

    body.theme-reading .tabs button:hover,
    body.theme-reading .tabs button[aria-selected="true"] {{
      color: var(--reading-paper);
      background: #2e2720;
      border-color: #4a4036;
    }}

    .tabs button:focus-visible {{
      outline: 2px solid var(--practice-accent);
      outline-offset: 2px;
    }}

    body.theme-reading .tabs button:focus-visible {{
      outline-color: var(--reading-accent);
    }}

    .layout {{
      max-width: 52rem;
      margin: 0 auto;
      padding: 1.25rem 1.25rem 3rem;
    }}

    body.theme-reading .layout {{
      max-width: calc(var(--measure) + 4rem);
    }}

    .panel-practice h1 {{
      font-family: var(--font-display);
      font-size: clamp(1.6rem, 4vw, 2rem);
      font-weight: 700;
      margin: 0 0 0.35rem;
      letter-spacing: -0.03em;
    }}

    .progress {{
      font-size: 1.05rem;
      font-weight: 600;
      color: var(--practice-accent);
      margin: 0 0 1rem;
    }}

    .intro {{
      color: var(--practice-muted);
      max-width: var(--measure);
    }}

    .intro a {{ color: var(--practice-accent); }}
    .intro strong {{ color: var(--practice-text); font-weight: 600; }}

    .jump-nav {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem 0.75rem;
      margin: 1.5rem 0 2rem;
      padding-bottom: 1rem;
      border-bottom: 1px solid var(--practice-border);
    }}

    .jump-nav a {{
      color: var(--practice-muted);
      text-decoration: none;
      font-size: 0.82rem;
    }}

    .jump-nav a:hover {{ color: var(--practice-accent); }}

    .panel-practice section {{ margin-bottom: 2rem; }}

    .panel-practice h2 {{
      font-size: 1.1rem;
      font-weight: 600;
      margin: 0 0 0.6rem;
      padding-bottom: 0.35rem;
      border-bottom: 1px solid var(--practice-border);
    }}

    .count {{
      color: var(--practice-muted);
      font-weight: 400;
      font-size: 0.88rem;
    }}

    ul.problems {{
      list-style: none;
      margin: 0;
      padding: 0;
    }}

    ul.problems li {{ margin: 0.35rem 0; }}

    label {{
      display: flex;
      align-items: flex-start;
      gap: 0.5rem;
      cursor: pointer;
    }}

    input[type="checkbox"] {{
      margin-top: 0.2rem;
      accent-color: var(--practice-accent);
    }}

    .panel-practice a {{
      color: var(--practice-accent);
      text-decoration: none;
    }}

    .panel-practice a:hover {{ text-decoration: underline; }}

    li.done a {{
      color: var(--practice-muted);
      text-decoration: line-through;
    }}

    .panel-foot {{
      margin-top: 2rem;
      font-size: 0.8rem;
      color: var(--practice-muted);
    }}

    .panel-reading {{
      background: var(--reading-paper);
      margin: 0 -1.25rem;
      padding: 2rem 1.5rem 2.5rem;
      border-radius: 2px;
      box-shadow: 0 1px 0 #4a4036 inset, 0 24px 48px rgba(0,0,0,0.35);
    }}

    .shelf-hero h1 {{
      font-family: var(--font-display);
      font-size: clamp(1.75rem, 4.5vw, 2.35rem);
      font-weight: 700;
      margin: 0 0 0.75rem;
      color: var(--reading-ink);
      letter-spacing: -0.03em;
      line-height: 1.15;
    }}

    .shelf-hero p {{
      margin: 0;
      color: var(--reading-muted);
      max-width: var(--measure);
      font-size: 1.02rem;
      line-height: 1.65;
    }}

    .shelf-toc {{
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
      margin: 2rem 0;
      padding: 1rem 0;
      border-top: 1px solid var(--reading-rule);
      border-bottom: 1px solid var(--reading-rule);
      max-width: var(--measure);
    }}

    .shelf-toc a {{
      color: var(--reading-accent);
      text-decoration: none;
      font-size: 0.92rem;
      line-height: 1.4;
    }}

    .shelf-toc a:hover {{ text-decoration: underline; }}

    .shelf-section {{
      max-width: var(--measure);
      margin-bottom: 2.25rem;
    }}

    .shelf-section h2 {{
      font-family: var(--font-display);
      font-size: 1.15rem;
      font-weight: 600;
      margin: 0 0 0.75rem;
      padding-left: 0.85rem;
      border-left: 3px solid var(--reading-accent);
      color: var(--reading-ink);
      line-height: 1.35;
    }}

    ul.shelf-links {{
      margin: 0;
      padding: 0 0 0 1.1rem;
      list-style: none;
    }}

    ul.shelf-links li {{
      position: relative;
      margin: 0.45rem 0;
      padding-left: 0.65rem;
    }}

    ul.shelf-links li::before {{
      content: "";
      position: absolute;
      left: 0;
      top: 0.65em;
      width: 4px;
      height: 4px;
      border-radius: 50%;
      background: var(--reading-muted);
    }}

    ul.shelf-links a {{
      color: var(--reading-ink);
      text-decoration: none;
      border-bottom: 1px solid transparent;
      transition: border-color 0.15s, color 0.15s;
    }}

    ul.shelf-links a:hover {{
      color: var(--reading-accent);
      border-bottom-color: color-mix(in srgb, var(--reading-accent) 40%, transparent);
    }}

    [hidden] {{ display: none !important; }}
  </style>
</head>
<body>
  <div class="site-bar">
    <span class="site-mark">Interview prep</span>
    <div class="tabs" role="tablist" aria-label="Main sections">
      <button type="button" role="tab" id="tab-practice" aria-controls="panel-practice" aria-selected="true">Blind 75</button>
      <button type="button" role="tab" id="tab-reading" aria-controls="panel-reading" aria-selected="false">Reading Shelf</button>
    </div>
  </div>
  <main class="layout">
    {practice}
    {reading}
  </main>
  <script>
    const TAB_KEY = 'leetcode-active-tab';
    const CHECK_KEY = 'leetcode-blind75-done';

    const tabPractice = document.getElementById('tab-practice');
    const tabReading = document.getElementById('tab-reading');
    const panelPractice = document.getElementById('panel-practice');
    const panelReading = document.getElementById('panel-reading');

    function setTab(name) {{
      const reading = name === 'reading';
      tabPractice.setAttribute('aria-selected', reading ? 'false' : 'true');
      tabReading.setAttribute('aria-selected', reading ? 'true' : 'false');
      panelPractice.hidden = reading;
      panelReading.hidden = !reading;
      document.body.classList.toggle('theme-reading', reading);
      localStorage.setItem(TAB_KEY, name);
      history.replaceState(null, '', reading ? '#reading' : '#practice');
    }}

    tabPractice.addEventListener('click', () => setTab('practice'));
    tabReading.addEventListener('click', () => setTab('reading'));

    const initial = location.hash === '#reading'
      ? 'reading'
      : (localStorage.getItem(TAB_KEY) || 'practice');
    setTab(initial);

    const load = () => JSON.parse(localStorage.getItem(CHECK_KEY) || '{{}}');
    const save = (state) => localStorage.setItem(CHECK_KEY, JSON.stringify(state));

    function refresh() {{
      const state = load();
      const boxes = document.querySelectorAll('input[data-slug]');
      let done = 0;
      boxes.forEach((box) => {{
        const slug = box.dataset.slug;
        box.checked = !!state[slug];
        box.closest('li').classList.toggle('done', box.checked);
        if (box.checked) done++;
      }});
      const progress = document.getElementById('progress');
      if (progress) progress.textContent = `${{done}} / ${{boxes.length}} solved`;
      document.querySelectorAll('.count').forEach((el) => {{
        const sid = el.dataset.section;
        const section = document.getElementById(sid);
        if (!section) return;
        const total = section.querySelectorAll('input[data-slug]').length;
        const sectionDone = section.querySelectorAll('input[data-slug]:checked').length;
        el.textContent = `(${{sectionDone}}/${{total}})`;
      }});
    }}

    document.querySelectorAll('input[data-slug]').forEach((box) => {{
      box.addEventListener('change', () => {{
        const state = load();
        state[box.dataset.slug] = box.checked;
        save(state);
        refresh();
      }});
    }});
    refresh();
  </script>
</body>
</html>"""


def main() -> None:
    practice_text = README.read_text(encoding="utf-8")
    practice_title, intro, sections = parse_readme(practice_text)

    reading_text = READING_SHELF.read_text(encoding="utf-8")
    reading_title, reading_intro, reading_sections = parse_reading_shelf(reading_text)

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(
        build_html(
            practice_title,
            intro,
            sections,
            reading_title,
            reading_intro,
            reading_sections,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {OUT / 'index.html'}")


if __name__ == "__main__":
    main()
