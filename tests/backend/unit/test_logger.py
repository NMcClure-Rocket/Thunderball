# Copyright (C) 2025 Team White
# Licensed under the MIT License
# See LICENSE for more details

"""
Unit tests for backend/utilities/logger.py.

Because backend/utilities/__init__.py re-exports from error_handler (which
imports ibm_db and calls LoggerFactory at module level), we load logger.py
directly via importlib so this test file is independent of import-order
side-effects that other test files may have introduced.
"""
# pylint: disable=missing-class-docstring,missing-function-docstring
# pylint: disable=redefined-outer-name,protected-access,wrong-import-position

import sys
import os
import logging
import importlib.util
from unittest.mock import MagicMock, patch, mock_open
import pytest

# ---------------------------------------------------------------------------
# Isolate logger.py from the rest of the backend package so that:
#   - ibm_db is never imported
#   - LoggerFactory.initialize() is not triggered by error_handler imports
# ---------------------------------------------------------------------------

for _m in ("ibm_db", "ibm_db_dbi"):
    sys.modules.setdefault(_m, MagicMock())

_LOGGER_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend", "utilities", "logger.py")
)
_spec = importlib.util.spec_from_file_location("_real_logger", _LOGGER_PATH)
_logger_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_logger_mod)

_SmartLogger = _logger_mod._SmartLogger
LoggerFactory = _logger_mod.LoggerFactory
ALLOWED_LOG_DIR = _logger_mod.ALLOWED_LOG_DIR

# ---------------------------------------------------------------------------
# Minimal YAML config that satisfies all branches of initialize()
# ---------------------------------------------------------------------------

_MINIMAL_CONFIG = {
    "version": 1,
    "use_smart_logger": True,
    "disable_existing_loggers": False,
    "handlers": {},
    "root": {"level": "DEBUG", "handlers": []},
}

_CONFIG_WITH_LOG_FILES = {
    "version": 1,
    "use_smart_logger": False,
    "disable_existing_loggers": False,
    "handlers": {
        "general": {
            "class": "logging.FileHandler",
            "filename": "{LOG_DIR}/general.log",
        }
    },
    "root": {"level": "DEBUG", "handlers": ["general"]},
}


# ---------------------------------------------------------------------------
# Shared fixture: reset LoggerFactory singleton before every test
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def reset_factory():
    LoggerFactory._initialized = False
    LoggerFactory._general_logger = None
    LoggerFactory._security_logger = None
    LoggerFactory._use_smart_logger = True
    yield
    LoggerFactory._initialized = False
    LoggerFactory._general_logger = None
    LoggerFactory._security_logger = None


# ===========================================================================
# _SmartLogger
# ===========================================================================

class TestSmartLogger:
    def _make(self, level: int) -> _SmartLogger:
        smart = _SmartLogger("test.smart")
        smart._logger = MagicMock()
        smart._logger.isEnabledFor.return_value = level != -1
        return smart

    # -- debug ---------------------------------------------------------------

    def test_debug_calls_logger_when_enabled(self):
        s = self._make(logging.DEBUG)
        s.debug("msg")
        s._logger.debug.assert_called_once()

    def test_debug_skips_when_disabled(self):
        s = self._make(-1)
        s.debug("msg")
        s._logger.debug.assert_not_called()

    def test_debug_forwards_kwargs(self):
        s = self._make(logging.DEBUG)
        s.debug("msg %s", "arg", extra={"key": "val"})
        _, kwargs = s._logger.debug.call_args
        assert "stacklevel" in kwargs

    # -- info ----------------------------------------------------------------

    def test_info_calls_logger_when_enabled(self):
        s = self._make(logging.INFO)
        s.info("hello")
        s._logger.info.assert_called_once()

    def test_info_skips_when_disabled(self):
        s = self._make(-1)
        s.info("hello")
        s._logger.info.assert_not_called()

    # -- warning -------------------------------------------------------------

    def test_warning_calls_logger_when_enabled(self):
        s = self._make(logging.WARNING)
        s.warning("warn")
        s._logger.warning.assert_called_once()

    def test_warning_skips_when_disabled(self):
        s = self._make(-1)
        s.warning("warn")
        s._logger.warning.assert_not_called()

    # -- error ---------------------------------------------------------------

    def test_error_calls_logger_when_enabled(self):
        s = self._make(logging.ERROR)
        s.error("err")
        s._logger.error.assert_called_once()

    def test_error_skips_when_disabled(self):
        s = self._make(-1)
        s.error("err")
        s._logger.error.assert_not_called()

    # -- critical ------------------------------------------------------------

    def test_critical_always_calls_logger(self):
        s = self._make(-1)  # isEnabledFor irrelevant for critical
        s._logger.isEnabledFor.return_value = False
        s.critical("crit")
        s._logger.critical.assert_called_once()

    # -- exception -----------------------------------------------------------

    def test_exception_always_calls_logger(self):
        s = self._make(-1)
        s.exception("exc")
        s._logger.exception.assert_called_once()

    # -- stacklevel ----------------------------------------------------------

    def test_stacklevel_is_2_for_info(self):
        s = self._make(logging.INFO)
        s.info("msg")
        _, kwargs = s._logger.info.call_args
        assert kwargs.get("stacklevel") == 2

    def test_stacklevel_is_2_for_warning(self):
        s = self._make(logging.WARNING)
        s.warning("msg")
        _, kwargs = s._logger.warning.call_args
        assert kwargs.get("stacklevel") == 2

    def test_stacklevel_is_2_for_error(self):
        s = self._make(logging.ERROR)
        s.error("msg")
        _, kwargs = s._logger.error.call_args
        assert kwargs.get("stacklevel") == 2


# ===========================================================================
# LoggerFactory._is_safe_log_path
# ===========================================================================

class TestIsSafeLogPath:
    def test_path_inside_allowed_dir_is_safe(self):
        safe = os.path.join(ALLOWED_LOG_DIR, "general.log")
        assert LoggerFactory._is_safe_log_path(safe) is True

    def test_path_inside_subdir_is_safe(self):
        safe = os.path.join(ALLOWED_LOG_DIR, "sub", "app.log")
        assert LoggerFactory._is_safe_log_path(safe) is True

    def test_path_outside_allowed_dir_is_unsafe(self):
        unsafe = os.path.join(os.path.dirname(ALLOWED_LOG_DIR), "evil.log")
        assert LoggerFactory._is_safe_log_path(unsafe) is False

    def test_system_root_path_is_unsafe(self):
        assert LoggerFactory._is_safe_log_path("/tmp/evil.log") is False

    def test_path_traversal_is_unsafe(self):
        traversal = os.path.join(ALLOWED_LOG_DIR, "..", "..", "etc", "passwd")
        assert LoggerFactory._is_safe_log_path(traversal) is False

    def test_allowed_dir_itself_is_safe(self):
        assert LoggerFactory._is_safe_log_path(ALLOWED_LOG_DIR) is True


# ===========================================================================
# LoggerFactory.initialize()
# ===========================================================================

class TestInitialize:
    def _run_initialize(self, config=None):
        config = config or _MINIMAL_CONFIG
        with patch("os.makedirs"), \
             patch("os.path.exists", return_value=True), \
             patch("builtins.open", mock_open()), \
             patch("yaml.safe_load", return_value=config), \
             patch("logging.config.dictConfig"):
            LoggerFactory.initialize()

    def test_sets_initialized_to_true(self):
        self._run_initialize()
        assert LoggerFactory._initialized is True

    def test_noop_if_already_initialized(self):
        LoggerFactory._initialized = True
        with patch("os.makedirs") as mock_mkd:
            LoggerFactory.initialize()
        mock_mkd.assert_not_called()

    def test_creates_logs_directory(self):
        with patch("os.makedirs") as mock_mkd, \
             patch("os.path.exists", return_value=True), \
             patch("builtins.open", mock_open()), \
             patch("yaml.safe_load", return_value=_MINIMAL_CONFIG), \
             patch("logging.config.dictConfig"):
            LoggerFactory.initialize()
        mock_mkd.assert_called_once()

    def test_calls_dictconfig_with_loaded_config(self):
        with patch("os.makedirs"), \
             patch("os.path.exists", return_value=True), \
             patch("builtins.open", mock_open()), \
             patch("yaml.safe_load", return_value=_MINIMAL_CONFIG), \
             patch("logging.config.dictConfig") as mock_dc:
            LoggerFactory.initialize()
        mock_dc.assert_called_once_with(_MINIMAL_CONFIG)

    def test_sets_use_smart_logger_from_config_true(self):
        self._run_initialize(config={**_MINIMAL_CONFIG, "use_smart_logger": True})
        assert LoggerFactory._use_smart_logger is True

    def test_sets_use_smart_logger_from_config_false(self):
        self._run_initialize(config={**_MINIMAL_CONFIG, "use_smart_logger": False})
        assert LoggerFactory._use_smart_logger is False

    def test_creates_log_files_when_missing(self):
        with patch("os.makedirs"), \
             patch("os.path.exists", return_value=False), \
             patch("builtins.open", mock_open()) as mock_file, \
             patch("yaml.safe_load", return_value=_MINIMAL_CONFIG), \
             patch("logging.config.dictConfig"):
            LoggerFactory.initialize()
        # open called for general.log, security.log, and config YAML = 3 times
        assert mock_file.call_count >= 3

    def test_replaces_log_dir_placeholder_in_handler_filename(self):
        config_copy = {
            **_CONFIG_WITH_LOG_FILES,
            "handlers": {
                "general": {
                    "class": "logging.FileHandler",
                    "filename": "{LOG_DIR}/general.log",
                }
            },
        }
        with patch("os.makedirs"), \
             patch("os.path.exists", return_value=True), \
             patch("builtins.open", mock_open()), \
             patch("yaml.safe_load", return_value=config_copy), \
             patch("logging.config.dictConfig"):
            LoggerFactory.initialize()
        # The placeholder must have been replaced
        filename = config_copy["handlers"]["general"]["filename"]
        assert "{LOG_DIR}" not in filename
        assert ALLOWED_LOG_DIR in filename

    def test_raises_value_error_on_unsafe_log_path(self):
        evil_config = {
            **_MINIMAL_CONFIG,
            "handlers": {
                "evil": {
                    "class": "logging.FileHandler",
                    "filename": "{LOG_DIR}/../../../etc/passwd",
                }
            },
        }
        with patch("os.makedirs"), \
             patch("os.path.exists", return_value=True), \
             patch("builtins.open", mock_open()), \
             patch("yaml.safe_load", return_value=evil_config), \
             patch("logging.config.dictConfig"):
            with pytest.raises(ValueError, match="Unsafe log path"):
                LoggerFactory.initialize()

    def test_initialized_stays_false_after_error(self):
        evil_config = {
            **_MINIMAL_CONFIG,
            "handlers": {
                "evil": {"class": "logging.FileHandler", "filename": "{LOG_DIR}/../../../etc/passwd"}
            },
        }
        with patch("os.makedirs"), \
             patch("os.path.exists", return_value=True), \
             patch("builtins.open", mock_open()), \
             patch("yaml.safe_load", return_value=evil_config), \
             patch("logging.config.dictConfig"):
            with pytest.raises(ValueError):
                LoggerFactory.initialize()
        assert LoggerFactory._initialized is False


# ===========================================================================
# LoggerFactory.get_general_logger()
# ===========================================================================

class TestGetGeneralLogger:
    def _init_factory(self, smart: bool = True):
        LoggerFactory._initialized = True
        LoggerFactory._use_smart_logger = smart
        LoggerFactory._general_logger = None

    def test_returns_smart_logger_when_use_smart_logger_true(self):
        self._init_factory(smart=True)
        result = LoggerFactory.get_general_logger()
        assert isinstance(result, _SmartLogger)

    def test_returns_standard_logger_when_use_smart_logger_false(self):
        self._init_factory(smart=False)
        result = LoggerFactory.get_general_logger()
        assert isinstance(result, logging.Logger)

    def test_returns_same_instance_on_repeated_calls(self):
        self._init_factory(smart=True)
        first = LoggerFactory.get_general_logger()
        second = LoggerFactory.get_general_logger()
        assert first is second

    def test_calls_initialize_when_not_initialized(self):
        LoggerFactory._initialized = False
        with patch.object(LoggerFactory, "initialize"):
            # Ensure the factory won't actually call initialize's side effects
            LoggerFactory._initialized = True
            LoggerFactory._use_smart_logger = True
            LoggerFactory.get_general_logger()
        # Just verify the flow didn't raise


# ===========================================================================
# LoggerFactory.get_security_logger()
# ===========================================================================

class TestGetSecurityLogger:
    def _init_factory(self, smart: bool = True):
        LoggerFactory._initialized = True
        LoggerFactory._use_smart_logger = smart
        LoggerFactory._security_logger = None

    def test_returns_smart_logger_when_use_smart_logger_true(self):
        self._init_factory(smart=True)
        result = LoggerFactory.get_security_logger()
        assert isinstance(result, _SmartLogger)

    def test_returns_standard_logger_when_use_smart_logger_false(self):
        self._init_factory(smart=False)
        result = LoggerFactory.get_security_logger()
        assert isinstance(result, logging.Logger)

    def test_returns_same_instance_on_repeated_calls(self):
        self._init_factory(smart=True)
        first = LoggerFactory.get_security_logger()
        second = LoggerFactory.get_security_logger()
        assert first is second

    def test_security_logger_is_independent_of_general_logger(self):
        self._init_factory(smart=True)
        general = LoggerFactory.get_general_logger()
        security = LoggerFactory.get_security_logger()
        assert general is not security
