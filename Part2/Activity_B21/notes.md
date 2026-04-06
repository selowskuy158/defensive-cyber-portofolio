# B21 - Design and Implement a Cybersecurity Learning Activity

**Date:** 15 April, 2026

## Summary
This activity involves designing and implementing a cybersecurity learning activity that can be used to educate others about cybersecurity concepts. I designed a phishing email identification quiz using a simple HTML/JavaScript web page that presents users with sample emails and asks them to identify which ones are phishing attempts and which ones are legitimate.

## Implementation Details

### The Learning Activity: Phishing Email Quiz
I created an interactive web-based quiz that shows users 10 different email screenshots and descriptions, and they must determine whether each email is a phishing attempt or a legitimate message. After each answer, the quiz provides an explanation of why the email is or is not a phishing attempt, highlighting the specific red flags or legitimate features that should be looked for.

### Design Decisions
I chose phishing identification as the topic because it is one of the most practical cybersecurity skills that everyone needs to have, regardless of their technical background. The quiz includes various types of phishing attempts including emails pretending to be from banks, delivery services, tech companies, and government agencies. I also included some legitimate emails that have features that might look suspicious to help users avoid being overly paranoid and blocking real emails. Each question includes detailed explanations that teach users what to look for, such as checking the sender email domain, looking for urgency language, checking for generic greetings, and hovering over links to see the actual URL.

### Technical Implementation
The quiz was built using HTML, CSS, and JavaScript as a single-page application that can be opened in any browser without needing a server. I used JavaScript to handle the quiz logic, score tracking, and feedback display. The quiz stores the score in memory and shows a final result screen at the end with the total score and recommendations for improvement based on which questions the user got wrong.

### Testing
I tested the quiz with several friends at UWA and collected feedback on the questions and explanations. Most users found the quiz helpful and said they learned new things about identifying phishing emails that they did not know before. The average score was around 7 out of 10, which shows that even university students can be fooled by sophisticated phishing attempts. The quiz and its source code were uploaded to my GitHub repository as part of the portfolio evidence.
