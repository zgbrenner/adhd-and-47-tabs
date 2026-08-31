#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
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
GENERIC_CLOSERS = re.compile(
    r"""(?ix)
    (?:let\s+me\s+know|hope\s+this\s+helps|feel\s+free|happy\s+to\s+(?:help|clarify)|
       if\s+you\s+want|anything\s+else|reach\s+out\s+if)
    [.!?]*\s*$
    """
)
NEXT_STEP = re.compile(
    r"(?im)^\s*(?:#{1,6}\s*)?(?:[-*>]\s*)?(?:\*\*)?next(?:\s+(?:steps?|active\s+steps?))?(?:\*\*)?\s*:"
)
CODE_FENCE = re.compile(r"(?ms)^[ \t]*(```|~~~).*?(?:^[ \t]*\1[ \t]*$|\Z)")
NUMBERED_STEP = re.compile(r"(?m)^\s*\d+[.)]\s+\S")
BULLET_ITEM = re.compile(r"(?m)^\s*[-*+]\s+\S")
MARKDOWN_HEADING = re.compile(r"(?m)^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
BOLD_LABEL = re.compile(r"(?m)^\s*(?:[-*+]\s+)?\*\*([^*\n]{1,80}?)(?::)?\*\*(?::)?(?:\s|$)")
WORD = re.compile(r"\b[\w'-]+\b", flags=re.UNICODE)

BOOLEAN_EXPECTATIONS = {
    "forbid_generic_opener",
    "forbid_generic_closer",
    "require_next_step",
    "forbid_next_step",
    "forbid_numbered_steps",
}

SUPPORTED_EXPECTATIONS = {
    "forbid_generic_opener",
    "forbid_generic_closer",
    "require_next_step",
    "forbid_next_step",
    "max_numbered_steps",
    "forbid_numbered_steps",
    "max_bullet_items",
    "min_total_list_items",
    "max_total_list_items",
    "max_questions",
    "max_headings",
    "min_paragraphs",
    "max_paragraphs",
    "required_substrings",
    "forbidden_substrings",
    "required_any_substrings",
    "first_line_required_substrings",
    "required_regexes",
    "forbidden_regexes",
    "required_ordered_substrings",
    "required_any_headings",
    "require_first_line_regex",
    "min_words",
    "max_words",
}


class EvaluationError(ValueError):
    """Raised when an evaluation suite or response export is malformed."""


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise EvaluationError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
        )
    except (OSError, json.JSONDecodeError, EvaluationError) as exc:
        raise EvaluationError(f"cannot read JSON file {path}: {exc}") from exc


def ensure_string_list(value: Any, key: str, case_id: str) -> list[str]:
    if not isinstance(value, list) or not value or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        raise EvaluationError(
            f"{case_id}.{key} must be a non-empty list of non-empty strings"
        )
    return value


def _validate_non_negative_int(value: Any, key: str, case_id: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise EvaluationError(f"{case_id}.{key} must be a non-negative integer")
    return value


def _validate_positive_int(value: Any, key: str, case_id: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise EvaluationError(f"{case_id}.{key} must be a positive integer")
    return value


def load_suite(path: Path) -> dict[str, Any]:
    data = load_json(path)
    if not isinstance(data, dict):
        raise EvaluationError("suite must be a JSON object")
    if data.get("schema_version") != 2:
        raise EvaluationError("suite.schema_version must equal 2")

    metadata = data.get("suite")
    if not isinstance(metadata, dict):
        raise EvaluationError("suite.suite must be an object")
    for key in ("name", "slug", "version"):
        if not isinstance(metadata.get(key), str) or not metadata[key].strip():
            raise EvaluationError(f"suite.suite.{key} must be a non-empty string")

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise EvaluationError("suite.cases must be a non-empty array")

    seen: set[str] = set()
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            raise EvaluationError(f"case {index} must be an object")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            raise EvaluationError(f"case {index} has no valid id")
        if case_id in seen:
            raise EvaluationError(f"duplicate case id: {case_id}")
        seen.add(case_id)

        category = case.get("category")
        if not isinstance(category, str) or not category.strip():
            raise EvaluationError(f"case {case_id} has no category")

        has_prompt = "prompt" in case
        has_conversation = "conversation" in case
        if has_prompt == has_conversation:
            raise EvaluationError(
                f"case {case_id} must define exactly one of prompt or conversation"
            )
        if has_prompt:
            prompt = case["prompt"]
            if not isinstance(prompt, str) or not prompt.strip():
                raise EvaluationError(f"case {case_id}.prompt must be a non-empty string")
        else:
            conversation = case["conversation"]
            if not isinstance(conversation, list) or not conversation:
                raise EvaluationError(
                    f"case {case_id}.conversation must be a non-empty array"
                )
            for turn_index, turn in enumerate(conversation, start=1):
                if not isinstance(turn, dict):
                    raise EvaluationError(
                        f"{case_id}.conversation[{turn_index}] must be an object"
                    )
                if turn.get("role") not in {"system", "user", "assistant"}:
                    raise EvaluationError(
                        f"{case_id}.conversation[{turn_index}].role is invalid"
                    )
                if not isinstance(turn.get("content"), str) or not turn["content"].strip():
                    raise EvaluationError(
                        f"{case_id}.conversation[{turn_index}].content is empty"
                    )

        expectations = case.get("expectations")
        if not isinstance(expectations, dict):
            raise EvaluationError(f"case {case_id} expectations must be an object")
        unknown = set(expectations) - SUPPORTED_EXPECTATIONS
        if unknown:
            raise EvaluationError(
                f"case {case_id} uses unsupported expectations: "
                + ", ".join(sorted(unknown))
            )

        for key in BOOLEAN_EXPECTATIONS & set(expectations):
            if not isinstance(expectations[key], bool):
                raise EvaluationError(f"{case_id}.{key} must be a boolean")

        for key in {
            "required_substrings",
            "forbidden_substrings",
            "required_any_substrings",
            "first_line_required_substrings",
            "required_regexes",
            "forbidden_regexes",
            "required_ordered_substrings",
            "required_any_headings",
        } & set(expectations):
            ensure_string_list(expectations[key], key, case_id)

        for key in {
            "max_numbered_steps",
            "max_bullet_items",
            "min_total_list_items",
            "max_total_list_items",
            "max_questions",
            "max_headings",
            "min_paragraphs",
            "max_paragraphs",
            "min_words",
        } & set(expectations):
            _validate_non_negative_int(expectations[key], key, case_id)
        if "max_words" in expectations:
            _validate_positive_int(expectations["max_words"], "max_words", case_id)

        if (
            "min_words" in expectations
            and "max_words" in expectations
            and expectations["min_words"] > expectations["max_words"]
        ):
            raise EvaluationError(f"{case_id}.min_words cannot exceed max_words")

        if (
            "min_total_list_items" in expectations
            and "max_total_list_items" in expectations
            and expectations["min_total_list_items"] > expectations["max_total_list_items"]
        ):
            raise EvaluationError(
                f"{case_id}.min_total_list_items cannot exceed max_total_list_items"
            )

        if (
            "min_paragraphs" in expectations
            and "max_paragraphs" in expectations
            and expectations["min_paragraphs"] > expectations["max_paragraphs"]
        ):
            raise EvaluationError(
                f"{case_id}.min_paragraphs cannot exceed max_paragraphs"
            )

        if "require_first_line_regex" in expectations:
            pattern = expectations["require_first_line_regex"]
            if not isinstance(pattern, str) or not pattern:
                raise EvaluationError(
                    f"{case_id}.require_first_line_regex must be a non-empty string"
                )
            try:
                re.compile(pattern)
            except re.error as exc:
                raise EvaluationError(
                    f"{case_id}.require_first_line_regex is invalid: {exc}"
                ) from exc

        for key in ("required_regexes", "forbidden_regexes"):
            for pattern in expectations.get(key, []):
                try:
                    re.compile(pattern)
                except re.error as exc:
                    raise EvaluationError(
                        f"{case_id}.{key} contains invalid regex {pattern!r}: {exc}"
                    ) from exc

        review_focus = case.get("review_focus")
        if not isinstance(review_focus, list) or not review_focus or not all(
            isinstance(item, str) and item.strip() for item in review_focus
        ):
            raise EvaluationError(f"case {case_id} has no valid review_focus")

        tags = case.get("tags", [])
        if not isinstance(tags, list) or not all(
            isinstance(item, str) and item.strip() for item in tags
        ):
            raise EvaluationError(f"case {case_id}.tags must be a string array")

    return data


def load_responses(path: Path) -> dict[str, str]:
    responses: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise EvaluationError(f"cannot read responses file {path}: {exc}") from exc

    for line_number, raw in enumerate(lines, start=1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw, object_pairs_hook=_reject_duplicate_keys)
        except (json.JSONDecodeError, EvaluationError) as exc:
            raise EvaluationError(
                f"invalid JSON on response line {line_number}: {exc}"
            ) from exc
        if not isinstance(row, dict):
            raise EvaluationError(f"response line {line_number} must be an object")
        case_id = row.get("id")
        response = row.get("response")
        if not isinstance(case_id, str) or not case_id.strip():
            raise EvaluationError(f"response line {line_number} has no valid id")
        if case_id in responses:
            raise EvaluationError(f"duplicate response id: {case_id}")
        if not isinstance(response, str) or not response.strip():
            raise EvaluationError(f"response {case_id} is empty")
        responses[case_id] = response
    return responses


def first_content_line(response: str) -> str:
    for line in response.splitlines():
        cleaned = line.strip()
        if cleaned:
            return cleaned
    return ""


def last_content_lines(response: str, count: int = 2) -> list[str]:
    lines = [line.strip() for line in response.splitlines() if line.strip()]
    return lines[-count:]


def strip_code_fences(response: str) -> str:
    # Fenced code blocks routinely contain #, -, *, and 1. lines that are not
    # response structure; remove them before counting structural markers.
    return CODE_FENCE.sub("", response)


def word_count(response: str) -> int:
    return len(WORD.findall(response))


def heading_texts(response: str) -> list[str]:
    headings = [match.group(1).strip(" *#:") for match in MARKDOWN_HEADING.finditer(response)]
    for match in BOLD_LABEL.finditer(response):
        label = match.group(1).strip(" *#:")
        if label and label.casefold() not in {item.casefold() for item in headings}:
            headings.append(label)
    return headings


def question_count(response: str) -> int:
    # A structural approximation. Markdown links and code may contain question
    # marks, but deterministic reports are more valuable than provider-specific parsing.
    return response.count("?")


def paragraph_count(response: str) -> int:
    # A paragraph is a non-empty block separated by at least one blank line.
    # This intentionally remains a transparent structural approximation.
    return sum(
        1
        for block in re.split(r"\n[ \t]*\n+", response.strip())
        if block.strip()
    )


def evaluate_case(case: dict[str, Any], response: str) -> list[str]:
    case_id = case["id"]
    expectations = case["expectations"]
    failures: list[str] = []

    response = response.replace("\r\n", "\n").replace("\r", "\n")
    lowered = response.casefold()
    first_line_raw = first_content_line(response)
    first_line = first_line_raw.casefold()
    last_lines = last_content_lines(response)
    structure_text = strip_code_fences(response)
    numbered_steps = len(NUMBERED_STEP.findall(structure_text))
    bullet_items = len(BULLET_ITEM.findall(structure_text))
    total_items = numbered_steps + bullet_items
    headings = heading_texts(structure_text)
    words = word_count(response)
    questions = question_count(response)
    paragraphs = paragraph_count(response)

    if expectations.get("forbid_generic_opener") and GENERIC_OPENERS.search(response):
        failures.append("starts with a generic preamble")
    if expectations.get("forbid_generic_closer") and any(
        GENERIC_CLOSERS.search(line) for line in last_lines
    ):
        failures.append("ends with a generic closer")

    has_next_step = bool(NEXT_STEP.search(structure_text))
    if expectations.get("require_next_step") and not has_next_step:
        failures.append("missing an explicit Next: line")
    if expectations.get("forbid_next_step") and has_next_step:
        failures.append("adds a forced Next: line")

    if expectations.get("forbid_numbered_steps") and numbered_steps:
        failures.append(f"uses {numbered_steps} numbered step(s) when none are expected")

    if "max_numbered_steps" in expectations:
        maximum = expectations["max_numbered_steps"]
        if numbered_steps > maximum:
            failures.append(
                f"uses {numbered_steps} numbered steps; maximum is {maximum}"
            )
    if "max_bullet_items" in expectations:
        maximum = expectations["max_bullet_items"]
        if bullet_items > maximum:
            failures.append(f"uses {bullet_items} bullet items; maximum is {maximum}")
    if "min_total_list_items" in expectations:
        minimum = expectations["min_total_list_items"]
        if total_items < minimum:
            failures.append(
                f"uses {total_items} total list items; minimum is {minimum}"
            )
    if "max_total_list_items" in expectations:
        maximum = expectations["max_total_list_items"]
        if total_items > maximum:
            failures.append(
                f"uses {total_items} total list items; maximum is {maximum}"
            )
    if "max_questions" in expectations:
        maximum = expectations["max_questions"]
        if questions > maximum:
            failures.append(f"uses {questions} question marks; maximum is {maximum}")
    if "max_headings" in expectations:
        maximum = expectations["max_headings"]
        if len(headings) > maximum:
            failures.append(f"uses {len(headings)} headings; maximum is {maximum}")

    if "min_paragraphs" in expectations:
        minimum = expectations["min_paragraphs"]
        if paragraphs < minimum:
            failures.append(f"uses {paragraphs} paragraphs; minimum is {minimum}")
    if "max_paragraphs" in expectations:
        maximum = expectations["max_paragraphs"]
        if paragraphs > maximum:
            failures.append(f"uses {paragraphs} paragraphs; maximum is {maximum}")

    if "required_substrings" in expectations:
        for item in expectations["required_substrings"]:
            if item.casefold() not in lowered:
                failures.append(f"missing required text: {item!r}")
    if "forbidden_substrings" in expectations:
        for item in expectations["forbidden_substrings"]:
            if item.casefold() in lowered:
                failures.append(f"contains forbidden text: {item!r}")
    if "required_any_substrings" in expectations:
        options = expectations["required_any_substrings"]
        if not any(item.casefold() in lowered for item in options):
            failures.append(
                "missing every acceptable term: "
                + ", ".join(repr(item) for item in options)
            )
    if "first_line_required_substrings" in expectations:
        for item in expectations["first_line_required_substrings"]:
            if item.casefold() not in first_line:
                failures.append(f"first content line is missing: {item!r}")

    if "required_regexes" in expectations:
        for pattern in expectations["required_regexes"]:
            if not re.search(pattern, response, flags=re.IGNORECASE | re.MULTILINE):
                failures.append(f"does not match required regex: {pattern!r}")
    if "forbidden_regexes" in expectations:
        for pattern in expectations["forbidden_regexes"]:
            if re.search(pattern, response, flags=re.IGNORECASE | re.MULTILINE):
                failures.append(f"matches forbidden regex: {pattern!r}")

    if "required_ordered_substrings" in expectations:
        cursor = 0
        for item in expectations["required_ordered_substrings"]:
            needle = item.casefold()
            position = lowered.find(needle, cursor)
            if position < 0:
                failures.append(f"missing ordered text after position {cursor}: {item!r}")
                break
            cursor = position + len(needle)

    if "required_any_headings" in expectations:
        lowered_headings = [heading.casefold() for heading in headings]
        options = expectations["required_any_headings"]
        if not any(
            option.casefold() in heading
            for option in options
            for heading in lowered_headings
        ):
            failures.append(
                "missing every acceptable heading: "
                + ", ".join(repr(item) for item in options)
            )

    if "require_first_line_regex" in expectations:
        pattern = expectations["require_first_line_regex"]
        if not re.search(pattern, first_line_raw):
            failures.append(f"first content line does not match regex: {pattern!r}")

    if "min_words" in expectations:
        minimum = expectations["min_words"]
        if words < minimum:
            failures.append(f"contains {words} words; minimum is {minimum}")
    if "max_words" in expectations:
        maximum = expectations["max_words"]
        if words > maximum:
            failures.append(f"contains {words} words; maximum is {maximum}")

    return failures


def score_suite(suite: dict[str, Any], responses: dict[str, str]) -> dict[str, Any]:
    cases = suite["cases"]
    known_ids = {case["id"] for case in cases}
    unknown_ids = sorted(set(responses) - known_ids)
    if unknown_ids:
        raise EvaluationError(
            "response file contains unknown case ids: " + ", ".join(unknown_ids)
        )

    results: list[dict[str, Any]] = []
    category_totals: Counter[str] = Counter()
    category_passed: Counter[str] = Counter()

    for case in cases:
        case_id = case["id"]
        category = case["category"]
        category_totals[category] += 1
        response = responses.get(case_id)
        if response is None:
            failures = ["missing response"]
        else:
            failures = evaluate_case(case, response)
        passed = not failures
        if passed:
            category_passed[category] += 1
        results.append(
            {
                "id": case_id,
                "category": category,
                "passed": passed,
                "failures": failures,
            }
        )

    passed_count = sum(1 for result in results if result["passed"])
    categories = {
        category: {
            "passed": category_passed[category],
            "total": category_totals[category],
        }
        for category in sorted(category_totals)
    }
    return {
        "suite": suite["suite"],
        "summary": {
            "passed": passed_count,
            "failed": len(results) - passed_count,
            "total": len(results),
        },
        "categories": categories,
        "results": results,
    }


def render_text(report: dict[str, Any]) -> str:
    lines: list[str] = []
    for result in report["results"]:
        if result["passed"]:
            lines.append(f"PASS {result['id']} [{result['category']}]")
        else:
            lines.append(
                f"FAIL {result['id']} [{result['category']}]: "
                + "; ".join(result["failures"])
            )
    summary = report["summary"]
    lines.append("")
    lines.append(
        f"{summary['passed']}/{summary['total']} cases passed; "
        f"{summary['failed']} failed"
    )
    lines.append("Categories:")
    for category, counts in report["categories"].items():
        lines.append(f"  {category}: {counts['passed']}/{counts['total']}")
    return "\n".join(lines) + "\n"


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def _markdown_escape(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", " ")


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        f"# {report['suite']['name']} evaluation report",
        "",
        f"**{summary['passed']}/{summary['total']} passed; "
        f"{summary['failed']} failed.**",
        "",
        "## Category summary",
        "",
        "| Category | Passed | Total |",
        "|---|---:|---:|",
    ]
    for category, counts in report["categories"].items():
        lines.append(f"| {_markdown_escape(category)} | {counts['passed']} | {counts['total']} |")
    lines.extend(
        [
            "",
            "## Cases",
            "",
            "| Case | Category | Result | Details |",
            "|---|---|---|---|",
        ]
    )
    for result in report["results"]:
        status = "PASS" if result["passed"] else "FAIL"
        details = "—" if result["passed"] else "; ".join(result["failures"])
        lines.append(
            f"| `{_markdown_escape(result['id'])}` | "
            f"{_markdown_escape(result['category'])} | {status} | "
            f"{_markdown_escape(details)} |"
        )
    return "\n".join(lines) + "\n"


def render_report(report: dict[str, Any], output_format: str) -> str:
    if output_format == "text":
        return render_text(report)
    if output_format == "json":
        return render_json(report)
    if output_format == "markdown":
        return render_markdown(report)
    raise EvaluationError(f"unsupported output format: {output_format}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Score ADHD & 47 Tabs response exports against the provider-neutral "
            "structural evaluation suite."
        )
    )
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "evals" / "cases.json",
        help="schema-v2 JSON suite (default: evals/cases.json)",
    )
    parser.add_argument(
        "--responses",
        type=Path,
        required=True,
        help='JSONL file with {"id": "...", "response": "..."} rows',
    )
    parser.add_argument(
        "--format",
        choices=("text", "json", "markdown"),
        default="text",
        dest="output_format",
        help="report format (default: text)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="write the report to this file instead of stdout",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        suite = load_suite(args.cases)
        responses = load_responses(args.responses)
        report = score_suite(suite, responses)
        output = render_report(report, args.output_format)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding="utf-8")
        else:
            sys.stdout.write(output)
    except (EvaluationError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    return 0 if report["summary"]["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
