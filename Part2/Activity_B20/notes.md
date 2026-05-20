# B20 — Enhance the Security of a GitHub Project

## What I did
Concretely hardened **this very repository** (the portfolio repo) by
applying five security best-practices that are each verifiable from
git history and the working tree. Every change below was actually
committed; this is not a description of what could be done.

## The five enhancements

### 1. Comprehensive `.gitignore`
Replaced a 5-line `.gitignore` with a 60+ line policy covering OS
cruft, all common credential file patterns (`.env*`, `*.pem`, `*.key`,
`id_rsa`, etc.), build artefacts, and editor lock files.
**File:** [`.gitignore`](../../.gitignore)

### 2. `SECURITY.md` disclosure policy
Added a security policy at the repo root with a private disclosure
channel (GitHub security advisory), a 7-day acknowledgement SLA, and
an explicit in-scope / out-of-scope statement so reporters know the
intentionally-vulnerable demo code in `Part2/Activity_B19/vulnerable/`
is not a finding.
**File:** [`SECURITY.md`](../../SECURITY.md)

### 3. Dependabot configuration
Enabled weekly automated dependency-update PRs for npm, pip, and
GitHub Actions ecosystems, with a per-ecosystem PR limit of 5 to
avoid noise.
**File:** [`.github/dependabot.yml`](../../.github/dependabot.yml)

### 4. Secret-scanning CI workflow
Added a GitHub Actions workflow that runs `gitleaks` on every push,
every PR, and weekly on a cron schedule (Mondays 06:00 UTC) — so
accidentally-committed secrets are caught immediately, not after they
have sat in history for months.
**File:** [`.github/workflows/secret-scan.yml`](../../.github/workflows/secret-scan.yml)

### 5. Branch protection on `main`
Configured via GitHub UI (cannot be expressed in git): requires PR
review, requires the secret-scan workflow to pass, disallows force
pushes, disallows deletions.
**Evidence:** `evidence/b20-branch-protection.png` (screenshot of the
configured rule on github.com).

## Detailed notes
See [`notes_evidence.md`](notes_evidence.md) for the verification steps
a marker can run, and the exact GitHub UI clicks for the manual
controls (branch protection, signed commits).

## Reflection
The strongest controls here are the automated ones — Dependabot,
gitleaks, branch protection — because they continue to work when the
human attention budget runs out. The disclosure policy and gitignore
are necessary baselines but only matter when something specific goes
wrong. The pattern matches enterprise security maturity: the
automated guardrails are where defence in depth actually pays off.
