#!/usr/bin/env python3
"""
password_audit.py — Personal Password Security Auditor
CITS2006 Activity B27: Apply a cybersecurity concept to a real-world problem.

Concept applied: password security (credential hygiene, breach exposure,
entropy analysis, policy compliance).

This tool audits a set of passwords against four security dimensions:
  1. BREACH EXPOSURE — checks HaveIBeenPwned via the k-anonymity API
     (only the first 5 chars of the SHA-1 hash are sent; the full
     password never leaves your machine).
  2. ENTROPY — calculates Shannon entropy and estimates brute-force
     time against offline attack rates.
  3. POLICY COMPLIANCE — checks against NIST SP 800-63B guidelines
     (length ≥ 8, no pure-numeric, no common patterns).
  4. PATTERN DETECTION — flags dictionary words, keyboard walks,
     repeated characters, and date patterns.

Usage:
    python3 password_audit.py                    # audit built-in demo passwords
    python3 password_audit.py --interactive      # enter your own passwords
    python3 password_audit.py --file passwords.txt  # audit from file (one per line)

The tool NEVER stores, logs, or transmits full passwords. The only
network call is the k-anonymity HIBP lookup (5-character SHA-1 prefix).
"""

import hashlib
import math
import re
import sys
import json
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
HIBP_API = "https://api.pwnedpasswords.com/range/"
COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123",
    "monkey", "1234567", "letmein", "trustno1", "dragon",
    "baseball", "iloveyou", "master", "sunshine", "ashley",
    "bailey", "shadow", "123456789", "1234567890", "password1",
    "admin", "welcome", "login", "starwars", "solo",
}
KEYBOARD_WALKS = [
    "qwerty", "asdf", "zxcv", "qazwsx", "1qaz2wsx",
    "!@#$%", "1234", "4321", "abcd", "dcba",
]
DATE_PATTERN = re.compile(
    r"(19|20)\d{2}[/-]?\d{2}[/-]?\d{2}|"   # YYYY-MM-DD
    r"\d{2}[/-]\d{2}[/-](19|20)\d{2}|"       # DD-MM-YYYY
    r"(0[1-9]|1[0-2])(19|20)\d{2}"           # MMYYYY
)

# Offline attack rates (guesses per second)
ATTACK_RATES = {
    "Online (rate-limited)":      100,
    "Offline (MD5, single GPU)":  50_000_000_000,
    "Offline (bcrypt, single GPU)": 30_000,
}


# ---------------------------------------------------------------------------
# Breach check via HaveIBeenPwned k-anonymity API
# ---------------------------------------------------------------------------
def check_hibp(password: str) -> int | None:
    """
    Check if a password appears in the HIBP breached-password database.
    Uses k-anonymity: only the first 5 hex chars of the SHA-1 hash are
    sent to the API. Returns the breach count, or None if the API is
    unreachable.
    """
    try:
        import urllib.request
        sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
        prefix, suffix = sha1[:5], sha1[5:]
        req = urllib.request.Request(
            HIBP_API + prefix,
            headers={"User-Agent": "CITS2006-PasswordAudit/1.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read().decode("utf-8")
        for line in body.splitlines():
            parts = line.split(":")
            if parts[0] == suffix:
                return int(parts[1])
        return 0
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Entropy calculation
# ---------------------------------------------------------------------------
def calculate_entropy(password: str) -> float:
    """Shannon entropy in bits, based on character-class pool size."""
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"\d", password):
        pool += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        pool += 32
    if pool == 0:
        return 0.0
    return len(password) * math.log2(pool)


def crack_time_display(entropy: float, rate: float) -> str:
    """Human-readable brute-force time estimate."""
    seconds = (2 ** entropy) / rate / 2  # average = half the keyspace
    if seconds < 1:
        return "< 1 second"
    elif seconds < 60:
        return f"{seconds:.0f} seconds"
    elif seconds < 3600:
        return f"{seconds / 60:.1f} minutes"
    elif seconds < 86400:
        return f"{seconds / 3600:.1f} hours"
    elif seconds < 86400 * 365:
        return f"{seconds / 86400:.1f} days"
    elif seconds < 86400 * 365 * 1e6:
        return f"{seconds / (86400 * 365):.1f} years"
    else:
        return f"{seconds / (86400 * 365):.2e} years"


# ---------------------------------------------------------------------------
# Policy & pattern checks
# ---------------------------------------------------------------------------
def check_nist_policy(password: str) -> list[str]:
    """Check against NIST SP 800-63B password guidelines."""
    issues = []
    if len(password) < 8:
        issues.append("Too short (NIST minimum: 8 characters)")
    if password.isdigit():
        issues.append("All-numeric (easily guessable)")
    if password.lower() in COMMON_PASSWORDS:
        issues.append("On the common-passwords blocklist")
    if len(set(password)) <= 2:
        issues.append("Too few unique characters")
    return issues


def detect_patterns(password: str) -> list[str]:
    """Detect weak patterns in the password."""
    patterns = []
    lower = password.lower()

    # Keyboard walks
    for walk in KEYBOARD_WALKS:
        if walk in lower:
            patterns.append(f"Keyboard walk detected: '{walk}'")
            break

    # Repeated characters (aaa, 111)
    if re.search(r"(.)\1{2,}", password):
        patterns.append("Repeated character sequence (3+)")

    # Sequential digits (123, 456)
    for i in range(len(password) - 2):
        if password[i:i+3].isdigit():
            a, b, c = int(password[i]), int(password[i+1]), int(password[i+2])
            if b - a == 1 and c - b == 1:
                patterns.append("Sequential digits detected")
                break

    # Date pattern
    if DATE_PATTERN.search(password):
        patterns.append("Date pattern detected (possible birthday/anniversary)")

    # Leet-speak substitution of common words
    leet_map = str.maketrans("@013$7!", "aolestt")
    decoded = lower.translate(leet_map)
    if decoded in COMMON_PASSWORDS:
        patterns.append(f"Leet-speak variant of common password '{decoded}'")

    return patterns


# ---------------------------------------------------------------------------
# Password strength rating
# ---------------------------------------------------------------------------
def rate_password(entropy: float, breach_count: int | None,
                  policy_issues: list, patterns: list) -> tuple[str, str]:
    """Return (rating, colour_code)."""
    score = 0

    # Entropy scoring
    if entropy >= 60:
        score += 3
    elif entropy >= 45:
        score += 2
    elif entropy >= 30:
        score += 1

    # Breach penalty
    if breach_count is not None and breach_count > 0:
        score -= 2
    elif breach_count == 0:
        score += 1

    # Policy penalty
    score -= len(policy_issues)

    # Pattern penalty
    score -= len(patterns)

    if score >= 3:
        return "STRONG", "green"
    elif score >= 1:
        return "MODERATE", "yellow"
    else:
        return "WEAK", "red"


# ---------------------------------------------------------------------------
# Audit a single password
# ---------------------------------------------------------------------------
def audit_password(password: str, label: str = "") -> dict:
    """Run all checks on a single password and return a result dict."""
    entropy = calculate_entropy(password)
    breach_count = check_hibp(password)
    policy_issues = check_nist_policy(password)
    patterns = detect_patterns(password)
    rating, colour = rate_password(entropy, breach_count, policy_issues, patterns)

    return {
        "label": label,
        "length": len(password),
        "entropy_bits": round(entropy, 1),
        "breach_count": breach_count,
        "policy_issues": policy_issues,
        "patterns": patterns,
        "rating": rating,
        "colour": colour,
        "crack_times": {
            name: crack_time_display(entropy, rate)
            for name, rate in ATTACK_RATES.items()
        },
    }


# ---------------------------------------------------------------------------
# Demo passwords (intentionally weak/strong mix for testing)
# ---------------------------------------------------------------------------
DEMO_PASSWORDS = [
    ("Email account",        "password123"),
    ("Banking app",          "Chris2004!"),
    ("University portal",    "qwerty"),
    ("Gaming account",       "Tr0ub4dor&3"),
    ("Password manager",     "correct-horse-battery-staple-2026"),
    ("Old Wi-Fi password",   "12345678"),
    ("Work VPN",             "j$9Kx!mP2@vL7nQ"),
    ("Social media",         "iloveyou"),
]


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------
def format_report(results: list[dict]) -> str:
    """Format audit results as a readable text report."""
    lines = []
    lines.append("=" * 70)
    lines.append("  PASSWORD SECURITY AUDIT REPORT")
    lines.append("  CITS2006 B27 — Real-world application of password security concepts")
    lines.append("=" * 70)
    lines.append(f"  Date:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
    lines.append(f"  Passwords: {len(results)} audited")
    lines.append(f"  HIBP API:  k-anonymity (SHA-1 prefix only; full password never sent)")
    lines.append("")

    strong = sum(1 for r in results if r["rating"] == "STRONG")
    moderate = sum(1 for r in results if r["rating"] == "MODERATE")
    weak = sum(1 for r in results if r["rating"] == "WEAK")
    breached = sum(1 for r in results if r["breach_count"] and r["breach_count"] > 0)

    lines.append(f"  OVERALL: {strong} strong, {moderate} moderate, {weak} weak")
    lines.append(f"  BREACHED: {breached} of {len(results)} passwords found in known breaches")
    lines.append("")

    for i, r in enumerate(results, 1):
        lines.append("-" * 70)
        label = r["label"] or f"Password #{i}"
        masked = r["length"] * "*"
        lines.append(f"  [{i}] {label}")
        lines.append(f"      Password:  {masked} ({r['length']} chars)")
        lines.append(f"      Rating:    [{r['rating']}]")
        lines.append(f"      Entropy:   {r['entropy_bits']} bits")

        if r["breach_count"] is not None:
            if r["breach_count"] > 0:
                lines.append(f"      HIBP:      BREACHED ({r['breach_count']:,} times in known leaks)")
            else:
                lines.append(f"      HIBP:      Not found in breaches")
        else:
            lines.append(f"      HIBP:      API unreachable (skipped)")

        if r["policy_issues"]:
            lines.append(f"      Policy:    FAIL")
            for issue in r["policy_issues"]:
                lines.append(f"                 - {issue}")
        else:
            lines.append(f"      Policy:    PASS (NIST SP 800-63B compliant)")

        if r["patterns"]:
            lines.append(f"      Patterns:")
            for p in r["patterns"]:
                lines.append(f"                 - {p}")

        lines.append(f"      Crack time estimates:")
        for name, t in r["crack_times"].items():
            lines.append(f"         {name:40s} {t}")

        lines.append("")

    # Recommendations
    lines.append("=" * 70)
    lines.append("  RECOMMENDATIONS")
    lines.append("=" * 70)
    lines.append("")

    if breached > 0:
        lines.append("  [CRITICAL] Change all breached passwords immediately.")
        lines.append("  Breached passwords are actively used in credential-stuffing attacks.")
        lines.append("")

    if weak > 0:
        lines.append("  [HIGH] Replace all WEAK passwords with randomly generated ones.")
        lines.append("  Use a password manager (Bitwarden is free) to generate and store")
        lines.append("  unique 16+ character passwords for every account.")
        lines.append("")

    lines.append("  [BEST PRACTICE] Enable 2FA/MFA on all accounts that support it.")
    lines.append("  Even a strong password is insufficient if the site gets breached")
    lines.append("  and the hash is cracked — 2FA adds an independent second factor.")
    lines.append("")
    lines.append("  [BEST PRACTICE] Use a passphrase (4+ random words) for passwords")
    lines.append("  you need to type manually (master password, device unlock).")
    lines.append("  Passphrases are easier to remember and harder to crack than short")
    lines.append("  complex strings.")
    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    mode = "demo"
    passwords = []

    if "--interactive" in sys.argv:
        mode = "interactive"
        print("Enter passwords to audit (one per line, empty line to finish):")
        while True:
            try:
                line = input("  > ")
            except EOFError:
                break
            if not line:
                break
            label = input("  Label (optional): ").strip() or f"Password #{len(passwords)+1}"
            passwords.append((label, line))
    elif "--file" in sys.argv:
        mode = "file"
        idx = sys.argv.index("--file") + 1
        if idx >= len(sys.argv):
            print("Error: --file requires a filename argument")
            sys.exit(1)
        with open(sys.argv[idx]) as f:
            for i, line in enumerate(f, 1):
                pw = line.strip()
                if pw:
                    passwords.append((f"Password #{i}", pw))
    else:
        mode = "demo"
        passwords = DEMO_PASSWORDS

    if not passwords:
        print("No passwords to audit.")
        sys.exit(0)

    print(f"\nAuditing {len(passwords)} password(s)...\n")

    results = []
    for label, pw in passwords:
        result = audit_password(pw, label)
        # Print progress
        icon = {"STRONG": "+", "MODERATE": "~", "WEAK": "!"}[result["rating"]]
        breach_str = ""
        if result["breach_count"] is not None and result["breach_count"] > 0:
            breach_str = f" [BREACHED x{result['breach_count']:,}]"
        print(f"  [{icon}] {label:30s} {result['rating']:10s} "
              f"{result['entropy_bits']:5.1f} bits{breach_str}")
        results.append(result)

    report = format_report(results)
    print("\n" + report)

    # Save report
    evidence_dir = os.path.join(os.path.dirname(__file__), "evidence")
    os.makedirs(evidence_dir, exist_ok=True)
    output_path = os.path.join(evidence_dir, "audit_report.txt")
    with open(output_path, "w") as f:
        f.write(report)
    print(f"\nReport saved to: {output_path}")

    # Save machine-readable results (without actual passwords)
    json_path = os.path.join(evidence_dir, "audit_results.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"JSON results saved to: {json_path}")


if __name__ == "__main__":
    main()
