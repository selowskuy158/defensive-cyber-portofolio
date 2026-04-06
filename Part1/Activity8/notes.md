# A8 - Discover Cryptography Used in Internet of Things Devices

**Date:** 17 March, 2026
**Location:** Perth, Western Australia

## Summary
This activity displays how encryption is used in smart home devices to protect data and communications, meaning that modern IoT devices in homes have built-in cryptography to keep user data secure. I tested this by examining the security features on several smart devices in my Perth home and researching their encryption implementations.

## IoT Device Cryptography Examples

### 1. Smart Lock with AES Encryption
- **What it is:** My smart front door lock uses AES-128 encryption to secure the communication between my smartphone app and the lock hardware, so meaning that when I unlock my door remotely, the unlock command gets encrypted with a 128-bit key.
- **How I discovered it:** I checked the lock's documentation and found that it communicates via Bluetooth with AES-128 encryption, and I also observed the encrypted Bluetooth traffic using a packet sniffer, seeing only hex data that I could not read.
- **How it protects my home:** When someone tries to unlock my door remotely or locally, the smart lock verifies the encrypted unlock command using a shared secret key, making sure that only authorized devices with the correct key can open the lock.
- **The risk if not encrypted:** Without encryption, an attacker could intercept the Bluetooth signal and either replay the unlock command or forge a fake command, meaning my home would not be secure, so the AES encryption is very important.

### 2. Smart Speaker (Google Home) with TLS
- **What it is:** My Google Home device uses TLS (Transport Layer Security) to encrypt all communication with Google's servers, meaning that voice commands and personal information get sent over an encrypted HTTPS connection instead of plain text.
- **How I tested this:** I captured network traffic from my Google Home using Wireshark and observed that all data going to Google servers uses TLS 1.3 encryption with AES-256-GCM cipher suite, showing that the traffic is properly encrypted.
- **What gets protected:** When I ask Google Home questions about my calendar, shopping, or give it smart home commands, these requests are encrypted so that my ISP, WiFi neighbors, or hackers on the network cannot read what I'm asking.
- **Why this is critical:** Voice data and smart home commands can reveal very personal information about my daily routines and preferences, so meaning that TLS encryption is really important to protect my privacy in my Perth home.

### 3. Smart Doorbell Camera with Encrypted Video Storage
- **What it is:** My smart doorbell camera records video and stores it encrypted in the cloud, meaning that the video file itself is encrypted using AES-256 encryption even while stored on the company's servers.
- **How encryption works:** When the doorbell camera records video, it encrypts the footage client-side using a unique encryption key stored on the device, and then uploads the encrypted video to cloud storage, making sure that even the company's employees cannot watch my footage.
- **How I verified this:** I checked the doorbell's app settings and found an option to enable "end-to-end encryption" which the documentation says uses AES-256 encryption, and I also reviewed the company's privacy policy confirming they cannot decrypt videos without my key.
- **Real-world benefit:** This means my doorbell video is protected from data breaches, meaning that if the company's servers get hacked, thieves cannot see my front door footage or understand my daily patterns, so this encryption is very important for home security and privacy.

## Evidence
- a8-smart-lock-encryption.png - Smart lock encryption summary showing AES protection
- a8-google-home-security.png - Google Home encrypted traffic observation
- a8-smart-doorbell-encryption.png - Smart doorbell encrypted storage and privacy summary
