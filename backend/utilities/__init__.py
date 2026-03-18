"""
Utilities module for Thunderball project.

This package contains utility classes and functions for error handling,
logging, and common operations.
"""

from utilities.error_handler import (
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

__all__ = [
    "ResponseCode",
    "ErrorSeverity",
    "DB2ErrorCode",
    "DB2ErrorHandler",
    "OperationResult",
    "success_response",
    "post_success_response",
    "update_success_response",
    "delete_success_response",
    "not_found_error",
    "malformed_content_error",
    "permission_error",
]
