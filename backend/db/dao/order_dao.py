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
        from db.dao.inventory_dao import InventoryDAO
        from db.connector import conn
        invdao = InventoryDAO(conn)
        amt = invdao.get_amount_by_itemid(entry["itemid"])
        if amt < entry["qty"] or entry["qty"] < 1:
            print(f"FAILED: qty={entry['qty']}")
            return False

        count_stmt = f"SELECT COUNT(*) FROM {self._table_name}"
        cursor = self._execute_query(count_stmt)
        count = cursor.fetchall()[0][0]
        count+=1 # Increment to get new CCID
        
        ins_stmt = f"INSERT INTO {self._table_name} (ORDERID, PURCHASE_TIME, DELIVERY_EST, ITEMID, AMOUNT, TRANSACTION, CCID, CUSTOMERID, ADDRESSID) VALUES (?,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,?,?,?,?,?,?)"
        ins_paras = [count, entry["itemid"], entry["qty"], entry["transaction"], entry["ccid"], entry["customerid"], entry["addressid"]]
        cursor = self._execute_query(ins_stmt, tuple(ins_paras))

        # Check that the insert was successful
        select_new_stmt = (f"SELECT * FROM {self._table_name} WHERE ORDERID = ?")
        cursor = self._execute_query(select_new_stmt, (count,))
        rows = cursor.fetchall()
        if len(rows) == 0:
            return False
        
        # Decrement inventory amount
        new_amt = amt - entry["qty"]
        return_amt = invdao.decrement_amount(entry["itemid"], new_amt)
        if return_amt == new_amt:
            return True
        else:
            return False
        
    def get_history(self, customerid: int) -> List[Any]:
        select_stmt = (
            f"SELECT INVENTORY.ITEMID, INVENTORY.NAME, INVENTORY.DESCRIPTION, "
            f"    INVENTORY.FORMAT, INVENTORY.POTENCY, "
            f"    INVENTORY.REUSABLE, INVENTORY.CATEGORY, "
            f"    INVORDER.AMOUNT, INVORDER.TRANSACTION, "
            f"    INVORDER.PURCHASE_TIME, INVORDER.DELIVERY_EST, "
            f"    BASEPRICE.IMAGELINK "
            f"FROM USER12.INVORDER "
            f"INNER JOIN USER12.INVENTORY "
            f"ON INVORDER.ITEMID = INVENTORY.ITEMID "
            f"INNER JOIN USER12.BASEPRICE "
            f"ON INVENTORY.BASEINFO = BASEPRICE.PRICEID "
            f"WHERE INVORDER.CUSTOMERID = ? "
        )
        cursor = self._execute_query(select_stmt, (customerid,))
        rows = cursor.fetchall()
        return rows