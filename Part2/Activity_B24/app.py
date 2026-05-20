"""
B24 - Role-Based Access Control (RBAC) demo using Flask.

Three roles: admin, editor, viewer.
- viewer  : read content
- editor  : read + create + update content
- admin   : everything + manage users

Every access attempt (allowed and denied) is appended to access.log.

Run:
    pip install flask werkzeug
    python app.py
    # then visit http://127.0.0.1:5000

Demo accounts (password = role name):
    admin / admin
    editor / editor
    viewer / viewer
"""
from __future__ import annotations

import functools
import logging
from datetime import datetime

from flask import Flask, redirect, render_template_string, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = "demo-rbac-secret-do-not-use-in-production"

# --- access log ---------------------------------------------------------------
log = logging.getLogger("rbac.access")
log.setLevel(logging.INFO)
fh = logging.FileHandler("access.log")
fh.setFormatter(logging.Formatter("%(asctime)s | %(message)s"))
log.addHandler(fh)


# --- user + role model --------------------------------------------------------
ROLE_PERMISSIONS = {
    "viewer": {"content:read"},
    "editor": {"content:read", "content:create", "content:update"},
    "admin":  {"content:read", "content:create", "content:update", "content:delete", "users:manage"},
}

USERS = {
    "admin":  {"password_hash": generate_password_hash("admin"),  "role": "admin"},
    "editor": {"password_hash": generate_password_hash("editor"), "role": "editor"},
    "viewer": {"password_hash": generate_password_hash("viewer"), "role": "viewer"},
}

CONTENT: list[dict] = [
    {"id": 1, "title": "Welcome", "body": "First post on the RBAC demo."},
]


def current_user() -> dict | None:
    username = session.get("username")
    return USERS.get(username) if username else None


def has_permission(perm: str) -> bool:
    user = current_user()
    if not user:
        return False
    return perm in ROLE_PERMISSIONS[user["role"]]


def require(perm: str):
    """Decorator: gate a route on a permission. Logs allow/deny."""
    def wrap(view):
        @functools.wraps(view)
        def inner(*args, **kwargs):
            username = session.get("username", "anonymous")
            if not has_permission(perm):
                log.info(f"DENY user={username} perm={perm} path={request.path}")
                return render_template_string(TEMPLATE_DENIED, perm=perm), 403
            log.info(f"ALLOW user={username} perm={perm} path={request.path}")
            return view(*args, **kwargs)
        return inner
    return wrap


# --- templates ----------------------------------------------------------------
BASE = """
<!doctype html><meta charset="utf-8">
<title>RBAC Demo</title>
<style>body{font-family:system-ui;max-width:680px;margin:40px auto;padding:0 16px}
nav a{margin-right:12px}.role{color:#999}.muted{color:#777;font-size:0.9em}
form input,form button{padding:6px;margin:4px 0;display:block}
.ok{color:#0a7d27}.bad{color:#b00}</style>
<nav>
  <a href="/">home</a>
  {% if user %}
    <a href="/content">content</a>
    {% if 'users:manage' in perms %}<a href="/users">users</a>{% endif %}
    <a href="/logout">logout</a>
    <span class="role">[{{user.role}}]</span>
  {% else %}
    <a href="/login">login</a>
  {% endif %}
</nav><hr>
"""

TEMPLATE_HOME = BASE + """
<h1>RBAC Demo</h1>
<p>Three demo accounts. Passwords match usernames: <code>admin</code>, <code>editor</code>, <code>viewer</code>.</p>
<p class="muted">Try logging in as each role and see which actions you can perform.</p>
"""

TEMPLATE_LOGIN = BASE + """
<h2>Login</h2>
{% if error %}<p class="bad">{{error}}</p>{% endif %}
<form method="post">
  <input name="username" placeholder="username" required>
  <input name="password" placeholder="password" type="password" required>
  <button>log in</button>
</form>
"""

TEMPLATE_CONTENT = BASE + """
<h2>Content ({{items|length}} items)</h2>
<ul>{% for item in items %}
  <li><b>{{item.title}}</b> &mdash; {{item.body}}
    {% if 'content:update' in perms %} <a href="/content/{{item.id}}/edit">edit</a>{% endif %}
    {% if 'content:delete' in perms %} <a href="/content/{{item.id}}/delete">delete</a>{% endif %}
  </li>
{% endfor %}</ul>
{% if 'content:create' in perms %}
  <h3>New post</h3>
  <form method="post" action="/content/new">
    <input name="title" placeholder="title" required>
    <input name="body" placeholder="body" required>
    <button>create</button>
  </form>
{% endif %}
"""

TEMPLATE_USERS = BASE + """
<h2>User Management (admin only)</h2>
<ul>{% for u,info in users.items() %}
  <li>{{u}} &mdash; <span class="role">{{info.role}}</span></li>
{% endfor %}</ul>
"""

TEMPLATE_DENIED = BASE + """
<h2 class="bad">Access Denied</h2>
<p>Your role does not include the required permission: <code>{{perm}}</code></p>
<p>This attempt has been logged to <code>access.log</code>.</p>
"""


# --- routes -------------------------------------------------------------------
@app.context_processor
def inject_user():
    user = current_user()
    return {
        "user": user,
        "perms": ROLE_PERMISSIONS.get(user["role"], set()) if user else set(),
    }


@app.get("/")
def home():
    return render_template_string(TEMPLATE_HOME)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        info = USERS.get(u)
        if info and check_password_hash(info["password_hash"], p):
            session["username"] = u
            log.info(f"LOGIN_OK user={u}")
            return redirect(url_for("home"))
        log.info(f"LOGIN_FAIL user={u}")
        return render_template_string(TEMPLATE_LOGIN, error="invalid credentials")
    return render_template_string(TEMPLATE_LOGIN, error=None)


@app.get("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))


@app.get("/content")
@require("content:read")
def content_list():
    return render_template_string(TEMPLATE_CONTENT, items=CONTENT)


@app.post("/content/new")
@require("content:create")
def content_new():
    CONTENT.append({"id": max((c["id"] for c in CONTENT), default=0) + 1,
                    "title": request.form["title"], "body": request.form["body"]})
    return redirect(url_for("content_list"))


@app.route("/content/<int:item_id>/edit", methods=["GET", "POST"])
@require("content:update")
def content_edit(item_id):
    item = next((c for c in CONTENT if c["id"] == item_id), None)
    if not item:
        return "not found", 404
    if request.method == "POST":
        item["title"] = request.form["title"]
        item["body"] = request.form["body"]
        return redirect(url_for("content_list"))
    return render_template_string(BASE + """
      <h2>Edit</h2><form method="post">
        <input name="title" value="{{item.title}}" required>
        <input name="body" value="{{item.body}}" required>
        <button>save</button>
      </form>""", item=item)


@app.get("/content/<int:item_id>/delete")
@require("content:delete")
def content_delete(item_id):
    CONTENT[:] = [c for c in CONTENT if c["id"] != item_id]
    return redirect(url_for("content_list"))


@app.get("/users")
@require("users:manage")
def users():
    return render_template_string(TEMPLATE_USERS, users=USERS)


if __name__ == "__main__":
    print("RBAC demo running on http://127.0.0.1:5000")
    print("Try logging in as admin/admin, editor/editor, viewer/viewer")
    app.run(debug=False, port=5000)
