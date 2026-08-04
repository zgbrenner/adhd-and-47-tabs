# ADHD & 47 Tabs v3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship v3.0.0 as a portable, adaptive cognitive-load Agent Skill with interruption recovery, memory offloading, a bounded working set, user controls, and substantially stronger local evaluations.

**Architecture:** Preserve the four v2 response contracts and add six orthogonal modifiers documented in one focused reference. Keep the always-loaded skill concise through progressive disclosure. Upgrade the local dependency-free evaluation suite to schema version 2 with single-turn and multi-turn cases, richer structural assertions, and machine-readable reports.

**Tech Stack:** Markdown, JSON, Python 3 standard library, Make, deterministic ZIP packaging, GitHub pull requests and releases.

## Global Constraints

- Canonical slug and package name remain exactly `adhd-and-47-tabs`.
- Release version is exactly `3.0.0`.
- `SKILL.md` remains below 500 lines.
- The uploadable skill contains no executable code, credentials, network calls, telemetry, or third-party dependencies.
- Repository validation remains local-only; add no GitHub Actions or hosted CI.
- Preserve MIT licensing and attribution to Ayoub Ghriss and Zachary Brenner.
- Preserve safety, factual accuracy, citations, necessary nuance, warmth, and explicitly requested depth.
- Do not diagnose, treat, or present one ADHD experience as universal.

---

### Task 1: Define the v3 behavioral core

**Files:**
- Modify: `adhd-and-47-tabs/SKILL.md`
- Create: `adhd-and-47-tabs/references/interaction-patterns.md`
- Create: `adhd-and-47-tabs/references/quick-reference.md`
- Modify: `adhd-and-47-tabs/references/examples.md`
- Modify: `adhd-and-47-tabs/README.md`
- Modify: `adhd-and-47-tabs/NOTICE.md`
- Modify: `chatgpt-custom-gpt/INSTRUCTIONS.md`

**Interfaces:**
- Consumes: The four v2 contracts and the design specification.
- Produces: Stable headings and phrases consumed by `scripts/validate_skill.py`; user controls `one thing`, `map it`, `resume`, `park that`, `more detail`, `less detail`, `why this`, and stop-mode phrases.

- [ ] **Step 1: Add failing static expectations**

Add required behavior signals to the validator before editing the skill:

```python
REQUIRED_SKILL_SIGNALS = {
    "Friction modifier",
    "Reorientation modifier",
    "Memory-offload modifier",
    "Decision modifier",
    "Recovery modifier",
    "Finish modifier",
    "You are here:",
    "one thing",
    "map it",
    "resume",
    "park that",
}
```

- [ ] **Step 2: Run validation and confirm failure**

Run: `python3 scripts/validate_skill.py`  
Expected: failure naming the first missing v3 behavior signal.

- [ ] **Step 3: Rewrite the skill around contracts plus modifiers**

Implement:

- four unchanged base contracts;
- six adaptive modifiers;
- Active/Ready/Blocked/Parked working-set protocol;
- resumption breadcrumb;
- memory reuse and no redundant re-entry;
- repeated-failure circuit breaker after two clear unsuccessful iterations;
- finish protection and observable definition of done;
- reversible-default versus irreversible-confirmation behavior;
- optional, assumption-labeled estimates and no false urgency;
- user controls and natural-language equivalents;
- exceptions and pre-send checks.

- [ ] **Step 4: Write focused references and examples**

`interaction-patterns.md` must define routing, state transitions, visible patterns, and anti-patterns. `quick-reference.md` must fit on one concise page. `examples.md` must include at least 20 examples, including interruption recovery, remembered constraints, repeated debugging failure, finish-line scope protection, low-bandwidth planning, and each user control.

- [ ] **Step 5: Synchronize packaged and Custom GPT documentation**

Ensure the package README, notice, and Custom GPT instructions use version 3 language without duplicating the entire skill.

- [ ] **Step 6: Run static validation**

Run: `python3 scripts/validate_skill.py`  
Expected: all behavior signals, links, controls, line budgets, and attribution checks pass once later suite files exist.

- [ ] **Step 7: Commit**

```bash
git add adhd-and-47-tabs chatgpt-custom-gpt/INSTRUCTIONS.md scripts/validate_skill.py
git commit -m "feat: add adaptive cognitive-load behavior"
```

### Task 2: Upgrade the declarative evaluation suite

**Files:**
- Modify: `evals/cases.json`
- Modify: `scripts/score_responses.py`
- Modify: `scripts/test_score_responses.py`
- Modify: `docs/EVALUATION.md`

**Interfaces:**
- Produces: `load_suite(path) -> dict[str, Any]`, `evaluate_case(case, response) -> list[str]`, `build_report(results, output_format) -> str`.
- Consumes: responses as JSONL rows with `id` and `response`.

- [ ] **Step 1: Write tests for schema v2 and new assertions**

Cover:

```python
{
    "schema_version": 2,
    "suite": {"name": "ADHD & 47 Tabs", "version": "3.0.0"},
    "cases": [{
        "id": "resume-after-interruption",
        "category": "reorientation",
        "conversation": [
            {"role": "user", "content": "We finished the outline."},
            {"role": "user", "content": "Resume the article."}
        ],
        "expectations": {
            "require_first_line_regex": "(?i)^you are here:",
            "max_questions": 0,
            "max_total_list_items": 4
        },
        "review_focus": ["The response restores the active thread without replaying history."]
    }]
}
```

Tests must also cover generic closers, ordered substrings, required heading alternatives, bullet counts, JSON output, Markdown output, invalid regexes, unknown assertions, missing responses, and category summaries.

- [ ] **Step 2: Run scorer tests and confirm failure**

Run: `python3 scripts/test_score_responses.py`  
Expected: failures because schema v2 and the new assertions are not implemented.

- [ ] **Step 3: Implement the scorer upgrade**

Supported additions:

```python
{
    "forbid_generic_closer",
    "max_bullet_items",
    "max_total_list_items",
    "max_questions",
    "max_headings",
    "required_ordered_substrings",
    "required_any_headings",
    "require_first_line_regex"
}
```

Add `--format text|json|markdown`, optional `--output`, category totals, deterministic result ordering, and exit codes `0` pass, `1` scored failures, `2` malformed input.

- [ ] **Step 4: Replace the suite with at least 30 cases**

Include single-turn and multi-turn coverage for all base contracts, all six modifiers, user controls, stop mode, long requested artifacts, high stakes, emotional support, creative work, troubleshooting, and adversarial over-compression.

- [ ] **Step 5: Update the evaluation guide**

Document provider-neutral collection, conversation replay, JSONL format, report formats, human review, regression workflow, and the boundary between structural and semantic evaluation.

- [ ] **Step 6: Run scorer tests**

Run: `python3 scripts/test_score_responses.py`  
Expected: all tests pass.

- [ ] **Step 7: Commit**

```bash
git add evals/cases.json scripts/score_responses.py scripts/test_score_responses.py docs/EVALUATION.md
git commit -m "test: expand adaptive behavior evaluations"
```

### Task 3: Harden validation and deterministic packaging

**Files:**
- Modify: `scripts/validate_skill.py`
- Modify: `scripts/build_zip.py`
- Modify: `scripts/test_repository.py`
- Modify: `scripts/prepare_release.py`
- Modify: `Makefile`

**Interfaces:**
- Produces: deterministic `dist/adhd-and-47-tabs.zip` and `dist/SHA256SUMS`.
- Consumes: the v3 source package, suite, documentation, and version surfaces.

- [ ] **Step 1: Write failing repository-contract tests**

Require:

- sorted ZIP entries;
- fixed timestamp `(2026, 8, 4, 0, 0, 0)`;
- one canonical top-level folder;
- byte-for-byte equality between packaged and source files;
- no symlinks, hidden caches, executables, or unexpected files;
- exact checksum line;
- package and source version synchronization;
- all focused references included.

- [ ] **Step 2: Run repository tests and confirm failure**

Run: `python3 scripts/test_repository.py`  
Expected: failure until the new references, version, and package are synchronized.

- [ ] **Step 3: Upgrade validation**

Validate schema version 2, suite version `3.0.0`, at least 30 unique cases, required categories, required modifiers and controls, one-level reference links, research ledger presence, no stale version strings on canonical surfaces, and no unfinished placeholders.

- [ ] **Step 4: Harden package generation**

Use standard-library ZIP creation with fixed permissions, fixed timestamp, sorted POSIX paths, compression level 9, atomic replacement, and automatic SHA-256 generation.

- [ ] **Step 5: Run all local checks**

Run:

```bash
make check
make release
```

Expected: validator, package builder, repository tests, scorer tests, checksum verification, and release preparation all pass without dependencies or network access.

- [ ] **Step 6: Commit**

```bash
git add scripts Makefile dist/adhd-and-47-tabs.zip dist/SHA256SUMS
git commit -m "build: harden deterministic v3 package"
```

### Task 4: Document research, migration, and release

**Files:**
- Create: `docs/RESEARCH.md`
- Create: `docs/releases/3.0.0.md`
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `CITATION.cff`
- Modify: `VERSION`
- Modify: `CONTRIBUTING.md`
- Modify: `PUBLISH.md`
- Modify: `docs/DIRECTORY_SUBMISSIONS.md`

**Interfaces:**
- Consumes: verified v3 behavior and package details.
- Produces: public installation, attribution, research, contributor, and release documentation.

- [ ] **Step 1: Set all version surfaces to 3.0.0**

Synchronize `VERSION`, skill metadata, suite metadata, citation version/date, changelog, release notes, and package documentation.

- [ ] **Step 2: Write the research ledger**

For every source, record:

- project or standard;
- primary source URL;
- principle adopted;
- how it was transformed for this project;
- what was deliberately not copied or adopted.

Include W3C COGA, Agent Skills, upstream `i-have-adhd`, Leantime, Taskwarrior, Super Productivity, ActivityWatch, Beads, `claude-adhd-skills`, Promptfoo, OpenAI Evals, and Inspect AI.

- [ ] **Step 3: Rewrite the public README**

Lead with the v3 value proposition, describe contracts plus modifiers, explain quick controls, provide the upgrade path, preserve current installation routes, and show local evaluation commands.

- [ ] **Step 4: Update contribution and publishing contracts**

Require a regression case for behavior changes, regenerated tracked package assets, local checks, exact release steps, and no hosted CI.

- [ ] **Step 5: Run placeholder and stale-version scans**

Run:

```bash
python3 scripts/validate_skill.py
python3 -c "from pathlib import Path; assert not any('TODO' in p.read_text(errors='ignore') or 'TBD' in p.read_text(errors='ignore') for p in Path('.').rglob('*.md'))"
```

Expected: no placeholders or stale v2 canonical copy.

- [ ] **Step 6: Commit**

```bash
git add README.md CHANGELOG.md CITATION.cff VERSION CONTRIBUTING.md PUBLISH.md docs
git commit -m "docs: publish v3 research and migration guide"
```

### Task 5: Review, merge, and release

**Files:**
- Review all changed files.
- Publish tracked assets: `dist/adhd-and-47-tabs.zip`, `dist/SHA256SUMS`.

**Interfaces:**
- Consumes: clean branch with passing local checks.
- Produces: merged `main`, tag `v3.0.0`, GitHub Release, and downloadable assets matching the merged tree.

- [ ] **Step 1: Run final verification from the branch tip**

```bash
make check
make release
python3 scripts/score_responses.py --help
```

Expected: all commands exit `0`; the help output lists text, JSON, and Markdown formats.

- [ ] **Step 2: Review the complete diff**

Check for unsupported medical claims, copied prose, contradictory rules, excessive rigidity, stale versions, missing attribution, hidden dependencies, credentials, and package drift.

- [ ] **Step 3: Open a pull request**

The pull request body must include research, behavior, evaluation, packaging, test evidence, migration, and release sections.

- [ ] **Step 4: Verify the pull-request head**

Confirm the expected changed-file set, no unresolved review threads, mergeability, and the exact head SHA.

- [ ] **Step 5: Squash merge into main**

Use the verified head SHA to prevent merging a moved branch.

- [ ] **Step 6: Verify main**

Fetch the merge commit, confirm `VERSION` is `3.0.0`, and verify the checksum in `main` matches the tracked ZIP bytes.

- [ ] **Step 7: Create release `v3.0.0`**

Use `docs/releases/3.0.0.md` as the release body. Attach the exact tracked ZIP and checksum. Mark it as the latest non-prerelease release.

- [ ] **Step 8: Verify the release**

Confirm the tag resolves to the merge commit, both assets are present, the asset checksum matches `main`, and the canonical repository download remains identical.
