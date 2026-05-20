# B16 — Survey of Current State-of-the-Art Cybersecurity Solutions

This survey covers five solution categories that represent the leading edge
of defensive cybersecurity in 2025–2026. For each I describe the problem
being solved, the principle the solution applies, leading commercial /
open-source examples, and the open research question.

## 1. Zero Trust Architecture (ZTA)
**Problem:** the traditional network perimeter dissolved with remote work
and cloud. A breach of one device inside the LAN gives an attacker
lateral access to everything.

**Principle:** never trust, always verify — per-request authentication and
authorisation conditioned on user identity, device posture, and context,
regardless of network location (NIST SP 800-207, 2020).

**Examples:** Google BeyondCorp (the canonical reference), Cloudflare
Access, Tailscale, Microsoft Entra Private Access.

**Open question:** how to extend ZTA principles to non-HTTP protocols
(legacy SCADA, industrial OT) where session-level auth is not native.

(See `Part2/Activity_B17/zero_trust_design.md` for my own scaled-down
design as a follow-up activity.)

## 2. Extended Detection and Response (XDR)
**Problem:** SOC analysts drown in disconnected alerts from endpoint AV,
network IDS, email gateways, and cloud logs.

**Principle:** ingest telemetry from every layer (endpoint, identity,
network, email, cloud workload) into one correlation engine that links
related events into a single incident narrative.

**Examples:** CrowdStrike Falcon XDR, Palo Alto Cortex XDR, Microsoft
Defender XDR, SentinelOne Singularity.

**Open question:** the consolidation tradeoff — single-vendor XDR loses
the depth of best-of-breed point tools; open standards (OCSF) are an
attempt to enable cross-vendor correlation but adoption is partial.

## 3. AI-augmented Security Operations
**Problem:** alert volumes scale faster than analyst hiring; the median
SOC sees thousands of alerts per day, with single-digit minutes per
investigation.

**Principle:** use large language models to summarise alerts, draft
investigation timelines, and propose containment playbooks in natural
language. Humans approve, models execute.

**Examples:** Microsoft Security Copilot, Google Chronicle's Duet AI,
CrowdStrike Charlotte AI.

**Open question:** prompt-injection attacks against AI SOCs are now a
demonstrated risk class (hostile log entries that pivot the model's
behaviour). Defenders are essentially extending the trust boundary into
the LLM, and the LLM's input is fully attacker-controlled.

## 4. Passwordless Authentication (WebAuthn / FIDO2 / Passkeys)
**Problem:** passwords are the root cause of credential-stuffing,
phishing, and credential-replay attacks, which collectively account for
over 80% of breaches (Verizon DBIR 2024).

**Principle:** replace shared-secret passwords with public-key
cryptography. The private key is held in a secure hardware element on
the user's device (or a roaming YubiKey) and never leaves. Each
authentication is origin-bound, so a phishing site at a look-alike
domain cannot replay the credential.

**Examples:** Apple Passkeys, Google Passkeys, 1Password Passkeys,
YubiKey FIDO2.

**Open question:** account recovery and cross-device portability still
fragment the user experience. The FIDO Alliance's CTAP2 spec is
evolving to address this.

## 5. Cloud-Native Application Protection Platform (CNAPP)
**Problem:** cloud misconfigurations (public S3 buckets, overly-broad
IAM roles, exposed Kubernetes APIs) are the most common cause of
modern data breaches.

**Principle:** continuous configuration scanning + workload runtime
protection + supply-chain analysis, all unified under one platform that
understands the cloud control plane.

**Examples:** Wiz, Prisma Cloud, Lacework, Microsoft Defender for
Cloud, Orca Security.

**Open question:** CNAPP tools are excellent at finding misconfigurations
but generate massive volumes of low-criticality findings. Prioritisation
("which of these 50,000 issues actually matters?") is still an open
research problem and the major differentiator among vendors.

## References
- NIST SP 800-207, "Zero Trust Architecture", 2020.
- Verizon Data Breach Investigations Report 2024.
- Cohn-Gordon et al., "A Formal Security Analysis of the Signal Messaging
  Protocol", IEEE EuroS&P 2017.
- FIDO Alliance, CTAP2 specification.
- MITRE ATT&CK framework (cited by every XDR / EDR product as their
  detection taxonomy).
