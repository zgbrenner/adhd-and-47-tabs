# Security policy

This repository distributes instruction and documentation files plus small standard-library validation and packaging scripts. The skill itself requires no network access, credentials, executable scripts, or third-party packages.

## Supported versions

| Version | Supported |
| --- | --- |
| 2.x | Yes |
| 1.x | Security fixes only |
| Earlier versions | No |

Install the latest release before reporting a problem that may already be fixed.

## Private vulnerability reporting

Do not open a public issue for a vulnerability that could expose credentials, enable unsafe execution, tamper with a release ZIP, or introduce malicious skill instructions.

Use [GitHub private vulnerability reporting](https://github.com/zgbrenner/adhd-and-47-tabs/security/advisories/new). This creates a private advisory visible only to the reporter and repository maintainers.

Include:

- the affected file and release version;
- the unsafe behavior and likely impact;
- a minimal reproduction or proof of concept;
- any suggested mitigation;
- whether you believe the issue is already being exploited.

## Response targets

The maintainer will aim to acknowledge a report within 3 business days and provide an initial assessment within 7 business days. These are targets, not guarantees, for a volunteer-maintained project.

## In scope

- malicious or hidden instructions in the distributed skill;
- release-asset tampering or checksum mismatch;
- packaging behavior that includes unintended files;
- scripts that expose credentials or change unrelated files;
- installation instructions that create a material security risk.

General prompt-quality disagreements, medical questions, and ordinary installation failures are not security vulnerabilities. Use Discussions or Issues for those.
