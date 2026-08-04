#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "adhd-and-47-tabs"
VERSION_FILE = ROOT / "VERSION"


def run(*command: str) -> None:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.returncode:
        if completed.stderr:
            print(completed.stderr, file=sys.stderr, end="")
        raise SystemExit(completed.returncode)


def main() -> None:
    version = VERSION_FILE.read_text(encoding="utf-8").strip()
    tag = f"v{version}"
    zip_path = ROOT / "dist" / f"{NAME}.zip"
    checksums = ROOT / "dist" / "SHA256SUMS"
    release_notes = ROOT / "docs" / "releases" / f"{version}.md"

    run(sys.executable, "scripts/validate_skill.py")
    run(sys.executable, "scripts/build_zip.py")
    run(sys.executable, "scripts/test_repository.py")
    run(sys.executable, "scripts/test_score_responses.py")
    run(sys.executable, "scripts/test_validate_skill.py")

    if not release_notes.is_file():
        raise SystemExit(f"ERROR: missing {release_notes.relative_to(ROOT)}")
    if f"v{version}" not in release_notes.read_text(encoding="utf-8"):
        raise SystemExit("ERROR: release notes do not identify the release version")

    digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    checksum_line = checksums.read_text(encoding="utf-8").strip()
    expected_line = f"{digest}  {zip_path.name}"
    if checksum_line != expected_line:
        raise SystemExit("ERROR: release checksum does not match the canonical ZIP")

    print(
        "\nRelease candidate ready\n"
        f"  Version: {version}\n"
        f"  Tag: {tag}\n"
        f"  Artifact: {zip_path.relative_to(ROOT)} ({zip_path.stat().st_size:,} bytes)\n"
        f"  Checksum: {digest}\n"
        f"  Notes: {release_notes.relative_to(ROOT)}\n"
        "\nPublish only from the verified merged main commit."
    )


if __name__ == "__main__":
    main()
