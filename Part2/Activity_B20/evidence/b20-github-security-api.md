# B20 GitHub Security API Evidence

Capture date: 2026-05-21  
Repository: `selowskuy158/defensive-cyber-portofolio`

## Repository Security Settings

Checked with:

```bash
gh api repos/selowskuy158/defensive-cyber-portofolio
```

Relevant returned values:

```text
default_branch: main
private: false
secret_scanning: enabled
secret_scanning_push_protection: enabled
secret_scanning_non_provider_patterns: disabled
secret_scanning_validity_checks: disabled
```

Interpretation:

GitHub secret scanning and push protection are enabled on the repository. This
means GitHub checks for committed secrets and blocks supported secrets before
they are pushed.

## Dependabot Vulnerability Alerts

Enabled with:

```bash
gh api -X PUT repos/selowskuy158/defensive-cyber-portofolio/vulnerability-alerts
```

Verified with:

```bash
gh api repos/selowskuy158/defensive-cyber-portofolio/vulnerability-alerts -i
```

Relevant returned value:

```text
HTTP/2.0 204 No Content
```

Interpretation:

HTTP `204 No Content` is GitHub's success response for this endpoint. It means
Dependabot vulnerability alerts are enabled for the repository.

## Branch Protection Check

Checked with:

```bash
gh api repos/selowskuy158/defensive-cyber-portofolio/branches/main/protection
```

Relevant returned value:

```text
Branch not protected
HTTP 404
```

Interpretation:

Branch protection is not currently enabled on `main`, so B20 lists it as a
remaining recommended control rather than completed evidence.
