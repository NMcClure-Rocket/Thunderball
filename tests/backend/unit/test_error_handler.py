"""
Unit tests for backend/utilities/error_handler.py.

ibm_db and backend.utilities.logger are mocked at module level (same pattern
as test_dao.py) so these tests run without a DB2 installation or log config.
"""
# pylint: disable=missing-class-docstring,missing-function-docstring
# pylint: disable=redefined-outer-name,wrong-import-position,protected-access

import sys
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Module-level mocks — must be in place before error_handler is imported.
# ---------------------------------------------------------------------------

for _m in ("ibm_db", "ibm_db_dbi"):
    sys.modules.setdefault(_m, MagicMock())

_mock_logger = MagicMock()
sys.modules.setdefault(
    "backend.utilities.logger",
    MagicMock(LoggerFactory=MagicMock(get_general_logger=MagicMock(return_value=_mock_logger))),
)

# ---------------------------------------------------------------------------
# Import the real error_handler after mocks are set up.
# ---------------------------------------------------------------------------

import pytest  # noqa: E402

from backend.utilities.error_handler import (  # noqa: E402
    ResponseCode,
    ErrorSeverity,
    DB2ErrorCode,
    DB2ErrorHandler,
    OperationResult,
    success_response,
    post_success_response,
    update_success_response,
    delete_success_response,
    not_found_error,
    malformed_content_error,
    permission_error,
)
import backend.utilities.error_handler as _eh_module  # noqa: E402


# ===========================================================================
# ResponseCode – construction & is_success
# ===========================================================================

class TestResponseCodeInit:
    def test_none_error_tag_means_success(self):
        rc = ResponseCode(error_tag=None)
        assert rc.is_success is True

    def test_set_error_tag_means_failure(self):
        rc = ResponseCode(error_tag="SomeError")
        assert rc.is_success is False

    def test_error_tag_stored(self):
        rc = ResponseCode(error_tag="Boom")
        assert rc.error_tag == "Boom"

    def test_data_stored(self):
        rc = ResponseCode(data={"key": "value"})
        assert rc.data == {"key": "value"}

    def test_default_severity_is_error(self):
        rc = ResponseCode(error_tag="X")
        assert rc.severity == ErrorSeverity.ERROR

    def test_custom_severity_stored(self):
        rc = ResponseCode(error_tag="X", severity=ErrorSeverity.CRITICAL)
        assert rc.severity == ErrorSeverity.CRITICAL

    def test_sqlstate_stored(self):
        rc = ResponseCode(sqlstate="23505")
        assert rc.sqlstate == "23505"

    def test_native_error_stored(self):
        rc = ResponseCode(native_error=-104)
        assert rc.native_error == -104

    def test_custom_message_stored(self):
        rc = ResponseCode(message="custom msg")
        assert rc.message == "custom msg"

    def test_default_message_used_when_none(self):
        rc = ResponseCode(error_tag="GeneralSuccess")
        assert rc.message == "Operation completed successfully"

    def test_timestamp_set_automatically(self):
        rc = ResponseCode()
        assert rc.timestamp is not None

    def test_custom_timestamp_stored(self):
        from datetime import datetime as _datetime  # pylint: disable=import-outside-toplevel
        ts = _datetime(2025, 1, 1)
        rc = ResponseCode(timestamp=ts)
        assert rc.timestamp == ts


# ===========================================================================
# ResponseCode – _get_default_message
# ===========================================================================

class TestGetDefaultMessage:
    @pytest.mark.parametrize("tag,expected", [
        ("GeneralSuccess", "Operation completed successfully"),
        ("PostSuccess", "Resource created successfully"),
        ("UpdateSuccess", "Resource updated successfully"),
        ("DeleteSuccess", "Resource deleted successfully"),
        ("ResourceNotFound", "The requested resource was not found"),
        ("MalformedContent", "The request content is malformed or invalid"),
        ("PermissionIncongruency", "User lacks required permissions for this operation"),
    ])
    def test_known_tags_return_expected_messages(self, tag, expected):
        rc = ResponseCode(error_tag=tag)
        assert rc.message == expected

    def test_unknown_tag_returns_error_prefix(self):
        rc = ResponseCode(error_tag="WeirdTag")
        assert rc.message == "Error: WeirdTag"

    def test_none_tag_returns_error_none_message(self):
        rc = ResponseCode(error_tag=None)
        # None tag → success, message lookup returns "Error: None" from fallback
        assert rc.is_success is True


# ===========================================================================
# ResponseCode – to_dict
# ===========================================================================

class TestResponseCodeToDict:
    def test_to_dict_contains_required_keys(self):
        rc = ResponseCode(error_tag="X", data=42)
        d = rc.to_dict()
        for key in ("is_success", "error_tag", "severity", "message",
                    "sqlstate", "native_error", "data", "timestamp"):
            assert key in d

    def test_to_dict_is_success_correct(self):
        assert ResponseCode(error_tag=None).to_dict()["is_success"] is True
        assert ResponseCode(error_tag="E").to_dict()["is_success"] is False

    def test_to_dict_severity_is_string(self):
        rc = ResponseCode(error_tag="E", severity=ErrorSeverity.WARNING)
        assert rc.to_dict()["severity"] == "WARNING"

    def test_to_dict_timestamp_is_string(self):
        rc = ResponseCode()
        assert isinstance(rc.to_dict()["timestamp"], str)

    def test_to_dict_data_preserved(self):
        payload = {"rows": [1, 2, 3]}
        rc = ResponseCode(data=payload)
        assert rc.to_dict()["data"] == payload


# ===========================================================================
# ResponseCode – __repr__
# ===========================================================================

class TestResponseCodeRepr:
    def test_repr_success(self):
        rc = ResponseCode(data="hello")
        r = repr(rc)
        assert "SUCCESS" in r
        assert "hello" in r

    def test_repr_error_contains_tag(self):
        rc = ResponseCode(error_tag="ResourceNotFound")
        r = repr(rc)
        assert "FAILED" in r
        assert "ResourceNotFound" in r


# ===========================================================================
# ResponseCode – log_response
# ===========================================================================

class TestLogResponse:
    mock_log: MagicMock  # declared here to satisfy pylint attribute-defined-outside-init

    @pytest.fixture(autouse=True)
    def patch_logger(self):
        """Replace the module-level logger with a fresh mock for each test."""
        self.mock_log = MagicMock()
        with patch.object(_eh_module, "logger", self.mock_log):
            yield

    def test_success_calls_info(self):
        ResponseCode(error_tag=None).log_response()
        self.mock_log.info.assert_called_once()

    def test_critical_severity_calls_critical(self):
        ResponseCode(error_tag="X", severity=ErrorSeverity.CRITICAL).log_response()
        self.mock_log.critical.assert_called_once()

    def test_error_severity_calls_error(self):
        ResponseCode(error_tag="X", severity=ErrorSeverity.ERROR).log_response()
        self.mock_log.error.assert_called_once()

    def test_warning_severity_calls_warning(self):
        ResponseCode(error_tag="X", severity=ErrorSeverity.WARNING).log_response()
        self.mock_log.warning.assert_called_once()

    def test_info_severity_calls_info(self):
        ResponseCode(error_tag="X", severity=ErrorSeverity.INFO).log_response()
        self.mock_log.info.assert_called_once()

    def test_operation_name_appears_in_log(self):
        ResponseCode(error_tag=None).log_response("MyOperation")
        call_args = self.mock_log.info.call_args[0][0]
        assert "MyOperation" in call_args


# ===========================================================================
# DB2ErrorHandler.parse_exception
# ===========================================================================

class TestParseException:
    @pytest.fixture(autouse=True)
    def patch_logger(self):
        with patch.object(_eh_module, "logger", MagicMock()):
            yield

    @pytest.mark.parametrize("msg,expected_tag", [
        ("connection refused", DB2ErrorCode.CONNECTION_FAILED.value),
        ("syntax error in SQL", DB2ErrorCode.SYNTAX_ERROR.value),
        ("constraint violation occurred", DB2ErrorCode.CONSTRAINT_VIOLATION.value),
        ("duplicate key value", DB2ErrorCode.DUPLICATE_KEY.value),
        ("foreign key violation", DB2ErrorCode.FOREIGN_KEY_VIOLATION.value),
        ("deadlock detected", DB2ErrorCode.DEADLOCK.value),
        ("timeout waiting for lock", DB2ErrorCode.LOCK_TIMEOUT.value),
        ("permission denied for user", DB2ErrorCode.PERMISSION_DENIED.value),
        ("not authorized to access table", DB2ErrorCode.PERMISSION_DENIED.value),
        ("some unrecognised error", DB2ErrorCode.GENERAL_ERROR.value),
    ])
    def test_exception_message_maps_to_correct_tag(self, msg, expected_tag):
        rc = DB2ErrorHandler.parse_exception(Exception(msg))
        assert rc.error_tag == expected_tag

    def test_returns_response_code_instance(self):
        rc = DB2ErrorHandler.parse_exception(RuntimeError("boom"))
        assert isinstance(rc, ResponseCode)

    def test_connection_error_has_critical_severity(self):
        rc = DB2ErrorHandler.parse_exception(Exception("connection failed"))
        assert rc.severity == ErrorSeverity.CRITICAL

    def test_deadlock_has_critical_severity(self):
        rc = DB2ErrorHandler.parse_exception(Exception("deadlock"))
        assert rc.severity == ErrorSeverity.CRITICAL

    def test_general_error_has_error_severity(self):
        rc = DB2ErrorHandler.parse_exception(Exception("something unknown"))
        assert rc.severity == ErrorSeverity.ERROR


# ===========================================================================
# DB2ErrorHandler.create_error_response
# ===========================================================================

class TestCreateErrorResponse:
    @pytest.fixture(autouse=True)
    def patch_logger(self):
        with patch.object(_eh_module, "logger", MagicMock()):
            yield

    def test_known_sqlstate_returns_correct_tag(self):
        rc = DB2ErrorHandler.create_error_response(sqlstate="23505")
        assert rc.error_tag == DB2ErrorCode.DUPLICATE_KEY.value

    def test_known_sqlstate_uses_mapped_severity(self):
        rc = DB2ErrorHandler.create_error_response(sqlstate="08001")
        assert rc.severity == ErrorSeverity.CRITICAL

    def test_unknown_sqlstate_uses_general_error(self):
        rc = DB2ErrorHandler.create_error_response(sqlstate="99999")
        assert rc.error_tag == DB2ErrorCode.GENERAL_ERROR.value

    def test_message_is_preserved_when_provided(self):
        rc = DB2ErrorHandler.create_error_response(sqlstate="23505", message="custom msg")
        assert rc.message == "custom msg"

    def test_sqlstate_stored_on_response(self):
        rc = DB2ErrorHandler.create_error_response(sqlstate="42601")
        assert rc.sqlstate == "42601"

    def test_native_error_stored_on_response(self):
        rc = DB2ErrorHandler.create_error_response(native_error=-204)
        assert rc.native_error == -204

    def test_no_sqlstate_returns_general_error(self):
        rc = DB2ErrorHandler.create_error_response()
        assert rc.error_tag == DB2ErrorCode.GENERAL_ERROR.value

    def test_returns_response_code_instance(self):
        rc = DB2ErrorHandler.create_error_response(sqlstate="42601")
        assert isinstance(rc, ResponseCode)


# ===========================================================================
# DB2ErrorHandler._map_sqlstate_to_error_tag
# ===========================================================================

class TestMapSqlstateToErrorTag:
    @pytest.mark.parametrize("sqlstate,expected_tag", [
        ("08001", DB2ErrorCode.CONNECTION_FAILED.value),
        ("08002", DB2ErrorCode.CONNECTION_CLOSED.value),
        ("08003", DB2ErrorCode.CONNECTION_CLOSED.value),
        ("08006", DB2ErrorCode.CONNECTION_FAILED.value),
        ("23001", DB2ErrorCode.DUPLICATE_KEY.value),
        ("23503", DB2ErrorCode.FOREIGN_KEY_VIOLATION.value),
        ("23505", DB2ErrorCode.DUPLICATE_KEY.value),
        ("40001", DB2ErrorCode.DEADLOCK.value),
        ("42703", DB2ErrorCode.COLUMN_NOT_FOUND.value),
        ("42704", DB2ErrorCode.TABLE_NOT_FOUND.value),
        ("42601", DB2ErrorCode.SYNTAX_ERROR.value),
        ("57017", DB2ErrorCode.PERMISSION_DENIED.value),
    ])
    def test_known_sqlstates_map_correctly(self, sqlstate, expected_tag):
        assert DB2ErrorHandler._map_sqlstate_to_error_tag(sqlstate) == expected_tag

    def test_unknown_sqlstate_returns_general_error(self):
        assert DB2ErrorHandler._map_sqlstate_to_error_tag("00000") == DB2ErrorCode.GENERAL_ERROR.value

    def test_empty_sqlstate_returns_general_error(self):
        assert DB2ErrorHandler._map_sqlstate_to_error_tag("") == DB2ErrorCode.GENERAL_ERROR.value


# ===========================================================================
# OperationResult
# ===========================================================================

class TestOperationResult:
    @pytest.fixture
    def ok_result(self):
        return OperationResult(ResponseCode(error_tag=None, data={"rows": [1, 2]}))

    @pytest.fixture
    def err_result(self):
        return OperationResult(ResponseCode(error_tag="ResourceNotFound"))

    def test_is_successful_true_on_success(self, ok_result):
        assert ok_result.is_successful() is True

    def test_is_successful_false_on_error(self, err_result):
        assert err_result.is_successful() is False

    def test_get_data_returns_payload(self, ok_result):
        assert ok_result.get_data() == {"rows": [1, 2]}

    def test_get_error_tag_returns_tag(self, err_result):
        assert err_result.get_error_tag() == "ResourceNotFound"

    def test_get_message_returns_string(self, err_result):
        assert isinstance(err_result.get_message(), str)

    def test_add_context_returns_self(self, ok_result):
        result = ok_result.add_context("step1")
        assert result is ok_result

    def test_add_context_stores_entries(self, ok_result):
        ok_result.add_context("step1").add_context("step2")
        assert "step1" in ok_result.operations
        assert "step2" in ok_result.operations

    def test_to_dict_has_success_key(self, ok_result):
        d = ok_result.to_dict()
        assert "success" in d
        assert d["success"] is True

    def test_to_dict_has_response_key(self, ok_result):
        d = ok_result.to_dict()
        assert "response" in d
        assert isinstance(d["response"], dict)

    def test_to_dict_has_operations_key(self, ok_result):
        ok_result.add_context("ctx")
        d = ok_result.to_dict()
        assert d["operations"] == ["ctx"]

    def test_repr_contains_response_code(self, ok_result):
        r = repr(ok_result)
        assert "OperationResult" in r


# ===========================================================================
# Helper factory functions
# ===========================================================================

class TestHelperFunctions:
    def test_success_response_is_success(self):
        rc = success_response(data="ok")
        assert rc.is_success is True

    def test_success_response_stores_data(self):
        rc = success_response(data=42)
        assert rc.data == 42

    def test_post_success_response_is_success(self):
        assert post_success_response(data="new").is_success is True

    def test_update_success_response_is_success(self):
        assert update_success_response().is_success is True

    def test_delete_success_response_is_success(self):
        assert delete_success_response().is_success is True

    def test_not_found_error_has_correct_tag(self):
        rc = not_found_error()
        assert rc.error_tag == "ResourceNotFound"

    def test_not_found_error_includes_resource_name(self):
        rc = not_found_error("Order")
        assert "Order" in rc.message

    def test_malformed_content_error_has_correct_tag(self):
        rc = malformed_content_error()
        assert rc.error_tag == "MalformedContent"

    def test_malformed_content_error_includes_details(self):
        rc = malformed_content_error("missing field X")
        assert "missing field X" in rc.message

    def test_permission_error_has_correct_tag(self):
        rc = permission_error()
        assert rc.error_tag == "PermissionIncongruency"

    def test_permission_error_includes_action(self):
        rc = permission_error(action="delete", role="admin")
        assert "delete" in rc.message
        assert "admin" in rc.message

    def test_not_found_error_has_warning_severity(self):
        rc = not_found_error()
        assert rc.severity == ErrorSeverity.WARNING

    def test_malformed_content_error_has_warning_severity(self):
        rc = malformed_content_error()
        assert rc.severity == ErrorSeverity.WARNING

    def test_permission_error_has_warning_severity(self):
        rc = permission_error()
        assert rc.severity == ErrorSeverity.WARNING


# ===========================================================================
# DB2ErrorHandler.parse_db2_error  (lines 219-243)
# ===========================================================================

class TestParseDB2Error:
    @pytest.fixture(autouse=True)
    def patch_logger(self):
        with patch.object(_eh_module, "logger", MagicMock()):
            yield

    def test_returns_response_code_instance(self):
        rc = DB2ErrorHandler.parse_db2_error(None)
        assert isinstance(rc, ResponseCode)

    def test_happy_path_returns_response_code(self):
        # ibm_db is mocked via sys.modules; conn_error/conn_errormsg return MagicMocks
        rc = DB2ErrorHandler.parse_db2_error(None)
        assert rc is not None

    def test_conn_error_exception_returns_critical_response(self):
        with patch.object(_eh_module.ibm_db, "conn_error", side_effect=RuntimeError("mock")):
            rc = DB2ErrorHandler.parse_db2_error(None)
        assert rc.severity == ErrorSeverity.CRITICAL

    def test_conn_error_exception_uses_unknown_error_tag(self):
        with patch.object(_eh_module.ibm_db, "conn_error", side_effect=AttributeError("fail")):
            rc = DB2ErrorHandler.parse_db2_error(None)
        assert rc.error_tag == DB2ErrorCode.UNKNOWN_ERROR.value

    def test_conn_error_exception_message_contains_error_text(self):
        with patch.object(_eh_module.ibm_db, "conn_error", side_effect=RuntimeError("conn broke")):
            rc = DB2ErrorHandler.parse_db2_error(None)
        assert "conn broke" in rc.message
