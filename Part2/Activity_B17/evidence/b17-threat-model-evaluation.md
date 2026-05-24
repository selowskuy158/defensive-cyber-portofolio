# B17 Threat Model and Evaluation Evidence

This file is a compact evidence extract from `zero_trust_design.md`. It shows
that the activity is not only a description of Zero Trust, but also a designed
and evaluated small-scale implementation plan.

## Threat Model Used

| ID | Threat | Likelihood | Impact |
|---|---|---|---|
| T1 | Compromised IoT device pivots to laptop | High | High |
| T2 | Guest phone browses to home file share | Medium | Medium |
| T3 | Phished credential gives remote access to email or cloud | High | High |
| T4 | Stolen laptop reused on home Wi-Fi | Low | High |
| T5 | Malicious USB inserted into laptop | Medium | Medium |

## Main Controls Designed

| Control | Purpose |
|---|---|
| Identity provider with MFA | Stops password-only access to cloud accounts |
| WebAuthn / passkeys where possible | Reduces phishing and credential replay |
| VLAN 10 TRUST | Keeps trusted laptop/phone separate from risky devices |
| VLAN 20 IOT | Allows IoT devices internet access but blocks lateral movement |
| VLAN 30 GUEST | Gives visitors internet access without exposing local devices |
| Firewall deny-by-default rules | Blocks cross-VLAN access unless explicitly allowed |
| DNS sinkhole | Blocks known malware and command-and-control domains |
| Endpoint posture checks | Keeps laptop encrypted, patched, and locked |
| Telemetry review | Uses DNS/router logs to notice abnormal behaviour |

## Evaluation Summary

| Threat | How the design handles it | Residual risk |
|---|---|---|
| T1 IoT lateral movement | IoT VLAN cannot reach TRUST VLAN | Low |
| T2 Guest snooping | Guest VLAN isolated from local shares | Low |
| T3 Phished credentials | MFA and WebAuthn reduce credential reuse | Medium |
| T4 Stolen laptop | Full-disk encryption and remote wipe reduce damage | Low |
| T5 Malicious USB | OS controls and AV help, but do not fully solve it | Medium |

## Honest Limitation

This is a student-scale implementation design, not a full enterprise Zero Trust
deployment. It cannot fully provide identity-aware proxying, MDM-backed device
attestation, or protection against malware that bypasses DNS filtering.
