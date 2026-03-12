# Copyright (C) 2025 Team White
# Licensed under the MIT License
# See LICENSE for more details

import ibm_db
import ibm_db_dbi
from abc import ABC
from typing import Any, Callable, Optional, List, Dict
from functools import wraps
from backend.utilities.error_handler import (
    ResponseCode, 
    DB2ErrorHandler, 
    ErrorSeverity,
    success_response,
    not_found_error,
    malformed_content_error
)


def db2_safe(func):
    '''
    Wraps a function to ensure that a ResponseCode is always returned and that the result of a given
    function is added to data. Specifically handles DB2 and SQL exceptions.

    Args:
        func (Any): base function to be wrapped

    Returns:
        wrapper (function): a wrapper that will return a ResponseCode with the error or result of the passed
        in function
    '''
    @wraps(func)
    def wrapper(*args, **kwargs) -> ResponseCode:
        try:
            result = func(*args, **kwargs)
            if isinstance(result, ResponseCode):
                return result  #Don't wrap again
            return ResponseCode(error_tag=None, data=result)
        except Exception as e:
            # Use DB2ErrorHandler to categorize the exception
            return DB2ErrorHandler.parse_exception(e)
    return wrapper

class DatabaseAccessObject(ABC):
    '''
    This class is an abstract class that all DAO objects extend from to access their corresponding DB2 tables.
    Each extension can define a custom ROLE_MATRIX for role-based access control.
    
    Subclasses must implement:
        - _get_primary_key(): Returns the name of the primary key column
        - _dict_from_row(row, columns): Converts a database row to a dictionary
    '''

    def __init__(self, table_name: str, connection: ibm_db_dbi.Connection):
        '''
        Args:
            table_name (str): the name of the table that the DAO accesses
            connection (ibm_db_dbi.Connection): the DB2 connection object
        '''
        self._table_name = table_name
        self._connection = connection

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
            Any: The query cursor
        '''
        cursor = self._connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor

    #Hook method; this should set any default field values; just override it
    def _prepare_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        '''
        Hook method that can be overridden to set default field values for new records.

        Args:
            entry (dict[str, Any]): the entry to be processed

        Returns:
            entry (dict[str, Any]): the entry after processing (usually defining a default field)
        '''
        return entry  # Default: no changes

    @db2_safe
    def get_by_key(self, ID: str) -> ResponseCode:
        '''
        Return DB2 record by primary key

        Args:
            ID (str): the primary key value

        Returns:
            ResponseCode: ResponseCode with the record as a dictionary, or error if not found
        '''
        primary_key = self._get_primary_key()
        query = f"SELECT * FROM {self._table_name} WHERE {primary_key} = ?"
        
        cursor = self._execute_query(query, (ID,))
        row = cursor.fetchone()
        
        if row is None:
            return not_found_error(f"Record with {primary_key}={ID}")
        
        columns = [desc[0] for desc in cursor.description]
        return success_response(self._dict_from_row(row, columns))

    @db2_safe
    def get_by_fields(self, filter: dict[str, Any]) -> ResponseCode:
        '''
        Return DB2 records by given fields

        Args:
            filter (dict[str, Any]): a dictionary with column names as keys and values to match

        Returns:
            ResponseCode: ResponseCode with records as a list of dictionaries, or error if none found
        '''
        if not filter:
            return malformed_content_error("Filter must not be empty")
        
        # Build WHERE clause
        conditions = [f"{col} = ?" for col in filter.keys()]
        where_clause = " AND ".join(conditions)
        query = f"SELECT * FROM {self._table_name} WHERE {where_clause}"
        
        cursor = self._execute_query(query, tuple(filter.values()))
        rows = cursor.fetchall()
        
        if not rows:
            return not_found_error("No matching records")
        
        columns = [desc[0] for desc in cursor.description]
        return success_response([self._dict_from_row(row, columns) for row in rows])

    @db2_safe
    def get_all_records(self, limit: int = None) -> ResponseCode:
        '''
        Return all (or the first x) DB2 records from a table

        Args:
            limit (int optional): an integer that determines the number of records to return. By default, it is set to None and returns the entire set

        Returns:
            ResponseCode: ResponseCode with records from the table as a list of dictionaries, or error if none found
        '''
        query = f"SELECT * FROM {self._table_name}"
        if limit is not None:
            query += f" FETCH FIRST {limit} ROWS ONLY"
        
        cursor = self._execute_query(query)
        rows = cursor.fetchall()
        
        if not rows:
            return not_found_error("No records found")
        
        columns = [desc[0] for desc in cursor.description]
        return success_response([self._dict_from_row(row, columns) for row in rows])

    @db2_safe
    def get_random(self, numReturned: int = 1, filter: dict[str, Any] = None) -> ResponseCode:
        '''
        Return a set number of random records given an optional filter

        Args:
            numReturned (int optional): an integer that determines the number of records returned. Defaults to 1
            filter (dict[str, Any] optional): a dictionary with column names and values to filter

        Returns:
            ResponseCode: ResponseCode with records as a list of dictionaries, or error if none found
        '''
        filter = filter or {}
        
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
            return not_found_error("No matching records found")
        
        columns = [desc[0] for desc in cursor.description]
        return success_response([self._dict_from_row(row, columns) for row in rows])

    @db2_safe
    def get_short_record(self, numReturned: int, filter: dict[str, Any] = None, max_length: int = 80) -> ResponseCode:
        '''
        Return a set number of random records given an optional filter that also have a content 
        field less than the given max_length

        Args:
            numReturned (int): an integer that determines the number of records returned
            filter (dict[str, Any] optional): a dictionary with column names and values to filter
            max_length (int optional): an integer that determines the max length of the content field. Defaults to 80

        Returns:
            ResponseCode: ResponseCode with records as a list of dictionaries, or error if none found
        '''
        filter = filter or {}
        
        # Build WHERE clause with both filter and length condition
        conditions = []
        params = []
        
        if filter:
            for col, val in filter.items():
                conditions.append(f"{col} = ?")
                params.append(val)
        
        # Add length condition for content field
        conditions.append(f"LENGTH(CONTENT) < ?")
        params.append(max_length)
        
        where_clause = " WHERE " + " AND ".join(conditions)
        
        # DB2 query with random ordering and length filter
        query = f"SELECT * FROM {self._table_name}{where_clause} ORDER BY RAND() FETCH FIRST {numReturned} ROWS ONLY"
        
        cursor = self._execute_query(query, tuple(params))
        rows = cursor.fetchall()
        
        if not rows:
            return not_found_error("No matching records found")
        
        columns = [desc[0] for desc in cursor.description]
        return success_response([self._dict_from_row(row, columns) for row in rows])

    @db2_safe
    def update_record(self, ID: str, updates: dict[str, Any]) -> ResponseCode:
        '''
        Updates a record with the given ID and updates

        Args:
            ID (str): the primary key value
            updates (dict[str, Any]): a dictionary with column names and new values

        Returns:
            ResponseCode: ResponseCode indicating success or error
        '''
        if not updates:
            return malformed_content_error("Update payload must not be empty")
        
        primary_key = self._get_primary_key()
        
        # Build SET clause
        set_clauses = [f"{col} = ?" for col in updates.keys()]
        set_clause = ", ".join(set_clauses)
        
        # Build query with primary key as WHERE condition
        query = f"UPDATE {self._table_name} SET {set_clause} WHERE {primary_key} = ?"
        
        # Combine update values with ID for the WHERE clause
        params = tuple(list(updates.values()) + [ID])
        
        cursor = self._execute_query(query, params)
        
        # Commit the transaction
        self._connection.commit()
        
        return success_response({"updated_id": ID})

    @db2_safe
    def create_record(self, entry: dict[str, Any]) -> ResponseCode:
        '''
        Creates a record with the entry data given

        Args:
            entry (dict[str, Any]): a dictionary of columns and values to insert

        Returns:
            ResponseCode: ResponseCode indicating success with the created record
        '''
        entry = self._prepare_entry(entry)  # Determines if there should be default field values; override in subclass
        
        # Build INSERT statement
        columns = list(entry.keys())
        placeholders = ", ".join(["?" for _ in columns])
        column_names = ", ".join(columns)
        
        query = f"INSERT INTO {self._table_name} ({column_names}) VALUES ({placeholders})"
        
        cursor = self._execute_query(query, tuple(entry.values()))
        
        # Commit the transaction
        self._connection.commit()
        
        return success_response(entry)

    @db2_safe
    def delete_record(self, ID: str) -> ResponseCode:
        '''
        Deletes a record with the given primary key

        Args:
            ID (str): the primary key value

        Returns:
            ResponseCode: ResponseCode indicating success or error
        '''
        primary_key = self._get_primary_key()
        query = f"DELETE FROM {self._table_name} WHERE {primary_key} = ?"
        
        cursor = self._execute_query(query, (ID,))
        
        # Commit the transaction
        self._connection.commit()
        
        return success_response({"deleted_id": ID})

    @db2_safe
    def delete_record_by_field(self, filter: dict[str, Any]) -> ResponseCode:
        '''
        Deletes records matching the given filter

        Args:
            filter (dict[str, Any]): a dictionary with column name and value to match for deletion

        Returns:
            ResponseCode: ResponseCode indicating success with deleted count
        '''
        if not filter:
            return malformed_content_error("Delete filter must not be empty")
        if len(filter) > 1:
            return malformed_content_error("Delete filter must contain only one field")
        
        # Build WHERE clause
        col = list(filter.keys())[0]
        val = list(filter.values())[0]
        
        query = f"DELETE FROM {self._table_name} WHERE {col} = ?"
        
        cursor = self._execute_query(query, (val,))
        
        # Commit the transaction
        self._connection.commit()
        
        return success_response({"deleted_count": cursor.rowcount if cursor.rowcount else 0})