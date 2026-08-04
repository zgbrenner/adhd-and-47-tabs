# Research ledger

Version 3 was designed from a broad review of cognitive-accessibility guidance, open-source productivity systems, agent-memory tools, and evaluation frameworks. The project adopts **principles and interaction patterns**, not copied prose or code.

For each source, this ledger records what was adopted, how it was transformed for a portable AI skill, and what was deliberately rejected.

## 1. W3C cognitive accessibility guidance

**Primary sources**

- [Making Content Usable for People with Cognitive and Learning Disabilities](https://www.w3.org/TR/coga-usable/)
- [Help Users Focus](https://www.w3.org/WAI/WCAG2/supplemental/objectives/o5-user-focus/)
- [Do Not Rely on Users Calculations or Memorizing Information](https://www.w3.org/WAI/WCAG2/supplemental/patterns/o6p05-low-cognition/)
- [All Supplemental Guidance](https://www.w3.org/WAI/WCAG2/supplemental/)

**Adopted**

- Clear headings and breadcrumbs help users reorient after distraction.
- Multi-step processes should carry forward the information needed for the current step.
- Critical paths should be short and unnecessary content should not interrupt the task.
- Instructions should be separated and written in clear, literal language.
- Personalization matters because cognitive needs vary across people, contexts, and time.

**Transformation**

The skill converts those interface-design patterns into conversational behavior: a compact **You are here:** breadcrumb, point-of-use restatement of dates and constraints, one active working item, progressive disclosure, and user-controlled depth.

**Not adopted**

- Claims that every person with ADHD has the same working-memory capacity or executive-function pattern.
- Any representation that supplemental guidance is a normative WCAG conformance requirement.
- Any attempt to diagnose a user from conversational behavior.

## 2. Agent Skills open specification

**Primary source**

- [Agent Skills specification](https://agentskills.io/specification)

**Adopted**

- A concise `SKILL.md` with required metadata.
- Focused, on-demand reference files.
- One-level progressive disclosure so the always-loaded context remains manageable.
- Portable, provider-neutral packaging.

**Transformation**

The behavioral core stays below 500 lines and links to three focused references: interaction patterns, examples, and a quick reference.

**Not adopted**

- Executable scripts inside the uploaded skill. This project needs no runtime code.
- Provider-specific tool instructions in the behavioral package.

## 3. Upstream `i-have-adhd`

**Primary source**

- [Ayoub Ghriss, `ayghri/i-have-adhd`](https://github.com/ayghri/i-have-adhd)

**Adopted**

- Put the useful action or answer first.
- Bound multi-step work.
- Restate state across turns.
- Suppress tangents.
- Make verified progress visible.
- Reset the assumption after a repeated debugging spiral.
- Prefer literal language to opaque idioms.

**Transformation**

Version 3 preserves those strengths but routes responses through four contracts and six modifiers. It removes universal cognitive claims, rigid list caps on requested artifacts, mandatory next steps after complete answers, and pressure-inducing precise estimates.

**Not adopted**

- Diagnostic or universal statements about what ADHD “changes” for every reader.
- A rule that every unfinished answer must end with a task, even when the user asked only for information.
- Hard-coded time estimates unsupported by scope or evidence.

## 4. Leantime

**Primary source**

- [Leantime](https://github.com/Leantime/leantime)

**Adopted**

- Connect goals, planning, and execution rather than treating a task list as the whole system.
- Make dependencies, milestones, and status visible.
- Design for users who are not project-management experts.
- Treat neurodivergent accessibility as a product-design concern.

**Transformation**

The skill uses the Project-update contract and Finish modifier to connect the goal, verified state, active work, blockers, and observable definition of done without exposing a full project-management interface.

**Not adopted**

- Kanban, Gantt, sprint, timesheet, and account-management features.
- Any claim that one project-management method works for every neurodivergent user.

## 5. Taskwarrior

**Primary source**

- [Taskwarrior](https://github.com/GothenburgBitFactory/taskwarrior)

**Adopted**

- Differentiate actionable work from blocked work.
- Let dependencies affect what appears ready.
- Give the next actionable item stronger prominence than the backlog.
- Keep priority explainable rather than arbitrary.

**Transformation**

The skill uses an Active/Ready/Blocked/Parked model. Only one item is Active, no more than two are Ready, and blockers appear only when they affect the active path.

**Not adopted**

- A numerical urgency formula.
- Requiring users to maintain metadata, priorities, or a task database for ordinary conversations.

## 6. Super Productivity

**Primary source**

- [Super Productivity](https://github.com/super-productivity/super-productivity)

**Adopted**

- Attach relevant context to the current task.
- Make focus and timeboxing optional supports.
- Preserve privacy and local control.
- Include breaks and anti-procrastination supports without equating them with productivity success.

**Transformation**

The skill places critical context beside the action that uses it and permits optional, assumption-labeled timeboxes. It explicitly preserves user-requested recovery and transition time.

**Not adopted**

- Mandatory Pomodoro cycles, time tracking, notifications, or behavioral metrics.
- Any background process or account.

## 7. ActivityWatch

**Primary source**

- [ActivityWatch](https://github.com/ActivityWatch/activitywatch)

**Adopted**

- Prefer observable evidence over intuition when making time or progress claims.
- Keep privacy and local-first design central.

**Transformation**

The skill reports progress only from verified outcomes and labels estimates with assumptions. It does not collect activity data.

**Not adopted**

- Surveillance, passive activity capture, analytics, or productivity scoring.
- Inferring attention or health from computer use.

## 8. Beads

**Primary source**

- [Beads](https://github.com/gastownhall/beads)

**Adopted**

- Preserve enough structured state to recover after context loss.
- Distinguish ready work, blockers, and parked or dependent work.
- Make the current actionable item easy to recover after a long interruption.
- Avoid flat plans that lose dependency information.

**Transformation**

The portable skill cannot maintain a database, so it uses a concise conversational state capsule: goal, verified state, Active, Ready, Blocked, and Parked. The **resume** control reconstructs the critical path from reliable conversation context.

**Not adopted**

- A persistent database, Git/Dolt synchronization, issue graph, hooks, or multi-agent coordination.
- Pretending the skill remembers across sessions when the host does not provide memory.

## 9. Claude ADHD Skills

**Primary source**

- [`ravila4/claude-adhd-skills`](https://github.com/ravila4/claude-adhd-skills)

**Adopted**

- Explicitly reconstruct context after a break.
- Treat time awareness and nudges as situational supports.
- Make external notes capable of carrying session state.
- Ask rather than assume when personal workflow details are truly missing.

**Transformation**

Version 3 adds reorientation and memory-offload behavior that works in any compatible host. It does not depend on Obsidian, hooks, SQLite, or a particular CLI.

**Not adopted**

- Mandatory journaling, a required Obsidian vault, platform hooks, or timed alerts.
- An assumption that every user wants interruption prompts.

## 10. Promptfoo

**Primary source**

- [Promptfoo](https://github.com/promptfoo/promptfoo)

**Adopted**

- Test-driven prompt and behavior development.
- Declarative cases and assertions.
- Regression testing of core use cases and failure cases.
- Local, private evaluation and machine-readable results.

**Transformation**

The repository keeps a dependency-free JSON suite and scorer tailored to response structure. It supports text, JSON, and Markdown reports without requiring a provider or API key.

**Not adopted**

- Hosted dashboards, provider adapters, red-teaming infrastructure, Node.js, or external packages.
- Treating structural regex checks as sufficient semantic evaluation.

## 11. OpenAI Evals

**Primary source**

- [OpenAI Evals](https://github.com/openai/evals)

**Adopted**

- Build evaluations around the real use cases the behavior must serve.
- Keep reusable data separate from scoring logic.
- Compare behavior across model and prompt changes.
- Make custom evaluation possible without hard-coding every case.

**Transformation**

Cases are provider-neutral, have stable IDs, and carry human-review criteria alongside deterministic assertions.

**Not adopted**

- API dependencies, model-specific completion functions, cloud logging, or model-graded scoring as a release requirement.

## 12. Inspect AI

**Primary source**

- [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)

**Adopted**

- Multi-turn scenarios matter for agent and conversational behavior.
- Evaluation should support different scoring techniques and auditable results.
- Reproducibility and clear test components improve confidence.

**Transformation**

Schema version 2 supports either a single `prompt` or a complete `conversation`. The local scorer remains deterministic, while `review_focus` preserves human semantic inspection.

**Not adopted**

- A full evaluation runtime, model execution, sandboxes, external dependencies, or model judges.
- Any claim that passing structural checks proves universal model quality.

## 13. Current host and installation documentation

**Primary sources**

- [Build skills for ChatGPT and Codex](https://developers.openai.com/codex/skills)
- [Skills in ChatGPT](https://help.openai.com/en/articles/20001066)
- [Plugins in Codex](https://help.openai.com/en/articles/20001256-plugins-in-codex/)
- [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
- [Adding Agent Skills for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
- [Vercel Labs `skills` CLI](https://github.com/vercel-labs/skills)
- [`skills` CLI telemetry documentation](https://www.skills.sh/docs/cli)

**Adopted**

- Current standalone-skill paths for ChatGPT desktop, Codex CLI, Codex IDE, Claude, and GitHub Copilot.
- Codex repository and user skill locations under `.agents/skills` and `~/.agents/skills`.
- Optional `agents/openai.yaml` presentation and invocation metadata.
- Explicit security guidance to review third-party skills.
- A precise `npx skills` command as an optional cross-agent convenience, paired with a visible telemetry opt-out note.
- Portability across products that implement the open standard.

**Transformation**

The package now includes instruction-only OpenAI host metadata but does not make core behavior product-specific. The README distinguishes local skills from plugin distribution and treats third-party installers as optional conveniences rather than trusted prerequisites.

**Not adopted**

- The deprecated `openai/skills` catalog as a current installation source.
- A product-specific plugin wrapper, connector, MCP server, executable installer, or dependency merely to distribute this single instruction-only skill.
- Silent third-party installer telemetry; the README calls out the opt-out variable.
- Any promise that installation menus, plan eligibility, preview commands, or host paths will remain unchanged indefinitely.

## Design conclusions

The most important synthesis is not “make answers shorter.” It is:

1. Put substance first.
2. Keep a small visible working set.
3. Carry reliable information forward.
4. Restore orientation after interruption.
5. Stop speculative loops and create evidence.
6. Protect the definition of done.
7. Let the user control depth and scope.
8. Preserve nuance, safety, warmth, and requested breadth.

Those conclusions drive the skill, examples, evaluation suite, and release tests.
