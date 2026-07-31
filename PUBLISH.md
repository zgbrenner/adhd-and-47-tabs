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

`make check` validates the source, rebuilds `dist/adhd-and-47-tabs.zip`, and runs the repository test suite. The ZIP is generated output and must not be edited manually.

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
3. Commit and merge the tracked changes to `main`.
4. From a clean checkout of `main`, run:

```bash
make release
```

This creates:

- `dist/adhd-and-47-tabs.zip`;
- `dist/SHA256SUMS`;
- a reference to the matching release-notes file.

Review the files, create a GitHub Release for `v<version>`, and upload the ZIP and checksum file. Release publishing stays an explicit maintainer action.

## Manual commands

```bash
python3 scripts/validate_skill.py
python3 scripts/build_zip.py
python3 -m unittest discover -s tests -v
python3 scripts/score_responses.py --responses responses.jsonl
python3 scripts/prepare_release.py
gh skill publish --dry-run
```
