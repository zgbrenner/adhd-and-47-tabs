#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
NAME = "adhd-and-47-tabs"
SKILL_DIR = ROOT / NAME
SKILL = SKILL_DIR / "SKILL.md"
VERSION_FILE = ROOT / "VERSION"
EVAL_CASES = ROOT / "evals" / "cases.json"
OLD_REPOSITORY = "zgbrenner/i-have-adhd-and-47-tabs"
OLD_ASSET = "i-have-adhd-and-47-tabs.zip"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_json_without_duplicate_keys(path: Path) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate key {key!r}")
            result[key] = value
        return result

    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def main() -> None:
    skill_dirs = sorted(
        path for path in ROOT.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()
    )
    if skill_dirs != [SKILL_DIR]:
        found = ", ".join(str(path.relative_to(ROOT)) for path in skill_dirs) or "none"
        fail(f"expected exactly one top-level skill folder named {NAME}; found: {found}")
    if not SKILL.is_file():
        fail(f"missing {SKILL.relative_to(ROOT)}")
    if not VERSION_FILE.is_file():
        fail("missing VERSION")

    version = VERSION_FILE.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail("VERSION must contain a semantic version such as 2.0.0")

    text = SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        fail("SKILL.md frontmatter is not closed")
    frontmatter = parts[1]

    name_match = re.search(r"(?m)^name:\s*(.+?)\s*$", frontmatter)
    description_match = re.search(r"(?m)^description:\s*(.+?)\s*$", frontmatter)
    compatibility_match = re.search(r"(?m)^compatibility:\s*(.+?)\s*$", frontmatter)
    version_match = re.search(r'(?m)^\s+version:\s*["\']?([^"\'\s]+)["\']?\s*$', frontmatter)

    if not name_match:
        fail("frontmatter name is required")
    name = name_match.group(1).strip()
    if name != NAME:
        fail(f"frontmatter name must be {NAME}")
    if len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        fail("frontmatter name must be 1-64 lowercase letters, numbers, or hyphens")

    if not description_match:
        fail("frontmatter description is required")
    description = description_match.group(1).strip()
    if not description.startswith("Use when"):
        fail("frontmatter description must begin with 'Use when'")
    if len(description) > 1024:
        fail("frontmatter description must be 1024 characters or fewer")

    if compatibility_match and len(compatibility_match.group(1).strip()) > 500:
        fail("frontmatter compatibility must be 500 characters or fewer")

    if not version_match or version_match.group(1) != version:
        found = version_match.group(1) if version_match else "missing"
        fail(f"SKILL.md metadata version must match VERSION ({version}); found: {found}")

    if len(text.splitlines()) > 500:
        fail("SKILL.md exceeds the recommended 500-line loading budget")
    if "TODO" in text or "TBD" in text:
        fail("SKILL.md contains an unfinished TODO or TBD marker")

    required_body_signals = [
        "lower cognitive load, not minimum word count",
        "Answer contract",
        "Action contract",
        "Artifact contract",
        "Project-update contract",
        "Do not force a next step",
        "High-stakes questions",
        "Emotional support",
        "Creative work",
        "definition of done",
    ]
    for signal in required_body_signals:
        if signal.casefold() not in text.casefold():
            fail(f"SKILL.md is missing required behavior signal: {signal}")

    required_files = [
        SKILL_DIR / "references" / "examples.md",
        SKILL_DIR / "LICENSE",
        SKILL_DIR / "NOTICE.md",
        SKILL_DIR / "README.md",
        EVAL_CASES,
        ROOT / "scripts" / "score_responses.py",
        ROOT / "docs" / "EVALUATION.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required_files if not path.is_file()]
    if missing:
        fail(f"missing supporting files: {', '.join(missing)}")

    if "references/examples.md" not in text:
        fail("SKILL.md must link to references/examples.md")
    if "https://github.com/ayghri/i-have-adhd" not in text:
        fail("SKILL.md must retain upstream attribution")

    cases = parse_json_without_duplicate_keys(EVAL_CASES)
    if not isinstance(cases, list) or len(cases) < 12:
        fail("evals/cases.json must contain at least 12 cases")
    case_ids: set[str] = set()
    categories: set[str] = set()
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            fail(f"evaluation case {index} must be an object")
        case_id = case.get("id")
        category = case.get("category")
        prompt = case.get("prompt")
        expectations = case.get("expectations")
        if not isinstance(case_id, str) or not case_id.strip():
            fail(f"evaluation case {index} has no valid id")
        if case_id in case_ids:
            fail(f"duplicate evaluation case id: {case_id}")
        case_ids.add(case_id)
        if not isinstance(category, str) or not category.strip():
            fail(f"evaluation case {case_id} has no category")
        categories.add(category)
        if not isinstance(prompt, str) or not prompt.strip():
            fail(f"evaluation case {case_id} has no prompt")
        if not isinstance(expectations, dict):
            fail(f"evaluation case {case_id} expectations must be an object")

    required_categories = {
        "answer",
        "action",
        "artifact",
        "project-update",
        "high-stakes",
        "creative",
        "emotional-support",
        "troubleshooting",
    }
    missing_categories = sorted(required_categories - categories)
    if missing_categories:
        fail(f"evaluation suite is missing categories: {', '.join(missing_categories)}")

    canonical_surfaces = [
        ROOT / "README.md",
        ROOT / "PUBLISH.md",
        ROOT / "CITATION.cff",
        ROOT / "CONTRIBUTING.md",
        ROOT / "SECURITY.md",
        ROOT / "SUPPORT.md",
        ROOT / "chatgpt-custom-gpt" / "INSTRUCTIONS.md",
        ROOT / "docs" / "DIRECTORY_SUBMISSIONS.md",
        ROOT / "docs" / "DISCUSSION_SEEDS.md",
        ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml",
        ROOT / "scripts" / "build_zip.py",
        ROOT / "scripts" / "create_release.sh",
        ROOT / "scripts" / "publish_to_github.sh",
        SKILL,
        SKILL_DIR / "README.md",
    ]
    for path in canonical_surfaces:
        if not path.is_file():
            fail(f"missing canonical surface: {path.relative_to(ROOT)}")
        surface = path.read_text(encoding="utf-8")
        if OLD_REPOSITORY in surface:
            fail(f"stale repository name in {path.relative_to(ROOT)}")
        if OLD_ASSET in surface:
            fail(f"stale release asset name in {path.relative_to(ROOT)}")

    print(f"OK: {NAME} source package v{version} is valid")


if __name__ == "__main__":
    main()
