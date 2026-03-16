# DB2 Data Access Object (DAO) Implementation Guide

## Overview
This document describes how the DAO classes have been adapted to work with IBM DB2 database. The abstract `DatabaseAccessObject` class provides common database operations that are inherited by specific table DAOs.

## Architecture Changes from MongoDB to DB2

### Key Differences:
1. **Connection Management**: Changed from PyMongo's `MongoClient` to `ibm_db_dbi.Connection`
2. **Query Language**: MongoDB queries replaced with standard SQL
3. **Error Handling**: Custom `db2_safe` decorator handles DB2-specific exceptions
4. **Row Conversion**: Database rows converted to dictionaries via `_dict_from_row()` method

## DAO Classes

### Abstract Base Class: `DatabaseAccessObject`
Located in `backend/db/dao/abstract_record.py`

**Required Methods to Implement** (in subclasses):
- `_get_primary_key()`: Returns the primary key column name
- `_dict_from_row(row, columns)`: Converts DB row tuple to dictionary

**Available Methods** (inherited):
- `get_by_key(ID)`: Get record by primary key
- `get_by_fields(filter)`: Get records matching filter dictionary
- `get_all_records(limit)`: Get all records with optional limit
- `get_random(numReturned, filter)`: Get random records
- `get_short_record(numReturned, filter, max_length)`: Get records with content length < max_length
- `create_record(entry)`: Insert new record
- `update_record(ID, updates)`: Update existing record
- `delete_record(ID)`: Delete record by primary key
- `delete_record_by_field(filter)`: Delete records matching filter

### Concrete DAO Classes:

#### 1. **CustomerDAO** (`customer_dao.py`)
- **Table**: `USER18.CUSTOMER`
- **Primary Key**: `CUSTOMERID`
- Managing customer information

#### 2. **ShippingAddressDAO** (`shipping_address_dao.py`)
- **Table**: `USER18.SHIPPINGADDRESS`
- **Primary Key**: `BILL_ADDY_ID`
- Managing billing address information

#### 3. **CCIDao** (`cci_dao.py`)
- **Table**: `USER18.CCI`
- **Primary Key**: `CCI_ID`
- Managing credit card information

#### 4. **InventoryDAO** (`inventory_dao.py`)
- **Table**: `USER18.INVENTORY`
- **Primary Key**: `INVENTORY_ID`
- Managing inventory records

#### 5. **OrderDAO** (`order_dao.py`)
- **Table**: `USER18.ORDER`
- **Primary Key**: `ORDER_ID`
- Managing order information

## Usage Example

```python
from backend.db.connector import db_conn
from backend.db.dao.customer_dao import CustomerDAO
import ibm_db_dbi

# Create a DB2 connection wrapper
connection = ibm_db_dbi.Connection(db_conn)

# Initialize the DAO
customer_dao = CustomerDAO(connection)

# Get a customer by ID
result = customer_dao.get_by_key("12345")
if result.error_tag is None:
    customer_data = result.data
    print(f"Customer found: {customer_data}")

# Get all customers (limit to 10)
result = customer_dao.get_all_records(limit=10)
if result.error_tag is None:
    customers = result.data
    
# Create a new customer
new_customer = {
    "CUSTOMERID": "99999",
    "NAME": "John Doe",
    "EMAIL": "john@example.com",
    "PASSWORD": "hashed_password"
}
result = customer_dao.create_record(new_customer)
if result.error_tag is None:
    print(f"Customer created: {result.data}")

# Update a customer
updates = {"NAME": "Jane Doe", "EMAIL": "jane@example.com"}
result = customer_dao.update_record("12345", updates)

# Delete a customer
result = customer_dao.delete_record("12345")

# Get customers by field
result = customer_dao.get_by_fields({"EMAIL": "john@example.com"})
```

## Customizing DAO Classes

To add custom methods to a DAO class, extend the base class:

```python
from backend.db.dao.customer_dao import CustomerDAO
from all_the_buzz.utilities.error_handler import ResponseCode

class CustomCustomerDAO(CustomerDAO):
    def get_customer_by_email(self, email: str):
        """Get customer by email address."""
        return self.get_by_fields({"EMAIL": email})
    
    def get_customers_by_region(self, region: str):
        """Get all customers from a specific region."""
        return self.get_by_fields({"REGION": region})
```

## Important Notes

1. **Table Names**: Update the table names in each DAO `__init__` method to match your actual DB2 schema and owner
2. **Primary Keys**: Verify the primary key column names match your DB2 table definitions
3. **Column Names**: The `_dict_from_row()` method uses column names from the cursor description, which should match your DB2 table
4. **Transactions**: All CREATE, UPDATE, and DELETE operations automatically commit after execution
5. **Role-Based Access Control**: The `ROLE_MATRIX` in the abstract class controls which user roles can perform which operations
6. **Error Handling**: All methods return `ResponseCode` objects with `error_tag`, `data`, and status information

## DB2-Specific SQL Features Used

- **FETCH FIRST ... ROWS ONLY**: DB2's equivalent to LIMIT in MySQL/PostgreSQL
- **ORDER BY RAND()**: For random record selection
- **LENGTH()**: For string length comparisons
- **Parameterized Queries**: Using `?` placeholders to prevent SQL injection

## Migration from MongoDB

When migrating from MongoDB to DB2:
1. Replace collection names with table names
2. Update document fields to match DB2 column names
3. Implement `_dict_from_row()` to convert tuples to dictionaries
4. Update any aggregation pipelines to equivalent SQL queries
5. Test role-based access control with updated credentials
