#!/usr/bin/env python3
"""Make the Judge Laugh in One Line — entry writer.

Writes one funny one-liner to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR/entry.txt), after checking it against the
competition gate: UTF-8 text, 1-200 characters, not whitespace-only,
a single line. Python 3.13 stdlib only, no network.
"""

import os
import sys

LINE = (
    "I told my barber 'surprise me' and now my driver's license photo "
    "looks like a mugshot with better lighting."
)

MAX_CHARS = 200


def validate(line: str) -> str | None:
    """Return an error message if the line fails the gate, else None."""
    if "\n" in line or "\r" in line:
        return "entry must be a single line"
    if not line.strip():
        return "entry must not be whitespace-only"
    if not 1 <= len(line) <= MAX_CHARS:
        return f"entry is {len(line)} chars, must be 1-{MAX_CHARS}"
    if any(ord(c) < 0x20 for c in line):
        return "entry contains control characters"
    try:
        if line.encode("utf-8").decode("utf-8") != line:
            return "UTF-8 round-trip failed"
    except UnicodeError:
        return "entry is not valid UTF-8"
    return None


def main() -> int:
    error = validate(LINE)
    if error is not None:
        print(error, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    # The file holds exactly the line: no trailing newline, no stray bytes.
    with open(path, "wb") as f:
        f.write(data)

    # Byte-exact write-back check.
    with open(path, "rb") as f:
        if f.read() != data:
            print("write-back check failed", file=sys.stderr)
            return 1

    print(f"wrote {len(LINE)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
