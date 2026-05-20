# B21 — Design and Implement a Cybersecurity Learning Activity

## What I built
An interactive **Phish-or-Legit** quiz: a single-page web app that
shows the user 10 realistic email mock-ups (one at a time), asks them
to classify each as phishing or legitimate, and after each answer
reveals an explanation listing the specific red flags or
legitimacy-signals to look for.

**File:** [`phishing_quiz.html`](phishing_quiz.html) — open in any
browser, no server required.

## Why phishing identification
- Phishing is the leading initial-access vector in every recent
  Verizon DBIR.
- It's the cybersecurity skill with the broadest audience — every
  internet user needs it, regardless of technical background.
- Identification can be taught through pattern recognition, which
  lends itself well to interactive quiz format.

## Question design
The 10 questions are split 6 phishing / 4 legitimate so users practise
both directions. The phishing examples target patterns commonly seen
by Australian users:
- Typo-squatted sender domains (paypa1-support.com vs paypal.com)
- Urgency/threat language ("suspended in 24 hours")
- HTTP credential forms
- Australia Post / ATO impersonation (very common in AU)
- UWA scholarship-prize scams (relevant to the audience)
- Microsoft 365 fake password-expiry alerts

The 4 legitimate emails (GitHub OAuth, UWA IT maintenance, LinkedIn
invitation, Google security alert) deliberately have features that
*could* look suspicious — so users learn not to over-flag, which is a
common failure mode of naive phishing training.

## Explanation design
Each question's explanation card lists 3–4 specific signals the user
should have noticed (sender domain, link target, urgency language,
credential request). The pattern across the explanations builds an
implicit checklist by the end of the quiz.

## Final results page
- Shows score out of 10 with a contextual message.
- Lists the questions the user got wrong.
- Provides a six-point red-flag summary so the takeaway survives
  past the quiz.

## Reflection
The hardest design decision was the 6/4 split — naive phishing quizzes
make every email a phish, which trains users to be paranoid rather
than discerning. Including legitimate emails (especially ones with
suspicious-looking features like the LinkedIn invitation) better
mirrors the real inbox.

## Evidence
- The file itself: [`phishing_quiz.html`](phishing_quiz.html)
- `evidence/b21-quiz-question.png` — screenshot of a question with an
  expanded explanation card
- `evidence/b21-quiz-results.png` — screenshot of the final results
  page
