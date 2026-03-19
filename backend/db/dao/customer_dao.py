# Copyright (C) 2025 Team White
# Licensed under the MIT License
# See LICENSE for more details
"""Data Access Object for the USER18.CUSTOMER DB2 table."""

from typing import Any, Dict, List
import ibm_db_dbi
from db.dao.abstract_record import DatabaseAccessObject


class CustomerDAO(DatabaseAccessObject):
    '''
    Data Access Object for the CUSTOMER table in DB2.
    Provides database operations for customer records.
    '''

    def __init__(self, connection: ibm_db_dbi.Connection):
        '''
        Initialize the CustomerDAO with the CUSTOMER table.
        
        Args:
            connection (ibm_db_dbi.Connection): The DB2 connection object
        '''
        super().__init__("USER12.CUSTOMER", connection)

    def _get_primary_key(self) -> str:
        '''
        Returns the primary key column name for the CUSTOMER table.
        
        Returns:
            str: The name of the primary key column
        '''
        return "CUSTOMERID"

    def _dict_from_row(self, row: tuple, columns: List[str]) -> Dict[str, Any]:
        '''
        Converts a database row tuple into a dictionary.
        
        Args:
            row (tuple): The database row as a tuple
            columns (List[str]): List of column names corresponding to the row values
            
        Returns:
            Dict[str, Any]: Dictionary representation of the database row
        '''
        return dict(zip(columns, row))

    # Custom methods specific to Customer operations can be added here
    # For example:
    # def get_customer_by_email(self, email: str):
    #     '''Gets a customer by their email address.'''
    #     return self.get_by_fields({"EMAIL": email})

    def get_user_by_name(self, username: str) -> List[Any]:

        select_stmt = (
            f"SELECT USERID, PASSWORD"
            f" FROM {self._table_name} WHERE EMAIL = ?"
        )
        
    #### SPENCERS CODE ##### vvvvvvvvvvv    
    def get_customer_by_email_and_password(self, email: str, password: str) -> tuple:
        '''
        Gets a customer by their email and password.
        
        Args:
            email (str): The customer's email address
            password (str): The customer's password
            
        Returns:
            tuple: Customer record if found, None if not found
        '''
        select_stmt = (
            f"SELECT CUSTOMERID FROM {self._table_name} "
            f"WHERE EMAIL = ? AND PASSWORD = ?"
        )
        
        cursor = self._connection.cursor()
        cursor.execute(select_stmt, (email, password))
        result = cursor.fetchone()
        cursor.close()
        
        return result