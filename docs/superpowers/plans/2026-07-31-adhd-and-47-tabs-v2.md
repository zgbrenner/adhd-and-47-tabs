# ADHD & 47 Tabs v2 Implementation Record

**Status:** Implemented, reviewed, and merged through pull request #18, with the canonical package follow-up on `fix/publish-v2-package`.

**Goal:** Ship a coherent v2 Agent Skill with adaptive response rules, canonical naming, behavior evaluations, stronger validation, and reliable local packaging.

## Completed work

### 1. Repository contracts

- [x] Standardized the canonical slug as `adhd-and-47-tabs` and version as `2.0.0`.
- [x] Removed the retired v1 skill folder and stale v1 ZIP.
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
- [x] Added `scripts/test_score_responses.py` for passing, failing, and malformed response fixtures.
- [x] Documented model-agnostic collection, scoring, and human review in `docs/EVALUATION.md`.

### 4. Identity, packaging, and release preparation

- [x] Synchronized repository URLs, package names, commands, citations, support routes, and Custom GPT instructions.
- [x] Added deterministic compressed ZIP packaging with one canonical top-level folder.
- [x] Added automatic SHA-256 generation and verification.
- [x] Track only `dist/adhd-and-47-tabs.zip` and `dist/SHA256SUMS` so the repository always exposes a working verified package.
- [x] Replaced automatic repository and release publishing scripts with explicit reviewed Git operations and local release preparation.
- [x] Documented the breaking rename and migration path.

### 5. Verification and review

- [x] Ran the validator, ZIP builder, repository contracts, and scorer regression tests using the branch sources.
- [x] Confirmed ZIP integrity, the single-folder package contract, and checksum correctness.
- [x] Verified every packaged file matched the merged GitHub source byte-for-byte by Git blob hash.
- [x] Reviewed the pull-request diff for stale names, contradictions, placeholders, rigid rules, and missing attribution.
- [x] Corrected evaluation-guide, platform-prerequisite, architecture, and package-publication drift found during review.

## Final architecture

```text
adhd-and-47-tabs/
├── adhd-and-47-tabs/          # Uploadable Agent Skill source
├── evals/                     # Portable behavior scenarios
├── scripts/                   # Validation, scoring, packaging, release preparation
├── docs/                      # Evaluation, design, release, and community documentation
├── chatgpt-custom-gpt/        # Custom GPT fallback
├── dist/                      # Tracked canonical ZIP and checksum only
└── .github/                   # Issue and discussion templates only
```

## Verification commands

```bash
make check
python3 scripts/score_responses.py --responses responses.jsonl
make release
gh skill publish --dry-run
```

`gh skill publish --dry-run` remains an optional external specification check. GitHub Releases may mirror the tracked canonical assets, but the public repository download does not depend on release publication.
