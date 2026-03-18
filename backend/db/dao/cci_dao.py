"""Data Access Object for the USER18.CCI (Credit Card Information) DB2 table."""

from typing import Any, Dict, List
from utilities.error_handler import ResponseCode
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
        super().__init__("USER12.CCI", connection)

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
    
    def get_records_by_customerid(self, customer_id: int) -> List[Any]:
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
            f"SELECT NUMBER, SECURITY_CODE, EXPIRATION, PROCESSOR, FIRST_NAME, LAST_NAME, ADDRESS, ADDR_2, CITY, STATE, COUNTRY, ZIP"
            f" FROM {self._table_name} WHERE CUSTOMERID = ?"
        )
        cursor = self._execute_query(select_stmt, (customer_id,))
        rows = cursor.fetchall()

        # if row is None:
        #     return ResponseCode(error_tag="ResourceNotFound")

        # columns = [desc[0] for desc in cursor.description]
        # return self._dict_from_row(row, columns)
        return rows

    # def create_record(self, entry: Dict[str, Any]) -> Dict[str, Any]:
    #     columns = list(entry.keys())
    #     placeholders = ", ".join(["?" for _ in columns])
    #     column_names = ", ".join(columns)
    #     query = f"INSERT INTO {self._table_name} ()"

    # Custom methods specific to CCI operations can be added here
    # For example:
    # def get_cci_by_customer(self, customer_id: str):
    #     '''Gets credit card information for a specific customer.'''
    #     return self.get_by_fields({"CUSTOMERID": customer_id})

    # def compare_records(self, entry1:List[Any], entry2:List[Any]) -> bool:
    #     if entry1 = entry2:

    def insert_cc(self, entry:List[Any]) -> List[Any]:
        select_stmt = (
            f"SELECT * FROM {self._table_name} "
            f"WHERE NUMBER = ? AND SECURITY_CODE = ? AND EXPIRATION = ? "
            f"AND   PROCESSOR = ? AND FIRST_NAME = ? AND LAST_NAME = ? "
            f"AND   ADDRESS = ? AND ADDR_2 = ? AND CITY = ? AND STATE = ? "
            f"AND   COUNTRY = ? AND ZIP = ? AND CUSTOMERID = ?"
        )
        cursor = self._execute_query(select_stmt, tuple(entry))
        rows = cursor.fetchall()

        if len(rows) == 0:
            count_stmt = f"SELECT COUNT(*) FROM {self._table_name}"
            cursor = self._execute_query(count_stmt)
            count = cursor.fetchall()[0][0]
            count+=1 # Increment to get new CCID
            
            ins_stmt = f"INSERT INTO {self._table_name} (CCID, NUMBER, SECURITY_CODE, EXPIRATION, PROCESSOR, FIRST_NAME, LAST_NAME, ADDRESS, ADDR_2, CITY, STATE, COUNTRY, ZIP, CUSTOMERID) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            ins_paras = [count] + entry
            cursor = self._execute_query(ins_stmt, tuple(ins_paras))

            select_new_stmt = (f"SELECT * FROM {self._table_name} WHERE CCID = ?")
            cursor = self._execute_query(select_new_stmt, (count,))
            rows = cursor.fetchall()

        return rows