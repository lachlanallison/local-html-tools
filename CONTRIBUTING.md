# Contributing a tool

Preview the site locally with Python (no npm): from the repo root run `python scripts/dev_server.py` and open http://127.0.0.1:8000/. Opening `index.html` directly will not load `data/tools.json` because of browser `file://` restrictions. The dev server also auto-regenerates tool detail pages when you edit `data/tools.json`.

1. Fork the repository.
2. Add one object to `data/tools.json` (see `data/tool.schema.json` for the full schema).
3. Open a pull request with a short description of the tool and why it fits "local HTML" (single-file, offline-capable, browser-first, limited network/API calls, etc.).

## Requirements

- **Open source** - every tool must have a public source repository (preferably GitHub).
- **`source_url`** is required and must link to a public repo where others can inspect, fork, or contribute to the code.
- The tool must do most of its work in the browser - single-file HTML, offline-capable tools, and tools with limited network/API calls are preferred.

## Required fields

| Field | Description |
| --- | --- |
| `id` | Stable kebab-case slug |
| `name` | Display name |
| `summary` | 280 characters or fewer for cards and SEO |
| `url` | HTTPS URL where users open the tool |
| `source_url` | HTTPS URL to the public source repository (GitHub or similar) |
| `authors` | Array of `{ "name", "url"?, "github"? }` |

## Optional fields

`license`, `tags`, `categories`, `runtime`, `kind` (`tool` or `collection`), `reference_urls`, `added` (date first listed).

## Badge

After merge, you can add a badge linking back to the directory; see `badge/` on the site.
