# Publishing

This repository intentionally uses no GitHub Actions or hosted CI. Validation, packaging, pushes, and releases run from a maintainer's computer.

## One-time setup

Install Python 3, Git, Make, and GitHub CLI, then authenticate:

```bash
gh auth login
make install-hooks
```

The optional Git hook runs `make check` before each push on that computer.

## Validate a change

```bash
make check
gh skill publish --dry-run
```

`make check` validates the source, rebuilds `dist/adhd-and-47-tabs.zip`, and runs the repository test suite. The ZIP is generated output and must not be edited manually.

## Publish repository changes

```bash
./scripts/publish_to_github.sh
```

The script validates the skill, rebuilds the distributable ZIP, runs tests, commits tracked source changes, verifies the `origin` repository, and pushes the current branch.

## Publish a release

1. Update `VERSION`, `adhd-and-47-tabs/SKILL.md`, `CITATION.cff`, `CHANGELOG.md`, and `docs/releases/<version>.md`.
2. Run `make check` and `gh skill publish --dry-run`.
3. Commit and push the tracked changes to `main`.
4. Run:

```bash
make release
```

The local release process:

- validates version and release notes;
- runs the complete repository test suite;
- generates the canonical ZIP locally;
- generates `dist/SHA256SUMS`;
- verifies local `main` matches `origin/main`;
- creates and pushes an annotated version tag when needed;
- creates or updates the GitHub Release and its assets.

## Manual commands

```bash
python3 scripts/validate_skill.py
python3 scripts/build_zip.py
python3 -m unittest discover -s tests -v
python3 scripts/score_responses.py --responses responses.jsonl
gh skill publish --dry-run
```
