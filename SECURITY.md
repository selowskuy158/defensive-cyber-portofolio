# Security Policy

This repository is a personal academic portfolio for CITS2006 (Defensive Cybersecurity)
at the University of Western Australia. It contains intentionally-vulnerable code
samples used to demonstrate attack and defence techniques.

## Reporting a Vulnerability

If you find a real security issue in any of the repository's *infrastructure* (not
the intentionally-vulnerable demo code), please report it privately rather than
opening a public issue.

- **Preferred:** open a private GitHub security advisory via the
  [Security tab](https://github.com/selowskuy158/defensive-cyber-portofolio/security/advisories/new).
- **Alternative:** email the maintainer (contact details on the GitHub profile).

You will receive an acknowledgement within 7 days. If a fix is required, the
maintainer will work with you to coordinate disclosure.

## What Counts as a Vulnerability Here

In scope:
- Secrets accidentally committed (API keys, credentials, private keys).
- Code in the portfolio that could be remotely exploited if deployed (outside
  the clearly-labelled `vulnerable/` demo directories).
- Supply-chain risks in dependencies.

Out of scope:
- Demo files explicitly marked as vulnerable for educational purposes
  (e.g. `Part2/Activity_B19/vulnerable/server.js`). These are intentional.
- Theoretical findings without a working proof of concept.

## Supported Versions

This is an academic submission, not a maintained product. Only the contents of
the `main` branch at the time of CITS2006 portfolio assessment are considered
"supported."

## Acknowledgements

Thanks in advance to anyone who responsibly discloses a real issue.
