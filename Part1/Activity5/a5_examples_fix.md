# A5 - Examples Fix (to be added to portfolio)

## Examples of Cryptography Used Online:

### HTTPS/TLS on Websites
HTTPS which stands for HyperText Transfer Protocol Secure is the most common use of cryptography on the internet. The way it works is by using TLS (Transport Layer Security) protocol to encrypt the data being sent between the browser and the web server, meaning that if someone tries to intercept the data, they will not be able to read it because it is encrypted. I tested this by visiting my bank website (CommBank) and checking the padlock icon on the address bar which shows that the connection is secured with TLS encryption. Without HTTPS, any data sent through the website like passwords, credit card numbers, and personal information could be intercepted by attackers using a man-in-the-middle attack.

### End-to-End Encryption in Messaging (Signal Protocol)
Many messaging platforms such as WhatsApp, Signal, and Facebook Messenger use end-to-end encryption to protect messages sent between users. The encryption is based on the Signal Protocol, which works by generating unique encryption keys for each conversation, meaning that only the sender and receiver can decrypt and read the messages. I verified this on my WhatsApp by opening a chat and checking the security information which shows the encryption status. Even WhatsApp as a company cannot read the content of the messages because they do not have access to the encryption keys, this shows how important end-to-end encryption is for protecting private communication online.

### Hashing in Password Storage
Websites and online platforms use cryptographic hashing algorithms such as SHA-256 or bcrypt to store user passwords securely. The way it works is that when a user creates an account and sets a password, the website does not store the actual password in plaintext but instead stores a hashed version of the password. So when the user logs in again, the website hashes the input password and compares it with the stored hash to check if they match. I learned about this in the CITS2006 unit and it is a very important security practice because even if an attacker gains access to the database, they cannot directly see the passwords, they would only see the hash values which are very difficult to reverse back to the original password.
