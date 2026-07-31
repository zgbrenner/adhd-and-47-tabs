#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORER = ROOT / "scripts" / "score_responses.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ERROR: {message}")


def run(cases: Path, responses: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCORER),
            "--cases",
            str(cases),
            "--responses",
            str(responses),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> None:
    cases_data = [
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
    good_data = [
        {"id": "answer", "response": "**4.**"},
        {
            "id": "action",
            "response": "Open the form.\n\n1. Enter your name.\n2. Add the deadline.\n\nNext: open the form.",
        },
    ]
    bad_data = [
        {
            "id": "answer",
            "response": "Great question! The answer is 4.\n\nNext: ask another question.",
        },
        {"id": "action", "response": "There are several ways to approach this."},
    ]

    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary)
        cases = directory / "cases.json"
        good = directory / "good.jsonl"
        bad = directory / "bad.jsonl"
        duplicate = directory / "duplicate.jsonl"

        cases.write_text(json.dumps(cases_data), encoding="utf-8")
        good.write_text(
            "\n".join(json.dumps(row) for row in good_data) + "\n",
            encoding="utf-8",
        )
        bad.write_text(
            "\n".join(json.dumps(row) for row in bad_data) + "\n",
            encoding="utf-8",
        )
        duplicate.write_text(
            json.dumps(good_data[0]) + "\n" + json.dumps(good_data[0]) + "\n",
            encoding="utf-8",
        )

        good_result = run(cases, good)
        require(good_result.returncode == 0, good_result.stdout + good_result.stderr)
        require("2/2 cases passed" in good_result.stdout, "good fixture did not fully pass")

        bad_result = run(cases, bad)
        require(bad_result.returncode == 1, bad_result.stdout + bad_result.stderr)
        require("0/2 cases passed" in bad_result.stdout, "bad fixture did not fully fail")

        duplicate_result = run(cases, duplicate)
        require(duplicate_result.returncode == 2, duplicate_result.stdout + duplicate_result.stderr)
        require("Duplicate response id" in duplicate_result.stderr, "duplicate response was not rejected")

    print("OK: response scorer regression tests passed")


if __name__ == "__main__":
    main()
