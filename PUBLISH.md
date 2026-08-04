# Publishing and release process

Releases are prepared and verified locally. GitHub Actions and hosted CI are intentionally not used.

## Release contract

A release is ready only when:

1. `VERSION`, `SKILL.md`, the evaluation suite, citation, changelog, and release notes agree.
2. `make check` passes.
3. `make release` passes.
4. The tracked ZIP is byte-for-byte reproducible from the source skill folder.
5. `dist/SHA256SUMS` matches the tracked ZIP.
6. The exact pull-request head is reviewed and merged.
7. The release tag points to the verified merged main commit.
8. The exact tracked ZIP and checksum are attached to the GitHub Release.

## Prepare

```bash
make check
make release
```

`make release` runs validation, deterministic packaging, repository tests, scorer tests, checksum verification, and release-note checks.

## Review

Inspect the complete diff for:

- unsupported medical claims;
- copied prose;
- contradictory routing rules;
- excessive rigidity;
- stale versions or package names;
- missing attribution;
- hidden dependencies, credentials, or telemetry;
- GitHub Actions or remote publishing scripts;
- package drift;
- optional polish turned into a release requirement.

## Merge

Merge only the reviewed head SHA. After merge, verify on `main`:

```bash
cat VERSION
sha256sum -c dist/SHA256SUMS
python3 scripts/test_repository.py
```

## GitHub Release

Create tag and release `v3.0.0` from the verified merged commit.

Use `docs/releases/3.0.0.md` as the release body. Attach:

- `dist/adhd-and-47-tabs.zip`
- `dist/SHA256SUMS`

Mark the release as the latest non-prerelease.

## Verify publication

- Tag resolves to the merged main commit.
- Both assets exist.
- Downloaded ZIP matches the published checksum.
- The repository's canonical raw ZIP matches the attached asset.
- Installation succeeds from the release asset, not a local untracked build.

Do not publish from an unmerged feature branch or a locally modified worktree.
