#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_skill.py"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_skill", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load validate_skill")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidateSkillTests(unittest.TestCase):
    def test_reference_path_stays_inside_references_directory(self) -> None:
        module = load_module()
        self.assertEqual(
            module.skill_reference_path("references/examples.md"),
            ROOT / "adhd-and-47-tabs" / "references" / "examples.md",
        )

    def test_reference_path_rejects_nested_or_escaping_paths(self) -> None:
        module = load_module()
        for value in ("references/nested/examples.md", "references/../SKILL.md", "/tmp/x.md"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    module.skill_reference_path(value)


if __name__ == "__main__":
    unittest.main(verbosity=2)
