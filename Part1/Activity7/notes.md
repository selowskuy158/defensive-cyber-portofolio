# A7 - Discover Cryptography Used in Modern Networks

**Date:** 16 March, 2026
**Location:** Perth, Western Australia

## Summary
This activity explores cryptographic implementations used in modern network communications, meaning that I investigated how encryption protects data when traveling across networks in my home setup and on the internet. I tested this by examining the encryption protocols used on different devices and services I use in Perth.

## Cryptographic Examples Found

### 1. WPA3 on Home WiFi Router
- **What it is:** WPA3 is the latest WiFi security standard that uses 192-bit encryption, so meaning that my home WiFi network uses a really strong encryption algorithm called CCMP (Counter Mode with CBC-MAC Protocol) to protect all wireless traffic.
- **How I discovered it:** I checked my home router settings in Perth and found the security type listed as "WPA3-Personal", which uses a pre-shared key (PSK) that gets hashed with modern cryptography.
- **How it works:** When I connect my laptop or phone to the WiFi, the router and device perform a handshake using AES encryption, making sure that even if someone captures the network traffic, they cannot read the data without the password.
- **Why it matters:** This prevents unauthorized access to my home network and protects all the data I send through WiFi, which is very important when sending sensitive information like bank details or emails over wireless networks.

### 2. VPN Encryption (NordVPN)
- **What it is:** I use NordVPN to encrypt all my internet traffic, meaning that my ISP and other networks cannot see what websites I visit or what data I send, so basically my entire connection gets wrapped in cryptography.
- **How I tested this:** I connected to a NordVPN server in Australia and checked my IP address, which changed to the VPN server's IP, and then I used Wireshark to observe that my traffic was encrypted using IKEv2 protocol with AES-256 encryption.
- **The technology:** NordVPN creates a tunnel through the internet using AES-256-GCM encryption and IKEv2 key exchange protocol, making sure that my data stays confidential even on public WiFi networks in Perth.
- **Real-world usage:** When I browse the internet through NordVPN, all my data is encrypted end-to-end, so meaning that even if someone intercepts my connection at a cafe, they would only see encrypted packets with no readable content.

### 3. TLS/SSL on HTTPS Websites
- **What it is:** Every website that starts with "https://" uses TLS (Transport Layer Security) encryption, meaning that when I visit a bank website or email service, my data is encrypted using public-key cryptography and AES symmetric encryption.
- **How I discovered it:** I opened my browser's developer tools and checked the SSL certificate details on various websites like banking sites and social media, finding certificates issued by trusted certificate authorities like DigiCert and GlobalSign.
- **How the handshake works:** My browser performs a TLS handshake using RSA or ECDHE key exchange to establish a shared encryption key, and then AES-256 encrypts all subsequent communication with the web server, making sure that usernames, passwords, and personal data stay secret.
- **Why websites need this:** Without TLS, a man-in-the-middle attacker could intercept my login credentials or payment information on unsecured WiFi, so HTTPS with TLS is very important for protecting sensitive online transactions.

## Evidence
- a7-router-wpa3-settings.png - WPA3 router encryption settings
- a7-nordvpn-connection.png - VPN connection details and protocol summary
- a7-https-tls-certificate.png - HTTPS/TLS certificate observation summary
