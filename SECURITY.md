# Security policy

ADHD & 47 Tabs is an instruction-only Agent Skill. The uploaded package contains Markdown instructions and references, one YAML host-metadata file, and the MIT license. It has no executable code, package installation, credentials, telemetry, network calls, or background processes.

## Supported version

Security fixes are made for the latest released version.

## Reporting

Report suspected prompt injection, unsafe instructions, packaging tampering, credential exposure, path traversal, malicious bundled content, or checksum mismatch privately through GitHub's security-reporting features when available.

Do not include secrets, personal data, or exploit payloads in a public issue.

## Supply-chain checks

Before enabling any downloaded skill:

1. Review its contents.
2. Verify the ZIP against `dist/SHA256SUMS`.
3. Confirm the root folder is `adhd-and-47-tabs`.
4. Confirm the package contains no scripts or unexpected binary files.
5. Download from this repository or its GitHub Release.

`make check` verifies deterministic archive entries, paths, file types, permissions, timestamps, source equality, and checksum.
