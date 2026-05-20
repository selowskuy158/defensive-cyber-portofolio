"""Exploit + fix verification for B19. Runs without Node.

Re-implements the route logic from server.js in Python so we can verify, in a
single test pass, that the same payloads execute in the vulnerable handler but
are blocked by the patched handler's three layers.
"""
from __future__ import annotations

import re


# ---- mirrored handlers ------------------------------------------------------
def vulnerable_render(tasks: list[str]) -> str:
    list_html = "".join(f"<li>{t}</li>" for t in tasks)
    return f"<ul>{list_html}</ul>"


def escape_html(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#39;"))


SAFE_TASK_RE = re.compile(r"^[\w\s.,!?'\"-]{1,200}$")


def patched_handle_add(task: str) -> tuple[bool, str]:
    task = task.strip()
    if not SAFE_TASK_RE.match(task):
        return False, "rejected"
    return True, escape_html(task)


# ---- exploit suite ---------------------------------------------------------
PAYLOADS = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>",
    "<a href='javascript:alert(1)'>click</a>",
    "\"><script>alert(1)</script>",
    "<iframe src='javascript:alert(1)'></iframe>",
]


def fires_xss(html: str) -> bool:
    """A naive heuristic: does the output contain an unescaped script-execution
    primitive?  Matches what a browser would also treat as executable."""
    lowered = html.lower()
    bad = ["<script", "onerror=", "onload=", "javascript:", "<iframe", "<svg"]
    return any(b in lowered for b in bad)


def main() -> int:
    print("=== Stage 1: confirm the bug ===")
    rendered = vulnerable_render(PAYLOADS)
    bug_fires = fires_xss(rendered)
    print(f"  vulnerable render contains executable primitives: {bug_fires}")
    assert bug_fires, "expected vulnerable handler to leak payloads"

    print("\n=== Stage 2: verify the patch ===")
    survived = []
    for p in PAYLOADS:
        ok, output = patched_handle_add(p)
        # Either rejected outright, or escaped to inert HTML entities
        if ok and fires_xss(output):
            survived.append((p, output))
        marker = "blocked" if not ok else "escaped"
        print(f"  [{marker:>8}] {p[:50]!r:<55} -> {output[:60]!r}")

    print()
    if survived:
        print(f"FAIL: {len(survived)} payload(s) bypassed the patch")
        for p, o in survived:
            print(f"  {p!r} -> {o!r}")
        return 1
    print(f"PASS: all {len(PAYLOADS)} payloads were blocked or neutralised.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
