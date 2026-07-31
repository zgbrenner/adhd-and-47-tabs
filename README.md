# ADHD & 47 Tabs - a skill for AI

<strong>An action-first skill for Claude, ChatGPT, Codex, and Copilot. For work, research, and life.</strong>

> **Your brain has enough tabs open. Your AI does not need to add twelve more.** 

  <a href="https://github.com/zgbrenner/i-have-adhd-and-47-tabs/releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/release/zgbrenner/i-have-adhd-and-47-tabs?display_name=tag"></a>
  <a href="https://github.com/zgbrenner/i-have-adhd-and-47-tabs/releases/latest/download/i-have-adhd-and-47-tabs.zip"><img alt="Download skill" src="https://img.shields.io/badge/download-skill.zip-6f42c1.svg"></a>
  <a href="https://github.com/zgbrenner/i-have-adhd-and-47-tabs/releases"><img alt="Total downloads" src="https://img.shields.io/github/downloads/zgbrenner/i-have-adhd-and-47-tabs/total?label=downloads"></a>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-2ea44f.svg"></a>

> Ensure that your preferred AI: 
> - Answers first;
> - Provides fewer wasteful options; and
> - Gives you one clear next step.

---

## The Two-Minute Version

Most AI answers are technically correct and operationally useless. They begin with a preamble, hide the actual answer in paragraph four, hand you eleven equally weighted options, and end with “hope this helps.”

**ADHD & 47 Tabs** changes the shape of the answer:

1. The answer or next action comes first.
2. Multi-step work becomes small numbered actions.
3. Long lists are capped, grouped, and ranked.
4. Context is restated when a project spans multiple turns.
5. The response ends when the useful part ends.

It works for **research, studying, writing, planning, email, administrative work, life logistics, and technical tasks**. It is a response-formatting skill, not a medical tool, and no diagnosis is required.

## Before & After

<table>
<tr>
<td width="50%" valign="top">

### Before

> Great question! There are several ways to approach planning your week. You may want to think about your priorities, deadlines, energy levels, meetings, errands, and personal obligations. One strategy is time blocking, while another is using a prioritized task list...

</td>
<td width="50%" valign="top">

### After

> **Open your calendar and block the three deadlines first.**
>
> 1. Add anything due this week.
> 2. Reserve one work block for each deadline.
> 3. Put errands into one shared block.
> 4. Leave one unscheduled recovery block.
>
> Next: open your calendar and add the nearest deadline.

</td>
</tr>
</table>

## Download

**[Download the latest ready-to-upload ZIP](https://github.com/zgbrenner/i-have-adhd-and-47-tabs/releases/latest/download/i-have-adhd-and-47-tabs.zip)**

Every release also includes `SHA256SUMS` for download verification. The ZIP contains exactly one top-level folder named `i-have-adhd-and-47-tabs`, with `SKILL.md` and its supporting files inside it.

## Install in Claude

1. Download the [latest ZIP](https://github.com/zgbrenner/i-have-adhd-and-47-tabs/releases/latest/download/i-have-adhd-and-47-tabs.zip).
2. Enable **Code execution and file creation** under **Settings → Capabilities**.
3. Open **Customize → Skills**.
4. Select **+ → Create skill → Upload a skill**.
5. Upload the ZIP and enable **I Have ADHD and 47 Tabs**.

Official guide: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## Install in ChatGPT Skills

1. Download the [latest ZIP](https://github.com/zgbrenner/i-have-adhd-and-47-tabs/releases/latest/download/i-have-adhd-and-47-tabs.zip).
2. Open **Plugins** in the ChatGPT sidebar.
3. Select **Skills → Create → Upload from your computer**.
4. Upload the ZIP.

Official guide: [Skills in ChatGPT](https://help.openai.com/en/articles/20001066).

## Install in Codex

```text
$skill-installer install https://github.com/zgbrenner/i-have-adhd-and-47-tabs/tree/main/i-have-adhd-and-47-tabs
```

Restart Codex after installation.

## Install for GitHub Copilot

GitHub CLI 2.90.0 or later can preview and install this skill:

```bash
gh skill preview zgbrenner/i-have-adhd-and-47-tabs i-have-adhd-and-47-tabs
gh skill install zgbrenner/i-have-adhd-and-47-tabs i-have-adhd-and-47-tabs --scope user
```

Omit `--scope user` to install it only for the current project.

Official guide: [Adding agent skills for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills).

## Install with the universal Skills CLI

```bash
npx skills add zgbrenner/i-have-adhd-and-47-tabs
```

## ChatGPT Plus / Custom GPT fallback

1. Open **Explore GPTs → Create → Configure**.
2. Name it **I Have ADHD and 47 Tabs**.
3. Copy [`chatgpt-custom-gpt/INSTRUCTIONS.md`](chatgpt-custom-gpt/INSTRUCTIONS.md) into the GPT’s **Instructions** field.
4. Add the included conversation starters.
5. Test it in Preview, then save or publish it.

## What is different from the original?

This is a browser-first, general-purpose adaptation of **[Ayoub Ghriss’s original `i-have-adhd`](https://github.com/ayghri/i-have-adhd)** skill. It keeps the original ten-rule structure while broadening the examples and behavior for everyday questions, research, school, writing, planning, administrative work, and technical tasks.

The key adaptation is simple: factual questions lead with the **answer**, while tasks lead with the **next action**.

## The Rules

1. Lead with the answer or next action.
2. Number multi-step tasks.
3. End with one concrete next step when work remains.
4. Suppress tangents.
5. Restate workflow state across turns.
6. Use concrete time estimates when useful.
7. Make progress and wins visible.
8. Describe errors matter-of-factly.
9. Keep lists short, grouped, and ranked.
10. Remove preambles, recaps, and empty closers.

The full instructions live in [`i-have-adhd-and-47-tabs/SKILL.md`](i-have-adhd-and-47-tabs/SKILL.md).

## Community

- Ask installation and usage questions in [Discussions](https://github.com/zgbrenner/i-have-adhd-and-47-tabs/discussions).
- Report reproducible bugs through the [issue forms](https://github.com/zgbrenner/i-have-adhd-and-47-tabs/issues/new/choose).
- Read [`SUPPORT.md`](SUPPORT.md) for the correct help channel.
- Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before proposing changes.

## Zero-cost local validation

This repository intentionally uses **no GitHub Actions or hosted CI**. Validation and releases run locally so maintaining the project does not consume GitHub Actions minutes.

```bash
make check
```

Optional one-time setup installs a local pre-push hook that runs the same checks before every push on your computer:

```bash
make install-hooks
```

No third-party Python packages are required.

## Repository map

```text
i-have-adhd-and-47-tabs/
├── i-have-adhd-and-47-tabs/      # Uploadable skill source
├── assets/                       # Social and launch artwork
├── chatgpt-custom-gpt/           # Custom GPT fallback
├── dist/                         # Reproducible release ZIP
├── docs/                         # Installation, release, and community notes
├── scripts/                      # Local validation, packaging, and publishing
├── tests/                        # Package contract tests
├── .githooks/                    # Optional local pre-push checks
└── .github/                      # Issue and discussion templates only
```

## Attribution

**Original concept and skill:** [Ayoub Ghriss - `ayghri/i-have-adhd`](https://github.com/ayghri/i-have-adhd)

**Browser/general-purpose adaptation:** [Zachary Brenner](https://github.com/zgbrenner)

The original copyright notice is preserved in [`LICENSE`](LICENSE), and the adaptation history is documented in [`NOTICE.md`](NOTICE.md).

## License

MIT. Use it, fork it, remix it, and close at least one tab.
