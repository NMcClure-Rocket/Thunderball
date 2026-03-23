"""Unit tests for backend.config.db_credentials_manager.DB_credentials."""
import json
from pathlib import Path

import pytest

from backend.config.db_credentials_manager import DB_credentials

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_REQUIRED = {
    "DATABASE": "TESTDB",
    "HOSTNAME": "localhost",
    "PORT": "50000",
    "PROTOCOL": "TCPIP",
    "AUTHENTICATION": "SERVER",
    "UID": "user1",
    "PWD": "pass1",
}


def _write_creds(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "Db_creds"
    p.write_text(content, encoding="utf-8")
    return p


# ===========================================================================
# load() – JSON path
# ===========================================================================

class TestLoadJSON:
    def test_valid_json_returns_uppercased_dict(self, tmp_path):
        path = _write_creds(tmp_path, json.dumps(_REQUIRED))
        creds = DB_credentials(file_path=path)
        result = creds.load()
        assert result["DATABASE"] == "TESTDB"
        assert result["UID"] == "user1"

    def test_lowercase_keys_are_uppercased(self, tmp_path):
        lower = {k.lower(): v for k, v in _REQUIRED.items()}
        path = _write_creds(tmp_path, json.dumps(lower))
        creds = DB_credentials(file_path=path)
        result = creds.load()
        assert "DATABASE" in result

    def test_non_dict_json_raises_value_error(self, tmp_path):
        path = _write_creds(tmp_path, json.dumps(["not", "a", "dict"]))
        creds = DB_credentials(file_path=path)
        with pytest.raises(ValueError, match="JSON object"):
            creds.load()

    def test_empty_file_raises_value_error(self, tmp_path):
        path = _write_creds(tmp_path, "   ")
        creds = DB_credentials(file_path=path)
        with pytest.raises(ValueError, match="[Ee]mpty|empty"):
            creds.load()

    def test_missing_keys_raises_value_error(self, tmp_path):
        partial = {"DATABASE": "DB", "HOSTNAME": "host"}
        path = _write_creds(tmp_path, json.dumps(partial))
        creds = DB_credentials(file_path=path)
        with pytest.raises(ValueError, match="Missing DB credential keys"):
            creds.load()

    def test_stores_creds_after_load(self, tmp_path):
        path = _write_creds(tmp_path, json.dumps(_REQUIRED))
        creds = DB_credentials(file_path=path)
        creds.load()
        assert creds._creds["DATABASE"] == "TESTDB"


# ===========================================================================
# load() – KEY=VALUE fallback path
# ===========================================================================

class TestLoadKeyValue:
    def _make_kv(self, data: dict) -> str:
        return "\n".join(f"{k}={v}" for k, v in data.items())

    def test_valid_keyvalue_file_loads_correctly(self, tmp_path):
        path = _write_creds(tmp_path, self._make_kv(_REQUIRED))
        creds = DB_credentials(file_path=path)
        result = creds.load()
        assert result["DATABASE"] == "TESTDB"
        assert result["PWD"] == "pass1"

    def test_comment_lines_are_ignored(self, tmp_path):
        content = "# this is a comment\n" + self._make_kv(_REQUIRED)
        path = _write_creds(tmp_path, content)
        creds = DB_credentials(file_path=path)
        result = creds.load()
        assert result["DATABASE"] == "TESTDB"

    def test_blank_lines_are_ignored(self, tmp_path):
        content = "\n\n" + self._make_kv(_REQUIRED) + "\n\n"
        path = _write_creds(tmp_path, content)
        creds = DB_credentials(file_path=path)
        result = creds.load()
        assert result["DATABASE"] == "TESTDB"

    def test_lines_without_equals_are_ignored(self, tmp_path):
        content = "BADLINE\n" + self._make_kv(_REQUIRED)
        path = _write_creds(tmp_path, content)
        creds = DB_credentials(file_path=path)
        result = creds.load()
        assert result["DATABASE"] == "TESTDB"

    def test_missing_keys_in_keyvalue_raises(self, tmp_path):
        partial = {"DATABASE": "DB", "HOSTNAME": "h"}
        path = _write_creds(tmp_path, self._make_kv(partial))
        creds = DB_credentials(file_path=path)
        with pytest.raises(ValueError, match="Missing DB credential keys"):
            creds.load()


# ===========================================================================
# get() – lazy loading
# ===========================================================================

class TestGet:
    def test_get_triggers_lazy_load(self, tmp_path):
        path = _write_creds(tmp_path, json.dumps(_REQUIRED))
        creds = DB_credentials(file_path=path)
        # _creds is empty; get() should auto-load
        assert creds.get("DATABASE") == "TESTDB"

    def test_get_returns_none_for_missing_key(self, tmp_path):
        path = _write_creds(tmp_path, json.dumps(_REQUIRED))
        creds = DB_credentials(file_path=path)
        assert creds.get("NONEXISTENT") is None

    def test_get_returns_default_for_missing_key(self, tmp_path):
        path = _write_creds(tmp_path, json.dumps(_REQUIRED))
        creds = DB_credentials(file_path=path)
        assert creds.get("NONEXISTENT", "fallback") == "fallback"

    def test_get_is_case_insensitive(self, tmp_path):
        path = _write_creds(tmp_path, json.dumps(_REQUIRED))
        creds = DB_credentials(file_path=path)
        assert creds.get("database") == "TESTDB"

    def test_get_does_not_reload_when_already_loaded(self, tmp_path):
        path = _write_creds(tmp_path, json.dumps(_REQUIRED))
        creds = DB_credentials(file_path=path)
        creds.load()
        # Delete the file; get() should use cached data without reloading
        path.unlink()
        assert creds.get("DATABASE") == "TESTDB"


# ===========================================================================
# as_connection_string()
# ===========================================================================

class TestAsConnectionString:
    def test_format_contains_all_required_parts(self, tmp_path):
        path = _write_creds(tmp_path, json.dumps(_REQUIRED))
        creds = DB_credentials(file_path=path)
        creds.load()
        conn_str = creds.as_connection_string()
        assert "DATABASE=TESTDB;" in conn_str
        assert "HOSTNAME=localhost;" in conn_str
        assert "PORT=50000;" in conn_str
        assert "PROTOCOL=TCPIP;" in conn_str
        assert "AUTHENTICATION=SERVER;" in conn_str
        assert "UID=user1;" in conn_str
        assert "PWD=pass1;" in conn_str

    def test_connection_string_is_single_string(self, tmp_path):
        path = _write_creds(tmp_path, json.dumps(_REQUIRED))
        creds = DB_credentials(file_path=path)
        creds.load()
        conn_str = creds.as_connection_string()
        assert isinstance(conn_str, str)
