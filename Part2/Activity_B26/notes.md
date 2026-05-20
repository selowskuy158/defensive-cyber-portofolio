# B26 — Help Another Student in CITS2006 Understand a Cybersecurity Concept

## Concept I helped with: Public-key cryptography
A classmate in CITS2006 was confused about why public-key
cryptography uses *two* keys, why one is published openly, and why
encryption and digital signatures use the keypair in opposite
directions.

## How I explained it

### Analogy 1 — the mailbox (for encryption)
"Think of your public key as a mailbox slot in the front of your
house. Anyone walking past can drop a letter in (anyone can encrypt
to you). But only you have the key that opens the mailbox from
inside (only your private key can decrypt). Putting your address on
the mailbox doesn't help a stranger steal your mail."

This addresses the most common confusion: *"why is it safe to share
the public key?"* — because publishing the slot location doesn't
help anyone read what's inside.

### Analogy 2 — the wax seal (for signatures)
"For signing it's the opposite. You have a unique wax seal stamp
(your private key) that only you possess. When you stamp a document,
anyone with a copy of the stamp's pattern (your public key) can
verify it was you who stamped it — but they can't make the stamp
themselves."

This addresses the second confusion: *"why is the key usage flipped
for signing vs encryption?"* — because the security property you
want is different. For encryption you want *confidentiality* (only
the holder can read), so the holder's secret key decrypts. For
signing you want *authenticity* (anyone can verify, only the holder
can produce), so the holder's secret key signs.

### Diagram I drew on paper
```
ENCRYPTION                          SIGNING
sender -----[your PUBLIC key]-----> sender -----[their PRIVATE key]-----
            encrypts                            signs
                |                                  |
receiver --[your PRIVATE key]----   receiver --[their PUBLIC key]--
            decrypts                            verifies
```

Drawing the flow side-by-side made it visually obvious that the
direction inverts and that the secret-holding party is different in
each scenario.

## Evidence
- `evidence/b26-teams-thread.png` — screenshot of the actual Teams
  discussion-channel thread where I posted the explanation in
  response to a real question from another student.
- The same explanation (with the diagram) lives in the CITS2006
  Teams channel and is searchable there for any marker that wants
  to verify.

## Reflection
Two things stood out from doing this:

1. **Teaching forces precision.** I had a vague understanding of why
   the keypair is used in opposite directions before this; explaining
   it to someone else forced me to construct the explicit
   confidentiality-vs-authenticity argument. The lesson cemented my
   own understanding more than any solo study would have.

2. **Concrete analogies beat formal definitions.** Saying
   "asymmetric primitive with directional invertibility" is correct
   and useless. "Mailbox vs wax seal" gave my classmate something
   to *remember*, and they came back two days later with a follow-up
   question about hybrid encryption that built directly on the
   analogy.
