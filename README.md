# ADHD & 47 Tabs

<strong>A cross-platform AI skill for clearer answers, smaller active workloads, and fewer cognitive dead ends.</strong>

> **Your brain has enough tabs open. Your AI does not need to add twelve more.**

<a href="https://github.com/zgbrenner/adhd-and-47-tabs/releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/release/zgbrenner/adhd-and-47-tabs?display_name=tag"></a>
<a href="https://github.com/zgbrenner/adhd-and-47-tabs/releases/latest/download/adhd-and-47-tabs.zip"><img alt="Download skill" src="https://img.shields.io/badge/download-adhd--and--47--tabs.zip-6f42c1.svg"></a>
<a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-2ea44f.svg"></a>

**ADHD & 47 Tabs** changes the shape of AI responses so the useful part is easier to find, start, and finish. It is not a medical tool and does not diagnose or treat ADHD. No diagnosis is required to use it.

## What it changes

The skill uses four response contracts:

1. **Answer:** conclusion first, then the evidence and caveats needed to trust it.
2. **Action:** smallest useful action first, bounded steps, and a definition of done.
3. **Artifact:** finished email, code, plan, prompt, or other reusable output first.
4. **Project update:** current state, verified progress, blockers, and one active next step.

The goal is **lower cognitive load, not minimum word count**. Detailed requests still receive detailed answers.

## Download

**[Download the latest ZIP](https://github.com/zgbrenner/adhd-and-47-tabs/releases/latest/download/adhd-and-47-tabs.zip)**

Each release includes `SHA256SUMS`. The ZIP contains exactly one top-level folder named `adhd-and-47-tabs`.

### Upgrading from v1

Version 2 renamed the package from `i-have-adhd-and-47-tabs` to `adhd-and-47-tabs`. Remove or disable the old copy before installing v2 so both versions do not load together.

## Install in Claude

1. Download the latest ZIP.
2. Open **Customize → Skills**.
3. Select **+ → Create skill → Upload a skill**.
4. Upload the ZIP and enable **ADHD & 47 Tabs**.

Official guide: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## Install in ChatGPT Skills

Personal Skills availability depends on your ChatGPT plan and workspace settings.

1. Download the latest ZIP.
2. Open **Plugins** in the ChatGPT sidebar.
3. Select **Skills → Create → Upload from your computer**.
4. Upload the ZIP.

Official guide: [Skills in ChatGPT](https://help.openai.com/en/articles/20001066).

### Custom GPT fallback

When direct Skills upload is unavailable, copy [`chatgpt-custom-gpt/INSTRUCTIONS.md`](chatgpt-custom-gpt/INSTRUCTIONS.md) into a Custom GPT named **ADHD & 47 Tabs**.

## Install in Codex

```text
$skill-installer install https://github.com/zgbrenner/adhd-and-47-tabs/tree/main/adhd-and-47-tabs
```

Restart Codex after installation.

## Install for GitHub Copilot

GitHub CLI 2.90.0 or later can preview and install Agent Skills:

```bash
gh skill preview zgbrenner/adhd-and-47-tabs adhd-and-47-tabs
gh skill install zgbrenner/adhd-and-47-tabs adhd-and-47-tabs --scope user
gh skill publish --dry-run
```

Omit `--scope user` to install it only for the current project.

Official guide: [Adding Agent Skills for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills).

## Install with the universal Skills CLI

```bash
npx skills add zgbrenner/adhd-and-47-tabs
```

## Core behavior

- Lead with the answer, finished output, recommendation, or first action.
- Show one active path by default and rank meaningful alternatives.
- Keep the active working set small; group longer requested material instead of truncating it.
- Preserve the thread across multi-turn projects without replaying the entire history.
- Make progress concrete and never claim unverified completion.
- Troubleshoot sequentially instead of opening several diagnostic branches.
- Do not force a next step after a complete answer or finished deliverable.
- Remove generic preambles, recap paragraphs, tangents, and empty closers.

The complete instructions live in [`adhd-and-47-tabs/SKILL.md`](adhd-and-47-tabs/SKILL.md).

## Evaluate behavior

The repository includes 14 cross-platform scenarios and a dependency-free scorer.

```bash
python3 scripts/score_responses.py --responses responses.jsonl
```

See [`docs/EVALUATION.md`](docs/EVALUATION.md) for the response format and human-review process.

## Local validation

This repository intentionally uses **no GitHub Actions or hosted CI**. Validation, packaging, and releases run locally with no third-party Python packages.

```bash
make check
make install-hooks
```

## Repository map

```text
adhd-and-47-tabs/
├── adhd-and-47-tabs/             # Uploadable skill source
├── evals/                        # Behavior scenarios
├── chatgpt-custom-gpt/           # Custom GPT fallback
├── docs/                         # Evaluation and release notes
├── scripts/                      # Validation, scoring, packaging, publishing
├── tests/                        # Repository contract tests
├── .githooks/                    # Optional local checks
└── .github/                      # Issue and discussion templates only
```

## Community

- Ask installation and usage questions in [Discussions](https://github.com/zgbrenner/adhd-and-47-tabs/discussions).
- Report reproducible bugs through the [issue forms](https://github.com/zgbrenner/adhd-and-47-tabs/issues/new/choose).
- Read [`SUPPORT.md`](SUPPORT.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Attribution

**Original concept and skill:** [Ayoub Ghriss, `ayghri/i-have-adhd`](https://github.com/ayghri/i-have-adhd)

**Cross-platform adaptation:** [Zachary Brenner](https://github.com/zgbrenner)

The original copyright notice is preserved in [`LICENSE`](LICENSE), and the adaptation history is documented in [`NOTICE.md`](NOTICE.md).

## License

MIT. Use it, fork it, remix it, and close at least one tab.
