# Copyright (C) 2025 Team White
# Licensed under the MIT License
# See LICENSE for more details

from typing import Any, Dict, List
import ibm_db_dbi
from backend.db.dao.abstract_record import DatabaseAccessObject


class OrderDAO(DatabaseAccessObject):
    '''
    Data Access Object for the ORDER table in DB2.
    Provides database operations for order records.
    '''

    def __init__(self, connection: ibm_db_dbi.Connection):
        '''
        Initialize the OrderDAO with the ORDER table.
        
        Args:
            connection (ibm_db_dbi.Connection): The DB2 connection object
        '''
        super().__init__("USER18.ORDER", connection)

    def _get_primary_key(self) -> str:
        '''
        Returns the primary key column name for the ORDER table.
        
        Returns:
            str: The name of the primary key column
        '''
        return "ORDER_ID"

    def _dict_from_row(self, row: tuple, columns: List[str]) -> Dict[str, Any]:
        '''
        Converts a database row tuple into a dictionary.
        
        Args:
            row (tuple): The database row as a tuple
            columns (List[str]): List of column names corresponding to the row values
            
        Returns:
            Dict[str, Any]: Dictionary representation of the database row
        '''
        return {col: val for col, val in zip(columns, row)}

    # Custom methods specific to Order operations can be added here
    # For example:
    # def get_orders_by_customer(self, customer_id: str):
    #     '''Gets all orders for a specific customer.'''
    #     return self.get_by_fields({"CUSTOMERID": customer_id})
    #
    # def get_orders_by_status(self, status: str):
    #     '''Gets all orders with a specific status.'''
    #     return self.get_by_fields({"ORDER_STATUS": status})
