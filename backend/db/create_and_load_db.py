"""
Create DB and Load Test Data

1. Connects to z/OSMF, submits MAKE_DB.jcl to create the VILNIUS database,
   and waits for the job to complete.
2. Connects to DB2 and loads all test data from ./test_data/.

Credentials:
  DB2      – backend/config/Db_creds  (JSON, see db_credentials_manager.py)
  z/OSMF   – cred.ini alongside this script  (INI, [MAIN] host/username/password)
"""

import os
import sys
import time
import argparse
import configparser
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import List

import requests
from urllib3.exceptions import InsecureRequestWarning

# ── Project root / sys.path ──────────────────────────────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parents[1]
sys.path.insert(0, str(_PROJECT_ROOT))

# ── DLL path setup (Windows ibm_db requirement) ──────────────────────────────
_venv_clidriver = _PROJECT_ROOT / ".venv" / "Lib" / "site-packages" / "clidriver"
_clidriver_bin = _venv_clidriver / "bin"
_clidriver_crt = _clidriver_bin / "amd64.VC12.CRT"

if hasattr(os, "add_dll_directory"):
    os.add_dll_directory(str(_clidriver_bin))  # type: ignore[attr-defined]
os.environ["PATH"] = str(_clidriver_crt) + ";" + os.environ.get("PATH", "")

import ibm_db  # type: ignore[import-untyped]  # noqa: E402
from backend.config.db_credentials_manager import DB_credentials  # noqa: E402

# Suppress SSL warnings for self-signed z/OSMF certificates
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# ── Data / JCL directories ───────────────────────────────────────────────────
DATA_DIR = str(_SCRIPT_DIR / "test_data")
JCL_DIR = str(_SCRIPT_DIR.parent / "cobol" / "jcl")


# ══════════════════════════════════════════════════════════════════════════════
# Data classes
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class Customer:
    customerid: int
    first_name: str
    last_name: str
    email: str
    password: str


@dataclass
class ShippingAddress:
    addressid: int
    first_name: str
    last_name: str
    address: str
    addr_2: str
    city: str
    state: str
    country: str
    zip: str
    customerid: int


@dataclass
class CCI:
    ccid: int
    number: int
    security_code: int
    expiration: str
    processor: str
    first_name: str
    last_name: str
    address: str
    addr_2: str
    city: str
    state: str
    country: str
    zip: str
    customerid: int


@dataclass
class BasePrice:
    priceid: int
    name: str
    price: Decimal
    imagelink: str


@dataclass
class Inventory:
    itemid: int
    name: str
    description: str
    format: str
    potency: int
    reusable: str
    category: str
    price: Decimal
    amount: int
    baseinfo: int


@dataclass
class Order:
    orderid: int
    purchase_time: str
    delivery_est: str
    itemid: int
    amount: int
    transaction: Decimal
    ccid: int
    customerid: int
    addressid: int


# ══════════════════════════════════════════════════════════════════════════════
# File readers
# ══════════════════════════════════════════════════════════════════════════════

def read_customers(filepath: str = None) -> List[Customer]:
    """Read pipe-delimited customer records.  Format: customerID|first_name|last_name|email|password"""
    if filepath is None:
        filepath = os.path.join(DATA_DIR, "customers.txt")
    customers = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            p = line.split("|")
            customers.append(Customer(int(p[0]), p[1], p[2], p[3], p[4]))
    return customers


def read_shipping_addresses(filepath: str = None) -> List[ShippingAddress]:
    """Read pipe-delimited shipping address records.
    Format: addressID|first_name|last_name|address|addr_2|city|state|country|zip|customerID"""
    if filepath is None:
        filepath = os.path.join(DATA_DIR, "shipping_addresses.txt")
    addresses = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            p = line.split("|")
            addresses.append(ShippingAddress(
                int(p[0]), p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], int(p[9])
            ))
    return addresses


def read_cci(filepath: str = None) -> List[CCI]:
    """Read pipe-delimited credit card records.
    Format: ccID|number|security_code|expiration|processor|first_name|last_name|address|addr_2|city|state|country|zip|customerID"""
    if filepath is None:
        filepath = os.path.join(DATA_DIR, "cci.txt")
    cards = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            p = line.split("|")
            cards.append(CCI(
                int(p[0]), int(p[1]), int(p[2]), p[3], p[4],
                p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], int(p[13])
            ))
    return cards


def read_base_prices(filepath: str = None) -> List[BasePrice]:
    """Read pipe-delimited base price records.  Format: priceID|name|price|image_link"""
    if filepath is None:
        filepath = os.path.join(DATA_DIR, "base_prices.txt")
    prices = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            p = line.split("|")
            prices.append(BasePrice(int(p[0]), p[1], Decimal(p[2]), p[3]))
    return prices


def read_inventory(filepath: str = None) -> List[Inventory]:
    """Read pipe-delimited inventory records.
    Format: itemID|name|description|format|potency|reusable|category|price|amount|base_info"""
    if filepath is None:
        filepath = os.path.join(DATA_DIR, "inventory.txt")
    items = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            p = line.split("|")
            items.append(Inventory(
                int(p[0]), p[1], p[2], p[3], int(p[4]),
                p[5], p[6], Decimal(p[7]), int(p[8]), int(p[9])
            ))
    return items


def read_orders(filepath: str = None) -> List[Order]:
    """Read pipe-delimited order records.
    Format: orderID|purchase_time|delivery_est|itemID|amount|transaction|ccID|customerID|addressID"""
    if filepath is None:
        filepath = os.path.join(DATA_DIR, "orders.txt")
    orders = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            p = line.split("|")
            orders.append(Order(
                int(p[0]), p[1], p[2], int(p[3]),
                int(p[4]), Decimal(p[5]), int(p[6]), int(p[7]), int(p[8])
            ))
    return orders


# ══════════════════════════════════════════════════════════════════════════════
# DB2 loaders
# ══════════════════════════════════════════════════════════════════════════════

def load_customers(db_conn) -> None:
    ins = (
        "INSERT INTO USER12.CUSTOMER "
        "(CUSTOMERID, FIRST_NAME, LAST_NAME, EMAIL, PASSWORD) VALUES (?,?,?,?,?)"
    )
    rows = [(c.customerid, c.first_name, c.last_name, c.email, c.password)
            for c in read_customers()]
    ibm_db.execute_many(ibm_db.prepare(db_conn, ins), tuple(rows))
    print(f"  Loaded {len(rows)} customers")


def load_addresses(db_conn) -> None:
    ins = (
        "INSERT INTO USER12.SHIPPINGADDRESS "
        "(ADDRESSID, FIRST_NAME, LAST_NAME, ADDRESS, ADDR_2, CITY, STATE, COUNTRY, ZIP, CUSTOMERID) "
        "VALUES (?,?,?,?,?,?,?,?,?,?)"
    )
    rows = [(a.addressid, a.first_name, a.last_name, a.address, a.addr_2,
             a.city, a.state, a.country, a.zip, a.customerid)
            for a in read_shipping_addresses()]
    ibm_db.execute_many(ibm_db.prepare(db_conn, ins), tuple(rows))
    print(f"  Loaded {len(rows)} shipping addresses")


def load_cci(db_conn) -> None:
    ins = (
        "INSERT INTO USER12.CCI "
        "(CCID, NUMBER, SECURITY_CODE, EXPIRATION, PROCESSOR, "
        "FIRST_NAME, LAST_NAME, ADDRESS, ADDR_2, CITY, STATE, COUNTRY, ZIP, CUSTOMERID) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    )
    rows = [(c.ccid, c.number, c.security_code, c.expiration, c.processor,
             c.first_name, c.last_name, c.address, c.addr_2,
             c.city, c.state, c.country, c.zip, c.customerid)
            for c in read_cci()]
    ibm_db.execute_many(ibm_db.prepare(db_conn, ins), tuple(rows))
    print(f"  Loaded {len(rows)} credit cards")


def load_baseprice(db_conn) -> None:
    ins = (
        "INSERT INTO USER12.BASEPRICE "
        "(PRICEID, NAME, PRICE, IMAGELINK) VALUES (?,?,?,?)"
    )
    rows = [(b.priceid, b.name, str(b.price), b.imagelink)
            for b in read_base_prices()]
    ibm_db.execute_many(ibm_db.prepare(db_conn, ins), tuple(rows))
    print(f"  Loaded {len(rows)} base prices")


def load_inventory(db_conn) -> None:
    ins = (
        "INSERT INTO USER12.INVENTORY "
        "(ITEMID, NAME, DESCRIPTION, FORMAT, POTENCY, REUSABLE, CATEGORY, PRICE, AMOUNT, BASEINFO) "
        "VALUES (?,?,?,?,?,?,?,?,?,?)"
    )
    rows = [(i.itemid, i.name, i.description, i.format, i.potency,
             i.reusable, i.category, str(i.price), i.amount, i.baseinfo)
            for i in read_inventory()]
    ibm_db.execute_many(ibm_db.prepare(db_conn, ins), tuple(rows))
    print(f"  Loaded {len(rows)} inventory items")


def load_orders(db_conn) -> None:
    ins = (
        "INSERT INTO USER12.INVORDER "
        "(ORDERID, PURCHASE_TIME, DELIVERY_EST, ITEMID, AMOUNT, TRANSACTION, CCID, CUSTOMERID, ADDRESSID) "
        "VALUES (?,?,?,?,?,?,?,?,?)"
    )
    rows = [(o.orderid, o.purchase_time, o.delivery_est, o.itemid, o.amount,
             str(o.transaction), o.ccid, o.customerid, o.addressid)
            for o in read_orders()]
    ibm_db.execute_many(ibm_db.prepare(db_conn, ins), tuple(rows))
    print(f"  Loaded {len(rows)} orders")


# ══════════════════════════════════════════════════════════════════════════════
# z/OSMF helpers
# ══════════════════════════════════════════════════════════════════════════════

def _load_zosmf_credentials() -> tuple:
    """Read z/OSMF host/username/password from cred.ini next to this script."""
    config = configparser.ConfigParser()
    cred_file = str(_SCRIPT_DIR / "cred.ini")
    if not os.path.exists(cred_file):
        raise FileNotFoundError(
            f"Could not find 'cred.ini' at {cred_file}. "
            "Create it with a [MAIN] section containing host, username, and password."
        )
    config.read(cred_file)
    try:
        host = config["MAIN"]["host"]
        username = config["MAIN"]["username"]
        password = config["MAIN"]["password"]
    except KeyError as exc:
        raise KeyError(
            f"Missing required key {exc} in cred.ini [MAIN] section."
        ) from exc

    if not host.startswith(("http://", "https://")):
        host = "https://" + host
    return host, username, password


def _connect_to_zosmf(host: str, username: str, password: str):
    """Authenticate to z/OSMF and return an active requests.Session."""
    session = requests.Session()
    session.auth = (username, password)
    session.verify = False
    session.headers.update({
        "Content-Type": "application/json",
        "X-CSRF-ZOSMF-HEADER": "true",
    })
    resp = session.post(f"{host.rstrip('/')}/zosmf/services/authenticate")
    if resp.status_code == 200:
        print(f"z/OSMF logon successful ({username})")
    else:
        print(f"ERROR: z/OSMF logon returned {resp.status_code}\n{resp.text}")
        sys.exit(1)
    return session


def _submit_jcl(session, host: str, jcl_text: str) -> dict:
    """Submit inline JCL text and return the job info dict."""
    url = f"{host.rstrip('/')}/zosmf/restjobs/jobs"
    resp = session.put(url, data=jcl_text, headers={"Content-Type": "text/plain"})
    resp.raise_for_status()
    data = resp.json()
    print(f"  Job submitted – Name: {data.get('jobname')}  ID: {data.get('jobid')}  Status: {data.get('status')}")
    return data


def _poll_job(session, host: str, jobname: str, jobid: str,
              poll_interval: int = 5, max_wait: int = 300) -> dict:
    """Poll until the job reaches OUTPUT/ABEND status or times out."""
    url = f"{host.rstrip('/')}/zosmf/restjobs/jobs/{jobname}/{jobid}"
    elapsed = 0
    while elapsed < max_wait:
        data = session.get(url).json()
        status = data.get("status", "")
        retcode = data.get("retcode", "")
        print(f"  status={status}  retcode={retcode}")
        if status in ("OUTPUT", "ABEND"):
            return data
        time.sleep(poll_interval)
        elapsed += poll_interval
    raise TimeoutError(f"Job {jobname}/{jobid} did not complete within {max_wait} seconds")


# ══════════════════════════════════════════════════════════════════════════════
# High-level operations
# ══════════════════════════════════════════════════════════════════════════════

def create_database() -> None:
    """Submit MAKE_DB.jcl via z/OSMF to create the VILNIUS database."""
    host, username, password = _load_zosmf_credentials()
    print("Connecting to z/OSMF...")
    session = _connect_to_zosmf(host, username, password)

    jcl_path = os.path.join(JCL_DIR, "MAKE_DB.jcl")
    with open(jcl_path, "r") as f:
        jcl = f.read()

    print(f"\nSubmitting MAKE_DB.jcl...")
    job_info = _submit_jcl(session, host, jcl)

    print("Waiting for job completion...")
    job_status = _poll_job(session, host, job_info["jobname"], job_info["jobid"])

    print("\n" + "=" * 60)
    print("JOB RESULTS:")
    print(f"  Job Name:    {job_info['jobname']}")
    print(f"  Job ID:      {job_info['jobid']}")
    print(f"  Return Code: {job_status.get('retcode', 'N/A')}")
    print("=" * 60)

    retcode = job_status.get("retcode", "")
    if retcode and not retcode.startswith("CC 0000"):
        raise RuntimeError(f"MAKE_DB job failed with return code: {retcode}")


def load_all_data() -> None:
    """Connect to DB2 and load all test data in dependency order."""
    conn_str = DB_credentials().as_connection_string()
    print("\nConnecting to DB2...")
    db_conn = ibm_db.connect(conn_str, "", "")
    if not db_conn:
        print("SQLSTATE:", ibm_db.conn_error())
        print("Message:", ibm_db.conn_errormsg())
        raise RuntimeError("Failed to connect to DB2")

    print("Connected. Loading data...")
    try:
        # Load in FK-safe order: parents before children
        load_customers(db_conn)
        load_baseprice(db_conn)
        load_inventory(db_conn)
        load_addresses(db_conn)
        load_cci(db_conn)
        load_orders(db_conn)
        print("\nAll data loaded successfully.")
    finally:
        ibm_db.close(db_conn)


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Create the VILNIUS DB2 database and load test data."
    )
    parser.add_argument(
        "--skip-create", action="store_true",
        help="Skip JCL submission; only load test data into an existing database."
    )
    parser.add_argument(
        "--skip-load", action="store_true",
        help="Skip data loading; only submit the MAKE_DB.jcl job."
    )
    args = parser.parse_args()

    if not args.skip_create:
        create_database()

    if not args.skip_load:
        load_all_data()


if __name__ == "__main__":
    main()
