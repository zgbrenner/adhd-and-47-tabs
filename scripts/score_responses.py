#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

GENERIC_OPENERS = re.compile(
    r"""^\s*(?:[#>*_\-\s]*)(?:
        great\s+question\b|
        good\s+question\b|
        sure[!,.]?\b|
        of\s+course[!,.]?\b|
        absolutely[!,.]?\b|
        let\s+me\s+(?:walk|explain|help|think)\b|
        to\s+answer\s+your\s+question\b|
        there\s+are\s+(?:several|a\s+few)\s+(?:ways|things|factors)\b
    )""",
    re.IGNORECASE | re.VERBOSE,
)
NEXT_STEP = re.compile(
    r"(?im)^\s*(?:[-*>]\s*)?(?:\*\*)?next(?:\s+(?:step|active step))?(?:\*\*)?\s*:"
)
NUMBERED_STEP = re.compile(r"(?m)^\s*\d+[.)]\s+\S")
SUPPORTED_EXPECTATIONS = {
    "forbid_generic_opener",
    "require_next_step",
    "forbid_next_step",
    "max_numbered_steps",
    "forbid_numbered_steps",
    "required_substrings",
    "forbidden_substrings",
    "required_any_substrings",
    "first_line_required_substrings",
    "required_regexes",
    "forbidden_regexes",
    "min_words",
    "max_words",
}


class EvaluationError(ValueError):
    pass


def load_cases(path: Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvaluationError(f"Cannot read cases file {path}: {exc}") from exc
    if not isinstance(data, list) or not data:
        raise EvaluationError("Cases file must contain a non-empty JSON array")

    seen: set[str] = set()
    for index, case in enumerate(data, start=1):
        if not isinstance(case, dict):
            raise EvaluationError(f"Case {index} must be an object")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            raise EvaluationError(f"Case {index} has no valid id")
        if case_id in seen:
            raise EvaluationError(f"Duplicate case id: {case_id}")
        seen.add(case_id)
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            raise EvaluationError(f"Case {case_id} has no prompt")
        expectations = case.get("expectations")
        if not isinstance(expectations, dict):
            raise EvaluationError(f"Case {case_id} expectations must be an object")
        unknown = set(expectations) - SUPPORTED_EXPECTATIONS
        if unknown:
            raise EvaluationError(
                f"Case {case_id} uses unsupported expectations: {', '.join(sorted(unknown))}"
            )
    return data


def load_responses(path: Path) -> dict[str, str]:
    responses: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise EvaluationError(f"Cannot read responses file {path}: {exc}") from exc

    for line_number, raw in enumerate(lines, start=1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise EvaluationError(
                f"Invalid JSON on response line {line_number}: {exc.msg}"
            ) from exc
        if not isinstance(row, dict):
            raise EvaluationError(f"Response line {line_number} must be an object")
        case_id = row.get("id")
        response = row.get("response")
        if not isinstance(case_id, str) or not case_id.strip():
            raise EvaluationError(f"Response line {line_number} has no valid id")
        if case_id in responses:
            raise EvaluationError(f"Duplicate response id: {case_id}")
        if not isinstance(response, str) or not response.strip():
            raise EvaluationError(f"Response {case_id} is empty")
        responses[case_id] = response
    return responses


def first_content_line(response: str) -> str:
    for line in response.splitlines():
        cleaned = line.strip()
        if cleaned:
            return cleaned
    return ""


def word_count(response: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", response, flags=re.UNICODE))


def ensure_string_list(value: Any, key: str, case_id: str) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise EvaluationError(f"{case_id}.{key} must be a list of non-empty strings")
    return value


def evaluate_case(case: dict[str, Any], response: str) -> list[str]:
    case_id = case["id"]
    expectations = case["expectations"]
    failures: list[str] = []
    lowered = response.casefold()
    first_line = first_content_line(response).casefold()
    numbered_steps = len(NUMBERED_STEP.findall(response))
    words = word_count(response)

    if expectations.get("forbid_generic_opener") and GENERIC_OPENERS.search(response):
        failures.append("starts with a generic preamble")

    has_next_step = bool(NEXT_STEP.search(response))
    if expectations.get("require_next_step") and not has_next_step:
        failures.append("missing an explicit Next: line")
    if expectations.get("forbid_next_step") and has_next_step:
        failures.append("adds a forced Next: line")

    if expectations.get("forbid_numbered_steps") and numbered_steps:
        failures.append(f"uses {numbered_steps} numbered step(s) when none are expected")

    if "max_numbered_steps" in expectations:
        maximum = expectations["max_numbered_steps"]
        if not isinstance(maximum, int) or maximum < 0:
            raise EvaluationError(
                f"{case_id}.max_numbered_steps must be a non-negative integer"
            )
        if numbered_steps > maximum:
            failures.append(
                f"uses {numbered_steps} numbered steps; maximum is {maximum}"
            )

    if "required_substrings" in expectations:
        for item in ensure_string_list(
            expectations["required_substrings"], "required_substrings", case_id
        ):
            if item.casefold() not in lowered:
                failures.append(f"missing required text: {item!r}")

    if "forbidden_substrings" in expectations:
        for item in ensure_string_list(
            expectations["forbidden_substrings"], "forbidden_substrings", case_id
        ):
            if item.casefold() in lowered:
                failures.append(f"contains forbidden text: {item!r}")

    if "required_any_substrings" in expectations:
        options = ensure_string_list(
            expectations["required_any_substrings"],
            "required_any_substrings",
            case_id,
        )
        if not any(item.casefold() in lowered for item in options):
            failures.append(
                "missing every acceptable term: "
                + ", ".join(repr(item) for item in options)
            )

    if "first_line_required_substrings" in expectations:
        for item in ensure_string_list(
            expectations["first_line_required_substrings"],
            "first_line_required_substrings",
            case_id,
        ):
            if item.casefold() not in first_line:
                failures.append(f"first content line is missing: {item!r}")

    if "required_regexes" in expectations:
        for pattern in ensure_string_list(
            expectations["required_regexes"], "required_regexes", case_id
        ):
            if not re.search(pattern, response, flags=re.IGNORECASE | re.MULTILINE):
                failures.append(f"does not match required regex: {pattern!r}")

    if "forbidden_regexes" in expectations:
        for pattern in ensure_string_list(
            expectations["forbidden_regexes"], "forbidden_regexes", case_id
        ):
            if re.search(pattern, response, flags=re.IGNORECASE | re.MULTILINE):
                failures.append(f"matches forbidden regex: {pattern!r}")

    if "min_words" in expectations:
        minimum = expectations["min_words"]
        if not isinstance(minimum, int) or minimum < 0:
            raise EvaluationError(f"{case_id}.min_words must be a non-negative integer")
        if words < minimum:
            failures.append(f"contains {words} words; minimum is {minimum}")

    if "max_words" in expectations:
        maximum = expectations["max_words"]
        if not isinstance(maximum, int) or maximum < 1:
            raise EvaluationError(f"{case_id}.max_words must be a positive integer")
        if words > maximum:
            failures.append(f"contains {words} words; maximum is {maximum}")

    return failures


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Score ADHD & 47 Tabs response exports against structural expectations."
    )
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "evals" / "cases.json",
        help="JSON case file (default: evals/cases.json)",
    )
    parser.add_argument(
        "--responses",
        type=Path,
        required=True,
        help='JSONL file with {"id": "...", "response": "..."} rows',
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        cases = load_cases(args.cases)
        responses = load_responses(args.responses)
    except EvaluationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    known_ids = {case["id"] for case in cases}
    unknown_ids = sorted(set(responses) - known_ids)
    if unknown_ids:
        print(
            "ERROR: response file contains unknown case ids: " + ", ".join(unknown_ids),
            file=sys.stderr,
        )
        return 2

    passed = 0
    for case in cases:
        case_id = case["id"]
        response = responses.get(case_id)
        if response is None:
            print(f"FAIL {case_id}: missing response")
            continue
        try:
            failures = evaluate_case(case, response)
        except (EvaluationError, re.error) as exc:
            print(f"ERROR {case_id}: {exc}", file=sys.stderr)
            return 2
        if failures:
            print(f"FAIL {case_id}: {'; '.join(failures)}")
        else:
            passed += 1
            print(f"PASS {case_id}")

    total = len(cases)
    print(f"\n{passed}/{total} cases passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
