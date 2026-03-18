import os
from pathlib import Path
from config.db_credentials_manager import DB_credentials

project_root = Path(__file__).parent.parent.parent
venv_path = project_root / ".venv" / "Lib" / "site-packages" / "clidriver"
clidriver_bin = venv_path / "bin"
clidriver_crt = clidriver_bin / "amd64.VC12.CRT"

os.add_dll_directory(str(clidriver_bin))
os.environ["PATH"] = str(clidriver_crt) + ";" + os.environ.get("PATH", "")

import ibm_db  # type: ignore[import-untyped]  # noqa: E402
import ibm_db_dbi  # type: ignore[import-untyped]  # noqa: E402

conn_str = DB_credentials().as_connection_string()


try:
    db_conn = ibm_db.connect(conn_str, "", "")
except Exception:
    print("SQLSTATE:", ibm_db.conn_error())
    print("Message:", ibm_db.conn_errormsg())
    db_conn = None

conn = None
if db_conn:
    conn = ibm_db_dbi.Connection(db_conn)
