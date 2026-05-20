# B17 — Implement and Evaluate a State-of-the-Art Cybersecurity Solution

## Solution chosen
**Zero Trust Architecture** (NIST SP 800-207), one of the SOTA solutions
surveyed in Activity B16. Rather than describe enterprise ZT (which I
have no infrastructure to deploy), I designed and evaluated a scaled-
down Zero Trust model for a small WFH network — a setting where ZT
principles are directly applicable but require adaptation to consumer-
grade equipment.

## What I produced
A complete design document with:
- A specific threat model (5 prioritised threats with likelihood/impact).
- A network architecture diagram showing three VLANs (Trust / IoT /
  Guest), an identity provider, and a DNS sinkhole.
- A mapping of each NIST SP 800-207 tenet to a concrete control and a
  consumer-grade tool that implements it.
- An implementation checklist with 7 ordered steps.
- An honest evaluation of which threats the design handles, and which
  it doesn't (the design explicitly documents what enterprise ZT
  features are NOT achievable with consumer gear).

**See: [`zero_trust_design.md`](zero_trust_design.md)**

## Evaluation
The design addresses 4 of 5 threats in the threat model (T1–T4) at
"Low residual risk" and one (T5, malicious USB) at "Medium residual
risk". The limitations section honestly notes the three things a
consumer setup cannot achieve: identity-aware proxying of every HTTP
request, cryptographic device-posture attestation, and protection
against malware that bypasses DNS.

## Why this is distinct from A23 (home cybersecurity)
A23 is about hardening a home network at a tactical level (change the
router password, enable WPA2, etc.). B17 is an architectural design
that frames the same building blocks inside an explicit Zero Trust
framework with a threat model, tenet mapping, and limitations
analysis — the SOTA solution framing required by B17 specifically.

## What I learned
The biggest insight from designing this was how much of "Zero Trust"
is a *process* (continuous verification, telemetry review, policy
adjustment) and not a *technology* you install once. The most powerful
controls (MFA, network segmentation, DNS sinkholing) are individually
cheap; the difficulty is keeping them tuned over time.
