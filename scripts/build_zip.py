#!/usr/bin/env python3
from __future__ import annotations

import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
NAME = "adhd-and-47-tabs"
SOURCE = ROOT / NAME
DIST = ROOT / "dist"
OUTPUT = DIST / f"{NAME}.zip"
STALE_OUTPUT = DIST / "i-have-adhd-and-47-tabs.zip"
FIXED_TIME = (2026, 7, 31, 0, 0, 0)
EXCLUDED_DIRS = {".git", "__pycache__"}
EXCLUDED_NAMES = {".DS_Store"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def should_include(path: Path) -> bool:
    relative = path.relative_to(SOURCE)
    if any(part in EXCLUDED_DIRS for part in relative.parts):
        return False
    if path.name in EXCLUDED_NAMES or path.suffix in EXCLUDED_SUFFIXES:
        return False
    if path.name.endswith("~"):
        return False
    return path.is_file()


def main() -> None:
    if not (SOURCE / "SKILL.md").is_file():
        raise SystemExit(f"Missing {SOURCE / 'SKILL.md'}")

    DIST.mkdir(parents=True, exist_ok=True)
    OUTPUT.unlink(missing_ok=True)
    STALE_OUTPUT.unlink(missing_ok=True)

    files = sorted(path for path in SOURCE.rglob("*") if should_include(path))
    if not files:
        raise SystemExit(f"No package files found in {SOURCE}")

    with zipfile.ZipFile(
        OUTPUT,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for path in files:
            relative = PurePosixPath(NAME) / PurePosixPath(
                path.relative_to(SOURCE).as_posix()
            )
            info = zipfile.ZipInfo(str(relative), FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    print(f"Built {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
