# pir_utils.py – Utility functions (secret sharing, dot product)

import numpy as np

def secret_share(vector, num_shares=4):
    """Secret-share a binary vector (0/1) into num_shares shares over mod 2^64."""
    shares = [np.random.randint(0, 2, size=vector.shape, dtype=np.uint64) for _ in range(num_shares - 1)]
    final = vector.astype(np.uint64)
    for share in shares:
        final = final - share  # Under np.uint64, wraparound happens automatically
    shares.append(final)
    return shares



def dot_product_mod2(vector, database):
    """Returns dot product mod 2^64 using unsigned 64-bit arithmetic."""
    vector = vector.astype(np.uint64)
    database = database.astype(np.uint64)
    result = np.dot(vector, database)  # uint64 dot uint64 stays in uint64
    return result  # Safe wraparound due to uint64 type

def reconstruct(shares):
    """Recombine shares with wrapping modulo 2^64 arithmetic."""
    shares = np.array(shares, dtype=np.uint64)
    return np.sum(shares, dtype=np.uint64)  #  no manual modulo!
