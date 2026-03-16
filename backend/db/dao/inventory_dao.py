# Copyright (C) 2025 Team White
# Licensed under the MIT License
# See LICENSE for more details
"""Data Access Object for the USER18.INVENTORY DB2 table."""

from typing import Any, Dict, List
import ibm_db_dbi
from backend.db.dao.abstract_record import DatabaseAccessObject, db2_safe, rbac_action
from backend.utilities.error_handler import ResponseCode


class InventoryDAO(DatabaseAccessObject):
    '''
    Data Access Object for the INVENTORY table in DB2.
    Provides database operations for inventory records.
    '''

    def __init__(self, connection: ibm_db_dbi.Connection):
        '''
        Initialize the InventoryDAO with the INVENTORY table.
        
        Args:
            connection (ibm_db_dbi.Connection): The DB2 connection object
        '''
        super().__init__("USER18.INVENTORY", connection)

    def _get_primary_key(self) -> str:
        '''
        Returns the primary key column name for the INVENTORY table.
        
        Returns:
            str: The name of the primary key column
        '''
        return "INVENTORY_ID"

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

    @rbac_action("read")
    @db2_safe
    def get_item_by_baseinfo(self, item_id: str):
        '''
        Retrieves inventory item details by BASEINFO identifier.

        Fetches NAME, DESCRIPTION, FORMAT, POTENCY, REUSABLE, CATEGORY, PRICE,
        and AMOUNT for the matching record.

        Args:
            item_id (str): The BASEINFO value to look up.

        Returns:
            ResponseCode: A ResponseCode wrapping a dict of the matching row,
                          or a ResourceNotFound ResponseCode if no record exists.
        '''
        select_stmt = (
            f"SELECT NAME, DESCRIPTION, FORMAT, POTENCY, REUSABLE, CATEGORY, PRICE, AMOUNT"
            f" FROM {self._table_name} WHERE BASEINFO = ?"
        )
        cursor = self._execute_query(select_stmt, (item_id,))
        row = cursor.fetchone()

        if row is None:
            return ResponseCode(error_tag="ResourceNotFound")

        columns = [desc[0] for desc in cursor.description]
        return self._dict_from_row(row, columns)
