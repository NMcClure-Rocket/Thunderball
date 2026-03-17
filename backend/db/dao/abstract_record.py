# Copyright (C) 2025 Team White
# Licensed under the MIT License
# See LICENSE for more details
"""Abstract base class and shared decorators for all DB2 Data Access Objects."""
from abc import ABC
from typing import Any, Callable, List, Dict
from functools import wraps

import ibm_db_dbi

from utilities.logger import LoggerFactory
from utilities.error_handler import ResponseCode
from entities.credentials_entity import Credentials

def rbac_action(action: str) -> Callable:  # pylint: disable=unused-argument
    '''
    Decorator for role-based access control on DAO methods.
    Validates that the current credentials permit the given action.

    Args:
        action (str): The action type (e.g. "read", "create", "update", "delete")

    Returns:
        Callable: The decorated function
    '''
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # TODO: enforce RBAC once credentials/roles are fully implemented
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

# def db2_safe(func):
#     '''
#     Wraps a function to ensure that a ResponseCode is always returned and that the result of a given
#     function is added to data.

#     Args:
#         func (Any): base function to be wrapped

#     Returns:
#         wrapper (function): a wrapper that will return a ResponseCode with the error or result of the passed
#         in function
#     '''
#     @wraps(func)
#     def wrapper(*args, **kwargs) -> ResponseCode:
#         try:
#             result = func(*args, **kwargs)
#             if isinstance(result, ResponseCode):
#                 return result  #Don't wrap again
#             return ResponseCode("GeneralSuccess", result)
#         except Exception as e:
#             error_tag = e.__class__.__name__
#             error_msg = str(e)
#             data = f"DatabaseError: {error_tag} - {error_msg}"
#             return ResponseCode(error_tag=error_tag, data=data)
#     return wrapper

class DatabaseAccessObject(ABC):
    '''
    This class is an abstract class that all DAO objects extend from to access their corresponding DB2 tables.
    Each extension can define a custom ROLE_MATRIX for role-based access control.

    Subclasses must implement:
        - _get_primary_key(): Returns the name of the primary key column
        - _dict_from_row(row, columns): Converts a database row tuple to a dictionary
    '''


    def __init__(self, table_name: str, connection: ibm_db_dbi.Connection):
        '''
        Args:
            table_name (str): the name of the table that the DAO accesses
            connection (ibm_db_dbi.Connection): the DB2 connection object
        '''
        self._table_name = table_name
        self._connection = connection
        self.__logger = LoggerFactory.get_general_logger()
        self.__credentials = None

    def get_credentials(self):
        '''Returns the currently set credentials, or None if not set.'''
        return self.__credentials

    def _get_primary_key(self) -> str:
        '''
        Abstract method to be implemented by subclasses.
        Returns the name of the primary key column for the table.

        Returns:
            str: The primary key column name
        '''
        raise NotImplementedError("Subclasses must implement _get_primary_key()")

    def _dict_from_row(self, row: tuple, columns: List[str]) -> Dict[str, Any]:
        '''
        Abstract method to be implemented by subclasses.
        Converts a database row tuple to a dictionary.

        Args:
            row (tuple): The database row
            columns (List[str]): The column names

        Returns:
            Dict[str, Any]: Dictionary representation of the row
        '''
        raise NotImplementedError("Subclasses must implement _dict_from_row()")

    def _execute_query(self, query: str, params: tuple = None) -> Any:
        '''
        Helper method to execute a DB2 query and handle errors.

        Args:
            query (str): The SQL query to execute
            params (tuple): Query parameters for parameterized queries

        Returns:
            Any: The query result
        '''
        try:
            cursor = self._connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
        except Exception as e:
            self.__logger.error(f"Database error executing query: {str(e)}")
            raise


    #Hook method; this should set any default field values; just override it
    def _prepare_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        '''
        Hooks to a function and overrides to give default values for MongoDB documents

        Args:
            entry (dict[str, Any]): the entry to be processed

        Returns:
            entry (dict[str, Any]): the entry after processing (usually defining a default field)
        '''
        return entry  #Default: no changes

    def set_credentials(self, credentials: Any) -> None:
        '''
        Sets the current credentials of the DAO

        Args:
            credentials (Any): the credentials given by the authorization server to use for role-based access control
        '''
        self.__credentials = credentials

    def clear_credentials(self) -> None:
        '''
        Clears any set credentials by setting the current one t "None"
        '''
        self.__credentials = None


    @rbac_action("read")
    # @db2_safe
    def get_by_key(self, ID: str) -> ResponseCode:
        '''
        Return DB2 record by primary key

        Args:
            ID (str): the primary key value

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode
            with the record as a dictionary
        '''
        self.__logger.debug(f"Getting {self.__class__.__name__} record by ID {ID}.")
        primary_key = self._get_primary_key()
        query = f"SELECT * FROM {self._table_name} WHERE {primary_key} = ?"

        cursor = self._execute_query(query, (ID,))
        row = cursor.fetchone()

        if row is None:
            return ResponseCode(error_tag="ResourceNotFound")

        columns = [desc[0] for desc in cursor.description]
        return self._dict_from_row(row, columns)

    @rbac_action("read")
    # @db2_safe
    def get_by_fields(self, filter: dict[str, Any]) -> ResponseCode:
        '''
        Return DB2 records by given fields

        Args:
            filter (dict[str, Any]): a dictionary with column names as keys and values to match

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode with the
            records as a list of dictionaries
        '''
        if not filter:
            return ResponseCode("MalformedContent", "Filter must not be empty.")

        self.__logger.debug(f"Getting {self.__class__.__name__} record by fields {filter}.")

        # Build WHERE clause
        conditions = [f"{col} = ?" for col in filter.keys()]
        where_clause = " AND ".join(conditions)
        query = f"SELECT * FROM {self._table_name} WHERE {where_clause}"

        cursor = self._execute_query(query, tuple(filter.values()))
        rows = cursor.fetchall()

        if not rows:
            return ResponseCode(error_tag="ResourceNotFound")

        columns = [desc[0] for desc in cursor.description]
        return [self._dict_from_row(row, columns) for row in rows]

    @rbac_action("read")
    # @db2_safe
    def get_all_records(self, limit: int = None) -> ResponseCode:
        '''
        Return all (or the first x) DB2 records from a table

        Args:
            limit (int optional): an integer that determines the number of records to return. By default, it is set to None and returns the entire set

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode with the
            records from the table as a list of dictionaries
        '''
        self.__logger.debug(f"Getting all {self.__class__.__name__} records with limit {limit}.")

        query = f"SELECT * FROM {self._table_name}"
        if limit is not None:
            query += f" FETCH FIRST {limit} ROWS ONLY"

        cursor = self._execute_query(query)
        rows = cursor.fetchall()

        if not rows:
            return ResponseCode(error_tag="ResourceNotFound")

        # columns = [desc[0] for desc in cursor.description]
        # return [self._dict_from_row(row, columns) for row in rows]
        return rows

    @rbac_action("read")
    # @db2_safe
    def get_random(self, numReturned: int = 1, filter: dict[str, Any] = None) -> ResponseCode:
        '''
        Return a set number of random records given an optional filter

        Args:
            numReturned (int optional): an integer that determines the number of records returned. Defaults to 1
            filter (dict[str, Any] optional): a dictionary with column names and values to filter

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode with the records as a list of dictionaries
        '''
        filter = filter or {}
        self.__logger.debug(f"Getting {numReturned} random {self.__class__.__name__} record by fields {filter}.")

        # Build WHERE clause if filter exists
        where_clause = ""
        params = list(filter.values()) if filter else []

        if filter:
            conditions = [f"{col} = ?" for col in filter.keys()]
            where_clause = " WHERE " + " AND ".join(conditions)

        # DB2 uses RAND() for random ordering
        query = f"SELECT * FROM {self._table_name}{where_clause} ORDER BY RAND() FETCH FIRST {numReturned} ROWS ONLY"

        cursor = self._execute_query(query, tuple(params) if params else None)
        rows = cursor.fetchall()

        if not rows:
            self.__logger.warning(f"Requested {numReturned}, but no records found.")
            return ResponseCode(error_tag="ResourceNotFound")

        if len(rows) < numReturned:
            self.__logger.warning(f"Requested {numReturned}, but only returned {len(rows)} records.")

        columns = [desc[0] for desc in cursor.description]
        return [self._dict_from_row(row, columns) for row in rows]

    @rbac_action("read")
    # @db2_safe
    def get_short_record(self, numReturned: int, filter: dict[str, Any] = None,
                         max_length: int = 80, content_column: str = "CONTENT") -> ResponseCode:
        '''
        Return a set number of random records given an optional filter that also have a content
        field less than the given max_length

        Args:
            numReturned (int): an integer that determines the number of records returned
            filter (dict[str, Any] optional): a dictionary with column names and values to filter
            max_length (int optional): an integer that determines the max length of the content field. Defaults to 80
            content_column (str optional): the name of the column to apply the length filter to. Defaults to "CONTENT"

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode with the records as a list of dictionaries
        '''
        filter = filter or {}
        self.__logger.debug(f"Getting {numReturned} random short (less than {max_length} characters) {self.__class__.__name__} record by fields {filter}.")

        # Build WHERE clause with both filter and length condition
        conditions = []
        params = []

        if filter:
            for col, val in filter.items():
                conditions.append(f"{col} = ?")
                params.append(val)

        # Add length condition for the specified content column
        conditions.append(f"LENGTH({content_column}) < ?")
        params.append(max_length)

        where_clause = " WHERE " + " AND ".join(conditions)

        # DB2 query with random ordering and length filter
        query = f"SELECT * FROM {self._table_name}{where_clause} ORDER BY RAND() FETCH FIRST {numReturned} ROWS ONLY"

        cursor = self._execute_query(query, tuple(params))
        rows = cursor.fetchall()

        if not rows:
            self.__logger.warning(f"Requested {numReturned}, but no records found matching criteria.")
            return ResponseCode(error_tag="ResourceNotFound")

        if len(rows) < numReturned:
            self.__logger.warning(f"Requested {numReturned}, but only returned {len(rows)} records.")

        columns = [desc[0] for desc in cursor.description]
        return [self._dict_from_row(row, columns) for row in rows]

    @rbac_action("update")
    # @db2_safe
    def update_record(self, ID: str, updates: dict[str, Any]) -> ResponseCode:
        '''
        Updates a record with the given ID and updates

        Args:
            ID (str): the primary key value
            updates (dict[str, Any]): a dictionary with column names and new values

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode with the ID
        '''
        if not updates:
            return ResponseCode("MalformedContent", "Update payload must not be empty.")

        self.__logger.debug(f"Updating {self.__class__.__name__} with ID {ID}: {updates}.")

        primary_key = self._get_primary_key()

        # Build SET clause
        set_clauses = [f"{col} = ?" for col in updates.keys()]
        set_clause = ", ".join(set_clauses)

        # Build query with primary key as WHERE condition
        query = f"UPDATE {self._table_name} SET {set_clause} WHERE {primary_key} = ?"

        # Combine update values with ID for the WHERE clause
        params = tuple(list(updates.values()) + [ID])

        self._execute_query(query, params)

        # Commit the transaction
        self._connection.commit()

        self.__logger.debug(f"Update completed for ID {ID}")
        return ID

    @rbac_action("create")
    # @db2_safe
    def create_record(self, entry: dict[str, Any]) -> ResponseCode:
        '''
        Creates a record with the entry data given

        Args:
            entry (dict[str, Any]): a dictionary of columns and values to insert

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode with the
            inserted entry as a string. Note: DB2 does not expose the generated primary key here;
            use IDENTITY_VAL_LOCAL() in a subsequent query if the PK is needed.
        '''
        entry = self._prepare_entry(entry)  # Determines if there should be default field values; override in subclass
        self.__logger.debug(f"Creating {self.__class__.__name__} record: {entry}.")

        # Build INSERT statement
        columns = list(entry.keys())
        placeholders = ", ".join(["?" for _ in columns])
        column_names = ", ".join(columns)

        query = f"INSERT INTO {self._table_name} ({column_names}) VALUES ({placeholders})"

        self._execute_query(query, tuple(entry.values()))

        # Commit the transaction
        self._connection.commit()

        self.__logger.debug("Created new record")
        return ResponseCode("PostSuccess", str(entry))

    @rbac_action("delete")
    # @db2_safe
    def delete_record(self, ID: str) -> ResponseCode:
        '''
        Deletes a record with the given primary key

        Args:
            ID (str): the primary key value

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode with the deleted count
        '''
        self.__logger.debug(f"Deleting {self.__class__.__name__} record with ID {ID}.")

        primary_key = self._get_primary_key()
        query = f"DELETE FROM {self._table_name} WHERE {primary_key} = ?"

        cursor = self._execute_query(query, (ID,))

        # Commit the transaction
        self._connection.commit()

        self.__logger.debug(f"Delete completed for ID {ID}")
        return {"deleted_count": cursor.rowcount if cursor.rowcount else 0}

    @rbac_action("delete")
    # @db2_safe
    def delete_record_by_field(self, filter: dict[str, Any]) -> ResponseCode:
        '''
        Deletes records matching the given filter

        Args:
            filter (dict[str, Any]): a dictionary with column name and value to match for deletion

        Returns:
            ResponseCode (ResponseCode): After being wrapped, it will return a ResponseCode with the deleted count
        '''
        if not filter:
            return ResponseCode("MalformedContent", "Delete filter must not be empty.")
        if len(filter) > 1:
            return ResponseCode("MalformedContent", "Delete filter must contain only one field.")

        self.__logger.debug(f"Deleting {self.__class__.__name__} records by filter {filter}.")

        # Build WHERE clause
        col = list(filter.keys())[0]
        val = list(filter.values())[0]

        query = f"DELETE FROM {self._table_name} WHERE {col} = ?"

        cursor = self._execute_query(query, (val,))

        # Commit the transaction
        self._connection.commit()

        self.__logger.debug(f"Delete completed for filter {filter}")
        return {"deleted_count": cursor.rowcount if cursor.rowcount else 0}
