# B20 - Enhance the Security of a GitHub Project

**Date:** 14 April, 2026

## Summary
This activity involves enhancing the security of a GitHub project by implementing security best practices and improvements. I chose to enhance the security of my own defensive-cyber-portofolio GitHub repository by implementing several security features and configurations that protect the repository and its contents.

## Security Enhancements Made

### 1. Added .gitignore for Sensitive Files
I created a comprehensive .gitignore file that prevents sensitive files from being accidentally committed to the repository. This includes patterns for environment files (.env), credentials files, private keys, database files, and operating system generated files like .DS_Store. This is important because accidentally committing sensitive data to a public repository is one of the most common security mistakes developers make, and once data is pushed to GitHub it can be very difficult to completely remove even if the commit is deleted.

### 2. Enabled Branch Protection Rules
I configured branch protection rules on the main branch of my repository to prevent direct pushes without a pull request review. This means that any changes to the main branch must go through a pull request, which adds a layer of review before code or content is merged. While this is more relevant for collaborative projects, it is a good security practice to learn and implement because it prevents unauthorized or accidental changes to the main codebase.

### 3. Added Security Policy (SECURITY.md)
I created a SECURITY.md file in the repository that outlines how to report security vulnerabilities if someone finds one in the project. This is a standard practice in open-source projects and shows that the project takes security seriously. The policy includes contact information and a description of the responsible disclosure process.

### 4. Enabled Dependabot Alerts
I enabled GitHub Dependabot alerts on the repository to automatically monitor dependencies for known security vulnerabilities. Although my portfolio repository does not have many code dependencies, this feature is important because outdated or vulnerable dependencies are a common attack vector in software projects. Dependabot automatically creates pull requests to update vulnerable dependencies when patches are available.

### 5. Added Commit Signing
I configured GPG commit signing for my GitHub account so that all my commits are cryptographically signed, proving that the commits actually came from me and were not tampered with. This is an important security feature because unsigned commits could potentially be forged by someone pretending to be the repository owner.
