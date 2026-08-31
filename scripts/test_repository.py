#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import stat
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
NAME = "adhd-and-47-tabs"
VERSION = "3.0.1"
SOURCE = ROOT / NAME
ZIP = ROOT / "dist" / f"{NAME}.zip"
CHECKSUMS = ROOT / "dist" / "SHA256SUMS"
FIXED_TIME = (2026, 8, 31, 0, 0, 0)
EXCLUDED_DIRS = {".git", "__pycache__"}
EXCLUDED_NAMES = {".DS_Store"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def expected_files() -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    for path in SOURCE.rglob("*"):
        relative = path.relative_to(SOURCE)
        if any(part in EXCLUDED_DIRS or part.startswith(".") for part in relative.parts):
            continue
        if path.name in EXCLUDED_NAMES or path.name.endswith(("~", ".pyc", ".pyo")):
            continue
        require(not path.is_symlink(), f"source contains a symlink: {relative}")
        if path.is_file():
            archive_name = (PurePosixPath(NAME) / PurePosixPath(relative.as_posix())).as_posix()
            result[archive_name] = path.read_bytes()
    return dict(sorted(result.items()))


def main() -> None:
    require(ZIP.is_file(), "canonical ZIP is missing")
    require(CHECKSUMS.is_file(), "SHA256SUMS is missing")
    require((ROOT / "dist" / ".gitkeep").is_file(), "dist/.gitkeep is missing")
    require(ZIP.stat().st_size < 250_000, "skill ZIP unexpectedly exceeds 250 KB")

    expected = expected_files()
    require(expected, "source package is empty")

    with zipfile.ZipFile(ZIP) as archive:
        require(archive.testzip() is None, "ZIP is corrupt")
        infos = archive.infolist()
        names = [info.filename for info in infos]
        require(names == sorted(names), "ZIP entries are not sorted")
        require(len(names) == len(set(names)), "ZIP contains duplicate entries")
        require(all(not name.endswith("/") for name in names), "ZIP contains directory entries")
        require(set(names) == set(expected), "ZIP file set does not match source package")

        for info in infos:
            path = PurePosixPath(info.filename)
            require(not path.is_absolute(), f"absolute ZIP path: {info.filename}")
            require(".." not in path.parts, f"path traversal in ZIP: {info.filename}")
            require("\\" not in info.filename, f"backslash in ZIP path: {info.filename}")
            require(path.parts[0] == NAME, f"wrong top-level folder: {info.filename}")
            require(info.date_time == FIXED_TIME, f"non-deterministic timestamp: {info.filename}")
            require(info.compress_type == zipfile.ZIP_DEFLATED, f"entry is not deflated: {info.filename}")
            mode = info.external_attr >> 16
            require(stat.S_ISREG(mode), f"entry is not a regular file: {info.filename}")
            require(stat.S_IMODE(mode) == 0o644, f"unexpected permissions: {info.filename}")
            require(archive.read(info.filename) == expected[info.filename], f"content drift: {info.filename}")

    digest = hashlib.sha256(ZIP.read_bytes()).hexdigest()
    expected_checksum = f"{digest}  {ZIP.name}"
    require(
        CHECKSUMS.read_text(encoding="utf-8").strip() == expected_checksum,
        "SHA256SUMS does not match the ZIP",
    )

    skill_inside = expected[f"{NAME}/SKILL.md"].decode("utf-8")
    require(f'version: "{VERSION}"' in skill_inside, "packaged SKILL version is stale")
    openai_metadata = expected[f"{NAME}/agents/openai.yaml"].decode("utf-8")
    for signal in (
        'display_name: "ADHD & 47 Tabs"',
        'allow_implicit_invocation: true',
        'default_prompt:',
    ):
        require(signal in openai_metadata, f"OpenAI host metadata is missing {signal}")
    for required in (
        f"{NAME}/references/interaction-patterns.md",
        f"{NAME}/references/examples.md",
        f"{NAME}/references/quick-reference.md",
        f"{NAME}/agents/openai.yaml",
        f"{NAME}/LICENSE",
        f"{NAME}/NOTICE.md",
        f"{NAME}/README.md",
    ):
        require(required in expected, f"package is missing {required}")

    forbidden_suffixes = {".py", ".sh", ".js", ".exe", ".dll", ".bat", ".cmd"}
    for name in names:
        require(PurePosixPath(name).suffix.lower() not in forbidden_suffixes, f"executable code in skill: {name}")
        require("__pycache__" not in name and "/." not in name, f"hidden/cache file in skill: {name}")

    before = ZIP.read_bytes()
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_zip.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    require(completed.returncode == 0, f"deterministic rebuild failed: {completed.stderr}")
    require(ZIP.read_bytes() == before, "rebuilding the ZIP changed its bytes")
    require(
        hashlib.sha256(ZIP.read_bytes()).hexdigest() == digest,
        "rebuilding changed the ZIP digest",
    )

    workflows = ROOT / ".github" / "workflows"
    require(
        not workflows.exists() or not any(path.is_file() for path in workflows.rglob("*")),
        "hosted GitHub Actions workflows are not allowed",
    )

    print(
        f"OK: deterministic package verified "
        f"({len(names)} files; {ZIP.stat().st_size:,} bytes; SHA-256 {digest})"
    )


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
