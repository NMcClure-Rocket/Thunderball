# DB2/SQL Error Handler - Integration Guide

## Overview

This guide demonstrates how to use the DB2/SQL error handler (`backend/utilities/error_handler.py`) with the Data Access Objects (DAOs) in real-world scenarios.

## Quick Start

### 1. Basic DAO Usage with Error Handling

```python
from backend.db.dao.customer_dao import CustomerDAO
from backend.utilities.error_handler import ErrorSeverity, ResponseCode
import ibm_db_dbi

# Initialize DAO with DB2 connection
connection = ibm_db_dbi.Connection(db_conn)
customer_dao = CustomerDAO(connection)

# Get a customer and handle response
response = customer_dao.get_by_key("12345")

if response.is_success:
    customer = response.get_data()
    print(f"Customer: {customer['NAME']}")
else:
    print(f"Error: {response.get_message()}")
    print(f"Severity: {response.severity.value}")
```

### 2. Handling Different Error Types

```python
from backend.utilities.error_handler import DB2ErrorCode

response = customer_dao.get_by_key("invalid_id")

# Check specific error type
if response.error_tag == DB2ErrorCode.CONNECTION_FAILED.value:
    # Handle connection failure - might retry
    retry_operation()
elif response.error_tag == "ResourceNotFound":
    # Handle not found - show user-friendly message
    return {"message": "Customer not found", "status": 404}
elif response.severity == ErrorSeverity.CRITICAL:
    # Handle critical errors - alert administrator
    notify_admin(response.get_message())
```

### 3. Creating Records with Constraint Error Handling

```python
from backend.db.dao.customer_dao import CustomerDAO

new_customer = {
    "CUSTOMERID": "NEW001",
    "NAME": "John Doe",
    "EMAIL": "john@example.com",
}

response = customer_dao.create_record(new_customer)

if response.is_success:
    print(f"Customer created: {response.get_data()}")
elif response.error_tag == DB2ErrorCode.DUPLICATE_KEY.value:
    # Duplicate key error - customer ID already exists
    return {"error": "Customer ID already exists", "status": 409}
elif response.error_tag == DB2ErrorCode.FOREIGN_KEY_VIOLATION.value:
    # Foreign key violation
    return {"error": "Referenced record does not exist", "status": 400}
else:
    # Generic error
    return {"error": response.get_message(), "status": 500}
```

### 4. Updating Records with Error Recovery

```python
updates = {
    "NAME": "Jane Doe",
    "EMAIL": "jane@example.com"
}

response = customer_dao.update_record("12345", updates)

if response.is_success:
    print(f"Updated customer: {response.get_data()}")
elif response.error_tag == "ResourceNotFound":
    print("Customer not found - cannot update")
elif response.severity == ErrorSeverity.CRITICAL:
    # Critical error - might be deadlock or connection issue
    # Consider retry logic
    print("Critical error, consider retrying...")
```

### 5. Deleting Records with Cascading Error Handling

```python
# Multiple DAOs for related entities
customer_dao = CustomerDAO(connection)
order_dao = OrderDAO(connection)

customer_id = "12345"

# Delete records with proper error handling
try:
    # First delete orders (to avoid foreign key violation)
    order_response = order_dao.delete_record_by_field({"CUSTOMERID": customer_id})
    if not order_response.is_success:
        raise Exception(f"Failed to delete orders: {order_response.get_message()}")
    
    # Then delete customer
    customer_response = customer_dao.delete_record(customer_id)
    if not customer_response.is_success:
        raise Exception(f"Failed to delete customer: {customer_response.get_message()}")
    
    print(f"Deleted {order_response.get_data()['deleted_count']} orders")
    print(f"Deleted customer {customer_id}")
    
except Exception as e:
    print(f"Error during deletion: {e}")
```

## Error Category Reference

### Connection Errors (Critical)

When DB2 cannot establish or maintain a connection:

```python
if response.error_tag == DB2ErrorCode.CONNECTION_FAILED.value:
    # Implementation: Retry with exponential backoff
    # Check DB2 availability
    # Notify operations team
    
    # Example retry:
    max_retries = 3
    for attempt in range(max_retries):
        response = dao.get_by_key(id)
        if response.is_success:
            break
        sleep(2 ** attempt)  # Exponential backoff
```

### Data Constraint Errors (Error)

When data violates database constraints:

```python
# Duplicate key
if response.sqlstate == "23505":  # or error_tag == DUPLICATE_KEY
    # User should try different key or retry with modified data
    return {"error": "This record already exists", "status": 409}

# Foreign key violation
if response.sqlstate == "23503":  # or error_tag == FOREIGN_KEY_VIOLATION
    # User must create referenced record first
    return {"error": "Referenced record does not exist", "status": 400}

# NOT NULL constraint
if response.sqlstate == "23502":  # or error_tag == NULL_CONSTRAINT_VIOLATION
    # User must provide required field
    return {"error": "Required field is missing", "status": 400}
```

### SQL Syntax Errors (Error)

When there's an issue with the SQL statement:

```python
if response.error_tag == DB2ErrorCode.SYNTAX_ERROR.value:
    # This indicates a programming error, not user error
    # Log for debugging
    logger.error(f"SQL Syntax Error: {response}")
    # Return generic error to user
    return {"error": "Database operation failed", "status": 500}

# Column not found
if response.error_tag == DB2ErrorCode.COLUMN_NOT_FOUND.value:
    # Schema mismatch - programming error
    logger.critical(f"Column not found: {response}")
    
# Table not found
if response.error_tag == DB2ErrorCode.TABLE_NOT_FOUND.value:
    # Schema mismatch - programming error  
    logger.critical(f"Table not found: {response}")
```

### Transaction Errors (Critical)

When DB2 has transaction management issues:

```python
if response.error_tag == DB2ErrorCode.DEADLOCK.value:
    # Deadlock detected - retry recommended
    # Implement backoff and retry logic
    response = retry_with_backoff(lambda: dao.update_record(id, updates), max_retries=3)
    
if response.error_tag == DB2ErrorCode.LOCK_TIMEOUT.value:
    # Lock timeout - resource contention
    # Can retry or fail gracefully
    return {"error": "Resource temporarily unavailable, please retry", "status": 503}
```

### Permission Errors (Error)

When user lacks database permissions:

```python
if response.error_tag == DB2ErrorCode.PERMISSION_DENIED.value:
    # User cannot perform this operation
    # Check credentials and permissions
    logger.warning(f"Permission denied for user: {current_user}")
    return {"error": "You lack permission for this operation", "status": 403}
```

## API Endpoint Examples

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException, status
from backend.db.dao.customer_dao import CustomerDAO
from backend.utilities.error_handler import ErrorSeverity, DB2ErrorCode

app = FastAPI()

@app.get("/api/customers/{customer_id}")
async def get_customer(customer_id: str):
    """Get customer by ID with proper error handling"""
    dao = CustomerDAO(get_db_connection())
    response = dao.get_by_key(customer_id)
    
    if response.is_success:
        return response.get_data()
    
    # Map error types to HTTP status codes
    error_map = {
        "ResourceNotFound": (404, "Customer not found"),
        DB2ErrorCode.CONNECTION_FAILED.value: (503, "Database unavailable"),
        DB2ErrorCode.PERMISSION_DENIED.value: (403, "Insufficient permissions"),
    }
    
    status_code, message = error_map.get(
        response.error_tag,
        (500, "Internal server error")
    )
    
    raise HTTPException(status_code=status_code, detail=message)


@app.post("/api/customers")
async def create_customer(customer: dict):
    """Create customer with comprehensive error handling"""
    dao = CustomerDAO(get_db_connection())
    response = dao.create_record(customer)
    
    if response.is_success:
        return {"id": response.get_data()["CUSTOMERID"], "status": 201}
    
    # Handle specific DB2 errors
    if response.error_tag == DB2ErrorCode.DUPLICATE_KEY.value:
        raise HTTPException(
            status_code=409,
            detail="Customer ID already exists"
        )
    
    if response.error_tag == DB2ErrorCode.FOREIGN_KEY_VIOLATION.value:
        raise HTTPException(
            status_code=400,
            detail="Referenced record does not exist"
        )
    
    if response.severity == ErrorSeverity.CRITICAL:
        raise HTTPException(
            status_code=503,
            detail="Database service unavailable"
        )
    
    raise HTTPException(
        status_code=500,
        detail=response.get_message()
    )


@app.put("/api/customers/{customer_id}")
async def update_customer(customer_id: str, updates: dict):
    """Update customer with retry logic for deadlocks"""
    dao = CustomerDAO(get_db_connection())
    
    # Retry on deadlock
    max_retries = 3
    for attempt in range(max_retries):
        response = dao.update_record(customer_id, updates)
        
        if response.is_success:
            return {"status": "updated", "id": customer_id}
        
        # Retry on deadlock
        if response.error_tag == DB2ErrorCode.DEADLOCK.value and attempt < max_retries - 1:
            await asyncio.sleep(0.1 * (2 ** attempt))  # Exponential backoff
            continue
        
        # Handle final error
        if response.error_tag == "ResourceNotFound":
            raise HTTPException(status_code=404, detail="Customer not found")
        
        raise HTTPException(
            status_code=500,
            detail=response.get_message()
        )


@app.delete("/api/customers/{customer_id}")
async def delete_customer(customer_id: str):
    """Delete customer with transaction management"""
    dao = CustomerDAO(get_db_connection())
    response = dao.delete_record(customer_id)
    
    if response.is_success:
        return {"status": "deleted", "id": customer_id}
    
    if response.error_tag == "ResourceNotFound":
        raise HTTPException(status_code=404, detail="Customer not found")
    
    if response.error_tag == DB2ErrorCode.FOREIGN_KEY_VIOLATION.value:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete customer with related records"
        )
    
    raise HTTPException(
        status_code=500,
        detail=response.get_message()
    )
```

## Logging Integration

```python
import logging
from backend.utilities.error_handler import ErrorSeverity

logger = logging.getLogger(__name__)

def log_response(response, operation_name):
    """Log response with appropriate level based on severity"""
    
    if response.is_success:
        logger.info(f"{operation_name}: Success")
        return
    
    severity = response.severity
    message = response.get_message()
    
    if severity == ErrorSeverity.CRITICAL:
        logger.critical(f"{operation_name}: {message} (SQLSTATE: {response.sqlstate})")
        # Alert operations team
        notify_ops_critical(f"{operation_name}: {message}")
    
    elif severity == ErrorSeverity.ERROR:
        logger.error(f"{operation_name}: {message}")
    
    elif severity == ErrorSeverity.WARNING:
        logger.warning(f"{operation_name}: {message}")
    
    else:
        logger.info(f"{operation_name}: {message}")

# Usage
response = customer_dao.get_by_key("12345")
log_response(response, "Get Customer")
```

## Testing with Mock Errors

```python
from backend.utilities.error_handler import (
    ResponseCode,
    ErrorSeverity,
    DB2ErrorCode,
    DB2ErrorHandler
)

def test_duplicate_key_handling():
    """Test handling of duplicate key error"""
    # Simulate duplicate key error
    response = DB2ErrorHandler.create_error_response(
        sqlstate="23505",
        native_error=-803,
        message="Duplicate value for primary key"
    )
    
    assert response.error_tag == DB2ErrorCode.DUPLICATE_KEY.value
    assert response.severity == ErrorSeverity.ERROR
    assert response.sqlstate == "23505"
    assert response.native_error == -803

def test_connection_failure_handling():
    """Test handling of connection failure"""
    response = DB2ErrorHandler.create_error_response(
        sqlstate="08001",
        message="Unable to connect to server"
    )
    
    assert response.error_tag == DB2ErrorCode.CONNECTION_FAILED.value
    assert response.severity == ErrorSeverity.CRITICAL

def test_response_serialization():
    """Test ResponseCode serialization to JSON"""
    response = ResponseCode(
        error_tag="ResourceNotFound",
        severity=ErrorSeverity.WARNING,
        message="Customer not found"
    )
    
    response_dict = response.to_dict()
    assert response_dict["is_success"] == False
    assert response_dict["error_tag"] == "ResourceNotFound"
    assert "timestamp" in response_dict
```

## Best Practices Summary

1. **Always check `is_success`** before accessing data
2. **Use severity levels** to determine user vs system error
3. **Log critical errors** immediately for monitoring
4. **Implement retry logic** for deadlocks and timeouts
5. **Map error codes to HTTP status codes** in API endpoints
6. **Provide user-friendly messages** while logging technical details
7. **Test error scenarios** explicitly
8. **Document expected errors** in API documentation
9. **Use SQLSTATE codes** for precise error identification
10. **Handle connection errors** with reconnection logic
