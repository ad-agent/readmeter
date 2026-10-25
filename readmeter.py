#!/usr/bin/env python3
"""Count words and estimate reading time using only the Python standard library."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import re
import sys

VERSION = "1.0.0"
WORD_PATTERN = re.compile(r"[^\W_]+(?:['’\-][^\W_]+)*", re.UNICODE)


def analyze(text: str, wpm: int = 200) -> dict[str, int]:
    """Return text metrics. WPM is a configurable estimate, not a reading test."""
    if wpm <= 0:
        raise ValueError("words per minute must be greater than zero")
    words = len(WORD_PATTERN.findall(text))
    return {
        "words": words,
        "characters": len(text),
        "lines": len(text.splitlines()),
        "reading_seconds": math.ceil(words * 60 / wpm),
        "reading_minutes": math.ceil(words / wpm),
        "words_per_minute": wpm,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Word counts and reading-time estimates for UTF-8 text.",
        epilog="Example: python3 readmeter.py examples/brief.txt --json",
    )
    parser.add_argument("file", help="path to a UTF-8 text file, or - for stdin")
    parser.add_argument("--wpm", type=int, default=200, help="words per minute (default: 200)")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--version", action="version", version=f"readmeter {VERSION}")
    args = parser.parse_args(argv)
    if args.wpm <= 0:
        parser.error("--wpm must be greater than zero")
    try:
        text = (
            sys.stdin.buffer.read().decode("utf-8")
            if args.file == "-"
            else Path(args.file).read_text(encoding="utf-8")
        )
    except (OSError, UnicodeError) as exc:
        parser.error(f"cannot read input: {exc}")

    result = {"source": "stdin" if args.file == "-" else args.file, **analyze(text, args.wpm)}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("READMETER\n")
        for label, value in (
            ("Source", result["source"]),
            ("Words", f'{result["words"]:,}'),
            ("Characters", f'{result["characters"]:,}'),
            ("Lines", result["lines"]),
            ("Read time", f'{result["reading_minutes"]} min at {args.wpm} wpm'),
        ):
            print(f"  {label:<12} {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
