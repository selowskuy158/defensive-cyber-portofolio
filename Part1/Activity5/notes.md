# A5 - Discover Cryptography Used Online

**Date:** 10 March 2026

## Summary
This activity explores how cryptography is used in online systems to protect sensitive information in the digital world. I looked at common examples that people use every day on websites, messaging platforms, and account systems.

## Examples of Cryptography Used Online

### 1. HTTPS/TLS on Websites
- HTTPS uses TLS encryption to protect the data sent between a web browser and a website.
- I checked the secure connection details on the CommBank website and confirmed that the site uses TLS to protect user traffic.
- This matters because encrypted traffic helps prevent attackers from reading passwords, card details, or other private data during transmission.

### 2. End-to-End Encryption in Messaging
- Messaging platforms such as WhatsApp use end-to-end encryption so that only the sender and receiver can read the message contents.
- I checked the security information for a chat and observed the end-to-end encryption notice.
- This is important because it protects private communication from interception by third parties.

### 3. Hashing in Password Storage
- Websites store password hashes rather than storing passwords in plain text.
- I reviewed how password hashing works using the SHA-256 and bcrypt concepts covered in the unit and supporting security guidance.
- This is important because even if a database is exposed, the attacker should not directly see the original user passwords.

## Evidence
- a5-https-tls-commbank.png - HTTPS/TLS verification on CommBank
- a5-whatsapp-e2e-encryption.png - End-to-end encryption note for messaging
- a5-password-hashing-note.png - Password hashing concept summary
