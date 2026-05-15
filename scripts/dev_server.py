#!/usr/bin/env python3
"""Development server that auto-regenerates tool pages when data/tools.json changes.

Usage:
    python scripts/dev_server.py

Then open http://127.0.0.1:8000/
"""

from __future__ import annotations

import http.server
import os
import socketserver
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS_PATH = ROOT / "data" / "tools.json"
GENERATOR = ROOT / "scripts" / "generate_pages.py"

_last_mtime: float | None = None


def _maybe_generate() -> None:
    """Run generate_pages.py if tools.json has changed since last check."""
    global _last_mtime
    if not TOOLS_PATH.is_file():
        return
    try:
        mtime = TOOLS_PATH.stat().st_mtime
    except OSError:
        return
    if _last_mtime is None or mtime > _last_mtime:
        _last_mtime = mtime
        try:
            subprocess.run(
                [sys.executable, str(GENERATOR)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            print("[dev] Regenerated tool pages")
        except subprocess.CalledProcessError as e:
            print("[dev] Generation failed:", e, file=sys.stderr)
            if e.stderr:
                print(e.stderr, file=sys.stderr)


class _RequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        # Disable caching so edits show immediately
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        if path == "/" or path.startswith("/tool/"):
            _maybe_generate()
        super().do_GET()


def main() -> int:
    os.chdir(ROOT)
    port = int(os.environ.get("PORT", "8000"))
    with socketserver.TCPServer(("", port), _RequestHandler) as httpd:
        print(f"[dev] Serving at http://127.0.0.1:{port}/")
        print("[dev] Pages auto-regenerate when data/tools.json changes")
        print("[dev] Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[dev] Stopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
