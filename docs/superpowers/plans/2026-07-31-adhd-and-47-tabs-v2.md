# ADHD & 47 Tabs v2 Implementation Record

**Status:** Implemented and reviewed on `improve/adhd-47-tabs-v2`.

**Goal:** Ship a coherent v2 Agent Skill with adaptive response rules, canonical naming, behavior evaluations, stronger validation, and reliable local packaging.

## Completed work

### 1. Repository contracts

- [x] Standardized the canonical slug as `adhd-and-47-tabs` and version as `2.0.0`.
- [x] Removed the retired v1 skill folder and tracked v1 ZIP.
- [x] Added validation for metadata, version synchronization, supporting files, evaluation coverage, duplicate JSON keys, and stale active references.
- [x] Added dependency-free package and repository contract checks.

### 2. Skill package

- [x] Added the canonical self-contained package under `adhd-and-47-tabs/`.
- [x] Implemented answer, action, artifact, and project-update contracts.
- [x] Added progressive disclosure, bounded active work, ranked alternatives, definitions of done, sequential troubleshooting, and evidence-based progress reporting.
- [x] Added exceptions for requested depth, high-stakes accuracy, emotional support, creative work, ambiguity, and irreversible actions.
- [x] Expanded examples to cover both compression and cases where detail must be preserved.

### 3. Behavior evaluation

- [x] Added 12 portable scenarios across answer, action, artifact, project-update, troubleshooting, high-stakes, creative, and emotional-support categories.
- [x] Added `scripts/score_responses.py` with structural checks and explicit exit codes.
- [x] Documented model-agnostic collection, scoring, and human review in `docs/EVALUATION.md`.
- [x] Exercised the scorer with passing and failing response fixtures.

### 4. Identity, packaging, and release preparation

- [x] Synchronized repository URLs, package names, badges, commands, citations, support routes, and Custom GPT instructions.
- [x] Added deterministic compressed ZIP packaging with one canonical top-level folder.
- [x] Ignored generated ZIP and checksum files to prevent stale-binary drift.
- [x] Replaced automatic repository and release publishing scripts with explicit reviewed Git operations and local release preparation.
- [x] Added `scripts/prepare_release.py` to run checks and create `adhd-and-47-tabs.zip` plus `SHA256SUMS`.
- [x] Documented the breaking rename and migration path.

### 5. Verification and review

- [x] Ran the validator, ZIP builder, and repository contract scripts in an isolated local fixture using the branch sources.
- [x] Confirmed ZIP integrity and the single-folder package contract.
- [x] Reviewed the pull-request diff for stale names, contradictions, placeholders, rigid rules, and missing attribution.
- [x] Corrected evaluation-guide and architecture-documentation drift found during review.

## Final architecture

```text
adhd-and-47-tabs/
├── adhd-and-47-tabs/          # Uploadable Agent Skill
├── evals/                     # Portable behavior scenarios
├── scripts/                   # Validation, scoring, packaging, release preparation
├── docs/                      # Evaluation, design, release, and community documentation
├── chatgpt-custom-gpt/        # Custom GPT fallback
├── dist/                      # Generated locally; release binaries are ignored
└── .github/                   # Issue and discussion templates only
```

## Verification commands

```bash
make check
python3 scripts/score_responses.py --responses responses.jsonl
make release
gh skill publish --dry-run
```

`gh skill publish --dry-run` remains an optional external specification check. GitHub Release creation and asset upload remain explicit maintainer actions.
