# B14 — Teach Friends About Cybersecurity (Password Hygiene + Password Managers)

## Topic
Password reuse is the single most common entry point for account
takeover (credential stuffing is a top-three attack vector in every
recent Verizon DBIR). I ran a short, practical session for two friends
covering: why reuse is dangerous, how to check if your email has been
breached, and how to set up a password manager.

## Session structure (~20 minutes)
1. **Show, don't tell.** Asked each friend to check their main email
   on https://haveibeenpwned.com. Both had at least one breach hit,
   which made the rest of the conversation concrete instead of
   abstract.
2. **Why reuse matters.** Walked through credential stuffing in plain
   language: one breached site → automated tries on every other site.
   The breach screenshot from HIBP made this real.
3. **Live demo of Bitwarden.** Installed the Bitwarden browser
   extension, set up the master password, imported a couple of their
   saved-in-browser passwords. Generated a 20-character random
   password for one of their sites.
4. **What to do this week.** I gave them a 3-step plan to migrate
   their highest-value accounts (email + bank) first.

## Evidence
- `evidence/b14-chat.png` — screenshot of the group chat with the
  session invite + HIBP result discussion.
- `evidence/b14-haveibeenpwned.png` — screenshot of a HIBP result
  (with identifying information redacted).

## What I learned
Three things that surprised me:
- Both friends were aware that password reuse was "bad" but had never
  seen what a credential-stuffing list looks like; the abstract risk
  turned concrete the moment they saw their email had been breached.
- The friction of password managers is mostly in the *first day* — the
  browser autofill experience after migration is actually faster than
  remembering passwords.
- People are much more receptive to security advice when it comes with
  a working tool and a concrete next step, not a lecture.
