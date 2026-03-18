"""
Auth service – user lookup and credential validation.
"""

from db.connector import conn
from db.dao.customer_dao import CustomerDAO

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
