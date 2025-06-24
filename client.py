# client.py – Creates secret shares, sends them, reconstructs answer

from multiprocessing import Pipe, Process
import numpy as np
from pir_utils import secret_share, reconstruct
from server import server_process

DB_FILE = "database.npy"
DB_SIZE = 10_000
NUM_SERVERS = 4

def main():
    # Step 1: Load DB and choose index to retrieve from 0 - 9999
    index = 700 # you can change index to retrieve from 0 - 9999
    print(f"Client wants to retrieve database[{index}]")

    # Step 2: Create query vector (standard basis)
    query = np.zeros(DB_SIZE, dtype=np.uint64)
    query[index] = 1

    # Step 3: Secret-share the query
    shares = secret_share(query, NUM_SERVERS)

    # Step 4: Start servers
    pipes = []
    processes = []
    for _ in range(NUM_SERVERS):
        parent_conn, child_conn = Pipe()
        proc = Process(target=server_process, args=(child_conn, DB_FILE))
        proc.start()
        pipes.append(parent_conn)
        processes.append(proc)

    # Step 5: Send shares and receive partial results
    for i in range(NUM_SERVERS):
        pipes[i].send(shares[i])

    partials = [pipes[i].recv() for i in range(NUM_SERVERS)]
    result = reconstruct(partials)

    # Step 6: Load database and verify
    db = np.load(DB_FILE)
    expected = db[index]
    print(f"Expected: {expected}")
    print(f"Recovered via PIR: {result}")
    assert expected == result, "Mismatch!"

    # Step 7: Stop servers
    for pipe in pipes:
        pipe.send("STOP")
    for proc in processes:
        proc.join()

if __name__ == "__main__":
    main()
