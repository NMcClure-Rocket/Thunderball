"""Entity class representing user credentials for role-based access control."""


class Credentials:
    """
    Represents the credentials of an authenticated user for role-based access control.
    """

    def __init__(self, role: str = "", user_id: str = ""):
        """
        Args:
            role (str): The role of the user (e.g. "admin", "read-only")
            user_id (str): The unique identifier of the user
        """
        self.role = role
        self.user_id = user_id

    def __repr__(self) -> str:
        return f"Credentials(role={self.role!r}, user_id={self.user_id!r})"
