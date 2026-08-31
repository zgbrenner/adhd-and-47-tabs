# Installation

Use the canonical [`dist/adhd-and-47-tabs.zip`](../dist/adhd-and-47-tabs.zip) from the repository, or the same asset attached to the latest GitHub Release. Verify it against `dist/SHA256SUMS`:

```bash
(cd dist && sha256sum -c SHA256SUMS)
```

## Claude

1. Download `adhd-and-47-tabs.zip`.
2. Enable **Code execution and file creation** in **Settings → Capabilities**. Team and Enterprise workspaces may use organization settings.
3. Open **Customize → Skills**.
4. Select **+ → Create skill → Upload a skill**.
5. Upload the ZIP and enable the skill.

Claude requires a ZIP containing one top-level folder whose name matches the skill name. That folder must contain `SKILL.md`.

Official documentation: https://support.claude.com/en/articles/12512180-use-skills-in-claude

## ChatGPT Skills

1. Download `adhd-and-47-tabs.zip`.
2. Open ChatGPT's **Skills** page. In the current web interface, this is under **Plugins → Skills** in the sidebar.
3. Select **Create → Upload from your computer**.
4. Upload the ZIP.

Personal Skills availability and workspace permissions can vary.

Official documentation: https://help.openai.com/en/articles/20001066

## Codex

Inside Codex, invoke the built-in installer:

```text
$skill-installer
```

Then ask it to install the `adhd-and-47-tabs` skill from this repository's `adhd-and-47-tabs` folder. For a manual user-wide install, place that folder at `~/.agents/skills/adhd-and-47-tabs`; for a repository-scoped install, place it at `.agents/skills/adhd-and-47-tabs`. Codex detects skill changes automatically; restart only when an install or update does not appear.

## GitHub Copilot

With GitHub CLI 2.90.0 or later:

```bash
gh skill preview zgbrenner/adhd-and-47-tabs adhd-and-47-tabs
gh skill install zgbrenner/adhd-and-47-tabs adhd-and-47-tabs --scope user
```

Omit `--scope user` to install it only for the current project.

Official documentation: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills

## Universal Skills CLI

```bash
npx skills add zgbrenner/adhd-and-47-tabs --skill adhd-and-47-tabs
```

This is a third-party CLI. Its documentation says anonymous skill-usage telemetry is enabled by default; set `DISABLE_TELEMETRY=1` before the command to opt out, or use one of the manual installation paths above.

## Custom GPT fallback

1. Open **Explore GPTs → Create → Configure**.
2. Copy [`chatgpt-custom-gpt/INSTRUCTIONS.md`](../chatgpt-custom-gpt/INSTRUCTIONS.md) into **Instructions**.
3. Add the included conversation starters.
4. Test in Preview and save.

Official documentation: https://help.openai.com/en/articles/8770868-gpt-builder
