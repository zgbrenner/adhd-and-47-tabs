# Publishing

This repository intentionally uses no GitHub Actions or hosted CI. Validation, packaging, and release preparation run locally.

## One-time setup

Install Python 3, Git, Make, and GitHub CLI, then authenticate:

```bash
gh auth login
make install-hooks
```

## Validate a change

```bash
make check
gh skill publish --dry-run
```

`make check` validates the source, deterministically rebuilds `dist/adhd-and-47-tabs.zip` and `dist/SHA256SUMS`, and runs the repository contract checks. These two generated files are intentionally tracked so the repository always exposes a working verified download. Do not edit them manually.

After `make check`, confirm the tracked package files are unchanged or include their regenerated versions in the same pull request as the source change.

## Push source changes

After the checks pass, use your normal reviewed Git workflow:

```bash
git add --all
git commit -m "describe the change"
git push
```

The repository does not include a script that commits, tags, or pushes automatically. That prevents a stale repository constant from publishing to the wrong destination.

## Prepare a release

1. Update `VERSION`, `adhd-and-47-tabs/SKILL.md`, `CITATION.cff`, `CHANGELOG.md`, and `docs/releases/<version>.md`.
2. Run `make check` and `gh skill publish --dry-run`.
3. Commit the regenerated ZIP and checksum with the source changes, then merge them to `main`.
4. From a clean checkout of `main`, run:

```bash
make release
```

This re-verifies the canonical package and checksum and identifies the matching release-notes file. A GitHub Release may mirror those exact tracked assets, but the repository download remains authoritative even when release publishing is unavailable.

## Manual commands

```bash
python3 scripts/validate_skill.py
python3 scripts/build_zip.py
python3 scripts/test_repository.py
python3 scripts/score_responses.py --responses responses.jsonl
python3 scripts/prepare_release.py
gh skill publish --dry-run
```
