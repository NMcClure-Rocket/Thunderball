"""JSON-backed DB2 credentials manager."""

from pathlib import Path
import json


class DB_credentials:
    """Loads and validates DB2 credentials from backend/config/Db_creds."""

    REQUIRED_KEYS = (
        "DATABASE",
        "HOSTNAME",
        "PORT",
        "PROTOCOL",
        "AUTHENTICATION",
        "UID",
        "PWD",
    )

    def __init__(self, file_path: Path | None = None):
        project_root = Path(__file__).resolve().parents[2]
        self.file_path = file_path or (project_root / "backend" / "config" / "Db_creds")
        self._creds: dict[str, str] = {}

    def load(self) -> dict[str, str]:
        """Read credentials JSON from disk and validate required keys."""
        raw_text = self.file_path.read_text(encoding="utf-8-sig").strip()
        if not raw_text:
            raise ValueError("Db_creds is empty")

        creds: dict[str, str]
        try:
            payload = json.loads(raw_text)
            if not isinstance(payload, dict):
                raise ValueError("Db_creds must contain a JSON object")
            creds = {str(key).upper(): str(value) for key, value in payload.items()}
        except json.JSONDecodeError:
            # Backward-compatible fallback for KEY=VALUE formatted credentials.
            creds = {}
            for line in raw_text.splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if "=" not in stripped:
                    continue
                key, value = stripped.split("=", 1)
                creds[key.strip().upper()] = value.strip()

        missing = [key for key in self.REQUIRED_KEYS if key not in creds]
        if missing:
            raise ValueError(f"Missing DB credential keys: {', '.join(missing)}")

        self._creds = creds
        return self._creds

    def get(self, key: str, default: str | None = None) -> str | None:
        """Get one credential value by key."""
        if not self._creds:
            self.load()
        return self._creds.get(key.upper(), default)

    def as_connection_string(self) -> str:
        """Build the DB2 connection string expected by ibm_db.connect."""
        if not self._creds:
            self.load()

        return (
            f"DATABASE={self._creds['DATABASE']};"
            f"HOSTNAME={self._creds['HOSTNAME']};"
            f"PORT={self._creds['PORT']};"
            f"PROTOCOL={self._creds['PROTOCOL']};"
            f"AUTHENTICATION={self._creds['AUTHENTICATION']};"
            f"UID={self._creds['UID']};"
            f"PWD={self._creds['PWD']};"
        )
