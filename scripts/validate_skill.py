#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
NAME = "adhd-and-47-tabs"
VERSION = "3.0.1"
RELEASE_DATE = "2026-08-31"
SITE_URL = "https://zgbrenner.github.io/adhd-and-47-tabs/"
SKILL_DIR = ROOT / NAME
SKILL = SKILL_DIR / "SKILL.md"
VERSION_FILE = ROOT / "VERSION"
EVAL_CASES = ROOT / "evals" / "cases.json"

REQUIRED_SKILL_SIGNALS = {
    "lower cognitive load, not minimum word count",
    "Answer contract",
    "Action contract",
    "Artifact contract",
    "Project-update contract",
    "Friction modifier",
    "Reorientation modifier",
    "Memory-offload modifier",
    "Decision modifier",
    "Recovery modifier",
    "Finish modifier",
    "You are here:",
    "Working-set protocol",
    "one thing",
    "map it",
    "resume",
    "park that",
    "Do not force a next step",
    "High-stakes questions",
    "Emotional support",
    "Creative work",
    "definition of done",
}
REQUIRED_CONTROLS = {
    "one thing",
    "map it",
    "resume",
    "park that",
    "more detail",
    "less detail",
    "why this",
    "normal mode",
    "stop 47-tabs mode",
}
REQUIRED_CATEGORIES = {
    "answer",
    "action",
    "artifact",
    "project-update",
    "decision",
    "reorientation",
    "memory-offload",
    "recovery",
    "finish",
    "troubleshooting",
    "time",
    "high-stakes",
    "emotional-support",
    "creative",
    "control",
}
RESEARCH_SOURCES = {
    "w3.org",
    "agentskills.io",
    "github.com/ayghri/i-have-adhd",
    "github.com/Leantime/leantime",
    "github.com/GothenburgBitFactory/taskwarrior",
    "github.com/super-productivity/super-productivity",
    "github.com/ActivityWatch/activitywatch",
    "github.com/gastownhall/beads",
    "github.com/ravila4/claude-adhd-skills",
    "github.com/promptfoo/promptfoo",
    "github.com/openai/evals",
    "github.com/UKGovernmentBEIS/inspect_ai",
    "developers.openai.com/codex/skills",
    "github.com/vercel-labs/skills",
    "skills.sh/docs/cli",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_file(path: Path) -> None:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")


def load_score_module() -> Any:
    path = ROOT / "scripts" / "score_responses.py"
    require_file(path)
    spec = importlib.util.spec_from_file_location("score_responses", path)
    if not spec or not spec.loader:
        fail("cannot load scripts/score_responses.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def frontmatter_value(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", frontmatter)
    if not match:
        return None
    return match.group(1).strip().strip("\"'")


def metadata_value(frontmatter: str, key: str) -> str | None:
    match = re.search(
        rf"(?m)^\s{{2}}{re.escape(key)}:\s*[\"']?([^\"'\n]+?)[\"']?\s*$",
        frontmatter,
    )
    return match.group(1).strip() if match else None


def check_no_placeholders(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if re.search(r"\b(?:TODO|TBD|FIXME)\b", text):
        fail(f"{path.relative_to(ROOT)} contains an unfinished placeholder")


def skill_reference_path(reference: str) -> Path:
    relative = PurePosixPath(reference)
    if (
        relative.is_absolute()
        or len(relative.parts) != 2
        or relative.parts[0] != "references"
        or any(part in {"", ".", ".."} for part in relative.parts)
    ):
        raise ValueError(f"invalid one-level skill reference: {reference}")
    return SKILL_DIR.joinpath(*relative.parts)


def main() -> None:
    skill_dirs = sorted(
        path for path in ROOT.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()
    )
    if skill_dirs != [SKILL_DIR]:
        found = ", ".join(str(path.relative_to(ROOT)) for path in skill_dirs) or "none"
        fail(f"expected exactly one top-level skill folder named {NAME}; found: {found}")

    required_files = [
        SKILL,
        VERSION_FILE,
        SKILL_DIR / "references" / "interaction-patterns.md",
        SKILL_DIR / "references" / "examples.md",
        SKILL_DIR / "references" / "quick-reference.md",
        SKILL_DIR / "agents" / "openai.yaml",
        SKILL_DIR / "LICENSE",
        SKILL_DIR / "NOTICE.md",
        SKILL_DIR / "README.md",
        EVAL_CASES,
        ROOT / "README.md",
        ROOT / "CHANGELOG.md",
        ROOT / "NOTICE.md",
        ROOT / "CITATION.cff",
        ROOT / "CONTRIBUTING.md",
        ROOT / "PUBLISH.md",
        ROOT / "SECURITY.md",
        ROOT / "SUPPORT.md",
        ROOT / "docs" / "EVALUATION.md",
        ROOT / "docs" / "RESEARCH.md",
        ROOT / "docs" / "DIRECTORY_SUBMISSIONS.md",
        ROOT / "docs" / "releases" / "3.0.0.md",
        ROOT / "docs" / "superpowers" / "specs" / "2026-08-04-adaptive-cognitive-load-v3-design.md",
        ROOT / "docs" / "superpowers" / "plans" / "2026-08-04-adaptive-cognitive-load-v3.md",
        ROOT / "chatgpt-custom-gpt" / "INSTRUCTIONS.md",
        ROOT / "scripts" / "build_zip.py",
        ROOT / "scripts" / "score_responses.py",
        ROOT / "scripts" / "test_repository.py",
        ROOT / "scripts" / "test_score_responses.py",
        ROOT / "scripts" / "test_validate_skill.py",
        ROOT / "scripts" / "prepare_release.py",
        ROOT / "dist" / ".gitkeep",
        ROOT / "index.html",
        ROOT / "robots.txt",
        ROOT / "sitemap.xml",
        ROOT / ".nojekyll",
    ]
    for path in required_files:
        require_file(path)

    if (ROOT / "i-have-adhd-and-47-tabs").exists():
        fail("retired v1 skill folder must not exist")
    if (ROOT / "scripts" / "create_release.sh").exists():
        fail("retired remote release script must not exist")
    if (ROOT / "scripts" / "publish_to_github.sh").exists():
        fail("retired repository publishing script must not exist")
    workflows = ROOT / ".github" / "workflows"
    if workflows.exists() and any(path.is_file() for path in workflows.rglob("*")):
        fail("hosted GitHub Actions workflows are not allowed")

    version = VERSION_FILE.read_text(encoding="utf-8").strip()
    if version != VERSION:
        fail(f"VERSION must equal {VERSION}; found {version!r}")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail("VERSION must contain a semantic version")

    text = SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        fail("SKILL.md frontmatter is not closed")
    frontmatter = parts[1]

    if frontmatter_value(frontmatter, "name") != NAME:
        fail(f"frontmatter name must be {NAME}")
    if len(NAME) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", NAME):
        fail("frontmatter name must be 1-64 lowercase letters, numbers, or hyphens")

    description = frontmatter_value(frontmatter, "description")
    if not description:
        fail("frontmatter description is required")
    if not description.startswith("Use when"):
        fail("frontmatter description must begin with 'Use when'")
    if len(description) > 1024:
        fail("frontmatter description must be 1024 characters or fewer")

    compatibility = frontmatter_value(frontmatter, "compatibility")
    if compatibility and len(compatibility) > 500:
        fail("frontmatter compatibility must be 500 characters or fewer")
    if metadata_value(frontmatter, "version") != version:
        fail("SKILL.md metadata version must match VERSION")
    if len(text.splitlines()) > 500:
        fail("SKILL.md exceeds the recommended 500-line loading budget")
    check_no_placeholders(SKILL)

    lowered_skill = text.casefold()
    for signal in sorted(REQUIRED_SKILL_SIGNALS):
        if signal.casefold() not in lowered_skill:
            fail(f"SKILL.md is missing required behavior signal: {signal}")

    references = set(
        re.findall(r"\]\((references/[^)#?]+\.md)(?:#[^)]+)?\)", text)
    )
    expected_refs = {
        "references/interaction-patterns.md",
        "references/examples.md",
        "references/quick-reference.md",
    }
    if references != expected_refs:
        fail(
            "SKILL.md reference links must equal "
            + ", ".join(sorted(expected_refs))
            + f"; found {', '.join(sorted(references))}"
        )
    for reference in references:
        try:
            reference_path = skill_reference_path(reference)
        except ValueError as exc:
            fail(str(exc))
        require_file(reference_path)

    if "https://github.com/ayghri/i-have-adhd" not in text:
        fail("SKILL.md must retain upstream attribution")

    score_module = load_score_module()
    try:
        suite = score_module.load_suite(EVAL_CASES)
    except Exception as exc:
        fail(f"invalid evaluation suite: {exc}")

    if suite["suite"]["slug"] != NAME:
        fail("evaluation suite slug must match the skill")
    if suite["suite"]["version"] != version:
        fail("evaluation suite version must match VERSION")
    cases = suite["cases"]
    if len(cases) < 47:
        fail("evals/cases.json must contain at least 47 cases")
    categories = {case["category"] for case in cases}
    missing_categories = sorted(REQUIRED_CATEGORIES - categories)
    if missing_categories:
        fail(f"evaluation suite is missing categories: {', '.join(missing_categories)}")
    multi_turn = sum(1 for case in cases if "conversation" in case)
    if multi_turn < 9:
        fail("evaluation suite must contain at least 9 multi-turn cases")
    if len({case["id"] for case in cases}) != len(cases):
        fail("evaluation ids are not unique")

    custom = (ROOT / "chatgpt-custom-gpt" / "INSTRUCTIONS.md").read_text(
        encoding="utf-8"
    )
    quick = (SKILL_DIR / "references" / "quick-reference.md").read_text(
        encoding="utf-8"
    )
    for control in sorted(REQUIRED_CONTROLS):
        for label, surface in (("SKILL.md", text), ("quick reference", quick), ("Custom GPT", custom)):
            if control.casefold() not in surface.casefold():
                fail(f"{label} is missing control phrase: {control}")

    openai_metadata = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    for signal in (
        'display_name: "ADHD & 47 Tabs"',
        'allow_implicit_invocation: true',
        'default_prompt:',
    ):
        if signal not in openai_metadata:
            fail(f"agents/openai.yaml is missing: {signal}")
    check_no_placeholders(SKILL_DIR / "agents" / "openai.yaml")

    research = (ROOT / "docs" / "RESEARCH.md").read_text(encoding="utf-8")
    for source in sorted(RESEARCH_SOURCES):
        if source.casefold() not in research.casefold():
            fail(f"docs/RESEARCH.md is missing source: {source}")

    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    if f"version: {version}" not in citation and f'version: "{version}"' not in citation:
        fail("CITATION.cff version must match VERSION")
    if f"date-released: {RELEASE_DATE}" not in citation:
        fail(f"CITATION.cff release date must be {RELEASE_DATE}")

    release_notes = (ROOT / "docs" / "releases" / f"{version}.md").read_text(
        encoding="utf-8"
    )
    if f"v{version}" not in release_notes:
        fail(f"release notes must identify v{version}")

    canonical_surfaces = [
        ROOT / "README.md",
        ROOT / "NOTICE.md",
        ROOT / "PUBLISH.md",
        ROOT / "CITATION.cff",
        ROOT / "CONTRIBUTING.md",
        ROOT / "SECURITY.md",
        ROOT / "SUPPORT.md",
        ROOT / "chatgpt-custom-gpt" / "INSTRUCTIONS.md",
        ROOT / "docs" / "DIRECTORY_SUBMISSIONS.md",
        ROOT / "docs" / "INSTALL.md",
        ROOT / "scripts" / "build_zip.py",
        ROOT / "scripts" / "test_repository.py",
        ROOT / "scripts" / "prepare_release.py",
        ROOT / "scripts" / "install_git_hooks.sh",
        ROOT / ".githooks" / "pre-push",
        ROOT / "index.html",
        SKILL,
        SKILL_DIR / "README.md",
    ]
    old_repository = "zgbrenner/i-have-adhd-and-47-tabs"
    old_asset = "i-have-adhd-and-47-tabs.zip"
    for path in canonical_surfaces:
        surface = path.read_text(encoding="utf-8")
        if old_repository in surface:
            fail(f"stale repository name in {path.relative_to(ROOT)}")
        if old_asset in surface:
            fail(f"stale package name in {path.relative_to(ROOT)}")
        check_no_placeholders(path)

    site = (ROOT / "index.html").read_text(encoding="utf-8")
    if version not in site:
        fail(f"index.html must state the current version {version}")
    if f'"softwareVersion": "{version}"' not in site:
        fail("index.html structured data must carry the current softwareVersion")
    if SITE_URL not in site:
        fail(f"index.html must set the canonical site URL {SITE_URL}")
    for required_tag in ('rel="canonical"', 'property="og:image"', 'application/ld+json'):
        if required_tag not in site:
            fail(f"index.html is missing required metadata: {required_tag}")
    if SITE_URL not in (ROOT / "sitemap.xml").read_text(encoding="utf-8"):
        fail(f"sitemap.xml must list {SITE_URL}")
    if SITE_URL not in (ROOT / "robots.txt").read_text(encoding="utf-8"):
        fail("robots.txt must point at the sitemap")

    print(
        f"OK: {NAME} source package v{version} is valid "
        f"({len(cases)} eval cases; {multi_turn} multi-turn)"
    )


if __name__ == "__main__":
    main()
