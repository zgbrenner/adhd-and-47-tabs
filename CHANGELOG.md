# Changelog

All notable changes are documented here.

## 2.0.0 — 2026-07-31

### Breaking change

- Renamed the canonical skill folder and package from `i-have-adhd-and-47-tabs` to `adhd-and-47-tabs` so the repository, skill name, install path, release asset, and product identity finally match.
- Existing installations should remove or disable the v1 skill before installing v2 to avoid loading both copies.

### Skill behavior

- Rebuilt the skill around four explicit response contracts: answer, action, artifact, and project update.
- Changed the optimization target from raw brevity to lower cognitive load, preserving necessary detail, citations, warmth, uncertainty, and safety guidance.
- Stopped forcing a `Next:` action after complete factual answers and finished deliverables.
- Added progressive disclosure, bounded active work, definitions of done, ranked alternatives, evidence-based progress updates, and sequential troubleshooting.
- Added explicit exceptions for high-stakes questions, emotional support, creative work, requested depth, ambiguity, and irreversible actions.
- Expanded examples to cover research, studying, writing, planning, code, troubleshooting, legal and financial questions, emotional support, creative work, and long requested artifacts.

### Quality and packaging

- Added a portable behavior-evaluation suite with cross-platform scenarios and a dependency-free JSONL response scorer.
- Strengthened validation for Agent Skills metadata, synchronized versioning, referenced files, behavior requirements, evaluation coverage, duplicate JSON keys, stale identity strings, and loading-budget limits.
- Switched to a compressed, deterministic release ZIP with one canonical top-level folder.
- Removed stale generated package artifacts from the source contract and made local release generation authoritative.
- Updated installation, support, security, contribution, directory-submission, citation, publishing, and Custom GPT documentation.
- Preserved local-only validation with no GitHub Actions, hosted CI, paid services, API keys, or third-party Python packages.

## 1.1.0 — 2026-07-22

- Improved the skill description so it states both the behavior and realistic trigger signals.
- Replaced self-referential packaging examples with general-purpose error handling examples.
- Removed undocumented OpenAI metadata and the redundant root-level ZIP copy.
- Added package freshness checks, broader Python coverage, safer publishing, and stray-file filtering.
- Standardized repository commands on `python3`.
- Added stable GitHub Release assets with SHA-256 verification.
- Added Codex, GitHub Copilot, and universal Skills CLI installation paths.
- Added structured issue and discussion forms, support routing, and starter community discussions.
- Expanded contribution guidance, adopted Contributor Covenant 2.1, and strengthened security reporting.
- Added a share-ready social preview and directory submission kit.

## 1.0.0 — 2026-07-21

- Renamed the adaptation to **I Have ADHD and 47 Tabs**.
- Generalized the skill for research, school, writing, planning, administration, everyday questions, and technical work.
- Added Claude custom-skill and ChatGPT Skill packaging.
- Added a Custom GPT fallback.
- Added explicit attribution to Ayoub Ghriss and the upstream project.
- Added validation, reproducible ZIP packaging, tests, CI, and contribution documentation.
