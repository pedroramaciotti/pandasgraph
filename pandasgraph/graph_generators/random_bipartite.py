import pandas as pd
from random import randint

def get_random_bipartite(n_edges=10000000, n_a=10000, n_b=10000):
    return pd.DataFrame([(f"a{randint(0, n_a)}", f"b{randint(0, n_b)}") for x in range(n_edges)], columns=["A_id", "B_id"])