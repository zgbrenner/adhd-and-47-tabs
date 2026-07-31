# ADHD & 47 Tabs v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a coherent v2 Agent Skill with adaptive response rules, canonical naming, behavior evaluations, stronger validation, and reliable local packaging.

**Architecture:** Keep the distributable skill self-contained in one top-level folder. Put detailed examples in a single referenced file, portable evaluation cases under `evals/`, and dependency-free validation and scoring scripts under `scripts/`. Enforce the repository contract through Python `unittest` tests and deterministic ZIP packaging.

**Tech Stack:** Markdown, YAML frontmatter, Python 3 standard library, Bash, Make, GitHub CLI.

## Global Constraints

- Canonical slug: `adhd-and-47-tabs`.
- Canonical repository: `zgbrenner/adhd-and-47-tabs`.
- Release version: `2.0.0`.
- No hosted CI, GitHub Actions, paid services, model API keys, or third-party Python packages.
- Preserve upstream attribution and MIT licensing.
- Skill rules must preserve safety, accuracy, citations, necessary nuance, and user-requested detail.

---

### Task 1: Write failing v2 repository contract tests

**Files:**
- Modify: `tests/test_repository.py`

**Interfaces:**
- Consumes: repository paths and text files.
- Produces: failing assertions for the v2 slug, metadata, documentation, evaluation suite, and release scripts.

- [ ] Replace the v1 skill constants with `adhd-and-47-tabs` and require `VERSION` to equal `2.0.0`.
- [ ] Add assertions that tracked text files contain no stale `zgbrenner/i-have-adhd-and-47-tabs` or `i-have-adhd-and-47-tabs.zip` references.
- [ ] Require `evals/cases.json`, `scripts/score_responses.py`, and `docs/EVALUATION.md`.
- [ ] Require scenario coverage for answer, action, artifact, project update, high-stakes, creative, and emotional-support cases.
- [ ] Require the skill to state that cognitive load, not word count, is the optimization target and that complete requests must not receive forced next steps.
- [ ] Run `python3 -m unittest discover -s tests -v` and confirm the new tests fail because v2 files and paths do not exist.

### Task 2: Implement the v2 skill package

**Files:**
- Create: `adhd-and-47-tabs/SKILL.md`
- Create: `adhd-and-47-tabs/README.md`
- Create: `adhd-and-47-tabs/LICENSE`
- Create: `adhd-and-47-tabs/NOTICE.md`
- Create: `adhd-and-47-tabs/references/examples.md`
- Delete: `i-have-adhd-and-47-tabs/`

**Interfaces:**
- Consumes: Agent Skills metadata rules and the v2 design.
- Produces: one uploadable package whose folder name matches its frontmatter name.

- [ ] Write frontmatter with the canonical name, concise what-and-when description, MIT license, version `2.0.0`, and cross-platform metadata.
- [ ] Implement the four response contracts: answer, action, artifact, and project update.
- [ ] Add progressive disclosure, bounded active steps, ranking, definitions of done, and matter-of-fact error handling.
- [ ] Add explicit exceptions for safety, high-stakes accuracy, requested depth, creative work, emotional support, ambiguity, and required formats.
- [ ] Add anti-patterns and a compact pre-send check.
- [ ] Expand examples to test both compression and necessary detail.
- [ ] Run the repository tests and confirm package-contract assertions move toward green.

### Task 3: Add portable behavior evaluation

**Files:**
- Create: `evals/cases.json`
- Create: `scripts/score_responses.py`
- Create: `docs/EVALUATION.md`
- Modify: `tests/test_repository.py`

**Interfaces:**
- Consumes: JSON array of case definitions and JSONL response exports.
- Produces: per-case structural scores and a nonzero exit code when required checks fail.

- [ ] Define at least twelve cases with unique IDs, categories, prompts, and machine-readable expectations.
- [ ] Implement checks for banned generic openers, required lead phrases, maximum active numbered steps, required next steps, forbidden forced next steps, and required substrings.
- [ ] Add unit tests that run the scorer against one passing and one failing temporary response set.
- [ ] Document how to collect outputs from any supported model and score them locally.
- [ ] Run the scorer tests and confirm they pass.

### Task 4: Synchronize repository identity and release tooling

**Files:**
- Modify: `README.md`
- Modify: `chatgpt-custom-gpt/INSTRUCTIONS.md`
- Modify: `scripts/validate_skill.py`
- Modify: `scripts/build_zip.py`
- Modify: `scripts/create_release.sh`
- Modify: `scripts/publish_to_github.sh`
- Modify: `PUBLISH.md`
- Modify: `CITATION.cff`
- Modify: `CHANGELOG.md`
- Modify: `VERSION`
- Create: `docs/releases/2.0.0.md`

**Interfaces:**
- Consumes: canonical identity and package paths.
- Produces: consistent installation, packaging, validation, citation, and release behavior.

- [ ] Replace stale repository URLs, folder names, package names, badges, commands, and titles.
- [ ] Update ChatGPT availability wording to match current product documentation and retain the Custom GPT fallback.
- [ ] Strengthen validation for Agent Skills name constraints, description length, compatibility length, version synchronization, referenced files, and stale identity strings.
- [ ] Keep deterministic ZIP output and SHA-256 release assets.
- [ ] Document the breaking v2 rename and migration path.

### Task 5: Verify and merge

**Files:**
- Review: all changed files.

**Interfaces:**
- Consumes: completed v2 branch.
- Produces: a reviewed pull request merged to `main`.

- [ ] Run all local static checks available through repository scripts or equivalent source inspection.
- [ ] Review the complete diff for stale names, contradictions, placeholders, overly rigid rules, and missing attribution.
- [ ] Open a pull request with a precise summary and test evidence.
- [ ] Review the PR diff and checks, fix any issues found, and squash-merge to `main`.
