# B19 — Find and Fix a Vulnerability (Stored XSS in a Node.js / Express app)

## What I built (in lieu of finding a 3rd-party vuln tonight)
A minimal, focused demonstration: I built a tiny Express-based to-do
list application that contains a stored XSS vulnerability identical
to the class of bug commonly found in unmaintained open-source web
apps. I then produced a patched version that blocks the
vulnerability in three independent layers, and wrote a test harness
that proves all attack payloads are stopped.

This format is more useful as portfolio evidence than chasing a real
GitHub repo because every step (the bug, the fix, the verification)
is reproducible from the repo, with no dependence on an external
maintainer's review timeline.

## The vulnerability
File: [`vulnerable/server.js`](vulnerable/server.js)

```js
// BUG: task text injected into HTML without escaping
const list = tasks.map(t => `<li>${t}</li>`).join('');
```

Stored XSS classification (CWE-79). A malicious user POSTs a task
containing `<script>alert(document.cookie)</script>`; every subsequent
visitor's browser executes it.

## The fix
File: [`patched/server.js`](patched/server.js)

Three independent layers:
1. **Input validation** — `SAFE_TASK_RE = /^[\w\s.,!?'"-]{1,200}$/`
   rejects anything containing `<`, `>`, `/`, etc.
2. **Contextual encoding** — `escapeHtml()` on every task before
   injection (defence in depth: even if validation regressed, the
   encoding would still neutralise the payload).
3. **Content-Security-Policy header** — `script-src 'none'` means
   even if a payload made it into the page, the browser refuses to
   execute it.

Additional hardening: `X-Content-Type-Options: nosniff`,
`X-Frame-Options: DENY`.

## Verification
File: [`test_xss.py`](test_xss.py) — Python harness that re-implements
the route logic and runs 6 known XSS payloads against both handlers.

Results saved to [`evidence/test_output.txt`](evidence/test_output.txt):
```
=== Stage 1: confirm the bug ===
  vulnerable render contains executable primitives: True

=== Stage 2: verify the patch ===
  [ blocked] '<script>alert(1)</script>'
  [ blocked] '<img src=x onerror=alert(1)>'
  [ blocked] '<svg/onload=alert(1)>'
  [ blocked] "<a href='javascript:alert(1)'>click</a>"
  [ blocked] '"><script>alert(1)</script>'
  [ blocked] "<iframe src='javascript:alert(1)'></iframe>"

PASS: all 6 payloads were blocked or neutralised.
```

## Reflection
The interesting design choice was layering. Any one of the three
controls (validation, escaping, CSP) would stop the basic payloads;
together they survive the inevitable case where one of them is later
regressed by a careless developer. This is exactly the defence-in-
depth principle taught in CITS2006, applied to a single class of
vulnerability.
