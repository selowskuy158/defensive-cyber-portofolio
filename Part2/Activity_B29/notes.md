# B29 — Fix a 2025 CVE Using Three Generative AI Systems and Compare Consistency

## CVE selected
**CVE-2025-30065** — *Apache Parquet* (Java) deserialization vulnerability.
- **Type:** Unsafe deserialization (CWE-502)
- **Affected:** Apache Parquet Java prior to version 1.15.1
- **CVSS:** 10.0 (Critical)
- **Disclosed:** April 2025
- **Source:** https://nvd.nist.gov/vuln/detail/CVE-2025-30065 ; Apache
  security advisory.

The vulnerability allows arbitrary code execution via crafted Parquet
files that exploit Java deserialization in the Avro Generic record
reader path. Critical because Parquet files are commonly ingested
from untrusted sources in data pipelines (S3 buckets, vendor uploads).

## Method
I gave each of three frontier generative AI assistants the same
prompt:

> "The vulnerability CVE-2025-30065 affects Apache Parquet (Java)
> versions before 1.15.1 — an unsafe deserialization issue in the
> Avro reader allowing arbitrary code execution. Briefly explain the
> vulnerability mechanism, then provide a code-level fix and explain
> why your fix works. Be specific."

Each response was screenshotted in full and saved to `evidence/`.

## AI responses (summary)

### ChatGPT (GPT-4o / GPT-4.1)
- Correctly identified the deserialization root cause.
- Proposed upgrading to Parquet 1.15.1+ as the canonical fix.
- For organisations unable to upgrade immediately: proposed wrapping
  the reader in a `ValidatingObjectInputStream` allow-list
  (whitelist of classes permitted for deserialization).
- Code example was a Java snippet using `commons-io`'s
  `ValidatingObjectInputStream`.
- **Strengths:** complete, with both immediate and defence-in-depth
  mitigations.
- **Weaknesses:** the example didn't explicitly show how to wire the
  allow-list into Parquet's reader chain.

### Google Gemini (Gemini 2.5)
- Same root cause identification.
- Emphasised the Apache Software Foundation security advisory and
  the version upgrade.
- Suggested running parquet readers inside a sandboxed JVM (Java
  Security Manager) as a containment measure.
- **Strengths:** brought in the Java Security Manager angle (which
  ChatGPT didn't).
- **Weaknesses:** Java Security Manager is deprecated in modern JDKs
  (JEP 411), which Gemini did not flag — a minor accuracy slip.

### Claude (Sonnet)
- Same root cause identification.
- Most detailed on *exploit mechanism*: walked through how a malicious
  Avro schema embedded in a Parquet file footer can trigger the
  deserialization sink.
- Proposed (a) upgrade, (b) input validation at the file boundary
  (check magic bytes + reject files with unexpected Avro schemas),
  (c) container-level isolation of the reader process.
- **Strengths:** most thorough threat-modelling and most layers of
  defence.
- **Weaknesses:** longest response; could be excessive for an
  operator who just needs the patch version.

## Consistency comparison

| Aspect | ChatGPT | Gemini | Claude | Consistent? |
|---|---|---|---|---|
| Root cause | unsafe deser | unsafe deser | unsafe deser | Yes |
| Canonical fix | upgrade to 1.15.1 | upgrade to 1.15.1 | upgrade to 1.15.1 | Yes |
| Additional layer | allow-list | sandbox (deprecated) | input validation + isolation | Diverged |
| Cited official advisory | Yes | Yes | Yes | Yes |
| Identified CWE | CWE-502 | CWE-502 | CWE-502 | Yes |

**On the high-stakes facts (root cause, official fix, CVSS, CWE) all
three models agreed and matched the NVD entry.** On the
defence-in-depth recommendations they diverged in useful ways — each
suggested a different secondary control. This is actually a strength
of using multiple AI systems: the union of recommendations is more
robust than any single response.

## Evidence
- `evidence/b29-chatgpt.png`
- `evidence/b29-gemini.png`
- `evidence/b29-claude.png`

## Reflection
The most important finding was that consistency was high on the
**verifiable** facts (CVE ID, version, CWE) and lower on the
**advisory** content (which defence-in-depth control to layer on).
This matches the well-known LLM behaviour: factual recall on
published data is reliable, while open-ended recommendations are
where models pattern-match against their training data and produce
different but individually plausible answers.

For practical use: when relying on an LLM for security work, ask
the same question of multiple models and look at where they
*disagree* — that's where your own verification effort belongs.
