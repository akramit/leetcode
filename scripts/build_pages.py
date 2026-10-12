#!/usr/bin/env python3
"""Build static GitHub Pages site from README.md."""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
OUT = ROOT / "site"


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


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


def build_html(title: str, intro: list[str], sections: list[dict]) -> str:
    intro_html = "\n".join(f"<p>{html.escape(p)}</p>" for p in intro)

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

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #0f1419;
      --surface: #1a2332;
      --text: #e7ecf3;
      --muted: #8b9cb3;
      --accent: #58a6ff;
      --border: #2d3a4f;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
    }}
    .wrap {{ max-width: 52rem; margin: 0 auto; padding: 1.5rem 1.25rem 3rem; }}
    h1 {{ font-size: 1.75rem; margin: 0 0 0.5rem; }}
    .progress {{
      font-size: 1.1rem;
      color: var(--accent);
      margin: 0.75rem 0 1.25rem;
      font-weight: 600;
    }}
    .intro {{ color: var(--muted); margin-bottom: 2rem; }}
    .intro a {{ color: var(--accent); }}
    nav {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem 0.75rem;
      margin-bottom: 2rem;
      padding-bottom: 1rem;
      border-bottom: 1px solid var(--border);
    }}
    nav a {{
      color: var(--muted);
      text-decoration: none;
      font-size: 0.85rem;
    }}
    nav a:hover {{ color: var(--accent); }}
    section {{ margin-bottom: 2rem; }}
    h2 {{
      font-size: 1.15rem;
      margin: 0 0 0.65rem;
      padding-bottom: 0.35rem;
      border-bottom: 1px solid var(--border);
    }}
    .count {{ color: var(--muted); font-weight: normal; font-size: 0.9rem; }}
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
      margin-top: 0.25rem;
      accent-color: var(--accent);
    }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    li.done a {{ color: var(--muted); text-decoration: line-through; }}
    footer {{
      margin-top: 2rem;
      font-size: 0.8rem;
      color: var(--muted);
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>{html.escape(title)}</h1>
    <p class="progress" id="progress">0 / 75 solved</p>
    <div class="intro">{intro_html}</div>
    <nav>
      {' '.join(f'<a href="#{slugify(s["title"])}">{html.escape(s["title"])}</a>' for s in sections)}
    </nav>
    {''.join(sections_html)}
    <footer>Progress is saved in this browser only (localStorage).</footer>
  </div>
  <script>
    const KEY = 'leetcode-blind75-done';
    const load = () => JSON.parse(localStorage.getItem(KEY) || '{{}}');
    const save = (state) => localStorage.setItem(KEY, JSON.stringify(state));

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
      document.getElementById('progress').textContent = `${{done}} / ${{boxes.length}} solved`;
      document.querySelectorAll('.count').forEach((el) => {{
        const sid = el.dataset.section;
        const section = document.getElementById(sid);
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
    text = README.read_text(encoding="utf-8")
    title, intro, sections = parse_readme(text)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(build_html(title, intro, sections), encoding="utf-8")
    print(f"Wrote {OUT / 'index.html'}")


if __name__ == "__main__":
    main()
