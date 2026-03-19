"""
Auth service – user lookup and credential validation.

Placeholder user list until Db2 adapter is ready.
"""

# ── Placeholder user data ──────────────────────────────────────
_users = [
    {"first_name": "John", "last_name": "Doe", "email": "jdoe@a.com", "pass": "mypassword"},
    {"first_name": "Admin", "last_name": "User", "email": "admin", "pass": "admin123"},
]


def authenticate(email: str, password: str) -> bool:
    """Return True if credentials match a known user."""
    return any(
        u["email"] == email and u["pass"] == password
        for u in _users
    )


def create_user(first_name: str, last_name: str, email: str, password: str) -> bool:
    """Add a new user. Returns False if email already exists."""
    if any(u["email"] == email for u in _users):
        return False
    _users.append({
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "pass": password,
    })
    return True
