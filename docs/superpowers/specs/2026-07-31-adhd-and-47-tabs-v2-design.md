# ADHD & 47 Tabs v2 Design

## Goal

Turn the repository into a coherent cross-platform Agent Skill that reduces cognitive overhead without making answers incomplete, rigid, or artificially terse.

## Canonical identity

- Product title: **ADHD & 47 Tabs**
- Skill and package slug: `adhd-and-47-tabs`
- Repository: `zgbrenner/adhd-and-47-tabs`
- Release asset: `adhd-and-47-tabs.zip`
- Version: `2.0.0`

The v2 package rename is intentionally breaking and is documented in the changelog and release notes.

## Behavioral model

The skill optimizes for **lower cognitive load, not minimum word count**. It routes responses into four primary shapes:

1. **Answer:** conclusion first, then the evidence and caveats needed to trust it.
2. **Action:** smallest useful action first, followed by bounded steps and a definition of done.
3. **Artifact:** finished reusable output first, with only essential notes afterward.
4. **Project update:** current state, completed work, blockers, and the next active step.

These are defaults, not traps. Safety, factual accuracy, user-requested detail, emotional support, creative work, citations, and required formats override compression.

## Final architecture

- `adhd-and-47-tabs/SKILL.md` contains activation guidance, routing logic, response contracts, exceptions, failure modes, and the pre-send check.
- `adhd-and-47-tabs/references/examples.md` contains examples and edge cases.
- `evals/cases.json` contains portable behavior scenarios and machine-readable expectations.
- `scripts/score_responses.py` scores exported responses using dependency-free structural checks.
- `scripts/validate_skill.py` validates metadata, identity, versioning, evaluation coverage, supporting files, and stale references.
- `scripts/build_zip.py` creates a deterministic compressed ZIP with one canonical top-level folder.
- `scripts/test_repository.py` checks the generated package and repository contracts.
- `scripts/prepare_release.py` runs the checks and creates the ZIP and SHA-256 checksum for explicit maintainer review and upload.

## Evaluation strategy

Quality checks have two layers:

1. **Static contracts:** valid metadata, synchronized versions, canonical paths, complete supporting files, deterministic packaging, unique evaluation IDs, and no stale v1 identity in active surfaces.
2. **Behavior shape:** scenarios cover direct answers, tasks, finished artifacts, deep explanations, high-stakes questions, creative work, emotional support, troubleshooting, and multi-turn project updates.

The scorer is a regression aid, not a substitute for human review. Factual accuracy, sourcing, empathy, creative quality, and semantic completeness still require inspection.

## Packaging and release

Validation remains local-only and dependency-free. `make check` validates the source, builds the ZIP, and runs repository checks. `make release` prepares the ZIP and `SHA256SUMS`; publication to GitHub Releases remains an explicit maintainer action.

Generated archives are ignored by Git so stale binaries cannot drift from source.

## Compatibility

The package follows the Agent Skills open specification and is designed for Claude, ChatGPT Skills, Codex, GitHub Copilot, and compatible hosts. The skill itself contains no scripts, credentials, network calls, or external dependencies.

## Non-goals

- Diagnosing or treating ADHD.
- Forcing every response into five bullets.
- Replacing platform safety or citation requirements.
- Adding hosted CI or paid infrastructure.
- Adding API-dependent automated model evaluations.
