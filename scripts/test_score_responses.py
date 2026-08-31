#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "score_responses.py"
SPEC = importlib.util.spec_from_file_location("score_responses", MODULE_PATH)
assert SPEC and SPEC.loader
score_responses = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(score_responses)


def suite_with(expectations: dict, *, category: str = "test") -> dict:
    return {
        "schema_version": 2,
        "suite": {
            "name": "Test suite",
            "slug": "test-suite",
            "version": "3.0.0",
        },
        "cases": [
            {
                "id": "case-1",
                "category": category,
                "prompt": "Test prompt",
                "expectations": expectations,
                "review_focus": ["Review the intended behavior."],
            }
        ],
    }


class ScoreResponsesTests(unittest.TestCase):
    def test_repository_suite_loads_and_has_multi_turn_cases(self) -> None:
        suite = score_responses.load_suite(ROOT / "evals" / "cases.json")
        self.assertEqual(suite["schema_version"], 2)
        self.assertGreaterEqual(len(suite["cases"]), 47)
        self.assertTrue(any("conversation" in case for case in suite["cases"]))
        self.assertEqual(
            suite["suite"]["version"],
            (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        )

    def test_passing_response_exercises_new_assertions(self) -> None:
        case = suite_with(
            {
                "forbid_generic_opener": True,
                "forbid_generic_closer": True,
                "require_first_line_regex": r"(?i)^you are here:",
                "required_ordered_substrings": ["Known", "One diagnostic"],
                "required_any_headings": ["Known"],
                "max_numbered_steps": 1,
                "max_bullet_items": 1,
                "max_total_list_items": 2,
                "max_questions": 0,
                "max_headings": 2,
                "min_words": 8,
                "max_words": 80,
            }
        )
        response = (
            "You are here: restore access → two token attempts failed → inspect audience.\n\n"
            "**Known:** both tokens return 401.\n\n"
            "**One diagnostic:** compare the token audience with the API audience."
        )
        failures = score_responses.evaluate_case(case["cases"][0], response)
        self.assertEqual(failures, [])

    def test_failing_response_reports_multiple_reasons(self) -> None:
        case = suite_with(
            {
                "forbid_generic_opener": True,
                "forbid_generic_closer": True,
                "forbid_next_step": True,
                "max_questions": 0,
                "required_substrings": ["Paris"],
            }
        )
        response = "Great question. Lyon?\n\nNext: ask anything else.\n\nHope this helps!"
        failures = score_responses.evaluate_case(case["cases"][0], response)
        joined = " | ".join(failures)
        self.assertIn("generic preamble", joined)
        self.assertIn("generic closer", joined)
        self.assertIn("forced Next", joined)
        self.assertIn("question marks", joined)
        self.assertIn("Paris", joined)

    def test_required_order_and_heading_checks(self) -> None:
        case = suite_with(
            {
                "required_ordered_substrings": ["Known", "Likely", "Diagnostic"],
                "required_any_headings": ["Known", "Evidence"],
            }
        )
        response = "**Known:** facts follow.\n\nDiagnostic check now.\n\nLikely cause later."
        failures = score_responses.evaluate_case(case["cases"][0], response)
        self.assertTrue(any("ordered text" in failure for failure in failures))
        self.assertEqual(
            [failure for failure in failures if "acceptable heading" in failure],
            [],
        )

    def test_list_counters_distinguish_numbered_and_bullets(self) -> None:
        case = suite_with(
            {
                "max_numbered_steps": 1,
                "max_bullet_items": 1,
                "max_total_list_items": 2,
            }
        )
        response = "1. First\n2. Second\n\n- A\n- B"
        failures = score_responses.evaluate_case(case["cases"][0], response)
        self.assertEqual(len(failures), 3)

    def test_minimum_total_list_items_enforces_requested_breadth(self) -> None:
        case = suite_with({"min_total_list_items": 3})
        passing = score_responses.evaluate_case(
            case["cases"][0], "- First\n- Second\n- Third"
        )
        self.assertEqual(passing, [])

        failures = score_responses.evaluate_case(
            case["cases"][0], "- First\n- Second"
        )
        self.assertTrue(any("minimum is 3" in failure for failure in failures))

    def test_paragraph_bounds_enforce_requested_prose_shape(self) -> None:
        case = suite_with({"min_paragraphs": 3, "max_paragraphs": 3})
        passing = score_responses.evaluate_case(
            case["cases"][0], "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        )
        self.assertEqual(passing, [])

        too_short = score_responses.evaluate_case(
            case["cases"][0], "First paragraph.\n\nSecond paragraph."
        )
        self.assertTrue(any("paragraphs; minimum is 3" in failure for failure in too_short))

        too_long = score_responses.evaluate_case(
            case["cases"][0],
            "First.\n\nSecond.\n\nThird.\n\nFourth.",
        )
        self.assertTrue(any("paragraphs; maximum is 3" in failure for failure in too_long))

    def test_next_step_detection_covers_plural_and_heading_forms(self) -> None:
        case = suite_with({"forbid_next_step": True})
        for phrasing in (
            "Done.\n\nNext: review the draft.",
            "Done.\n\nNext steps: review the draft.",
            "Done.\n\n## Next: review the draft.",
            "Done.\n\n**Next step:** review the draft.",
        ):
            failures = score_responses.evaluate_case(case["cases"][0], phrasing)
            self.assertTrue(
                any("forced Next" in failure for failure in failures), phrasing
            )

    def test_crlf_responses_count_paragraphs_correctly(self) -> None:
        case = suite_with({"min_paragraphs": 3, "max_paragraphs": 3})
        failures = score_responses.evaluate_case(
            case["cases"][0], "First.\r\n\r\nSecond.\r\n\r\nThird."
        )
        self.assertEqual(failures, [])

    def test_fenced_code_is_excluded_from_structure_counts(self) -> None:
        case = suite_with(
            {"max_headings": 0, "max_numbered_steps": 0, "max_bullet_items": 0}
        )
        response = (
            "Run the script below.\n\n"
            "```bash\n# comment heading\n1. not a step\n- not a bullet\n```\n"
        )
        failures = score_responses.evaluate_case(case["cases"][0], response)
        self.assertEqual(failures, [])

    def test_ordered_substrings_do_not_overlap(self) -> None:
        case = suite_with({"required_ordered_substrings": ["step 1", "1"]})
        failures = score_responses.evaluate_case(case["cases"][0], "step 1 only")
        self.assertTrue(any("ordered text" in failure for failure in failures))
        passing = score_responses.evaluate_case(case["cases"][0], "step 1, then 1")
        self.assertEqual(passing, [])

    def test_generic_closer_is_caught_before_a_trailing_note(self) -> None:
        case = suite_with({"forbid_generic_closer": True})
        failures = score_responses.evaluate_case(
            case["cases"][0], "Paris.\n\nHope this helps!\n\n(see the docs)"
        )
        self.assertTrue(any("generic closer" in failure for failure in failures))

    def test_unknown_expectation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.json"
            path.write_text(
                json.dumps(suite_with({"unknown_rule": True})),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                score_responses.EvaluationError, "unsupported expectations"
            ):
                score_responses.load_suite(path)

    def test_boolean_expectations_require_actual_booleans(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.json"
            path.write_text(
                json.dumps(suite_with({"forbid_generic_opener": "true"})),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(score_responses.EvaluationError, "must be a boolean"):
                score_responses.load_suite(path)

    def test_word_bounds_reject_inverted_range(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.json"
            path.write_text(
                json.dumps(suite_with({"min_words": 20, "max_words": 10})),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(score_responses.EvaluationError, "min_words cannot exceed max_words"):
                score_responses.load_suite(path)

    def test_empty_prompt_cannot_hide_alongside_conversation(self) -> None:
        data = suite_with({})
        data["cases"][0]["prompt"] = "   "
        data["cases"][0]["conversation"] = [
            {"role": "user", "content": "A valid conversation"}
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(score_responses.EvaluationError, "exactly one"):
                score_responses.load_suite(path)

    def test_invalid_regex_is_rejected_during_load(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.json"
            path.write_text(
                json.dumps(suite_with({"required_regexes": ["("]})),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(score_responses.EvaluationError, "invalid regex"):
                score_responses.load_suite(path)

    def test_duplicate_json_keys_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.json"
            path.write_text(
                '{"schema_version":2,"schema_version":2,"suite":{},"cases":[]}',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(score_responses.EvaluationError, "duplicate"):
                score_responses.load_suite(path)

    def test_prompt_or_conversation_is_exclusive(self) -> None:
        data = suite_with({})
        data["cases"][0]["conversation"] = [
            {"role": "user", "content": "Also a conversation"}
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(score_responses.EvaluationError, "exactly one"):
                score_responses.load_suite(path)

    def test_response_export_rejects_unknown_ids(self) -> None:
        report_suite = suite_with({})
        with self.assertRaisesRegex(score_responses.EvaluationError, "unknown case ids"):
            score_responses.score_suite(report_suite, {"other": "response"})

    def test_missing_response_is_a_scored_failure(self) -> None:
        report = score_responses.score_suite(suite_with({}), {})
        self.assertEqual(report["summary"], {"passed": 0, "failed": 1, "total": 1})
        self.assertEqual(report["results"][0]["failures"], ["missing response"])

    def test_category_summary_is_deterministic(self) -> None:
        data = suite_with({})
        data["cases"].append(
            {
                "id": "case-2",
                "category": "alpha",
                "prompt": "Second prompt",
                "expectations": {},
                "review_focus": ["Review."],
            }
        )
        data["cases"][0]["category"] = "zeta"
        report = score_responses.score_suite(
            data, {"case-1": "pass", "case-2": "pass"}
        )
        self.assertEqual(list(report["categories"]), ["alpha", "zeta"])

    def test_json_report_is_machine_readable(self) -> None:
        report = score_responses.score_suite(
            suite_with({}), {"case-1": "A passing response."}
        )
        rendered = score_responses.render_report(report, "json")
        parsed = json.loads(rendered)
        self.assertEqual(parsed["summary"]["passed"], 1)
        self.assertEqual(parsed["results"][0]["id"], "case-1")

    def test_markdown_report_contains_summary_and_case_table(self) -> None:
        report = score_responses.score_suite(
            suite_with({}), {"case-1": "A passing response."}
        )
        rendered = score_responses.render_report(report, "markdown")
        self.assertIn("# Test suite evaluation report", rendered)
        self.assertIn("| Category | Passed | Total |", rendered)
        self.assertIn("| `case-1` | test | PASS |", rendered)

    def test_cli_writes_output_file_and_returns_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            cases_path = tmp_path / "cases.json"
            responses_path = tmp_path / "responses.jsonl"
            output_path = tmp_path / "report.md"
            cases_path.write_text(json.dumps(suite_with({})), encoding="utf-8")
            responses_path.write_text(
                json.dumps({"id": "case-1", "response": "A passing response."}) + "\n",
                encoding="utf-8",
            )
            code = score_responses.main(
                [
                    "--cases",
                    str(cases_path),
                    "--responses",
                    str(responses_path),
                    "--format",
                    "markdown",
                    "--output",
                    str(output_path),
                ]
            )
            self.assertEqual(code, 0)
            self.assertIn("PASS", output_path.read_text(encoding="utf-8"))

    def test_cli_returns_one_for_scored_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            cases_path = tmp_path / "cases.json"
            responses_path = tmp_path / "responses.jsonl"
            cases_path.write_text(
                json.dumps(suite_with({"required_substrings": ["Paris"]})),
                encoding="utf-8",
            )
            responses_path.write_text(
                json.dumps({"id": "case-1", "response": "Lyon"}) + "\n",
                encoding="utf-8",
            )
            with contextlib.redirect_stdout(io.StringIO()):
                code = score_responses.main(
                    ["--cases", str(cases_path), "--responses", str(responses_path)]
                )
            self.assertEqual(code, 1)

    def test_cli_returns_two_for_malformed_response_export(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            cases_path = tmp_path / "cases.json"
            responses_path = tmp_path / "responses.jsonl"
            cases_path.write_text(json.dumps(suite_with({})), encoding="utf-8")
            responses_path.write_text("{not json}\n", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                code = score_responses.main(
                    ["--cases", str(cases_path), "--responses", str(responses_path)]
                )
            self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
