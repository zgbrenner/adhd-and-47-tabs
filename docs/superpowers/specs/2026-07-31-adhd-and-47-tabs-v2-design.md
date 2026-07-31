# ADHD & 47 Tabs v2 Design

## Goal

Turn the repository into a coherent, cross-platform Agent Skill that reduces cognitive overhead without making answers incomplete, rigid, or artificially terse.

## Canonical identity

Use one identity everywhere:

- Product title: **ADHD & 47 Tabs**
- Skill and package slug: `adhd-and-47-tabs`
- Repository: `zgbrenner/adhd-and-47-tabs`
- Release asset: `adhd-and-47-tabs.zip`
- Version: `2.0.0`

The v2 package rename is intentionally breaking and will be documented in the changelog and release notes.

## Behavioral model

The skill will optimize for **low cognitive switching cost**, not minimum word count. It will route responses into four primary shapes:

1. **Answer:** conclusion first, then the minimum evidence and caveats needed.
2. **Action:** smallest useful action first, then bounded steps and a definition of done.
3. **Artifact:** finished reusable output first, with only essential notes afterward.
4. **Project update:** current state, completed work, blockers, and the next active step.

Rules will be defaults, not traps. User-requested detail, safety, factual accuracy, emotional support, creative work, required formats, and complete deliverables override compression.

## Skill architecture

- `adhd-and-47-tabs/SKILL.md` contains the activation contract, routing logic, response contracts, exceptions, anti-patterns, and pre-send check.
- `adhd-and-47-tabs/references/examples.md` contains diverse examples, including cases where the skill should remain detailed or should not force a next step.
- `evals/cases.json` contains portable behavior scenarios and machine-readable expectations.
- `scripts/score_responses.py` scores exported model responses with dependency-free structural checks.
- `tests/test_repository.py` validates package identity, metadata, documentation, release paths, and evaluator behavior.

## Evaluation strategy

Repository checks will cover two layers:

1. **Static contract checks:** valid Agent Skills metadata, synchronized versioning, canonical paths, no stale repository names, deterministic packaging, and complete documentation.
2. **Behavior-shape checks:** scenario definitions must cover direct answers, multi-step tasks, completed artifacts, complex research, high-stakes questions, creative requests, emotional support, troubleshooting, and multi-turn project updates. The optional scorer will detect common failures such as generic preambles, excessive active steps, missing required next actions, and forced next actions after a complete answer.

The scorer is a regression aid, not a substitute for human review. Semantic accuracy and tone still require manual inspection.

## Packaging and release

Validation remains local-only and dependency-free. `make check` validates, packages, and runs tests. Releases are created locally with GitHub CLI, SHA-256 checksums, synchronized version metadata, clean-tree checks, and canonical repository verification.

## Compatibility

The package follows the Agent Skills open specification and is designed for Claude, ChatGPT Skills, Codex, GitHub Copilot, and compatible hosts. The skill itself contains no scripts, credentials, network calls, or external dependencies.

## Non-goals

- Diagnosing or treating ADHD.
- Forcing every response into five bullets.
- Replacing platform safety or citation requirements.
- Adding hosted CI or paid infrastructure.
- Adding API-dependent automated model evaluations.
