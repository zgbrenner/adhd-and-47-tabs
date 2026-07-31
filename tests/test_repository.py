from __future__ import annotations

import json
import re
import struct
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "adhd-and-47-tabs"
SKILL_DIR = ROOT / SKILL_NAME
DIST_ZIP = ROOT / "dist" / f"{SKILL_NAME}.zip"
SOCIAL_PREVIEW = ROOT / "assets" / "social-preview.png"
OLD_REPOSITORY = "zgbrenner/i-have-adhd-and-47-tabs"
OLD_ASSET = "i-have-adhd-and-47-tabs.zip"


class RepositoryContractTests(unittest.TestCase):
    def test_required_repository_files_exist(self) -> None:
        required = [
            ROOT / "README.md",
            ROOT / "LICENSE",
            ROOT / "NOTICE.md",
            ROOT / "CONTRIBUTING.md",
            ROOT / "CODE_OF_CONDUCT.md",
            ROOT / "SECURITY.md",
            ROOT / "SUPPORT.md",
            ROOT / "CHANGELOG.md",
            ROOT / "CITATION.cff",
            ROOT / "PUBLISH.md",
            ROOT / "VERSION",
            ROOT / "Makefile",
            ROOT / "docs" / "DIRECTORY_SUBMISSIONS.md",
            ROOT / "docs" / "DISCUSSION_SEEDS.md",
            ROOT / "docs" / "EVALUATION.md",
            ROOT / "evals" / "cases.json",
            ROOT / "scripts" / "score_responses.py",
            ROOT / "scripts" / "publish_to_github.sh",
            ROOT / "scripts" / "create_release.sh",
            ROOT / "scripts" / "install_git_hooks.sh",
            ROOT / ".githooks" / "pre-push",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "bug.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "behavior-improvement.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "platform-compatibility.yml",
            ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml",
            ROOT / ".github" / "DISCUSSION_TEMPLATE" / "ideas.yml",
            ROOT / ".github" / "DISCUSSION_TEMPLATE" / "q-a.yml",
            ROOT / ".github" / "DISCUSSION_TEMPLATE" / "show-and-tell.yml",
            SOCIAL_PREVIEW,
            SKILL_DIR / "SKILL.md",
            SKILL_DIR / "README.md",
            SKILL_DIR / "LICENSE",
            SKILL_DIR / "NOTICE.md",
            SKILL_DIR / "references" / "examples.md",
        ]
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual(missing, [], f"Missing required files: {missing}")
        self.assertFalse((ROOT / "i-have-adhd-and-47-tabs").exists())
        self.assertFalse((SKILL_DIR / "agents" / "openai.yaml").exists())
        self.assertFalse((ROOT / f"{SKILL_NAME}.zip").exists(), "Only dist/ may contain a ZIP")

    def test_no_hosted_ci_or_actions_configuration(self) -> None:
        workflows = ROOT / ".github" / "workflows"
        workflow_files = (
            list(workflows.glob("*.yml")) + list(workflows.glob("*.yaml"))
            if workflows.exists()
            else []
        )
        self.assertEqual(workflow_files, [], "Repository must not use GitHub Actions")
        self.assertFalse((ROOT / ".github" / "dependabot.yml").exists())
        self.assertFalse((ROOT / ".github" / "dependabot.yaml").exists())

    def test_versions_are_synchronized(self) -> None:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version, "2.0.0")
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn(f'version: "{version}"', skill)
        self.assertIn(f"version: {version}", citation)
        self.assertIn(f"## {version}", changelog)
        self.assertTrue((ROOT / "docs" / "releases" / f"{version}.md").is_file())

    def test_skill_frontmatter_follows_agent_skills_contract(self) -> None:
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        self.assertRegex(text, rf"(?m)^name: {re.escape(SKILL_NAME)}$")
        description = re.search(r"(?m)^description:\s*(.+)$", text)
        self.assertIsNotNone(description)
        assert description is not None
        value = description.group(1).strip()
        self.assertGreater(len(value), 20)
        self.assertLessEqual(len(value), 1024)
        self.assertTrue(value.startswith("Use when"))
        self.assertRegex(SKILL_NAME, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertLessEqual(len(SKILL_NAME), 64)
        compatibility = re.search(r"(?m)^compatibility:\s*(.+)$", text)
        if compatibility:
            self.assertLessEqual(len(compatibility.group(1).strip()), 500)
        self.assertIn("https://github.com/ayghri/i-have-adhd", text)

    def test_skill_optimizes_cognitive_load_without_forcing_brevity(self) -> None:
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").lower()
        for required in [
            "cognitive load",
            "not minimum word count",
            "answer contract",
            "action contract",
            "artifact contract",
            "project-update contract",
            "do not force a next step",
            "emotional support",
            "high-stakes",
            "creative",
            "definition of done",
        ]:
            self.assertIn(required, text)

    def test_primary_surfaces_use_canonical_identity(self) -> None:
        paths = [
            ROOT / "README.md",
            ROOT / "PUBLISH.md",
            ROOT / "CITATION.cff",
            ROOT / "chatgpt-custom-gpt" / "INSTRUCTIONS.md",
            ROOT / "scripts" / "validate_skill.py",
            ROOT / "scripts" / "build_zip.py",
            ROOT / "scripts" / "create_release.sh",
            ROOT / "scripts" / "publish_to_github.sh",
            SKILL_DIR / "SKILL.md",
            SKILL_DIR / "README.md",
        ]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(OLD_REPOSITORY, text, str(path.relative_to(ROOT)))
            self.assertNotIn(OLD_ASSET, text, str(path.relative_to(ROOT)))
        self.assertIn("zgbrenner/adhd-and-47-tabs", (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_readme_documents_current_installation_and_validation_paths(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for required in [
            "Claude",
            "ChatGPT",
            "Codex",
            "GitHub Copilot",
            "gh skill install",
            "gh skill publish --dry-run",
            "npx skills add",
            "make check",
            "make install-hooks",
            "no GitHub Actions or hosted CI",
            "not a medical tool",
        ]:
            self.assertIn(required, text)
        self.assertNotIn("actions/workflows", text)

    def test_license_preserves_original_notice(self) -> None:
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Ayoub Ghriss", text)
        self.assertIn("Copyright (c) 2026 Zachary Brenner", text)
        self.assertIn("MIT License", text)

    def test_security_and_support_routes_are_explicit(self) -> None:
        security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        support = (ROOT / "SUPPORT.md").read_text(encoding="utf-8")
        self.assertIn("security/advisories/new", security)
        self.assertIn("Private vulnerability reporting", security)
        self.assertIn("Discussions", support)
        self.assertIn("medical", support.lower())

    def test_evaluation_suite_covers_core_response_modes_and_exceptions(self) -> None:
        cases = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
        self.assertIsInstance(cases, list)
        self.assertGreaterEqual(len(cases), 12)
        ids = [case["id"] for case in cases]
        self.assertEqual(len(ids), len(set(ids)))
        categories = {case["category"] for case in cases}
        self.assertTrue(
            {
                "answer",
                "action",
                "artifact",
                "project-update",
                "high-stakes",
                "creative",
                "emotional-support",
                "troubleshooting",
            }.issubset(categories)
        )
        for case in cases:
            self.assertTrue(case["prompt"].strip())
            self.assertIsInstance(case["expectations"], dict)

    def test_response_scorer_accepts_good_output_and_rejects_bad_output(self) -> None:
        cases = [
            {
                "id": "answer",
                "category": "answer",
                "prompt": "What is two plus two?",
                "expectations": {
                    "forbid_generic_opener": True,
                    "forbid_next_step": True,
                    "required_substrings": ["4"],
                },
            },
            {
                "id": "action",
                "category": "action",
                "prompt": "Help me start the form.",
                "expectations": {
                    "forbid_generic_opener": True,
                    "require_next_step": True,
                    "max_numbered_steps": 3,
                },
            },
        ]
        good = [
            {"id": "answer", "response": "**4.**"},
            {
                "id": "action",
                "response": "Open the form.\n\n1. Enter your name.\n2. Add the deadline.\n\nNext: open the form.",
            },
        ]
        bad = [
            {"id": "answer", "response": "Great question! The answer is 4. Next: ask another question."},
            {"id": "action", "response": "There are several ways to approach this."},
        ]
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            cases_path = directory / "cases.json"
            good_path = directory / "good.jsonl"
            bad_path = directory / "bad.jsonl"
            cases_path.write_text(json.dumps(cases), encoding="utf-8")
            good_path.write_text("\n".join(json.dumps(row) for row in good) + "\n", encoding="utf-8")
            bad_path.write_text("\n".join(json.dumps(row) for row in bad) + "\n", encoding="utf-8")

            good_result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "score_responses.py"),
                    "--cases",
                    str(cases_path),
                    "--responses",
                    str(good_path),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(good_result.returncode, 0, good_result.stdout + good_result.stderr)
            self.assertIn("2/2 cases passed", good_result.stdout)

            bad_result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "score_responses.py"),
                    "--cases",
                    str(cases_path),
                    "--responses",
                    str(bad_path),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(bad_result.returncode, 0)
            self.assertIn("0/2 cases passed", bad_result.stdout)

    def test_issue_and_discussion_forms_are_structured(self) -> None:
        bug = (ROOT / ".github" / "ISSUE_TEMPLATE" / "bug.yml").read_text(encoding="utf-8")
        discussion = (ROOT / ".github" / "DISCUSSION_TEMPLATE" / "q-a.yml").read_text(encoding="utf-8")
        self.assertIn("type: dropdown", bug)
        self.assertIn("required: true", bug)
        self.assertIn("type: textarea", discussion)

    def test_local_release_script_publishes_versioned_assets(self) -> None:
        text = (ROOT / "scripts" / "create_release.sh").read_text(encoding="utf-8")
        self.assertIn("make check", text)
        self.assertIn("hashlib.sha256", text)
        self.assertIn("gh release create", text)
        self.assertIn("gh release upload", text)
        self.assertIn("dist/adhd-and-47-tabs.zip", text)
        self.assertIn("dist/SHA256SUMS", text)
        self.assertIn('CURRENT_BRANCH="$(git branch --show-current)"', text)
        self.assertIn('REPO="zgbrenner/adhd-and-47-tabs"', text)

    def test_local_hook_runs_repository_checks(self) -> None:
        hook = (ROOT / ".githooks" / "pre-push").read_text(encoding="utf-8")
        installer = (ROOT / "scripts" / "install_git_hooks.sh").read_text(encoding="utf-8")
        self.assertIn("make check", hook)
        self.assertIn("core.hooksPath .githooks", installer)

    def test_social_preview_has_recommended_dimensions(self) -> None:
        data = SOCIAL_PREVIEW.read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", data[16:24])
        self.assertEqual((width, height), (1280, 640))

    def test_distribution_zip_has_one_top_level_skill_folder(self) -> None:
        self.assertTrue(DIST_ZIP.is_file(), f"Missing {DIST_ZIP.relative_to(ROOT)}")
        with zipfile.ZipFile(DIST_ZIP) as archive:
            self.assertIsNone(archive.testzip())
            names = [name for name in archive.namelist() if name and not name.endswith("/")]
        self.assertEqual({name.split("/", 1)[0] for name in names}, {SKILL_NAME})
        self.assertIn(f"{SKILL_NAME}/SKILL.md", names)
        self.assertNotIn("__MACOSX", "\n".join(names))

    def test_build_ignores_common_stray_files(self) -> None:
        ds_store = SKILL_DIR / ".DS_Store"
        cache_dir = SKILL_DIR / "__pycache__"
        cache_file = cache_dir / "junk.pyc"
        backup = SKILL_DIR / "notes.md~"
        cache_dir.mkdir(exist_ok=True)
        ds_store.write_bytes(b"junk")
        cache_file.write_bytes(b"junk")
        backup.write_text("junk", encoding="utf-8")
        try:
            subprocess.run([sys.executable, str(ROOT / "scripts" / "build_zip.py")], check=True, cwd=ROOT)
            with zipfile.ZipFile(DIST_ZIP) as archive:
                names = set(archive.namelist())
            self.assertNotIn(f"{SKILL_NAME}/.DS_Store", names)
            self.assertNotIn(f"{SKILL_NAME}/__pycache__/junk.pyc", names)
            self.assertNotIn(f"{SKILL_NAME}/notes.md~", names)
        finally:
            ds_store.unlink(missing_ok=True)
            cache_file.unlink(missing_ok=True)
            backup.unlink(missing_ok=True)
            cache_dir.rmdir()


if __name__ == "__main__":
    unittest.main()
