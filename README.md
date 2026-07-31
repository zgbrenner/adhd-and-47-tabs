# ADHD & 47 Tabs

**A cross-platform AI skill for clearer answers, smaller active workloads, and fewer cognitive dead ends.**

> Your brain has enough tabs open. Your AI does not need to add twelve more.

[![Latest release](https://img.shields.io/github/v/release/zgbrenner/adhd-and-47-tabs?display_name=tag)](https://github.com/zgbrenner/adhd-and-47-tabs/releases/latest)
[![Download](https://img.shields.io/badge/download-adhd--and--47--tabs.zip-6f42c1.svg)](https://github.com/zgbrenner/adhd-and-47-tabs/releases/latest/download/adhd-and-47-tabs.zip)
[![MIT License](https://img.shields.io/badge/license-MIT-2ea44f.svg)](LICENSE)

ADHD & 47 Tabs makes the useful part of an AI response easier to find, start, and finish. It is not a medical tool and does not diagnose or treat ADHD. No diagnosis is required.

## How it works

The skill uses four response contracts:

1. **Answer:** conclusion first, then necessary evidence and caveats.
2. **Action:** smallest useful action first, bounded steps, and a definition of done.
3. **Artifact:** finished email, code, plan, prompt, or checklist first.
4. **Project update:** current state, verified progress, blockers, and one active next step.

The goal is **lower cognitive load, not minimum word count**. Detailed requests still receive detailed answers.

## Download and upgrade

[Download `adhd-and-47-tabs.zip`](https://github.com/zgbrenner/adhd-and-47-tabs/releases/latest/download/adhd-and-47-tabs.zip). Each release also includes `SHA256SUMS`.

Version 2 renamed the package from `i-have-adhd-and-47-tabs`. Remove or disable the old copy before installing v2 so both versions do not load together.

## Claude

1. Download the ZIP.
2. Open **Customize → Skills**.
3. Select **+ → Create skill → Upload a skill**.
4. Upload and enable **ADHD & 47 Tabs**.

Official guide: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## ChatGPT

Personal Skills availability depends on plan and workspace settings.

1. Download the ZIP.
2. Open **Plugins** in the ChatGPT sidebar.
3. Select **Skills → Create → Upload from your computer**.
4. Upload the ZIP.

Official guide: [Skills in ChatGPT](https://help.openai.com/en/articles/20001066).

For a Custom GPT fallback, copy [`chatgpt-custom-gpt/INSTRUCTIONS.md`](chatgpt-custom-gpt/INSTRUCTIONS.md) into a GPT named **ADHD & 47 Tabs**.

## Codex

```text
$skill-installer install https://github.com/zgbrenner/adhd-and-47-tabs/tree/main/adhd-and-47-tabs
```

Restart Codex after installation.

## GitHub Copilot

GitHub CLI 2.90.0 or later can preview and install Agent Skills:

```bash
gh skill preview zgbrenner/adhd-and-47-tabs adhd-and-47-tabs
gh skill install zgbrenner/adhd-and-47-tabs adhd-and-47-tabs --scope user
gh skill publish --dry-run
```

Official guide: [Adding Agent Skills for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills).

## Universal Skills CLI

```bash
npx skills add zgbrenner/adhd-and-47-tabs
```

## Core behavior

- Lead with the answer, finished output, recommendation, or first action.
- Show one active path and rank meaningful alternatives.
- Keep the active working set small without truncating requested artifacts.
- Preserve project state without replaying the full history.
- Report progress only when it is verified.
- Troubleshoot sequentially.
- Do not force a next step after a complete answer.
- Remove generic preambles, recaps, tangents, and empty closers.

Read the full skill at [`adhd-and-47-tabs/SKILL.md`](adhd-and-47-tabs/SKILL.md).

## Evaluate and validate

The repository includes 12 cross-platform scenarios and a dependency-free scorer:

```bash
python3 scripts/score_responses.py --responses responses.jsonl
make check
make install-hooks
```

See [`docs/EVALUATION.md`](docs/EVALUATION.md). This repository intentionally uses **no GitHub Actions or hosted CI** and requires no third-party Python packages.

## Community

Use [Discussions](https://github.com/zgbrenner/adhd-and-47-tabs/discussions) for questions and the [issue forms](https://github.com/zgbrenner/adhd-and-47-tabs/issues/new/choose) for reproducible problems. Read [`SUPPORT.md`](SUPPORT.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Attribution and license

Original concept and skill: [Ayoub Ghriss, `ayghri/i-have-adhd`](https://github.com/ayghri/i-have-adhd).

Cross-platform adaptation: [Zachary Brenner](https://github.com/zgbrenner).

MIT licensed. The original notice is preserved in [`LICENSE`](LICENSE) and adaptation history is in [`NOTICE.md`](NOTICE.md).
