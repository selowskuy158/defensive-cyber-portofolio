# A4 - Discover a Vulnerable Website

**Date:** 8 March, 2026

## Summary
This activity explores finding security vulnerabilities on a deliberately vulnerable test website, meaning that I set up a local instance of OWASP Juice Shop to practice identifying common web application security flaws. I tested this by attempting various attacks against the application and discovered multiple vulnerabilities that match common OWASP Top 10 categories.

## Vulnerabilities Discovered

### 1. Unsafe Reflected Input (XSS Risk)
- **What it is:** The website reflects user input back into the page without proper sanitization, meaning that user-controlled content appears directly in the response.
- **How I found it:** I tested the search feature and confirmed that custom input was reflected back into the page output. This shows unsafe handling of input and a possible XSS risk if script execution is also allowed.
- **Why it matters:** When websites reflect unsafe input, attackers may be able to inject malicious content that misleads users or executes unwanted browser behavior depending on how the application renders the response.

### 2. Unauthorized Account Access
- **What it is:** The application does not properly enforce access controls, meaning that account data can be accessed by changing the user ID in the URL parameter.
- **How I tested this:** I manually changed the account ID in the request and the application returned another user's profile data without checking whether I was authorized to view it.
- **The vulnerability:** This happens because the backend does not properly verify whether the requestor should be allowed to access that specific account record.

### 3. Weak Login Credentials
- **What it is:** The website accepts a very weak default credential combination, which means the login protection can be bypassed by guessing common administrator credentials.
- **How I discovered it:** I tested a simple credential pair, `admin/admin`, and the application accepted it immediately.
- **Security impact:** Weak default credentials make unauthorized access much easier and show poor authentication practice for any application.

## Evidence
- a4-reflected-input.png - Shows the XSS payload being executed in the browser
- a4-unauthorized-account.png - Shows accessing another user's account without authorization
- a4-weak-login.png - Shows successful login with default weak credentials
