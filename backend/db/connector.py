import os
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
venv_path = project_root / ".venv" / "Lib" / "site-packages" / "clidriver"
clidriver_bin = venv_path / "bin"
clidriver_crt = clidriver_bin / "amd64.VC12.CRT"

os.add_dll_directory(str(clidriver_bin))
os.environ["PATH"] = str(clidriver_crt) + ";" + os.environ.get("PATH", "")

import ibm_db
import ibm_db_dbi

conn_str = (
    f"DATABASE=HL02HL2D;"
    f"HOSTNAME=192.168.54.250;"
    f"PORT=3600;"
    f"PROTOCOL=TCPIP;"
    f"AUTHENTICATION=SERVER;"
    f"UID=USER12;"
    f"PWD=35LLBAE_;"
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
