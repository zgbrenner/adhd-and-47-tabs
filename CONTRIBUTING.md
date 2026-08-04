# Contributing

Contributions should make ADHD & 47 Tabs easier to use **without deleting necessary substance**.

## Before proposing a change

Read:

- `adhd-and-47-tabs/SKILL.md`
- `adhd-and-47-tabs/references/interaction-patterns.md`
- `docs/RESEARCH.md`
- `docs/EVALUATION.md`

A behavior change should answer:

1. What real friction or failure does this fix?
2. Which base contract or modifier owns the behavior?
3. Does it preserve safety, accuracy, warmth, and requested depth?
4. What regression case proves the change?
5. Does it remain portable and dependency-free?

## Local requirements

Python 3 and Make are sufficient. The skill itself contains no executable code.

Run:

```bash
make check
make release
```

Optional local protection:

```bash
make install-hooks
```

The pre-push hook runs `make check` locally. This repository intentionally has no GitHub Actions or hosted CI.

## Behavior changes

For changes to the skill or references:

1. Update the smallest responsible file.
2. Add or update a case in `evals/cases.json`.
3. Add an example when the interaction shape is not already obvious.
4. Update the research ledger when a new external source materially informs the design.
5. Run the complete local suite.
6. Rebuild and commit `dist/adhd-and-47-tabs.zip` and `dist/SHA256SUMS`.

Do not add rigid rules that:

- make every answer short;
- force a task after a complete answer;
- truncate requested artifacts;
- infer diagnosis or energy;
- remove necessary high-stakes guidance;
- create false urgency or unsupported estimates;
- require a particular vendor, host, timer, note app, or task manager.

## Evaluation changes

`evals/cases.json` uses schema version 2. Every case must have:

- a unique stable ID;
- one category;
- exactly one prompt or conversation;
- supported deterministic expectations;
- non-empty human-review focus.

When adding a new assertion:

1. Write a failing unit test in `scripts/test_score_responses.py`.
2. Implement the assertion in `scripts/score_responses.py`.
3. Document it in `docs/EVALUATION.md`.
4. Add a real suite case that uses it.

## Documentation and attribution

Use primary sources whenever possible. Preserve attribution to Ayoub Ghriss and Zachary Brenner in the MIT license, notice, metadata, citation, and package.

Do not copy substantial prose or code from another project. Record adopted principles and rejected scope in `docs/RESEARCH.md`.

## Pull requests

A pull request should include:

- behavioral summary;
- regression coverage;
- local verification output;
- package checksum;
- migration or compatibility impact;
- any research sources added.

No credentials, API keys, generated caches, untracked release assets, remote publishing scripts, or hosted workflow files are accepted.
