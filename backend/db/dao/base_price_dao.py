# Copyright (C) 2025 Team White
# Licensed under the MIT License
# See LICENSE for more details
"""Data Access Object for the USER18.BASE_PRICE DB2 table."""

from typing import Any, Dict, List
import ibm_db_dbi
from backend.db.dao.abstract_record import DatabaseAccessObject


class BasePriceDAO(DatabaseAccessObject):
    '''
    Data Access Object for the BASEPRICE table in DB2.
    Provides database operations for base price records.
    '''

    def __init__(self, connection: ibm_db_dbi.Connection):
        '''
        Initialize the BasePriceDAO with the BASEPRICE table.
        
        Args:
            connection (ibm_db_dbi.Connection): The DB2 connection object
        '''
        super().__init__("USER18.BASEPRICE", connection)

    def _get_primary_key(self) -> str:
        '''
        Returns the primary key column name for the BASEPRICE table.
        
        Returns:
            str: The name of the primary key column
        '''
        return "PRICE_ID"

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

    # Custom methods specific to BasPrice operations can be added here
    # For example:
    # def get_price_by_item(self, item_id: str):
    #     '''Gets the base price for a specific item.'''
    #     return self.get_by_fields({"ITEM_ID": item_id})
