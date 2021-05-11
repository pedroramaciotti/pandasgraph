import pandas as pd
import numpy as np
import os
import time

from comcore1 import project_graph

def calculate_projection(df=pd.read_csv('pandasgraph/sample_graphs/sample_bipartite_1.csv'), projection='A_id'):
    """
    Writing the bipartite graph in community structure and passing it to comcore1
    Each node of the non-projected side is a "community"
    We write one line per community, each line contains the nodes from the projected side that belong (are connected) 
    to the community
    """

    start = time.time()

    if projection is None:
        projection=df.columns[0]
    elif projection not in df.columns:
        raise ValueError("Selected columns not in graph")

    lut = pd.Series({node: i + 1 for i, node in enumerate(df[projection].unique())})
    df['int_id'] = df[projection].map(lut)
    df['int_id']=df['int_id'].astype(str)

    non_projected_part = [c for c in df.columns[:-1] if c not in [projection,'int_id']][0]
    communitized_df = df[['int_id',non_projected_part]].groupby(non_projected_part)['int_id'].apply(lambda n: ' '.join(np.sort(n))).reset_index(drop=True)

    bigraph_as_list = [[int(i) for i in l.split(" ")] for l in list(communitized_df)]

    project_graph(bigraph_as_list)

    projected=pd.read_csv('py_output.csv',header=None,names=['source','target','weight'],
                        sep=' ',dtype={'source':int,'target':int,'weight':int})
    projected['source']=projected['source'].map(lut)
    projected['target']=projected['target'].map(lut)

    print(f'It took {time.time() - start} seconds')







