"""Data Access Object for the USER18.ORDER DB2 table."""

from typing import Any, Dict, List
import ibm_db_dbi  # type: ignore[import-untyped]
from db.dao.abstract_record import DatabaseAccessObject
from api.models.purchase import PurchaseRequest


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
        super().__init__("USER12.INVORDER", connection)

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
        return dict(zip(columns, row))

    # Custom methods specific to Order operations can be added here
    # For example:
    # def get_orders_by_customer(self, customer_id: str):
    #     '''Gets all orders for a specific customer.'''
    #     return self.get_by_fields({"CUSTOMERID": customer_id})
    #
    # def get_orders_by_status(self, status: str):
    #     '''Gets all orders with a specific status.'''
    #     return self.get_by_fields({"ORDER_STATUS": status})

    def insert_order(self, entry: Dict[str, Any]) -> bool:
        # Check that user isn't ordering more of the item than exists

        count_stmt = f"SELECT COUNT(*) FROM {self._table_name}"
        cursor = self._execute_query(count_stmt)
        count = cursor.fetchall()[0][0]
        count+=1 # Increment to get new CCID
        
        ins_stmt = f"INSERT INTO {self._table_name} (ORDERID, PURCHASE_TIME, DELIVERY_EST, ITEMID, AMOUNT, TRANSACTION, CCID, CUSTOMERID, ADDRESSID) VALUES (?,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,?,?,?,?,?,?)"
        ins_paras = [count, entry["itemid"], entry["qty"], entry["transaction"], entry["customerid"], entry["addressid"], entry["ccid"]]
        cursor = self._execute_query(ins_stmt, tuple(ins_paras))

        # Check that the insert was successful
        select_new_stmt = (f"SELECT * FROM {self._table_name} WHERE ORDERID = ?")
        cursor = self._execute_query(select_new_stmt, (count,))
        rows = cursor.fetchall()
        if len(rows) == 0:
            return False
        else:
            return True