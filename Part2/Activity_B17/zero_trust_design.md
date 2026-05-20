# B17 — Zero Trust Architecture for a Small WFH Network: Design & Evaluation

This document is a **design** for applying a Zero Trust security model to a
small work-from-home network (one student / one knowledge-worker household).
Real enterprise Zero Trust requires equipment a student does not have access to
(identity-aware proxies, hardware TPM-attested endpoints, an enterprise IdP).
The design below adapts the core principles to consumer-grade equipment and
free SaaS tiers, and evaluates the result against the original SP 800-207
tenets.

## 1. Background — why Zero Trust

Traditional perimeter security trusts everything inside the LAN. As soon as
one device on the network is compromised — a phished laptop, an IoT camera
with a default password, a guest's phone — the attacker can move laterally to
everything else. NIST SP 800-207 redefines this: **trust is never granted by
network location**; every request is authenticated, authorised, and verified
against device posture.

The seven tenets (NIST SP 800-207 §2.1):
1. All data sources and services are resources.
2. All communication is secured regardless of network location.
3. Access is granted per-session.
4. Access is policy-driven (identity, device, behaviour, etc.).
5. Asset integrity is continuously monitored.
6. Authentication and authorisation are dynamic and strictly enforced.
7. The organisation collects telemetry to improve its posture.

## 2. Threat model

| # | Threat | Likelihood | Impact |
|---|---|---|---|
| T1 | Compromised IoT device (smart speaker, doorbell cam) pivots to laptop | High | High |
| T2 | Guest phone on Wi-Fi browses to home file share | Medium | Medium |
| T3 | Phished credential gives attacker remote access to email/cloud | High | High |
| T4 | Stolen laptop reused on the home Wi-Fi | Low | High |
| T5 | Malicious USB inserted into laptop | Medium | Medium |

## 3. Architecture

```
                          ┌──────────────────────────┐
                          │  Identity Provider        │
                          │  (Google / Microsoft IdP) │
                          │  + WebAuthn / TOTP MFA    │
                          └────────────┬──────────────┘
                                       │  (policy decisions)
        ┌──────────────────────────────┼──────────────────────────────┐
        │                              │                              │
┌───────▼────────┐          ┌──────────▼─────────┐         ┌──────────▼─────────┐
│ VLAN 10 — TRUST│          │ VLAN 20 — IOT      │         │ VLAN 30 — GUEST    │
│ Laptop, phone  │          │ Doorbell, speaker  │         │ Visitor phones     │
│ - 802.1X auth  │          │ - egress only      │         │ - egress only      │
│ - posture chk  │          │ - no inter-VLAN    │         │ - bandwidth cap    │
└────────┬───────┘          └──────────┬─────────┘         └──────────┬─────────┘
         │                              │                              │
         └──────────────┬───────────────┴──────────────────────────────┘
                        │                       Firewall (deny by default,
                ┌───────▼───────┐                 explicit allow rules)
                │ Home router   │
                │ + DNS sinkhole│  ←—— NextDNS / Pi-hole (block known C2)
                └───────┬───────┘
                        │
                  ┌─────▼──────┐
                  │  Internet  │
                  └────────────┘
```

## 4. Controls mapped to the seven tenets

| Tenet | Control | Tool (consumer-grade) |
|---|---|---|
| 1 — Resources | Inventory of every device (MAC + purpose) | Spreadsheet + router DHCP list |
| 2 — Secured comms | All HTTP→HTTPS, DoH for DNS, VPN for off-home traffic | Cloudflare WARP, Firefox HTTPS-Only mode |
| 3 — Per-session | Short browser session cookies, re-auth on sensitive actions | Browser settings + IdP session policy |
| 4 — Policy-driven | VLAN isolation by device type; firewall rules between VLANs | OpenWrt / OPNsense (free) |
| 5 — Integrity monitoring | Endpoint AV + OS-level update enforcement | Windows Defender, macOS XProtect |
| 6 — Dynamic auth | MFA on every cloud account (WebAuthn preferred over TOTP) | Google Advanced Protection, Bitwarden + YubiKey |
| 7 — Telemetry | DNS query logs, router flow logs, free SIEM tier | Pi-hole logs, Cloudflare WARP analytics |

## 5. Implementation checklist (what someone would actually do)

1. **IdP first.** Move all primary accounts to a single IdP (Google or
   Microsoft) and enable WebAuthn (hardware key or device passkey).
2. **Segment Wi-Fi.** Create three SSIDs on the router mapping to the three
   VLANs above. Use WPA3 where supported, WPA2-AES otherwise.
3. **Deny inter-VLAN by default.** Add explicit allow rules only for things
   that need them (e.g. Chromecast on TRUST → guest screen on IOT). Most
   homes have zero legitimate inter-VLAN traffic.
4. **DNS sinkhole.** Point the network's DNS at NextDNS or a self-hosted
   Pi-hole that blocks known malware/C2 domains. This is the single
   highest-leverage cheap control for the IoT VLAN.
5. **Endpoint posture.** Enforce auto-updates, full-disk encryption
   (BitLocker / FileVault), and screen lock under 5 minutes.
6. **Password manager + MFA.** Move every password into a manager
   (Bitwarden free tier is sufficient) and turn on MFA wherever the service
   supports it.
7. **Telemetry review.** Once a week, scan Pi-hole's blocked-query list and
   the router's flow logs for anything weird.

## 6. Evaluation — does the design meet the threat model?

| Threat | How the design handles it | Residual risk |
|---|---|---|
| T1 IoT lateral movement | VLAN 20 cannot reach VLAN 10; firewall blocks east-west | Low |
| T2 Guest snooping | VLAN 30 isolated; no SMB / mDNS leakage | Low |
| T3 Phished credentials | MFA + WebAuthn defeats credential reuse; IdP session policy limits damage | Medium (still vulnerable to MFA-fatigue attacks; mitigated by WebAuthn) |
| T4 Stolen laptop | Full-disk encryption + remote wipe + 802.1X means the laptop is a brick on the home network | Low |
| T5 Malicious USB | OS-level USB-mass-storage policy + AV; not fully solved | Medium |

## 7. Limitations honestly noted

- **No identity-aware proxy.** Real enterprise ZT (Google BeyondCorp,
  Cloudflare Access, Tailscale) intercepts every HTTP request and re-evaluates
  policy per resource. Consumer routers cannot do this. The design substitutes
  IdP MFA + DNS sinkholing as a partial proxy.
- **No device posture attestation.** Enterprise ZT requires the IdP to
  cryptographically verify the device is patched / encrypted. Without an
  MDM, the design relies on the user manually keeping endpoints healthy.
- **DNS-based defence can be bypassed** if malware hard-codes IPs and skips
  DNS. The Pi-hole layer is a control on most malware, not all.

## 8. Why this isn't B22 (community website hardening) or A23 (home cybersecurity)

- This activity is the **design and evaluation of a SOTA solution** (Zero
  Trust) per the brief for B17. It is not the deployment of an actual ISP
  router or the hardening of an existing community website.
- A23 (Part 1) covers concrete home-network hygiene (router password, WPA2,
  guest network) at a tactical level. B17 is the architectural level above
  that — the same building blocks combined into an explicit Zero Trust
  framework with a threat model and tenet mapping.

## References
- NIST SP 800-207, "Zero Trust Architecture", August 2020.
- Google BeyondCorp papers (research.google/pubs/), 2014–2017.
- Microsoft Zero Trust deployment guide, Microsoft Learn.
