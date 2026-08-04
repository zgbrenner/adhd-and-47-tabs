# ADHD & 47 Tabs v3: Adaptive Cognitive Load Design

**Date:** 2026-08-04  
**Status:** Approved for implementation by the maintainer's request to research, improve, merge, and release using best judgment.

## Goal

Turn ADHD & 47 Tabs from a strong response-formatting skill into an adaptive interaction system that helps a user enter work, stay oriented, recover after interruption, make decisions, and finish without losing necessary depth.

The project remains a portable Agent Skill, not an application, medical tool, timer, task database, or tracking service.

## Design principles

1. **Lower cognitive load, not word count.** Preserve accuracy, safety, citations, warmth, nuance, and requested depth.
2. **One visible working set.** Show the active item, at most two ready items, and only blockers that affect the active path. Keep parked work out of the active lane.
3. **Do not depend on memory.** Reuse information already provided, restate critical values where needed, and provide a short orientation breadcrumb after interruption.
4. **Short critical path.** Put the answer, artifact, recommendation, or smallest meaningful action first. Separate one instruction from another.
5. **Adaptive, not diagnostic.** Respond to the user's expressed friction, energy, uncertainty, or request without inferring a condition or presenting one attention style as universal.
6. **Reversible defaults; careful irreversible actions.** Choose sensible defaults for low-risk reversible decisions. Surface consequences and obtain required confirmation for costly, public, destructive, or irreversible actions.
7. **Evidence over theater.** Report only verified progress and reset assumptions when repeated attempts fail.

## Research synthesis

The design adapts principles rather than copying implementation or prose from other projects.

- **W3C cognitive accessibility guidance:** use clear headings and breadcrumbs for reorientation, keep critical paths short, avoid relying on memory, reuse previously entered information, separate instructions, and suppress irrelevant distraction.
- **Agent Skills specification:** keep the always-loaded skill concise and use progressive disclosure into focused references.
- **Ayoub Ghriss's `i-have-adhd`:** preserve the useful next-action, state-restatement, tangent suppression, literal-language, and repeated-debug-failure reset concepts while removing universal medical claims and rigid rules.
- **Leantime:** connect goals, planning, and execution without requiring project-management expertise.
- **Taskwarrior and Beads:** distinguish ready, blocked, and parked work so only actionable work occupies the active lane; retain enough state to recover after context loss.
- **Super Productivity:** attach relevant context to the current task and treat focus or timeboxing as optional supports, not mandatory pressure.
- **ActivityWatch:** prefer observable evidence for progress and time claims while preserving privacy and avoiding surveillance.
- **`ravila4/claude-adhd-skills`:** recover context after a break and use explicit time awareness only when it serves the user; omit platform-specific hooks from this cross-platform skill.
- **Promptfoo, OpenAI Evals, and Inspect AI:** define behavior as a declarative regression suite, include failure cases and multi-turn scenarios, and retain human review for semantic qualities that structural checks cannot measure.

A full source ledger and adoption/rejection rationale will live in `docs/RESEARCH.md`.

## Architecture

### Layer 1: Four base contracts

The existing four contracts remain because they are simple, mutually understandable, and already evaluated:

1. **Answer** — conclusion first, then required support.
2. **Action** — smallest meaningful action, bounded active work, definition of done.
3. **Artifact** — finished reusable output first.
4. **Project update** — current state, verified progress, blockers, and one active next item.

### Layer 2: Adaptive modifiers

A response may apply one or more modifiers without inventing a new primary format.

1. **Friction modifier** — shrink scope when the user is stuck, overwhelmed, tired, or unable to start. The first action must change the state of the task, not merely create busywork.
2. **Reorientation modifier** — after interruption, compaction, topic switching, or a request to resume, start with `You are here: goal → verified state → next action.` Do not replay the full history.
3. **Memory-offload modifier** — reuse names, dates, constraints, choices, paths, and decisions already present in the conversation. Put critical values next to the step that uses them. Ask only for a genuinely missing fact.
4. **Decision modifier** — recommend one path, state the deciding criterion, and include at most two materially different alternatives. For reversible choices, choose a reasonable default when authorized; for irreversible choices, surface consequences.
5. **Recovery modifier** — after repeated unsuccessful attempts, stop producing nearby variants. State what is known, name the assumption most likely to be wrong, and run or request one discriminating diagnostic.
6. **Finish modifier** — when the required outcome is close, protect the definition of done. Park polish, expansion, and adjacent ideas until the core result is verified.

Safety, emotional support, creative work, and requested depth remain overrides rather than modifiers because they can change the entire response shape.

### Layer 3: Working-set protocol

For tasks that need state tracking, use:

- **Active:** exactly one item being done now.
- **Ready:** zero to two items that become relevant immediately after Active.
- **Blocked:** only blockers that prevent Active or Ready.
- **Parked:** captured but hidden from the working response unless requested.

Do not display this vocabulary mechanically for simple questions. It is an internal organizing model and an optional visible structure for complex work.

### Layer 4: User controls

The skill recognizes concise control phrases within the current conversation:

- **`one thing`** — show only the current action and its stopping condition.
- **`map it`** — show the compact route, dependencies, and definition of done.
- **`resume`** — provide the reorientation breadcrumb and continue from the active state.
- **`park that`** — capture the tangent or optional idea without allowing it to replace the current goal.
- **`more detail` / `less detail`** — change depth without changing the underlying conclusion.
- **`why this`** — explain the deciding reason for the current recommendation or action.
- **`normal mode` / `stop 47-tabs mode` / `stop ADHD mode`** — stop applying the defaults until the user asks to resume.

These controls are conveniences, not required command syntax. Natural-language equivalents work.

## Behavioral rules

### Starting

- Prefer a minimum viable start: the smallest action that produces evidence, commits a choice, or creates a usable partial artifact.
- Do not substitute trivial setup for progress merely because it is easy.
- State a stopping condition so the user can finish a bounded block without completing the whole project.

### Continuing

- Do not ask the user to remember or re-enter information that is already available.
- Keep one scope lock: finish or intentionally park the current goal before opening an adjacent goal.
- When the user reports completion, advance the state rather than repeating the instructions they just completed.

### Recovering

- After two clearly unsuccessful iterations, or when the user says the same thing is still broken, invoke the recovery modifier.
- Distinguish evidence from hypothesis.
- Change one diagnostic variable at a time.

### Finishing

- Define done in observable terms.
- Verify before claiming completion.
- Do not let optional improvements silently become requirements.
- End completed answers and artifacts without a forced follow-up.

### Time and urgency

- Use deadlines supplied by the user and explain real sequencing constraints.
- Do not invent urgency, arbitrary timers, or precise effort estimates.
- Offer timeboxing only when it is useful and optional; include the assumption behind any estimate.
- Preserve breaks, recovery, and transition time the user explicitly includes in a plan.

## Content structure and progressive disclosure

`adhd-and-47-tabs/SKILL.md` contains the routing model, core rules, controls, exceptions, and pre-send check. It stays below the recommended 500-line loading budget.

Focused references:

- `references/interaction-patterns.md` — modifiers, working-set patterns, controls, and state transitions.
- `references/examples.md` — realistic examples and adversarial edge cases.
- `references/quick-reference.md` — a compact implementation checklist for hosts that benefit from a short reference.

Repository documentation, research notes, evaluation details, and release records remain outside the uploadable skill package.

## Evaluation design

### Suite schema

`evals/cases.json` moves to schema version 2:

```json
{
  "schema_version": 2,
  "suite": {
    "name": "ADHD & 47 Tabs",
    "version": "3.0.0"
  },
  "cases": []
}
```

A case contains either a single `prompt` or a `conversation` array. This permits multi-turn tests for resume, remembered constraints, interruption, completion advancement, and repeated failure while keeping response collection provider-neutral.

### Coverage

The release must include at least 30 cases across:

- answer, action, artifact, project update, decision;
- reorientation, memory offload, repeated-failure recovery, finish protection;
- troubleshooting, high stakes, emotional support, creative work;
- requested depth, long artifacts, user controls, and stop-mode behavior.

### Scoring

The dependency-free scorer retains deterministic structural checks and adds:

- generic closer detection;
- question, heading, bullet, and total-list-item limits;
- ordered text requirements;
- required heading alternatives;
- first-line regex checks;
- text, JSON, and Markdown reports;
- category summaries;
- explicit schema validation and useful exit codes.

Structural checks are regression aids, not semantic judges. Each case retains `review_focus` for human inspection.

## Testing and verification

`make check` must run locally with only Python's standard library and verify:

1. metadata, identity, versions, references, research ledger, and evaluation coverage;
2. scorer behavior for pass, fail, malformed, JSON, and Markdown cases;
3. deterministic package construction and checksum;
4. ZIP integrity, sorted entries, fixed timestamps, source-to-package byte equality, and absence of unsafe or extraneous files;
5. no GitHub Actions, hosted CI, API calls, credentials, third-party packages, or executable code inside the uploaded skill.

## Compatibility and migration

The slug and install path remain `adhd-and-47-tabs`, so v3 is an in-place upgrade. Version 3 is a major behavioral and evaluation-schema release, not a package rename.

Existing v2 users replace the installed ZIP. Hosts that cache skills may require restart or re-enable. The old v1 slug remains retired.

## Non-goals

- Diagnosing or treating ADHD.
- Tracking users, browsing behavior, health, or productivity metrics.
- Running timers, notifications, hooks, or background processes.
- Creating a task manager, browser extension, or web application.
- Requiring an API key, model provider, hosted evaluator, GitHub Actions, or third-party dependency.
- Forcing terse output, command vocabulary, visible state labels, or productivity framing onto every response.
