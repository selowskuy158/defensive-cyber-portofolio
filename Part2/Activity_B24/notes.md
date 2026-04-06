# B24 - Design and Implement Access Control of Your Choice

**Date:** 16 April, 2026

## Summary
This activity involves designing and implementing an access control system. I created a simple Role-Based Access Control (RBAC) system using Python and Flask that demonstrates how different users can have different levels of access to resources based on their assigned roles. This is a fundamental concept in cybersecurity and is used in almost every organisation to control who can access what.

## Implementation Details

### What is Role-Based Access Control (RBAC)
RBAC is a method of restricting access to resources based on the roles assigned to individual users. Instead of assigning permissions directly to each user, permissions are grouped into roles like admin, editor, and viewer, and then users are assigned to these roles. This makes it much easier to manage permissions especially in large organisations where there are many users and resources.

### The System I Built
I built a simple web application using Python Flask that has three different user roles: Admin, Editor, and Viewer. Each role has different permissions. The Admin can view, create, edit, and delete content and also manage user accounts. The Editor can view, create, and edit content but cannot delete or manage users. The Viewer can only view content and cannot make any changes. The application uses Flask session management to track who is logged in and their role, and each route checks the user role before allowing access to the requested action.

### How It Works
When a user logs in, the application checks their credentials against a database and retrieves their assigned role. Each protected page and function has a role check decorator that verifies whether the current user role has sufficient permissions to perform the action. If a user tries to access a function they do not have permission for, they receive an "Access Denied" message. I also implemented a logging system that records all access attempts including denied ones, which is important for security auditing and monitoring.

### Testing
I tested the system by creating three test accounts, one for each role, and verifying that each account could only access the functions allowed by their role. The admin account could perform all actions, the editor could create and edit but not delete, and the viewer could only read content. All unauthorized access attempts were correctly blocked and logged. The code was uploaded to my GitHub repository as evidence.
