# Local HTML Tools

A curated directory of browser-first tools where the browser does the work, especially single-file, offline-friendly, and inspectable HTML utilities with limited network or API dependence.

The directory is here: https://localhtmltools.lachlanallison.com

## Submit A Tool

Add one tool per pull request by editing [data/tools.json](data/tools.json).

Good fits are:

- Tools that run directly in the browser
- Single-file HTML tools
- Client-side utilities with no login requirement
- Offline-capable tools, or tools with limited network/API calls
- Open source tools with public, inspectable source code

Less good fits are:

- Backend-heavy SaaS apps where the browser is mostly just a client
- Login-gated products
- Closed-source tools
- Pages that are mostly marketing sites rather than usable tools

## Required Fields

Each listing needs:

| Field | Description |
| --- | --- |
| `id` | Stable kebab-case slug, used for the detail page URL |
| `name` | Tool name |
| `summary` | Short description, maximum 280 characters |
| `url` | HTTPS URL where people can use the tool |
| `source_url` | Public source repository, gist, or source folder |
| `authors` | One or more authors, usually with `name` and `url` or `github` |

The full schema lives in [data/tool.schema.json](data/tool.schema.json).

## Example

```json
{
  "id": "html-preview",
  "name": "HTML preview",
  "summary": "Type HTML and see it rendered live in your browser.",
  "url": "https://example.com/html-preview",
  "source_url": "https://github.com/example/html-preview",
  "authors": [
    {
      "name": "Example Author",
      "github": "https://github.com/example"
    }
  ],
  "license": "MIT",
  "tags": ["html", "preview", "editor"],
  "categories": ["developer"],
  "runtime": {
    "single_file": true,
    "offline": "yes",
    "needs_network": false
  },
  "kind": "tool"
}
```

## Badge

After your tool is listed, you can add a badge linking back to the directory:

https://localhtmltools.lachlanallison.com/badge/

## Local Preview

For contributors who want to preview changes locally:

```bash
python scripts/dev_server.py
```

Then open http://127.0.0.1:8000/

Opening `index.html` directly will not load `data/tools.json` because browsers restrict `file://` fetches.

## Maintainers

GitHub Actions validates `data/tools.json`, generates `tool/` pages and `sitemap.xml`, and deploys to GitHub Pages. Generated output is ignored by Git.
