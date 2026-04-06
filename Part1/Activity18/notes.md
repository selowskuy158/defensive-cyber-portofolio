# A18 - Discover Two Hallucination Cases When Using a Generative AI System

**Date:** 2 April, 2026

## Summary
This activity explores the phenomenon of hallucinations in generative AI systems, meaning that the AI generates false or made-up information with confidence. I tested ChatGPT and discovered two clear cases where it hallucinated information, which raises very important concerns for cybersecurity research and decision-making.

## Hallucination Case 1: Made-Up Cybersecurity Tool

**What I tested:** I asked ChatGPT about a tool I created called "SecureVault Pro" - a completely fictional cybersecurity tool that does not actually exist anywhere, meaning that ChatGPT should have said it doesn't know about this tool.

**What happened:** ChatGPT confidently described the tool as if it were real, providing detailed information about features, security protocols, and use cases. It gave me descriptions of functionality like "advanced encryption methods" and "real-time threat detection," so meaning that it completely fabricated specifications for a tool that never existed. The AI presented this false information in a very authoritative way, making it sound like established fact rather than made-up content.

**Why this is dangerous:** For cybersecurity research, this hallucination is very dangerous because researchers might trust AI-generated information and build upon false foundations. If someone was researching cybersecurity tools and encountered this hallucinated tool, they might include it in their analysis, leading to incorrect conclusions and wasted research effort.

## Hallucination Case 2: Non-Existent CVE Number

**What I tested:** I asked ChatGPT for information about a specific CVE number - CVE-2025-44821 - which was a number I made up. I presented it as a recent critical vulnerability in a popular software library that was supposedly discovered in early 2026, meaning that ChatGPT would need to either admit it doesn't have information about future vulnerabilities or correctly identify that this CVE doesn't exist.

**What happened:** ChatGPT provided what seemed like legitimate CVE information, including a description of the vulnerability, affected software versions, and remediation steps. The response included technical jargon and vulnerability scores, making the information appear credible and trustworthy. I noticed that the AI never said "I'm not sure about this CVE" or "I cannot find information about this number," instead it just generated plausible-sounding security details.

**Why this is dangerous:** For cybersecurity researchers and security teams, hallucinated CVE numbers are very dangerous. Organizations might spend resources investigating and patching vulnerabilities that don't exist, or they might miss real vulnerabilities because they are distracted by false ones. If this hallucinated CVE made it into threat intelligence reports or security advisories, it could spread misinformation across the entire industry.

## Key Implications for Cybersecurity Research

1. **Cannot fully trust AI for security research** - Generative AI should never be the sole source for critical security information, even when it sounds confident. Researchers need to verify all information through official sources like CVE databases, vendor security advisories, and peer-reviewed research.

2. **Hallucinations appear very realistic** - The confidence and detail in the AI's responses makes hallucinations especially dangerous because they fool people into thinking the information is real. This is more problematic than obvious errors or refusals.

3. **Risk of misinformation spread** - If cybersecurity professionals use AI-generated information without verification, false information can spread throughout reports, advisories, and organizational security policies, creating cascading problems.

4. **Need for human verification** - Any information from generative AI systems used in cybersecurity contexts must be independently verified against authoritative sources, adding extra work to the research process.

## Conclusion
This activity really helps demonstrate why critical thinking about AI outputs is essential in cybersecurity. The ability of AI to generate convincing false information with confidence means we cannot rely on these systems for accurate security information without additional verification.
