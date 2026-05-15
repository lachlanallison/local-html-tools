#!/usr/bin/env python3
"""Validate data/tools.json entries against data/tool.schema.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import urllib.parse

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parent.parent


@Draft202012Validator.FORMAT_CHECKER.checks("uri", raises=ValueError)
def _check_uri(value: str) -> bool:
    result = urllib.parse.urlparse(value)
    if not result.scheme or not result.netloc:
        raise ValueError(f"{value!r} is not a valid URI")
    return True
TOOLS_PATH = ROOT / "data" / "tools.json"
SCHEMA_PATH = ROOT / "data" / "tool.schema.json"


def main() -> int:
    if not TOOLS_PATH.is_file():
        print(f"Missing {TOOLS_PATH}", file=sys.stderr)
        return 1
    if not SCHEMA_PATH.is_file():
        print(f"Missing {SCHEMA_PATH}", file=sys.stderr)
        return 1

    with SCHEMA_PATH.open(encoding="utf-8") as f:
        schema = json.load(f)
    with TOOLS_PATH.open(encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict) or "tools" not in data:
        print("tools.json must be an object with a 'tools' array.", file=sys.stderr)
        return 1
    tools = data["tools"]
    if not isinstance(tools, list):
        print("'tools' must be an array.", file=sys.stderr)
        return 1

    validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
    seen_ids: set[str] = set()
    errors = 0

    for i, tool in enumerate(tools):
        prefix = f"tools[{i}]"
        try:
            validator.validate(tool)
        except ValidationError as e:
            print(f"{prefix}: {e.message}", file=sys.stderr)
            errors += 1
            continue
        tid = tool.get("id")
        if isinstance(tid, str):
            if tid in seen_ids:
                print(f"{prefix}: duplicate id {tid!r}", file=sys.stderr)
                errors += 1
            seen_ids.add(tid)

    if errors:
        print(f"Validation failed with {errors} error(s).", file=sys.stderr)
        return 1

    print(f"OK: {len(tools)} tool(s), schema valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
