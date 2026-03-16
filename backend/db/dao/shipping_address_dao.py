# Copyright (C) 2025 Team White
# Licensed under the MIT License
# See LICENSE for more details
"""Data Access Object for the USER18.BILLING_ADDRESS DB2 table."""

from typing import Any, Dict, List
import ibm_db_dbi
from backend.db.dao.abstract_record import DatabaseAccessObject


class ShippingAddressDAO(DatabaseAccessObject):
    '''
    Data Access Object for the SHIPPINGADDRESS table in DB2.
    Provides database operations for billing address records.
    '''

    def __init__(self, connection: ibm_db_dbi.Connection):
        '''
        Initialize the ShippingAddressDAO with the SHIPPINGADDRESS table.

        Args:
            connection (ibm_db_dbi.Connection): The DB2 connection object
        '''
        super().__init__("USER18.SHIPPINGADDRESS", connection)

    def _get_primary_key(self) -> str:
        '''
        Returns the primary key column name for the SHIPPINGADDRESS table.

        Returns:
            str: The name of the primary key column
        '''
        return "BILL_ADDY_ID"

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

    # Custom methods specific to Shipping Address operations can be added here
    # For example:
    # def get_address_by_customer(self, customer_id: str):
    #     '''Gets all billing addresses for a specific customer.'''
    #     return self.get_by_fields({"CUSTOMERID": customer_id})