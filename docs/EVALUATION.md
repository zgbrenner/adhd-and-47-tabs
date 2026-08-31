# Evaluation guide

ADHD & 47 Tabs uses a 47-case provider-neutral, local-first regression suite, including nine multi-turn cases. It is designed to catch structural behavior regressions without pretending that regexes can judge every semantic quality.

## Suite format

`evals/cases.json` uses schema version 2:

```json
{
  "schema_version": 2,
  "suite": {
    "name": "ADHD & 47 Tabs",
    "slug": "adhd-and-47-tabs",
    "version": "3.0.1"
  },
  "cases": []
}
```

Each case contains:

- a stable `id`;
- a `category` and optional `tags`;
- exactly one `prompt` or `conversation`;
- deterministic `expectations`;
- one or more `review_focus` statements for human inspection.

A `conversation` is an ordered array of `system`, `user`, and `assistant` turns. Send the full conversation to the model under test and capture only the final assistant response.

## Response export

Create a UTF-8 JSONL file with one row per case:

```json
{"id":"direct-fact","response":"Paris is the capital of France."}
{"id":"resume-after-interruption","response":"You are here: draft the article → outline complete → write the opening section."}
```

The scorer rejects duplicate IDs, empty responses, malformed JSON, and IDs that do not exist in the suite. Missing known cases are reported as scored failures.

## Run the scorer

Text report:

```bash
python3 scripts/score_responses.py --responses responses.jsonl
```

JSON report:

```bash
python3 scripts/score_responses.py \
  --responses responses.jsonl \
  --format json \
  --output report.json
```

Markdown report:

```bash
python3 scripts/score_responses.py \
  --responses responses.jsonl \
  --format markdown \
  --output report.md
```

Make shortcuts:

```bash
make score RESPONSES=responses.jsonl
make score-json RESPONSES=responses.jsonl OUTPUT=report.json
make score-markdown RESPONSES=responses.jsonl OUTPUT=report.md
```

Exit codes:

- `0`: every supplied suite case passed;
- `1`: one or more cases failed or were missing;
- `2`: suite, response export, regex, or CLI input was malformed.

## Deterministic assertions

The scorer supports:

- `forbid_generic_opener`
- `forbid_generic_closer`
- `require_next_step`
- `forbid_next_step`
- `max_numbered_steps`
- `forbid_numbered_steps`
- `max_bullet_items`
- `min_total_list_items`
- `max_total_list_items`
- `max_questions`
- `max_headings`
- `min_paragraphs`
- `max_paragraphs`
- `required_substrings`
- `forbidden_substrings`
- `required_any_substrings`
- `first_line_required_substrings`
- `required_regexes`
- `forbidden_regexes`
- `required_ordered_substrings`
- `required_any_headings`
- `require_first_line_regex`
- `min_words`
- `max_words`

Assertions are intentionally simple, transparent, deterministic, and provider-independent.

## What structural scoring can catch

- empty throat-clearing before the answer;
- empty closing offers after a complete answer;
- a forced `Next:` line where no task remains;
- missing interruption-recovery breadcrumbs;
- too many simultaneously active list items;
- missing ordered recovery sections;
- missing required values carried from prior turns;
- responses that truncate a requested deep dive, long artifact, requested option count, or paragraph structure;
- stop-mode responses that keep talking;
- absent safety or escalation terminology in selected high-stakes cases.

## What requires human review

Read the response against each case's `review_focus`. In particular, inspect:

- factual accuracy and source quality;
- whether the first action is meaningful rather than trivial;
- whether recommendations are well reasoned;
- whether remembered information is reliable and used appropriately;
- whether the **You are here:** state is actually supported by the conversation;
- whether a diagnostic distinguishes plausible causes;
- whether finish protection preserves every real requirement;
- whether tone is humane in emotional-support cases;
- whether high-stakes caveats are proportional;
- whether creative or detailed requests retain their intended experience;
- whether the response is concise enough to navigate but complete enough to use.

A structural pass is not a semantic certification.

## Regression workflow

1. Add or edit behavior in `SKILL.md` or a focused reference.
2. Add at least one case that fails under the old behavior and represents a real use or failure mode.
3. Generate responses from the model or host being evaluated.
4. Run the scorer.
5. Review every failed assertion and every `review_focus`.
6. Compare against a known-good baseline when changing models, host versions, or skill wording.
7. Run `make check` before packaging or release.

## Case design rules

A strong case:

- tests one primary behavior;
- includes enough context to distinguish good and bad behavior;
- avoids requiring exact prose when several responses could be good;
- uses deterministic assertions only for observable structure;
- states the semantic review target explicitly;
- includes adversarial cases where a simplistic “be brief” implementation would fail.

For behavior changes, the regression case is part of the feature.
