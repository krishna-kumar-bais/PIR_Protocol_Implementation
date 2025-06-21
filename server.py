# server.py – Simulates 4 servers using multiprocessing

from multiprocessing import Process, Pipe
import numpy as np
from pir_utils import dot_product_mod2

def server_process(conn, db_path):
    db = np.load(db_path).astype(np.uint64)  # Ensure database is uint64
    while True:
        query = conn.recv()
        if isinstance(query, str) and query == "STOP":
            break
        query = query.astype(np.uint64)       # Ensure query is uint64
        result = dot_product_mod2(query, db)
        conn.send(result)