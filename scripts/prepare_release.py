#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "VERSION"
DIST = ROOT / "dist"
ZIP = DIST / "adhd-and-47-tabs.zip"
CHECKSUMS = DIST / "SHA256SUMS"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    version = VERSION_FILE.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail("VERSION must contain a semantic version such as 2.0.0")

    notes = ROOT / "docs" / "releases" / f"{version}.md"
    if not notes.is_file():
        fail(f"missing release notes: {notes.relative_to(ROOT)}")

    subprocess.run(["make", "check"], cwd=ROOT, check=True)
    if not ZIP.is_file():
        fail(f"package was not created: {ZIP.relative_to(ROOT)}")

    digest = hashlib.sha256(ZIP.read_bytes()).hexdigest()
    CHECKSUMS.write_text(f"{digest}  {ZIP.name}\n", encoding="utf-8")

    print(f"Prepared release assets for v{version}:")
    print(f"- {ZIP.relative_to(ROOT)}")
    print(f"- {CHECKSUMS.relative_to(ROOT)}")
    print(f"- {notes.relative_to(ROOT)}")
    print("Review these files, then upload them to the matching GitHub Release.")


if __name__ == "__main__":
    main()
