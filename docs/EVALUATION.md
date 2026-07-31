# Behavior evaluation

`make check` validates the package and repository contract. The optional behavior suite checks whether a model using **ADHD & 47 Tabs** produces the intended response shape across common and adversarial scenarios.

The evaluator is dependency-free and does not call any model API. You can use it with Claude, ChatGPT, Codex, GitHub Copilot, or any other host by collecting responses manually or through your own approved tooling.

## 1. Run the scenarios

Open `evals/cases.json`. For each case:

1. Start a fresh conversation with the skill enabled.
2. Send the exact `prompt` value.
3. Copy the complete response.
4. Add one JSON object to `responses.jsonl`:

```json
{"id":"direct-fact-no-forced-task","response":"Paris is the capital of France."}
```

Use one object per line. Newlines inside a response must be encoded as `\n` by whatever tool creates the JSONL file.

## 2. Score the responses

```bash
python3 scripts/score_responses.py --responses responses.jsonl
```

To use a custom case file:

```bash
python3 scripts/score_responses.py \
  --cases path/to/cases.json \
  --responses path/to/responses.jsonl
```

Exit codes:

- `0`: every case passed its structural checks.
- `1`: one or more responses failed expectations or are missing.
- `2`: the case or response file is invalid.

## 3. Perform human review

The scorer catches structural regressions such as:

- generic preambles;
- missing or forced `Next:` lines;
- too many active numbered steps;
- missing required terms;
- over-compressed high-stakes answers;
- checklist formatting where prose is required.

It cannot determine whether an answer is factually correct, well sourced, legally or medically sound, genuinely empathetic, creatively strong, or semantically complete. Review every case's `review_focus` fields manually.

A strong evaluation record should include:

- model and host;
- model version when visible;
- skill version;
- date tested;
- raw response JSONL;
- scorer output;
- brief human notes for failures and borderline cases.

## Adding a regression case

Add a case when a real response reveals a reusable failure mode.

Each case needs:

- a unique `id`;
- a `category`;
- the exact `prompt`;
- an `expectations` object using supported checks;
- `review_focus` notes for semantic review.

List supported checks:

```bash
python3 scripts/score_responses.py --help
```

The implementation currently supports generic-opener checks, required or forbidden next steps, numbered-step limits, required or forbidden text and regular expressions, first-line requirements, and word-count floors or ceilings.

Do not add a case merely to force one preferred wording. Test behavior that should remain stable across capable models.
