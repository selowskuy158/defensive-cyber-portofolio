# B20 Local Repository Hardening Evidence

Capture date: 2026-05-21  
Repository path: `/Users/Chris/Desktop/Projects/defensive-cyber-portofolio`

## Completed / Present Files

The following hardening files are present in the repository working tree:

| Control | File | Evidence |
|---|---|---|
| Ignore secrets and local artefacts | `.gitignore` | Includes `.env`, `.env.*`, `*.pem`, `*.key`, `*.p12`, `*.pfx`, `id_rsa`, `id_ed25519`, and `*.kdbx` |
| Security disclosure policy | `SECURITY.md` | Includes private disclosure via GitHub security advisory and a 7-day acknowledgement target |
| Dependabot update config | `.github/dependabot.yml` | Enables weekly checks for npm, pip, and GitHub Actions |
| Secret scan CI workflow | `.github/workflows/secret-scan.yml` | Adds a Gitleaks workflow for push, pull request, weekly schedule, and manual runs |

## Git Tracking Status

`git ls-files .github/dependabot.yml SECURITY.md .gitignore .github/workflows/secret-scan.yml`

Tracked files:

```text
.github/dependabot.yml
.gitignore
SECURITY.md
```

Current working-tree changes:

```text
 M .gitignore
?? .github/workflows/secret-scan.yml
```

## Important Note

The secret-scan workflow exists locally but has not been committed/pushed yet,
so it will not appear in GitHub Actions until it is committed and pushed to the
remote repository. This is why the activity evidence separates "local hardening
completed" from "remote GitHub settings enabled."
