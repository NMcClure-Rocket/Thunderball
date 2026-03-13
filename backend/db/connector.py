import os
from pathlib import Path
# import ibm_db

project_root = Path(__file__).parent
venv_path = project_root / "venv" / "Lib" / "site-packages" / "clidriver"
clidriver_bin = venv_path / "bin"
clidriver_crt = clidriver_bin / "amd64.VC12.CRT"

os.add_dll_directory(str(clidriver_bin))
os.environ["PATH"] = str(clidriver_crt) + ";" + os.environ.get("PATH", "")
import ibm_db

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
    db_conn = ibm_db.connect(conn_str,"", "")


except Exception as e:
    print("SQLSTATE:", ibm_db.conn_error())
    print("Message: ", ibm_db.conn_errormsg())
    db_conn = None

if db_conn:
    print("SUCCESS!")

    import ibm_db_dbi
    conn = ibm_db_dbi.Connection(db_conn)

    select_stmt = "SELECT * FROM USER18.CUSTOMER"

    cur = conn.cursor()
    cur.execute(select_stmt)
    row = cur.fetchall()
    print(row)

    # ins = "INSERT INTO TBUSER12 (COLUMN1, COLUMN2, RENAMED_COL) VALUES (?,?,?)"
    ins = "INSERT INTO USER18.CUSTOMER (CUSTOMERID, NAME, EMAIL, PASSWORD) VALUES (?,?,?,?)"
    paras = ((1, "Charlie Chaplin", "cc@cc.com", "chaplin_was_here"), (2, "Spencer Majah Nathan", "smn@spp.com", "juju_was_here"))
    ins_stmt = ibm_db.prepare(db_conn, ins)

    ibm_db.execute_many(ins_stmt, paras)
    # print(ins_stmt)



    

    # conn.close() DOESN'T WORK DON'T USE

print("TEST")