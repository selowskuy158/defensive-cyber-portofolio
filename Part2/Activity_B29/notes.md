# B29 - Find a CVE in This Year and Fix It Using Three Different Generative AI Systems

**Date:** 19 April, 2026

## Summary
This activity involves finding a CVE (Common Vulnerabilities and Exposures) from this year and using three different generative AI systems to propose fixes, then comparing the quality and consistency of their responses. I chose CVE-2026-21407, a path traversal vulnerability in a popular open-source web framework, and asked ChatGPT, Google Gemini, and Claude to explain and fix it.

## CVE Details
- **CVE ID:** CVE-2026-21407
- **Type:** Path Traversal (Directory Traversal)
- **Affected Software:** A popular open-source file management web application
- **Severity:** High (CVSS 8.1)
- **Description:** The vulnerability allows an attacker to access files outside the intended directory by manipulating file path parameters in HTTP requests using sequences like ../ to traverse the directory structure and read sensitive system files.

## AI Responses Comparison

### ChatGPT (GPT-4o)
ChatGPT provided a detailed explanation of the path traversal vulnerability and suggested a fix that involved sanitizing the file path input by removing any ../ sequences and validating that the resolved path stays within the allowed directory. The code example used Python os.path.realpath() to resolve the actual path and then checked if it starts with the allowed base directory. ChatGPT also suggested additional measures like implementing a whitelist of allowed file extensions and adding logging for suspicious path traversal attempts. The response was very comprehensive and well-structured.

### Google Gemini
Gemini provided a similar fix but took a slightly different approach. Instead of just stripping ../ sequences, Gemini suggested using a chroot-like approach where the application runs in a restricted directory environment. The code example used pathlib.Path.resolve() in Python and included a check to ensure the resolved path is a child of the base directory. Gemini also mentioned the importance of configuring web server settings to disable directory listing and restrict access to sensitive directories at the server level. However, Gemini response was slightly less detailed than ChatGPT in terms of the code implementation.

### Claude
Claude provided a very thorough analysis of the vulnerability and suggested a multi-layered fix. The first layer was input validation to reject any path containing suspicious characters or sequences. The second layer used Python os.path.normpath() followed by a prefix check against the base directory. The third layer suggested implementing operating system level file permissions as a defence-in-depth measure. Claude also highlighted potential bypass techniques that attackers might use such as URL encoding the ../ characters or using null bytes, and provided additional validation checks for these. Claude response was the most comprehensive in terms of addressing edge cases and bypass techniques.

### Comparison and Conclusion
All three AI systems correctly identified the nature of the vulnerability and provided valid fixes. ChatGPT was the most well-structured and easy to follow. Gemini offered a unique server-level perspective. Claude was the most thorough in addressing edge cases and bypass techniques. However, I noticed that the three AI systems sometimes gave slightly different code approaches, which shows that there is no single correct way to fix a vulnerability and that it is important to use multiple sources and not rely on just one AI system for security fixes. Comparing the consistency across the three systems helps identify the most robust and comprehensive solution.
