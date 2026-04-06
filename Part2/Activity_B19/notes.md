# B19 - Find and Fix a Vulnerability from a GitHub Project

**Date:** 14 April, 2026

## Summary
This activity involves finding a security vulnerability in an open-source GitHub project and implementing a fix for it. I searched for projects with known security issues on GitHub and found a simple Node.js web application with an XSS (Cross-Site Scripting) vulnerability that I was able to identify and fix.

## Details

### Finding the Vulnerability
I searched GitHub for small open-source web applications that had open security-related issues. I found a simple to-do list application written in Node.js and Express that had an XSS vulnerability in the task input field. The application took user input from a text field and rendered it directly into the HTML page without sanitizing it, meaning that if a user typed a script tag as their task name, the JavaScript code would execute in the browser when the page loaded. I confirmed this by cloning the repository, running the app locally, and entering a simple XSS payload in the task field which triggered an alert box.

### Implementing the Fix
To fix the XSS vulnerability, I implemented input sanitization using the DOMPurify library on the client side and also added server-side input validation using the express-validator middleware. On the server side, I added a validation rule that strips any HTML tags from the user input before saving it to the database. On the client side, I added DOMPurify to sanitize any HTML content before rendering it in the DOM. I also set the Content-Security-Policy header on the server to restrict inline script execution as an additional layer of protection.

### Testing the Fix
After implementing the fix, I tested it by attempting the same XSS payloads that worked before. None of the payloads executed anymore because the input was being properly sanitized both on the server and client side. I also tested with more advanced XSS payloads including event handler attributes and URL-encoded payloads, and all were successfully blocked.

### Submitting the Fix
I created a pull request on the GitHub repository with a clear description of the vulnerability, how it could be exploited, and the changes I made to fix it. I also included screenshots showing the vulnerability before and after the fix. The repository owner reviewed and merged my pull request, which was a great feeling knowing that I contributed to making an open-source project more secure.
