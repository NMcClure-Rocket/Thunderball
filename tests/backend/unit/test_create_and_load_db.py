"""
Unit tests for backend.db.create_and_load_db.

Mocks ibm_db, ibm_db_dbi, and requests before importing the module so the
tests run without a live DB2 connection or z/OSMF instance.
"""
import configparser
import os
import sys
from decimal import Decimal
from pathlib import Path
from unittest.mock import MagicMock, patch, call
import pytest

# ---------------------------------------------------------------------------
# Module-level mocks – must be in place BEFORE the module is imported.
# ---------------------------------------------------------------------------
for _name in ("ibm_db", "ibm_db_dbi"):
    sys.modules.setdefault(_name, MagicMock())

# Provide a minimal mock for requests so the import doesn't fail.
_mock_requests = MagicMock()
_mock_requests.packages = MagicMock()
_mock_requests.packages.urllib3 = MagicMock()
_mock_requests.packages.urllib3.disable_warnings = MagicMock()
sys.modules.setdefault("requests", _mock_requests)
sys.modules.setdefault("urllib3", MagicMock())
sys.modules.setdefault("urllib3.exceptions", MagicMock())

# ---------------------------------------------------------------------------
# Import the module under test.
# ---------------------------------------------------------------------------
import backend.db.create_and_load_db as db_script  # noqa: E402
from backend.db.create_and_load_db import (  # noqa: E402
    Customer,
    ShippingAddress,
    CCI,
    BasePrice,
    Inventory,
    Order,
    read_customers,
    read_shipping_addresses,
    read_cci,
    read_base_prices,
    read_inventory,
    read_orders,
    _load_zosmf_credentials,
    _connect_to_zosmf,
    _submit_jcl,
    _poll_job,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_CUSTOMER_LINE = "1|John|Smith|john.smith@email.com|P@ssw0rd123!\n"
_ADDRESS_LINE = "1|John|Smith|123 Main Street|Apt 4B|New York|NY|United States|10001|1\n"
_CCI_LINE = "1|4532015112830366|123|03/28|Visa|John|Smith|123 Main Street|Apt 4B|New York|NY|United States|10001|1\n"
_BASEPRICE_LINE = "1|Healing Elixir|24.99|https://example.com/image.jpg\n"
_INVENTORY_LINE = "1|Healing Elixir Standard|Restores health|Tome|45|1|Health|24.99|150|1\n"
_ORDER_LINE = "1|2026-01-15 10:23:45|2026-01-22 14:00:00|1|2|49.98|1|1|1\n"


def _write_tmp(tmp_path: Path, name: str, content: str) -> str:
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return str(p)


# ===========================================================================
# Dataclasses – basic instantiation
# ===========================================================================

class TestDataclasses:
    def test_customer_instantiation(self):
        c = Customer(1, "John", "Smith", "j@e.com", "pw")
        assert c.customerid == 1
        assert c.first_name == "John"
        assert c.email == "j@e.com"

    def test_shipping_address_instantiation(self):
        a = ShippingAddress(1, "John", "Smith", "1 St", "", "NYC", "NY", "US", "10001", 1)
        assert a.addressid == 1
        assert a.city == "NYC"

    def test_cci_instantiation(self):
        c = CCI(1, 4111111111111111, 123, "12/28", "Visa",
                "John", "Smith", "1 St", "", "NYC", "NY", "US", "10001", 1)
        assert c.ccid == 1
        assert c.processor == "Visa"

    def test_base_price_instantiation(self):
        b = BasePrice(1, "Elixir", Decimal("24.99"), "http://img.jpg")
        assert b.name == "Elixir"
        assert b.price == Decimal("24.99")

    def test_inventory_instantiation(self):
        i = Inventory(1, "Tome", "desc", "PDF", 5, "Y", "Health", Decimal("9.99"), 100, 1)
        assert i.name == "Tome"
        assert i.amount == 100

    def test_order_instantiation(self):
        o = Order(1, "2026-01-15", "2026-01-22", 1, 2, Decimal("49.98"), 1, 1, 1)
        assert o.orderid == 1
        assert o.transaction == Decimal("49.98")


# ===========================================================================
# File readers
# ===========================================================================

class TestReadCustomers:
    def test_reads_one_record(self, tmp_path):
        path = _write_tmp(tmp_path, "customers.txt", _CUSTOMER_LINE)
        records = read_customers(path)
        assert len(records) == 1
        assert records[0].customerid == 1
        assert records[0].first_name == "John"
        assert records[0].email == "john.smith@email.com"

    def test_skips_blank_lines(self, tmp_path):
        path = _write_tmp(tmp_path, "customers.txt", "\n" + _CUSTOMER_LINE + "\n")
        records = read_customers(path)
        assert len(records) == 1

    def test_reads_multiple_records(self, tmp_path):
        content = _CUSTOMER_LINE + "2|Jane|Doe|j@d.com|pw2\n"
        path = _write_tmp(tmp_path, "customers.txt", content)
        records = read_customers(path)
        assert len(records) == 2
        assert records[1].last_name == "Doe"


class TestReadShippingAddresses:
    def test_reads_one_record(self, tmp_path):
        path = _write_tmp(tmp_path, "shipping_addresses.txt", _ADDRESS_LINE)
        records = read_shipping_addresses(path)
        assert len(records) == 1
        assert records[0].addressid == 1
        assert records[0].city == "New York"
        assert records[0].customerid == 1

    def test_skips_blank_lines(self, tmp_path):
        path = _write_tmp(tmp_path, "shipping_addresses.txt", "\n" + _ADDRESS_LINE)
        records = read_shipping_addresses(path)
        assert len(records) == 1


class TestReadCCI:
    def test_reads_one_record(self, tmp_path):
        path = _write_tmp(tmp_path, "cci.txt", _CCI_LINE)
        records = read_cci(path)
        assert len(records) == 1
        assert records[0].ccid == 1
        assert records[0].number == 4532015112830366
        assert records[0].processor == "Visa"
        assert records[0].customerid == 1

    def test_skips_blank_lines(self, tmp_path):
        path = _write_tmp(tmp_path, "cci.txt", "\n" + _CCI_LINE)
        records = read_cci(path)
        assert len(records) == 1


class TestReadBasePrices:
    def test_reads_one_record(self, tmp_path):
        path = _write_tmp(tmp_path, "base_prices.txt", _BASEPRICE_LINE)
        records = read_base_prices(path)
        assert len(records) == 1
        assert records[0].priceid == 1
        assert records[0].name == "Healing Elixir"
        assert records[0].price == Decimal("24.99")

    def test_skips_blank_lines(self, tmp_path):
        path = _write_tmp(tmp_path, "base_prices.txt", "\n" + _BASEPRICE_LINE)
        records = read_base_prices(path)
        assert len(records) == 1


class TestReadInventory:
    def test_reads_one_record(self, tmp_path):
        path = _write_tmp(tmp_path, "inventory.txt", _INVENTORY_LINE)
        records = read_inventory(path)
        assert len(records) == 1
        assert records[0].itemid == 1
        assert records[0].name == "Healing Elixir Standard"
        assert records[0].potency == 45
        assert records[0].price == Decimal("24.99")

    def test_skips_blank_lines(self, tmp_path):
        path = _write_tmp(tmp_path, "inventory.txt", "\n" + _INVENTORY_LINE)
        records = read_inventory(path)
        assert len(records) == 1


class TestReadOrders:
    def test_reads_one_record(self, tmp_path):
        path = _write_tmp(tmp_path, "orders.txt", _ORDER_LINE)
        records = read_orders(path)
        assert len(records) == 1
        assert records[0].orderid == 1
        assert records[0].itemid == 1
        assert records[0].transaction == Decimal("49.98")
        assert records[0].customerid == 1

    def test_skips_blank_lines(self, tmp_path):
        path = _write_tmp(tmp_path, "orders.txt", "\n" + _ORDER_LINE)
        records = read_orders(path)
        assert len(records) == 1


# ===========================================================================
# z/OSMF helper: _load_zosmf_credentials
# ===========================================================================

class TestLoadZosmfCredentials:
    def _write_ini(self, tmp_path: Path) -> str:
        config = configparser.ConfigParser()
        config["MAIN"] = {
            "host": "mainframe.example.com",
            "username": "user1",
            "password": "pass1",
        }
        cred_file = str(tmp_path / "cred.ini")
        with open(cred_file, "w") as f:
            config.write(f)
        return cred_file

    def test_returns_host_username_password(self, tmp_path):
        cred_file = self._write_ini(tmp_path)
        with patch.object(db_script, "_SCRIPT_DIR", tmp_path):
            host, username, password = _load_zosmf_credentials()
        assert username == "user1"
        assert password == "pass1"

    def test_adds_https_prefix_when_missing(self, tmp_path):
        cred_file = self._write_ini(tmp_path)
        with patch.object(db_script, "_SCRIPT_DIR", tmp_path):
            host, _, _ = _load_zosmf_credentials()
        assert host.startswith("https://")

    def test_preserves_existing_https_prefix(self, tmp_path):
        config = configparser.ConfigParser()
        config["MAIN"] = {
            "host": "https://mf.example.com",
            "username": "u",
            "password": "p",
        }
        with open(str(tmp_path / "cred.ini"), "w") as f:
            config.write(f)
        with patch.object(db_script, "_SCRIPT_DIR", tmp_path):
            host, _, _ = _load_zosmf_credentials()
        assert host == "https://mf.example.com"

    def test_missing_cred_ini_raises_file_not_found(self, tmp_path):
        with patch.object(db_script, "_SCRIPT_DIR", tmp_path):
            with pytest.raises(FileNotFoundError, match="cred.ini"):
                _load_zosmf_credentials()

    def test_missing_ini_key_raises_key_error(self, tmp_path):
        config = configparser.ConfigParser()
        config["MAIN"] = {"host": "h"}  # missing username & password
        with open(str(tmp_path / "cred.ini"), "w") as f:
            config.write(f)
        with patch.object(db_script, "_SCRIPT_DIR", tmp_path):
            with pytest.raises(KeyError):
                _load_zosmf_credentials()


# ===========================================================================
# z/OSMF helper: _connect_to_zosmf
# ===========================================================================

class TestConnectToZosmf:
    def test_returns_session_on_200(self):
        mock_session = MagicMock()
        mock_session.post.return_value.status_code = 200
        with patch("backend.db.create_and_load_db.requests") as mock_requests:
            mock_requests.Session.return_value = mock_session
            session = _connect_to_zosmf("https://host", "user", "pass")
        assert session is mock_session

    def test_exits_on_non_200(self):
        mock_session = MagicMock()
        mock_session.post.return_value.status_code = 401
        mock_session.post.return_value.text = "Unauthorized"
        with patch("backend.db.create_and_load_db.requests") as mock_requests:
            mock_requests.Session.return_value = mock_session
            with pytest.raises(SystemExit):
                _connect_to_zosmf("https://host", "user", "wrong_pass")


# ===========================================================================
# z/OSMF helper: _submit_jcl
# ===========================================================================

class TestSubmitJcl:
    def test_returns_job_info_dict(self):
        mock_session = MagicMock()
        mock_session.put.return_value.json.return_value = {
            "jobname": "MYJOB", "jobid": "JOB00001", "status": "INPUT"
        }
        mock_session.put.return_value.raise_for_status = MagicMock()
        result = _submit_jcl(mock_session, "https://host", "//JCL HERE")
        assert result["jobname"] == "MYJOB"
        assert result["jobid"] == "JOB00001"

    def test_raises_on_http_error(self):
        mock_session = MagicMock()
        mock_session.put.return_value.raise_for_status.side_effect = Exception("HTTP 500")
        with pytest.raises(Exception, match="HTTP 500"):
            _submit_jcl(mock_session, "https://host", "//JCL")


# ===========================================================================
# z/OSMF helper: _poll_job
# ===========================================================================

class TestPollJob:
    def test_returns_when_status_is_output(self):
        mock_session = MagicMock()
        mock_session.get.return_value.json.return_value = {
            "status": "OUTPUT", "retcode": "CC 0000"
        }
        result = _poll_job(mock_session, "https://host", "MYJOB", "JOB00001",
                           poll_interval=0, max_wait=10)
        assert result["status"] == "OUTPUT"

    def test_returns_when_status_is_abend(self):
        mock_session = MagicMock()
        mock_session.get.return_value.json.return_value = {
            "status": "ABEND", "retcode": "ABEND S0C7"
        }
        result = _poll_job(mock_session, "https://host", "MYJOB", "JOB00001",
                           poll_interval=0, max_wait=10)
        assert result["status"] == "ABEND"

    def test_raises_timeout_when_max_wait_exceeded(self):
        mock_session = MagicMock()
        mock_session.get.return_value.json.return_value = {
            "status": "ACTIVE", "retcode": ""
        }
        with patch("backend.db.create_and_load_db.time") as mock_time:
            mock_time.sleep = MagicMock()
            with pytest.raises(TimeoutError, match="did not complete"):
                _poll_job(mock_session, "https://host", "MYJOB", "JOB00001",
                          poll_interval=5, max_wait=5)


# ===========================================================================
# File readers – default filepath (exercises the `if filepath is None:` branch)
# ===========================================================================

class TestReadersUseDefaultPaths:
    """These tests call readers without a filepath so they fall through to the
    real test_data directory, exercising the `if filepath is None:` branches."""

    def test_read_customers_default_path(self):
        records = read_customers()
        assert isinstance(records, list)
        assert len(records) > 0
        assert isinstance(records[0], Customer)

    def test_read_shipping_addresses_default_path(self):
        records = read_shipping_addresses()
        assert isinstance(records, list)
        assert len(records) > 0
        assert isinstance(records[0], ShippingAddress)

    def test_read_cci_default_path(self):
        records = read_cci()
        assert isinstance(records, list)
        assert len(records) > 0
        assert isinstance(records[0], CCI)

    def test_read_base_prices_default_path(self):
        records = read_base_prices()
        assert isinstance(records, list)
        assert len(records) > 0
        assert isinstance(records[0], BasePrice)

    def test_read_inventory_default_path(self):
        records = read_inventory()
        assert isinstance(records, list)
        assert len(records) > 0
        assert isinstance(records[0], Inventory)

    def test_read_orders_default_path(self):
        records = read_orders()
        assert isinstance(records, list)
        assert len(records) > 0
        assert isinstance(records[0], Order)


# ===========================================================================
# DB2 loader functions (ibm_db is mocked at module level)
# ===========================================================================

from backend.db.create_and_load_db import (  # noqa: E402
    load_customers,
    load_addresses,
    load_cci,
    load_baseprice,
    load_inventory,
    load_orders,
    create_database,
    load_all_data,
    main as db_main,
)


class TestDB2Loaders:
    """Tests for the load_* functions that call ibm_db.execute_many."""

    @pytest.fixture
    def mock_db_conn(self):
        return MagicMock()

    def test_load_customers_calls_execute_many(self, mock_db_conn, tmp_path):
        _write_tmp(tmp_path, "customers.txt", _CUSTOMER_LINE)
        with patch("backend.db.create_and_load_db.ibm_db") as mock_ibm_db, \
             patch.object(db_script, "DATA_DIR", str(tmp_path)):
            load_customers(mock_db_conn)
        mock_ibm_db.execute_many.assert_called_once()

    def test_load_addresses_calls_execute_many(self, mock_db_conn, tmp_path):
        _write_tmp(tmp_path, "shipping_addresses.txt", _ADDRESS_LINE)
        with patch("backend.db.create_and_load_db.ibm_db") as mock_ibm_db, \
             patch.object(db_script, "DATA_DIR", str(tmp_path)):
            load_addresses(mock_db_conn)
        mock_ibm_db.execute_many.assert_called_once()

    def test_load_cci_calls_execute_many(self, mock_db_conn, tmp_path):
        _write_tmp(tmp_path, "cci.txt", _CCI_LINE)
        with patch("backend.db.create_and_load_db.ibm_db") as mock_ibm_db, \
             patch.object(db_script, "DATA_DIR", str(tmp_path)):
            load_cci(mock_db_conn)
        mock_ibm_db.execute_many.assert_called_once()

    def test_load_baseprice_calls_execute_many(self, mock_db_conn, tmp_path):
        _write_tmp(tmp_path, "base_prices.txt", _BASEPRICE_LINE)
        with patch("backend.db.create_and_load_db.ibm_db") as mock_ibm_db, \
             patch.object(db_script, "DATA_DIR", str(tmp_path)):
            load_baseprice(mock_db_conn)
        mock_ibm_db.execute_many.assert_called_once()

    def test_load_inventory_calls_execute_many(self, mock_db_conn, tmp_path):
        _write_tmp(tmp_path, "inventory.txt", _INVENTORY_LINE)
        with patch("backend.db.create_and_load_db.ibm_db") as mock_ibm_db, \
             patch.object(db_script, "DATA_DIR", str(tmp_path)):
            load_inventory(mock_db_conn)
        mock_ibm_db.execute_many.assert_called_once()

    def test_load_orders_calls_execute_many(self, mock_db_conn, tmp_path):
        _write_tmp(tmp_path, "orders.txt", _ORDER_LINE)
        with patch("backend.db.create_and_load_db.ibm_db") as mock_ibm_db, \
             patch.object(db_script, "DATA_DIR", str(tmp_path)):
            load_orders(mock_db_conn)
        mock_ibm_db.execute_many.assert_called_once()


# ===========================================================================
# High-level operations: create_database, load_all_data, main
# ===========================================================================

class TestCreateDatabase:
    def _make_ini(self, tmp_path: Path) -> None:
        config = configparser.ConfigParser()
        config["MAIN"] = {"host": "https://mf.example.com", "username": "u", "password": "p"}
        with open(str(tmp_path / "cred.ini"), "w") as f:
            config.write(f)

    def test_create_database_success(self, tmp_path):
        self._make_ini(tmp_path)
        # Write a minimal JCL file
        jcl_dir = tmp_path / "jcl"
        jcl_dir.mkdir()
        (jcl_dir / "MAKE_DB.jcl").write_text("//MAKEJOB JOB\n")
        mock_session = MagicMock()
        mock_session.post.return_value.status_code = 200
        mock_session.put.return_value.raise_for_status = MagicMock()
        mock_session.put.return_value.json.return_value = {
            "jobname": "MAKEJOB", "jobid": "JOB00001", "status": "INPUT"
        }
        mock_session.get.return_value.json.return_value = {
            "status": "OUTPUT", "retcode": "CC 0000"
        }
        with patch.object(db_script, "_SCRIPT_DIR", tmp_path), \
             patch.object(db_script, "JCL_DIR", str(jcl_dir)), \
             patch("backend.db.create_and_load_db.requests") as mock_req:
            mock_req.Session.return_value = mock_session
            create_database()  # Should not raise

    def test_create_database_nonzero_retcode_raises(self, tmp_path):
        self._make_ini(tmp_path)
        jcl_dir = tmp_path / "jcl"
        jcl_dir.mkdir()
        (jcl_dir / "MAKE_DB.jcl").write_text("//MAKEJOB JOB\n")
        mock_session = MagicMock()
        mock_session.post.return_value.status_code = 200
        mock_session.put.return_value.raise_for_status = MagicMock()
        mock_session.put.return_value.json.return_value = {
            "jobname": "MAKEJOB", "jobid": "JOB00001", "status": "INPUT"
        }
        mock_session.get.return_value.json.return_value = {
            "status": "OUTPUT", "retcode": "CC 0008"
        }
        with patch.object(db_script, "_SCRIPT_DIR", tmp_path), \
             patch.object(db_script, "JCL_DIR", str(jcl_dir)), \
             patch("backend.db.create_and_load_db.requests") as mock_req:
            mock_req.Session.return_value = mock_session
            with pytest.raises(RuntimeError, match="return code"):
                create_database()


class TestLoadAllData:
    def test_load_all_data_connects_and_loads(self):
        mock_db_conn = MagicMock()
        with patch("backend.db.create_and_load_db.ibm_db") as mock_ibm_db, \
             patch("backend.db.create_and_load_db.DB_credentials") as mock_creds, \
             patch("backend.db.create_and_load_db.load_customers") as mock_lc, \
             patch("backend.db.create_and_load_db.load_baseprice") as mock_lb, \
             patch("backend.db.create_and_load_db.load_inventory") as mock_li, \
             patch("backend.db.create_and_load_db.load_addresses") as mock_la, \
             patch("backend.db.create_and_load_db.load_cci") as mock_lcci, \
             patch("backend.db.create_and_load_db.load_orders") as mock_lo:
            mock_creds.return_value.as_connection_string.return_value = "DSN=TEST"
            mock_ibm_db.connect.return_value = mock_db_conn
            load_all_data()
        mock_lc.assert_called_once()
        mock_lb.assert_called_once()
        mock_li.assert_called_once()
        mock_la.assert_called_once()
        mock_lcci.assert_called_once()
        mock_lo.assert_called_once()
        mock_ibm_db.close.assert_called_once_with(mock_db_conn)

    def test_load_all_data_raises_if_connect_returns_none(self):
        with patch("backend.db.create_and_load_db.ibm_db") as mock_ibm_db, \
             patch("backend.db.create_and_load_db.DB_credentials") as mock_creds:
            mock_creds.return_value.as_connection_string.return_value = "DSN=BAD"
            mock_ibm_db.connect.return_value = None
            mock_ibm_db.conn_error.return_value = "08001"
            mock_ibm_db.conn_errormsg.return_value = "Connection failed"
            with pytest.raises(RuntimeError, match="Failed to connect"):
                load_all_data()


class TestMain:
    def test_main_calls_both_by_default(self):
        with patch("backend.db.create_and_load_db.create_database") as mock_cd, \
             patch("backend.db.create_and_load_db.load_all_data") as mock_lad, \
             patch("sys.argv", ["prog"]):
            db_main()
        mock_cd.assert_called_once()
        mock_lad.assert_called_once()

    def test_main_skip_create(self):
        with patch("backend.db.create_and_load_db.create_database") as mock_cd, \
             patch("backend.db.create_and_load_db.load_all_data") as mock_lad, \
             patch("sys.argv", ["prog", "--skip-create"]):
            db_main()
        mock_cd.assert_not_called()
        mock_lad.assert_called_once()

    def test_main_skip_load(self):
        with patch("backend.db.create_and_load_db.create_database") as mock_cd, \
             patch("backend.db.create_and_load_db.load_all_data") as mock_lad, \
             patch("sys.argv", ["prog", "--skip-load"]):
            db_main()
        mock_cd.assert_called_once()
        mock_lad.assert_not_called()

    def test_main_skip_both(self):
        with patch("backend.db.create_and_load_db.create_database") as mock_cd, \
             patch("backend.db.create_and_load_db.load_all_data") as mock_lad, \
             patch("sys.argv", ["prog", "--skip-create", "--skip-load"]):
            db_main()
        mock_cd.assert_not_called()
        mock_lad.assert_not_called()
