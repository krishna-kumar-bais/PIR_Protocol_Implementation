# setup_database.py – Create the databas

import numpy as np
DB_SIZE = 10_000
DB_FILE = "database.npy"

def generate_database():
    db = np.random.randint(
        low=0,                      # Start of range
        high=2**64,                 # End of range (exclusive)
        size=DB_SIZE,               # Number of entries
        dtype=np.uint64             # 64-bit unsigned integers
    )
    np.save(DB_FILE, db)
    print("Database saved to", DB_FILE)
    print("Example:", db[:5])

if __name__ == "__main__":
    generate_database()
