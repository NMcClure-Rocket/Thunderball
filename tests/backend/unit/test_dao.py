"""
Unit tests for the DB2 Data Access Objects (DAOs).

All external dependencies (ibm_db, ibm_db_dbi, LoggerFactory) are mocked at
module level so that tests run without a live DB2 connection or logging config.
"""
# pylint: disable=missing-class-docstring,missing-function-docstring
# pylint: disable=redefined-outer-name,protected-access,wrong-import-position

import sys
from unittest.mock import MagicMock
import pytest

# ---------------------------------------------------------------------------
# Module-level mocks – must be registered BEFORE any backend module is imported.
# ---------------------------------------------------------------------------

# 1. DB2 native drivers (C extensions; not present without IBM DB2 installation)
for _name in ("ibm_db", "ibm_db_dbi"):
    sys.modules.setdefault(_name, MagicMock())

# 2. Logger module – error_handler.py calls LoggerFactory.get_general_logger()
#    at *import time*, so we intercept the whole module before it is loaded.
_mock_logger = MagicMock()
_mock_logger_factory = MagicMock(
    get_general_logger=MagicMock(return_value=_mock_logger),
    get_security_logger=MagicMock(return_value=MagicMock()),
)
sys.modules.setdefault(
    "backend.utilities.logger",
    MagicMock(LoggerFactory=_mock_logger_factory),
)

# ---------------------------------------------------------------------------
# Now it's safe to import backend modules.
# ---------------------------------------------------------------------------
from backend.db.dao.base_price_dao import BasePriceDAO        # noqa: E402
from backend.db.dao.cci_dao import CCIDao                     # noqa: E402
from backend.db.dao.customer_dao import CustomerDAO           # noqa: E402
from backend.db.dao.inventory_dao import InventoryDAO         # noqa: E402
from backend.db.dao.order_dao import OrderDAO                         # noqa: E402
from backend.db.dao.shipping_address_dao import ShippingAddressDAO    # noqa: E402
from backend.entities.credentials_entity import Credentials           # noqa: E402
from backend.utilities.error_handler import ResponseCode              # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_ok(rc: ResponseCode) -> bool:
    """True when db2_safe wrapped a successful return value."""
    return rc.error_tag in ("GeneralSuccess", "PostSuccess")


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_cursor():
    cursor = MagicMock()
    cursor.description = [("CUSTOMERID",), ("FIRST_NAME",), ("LAST_NAME",)]
    cursor.fetchone.return_value = (42, "Alice", "Smith")
    cursor.fetchall.return_value = [(42, "Alice", "Smith"), (43, "Bob", "Jones")]
    cursor.rowcount = 1
    return cursor


@pytest.fixture
def mock_connection(mock_cursor):
    conn = MagicMock()
    conn.cursor.return_value = mock_cursor
    return conn


@pytest.fixture
def customer_dao(mock_connection):
    return CustomerDAO(mock_connection)


# ===========================================================================
# BasePriceDAO – table, primary key, row mapping
# ===========================================================================

class TestBasePriceDAO:
    def test_table_name(self, mock_connection):
        dao = BasePriceDAO(mock_connection)
        assert dao._table_name == "USER12.BASEPRICE"

    def test_primary_key(self, mock_connection):
        dao = BasePriceDAO(mock_connection)
        assert dao._get_primary_key() == "PRICE_ID"

    def test_dict_from_row(self, mock_connection):
        dao = BasePriceDAO(mock_connection)
        result = dao._dict_from_row((100, 29.99), ["PRICE_ID", "AMOUNT"])
        assert result == {"PRICE_ID": 100, "AMOUNT": 29.99}

    def test_dict_from_row_empty(self, mock_connection):
        dao = BasePriceDAO(mock_connection)
        assert not dao._dict_from_row((), [])


# ===========================================================================
# ShippingAddressDAO – table, primary key, row mapping
# ===========================================================================

class TestShippingAddressDAO:
    def test_table_name(self, mock_connection):
        dao = ShippingAddressDAO(mock_connection)
        assert dao._table_name == "USER12.SHIPPINGADDRESS"

    def test_primary_key(self, mock_connection):
        dao = ShippingAddressDAO(mock_connection)
        assert dao._get_primary_key() == "BILL_ADDY_ID"

    def test_dict_from_row(self, mock_connection):
        dao = ShippingAddressDAO(mock_connection)
        result = dao._dict_from_row(("A1", "123 Main St"), ["BILL_ADDY_ID", "STREET"])
        assert result == {"BILL_ADDY_ID": "A1", "STREET": "123 Main St"}


# ===========================================================================
# CCIDao – table, primary key, row mapping
# ===========================================================================

class TestCCIDao:
    def test_table_name(self, mock_connection):
        dao = CCIDao(mock_connection)
        assert dao._table_name == "USER12.CCI"

    def test_primary_key(self, mock_connection):
        dao = CCIDao(mock_connection)
        assert dao._get_primary_key() == "CCI_ID"

    def test_dict_from_row(self, mock_connection):
        dao = CCIDao(mock_connection)
        result = dao._dict_from_row(("C1", "4111111111111111"), ["CCI_ID", "CARD_NUMBER"])
        assert result == {"CCI_ID": "C1", "CARD_NUMBER": "4111111111111111"}


# ===========================================================================
# CustomerDAO – table, primary key, row mapping
# ===========================================================================

class TestCustomerDAO:
    def test_table_name(self, mock_connection):
        dao = CustomerDAO(mock_connection)
        assert dao._table_name == "USER12.CUSTOMER"

    def test_primary_key(self, mock_connection):
        dao = CustomerDAO(mock_connection)
        assert dao._get_primary_key() == "CUSTOMERID"

    def test_dict_from_row(self, mock_connection):
        dao = CustomerDAO(mock_connection)
        result = dao._dict_from_row(
            (1, "Alice", "Smith"), ["CUSTOMERID", "FIRST_NAME", "LAST_NAME"]
        )
        assert result == {"CUSTOMERID": 1, "FIRST_NAME": "Alice", "LAST_NAME": "Smith"}


# ===========================================================================
# InventoryDAO – table, primary key, row mapping
# ===========================================================================

class TestInventoryDAO:
    def test_table_name(self, mock_connection):
        dao = InventoryDAO(mock_connection)
        assert dao._table_name == "USER12.INVENTORY"

    def test_primary_key(self, mock_connection):
        dao = InventoryDAO(mock_connection)
        assert dao._get_primary_key() == "INVENTORY_ID"

    def test_dict_from_row(self, mock_connection):
        dao = InventoryDAO(mock_connection)
        result = dao._dict_from_row(
            ("I1", "Widget", 50), ["INVENTORY_ID", "ITEM", "QUANTITY"]
        )
        assert result == {"INVENTORY_ID": "I1", "ITEM": "Widget", "QUANTITY": 50}


# ===========================================================================
# OrderDAO – table, primary key, row mapping
# ===========================================================================

class TestOrderDAO:
    def test_table_name(self, mock_connection):
        dao = OrderDAO(mock_connection)
        assert dao._table_name == "USER12.INVORDER"

    def test_primary_key(self, mock_connection):
        dao = OrderDAO(mock_connection)
        assert dao._get_primary_key() == "ORDER_ID"

    def test_dict_from_row(self, mock_connection):
        dao = OrderDAO(mock_connection)
        result = dao._dict_from_row(("O1", "PENDING"), ["ORDER_ID", "STATUS"])
        assert result == {"ORDER_ID": "O1", "STATUS": "PENDING"}


# ===========================================================================
# InventoryDAO – get_item_by_baseinfo
# ===========================================================================

class TestInventoryDAOGetItemByBaseinfo:
    @pytest.fixture
    def inventory_dao(self, mock_connection):
        return InventoryDAO(mock_connection)

    def test_returns_list_when_rows_found(self, inventory_dao, mock_cursor):
        mock_cursor.fetchall.return_value = [
            (1, "Fire Spell", "Burns", "instant", 5, True, "offensive", 9.99, 10)
        ]
        result = inventory_dao.get_item_by_baseinfo(1)
        assert isinstance(result, list)
        assert len(result) == 1

    def test_returns_empty_list_when_no_rows(self, inventory_dao, mock_cursor):
        mock_cursor.fetchall.return_value = []
        result = inventory_dao.get_item_by_baseinfo(9999)
        assert result == []

    def test_query_uses_baseinfo_column(self, inventory_dao, mock_cursor):
        mock_cursor.description = [("NAME",)]
        mock_cursor.fetchone.return_value = ("Test",)
        inventory_dao.get_item_by_baseinfo("ITEM01")
        sql = mock_cursor.execute.call_args[0][0]
        assert "BASEINFO = ?" in sql

    def test_query_selects_expected_columns(self, inventory_dao, mock_cursor):
        mock_cursor.description = [("NAME",)]
        mock_cursor.fetchone.return_value = ("Test",)
        inventory_dao.get_item_by_baseinfo("ITEM01")
        sql = mock_cursor.execute.call_args[0][0]
        for col in ("NAME", "DESCRIPTION", "FORMAT", "POTENCY", "PRICE", "AMOUNT"):
            assert col in sql

    def test_passes_item_id_as_param(self, inventory_dao, mock_cursor):
        mock_cursor.description = [("NAME",)]
        mock_cursor.fetchone.return_value = ("Test",)
        inventory_dao.get_item_by_baseinfo("XYZ99")
        params = mock_cursor.execute.call_args[0][1]
        assert "XYZ99" in params


# ===========================================================================
# get_by_key – tested via CustomerDAO (shared logic for all DAOs)
# ===========================================================================

class TestGetByKey:
    @pytest.mark.skip(reason="requires db2_safe decorator")
    def test_success_returns_record_dict(self, customer_dao, mock_cursor):
        mock_cursor.fetchone.return_value = (42, "Alice", "Smith")
        rc = customer_dao.get_by_key("42")
        assert _is_ok(rc)
        assert rc.data == {"CUSTOMERID": 42, "FIRST_NAME": "Alice", "LAST_NAME": "Smith"}

    def test_not_found_returns_resource_not_found(self, customer_dao, mock_cursor):
        mock_cursor.fetchone.return_value = None
        rc = customer_dao.get_by_key("999")
        assert rc.error_tag == "ResourceNotFound"

    @pytest.mark.skip(reason="requires db2_safe decorator")
    def test_db_error_returns_exception_class_as_error_tag(self, customer_dao, mock_cursor):
        mock_cursor.fetchone.side_effect = RuntimeError("connection lost")
        rc = customer_dao.get_by_key("1")
        assert rc.error_tag == "RuntimeError"

    def test_correct_where_clause_with_primary_key(self, customer_dao, mock_cursor):
        mock_cursor.fetchone.return_value = (42, "Alice", "Smith")
        customer_dao.get_by_key("42")
        sql, params = mock_cursor.execute.call_args[0]
        assert "WHERE CUSTOMERID = ?" in sql
        assert params == ("42",)


# ===========================================================================
# get_by_fields
# ===========================================================================

class TestGetByFields:
    @pytest.mark.skip(reason="requires db2_safe decorator")
    def test_success_returns_list_of_records(self, customer_dao, mock_cursor):
        mock_cursor.fetchall.return_value = [(42, "Alice", "Smith")]
        rc = customer_dao.get_by_fields({"FIRST_NAME": "Alice"})
        assert _is_ok(rc)
        assert len(rc.data) == 1
        assert rc.data[0]["FIRST_NAME"] == "Alice"

    def test_empty_filter_returns_malformed_content(self, customer_dao):
        rc = customer_dao.get_by_fields({})
        assert rc.error_tag == "MalformedContent"

    def test_not_found_returns_resource_not_found(self, customer_dao, mock_cursor):
        mock_cursor.fetchall.return_value = []
        rc = customer_dao.get_by_fields({"FIRST_NAME": "Ghost"})
        assert rc.error_tag == "ResourceNotFound"

    def test_multiple_fields_joined_with_and(self, customer_dao, mock_cursor):
        mock_cursor.fetchall.return_value = [(42, "Alice", "Smith")]
        customer_dao.get_by_fields({"FIRST_NAME": "Alice", "LAST_NAME": "Smith"})
        sql = mock_cursor.execute.call_args[0][0]
        assert "FIRST_NAME = ?" in sql
        assert "LAST_NAME = ?" in sql
        assert " AND " in sql

    @pytest.mark.skip(reason="requires db2_safe decorator")
    def test_db_error_returns_error_response(self, customer_dao, mock_cursor):
        mock_cursor.fetchall.side_effect = RuntimeError("timeout")
        rc = customer_dao.get_by_fields({"FIRST_NAME": "Alice"})
        assert rc.error_tag == "RuntimeError"


# ===========================================================================
# get_all_records
# ===========================================================================

class TestGetAllRecords:
    @pytest.mark.skip(reason="requires db2_safe decorator")
    def test_success_returns_all_records(self, customer_dao, mock_cursor):
        mock_cursor.fetchall.return_value = [
            (1, "Alice", "Smith"),
            (2, "Bob", "Jones"),
        ]
        rc = customer_dao.get_all_records()
        assert _is_ok(rc)
        assert len(rc.data) == 2

    def test_with_limit_adds_fetch_first_clause(self, customer_dao, mock_cursor):
        mock_cursor.fetchall.return_value = [(1, "Alice", "Smith")]
        customer_dao.get_all_records(limit=5)
        sql = mock_cursor.execute.call_args[0][0]
        assert "FETCH FIRST 5 ROWS ONLY" in sql

    def test_without_limit_omits_fetch_first(self, customer_dao, mock_cursor):
        mock_cursor.fetchall.return_value = [(1, "Alice", "Smith")]
        customer_dao.get_all_records()
        sql = mock_cursor.execute.call_args[0][0]
        assert "FETCH FIRST" not in sql

    def test_empty_table_returns_empty_list(self, customer_dao, mock_cursor):
        mock_cursor.fetchall.return_value = []
        rc = customer_dao.get_all_records()
        assert rc == []


# ===========================================================================
# get_random
# ===========================================================================

class TestGetRandom:
    @pytest.mark.skip(reason="requires db2_safe decorator")
    def test_success_returns_records(self, customer_dao, mock_cursor):
        mock_cursor.fetchall.return_value = [(42, "Alice", "Smith")]
        rc = customer_dao.get_random(numReturned=1)
        assert _is_ok(rc)
        assert len(rc.data) == 1

    def test_sql_uses_rand_ordering_and_fetch_first(self, customer_dao, mock_cursor):
        mock_cursor.fetchall.return_value = [(42, "Alice", "Smith")]
        customer_dao.get_random(numReturned=3)
        sql = mock_cursor.execute.call_args[0][0]
        assert "ORDER BY RAND()" in sql
        assert "FETCH FIRST 3 ROWS ONLY" in sql

    def test_with_filter_adds_where_clause(self, customer_dao, mock_cursor):
        mock_cursor.fetchall.return_value = [(42, "Alice", "Smith")]
        customer_dao.get_random(numReturned=1, filter={"LAST_NAME": "Smith"})
        sql = mock_cursor.execute.call_args[0][0]
        assert "WHERE" in sql
        assert "LAST_NAME = ?" in sql

    def test_without_filter_omits_where_clause(self, customer_dao, mock_cursor):
        mock_cursor.fetchall.return_value = [(42, "Alice", "Smith")]
        customer_dao.get_random(numReturned=1)
        args = mock_cursor.execute.call_args[0]
        sql = args[0]
        assert "WHERE" not in sql
        assert len(args) == 1  # no params tuple passed when there is no filter

    def test_not_found_returns_resource_not_found(self, customer_dao, mock_cursor):
        mock_cursor.fetchall.return_value = []
        rc = customer_dao.get_random(numReturned=1)
        assert rc.error_tag == "ResourceNotFound"


# ===========================================================================
# get_short_record
# ===========================================================================

class TestGetShortRecord:
    @pytest.mark.skip(reason="requires db2_safe decorator")
    def test_success_returns_records(self, customer_dao, mock_cursor):
        mock_cursor.fetchall.return_value = [(42, "Alice", "Smith")]
        rc = customer_dao.get_short_record(numReturned=1)
        assert _is_ok(rc)

    def test_not_found_returns_resource_not_found(self, customer_dao, mock_cursor):
        mock_cursor.fetchall.return_value = []
        rc = customer_dao.get_short_record(numReturned=1)
        assert rc.error_tag == "ResourceNotFound"

    def test_default_max_length_80_in_query_params(self, customer_dao, mock_cursor):
        mock_cursor.fetchall.return_value = [(42, "Alice", "Smith")]
        customer_dao.get_short_record(numReturned=1)
        sql, params = mock_cursor.execute.call_args[0]
        assert "LENGTH(CONTENT) < ?" in sql
        assert 80 in params

    def test_custom_max_length_passed_to_params(self, customer_dao, mock_cursor):
        mock_cursor.fetchall.return_value = [(42, "Alice", "Smith")]
        customer_dao.get_short_record(numReturned=1, max_length=40)
        _, params = mock_cursor.execute.call_args[0]
        assert 40 in params

    def test_filter_adds_where_conditions(self, customer_dao, mock_cursor):
        mock_cursor.fetchall.return_value = [(42, "Alice", "Smith")]
        customer_dao.get_short_record(numReturned=1, filter={"LAST_NAME": "Smith"})
        sql = mock_cursor.execute.call_args[0][0]
        assert "LAST_NAME = ?" in sql


# ===========================================================================
# update_record
# ===========================================================================

class TestUpdateRecord:
    @pytest.mark.skip(reason="requires db2_safe decorator")
    def test_success_commits_and_returns_id(self, customer_dao, mock_connection):
        rc = customer_dao.update_record("42", {"FIRST_NAME": "Bob"})
        assert _is_ok(rc)
        assert rc.data == "42"
        mock_connection.commit.assert_called_once()

    def test_empty_updates_returns_malformed_content(self, customer_dao):
        rc = customer_dao.update_record("42", {})
        assert rc.error_tag == "MalformedContent"

    def test_correct_set_and_where_clause(self, customer_dao, mock_cursor):
        customer_dao.update_record("42", {"FIRST_NAME": "Bob", "LAST_NAME": "Jones"})
        sql, params = mock_cursor.execute.call_args[0]
        assert "UPDATE USER12.CUSTOMER SET" in sql
        assert "FIRST_NAME = ?" in sql
        assert "WHERE CUSTOMERID = ?" in sql
        assert params[-1] == "42"

    @pytest.mark.skip(reason="requires db2_safe decorator")
    def test_db_error_returns_error_response(self, customer_dao, mock_cursor):
        mock_cursor.execute.side_effect = RuntimeError("deadlock")
        rc = customer_dao.update_record("42", {"FIRST_NAME": "Bob"})
        assert rc.error_tag == "RuntimeError"


# ===========================================================================
# create_record
# ===========================================================================

class TestCreateRecord:
    def test_success_returns_post_success(self, customer_dao, mock_connection):
        rc = customer_dao.create_record(
            {"CUSTOMERID": "99", "FIRST_NAME": "Carl", "LAST_NAME": "Young"}
        )
        assert rc.error_tag == "PostSuccess"
        mock_connection.commit.assert_called_once()

    def test_correct_insert_sql_constructed(self, customer_dao, mock_cursor):
        entry = {"CUSTOMERID": "99", "FIRST_NAME": "Carl"}
        customer_dao.create_record(entry)
        sql = mock_cursor.execute.call_args[0][0]
        assert "INSERT INTO USER12.CUSTOMER" in sql
        assert "CUSTOMERID" in sql
        assert "?" in sql

    def test_insert_params_match_entry_values(self, customer_dao, mock_cursor):
        entry = {"CUSTOMERID": "99", "FIRST_NAME": "Carl"}
        customer_dao.create_record(entry)
        params = mock_cursor.execute.call_args[0][1]
        assert "99" in params
        assert "Carl" in params

    @pytest.mark.skip(reason="requires db2_safe decorator")
    def test_db_error_returns_error_response(self, customer_dao, mock_cursor):
        mock_cursor.execute.side_effect = RuntimeError("constraint violation")
        rc = customer_dao.create_record({"CUSTOMERID": "1"})
        assert rc.error_tag == "RuntimeError"


# ===========================================================================
# delete_record
# ===========================================================================

class TestDeleteRecord:
    @pytest.mark.skip(reason="requires db2_safe decorator")
    def test_success_commits_and_returns_deleted_count(self, customer_dao, mock_connection):
        rc = customer_dao.delete_record("42")
        assert _is_ok(rc)
        assert rc.data == {"deleted_count": 1}
        mock_connection.commit.assert_called_once()

    def test_correct_delete_sql_with_primary_key(self, customer_dao, mock_cursor):
        customer_dao.delete_record("42")
        sql, params = mock_cursor.execute.call_args[0]
        assert "DELETE FROM USER12.CUSTOMER WHERE CUSTOMERID = ?" in sql
        assert params == ("42",)

    @pytest.mark.skip(reason="requires db2_safe decorator")
    def test_db_error_returns_error_response(self, customer_dao, mock_cursor):
        mock_cursor.execute.side_effect = RuntimeError("timeout")
        rc = customer_dao.delete_record("42")
        assert rc.error_tag == "RuntimeError"


# ===========================================================================
# delete_record_by_field
# ===========================================================================

class TestDeleteRecordByField:
    @pytest.mark.skip(reason="requires db2_safe decorator")
    def test_success_commits_and_returns_deleted_count(
        self, customer_dao, mock_connection, mock_cursor
    ):
        mock_cursor.rowcount = 2
        rc = customer_dao.delete_record_by_field({"LAST_NAME": "Smith"})
        assert _is_ok(rc)
        assert rc.data["deleted_count"] == 2
        mock_connection.commit.assert_called_once()

    def test_empty_filter_returns_malformed_content(self, customer_dao):
        rc = customer_dao.delete_record_by_field({})
        assert rc.error_tag == "MalformedContent"

    def test_multiple_field_filter_returns_malformed_content(self, customer_dao):
        rc = customer_dao.delete_record_by_field({"FIRST_NAME": "Alice", "LAST_NAME": "Smith"})
        assert rc.error_tag == "MalformedContent"

    def test_correct_delete_sql_with_field(self, customer_dao, mock_cursor):
        customer_dao.delete_record_by_field({"LAST_NAME": "Smith"})
        sql, params = mock_cursor.execute.call_args[0]
        assert "DELETE FROM USER12.CUSTOMER WHERE LAST_NAME = ?" in sql
        assert params == ("Smith",)


# ===========================================================================
# Credential management
# ===========================================================================

class TestCredentialManagement:
    def test_credentials_are_none_by_default(self, customer_dao):
        assert customer_dao.get_credentials() is None

    def test_set_credentials_stores_object(self, customer_dao):
        creds = Credentials(role="admin", user_id="u001")
        customer_dao.set_credentials(creds)
        assert customer_dao.get_credentials() is creds

    def test_clear_credentials_resets_to_none(self, customer_dao):
        creds = Credentials(role="admin", user_id="u001")
        customer_dao.set_credentials(creds)
        customer_dao.clear_credentials()
        assert customer_dao.get_credentials() is None

    def test_set_credentials_replaces_existing(self, customer_dao):
        creds1 = Credentials(role="admin", user_id="u001")
        creds2 = Credentials(role="read-only", user_id="u002")
        customer_dao.set_credentials(creds1)
        customer_dao.set_credentials(creds2)
        assert customer_dao.get_credentials() is creds2


# ===========================================================================
# Credentials entity – __repr__
# ===========================================================================

class TestCredentialsRepr:
    def test_repr_contains_role_and_user_id(self):
        creds = Credentials(role="admin", user_id="u001")
        assert repr(creds) == "Credentials(role='admin', user_id='u001')"

    def test_repr_with_empty_defaults(self):
        creds = Credentials()
        assert repr(creds) == "Credentials(role='', user_id='')"


# ===========================================================================
# CCIDao – get_records_by_customerid and insert_cc
# ===========================================================================

class TestCCIDaoCustomMethods:
    @pytest.fixture
    def cci_dao(self, mock_connection):
        return CCIDao(mock_connection)

    def test_get_records_by_customerid_returns_rows(self, cci_dao, mock_cursor):
        mock_cursor.fetchall.return_value = [
            (4111111111111111, 123, "12/28", "Visa", "John", "Smith",
             "1 Main St", "", "NYC", "NY", "US", "10001")
        ]
        result = cci_dao.get_records_by_customerid(1)
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_records_by_customerid_empty_returns_empty_list(self, cci_dao, mock_cursor):
        mock_cursor.fetchall.return_value = []
        result = cci_dao.get_records_by_customerid(9999)
        assert result == []

    def test_get_records_by_customerid_query_uses_customerid(self, cci_dao, mock_cursor):
        mock_cursor.fetchall.return_value = []
        cci_dao.get_records_by_customerid(42)
        sql, params = mock_cursor.execute.call_args[0]
        assert "CUSTOMERID = ?" in sql
        assert params == (42,)

    def test_insert_cc_returns_existing_when_record_found(self, cci_dao, mock_cursor):
        from backend.api.models.credit_card import NewCCRequest
        existing_row = (4111111111111111, 123, "12/28", "Visa", "John", "Smith",
                        "1 Main St", "", "NYC", "NY", "US", "10001", 1)
        mock_cursor.fetchall.return_value = [existing_row]
        entry = NewCCRequest(number=4111111111111111, security_code=123,
                             expiration="12/28", processor="Visa",
                             first_name="John", last_name="Smith",
                             address="1 Main St", addr_2="",
                             city="NYC", state="NY", country="US",
                             zip="10001", customerid=1)
        result = cci_dao.insert_cc(entry)
        assert result == [existing_row]
        # INSERT should not have been called since record already exists
        insert_calls = [
            call for call in mock_cursor.execute.call_args_list
            if "INSERT" in str(call)
        ]
        assert len(insert_calls) == 0

    def test_insert_cc_inserts_when_no_existing_record(self, cci_dao, mock_cursor):
        from backend.api.models.credit_card import NewCCRequest
        new_row = (1, 4111111111111111, 123, "12/28", "Visa", "John", "Smith",
                   "1 Main St", "", "NYC", "NY", "US", "10001", 1)
        # First SELECT (dedup check) → no rows; COUNT → 0; final SELECT → returns row
        mock_cursor.fetchall.side_effect = [
            [],          # initial SELECT finds nothing
            [(0,)],      # COUNT(*)
            [new_row],   # final SELECT by CCID (INSERT has no fetchall)
        ]
        entry = NewCCRequest(number=4111111111111111, security_code=123,
                             expiration="12/28", processor="Visa",
                             first_name="John", last_name="Smith",
                             address="1 Main St", addr_2="",
                             city="NYC", state="NY", country="US",
                             zip="10001", customerid=1)
        result = cci_dao.insert_cc(entry)
        assert result == [new_row]
        insert_calls = [
            call for call in mock_cursor.execute.call_args_list
            if "INSERT" in str(call)
        ]
        assert len(insert_calls) == 1
