#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import os
import stat
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
NAME = "adhd-and-47-tabs"
SOURCE = ROOT / NAME
DIST = ROOT / "dist"
OUTPUT = DIST / f"{NAME}.zip"
CHECKSUMS = DIST / "SHA256SUMS"
FIXED_TIME = (2026, 8, 4, 0, 0, 0)
EXCLUDED_DIRS = {".git", "__pycache__"}
EXCLUDED_NAMES = {".DS_Store"}
ALLOWED_SUFFIXES = {".md", ".yaml"}
ALLOWED_FILENAMES = {"LICENSE"}


def source_files() -> list[Path]:
    files: list[Path] = []
    for path in SOURCE.rglob("*"):
        relative = path.relative_to(SOURCE)
        if any(part in EXCLUDED_DIRS or part.startswith(".") for part in relative.parts):
            continue
        if path.name in EXCLUDED_NAMES or path.name.endswith(("~", ".pyc", ".pyo")):
            continue
        if path.is_symlink():
            raise SystemExit(f"ERROR: symlink is not allowed in skill package: {relative}")
        if not path.is_file():
            continue
        if path.name not in ALLOWED_FILENAMES and path.suffix.lower() not in ALLOWED_SUFFIXES:
            raise SystemExit(f"ERROR: unexpected package file type: {relative}")
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(SOURCE).as_posix())


def archive_name(path: Path) -> str:
    relative = PurePosixPath(path.relative_to(SOURCE).as_posix())
    return str(PurePosixPath(NAME) / relative)


def write_archive(target: Path) -> None:
    with zipfile.ZipFile(
        target,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        strict_timestamps=True,
    ) as archive:
        for path in source_files():
            info = zipfile.ZipInfo(archive_name(path), date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.flag_bits |= 0x800  # UTF-8 names
            archive.writestr(
                info,
                path.read_bytes(),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )


def main() -> None:
    if not SOURCE.is_dir():
        raise SystemExit(f"ERROR: missing source directory: {SOURCE}")
    DIST.mkdir(parents=True, exist_ok=True)
    temporary = OUTPUT.with_suffix(".zip.tmp")
    if temporary.exists():
        temporary.unlink()

    write_archive(temporary)
    os.replace(temporary, OUTPUT)

    digest = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    checksum_text = f"{digest}  {OUTPUT.name}\n"
    temporary_checksum = CHECKSUMS.with_suffix(".tmp")
    temporary_checksum.write_text(checksum_text, encoding="utf-8", newline="\n")
    os.replace(temporary_checksum, CHECKSUMS)

    print(
        f"Built {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size:,} bytes)\n"
        f"SHA-256: {digest}"
    )


if __name__ == "__main__":
    main()
