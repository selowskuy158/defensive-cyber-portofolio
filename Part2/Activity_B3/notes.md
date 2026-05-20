# B3 — Discover 3 Proactive Security Implementations in Practice

A proactive control prevents or detects threats before they cause harm,
rather than responding after an incident. I documented three implementations
where I could verify the control is actually deployed and producing useful
output.

## 1. ACSC Threat Intelligence Sharing (CTIS)
The Australian Cyber Security Centre operates the Cyber Threat Intelligence
Sharing (CTIS) service, which lets partnered organisations exchange machine-
readable indicators of compromise via STIX / TAXII before those indicators
appear in commercial feeds. Organisations subscribe and pull updated IOC
sets that are then loaded into their SIEM / IDS for automated blocking.

This is proactive in the strictest sense: the goal is to block known-bad
domains and hashes *before* the org's own users encounter them. I verified
the service exists via the official ACSC page (cyber.gov.au) and via the
CISA / ACSC joint cybersecurity advisories that publish IOCs in TAXII
format.

**Citation:** ACSC, "Cyber Threat Intelligence Sharing (CTIS)",
cyber.gov.au/business-government/asds-cyber-security-services/ctis

### 2. GitHub secret scanning + push protection
GitHub now scans every push for credentials matching ~200 known token
patterns (AWS access keys, Stripe live keys, etc.). With push protection
enabled, a commit containing a recognised secret is *blocked at the
client* before the push completes — the secret never reaches the remote.
This is proactive: a secret that never reaches GitHub never has to be
rotated or audited.

I enabled push protection on this repository as part of B20. Evidence:
`Part2/Activity_B20/notes_evidence.md` and the `.github/workflows/secret-scan.yml`
file added to the repo.

**Citation:** GitHub Docs, "Push protection for repositories and
organizations".

### 3. EDR behavioural detection on managed laptops
Modern enterprise EDR products (CrowdStrike Falcon, Microsoft Defender for
Endpoint, SentinelOne) hook the OS kernel to monitor process trees,
command-line arguments, and child-process spawn patterns. Where signature
AV waits for a known-bad hash, behavioural EDR flags "Word spawned
powershell.exe with a base64-encoded argument longer than 200 chars" —
a pattern, not a hash — and blocks the process before it can execute its
payload.

I verified the principle live by enabling Microsoft Defender's Attack
Surface Reduction rules on my own laptop and observing the events in
Event Viewer. The "Block Office applications from creating child
processes" rule (rule ID `d4f940ab-401b-4efc-aadc-ad5f3c50688a`) blocks
the most common macro-malware execution path before any payload runs.

**Citation:** Microsoft Learn, "Attack Surface Reduction Rules
Reference".

## Why these three together
Each operates at a different layer: CTIS at the threat-intel network
level, GitHub secret scanning at the code-supply-chain level, and EDR
behavioural detection at the endpoint runtime level. Together they
demonstrate that "proactive" isn't one technology — it's a mindset
applied across the stack.
