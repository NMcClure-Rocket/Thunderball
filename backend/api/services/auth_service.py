"""
Auth service – user lookup and credential validation.

Placeholder user list until Db2 adapter is ready.
"""

# ── Placeholder user data ──────────────────────────────────────
_users = [
    {"first_name": "John", "last_name": "Doe", "user": "jdoe@a.com", "pass": "mypassword"},
    {"first_name": "Admin", "last_name": "User", "user": "admin", "pass": "admin123"},
    {"first_name": "Admin", "last_name": "User", "user": "a", "pass": "a"}, # FOR TESTING
]


def authenticate(user: str, password: str) -> bool:
    """Return True if credentials match a known user."""
    return any(
        u["user"] == user and u["pass"] == password
        for u in _users
    )


def create_user(first_name: str, last_name: str, user: str, password: str) -> bool:
    """Add a new user. Returns False if username already exists."""
    if any(u["user"] == user for u in _users):
        return False
    _users.append({
        "first_name": first_name,
        "last_name": last_name,
        "user": user,
        "pass": password,
    })
    return True
