# kata 7.W.0 — environment setup cell
# compatible with local Jupyter and Google Colab

import subprocess, sys

subprocess.check_call(
    [sys.executable, "-m", "pip", "install", "duckdb>=1.4", "pandas", "--quiet"]
)

import duckdb
import pandas as pd
import os
import random
import numpy as np
from datetime import datetime

# in-memory DuckDB connection (no file on disk)
con = duckdb.connect()

# create test table
con.execute("""
    CREATE TABLE hello_world (
        id          INTEGER,
        message     VARCHAR,
        created_at  TIMESTAMP
    )
""")

# insert 3 rows
con.execute("""
    INSERT INTO hello_world VALUES
        (1, 'Bronze layer ready',  '2026-07-28 09:00:00'),
        (2, 'Silver layer ready',  '2026-07-28 09:01:00'),
        (3, 'Gold layer ready',    '2026-07-28 09:02:00')
""")

# query and display
result = con.execute("SELECT * FROM hello_world ORDER BY id").df()
print(result.to_string(index=False))
print("\nEnvironment ready ✓")
print(f"  python  : {sys.version.split()[0]}")
print(f"  duckdb  : {duckdb.__version__}")
print(f"  pandas  : {pd.__version__}")
