import os
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
venv_path = project_root / ".venv" / "Lib" / "site-packages" / "clidriver"
clidriver_bin = venv_path / "bin"
clidriver_crt = clidriver_bin / "amd64.VC12.CRT"

if hasattr(os, "add_dll_directory"):
    os.add_dll_directory(str(clidriver_bin))  # type: ignore[attr-defined]
os.environ["PATH"] = str(clidriver_crt) + ";" + os.environ.get("PATH", "")

import ibm_db  # noqa: E402  # type: ignore[import-untyped]
import ibm_db_dbi  # noqa: E402  # type: ignore[import-untyped]

conn_str = (
    "DATABASE=HL02HL2D;"
    "HOSTNAME=192.168.54.250;"
    "PORT=3600;"
    "PROTOCOL=TCPIP;"
    "AUTHENTICATION=SERVER;"
    "UID=USER12;"
    "PWD=35LLBAE_;"
)

try:
    db_conn = ibm_db.connect(conn_str, "", "")
except Exception:
    print("SQLSTATE:", ibm_db.conn_error())
    print("Message:", ibm_db.conn_errormsg())
    db_conn = None

conn = None
if db_conn:
    conn = ibm_db_dbi.Connection(db_conn)
