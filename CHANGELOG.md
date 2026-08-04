# Changelog

All notable changes to ADHD & 47 Tabs are documented here.

## [3.0.0] — 2026-08-04

### Added

- Six adaptive modifiers: Friction, Reorientation, Memory offload, Decision, Recovery, and Finish.
- A compact `You are here: goal → verified state → next action` interruption-recovery breadcrumb.
- Active, Ready, Blocked, and Parked working-set semantics.
- Conversation controls: `one thing`, `map it`, `resume`, `park that`, `more detail`, `less detail`, `why this`, and stop mode.
- Reuse of reliable conversation details at the point of action.
- A repeated-failure circuit breaker that separates known evidence, the likely wrong assumption, and one diagnostic.
- Finish-line scope protection and observable definitions of done.
- Explicit handling of reversible defaults, irreversible actions, false urgency, optional timeboxes, and user-provided recovery time.
- Focused interaction-pattern and quick-reference documents.
- A schema-v2 provider-neutral evaluation format with single-turn and multi-turn cases.
- Text, JSON, and Markdown evaluation reports with category summaries.
- Structural assertions for generic closers, headings, questions, bullets, total list items, ordered content, and first-line patterns.
- A detailed open-source and accessibility research ledger.

### Changed

- Expanded the regression suite from 12 to 47 cases across 15 categories.
- Reworked examples from 12 basic scenarios to 32 interaction and edge-case examples.
- Hardened deterministic ZIP generation with fixed timestamps, permissions, entry order, atomic writes, and byte-level source verification.
- Strengthened local validation for behavior signals, controls, progressive disclosure, multi-turn coverage, research attribution, and canonical version surfaces.
- Updated installation guidance for current Claude, ChatGPT, Codex, and GitHub Copilot skill workflows.
- Clarified that active-work limits never truncate requested artifacts or necessary high-stakes detail.

### Preserved

- Canonical slug and package: `adhd-and-47-tabs`.
- Four base contracts: Answer, Action, Artifact, and Project update.
- MIT license and upstream attribution.
- No hosted CI, GitHub Actions, API keys, executable skill code, telemetry, or third-party Python dependencies.

## [2.0.0] — 2026-07-31

- Introduced the four response contracts.
- Reframed the goal as lower cognitive load rather than minimum word count.
- Added progressive disclosure, ranked choices, bounded steps, definitions of done, project-state restoration, and explicit exceptions.
- Added 12 provider-neutral scenarios, a local structural scorer, deterministic packaging, and canonical identity cleanup.

## [1.1.0] — 2026-07-22

- Expanded the upstream concept for cross-platform knowledge work, planning, administrative tasks, and technical work.

## [1.0.0] — 2026-07-22

- Initial cross-platform adaptation of `ayghri/i-have-adhd`.
