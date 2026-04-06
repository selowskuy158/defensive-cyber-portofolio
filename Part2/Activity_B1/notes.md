# B1 - Discover 5 Unique Weak/Vulnerable Security Implementations

**Date:** 5 April, 2026

## Summary
This activity explores weak and vulnerable security implementations that I have observed in real life and online. These are examples of security measures that exist but are poorly implemented or outdated, making them easy for attackers to exploit or bypass. Understanding weak security is just as important as understanding strong security because it helps identify what not to do when designing or implementing security systems.

## Weak/Vulnerable Security Implementations

### 1. HTTP Websites Without Encryption
Some older websites still use HTTP instead of HTTPS, meaning that all data transmitted between the user and the website is sent in plaintext without any encryption. I found several small local business websites in Perth that still use HTTP, which means if someone is on the same network they could intercept sensitive information like login credentials or personal details using a simple packet sniffer tool like Wireshark. This is a very weak security implementation because HTTPS has been the standard for years now and SSL/TLS certificates are even available for free through services like Let's Encrypt.

### 2. Default Credentials on Home Routers
Many home routers come with default usernames and passwords like "admin/admin" or "admin/password" printed on a sticker on the router itself. I checked my neighbour's old router model online and found that the default credentials were publicly listed on the manufacturer's website. If the owner does not change these defaults, anyone who connects to the network could log into the router's admin panel and change settings, redirect traffic, or even lock the real owner out. This is a very common and dangerous weak security practice that many people do not even think about.

### 3. Unencrypted Public WiFi Networks
Many cafes and public spaces in Perth still offer open WiFi networks that do not require a password and have no encryption at all. I noticed this at several places around Northbridge and even at some smaller cafes around Mount Lawley. Without encryption, anyone on the same network can potentially intercept data being sent by other users using man-in-the-middle attacks. This is a weak implementation because at the very minimum these networks should be using WPA2 or WPA3 encryption even if the password is shared publicly.

### 4. Weak Password Policies on Local Websites
I tested creating accounts on several small Australian business websites and found that some of them allowed passwords as short as 4 characters with no requirement for uppercase letters, numbers, or special characters. One website even let me set my password as "1234" without any warning. This is a very weak security implementation because short and simple passwords can be cracked within seconds using brute force attacks. A strong password policy should require a minimum of 8 characters with a mix of different character types.

### 5. Security Cameras with No Night Vision or Blind Spots
I observed that some CCTV cameras installed at a local shopping centre in Perth were positioned in a way that created obvious blind spots, and some older cameras clearly did not have infrared or night vision capability. This means that after dark, the cameras would not be able to capture clear footage which defeats the purpose of having surveillance in the first place. This is a weak physical security implementation because a security system that cannot function properly at night leaves the property vulnerable during the hours when most break-ins actually happen.
