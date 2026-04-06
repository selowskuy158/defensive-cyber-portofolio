# A27 - Research and Implement a System Vulnerability

**Date:** 3 April, 2026

## Summary
This activity explores the concept of SQL injection, which is one of the most common and well known web application vulnerabilities. I researched how SQL injection works and then tested it on a controlled local environment using DVWA (Damn Vulnerable Web Application) that I set up on my own computer. This was all done in a safe and legal environment, meaning that no real systems or websites were attacked or harmed during this activity.

## What is SQL Injection
SQL injection is a type of cyberattack where an attacker inserts malicious SQL code into an input field on a web application, such as a login form or a search box. The way it works is that if the web application does not properly sanitize or filter user input, the attacker can manipulate the SQL query that the application sends to the database. This can allow the attacker to bypass authentication, access sensitive data, modify or delete records, and even take control of the entire database server. SQL injection is listed as one of the top vulnerabilities in the OWASP Top 10 and has been responsible for many major data breaches around the world.

## Implementation on DVWA
I set up DVWA locally on my laptop using XAMPP to run the Apache server and MySQL database. DVWA is a PHP/MySQL web application that is intentionally made vulnerable for people to practice and learn about web security in a safe environment.

### Testing SQL Injection on the Login Form
On the DVWA login page, I tested a basic SQL injection payload by entering the following into the username field:

`admin' OR '1'='1`

And for the password I just entered anything random. The way this works is that the SQL query behind the login form normally looks something like: SELECT * FROM users WHERE username='admin' AND password='password'. But by injecting the OR '1'='1' part, the query becomes always true, meaning that the database returns a valid result and the application lets me in without needing the correct password. I was able to successfully log in as the admin user without knowing the actual password, which shows how dangerous SQL injection can be if the application does not properly handle user input.

### Testing on the Search Field
I also tested SQL injection on the DVWA search functionality by entering a UNION based payload to extract data from other database tables. By using the payload `1' UNION SELECT user, password FROM users#`, I was able to retrieve the usernames and password hashes of all users stored in the database. This shows that SQL injection can be used not just to bypass login but also to steal sensitive data from the entire database.

## Prevention
The main way to prevent SQL injection is by using parameterized queries or prepared statements, which means that the application treats user input as data only and not as part of the SQL command. Other prevention methods include input validation and sanitization, using ORM (Object Relational Mapping) frameworks that automatically handle query building, and applying the principle of least privilege to database accounts so that even if an attacker gets in, they have limited access to the database.
