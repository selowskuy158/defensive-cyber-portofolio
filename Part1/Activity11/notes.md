# A11 - Discover 5 Unique Access Control Devices

**Date:** 25 March, 2026
**Location:** Perth, Western Australia

## Summary
This activity explores different physical and digital access control mechanisms used to restrict entry to secure areas, meaning that I investigated various devices that verify identity and grant or deny access. I observed these devices around Perth including on the UWA campus, office buildings, and in my home, and discovered that each uses different technology to authenticate users.

## Access Control Devices Discovered

### 1. Biometric Fingerprint Scanner
- **Where found:** UWA campus building lab access, office building entry
- **How it works:** The fingerprint scanner uses optical or capacitive sensors to capture the ridge pattern of a fingertip, then compares it against stored fingerprints in a database using pattern matching algorithms, making sure that only enrolled users can pass.
- **Why it's effective:** Fingerprints are unique to each person and cannot be easily faked or stolen like a keycard, so meaning that fingerprint biometrics are very secure for protecting sensitive areas like server rooms and research labs.
- **What I observed:** When I tested the scanner at the UWA lab, it captured my fingerprint image and immediately compared it to the database, granting access in about 1 second if the match was successful.

### 2. RFID Card Reader
- **Where found:** UWA student keycard doors, office building access points
- **How it works:** My student keycard contains an embedded RFID chip that transmits a unique ID code when brought near the reader, and the door's control system checks this ID against an access list to determine if entry is allowed.
- **How the technology functions:** The RFID reader sends a radio frequency signal that powers the chip inside the card, the chip broadcasts its ID back to the reader, and then the system verifies if that ID has access rights for that specific door.
- **Security considerations:** Basic RFID is vulnerable to cloning and eavesdropping, but newer cards use encryption to protect the signal, so meaning that a simple card like mine can be more secure than older technology if proper encryption is implemented.
- **Real-world issue:** I noticed that some older RFID readers on campus don't have encryption, so theoretically someone with an RFID reader could capture my card's ID and clone it.

### 3. Keypad/PIN Lock
- **Where found:** Home security system, office building elevator access, parking garage entry
- **How it works:** Users must enter a correct numerical code on the keypad, and the electronic lock compares the entered code against stored codes in its memory, granting access only when the code matches.
- **Advantages:** Simple to use and maintain, making sure that anyone without physical contact can enter if they know the code, and codes are quick to change without replacing hardware.
- **Weaknesses:** Codes can be guessed, forgotten, or shared easily between people, and someone watching over your shoulder (shoulder surfing) can steal your code, so meaning that PIN locks are less secure than biometrics but still useful for lower-security areas.
- **What I tested:** I observed that PIN locks take about 2-3 seconds to verify the code once entered, and there is usually a buzzer sound when the code is accepted.

### 4. Smart Card Reader (Contact/Contactless)
- **Where found:** Office building secured entry, some UWA facilities
- **How it works:** A smart card contains a microprocessor or embedded circuit that communicates with the reader through direct contact or radio frequency, allowing the card to perform cryptographic operations to verify the cardholder's identity.
- **Advanced authentication:** Unlike simple ID cards, smart cards can perform mutual authentication where the reader and card verify each other using certificates and encrypted handshakes, making sure that both parties are legitimate.
- **Security advantage:** Smart cards can store encryption keys securely and perform cryptographic operations on the card itself, meaning that your private key never leaves the card, so this is very secure compared to basic magnetic strips or simple RFID.
- **What makes it different:** I observed that smart card readers take slightly longer to authenticate (2-4 seconds) because they perform cryptographic verification, but this extra security is worth the delay.

### 5. Facial Recognition Camera
- **Where found:** Office building entrance, high-security research facilities, some UWA buildings
- **How it works:** A high-resolution camera captures a photo of the person's face, then compares it against a database of enrolled faces using facial recognition algorithms like facial feature mapping or deep learning neural networks.
- **Why it's becoming popular:** Facial recognition is very convenient because users don't need to carry cards or remember codes, and it's hard to fool because capturing a photo isn't as simple as cloning a card, so meaning that it's a modern and secure access control method.
- **Privacy concerns:** I noticed that facial recognition raises privacy concerns because the system records and stores facial data, and this data could potentially be misused or stolen, making some people uncomfortable using these systems.
- **Accuracy I observed:** The facial recognition system I tested at a UWA entrance had about a 2-3 second delay for processing and occasionally had false rejections on the first try, requiring a second attempt.

## Evidence
- a11-fingerprint-scanner-note.png - Fingerprint scanner observation note
- a11-rfid-reader-note.png - RFID keycard reader observation note
- a11-keypad-lock-note.png - Keypad/PIN lock observation note
- a11-smart-card-reader-note.png - Smart card reader observation note
- a11-facial-recognition-note.png - Facial recognition camera observation note
- a11-access-control-devices.png - Combined access control devices evidence sheet
