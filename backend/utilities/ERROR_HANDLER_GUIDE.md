# DB2/SQL Error Handler Documentation

## Overview

The error handler (`backend/utilities/error_handler.py`) provides comprehensive error handling and response standardization for all database operations in the Thunderball project. It's specifically designed to work with IBM DB2 and SQL operations.

## Core Components

### 1. **ErrorSeverity Enum**
Defines the severity level of errors:
- `INFO`: Informational message
- `WARNING`: Warning condition (e.g., no records found)
- `ERROR`: Standard error condition
- `CRITICAL`: Critical system error (e.g., deadlock, connection failure)

### 2. **DB2ErrorCode Enum**
Enumeration of DB2-specific error codes organized by category:

**Connection Errors:**
- `CONNECTION_FAILED`: Cannot establish DB2 connection
- `CONNECTION_TIMEOUT`: Connection timeout
- `CONNECTION_CLOSED`: Connection is closed
- `AUTHENTICATION_FAILED`: Authentication failed

**SQL Errors:**
- `SYNTAX_ERROR`: SQL syntax error
- `CONSTRAINT_VIOLATION`: Generic constraint violation
- `COLUMN_NOT_FOUND`: Specified column doesn't exist
- `TABLE_NOT_FOUND`: Specified table doesn't exist

**Data Errors:**
- `DATA_TYPE_MISMATCH`: Value type doesn't match column type
- `VALUE_TOO_LONG`: Value exceeds column length
- `NULL_CONSTRAINT_VIOLATION`: NULL value in non-nullable column
- `DUPLICATE_KEY`: Duplicate primary/unique key value
- `FOREIGN_KEY_VIOLATION`: Foreign key constraint violation

**Statement Errors:**
- `DEADLOCK`: Database deadlock detected
- `LOCK_TIMEOUT`: Lock timeout waiting for resource
- `PERMISSION_DENIED`: Insufficient DB2 permissions
- `RESOURCE_UNAVAILABLE`: Required resource unavailable

### 3. **ResponseCode Class**
The main response object returned by all DAO operations.

#### Constructor Parameters:
```python
ResponseCode(
    error_tag: Optional[str] = None,      # Error code (None = success)
    data: Optional[Any] = None,           # Response data payload
    severity: ErrorSeverity = ERROR,      # Error severity level
    sqlstate: Optional[str] = None,       # DB2 SQLSTATE code
    native_error: Optional[int] = None,   # Native DB2 error code
    message: Optional[str] = None,        # Human-readable message
    timestamp: Optional[datetime] = None  # Error timestamp
)
```

#### Key Properties:
- `is_success`: Boolean indicating if operation succeeded
- `error_tag`: Standard error code for programmatic handling
- `severity`: Error severity level
- `message`: Human-readable error description
- `sqlstate`: 5-character DB2 SQLSTATE code
- `native_error`: Native DB2 error number
- `data`: Operation result data

#### Key Methods:
```python
# Check if operation succeeded
response.is_success  # True if no error_tag

# Get operation result
response.get_data()  # Returns the data

# Get error information
response.get_error_tag()  # Returns error code
response.get_message()    # Returns error message

# Convert to JSON
response.to_dict()  # Returns dict for serialization
```

### 4. **DB2ErrorHandler Class**
Static utility class for handling DB2-specific errors.

#### SQLSTATE Mapping:
Maps DB2 5-character SQLSTATE codes to severity and error information:
- `08001-08006`: Connection errors
- `22001-22012`: Data type/value errors
- `23001-23514`: Constraint violations
- `40001-40003`: Deadlock and serialization errors
- `42601-42884`: SQL syntax and object errors
- `57017-57019`: Permission errors
- `58004-58015`: System errors

#### Key Methods:

**`parse_db2_error(db_connection)`**
Parse error from a DB2 connection object:
```python
from backend.utilities.error_handler import DB2ErrorHandler

response = DB2ErrorHandler.parse_db2_error(db_conn)
if not response.is_success:
    print(f"Error: {response.message}")
    print(f"SQLSTATE: {response.sqlstate}")
```

**`parse_exception(exception)`**
Convert any Python exception to ResponseCode:
```python
try:
    # Some operation
    pass
except Exception as e:
    response = DB2ErrorHandler.parse_exception(e)
    return response
```

**`create_error_response(sqlstate, native_error, message)`**
Create error response from SQLSTATE and error codes:
```python
response = DB2ErrorHandler.create_error_response(
    sqlstate="23505",  # Duplicate key
    native_error=-803,
    message="Duplicate customer ID"
)
```

### 5. **OperationResult Class**
Wrapper for operation results with context tracking:

```python
from backend.utilities.error_handler import OperationResult

result = OperationResult(response_code)
result.add_context("Customer lookup")
result.add_context("Record update")

if result.is_successful():
    data = result.get_data()
```

## Helper Functions

Quick functions for common response scenarios:

```python
from backend.utilities.error_handler import (
    success_response,
    post_success_response,
    update_success_response,
    delete_success_response,
    not_found_error,
    malformed_content_error,
    permission_error
)

# Success responses
response = success_response(data={"id": 123})
response = post_success_response(data=record)
response = update_success_response(data=updated_record)
response = delete_success_response(data={"count": 1})

# Error responses
response = not_found_error("Customer record")
response = malformed_content_error("Missing required field: email")
response = permission_error(action="update", role="Manager")
```

## Integration with DAOs

The error handler is integrated with all DAO operations through the `db2_safe` decorator:

```python
from backend.utilities.error_handler import ResponseCode, DB2ErrorHandler

@db2_safe
def some_database_operation(self):
    # This method automatically:
    # 1. Catches all exceptions
    # 2. Categorizes them using DB2ErrorHandler
    # 3. Returns ResponseCode with proper error info
    pass
```

## Usage Examples

### Example 1: Handling DAO Response
```python
from backend.db.dao.customer_dao import CustomerDAO
from backend.utilities.error_handler import ErrorSeverity

# Get a customer
response = customer_dao.get_by_key("12345")

# Check if successful
if response.is_success:
    customer = response.get_data()
    print(f"Found customer: {customer}")
else:
    severity = response.severity
    message = response.get_message()
    
    if severity == ErrorSeverity.CRITICAL:
        # Handle critical error
        log_critical(message)
    else:
        # Handle regular error
        log_info(message)
```

### Example 2: Converting Exception to Response
```python
from backend.utilities.error_handler import DB2ErrorHandler, ResponseCode

try:
    cursor.execute(query, params)
except Exception as e:
    response = DB2ErrorHandler.parse_exception(e)
    
    if response.error_tag == "SQL_DUPLICATE_KEY":
        # Handle duplicate key
        return {"status": 409, "message": "Record already exists"}
    else:
        # Handle other errors
        return {"status": 500, "message": response.message}
```

### Example 3: Custom Error Handling with SQLSTATE
```python
from backend.utilities.error_handler import DB2ErrorHandler

try:
    cursor.execute(query)
except Exception as e:
    response = DB2ErrorHandler.parse_exception(e)
    
    # SQLSTATE "23505" = Duplicate key
    if response.sqlstate == "23505":
        # Retry with updated key or return error
        pass
```

### Example 4: API Response Conversion
```python
from fastapi import FastAPI
from backend.db.dao.customer_dao import CustomerDAO
from backend.utilities.error_handler import ErrorSeverity

app = FastAPI()

@app.get("/customers/{customer_id}")
async def get_customer(customer_id: str):
    dao = CustomerDAO(db_connection)
    response = dao.get_by_key(customer_id)
    
    # Convert ResponseCode to HTTP response
    if response.is_success:
        return {"status": 200, "data": response.get_data()}
    
    # Map severity to HTTP status code
    status_map = {
        ErrorSeverity.WARNING: 400,
        ErrorSeverity.ERROR: 404,
        ErrorSeverity.CRITICAL: 503
    }
    
    status_code = status_map.get(response.severity, 500)
    return {"status": status_code, "error": response.message}
```

## DB2-Specific Considerations

### SQLSTATE Codes
DB2 uses 5-character SQLSTATE codes for detailed error information:
- First two digits (class): Error category
- Last three digits (subclass): Specific condition

Common classes:
- `00`: Success
- `01`: Warning
- `22`: Data exception
- `23`: Constraint violation
- `42`: Syntax/access error
- `40`: Transaction error
- `57`: Resource unavailable

### Native Error Codes
DB2 also provides native error codes (negative numbers typically):
- `-803`: Duplicate key
- `-530`: Foreign key violation
- `-911`: Deadlock
- `-913`: Resource unavailable

### Connection Strings
The error handler works with DB2 connections configured in `backend/db/connector.py`:
```python
import ibm_db

conn_str = (
    f"DATABASE=HL02HL2D;"
    f"HOSTNAME=192.168.54.250;"
    f"PORT=3600;"
    f"PROTOCOL=TCPIP;"
    f"AUTHENTICATION=SERVER;"
)

db_conn = ibm_db.connect(conn_str, "", "")
```

## Best Practices

1. **Always Check Response Status**: 
```python
response = dao.operation()
if not response.is_success:
    handle_error(response.get_message())
```

2. **Use Severity for Conditional Logic**:
```python
if response.severity == ErrorSeverity.CRITICAL:
    # Escalate or retry
    alert_admin(response)
```

3. **Log with Context**:
```python
response = dao.get_by_key(id)
if not response.is_success:
    logger.error(f"Failed to get customer {id}: {response}")
```

4. **Serialize Responses Safely**:
```python
return JsonResponse(response.to_dict())
```

5. **Handle Specific SQLSTATE Codes**:
```python
response = db.execute(query)
if response.sqlstate == "23505":  # Duplicate key
    # Try alternate strategy
    pass
```

## Common Error Scenarios

### Duplicate Key Error
```python
response.error_tag == "SQL_DUPLICATE_KEY"
response.sqlstate == "23505"
response.native_error == -803
```

### Foreign Key Violation
```python
response.error_tag == "SQL_FOREIGN_KEY_VIOLATION"
response.sqlstate == "23503"
response.native_error == -530
```

### Deadlock
```python
response.error_tag == "DB2_DEADLOCK"
response.sqlstate == "40001"
response.native_error == -911
# Consider retry logic
```

### Connection Failed
```python
response.error_tag == "DB2_CONNECTION_FAILED"
response.severity == ErrorSeverity.CRITICAL
# Requires reconnection
```

## Extending the Error Handler

To add support for additional error codes:

```python
# In DB2ErrorHandler class
SQLSTATE_MAPPING = {
    "YOUR_CODE": ("Your message", ErrorSeverity.YOUR_LEVEL),
    ...
}

# In DB2ErrorHandler._map_sqlstate_to_error_tag()
mapping = {
    "YOUR_CODE": DB2ErrorCode.YOUR_ERROR.value,
    ...
}
```

## Testing Error Handling

```python
from backend.utilities.error_handler import (
    ResponseCode, 
    DB2ErrorHandler, 
    ErrorSeverity,
    DB2ErrorCode
)

def test_duplicate_key_error():
    response = DB2ErrorHandler.create_error_response(
        sqlstate="23505",
        native_error=-803,
        message="Duplicate customer ID"
    )
    assert response.error_tag == DB2ErrorCode.DUPLICATE_KEY.value
    assert response.severity == ErrorSeverity.ERROR
    assert not response.is_success
```
