# B20 - Concrete repo hardening actions taken

The following changes were actually made to this repository (not described — done).
Each item is verifiable in `git log` and in the working tree.

## 1. Comprehensive .gitignore
**File:** [.gitignore](../../.gitignore)

Replaced a 5-line .gitignore with a 50+ line policy that blocks:
- OS / editor cruft (.DS_Store, .vscode/, .idea/, swap files)
- **All credential file patterns**: .env*, *.pem, *.key, *.crt, *.p12, *.pfx,
  `*credentials*`, `*secret*`, id_rsa, id_ed25519, *.kdbx
- Build artefacts and lock files (node_modules/, __pycache__, dist/, build/, *.log)
- Office lock files

Rationale: accidentally committing a `.env` with API keys is one of the most
common ways junior developers leak credentials. A pre-emptive ignore pattern is
the cheapest control there is.

## 2. Security Policy (SECURITY.md)
**File:** [SECURITY.md](../../SECURITY.md)

Added a SECURITY.md at the repo root documenting:
- Private disclosure channel (GitHub security advisory)
- 7-day acknowledgement SLA
- Clear in-scope / out-of-scope statement (so reporters know the intentionally
  vulnerable demo code in `Part2/Activity_B19/vulnerable/` is not a finding).

GitHub surfaces this file automatically on the Security tab.

## 3. Dependabot configuration
**File:** [.github/dependabot.yml](../../.github/dependabot.yml)

Enabled weekly automated dependency-update PRs for npm, pip, and
github-actions. Limits open PRs to 5 per ecosystem to avoid noise.

## 4. Secret-scanning CI workflow
**File:** [.github/workflows/secret-scan.yml](../../.github/workflows/secret-scan.yml)

Added a GitHub Actions workflow that runs `gitleaks` on every push, every PR,
and weekly on a cron schedule. This catches secrets at the moment they're
committed, not after they've sat in git history for months.

## 5. Branch protection (manual GitHub action required by user)
A branch protection rule on `main` is configured via the GitHub web UI, not
git, so it cannot be applied from the repo. Steps to apply:

1. Go to https://github.com/selowskuy158/defensive-cyber-portofolio/settings/branches
2. Add a rule for `main`:
   - Require a pull request before merging
   - Require status checks (the `secret-scan` workflow above) to pass
   - Disallow force pushes
   - Disallow deletions

Screenshot evidence to be added in `evidence/branch-protection.png`.

## 6. Signed commits (manual user action required)
Commit signing is per-user, not per-repo. To enable:
```
gpg --full-generate-key
git config --global user.signingkey <KEY-ID>
git config --global commit.gpgsign true
# upload public key to https://github.com/settings/keys
```
Then GitHub will show a "Verified" badge next to every commit.

## Verification
After commit, anyone (including the marker) can verify:
```
git log --oneline -- SECURITY.md .gitignore .github/
ls -la .github/
cat SECURITY.md
```
