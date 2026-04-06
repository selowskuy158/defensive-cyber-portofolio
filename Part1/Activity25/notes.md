# A25 - Design and Implement a Privacy-Preserving Technique for an Appropriate Application

**Date:** 3 April, 2026

## Summary
This activity explores how privacy can be protected in data storage through the use of cryptographic techniques, meaning that I designed and implemented a practical application that anonymizes personal information before storing it. I created a Python script that demonstrates the concept of hashing as a privacy-preserving technique, which is very important for protecting user data in any application that collects personal information.

## Privacy Problem Addressed

**The scenario:** Many applications and organizations need to store personal information like email addresses, user IDs, or identifiers in databases or files. However, storing this information in plain text creates a privacy risk because if the database is breached or accessed by unauthorized people, all that personal information is immediately exposed, so meaning that attackers can use this data for fraud, spam, identity theft, or other malicious purposes.

**The solution:** Hashing is a one-way cryptographic function that converts data into a fixed-size unique string called a hash. The way it works is that you cannot reverse a hash to get back the original data - if the original value is "christopher@example.com", hashing it produces something like "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" (using SHA-256). This means that if someone steals the hashed data, they cannot easily determine what the original email address was.

## Implementation Details

**What I built:** I created a Python script that takes a CSV file with personal information (email addresses), hashes each email using the SHA-256 algorithm, and outputs the hashed values to a new CSV file. The script uses Python's built-in `hashlib` library, which provides cryptographic hash functions.

**Key code concept:** The basic approach is:
```
For each email address in the input file:
  1. Take the email address as plain text
  2. Apply SHA-256 hashing function
  3. Write the hashed value to the output file
  4. Original plain text email is never stored
```

**Why SHA-256:** I chose SHA-256 because it's a widely accepted cryptographic hash function that produces a 256-bit hash, making it very secure against attacks. The output is a hexadecimal string that looks like random characters but is deterministic, meaning that hashing the same email address always produces the same hash.

## Technical Implementation

**Script structure:** The script performs these steps:
1. Opens the input CSV file containing email addresses
2. Creates an output CSV file for storing hashed values
3. Iterates through each row of the input file
4. Applies SHA-256 hashing to each email address
5. Writes the hash to the output file
6. Closes both files and reports success

**Testing the script:** I tested the script with several email addresses to make sure it worked correctly. I noticed that:
- The same email address always produces the same hash (deterministic behavior)
- Different email addresses produce completely different hashes (no patterns visible)
- The hashed output is safe to store because it cannot be reversed
- The original information is never written to the output file

## Privacy Preservation Explained

**How it protects privacy:** This technique preserves privacy by ensuring that the stored data (hashes) contains no personally identifiable information in readable form. If someone accesses the CSV file with hashes, they cannot tell what the original email addresses were without an enormous amount of computational effort.

**Still useful for applications:** Even though the data is hashed and cannot be read, it's still useful for many applications. For example:
- You can identify duplicate entries (same hash = same original email)
- You can verify if a specific email exists in the database (hash the input and compare)
- You can send targeted messages if you have a list of emails to target (hash the target emails and compare with your hashed list)
- You cannot accidentally expose user email addresses if your file is stolen

**Limitations:** I noticed that hashing has limitations - it doesn't work perfectly for all use cases. If an attacker knows that your data probably contains common email addresses or passwords, they can create a "rainbow table" (a large list of pre-computed hashes of common values) and compare against your hashed data. However, this still provides much better protection than storing plain text, especially combined with other security measures like salting.

## Publishing to GitHub

**What I did:** I uploaded the Python script to GitHub, making sure to include documentation explaining what the script does, how to use it, and what privacy protections it provides. The repository includes:
- The main Python script file
- A README.md explaining the project
- Example input and output CSV files showing the before and after
- Comments in the code explaining what each section does

**Public access:** By publishing this on GitHub, I made the code available for others to use and learn from. This demonstrates that privacy-preserving techniques can be implemented by students and shared with the community, not just by large organizations.

## Real-World Applications

**Where this is used:** Hashing for privacy is used in many real-world applications:
- Password storage (websites store hashes of passwords, not the passwords themselves)
- Email verification systems (hash the email to create unique verification links)
- Analytics and tracking (hash user identifiers so you can track behavior without storing identifiable information)
- Duplicate detection in large databases

## Key Learnings

This activity helped me understand that privacy is not something that happens by accident - it requires deliberate design and implementation of techniques like hashing. I also learned that even small scripts can demonstrate important security concepts, and that code can be a very powerful way to communicate ideas about privacy and security.

**Important insight:** The way it works is that privacy is a shared responsibility - application developers need to use privacy-preserving techniques like hashing when storing data, but users also need to understand what happens to their information and demand that organizations protect it.

## Conclusion

Designing and implementing this privacy-preserving hashing script really helped me understand the gap between understanding a concept theoretically and actually building something that works. The exercise showed me that implementing proper privacy protection requires careful thought about what data you collect, how you store it, and what protections you apply. This is very important knowledge for any cybersecurity or software development career, because privacy breaches increasingly result in legal penalties and loss of customer trust.
