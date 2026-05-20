"""Smoke test for the RBAC demo. Verifies each role's permissions.

Run:  pip install flask werkzeug && python test_rbac.py
"""
from app import app


def login(client, username, password):
    return client.post("/login", data={"username": username, "password": password},
                       follow_redirects=True)


def test_matrix():
    cases = [
        # (role, path, method, expected_status)
        ("viewer", "/content",           "GET",  200),
        ("viewer", "/content/new",       "POST", 403),
        ("viewer", "/users",             "GET",  403),
        ("editor", "/content",           "GET",  200),
        ("editor", "/content/new",       "POST", 302),  # redirect on success
        ("editor", "/users",             "GET",  403),
        ("admin",  "/content",           "GET",  200),
        ("admin",  "/content/new",       "POST", 302),
        ("admin",  "/users",             "GET",  200),
    ]
    fails = 0
    for role, path, method, expected in cases:
        client = app.test_client()
        login(client, role, role)
        if method == "GET":
            r = client.get(path)
        else:
            r = client.post(path, data={"title": "t", "body": "b"})
        ok = r.status_code == expected
        marker = "OK " if ok else "FAIL"
        print(f"  {marker}  role={role:<6} {method:<4} {path:<20} got={r.status_code} want={expected}")
        if not ok:
            fails += 1
    print(f"\n{len(cases) - fails}/{len(cases)} passed")
    return fails == 0


if __name__ == "__main__":
    print("Running RBAC permission matrix test...")
    test_matrix()
