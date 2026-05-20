# B2 — Discover 5 Unique Strong Security Implementations

## What I did
Same walk + observation method as B1, but looking for controls that are
implemented well. For each I noted what the threat model is and what the
specific implementation does to address it.

## The five strong implementations

### 1. MFA with WebAuthn on the UWA student portal
The Pheme single sign-on supports WebAuthn passkeys / hardware security
keys, not just SMS or TOTP. WebAuthn is phishing-resistant by design:
the browser refuses to authenticate against a domain the credential
wasn't registered with, so even a perfect look-alike phishing site fails
to capture a usable credential.
**Evidence:** `evidence/01-pheme-2fa-options.png`

### 2. Mantrap / two-stage door at a campus server room
The CSSE server room I walked past uses a vestibule design: an outer door
opens to a small lobby, an inner door opens from the lobby into the
secure area, and the inner door will not open while the outer door is
open. This stops tailgating (one badged person, one unbadged person
walking through together).
**Evidence:** `evidence/02-mantrap-door.png` (signage photographed, not
the secure space).

### 3. HSTS preload on banking
CommBank's netbank.commbank.com.au sets a Strict-Transport-Security
header with `max-age=63072000; includeSubDomains; preload`, and the
domain is on the Chromium HSTS preload list. This means even on the
first connection from a fresh browser, an attacker cannot strip HTTPS
or downgrade to HTTP.
**Evidence:** `evidence/03-hsts-header.png` (Chrome devtools network tab).

### 4. End-to-end encryption defaulted on Signal
Signal encrypts messages and calls end-to-end by default, the protocol
is open-source and independently audited (Cohn-Gordon et al., "A Formal
Security Analysis of the Signal Messaging Protocol", 2017), and the
keys can be verified out-of-band by comparing safety numbers.
**Evidence:** `evidence/04-signal-safety-numbers.png`

### 5. Defence-in-depth at airport security
Perth Airport's domestic departures use four overlapping controls: ID
check, boarding-pass scan, X-ray of carry-ons, and walk-through scanner
plus random ETD swabbing. Each control individually has high false-pass
rates; together they layer to a much lower overall miss probability.
This is a real-world defence-in-depth implementation that maps directly
to the CITS2006 lecture material on layered controls.
**Evidence:** `evidence/05-airport-signage.png` (signage only — no
photos of staff or operational security).

## Reflection
The pattern across the strong implementations is that none of them rely
on a single control. WebAuthn beats SMS not because hardware is
unbreakable but because the cryptographic protocol refuses to leak
credentials to the wrong origin. The mantrap door doesn't rely on the
guard being attentive; it physically cannot be both-open. Good security
removes the single point of failure from the user / operator.

## Note on evidence
All photos are of public-facing signage or my own devices. No security
control was tested or probed.
