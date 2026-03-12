# DB2/SQL Error Handler - Summary

## What Was Created

A comprehensive error handling system specifically designed for DB2 and SQL database operations in the Thunderball project.

## Files Created/Modified

### 1. **backend/utilities/error_handler.py** (NEW)
The main error handler module containing:
- `ErrorSeverity` enum: INFO, WARNING, ERROR, CRITICAL
- `DB2ErrorCode` enum: 20+ DB2-specific error codes
- `ResponseCode` class: Standardized response object for all operations
- `DB2ErrorHandler` class: Error parsing and categorization
- `OperationResult` class: Result wrapper with context tracking
- Helper functions: `success_response()`, `not_found_error()`, `malformed_content_error()`, etc.

### 2. **backend/utilities/__init__.py** (NEW)
Package initialization file exposing all public error handler classes and functions.

### 3. **backend/db/dao/abstract_record.py** (MODIFIED)
Updated to use the new error handler:
- Imports from `backend.utilities.error_handler`
- Uses `ResponseCode` for all operations
- `db2_safe` decorator now uses `DB2ErrorHandler.parse_exception()`
- Removed external dependencies (logger, credentials)
- Simplified error handling with helper functions

### 4. **backend/utilities/ERROR_HANDLER_GUIDE.md** (NEW)
Comprehensive documentation including:
- Core component descriptions
- SQLSTATE mapping reference
- All class methods and properties
- Usage examples
- DB2-specific considerations
- Best practices
- Extension guidelines

### 5. **backend/utilities/INTEGRATION_GUIDE.md** (NEW)
Practical integration guide with:
- Quick start examples
- Error type handling patterns
- API endpoint examples (FastAPI)
- Logging integration
- Testing patterns
- Transaction error handling

## Key Features

### Error Categorization
Errors are automatically categorized by type:
- Connection errors
- SQL syntax errors
- Data constraint violations
- Transaction/deadlock errors
- Permission errors
- System errors

### Error Severity Levels
```python
ErrorSeverity.INFO       # Informational
ErrorSeverity.WARNING    # Warning (resource not found, etc.)
ErrorSeverity.ERROR      # Standard error (constraint violation, etc.)
ErrorSeverity.CRITICAL   # Critical (connection failure, deadlock, etc.)
```

### SQLSTATE Support
Maps DB2's 5-character SQLSTATE codes to error types:
```
08001 - Connection failed
23505 - Duplicate key
40001 - Deadlock
42703 - Column not found
...and 30+ more codes
```

### ResponseCode Object
Every DAO operation returns a `ResponseCode` with:
- `error_tag`: Standard error code for programmatic handling
- `data`: Operation result
- `severity`: Error severity level
- `sqlstate`: DB2 SQLSTATE code (5 chars)
- `native_error`: DB2 native error code
- `message`: Human-readable message
- `timestamp`: When the error occurred
- `is_success`: Boolean for easy checking

## Usage Pattern

```python
response = dao.perform_operation()

# Check success
if response.is_success:
    result = response.get_data()
   # Use result
else:
    # Handle error
    if response.severity == ErrorSeverity.CRITICAL:
        # Alert operations
        pass
    elif response.error_tag == DB2ErrorCode.DUPLICATE_KEY.value:
        # Handle duplicate key
        pass
    else:
        # Handle generic error
        user_message = response.get_message()
```

## Error Type Handling

### Duplicate Key
```python
response.error_tag == DB2ErrorCode.DUPLICATE_KEY.value
response.sqlstate == "23505"
response.native_error == -803
# Action: Return 409 Conflict to user
```

### Foreign Key Violation
```python
response.error_tag == DB2ErrorCode.FOREIGN_KEY_VIOLATION.value
response.sqlstate == "23503"
response.native_error == -530
# Action: Return 400 Bad Request, user must create referenced record first
```

### Deadlock
```python
response.error_tag == DB2ErrorCode.DEADLOCK.value
response.sqlstate == "40001"
response.native_error == -911
# Action: Implement retry logic with exponential backoff
```

### Connection Failed
```python
response.error_tag == DB2ErrorCode.CONNECTION_FAILED.value
response.severity == ErrorSeverity.CRITICAL
# Action: Reconnect to DB2 or return 503 Service Unavailable
```

### Resource Not Found
```python
response.error_tag == "ResourceNotFound"
response.severity == ErrorSeverity.WARNING
# Action: Return 404 Not Found to user
```

## Integration with DAOs

All DAO methods are wrapped with `@db2_safe` decorator:

```python
@db2_safe
def get_by_key(self, ID: str) -> ResponseCode:
    # Automatic exception catching and conversion
    pass
```

The decorator:
1. Catches any exception raised
2. Uses `DB2ErrorHandler.parse_exception()` to categorize it
3. Returns a properly formatted `ResponseCode`

## HTTP Status Code Mapping

| Error Type | Status Code | ResponseCode |
|-----------|------------|--------------|
| Success | 200 | `error_tag=None` |
| Resource not found | 404 | `error_tag="ResourceNotFound"` |
| Duplicate key | 409 | `error_tag="SQL_DUPLICATE_KEY"` |
| Bad request | 400 | `error_tag="MalformedContent"` |
| Permission denied | 403 | `error_tag="DB2_PERMISSION_DENIED"` |
| Service unavailable | 503 | `severity=CRITICAL` |
| Internal error | 500 | Other errors |

## API Response Examples

### Success Response
```json
{
  "is_success": true,
  "error_tag": null,
  "severity": "INFO",
  "message": "Operation completed successfully",
  "data": {"id": "12345", "name": "John Doe"},
  "timestamp": "2026-03-12T10:30:45.123456"
}
```

### Error Response (Duplicate Key)
```json
{
  "is_success": false,
  "error_tag": "SQL_DUPLICATE_KEY",
  "severity": "ERROR",
  "message": "Duplicate value for primary key",
  "sqlstate": "23505",
  "native_error": -803,
  "data": null,
  "timestamp": "2026-03-12T10:30:45.123456"
}
```

### Error Response (Connection Failed)
```json
{
  "is_success": false,
  "error_tag": "DB2_CONNECTION_FAILED",
  "severity": "CRITICAL",
  "message": "Unable to connect to server",
  "sqlstate": "08001",
  "native_error": -1224,
  "data": null,
  "timestamp": "2026-03-12T10:30:45.123456"
}
```

## Testing Error Scenarios

```python
from backend.utilities.error_handler import DB2ErrorHandler

# Simulate duplicate key error
response = DB2ErrorHandler.create_error_response(
    sqlstate="23505",
    native_error=-803,
    message="Duplicate customer ID"
)
assert response.error_tag == DB2ErrorCode.DUPLICATE_KEY.value

# Simulate connection error
response = DB2ErrorHandler.parse_exception(
    Exception("Unable to connect to server")
)
assert response.severity == ErrorSeverity.CRITICAL
```

## Quick Reference

### Check Operation Success
```python
if response.is_success:
    # Success - use response.get_data()
else:
    # Failure - use response.get_message()
```

### Get Specific Information
```python
response.get_error_tag()   # Error code
response.get_message()     # Human-readable message
response.get_data()        # Operation result (if successful)
response.severity          # ErrorSeverity enum
response.sqlstate          # DB2 SQLSTATE code
response.native_error      # DB2 native error code
```

### Convert to JSON
```python
response.to_dict()  # Returns dictionary for JSON serialization
```

### Common Helper Functions
```python
from backend.utilities import (
    success_response,                    # Generic success
    post_success_response,               # POST success
    update_success_response,             # UPDATE success
    delete_success_response,             # DELETE success
    not_found_error,                     # Resource not found
    malformed_content_error,             # Bad request
    permission_error                     # Permission denied
)
```

## Implementation Checklist

- [x] Error handler module created (`error_handler.py`)
- [x] Error codes defined (20+ DB2-specific codes)
- [x] SQLSTATE mapping implemented (35+ codes)
- [x] ResponseCode class implemented
- [x] Helper functions implemented
- [x] DAOs updated to use error handler
- [x] Documentation created (2 comprehensive guides)
- [x] Integration examples provided
- [x] API endpoint examples provided
- [x] Testing patterns documented

## Next Steps

1. **Update remaining services** to use the error handler
2. **Implement logging** integration (see INTEGRATION_GUIDE.md)
3. **Create unit tests** for error scenarios
4. **Update API endpoints** to return appropriate HTTP status codes
5. **Configure monitoring** alerts for CRITICAL errors
6. **Document custom error codes** specific to your business logic

## Support Documentation

- **ERROR_HANDLER_GUIDE.md**: Comprehensive reference manual
- **INTEGRATION_GUIDE.md**: Practical usage examples and patterns
- **Code comments**: All classes and methods have detailed docstrings

## Questions?

Refer to:
1. `ERROR_HANDLER_GUIDE.md` for detailed API documentation
2. `INTEGRATION_GUIDE.md` for practical examples
3. Code docstrings in `error_handler.py` for method documentation
