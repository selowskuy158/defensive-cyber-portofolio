# B1 — Discover 5 Unique Weak/Vulnerable Security Implementations

## What I did
Walked around UWA campus and my local area in Mount Lawley over two afternoons
looking for security controls that exist but are mis-implemented. For each I
captured a photo and a short note on why the implementation is weak and what
the realistic attack would look like.

## The five weak implementations

### 1. HTTP-only login page on a Perth small-business site
A local business's customer login page transmits the login form over plain
HTTP (no padlock in the address bar). Anyone on the same Wi-Fi (e.g. a cafe
hotspot) can sniff credentials in cleartext using Wireshark in ~3 minutes.
Free Let's Encrypt certificates have removed every practical excuse for
HTTP-only auth.
**Evidence:** `evidence/01-http-login.png`

### 2. Default-credential sticker on a home router
A neighbour's WAN router has the default admin password printed on a sticker
on the side of the device. Default credentials for almost every consumer
router are indexed publicly on routerpasswords.com. An attacker on the
network can change DNS to a hostile server in under a minute.
**Evidence:** `evidence/02-default-creds-router.png` (sticker cropped to hide
brand/MAC).

### 3. Open Wi-Fi network at a public venue
A cafe in Northbridge advertised "Free Wi-Fi - No Password". Open networks
provide no link-layer encryption, so every device on the network can see
every other device's unencrypted traffic. WPA2 with a shared password
printed on a poster would be a strict improvement.
**Evidence:** `evidence/03-open-wifi-poster.png`

### 4. CCTV blind spot at a retail entrance
A shop near the campus has a CCTV camera mounted directly above its front
door pointing straight down, which gives it no view of anyone standing
within ~2 m of the door (the dead zone immediately under the dome). The
implementation exists, but it doesn't deter or record the most common
threat (someone walking up to the door).
**Evidence:** `evidence/04-cctv-blind-spot.png`

### 5. Shoulder-surfing risk at a self-service kiosk
A self-service kiosk in a shopping centre has its screen facing directly
into the open thoroughfare — anyone walking past can read the PIN being
entered. A simple polarising privacy filter (~$20) would solve it.
**Evidence:** `evidence/05-shoulder-surfing-kiosk.png`

## Reflection
Most weak controls aren't the absence of security — they're the presence of
security applied carelessly (the camera is there but pointing the wrong
way; the password protection exists but the password is "admin"; the login
form exists but goes over HTTP). The lesson for design is that
"implemented" and "implemented correctly" are two different things, and
threat-modelling has to ask both.

## Note on evidence
Photos were captured on my own phone. Faces and identifying brand markings
were cropped or blurred before commit. No private property was entered to
take any photo.
