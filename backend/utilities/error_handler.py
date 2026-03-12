# Copyright (C) 2025 Team White
# Licensed under the MIT License
# See LICENSE for more details

import ibm_db
from enum import Enum
from typing import Optional, Any, Dict
from datetime import datetime
from backend.utilities.logger import LoggerFactory


# Logger Factory Integration
# Initialize logger for error handling operations
logger = LoggerFactory.get_general_logger()


class ErrorSeverity(Enum):
    """Enumeration of error severity levels"""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class DB2ErrorCode(Enum):
    """DB2-specific error codes"""
    # Connection errors
    CONNECTION_FAILED = "DB2_CONNECTION_FAILED"
    CONNECTION_TIMEOUT = "DB2_CONNECTION_TIMEOUT"
    CONNECTION_CLOSED = "DB2_CONNECTION_CLOSED"
    AUTHENTICATION_FAILED = "DB2_AUTHENTICATION_FAILED"
    
    # SQL errors
    SYNTAX_ERROR = "SQL_SYNTAX_ERROR"
    CONSTRAINT_VIOLATION = "SQL_CONSTRAINT_VIOLATION"
    COLUMN_NOT_FOUND = "SQL_COLUMN_NOT_FOUND"
    TABLE_NOT_FOUND = "SQL_TABLE_NOT_FOUND"
    
    # Data errors
    DATA_TYPE_MISMATCH = "SQL_DATA_TYPE_MISMATCH"
    VALUE_TOO_LONG = "SQL_VALUE_TOO_LONG"
    NULL_CONSTRAINT_VIOLATION = "SQL_NULL_CONSTRAINT_VIOLATION"
    DUPLICATE_KEY = "SQL_DUPLICATE_KEY"
    FOREIGN_KEY_VIOLATION = "SQL_FOREIGN_KEY_VIOLATION"
    
    # Statement errors
    DEADLOCK = "DB2_DEADLOCK"
    LOCK_TIMEOUT = "DB2_LOCK_TIMEOUT"
    PERMISSION_DENIED = "DB2_PERMISSION_DENIED"
    RESOURCE_UNAVAILABLE = "DB2_RESOURCE_UNAVAILABLE"
    
    # General errors
    GENERAL_ERROR = "DB2_GENERAL_ERROR"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class ResponseCode:
    """
    Standardized response code class for all DAO and service operations.
    Provides consistent error handling for DB2/SQL operations.
    """
    
    def __init__(
        self,
        error_tag: Optional[str] = None,
        data: Optional[Any] = None,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        sqlstate: Optional[str] = None,
        native_error: Optional[int] = None,
        message: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize a ResponseCode object.
        
        Args:
            error_tag (str, optional): Standard error code. None indicates success
            data (Any, optional): Response data payload
            severity (ErrorSeverity, optional): Severity level of the error
            sqlstate (str, optional): DB2 SQLSTATE code (5 chars)
            native_error (int, optional): Native DB2 error code
            message (str, optional): Human-readable error message
            timestamp (datetime, optional): Error timestamp
        """
        self.error_tag = error_tag
        self.data = data
        self.severity = severity
        self.sqlstate = sqlstate
        self.native_error = native_error
        self.message = message or self._get_default_message(error_tag)
        self.timestamp = timestamp or datetime.now()
        self.is_success = error_tag is None
    
    def _get_default_message(self, error_tag: Optional[str]) -> str:
        """Get default message for common error tags"""
        messages = {
            "GeneralSuccess": "Operation completed successfully",
            "PostSuccess": "Resource created successfully",
            "UpdateSuccess": "Resource updated successfully",
            "DeleteSuccess": "Resource deleted successfully",
            "ResourceNotFound": "The requested resource was not found",
            "MalformedContent": "The request content is malformed or invalid",
            "PermissionIncongruency": "User lacks required permissions for this operation",
            DB2ErrorCode.CONNECTION_FAILED.value: "Failed to establish DB2 connection",
            DB2ErrorCode.SYNTAX_ERROR.value: "SQL syntax error in query",
            DB2ErrorCode.CONSTRAINT_VIOLATION.value: "Database constraint violation",
            DB2ErrorCode.DUPLICATE_KEY.value: "Duplicate key value attempted",
            DB2ErrorCode.FOREIGN_KEY_VIOLATION.value: "Foreign key constraint violation",
            DB2ErrorCode.DEADLOCK.value: "Database deadlock detected",
            DB2ErrorCode.LOCK_TIMEOUT.value: "Lock timeout waiting for resource",
            DB2ErrorCode.PERMISSION_DENIED.value: "Insufficient database permissions",
        }
        return messages.get(error_tag, f"Error: {error_tag}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ResponseCode to dictionary for JSON serialization"""
        return {
            "is_success": self.is_success,
            "error_tag": self.error_tag,
            "severity": self.severity.value if isinstance(self.severity, ErrorSeverity) else self.severity,
            "message": self.message,
            "sqlstate": self.sqlstate,
            "native_error": self.native_error,
            "data": self.data,
            "timestamp": self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else str(self.timestamp)
        }
    
    def __repr__(self) -> str:
        """String representation of ResponseCode"""
        status = "SUCCESS" if self.is_success else "FAILED"
        if self.error_tag:
            return f"ResponseCode({status}, error={self.error_tag}, message='{self.message}')"
        return f"ResponseCode({status}, data={self.data})"

    def log_response(self, operation_name: str = "Database Operation") -> None:
        """
        Log the response with appropriate level based on severity.
        
        Args:
            operation_name (str): Name of the operation for logging context
        """
        if self.is_success:
            logger.info(f"{operation_name}: Success - {self.message}")
        elif self.severity == ErrorSeverity.CRITICAL:
            logger.critical(
                f"{operation_name}: CRITICAL - {self.message} "
                f"(SQLSTATE: {self.sqlstate}, Error: {self.native_error})"
            )
        elif self.severity == ErrorSeverity.ERROR:
            logger.error(
                f"{operation_name}: ERROR - {self.message} "
                f"(SQLSTATE: {self.sqlstate}, Error: {self.native_error})"
            )
        elif self.severity == ErrorSeverity.WARNING:
            logger.warning(f"{operation_name}: WARNING - {self.message}")
        else:
            logger.info(f"{operation_name}: {self.message}")


class DB2ErrorHandler:
    """
    Handles DB2 and SQL-specific errors with proper categorization and logging.
    """
    
    # SQLState codes for DB2
    SQLSTATE_MAPPING = {
        "00000": ("Success", ErrorSeverity.INFO),
        "01004": ("String data truncated", ErrorSeverity.WARNING),
        "01505": ("Warning: Column already exists", ErrorSeverity.WARNING),
        "07001": ("Parameter count mismatch", ErrorSeverity.ERROR),
        "08001": ("Unable to connect to server", ErrorSeverity.CRITICAL),
        "08002": ("Connection name in use", ErrorSeverity.ERROR),
        "08003": ("Connection not open", ErrorSeverity.ERROR),
        "08006": ("Connection failure", ErrorSeverity.CRITICAL),
        "22001": ("String data right truncation", ErrorSeverity.ERROR),
        "22005": ("Error in assignment", ErrorSeverity.ERROR),
        "22012": ("Division by zero", ErrorSeverity.ERROR),
        "22501": ("The statement string attempted to update or delete all rows", ErrorSeverity.WARNING),
        "23001": ("Primary key constraint violation", ErrorSeverity.ERROR),
        "23502": ("NOT NULL constraint violation", ErrorSeverity.ERROR),
        "23503": ("Foreign key constraint violation", ErrorSeverity.ERROR),
        "23505": ("Duplicate key violation", ErrorSeverity.ERROR),
        "23514": ("Check constraint violation", ErrorSeverity.ERROR),
        "40001": ("Serialization failure (deadlock)", ErrorSeverity.CRITICAL),
        "40003": ("Statement completion unknown", ErrorSeverity.CRITICAL),
        "42601": ("Syntax error", ErrorSeverity.ERROR),
        "42602": ("Invalid name", ErrorSeverity.ERROR),
        "42703": ("Column not found", ErrorSeverity.ERROR),
        "42704": ("Object not found", ErrorSeverity.ERROR),
        "42705": ("Schema not found", ErrorSeverity.ERROR),
        "42710": ("Object already exists", ErrorSeverity.ERROR),
        "42802": ("Number of columns mismatch", ErrorSeverity.ERROR),
        "42823": ("Invalid operation on object", ErrorSeverity.ERROR),
        "42884": ("Function not found", ErrorSeverity.ERROR),
        "42962": ("Check constraint violation", ErrorSeverity.ERROR),
        "44000": ("Check constraint violation", ErrorSeverity.ERROR),
        "55019": ("Resource limit exceeded", ErrorSeverity.CRITICAL),
        "57011": ("Resource limit exceeded", ErrorSeverity.CRITICAL),
        "57017": ("User does not have permission", ErrorSeverity.ERROR),
        "57019": ("User does not have permission", ErrorSeverity.ERROR),
        "58004": ("System error", ErrorSeverity.CRITICAL),
        "58005": ("SQL statement too long", ErrorSeverity.ERROR),
        "58015": ("Output parameter overflow", ErrorSeverity.ERROR),
    }

    @staticmethod
    def parse_db2_error(db_connection) -> ResponseCode:
        """
        Parse DB2 error from connection object and return ResponseCode.
        
        Args:
            db_connection: The DB2 connection object with error info
            
        Returns:
            ResponseCode: Properly formatted error response
        """
        try:
            sqlstate = ibm_db.conn_error()
            error_msg = ibm_db.conn_errormsg()
            
            # Parse native error code if available
            parts = error_msg.split("]")
            native_error = None
            if len(parts) > 0:
                try:
                    native_error = int(parts[0].strip("["))
                except (ValueError, IndexError):
                    native_error = None
            
            response = DB2ErrorHandler.create_error_response(
                sqlstate=sqlstate,
                native_error=native_error,
                message=error_msg
            )
            
            # Log the parsed error
            response.log_response(f"DB2 Connection Error (SQLSTATE: {sqlstate})")
            return response
        except Exception as e:
            logger.critical(f"Failed to parse DB2 error: {str(e)}")
            return ResponseCode(
                error_tag=DB2ErrorCode.UNKNOWN_ERROR.value,
                severity=ErrorSeverity.CRITICAL,
                message=f"Failed to parse DB2 error: {str(e)}"
            )
    
    @staticmethod
    def parse_exception(exception: Exception) -> ResponseCode:
        """
        Parse a Python exception and convert to ResponseCode with DB2 context.
        
        Args:
            exception (Exception): The exception to parse
            
        Returns:
            ResponseCode: Properly formatted error response
        """
        error_class = exception.__class__.__name__
        error_msg = str(exception)
        
        response = None
        
        # Map common exceptions to DB2 error codes
        if "connection" in error_msg.lower():
            response = ResponseCode(
                error_tag=DB2ErrorCode.CONNECTION_FAILED.value,
                severity=ErrorSeverity.CRITICAL,
                message=error_msg
            )
        elif "syntax" in error_msg.lower():
            response = ResponseCode(
                error_tag=DB2ErrorCode.SYNTAX_ERROR.value,
                severity=ErrorSeverity.ERROR,
                message=error_msg
            )
        elif "constraint" in error_msg.lower():
            response = ResponseCode(
                error_tag=DB2ErrorCode.CONSTRAINT_VIOLATION.value,
                severity=ErrorSeverity.ERROR,
                message=error_msg
            )
        elif "duplicate" in error_msg.lower():
            response = ResponseCode(
                error_tag=DB2ErrorCode.DUPLICATE_KEY.value,
                severity=ErrorSeverity.ERROR,
                message=error_msg
            )
        elif "foreign key" in error_msg.lower():
            response = ResponseCode(
                error_tag=DB2ErrorCode.FOREIGN_KEY_VIOLATION.value,
                severity=ErrorSeverity.ERROR,
                message=error_msg
            )
        elif "deadlock" in error_msg.lower():
            response = ResponseCode(
                error_tag=DB2ErrorCode.DEADLOCK.value,
                severity=ErrorSeverity.CRITICAL,
                message=error_msg
            )
        elif "timeout" in error_msg.lower():
            response = ResponseCode(
                error_tag=DB2ErrorCode.LOCK_TIMEOUT.value,
                severity=ErrorSeverity.ERROR,
                message=error_msg
            )
        elif "permission" in error_msg.lower() or "not authorized" in error_msg.lower():
            response = ResponseCode(
                error_tag=DB2ErrorCode.PERMISSION_DENIED.value,
                severity=ErrorSeverity.ERROR,
                message=error_msg
            )
        else:
            response = ResponseCode(
                error_tag=DB2ErrorCode.GENERAL_ERROR.value,
                severity=ErrorSeverity.ERROR,
                message=f"{error_class}: {error_msg}"
            )
        
        # Log the parsed exception
        response.log_response(f"Exception Handling ({error_class})")
        return response
    
    @staticmethod
    def create_error_response(
        sqlstate: Optional[str] = None,
        native_error: Optional[int] = None,
        message: Optional[str] = None
    ) -> ResponseCode:
        """
        Create an error ResponseCode based on SQLSTATE code.
        
        Args:
            sqlstate (str, optional): 5-character SQLSTATE code
            native_error (int, optional): Native DB2 error code
            message (str, optional): Error message
            
        Returns:
            ResponseCode: Properly categorized error response
        """
        # Look up SQLSTATE in mapping
        if sqlstate and sqlstate in DB2ErrorHandler.SQLSTATE_MAPPING:
            msg, severity = DB2ErrorHandler.SQLSTATE_MAPPING[sqlstate]
            error_tag = DB2ErrorHandler._map_sqlstate_to_error_tag(sqlstate)
        else:
            msg = message or "Unknown DB2 error"
            severity = ErrorSeverity.ERROR
            error_tag = DB2ErrorCode.GENERAL_ERROR.value
        
        response = ResponseCode(
            error_tag=error_tag,
            severity=severity,
            sqlstate=sqlstate,
            native_error=native_error,
            message=message or msg
        )
        
        # Log the created error response
        response.log_response(f"DB2 Error Created (SQLSTATE: {sqlstate})")
        return response
    
    @staticmethod
    def _map_sqlstate_to_error_tag(sqlstate: str) -> str:
        """Map SQLSTATE code to error tag"""
        mapping = {
            "08001": DB2ErrorCode.CONNECTION_FAILED.value,
            "08002": DB2ErrorCode.CONNECTION_CLOSED.value,
            "08003": DB2ErrorCode.CONNECTION_CLOSED.value,
            "08006": DB2ErrorCode.CONNECTION_FAILED.value,
            "23001": DB2ErrorCode.DUPLICATE_KEY.value,
            "23502": DB2ErrorCode.NULL_CONSTRAINT_VIOLATION.value,
            "23503": DB2ErrorCode.FOREIGN_KEY_VIOLATION.value,
            "23505": DB2ErrorCode.DUPLICATE_KEY.value,
            "40001": DB2ErrorCode.DEADLOCK.value,
            "42703": DB2ErrorCode.COLUMN_NOT_FOUND.value,
            "42704": DB2ErrorCode.TABLE_NOT_FOUND.value,
            "42705": DB2ErrorCode.TABLE_NOT_FOUND.value,
            "42601": DB2ErrorCode.SYNTAX_ERROR.value,
            "57017": DB2ErrorCode.PERMISSION_DENIED.value,
            "57019": DB2ErrorCode.PERMISSION_DENIED.value,
        }
        return mapping.get(sqlstate, DB2ErrorCode.GENERAL_ERROR.value)


class OperationResult:
    """
    Wrapper for operation results with built-in error handling.
    Provides a fluent API for chaining operations with error context.
    """
    
    def __init__(self, response_code: ResponseCode):
        """
        Initialize OperationResult with a ResponseCode.
        
        Args:
            response_code (ResponseCode): The response code for this operation
        """
        self.response_code = response_code
        self.operations = []
    
    def is_successful(self) -> bool:
        """Check if operation was successful"""
        return self.response_code.is_success
    
    def get_data(self) -> Any:
        """Get the operation data"""
        return self.response_code.data
    
    def get_error_tag(self) -> Optional[str]:
        """Get the error tag"""
        return self.response_code.error_tag
    
    def get_message(self) -> str:
        """Get the error message"""
        return self.response_code.message
    
    def add_context(self, context: str) -> "OperationResult":
        """Add context information to the operation"""
        self.operations.append(context)
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "success": self.is_successful(),
            "response": self.response_code.to_dict(),
            "operations": self.operations
        }
    
    def __repr__(self) -> str:
        return f"OperationResult({self.response_code})"


# Common success responses
def success_response(data: Any = None, message: str = "GeneralSuccess") -> ResponseCode:
    """Create a success response"""
    return ResponseCode(error_tag=None, data=data)


def post_success_response(data: Any = None) -> ResponseCode:
    """Create a POST success response (resource created)"""
    return ResponseCode(error_tag=None, data=data)


def update_success_response(data: Any = None) -> ResponseCode:
    """Create an UPDATE success response"""
    return ResponseCode(error_tag=None, data=data)


def delete_success_response(data: Any = None) -> ResponseCode:
    """Create a DELETE success response"""
    return ResponseCode(error_tag=None, data=data)


# Common error responses
def not_found_error(resource: str = "Resource") -> ResponseCode:
    """Create a 'not found' error response"""
    return ResponseCode(
        error_tag="ResourceNotFound",
        severity=ErrorSeverity.WARNING,
        message=f"{resource} was not found"
    )


def malformed_content_error(details: str = "") -> ResponseCode:
    """Create a 'malformed content' error response"""
    return ResponseCode(
        error_tag="MalformedContent",
        severity=ErrorSeverity.WARNING,
        message=f"Request content is invalid. {details}".strip()
    )


def permission_error(action: str = "", role: str = "") -> ResponseCode:
    """Create a 'permission denied' error response"""
    msg = f"Insufficient permissions"
    if action:
        msg += f" to {action}"
    if role:
        msg += f" (required role: {role})"
    return ResponseCode(
        error_tag="PermissionIncongruency",
        severity=ErrorSeverity.WARNING,
        message=msg
    )
