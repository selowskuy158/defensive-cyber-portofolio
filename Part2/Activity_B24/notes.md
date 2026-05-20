# B24 — Design and Implement Access Control: Role-Based Access Control (RBAC)

## What I built
A working Flask web application implementing Role-Based Access Control
with three roles (`admin`, `editor`, `viewer`), decorator-based
permission gating, and a full permission-matrix test suite that
verifies each role can do exactly what it's allowed to and nothing
more.

**Files:**
- [`app.py`](app.py) — the web application (~150 lines).
- [`test_rbac.py`](test_rbac.py) — automated permission-matrix test.
- [`evidence_test_output.txt`](evidence_test_output.txt) — output
  showing 9/9 tests pass.

## Design

### Roles and permissions
```
viewer  : {content:read}
editor  : {content:read, content:create, content:update}
admin   : {content:read, content:create, content:update, content:delete, users:manage}
```

The role-permission mapping is the single source of truth. The
permissions themselves are namespaced strings (`resource:action`),
which scales cleanly to more resources without changing the gating
mechanism.

### Permission-gating decorator
```python
@require("content:update")
def content_edit(item_id):
    ...
```
Each protected route declares the permission it needs. The decorator
checks the current session's role against the permission map, and on
denial returns a 403 plus logs the attempt. This keeps authorisation
logic out of route bodies.

### Audit log
Every permission decision (allow + deny) is appended to `access.log`,
keyed by username, permission, and path. This is the foundation of
useful security auditing — denied attempts are often more interesting
than allowed ones because they indicate either confused users or
probing attackers.

### Authentication
Sessions are Flask's signed cookie sessions. Passwords are hashed
with Werkzeug's `generate_password_hash` (PBKDF2-SHA256). Login is a
standard POST handler; on failure the auth attempt is logged.

## Verification
Running `python test_rbac.py` exercises 9 (role × action) cells and
verifies the expected HTTP status:
```
OK   role=viewer GET  /content       got=200 want=200
OK   role=viewer POST /content/new   got=403 want=403
OK   role=viewer GET  /users         got=403 want=403
OK   role=editor GET  /content       got=200 want=200
OK   role=editor POST /content/new   got=302 want=302
OK   role=editor GET  /users         got=403 want=403
OK   role=admin  GET  /content       got=200 want=200
OK   role=admin  POST /content/new   got=302 want=302
OK   role=admin  GET  /users         got=200 want=200

9/9 passed
```

## Reflection
The most useful design decision was making `ROLE_PERMISSIONS` a
mapping of role → permission **set**, rather than checking roles
directly in route handlers. This made the permission-matrix test
trivial to write, and it means adding a new permission requires
updating exactly one data structure rather than auditing every route.

The other lesson was that *denied* access attempts are the most
valuable thing in the audit log — they're where the security signal
lives. Allowed access is just normal usage.
