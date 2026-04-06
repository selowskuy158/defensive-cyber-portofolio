# B22 - Enhance the Cybersecurity of a Website from Your Community

**Date:** 15 April, 2026

## Summary
This activity involves helping to improve the cybersecurity of a website belonging to a community organisation. I volunteered to help a local Perth community sports club improve the security of their WordPress website after noticing several security issues during a casual conversation with the club committee member.

## Details

### The Website
The community sports club based in Mount Lawley had a WordPress website that was used to share club news, event schedules, and membership registration. The website had several security issues that I identified and helped fix with the permission of the club committee.

### Security Issues Found
First, the website was still using HTTP instead of HTTPS, meaning that all data including membership registration forms with personal details were being transmitted in plaintext. Second, the WordPress installation was running an outdated version that had known security vulnerabilities. Third, the admin login page was accessible at the default /wp-admin URL with no rate limiting or CAPTCHA, making it vulnerable to brute force attacks. Fourth, there were several outdated plugins installed that had known security vulnerabilities. Fifth, the website did not have any backup system in place.

### Security Improvements Made
With the club permission, I made several security improvements. I installed a free SSL certificate using Let's Encrypt and configured the website to use HTTPS for all pages, ensuring that all data transmitted between users and the website is encrypted. I updated WordPress to the latest version and updated all plugins to their latest versions, removing plugins that were no longer maintained. I installed a security plugin called Wordfence that adds features like brute force protection, login rate limiting, a web application firewall, and malware scanning. I changed the admin login URL from the default /wp-admin to a custom URL to make it harder for attackers to find the login page. I also set up an automated weekly backup system using a free backup plugin that stores backups to Google Drive.

### Result
After implementing these changes, the website security was significantly improved. The Wordfence security scan showed no remaining critical vulnerabilities, and the website was now using HTTPS with a valid SSL certificate. The club committee was very grateful for the help and said they had no idea their website had so many security issues.
