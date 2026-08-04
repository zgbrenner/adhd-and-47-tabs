# ADHD & 47 Tabs

**An adaptive AI skill for clearer answers, smaller working sets, interruption recovery, and reliable finishing.**

> Your brain has enough tabs open. Your AI does not need to add twelve more.

[![Download](https://img.shields.io/badge/download-adhd--and--47--tabs.zip-6f42c1.svg)](https://github.com/zgbrenner/adhd-and-47-tabs/raw/main/dist/adhd-and-47-tabs.zip)
[![Version](https://img.shields.io/badge/version-3.0.0-1f6feb.svg)](VERSION)
[![Evaluation](https://img.shields.io/badge/evals-47%20cases-2ea44f.svg)](evals/cases.json)
[![MIT License](https://img.shields.io/badge/license-MIT-2ea44f.svg)](LICENSE)

ADHD & 47 Tabs makes the useful part of an AI response easier to **find, start, resume, and finish**. It is not a medical tool and does not diagnose or treat ADHD. No diagnosis is required.

Version 3 moves beyond “be shorter.” It preserves necessary depth while adapting the response to the kind of work and the friction in the moment.

## What v3 does

### Four base contracts

| Need | Response begins with |
|---|---|
| **Answer** | The conclusion, result, or recommendation |
| **Action** | The smallest meaningful action |
| **Artifact** | The finished email, code, plan, prompt, table, or checklist |
| **Project update** | The last verified state and one active next item |

### Six adaptive modifiers

- **Friction:** shrinks the active scope when starting feels impossible.
- **Reorientation:** restores the thread with `You are here: goal → state → next`.
- **Memory offload:** reuses dates, names, constraints, paths, and decisions already provided.
- **Decision:** recommends one path and states the deciding criterion.
- **Recovery:** stops speculative patch loops after repeated failure and runs one discriminating diagnostic.
- **Finish:** protects the definition of done from optional scope growth.

The goal remains **lower cognitive load, not minimum word count**. Detailed requests still receive detailed answers. High-stakes questions retain the nuance and escalation guidance they need. Creative work stays creative. Emotional support is not turned into a productivity checklist.

## Small working set, complete output

For complex work, the skill keeps:

- **Active:** one item;
- **Ready:** up to two;
- **Blocked:** only what affects the active path;
- **Parked:** captured but normally hidden.

That limit applies to the working set, not the deliverable. A requested 30-item checklist still contains all 30 items, grouped so it is navigable.

## Conversation controls

Natural language works, but these short phrases are convenient:

| Say | Result |
|---|---|
| `one thing` | Only the current action and stopping condition |
| `map it` | Compact route, dependencies, definition of done, and first action |
| `resume` | Reorientation breadcrumb and continuation |
| `park that` | Capture the tangent without replacing the current goal |
| `more detail` / `less detail` | Change depth without losing the conclusion or safety |
| `why this` | Explain the deciding reason |
| `normal mode` / `stop 47-tabs mode` | Disable the defaults until asked to resume |

## Download and verify

Download the canonical [`adhd-and-47-tabs.zip`](https://github.com/zgbrenner/adhd-and-47-tabs/raw/main/dist/adhd-and-47-tabs.zip).

Verify it against [`dist/SHA256SUMS`](dist/SHA256SUMS):

```bash
sha256sum -c dist/SHA256SUMS
```

The ZIP is rebuilt deterministically from the source folder during `make check`. It contains Markdown instructions and references, one YAML host-metadata file, and the MIT license—no executable code, packages, credentials, telemetry, or network instructions.

## Install

### Claude

Claude custom skills are available on Free, Pro, Max, Team, and Enterprise plans when code execution is enabled.

1. Download the ZIP.
2. Enable **Code execution and file creation** in **Settings → Capabilities**. Team and Enterprise workspaces may use organization settings.
3. Open **Customize → Skills**.
4. Select **+ → Create skill → Upload a skill**.
5. Upload and enable the ZIP.

Official guide: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

### ChatGPT

1. Download the ZIP.
2. Open ChatGPT's **Skills** page. In the current web interface, this is under **Plugins → Skills** in the sidebar.
3. Select **Create → Upload from your computer**.
4. Upload the ZIP.

Workspace administrators may control skill creation, uploading, installation, and sharing. Personal skills may need to be installed separately on different ChatGPT surfaces.

Official guide: [Skills in ChatGPT](https://help.openai.com/en/articles/20001066).

For accounts without uploaded Skills, copy [`chatgpt-custom-gpt/INSTRUCTIONS.md`](chatgpt-custom-gpt/INSTRUCTIONS.md) into a Custom GPT named **ADHD & 47 Tabs**.

### Codex

Inside Codex, invoke the built-in installer:

```text
$skill-installer
```

Then ask it to install the `adhd-and-47-tabs` skill from this repository's `adhd-and-47-tabs` folder. For a manual user-wide install, place that folder at `~/.agents/skills/adhd-and-47-tabs`. For a repository-scoped install, place it at `.agents/skills/adhd-and-47-tabs` inside the repository. Codex detects skill changes automatically; restart only when an install or update does not appear.

The package includes `agents/openai.yaml` so ChatGPT desktop and Codex can show a clean display name, description, default prompt, and implicit-invocation policy.

Official guide: [Build skills for ChatGPT and Codex](https://developers.openai.com/codex/skills).

### GitHub Copilot

GitHub CLI 2.90.0 or later can preview and install Agent Skills:

```bash
gh skill preview zgbrenner/adhd-and-47-tabs adhd-and-47-tabs
gh skill install zgbrenner/adhd-and-47-tabs adhd-and-47-tabs --scope user
```

You can also copy the skill folder into `~/.copilot/skills`, `~/.agents/skills`, `.github/skills`, or `.agents/skills`, depending on scope.

Official guide: [Adding Agent Skills for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills).

### Universal Skills CLI

```bash
npx skills add zgbrenner/adhd-and-47-tabs --skill adhd-and-47-tabs
```

This is a third-party CLI. Its documentation says anonymous skill-usage telemetry is enabled by default; set `DISABLE_TELEMETRY=1` before the command to opt out, or use one of the manual installation paths above.

## Upgrade from v2

The slug is unchanged. Replace the installed ZIP or skill folder with v3.0.0, then restart or reload the host if it caches skills.

Version 3 changes behavior and the repository evaluation schema, not the package identity. Version 1 used the retired slug `i-have-adhd-and-47-tabs`; remove that copy so two versions do not load together.

## Read the skill

- [`adhd-and-47-tabs/SKILL.md`](adhd-and-47-tabs/SKILL.md) — always-loaded behavioral core.
- [`references/interaction-patterns.md`](adhd-and-47-tabs/references/interaction-patterns.md) — routing, state, controls, and recovery patterns.
- [`references/examples.md`](adhd-and-47-tabs/references/examples.md) — 32 examples and edge cases.
- [`references/quick-reference.md`](adhd-and-47-tabs/references/quick-reference.md) — compact host checklist.

The structure follows the Agent Skills progressive-disclosure model: concise metadata and core instructions first, focused references on demand.

## Evaluate and validate

The repository includes **47 provider-neutral cases**, including nine multi-turn scenarios, and a dependency-free scorer:

```bash
python3 scripts/score_responses.py --responses responses.jsonl
python3 scripts/score_responses.py --responses responses.jsonl --format json --output report.json
python3 scripts/score_responses.py --responses responses.jsonl --format markdown --output report.md
make check
make release
make install-hooks
```

The scorer checks structural regressions such as generic preambles and closers, forced next steps, excessive active lists, missing orientation breadcrumbs, ordered recovery sections, and requested breadth, list, paragraph, and depth preservation. Each case also includes a human-review focus because semantic quality cannot be reduced to regexes.

See [`docs/EVALUATION.md`](docs/EVALUATION.md).

This repository intentionally uses **no GitHub Actions or hosted CI**. All release checks run locally with Python's standard library and Make.

## Research and design

Version 3 synthesizes accessibility guidance and open-source patterns from W3C COGA, the Agent Skills specification, the upstream skill, Leantime, Taskwarrior, Super Productivity, ActivityWatch, Beads, Claude ADHD Skills, Promptfoo, OpenAI Evals, and Inspect AI.

The project adopts principles—not copied prose or code—and records what was deliberately rejected. See [`docs/RESEARCH.md`](docs/RESEARCH.md).

## Contributing

Behavior changes should include a regression case. Run `make check`, regenerate the tracked ZIP and checksum, and explain how the change lowers friction without deleting necessary substance.

See [`CONTRIBUTING.md`](CONTRIBUTING.md), [`SUPPORT.md`](SUPPORT.md), and [`SECURITY.md`](SECURITY.md).

## Attribution and license

Original concept and skill: [Ayoub Ghriss, `ayghri/i-have-adhd`](https://github.com/ayghri/i-have-adhd).

Cross-platform adaptation: [Zachary Brenner](https://github.com/zgbrenner).

MIT licensed. The upstream notice is preserved in [`LICENSE`](LICENSE), and adaptation history is documented in [`NOTICE.md`](NOTICE.md).
