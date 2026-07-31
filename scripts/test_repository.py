#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "adhd-and-47-tabs"
ZIP = ROOT / "dist" / "adhd-and-47-tabs.zip"
CHECKSUMS = ROOT / "dist" / "SHA256SUMS"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ERROR: {message}")


def main() -> None:
    require((ROOT / "VERSION").read_text().strip() == "2.0.0", "VERSION is not 2.0.0")
    require((SKILL / "SKILL.md").is_file(), "missing canonical SKILL.md")
    require(not (ROOT / "i-have-adhd-and-47-tabs").exists(), "retired skill folder still exists")

    cases = json.loads((ROOT / "evals" / "cases.json").read_text())
    require(len(cases) >= 12, "evaluation suite has fewer than 12 cases")
    require(len(cases) == len({case["id"] for case in cases}), "evaluation ids are not unique")

    require(ZIP.is_file(), "generated ZIP is missing")
    require(CHECKSUMS.is_file(), "generated checksum file is missing")
    with zipfile.ZipFile(ZIP) as archive:
        require(archive.testzip() is None, "generated ZIP is corrupt")
        names = [name for name in archive.namelist() if name and not name.endswith("/")]
    require({name.split("/", 1)[0] for name in names} == {"adhd-and-47-tabs"}, "ZIP has the wrong top-level folder")
    require("adhd-and-47-tabs/SKILL.md" in names, "ZIP is missing SKILL.md")

    digest = hashlib.sha256(ZIP.read_bytes()).hexdigest()
    expected_line = f"{digest}  {ZIP.name}"
    require(CHECKSUMS.read_text(encoding="utf-8").strip() == expected_line, "SHA256SUMS does not match the ZIP")

    require((ROOT / "scripts" / "prepare_release.py").is_file(), "release preparation script is missing")
    require(not (ROOT / "scripts" / "create_release.sh").exists(), "retired release script still exists")
    require(not (ROOT / "scripts" / "publish_to_github.sh").exists(), "retired publishing script still exists")

    print("OK: repository contracts passed")


if __name__ == "__main__":
    main()
