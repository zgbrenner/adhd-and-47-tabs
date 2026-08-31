# Changelog

All notable changes to ADHD & 47 Tabs are documented here.

## [3.0.1] — 2026-08-31

### Fixed

- The pre-push hook's package-drift check pointed at the retired v1 ZIP name, so it never compared anything; it now diffs `dist/adhd-and-47-tabs.zip` and `dist/SHA256SUMS`, and the stale-name validation scan now covers the hook, the hook installer, and `docs/INSTALL.md`.
- `docs/INSTALL.md` still described the retired `i-have-adhd-and-47-tabs` slug and repository; it now matches the canonical package and README instructions.
- Removed a forced `Next:` line from examples 2 and 16, which modeled the exact failure mode the skill forbids.
- The scorer now detects `Next steps:` and heading-form `## Next:` lines, normalizes CRLF line endings before counting paragraphs, excludes fenced code blocks from heading and list counts, catches a generic closer followed by a trailing note, and no longer lets ordered-substring checks satisfy one item inside another.
- The checksum-verification command in README and PUBLISH now runs from `dist/` so `sha256sum -c` resolves the bare filename.
- Aligned the `one thing` and `map it` control definitions across SKILL.md, the quick reference, and the Custom GPT instructions (essential safety warnings and the first active item are part of the contract everywhere).

### Changed

- Rewrote the frontmatter description to name the skill's actual triggers — ADHD, executive function, focus difficulty, feeling overwhelmed, stuck starts, interruptions — and what the skill does, so hosts can route to it reliably.
- Removed the three legacy Markdown issue templates that bypassed the structured forms and `blank_issues_enabled: false`.
- Updated stale `1.1.0` version strings in the bug-report template and directory-submission notes.
- The multi-turn evaluation floor now matches the documented nine cases, and release-note/citation checks derive their messages from the current version.
- Added `.gitattributes` (`* -text`) so checkouts on every platform keep byte-identical sources for deterministic packaging.

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
