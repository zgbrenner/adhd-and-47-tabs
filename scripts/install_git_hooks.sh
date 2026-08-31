#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

git config core.hooksPath .githooks
chmod +x .githooks/pre-push scripts/install_git_hooks.sh 2>/dev/null || true

printf 'Installed local Git hooks from .githooks/.\n'
printf 'Every git push will now run make check on this computer.\n'
