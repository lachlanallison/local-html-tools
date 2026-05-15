#!/usr/bin/env python3
"""Generate a static detail page for every tool in data/tools.json.

Also regenerates sitemap.xml to include tool pages.
Run after editing tools.json and commit the results.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS_PATH = ROOT / "data" / "tools.json"
TOOL_DIR = ROOT / "tool"
SITEMAP_PATH = ROOT / "sitemap.xml"

CATEGORY_LABELS = {
    "images": "Images & design",
    "text-data": "Text & data",
    "developer": "Developer",
    "productivity": "Productivity",
    "education": "Education",
    "audio-video": "Audio & video",
    "utilities": "Utilities",
    "other": "Other",
}

SEP = " &middot; "


def escape_html(value: str) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def escape_attr(value: str) -> str:
    return escape_html(value).replace("'", "&#39;")


def format_authors(authors: list[dict]) -> str:
    parts = []
    for author in authors:
        name = escape_html(author["name"])
        url = author.get("url")
        github = author.get("github")
        if url:
            parts.append(
            f'<a href="{escape_attr(url)}" target="_blank" rel="noopener noreferrer">{name}</a>'
            )
        elif github:
            parts.append(
            f'<a href="{escape_attr(github)}" target="_blank" rel="noopener noreferrer">{name}</a>'
            )
        else:
            parts.append(name)
    return SEP.join(parts)


def runtime_badge(tool: dict) -> str:
    runtime = tool.get("runtime") or {}
    parts = []
    if runtime.get("single_file"):
        parts.append("single-file")
    offline = runtime.get("offline")
    if offline == "yes":
        parts.append("offline OK")
    elif offline == "partial":
        parts.append("partial offline")
    elif offline == "no":
        parts.append("needs network")
    if runtime.get("needs_network"):
        parts.append("API/remote")
    return SEP.join(parts) if parts else ""


def build_page(tool: dict, site_url: str) -> str:
    tool_id = tool["id"]
    name = tool["name"]
    summary = tool["summary"]
    url = tool["url"]
    source_url = tool.get("source_url")
    authors = tool.get("authors", [])
    license_name = tool.get("license")
    tags = tool.get("tags", [])
    categories = tool.get("categories", [])
    kind = tool.get("kind", "tool")
    reference_urls = tool.get("reference_urls", [])
    added = tool.get("added", "")

    canonical = f"{site_url.rstrip('/')}/tool/{tool_id}/"
    kind_label = "Collection" if kind == "collection" else "Tool"
    runtime = runtime_badge(tool)

    categories_html = "\n".join(
        f'            <span>{escape_html(CATEGORY_LABELS.get(category, category))}</span>'
        for category in categories
    )
    categories_inline_html = "".join(
        f'<span>{escape_html(CATEGORY_LABELS.get(category, category))}</span>'
        for category in categories
    )
    tags_html = "\n".join(
        f'            <span>{escape_html(tag)}</span>' for tag in tags
    )

    tags_block = ""
    if tags_html:
        tags_block = (
            "          <div class=\"tags\" aria-label=\"Tags\">\n"
            f"{tags_html}\n"
            "          </div>"
        )

    references_block = ""
    if reference_urls:
        references_list = "\n".join(
            f'          <li><a href="{escape_attr(ref)}" target="_blank" rel="noopener noreferrer">{escape_attr(ref)}</a></li>'
            for ref in reference_urls
        )
        references_block = (
            "          <h3 class=\"detail-subtitle\">References</h3>\n"
            "          <ul class=\"summary detail-refs\">\n"
            f"{references_list}\n"
            "          </ul>"
        )

    github_icon = (
        '<svg viewBox="0 0 24 24" fill="currentColor" style="width:14px;height:14px">'
        '<path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.44 9.8 8.2 11.4.6.1.82-.26.82-.58 '
        '0-.28-.01-1.04-.02-2.04-3.34.72-4.04-1.61-4.04-1.61-.55-1.4-1.34-1.77-1.34-1.77'
        '-1.1-.75.08-.74.08-.74 1.22.09 1.86 1.25 1.86 1.25 1.08 1.85 2.83 1.32 3.52 '
        '1.01.11-.79.42-1.32.77-1.62-2.69-.31-5.53-1.35-5.53-6 0-1.33.47-2.41 '
        '1.24-3.26-.13-.31-.54-1.56.12-3.25 0 0 1.01-.32 3.3 1.24.96-.27 1.98-.4 '
        '3-.4s2.04.13 3 .4c2.29-1.56 3.3-1.24 3.3-1.24.66 1.69.25 2.94.12 3.25.77.85 '
        '1.24 1.93 1.24 3.26 0 4.66-2.84 5.69-5.54 5.99.44.38.83 1.13.83 2.27 '
        '0 1.64-.02 2.96-.02 3.36 0 .32.22.7.83.58C20.56 21.8 24 17.3 24 12 '
        '24 5.37 18.63 0 12 0z"/></svg>'
    )
    external_icon = (
        '<svg viewBox="0 0 24 24" fill="currentColor" style="width:14px;height:14px">'
        '<path d="M21 13v10H3V4h12v2H5v15h14v-8h2zm3-12H13l4 4-8 8 2 2 8-8 4 4V1z"/>'
        "</svg>"
    )

    source_link = ""
    if source_url:
        source_link = (
            f'          <a class="btn btn-secondary" href="{escape_attr(source_url)}" '
            f'target="_blank" rel="noopener noreferrer">{github_icon} Source</a>\n'
        )

    license_span = (
        f"<span>License: {escape_html(license_name)}</span>" if license_name else ""
    )
    added_span = f"<span>Added: {escape_html(added)}</span>" if added else ""
    meta_extra = ""
    if license_span or added_span:
        separator = '<span aria-hidden="true">&middot;</span>' if license_span and added_span else ""
        meta_extra = (
            '          <div class="meta-row" style="margin-top:0.25rem">\n'
            f"            {license_span}\n"
            f"            {separator}\n"
            f"            {added_span}\n"
            "          </div>"
        )

    runtime_html = ""
    if runtime:
        runtime_html = (
            '<span aria-hidden="true">&middot;</span>'
            f'<span class="badge-runtime">{runtime}</span>'
        )

    json_ld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": name,
            "description": summary,
            "url": url,
            "applicationCategory": CATEGORY_LABELS.get(categories[0], "Utility")
            if categories
            else "Utility",
            "operatingSystem": "Any",
            "author": [
                {
                    "@type": "Person",
                    "name": author["name"],
                    "url": author.get("url") or author.get("github"),
                }
                for author in authors
            ],
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "isPartOf": {
                "@type": "WebSite",
                "name": "Local HTML Tools",
                "url": site_url.rstrip("/") + "/",
            },
        },
        indent=2,
    )

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{escape_html(name)} - Local HTML Tools</title>
    <meta name="description" content="{escape_attr(summary)}" />
    <link rel="canonical" href="{escape_attr(canonical)}" />
    <script>
      (function () {{
        var mode = "auto";
        try {{
          var saved = localStorage.getItem("lht-theme");
          if (["auto", "light", "dark"].indexOf(saved) !== -1) mode = saved;
        }} catch (error) {{}}
        var theme = mode === "auto"
          ? (window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark")
          : mode;
        document.documentElement.setAttribute("data-theme", theme);
      }})();
    </script>
    <link id="theme-css" rel="stylesheet" href="../../css/themes/site.css" data-base="../../css/themes/" />
    <link rel="icon" href="../../favicon.svg" type="image/svg+xml" />

    <!-- Open Graph -->
    <meta property="og:title" content="{escape_attr(name)} - Local HTML Tools" />
    <meta property="og:description" content="{escape_attr(summary)}" />
    <meta property="og:url" content="{escape_attr(canonical)}" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="{site_url.rstrip('/')}/assets/og-cover.png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{escape_attr(name)} - Local HTML Tools" />
    <meta name="twitter:description" content="{escape_attr(summary)}" />
    <meta name="twitter:image" content="{site_url.rstrip('/')}/assets/og-cover.png" />

    <script type="application/ld+json">
{json_ld}
    </script>
  </head>
  <body class="detail-page">
    <div class="wrap">
      <header class="site">
        <div class="header-top">
          <a href="../../" class="site-logo" style="text-decoration:none">
            <img src="../../favicon.svg" alt="" />
            <span class="site-logo-wordmark">LOCAL HTML TOOLS</span>
          </a>
          <label class="theme-picker" for="theme-switcher">
            <span class="sr-only">Theme</span>
            <select id="theme-switcher" class="filter">
              <option value="auto" selected>&#9680;&nbsp;&nbsp;Auto</option>
              <option value="light">&#9788;&nbsp;&nbsp;Light</option>
              <option value="dark">&#9790;&nbsp;&nbsp;Dark</option>
            </select>
          </label>
        </div>
        <p class="lede">A curated directory of browser-local and single-file HTML tools.</p>
      </header>

      <main>
        <div class="detail-nav">
          <a href="../../" class="detail-back">&larr; Back to directory</a>
          <a href="../../badge/" class="detail-badge-link">
            <span class="detail-badge-label">Get your badge:</span>
            <img src="../../badge/badge.svg" alt="Listed on Local HTML Tools" />
          </a>
        </div>

        <article class="tool-card detail-card">
          <h2 class="detail-title">{escape_html(name)}</h2>
          <div class="tags tags-categories detail-categories" aria-label="Categories">
            {categories_inline_html}
          </div>
          <p class="summary">{escape_html(summary)}</p>
          <div class="meta-row">
            <span>{escape_html(kind_label)}</span>
            <span aria-hidden="true">&middot;</span>
            {format_authors(authors)}
            {runtime_html}
          </div>
{meta_extra}
{tags_block}
          <div class="tool-actions" style="margin-top:0.85rem">
            <a class="btn btn-primary" href="{escape_attr(url)}" target="_blank" rel="noopener noreferrer">{external_icon} Open {escape_html(kind_label.lower())}</a>
{source_link}          </div>
{references_block}
        </article>
      </main>

      <footer class="site">
        <p>
          Data lives in <code>data/tools.json</code>. See <a href="../../contributing.html">how to contribute</a> (and <code>CONTRIBUTING.md</code> in the repo).
        </p>
        <p>Inspired by the spirit of local-first, inspectable HTML - see e.g. Simon Willison's <a href="https://simonwillison.net/2025/Dec/10/html-tools/">HTML tools</a> write-up.</p>
        <p>Built by <a href="https://lachlanallison.com/">Lachlan</a>.</p>
      </footer>
    </div>
    <script src="../../js/theme.js" defer></script>
  </body>
</html>
"""


def generate_sitemap(tools: list[dict], site_url: str) -> str:
    base = site_url.rstrip("/")
    urls = [
        f"""  <url>
    <loc>{base}/</loc>
    <changefreq>weekly</changefreq>
    <priority>1</priority>
  </url>""",
        f"""  <url>
    <loc>{base}/contributing.html</loc>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>""",
        f"""  <url>
    <loc>{base}/badge/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>""",
    ]
    for tool in tools:
        urls.append(
            f"""  <url>
    <loc>{base}/tool/{tool["id"]}/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>"""
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )


def main() -> int:
    if not TOOLS_PATH.is_file():
        print(f"Missing {TOOLS_PATH}", file=sys.stderr)
        return 1

    with TOOLS_PATH.open(encoding="utf-8") as file_obj:
        data = json.load(file_obj)

    tools = data.get("tools", [])
    site_url = data.get("meta", {}).get("site_url", "https://localhtmltools.lachlanallison.com")

    if TOOL_DIR.exists():
        shutil.rmtree(TOOL_DIR)
    TOOL_DIR.mkdir(parents=True)

    for tool in tools:
        tool_id = tool["id"]
        page_dir = TOOL_DIR / tool_id
        page_dir.mkdir(parents=True)
        html = build_page(tool, site_url)
        (page_dir / "index.html").write_text(html, encoding="utf-8")
        print(f"Generated tool/{tool_id}/index.html")

    sitemap = generate_sitemap(tools, site_url)
    SITEMAP_PATH.write_text(sitemap, encoding="utf-8")
    print(f"Updated {SITEMAP_PATH}")

    print(f"Done: {len(tools)} page(s) generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
