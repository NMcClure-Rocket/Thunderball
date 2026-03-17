"""Data Access Object for the USER18.CCI (Credit Card Information) DB2 table."""

from typing import Any, Dict, List
import ibm_db_dbi  # type: ignore[import-untyped]
from db.dao.abstract_record import DatabaseAccessObject


class CCIDao(DatabaseAccessObject):
    '''
    Data Access Object for the CCI (Credit Card Information) table in DB2.
    Provides database operations for credit card records.
    '''

    def __init__(self, connection: ibm_db_dbi.Connection):
        '''
        Initialize the CCIDao with the CCI table.

        Args:
            connection (ibm_db_dbi.Connection): The DB2 connection object
        '''
        super().__init__("USER18.CCI", connection)

    def _get_primary_key(self) -> str:
        '''
        Returns the primary key column name for the CCI table.

        Returns:
            str: The name of the primary key column
        '''
        return "CCI_ID"

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

    # Custom methods specific to CCI operations can be added here
    # For example:
    # def get_cci_by_customer(self, customer_id: str):
    #     '''Gets credit card information for a specific customer.'''
    #     return self.get_by_fields({"CUSTOMERID": customer_id})
