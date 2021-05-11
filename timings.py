
import pandas as pd
import numpy as np
import os
import timeit

def run():
    projection = 'A_id' # the part of the bipartite whose nodes will be retained in the projection
    df = pd.read_csv('sample_graphs/sample_bipartite_1.csv')

    # Lookup table between projected nodes and integer numbering
    lut = pd.DataFrame.from_dict({projection:df[projection].unique(),'int_id':np.arange(1,df[projection].nunique()+1,dtype=int)})

    # The nodes of part to be projected need integer numbering, starting from 1
    df['int_id'] = df[projection].map(pd.Series(index=lut[projection].values,data=lut['int_id'].values))
        
    df['int_id']=df['int_id'].astype(str)
    non_projected_part = [c for c in df.columns[:-1] if c not in [projection,'int_id']][0]
    communitized_df = df[['int_id',non_projected_part]].groupby(non_projected_part)['int_id'].apply(lambda n: ' '.join(np.sort(n))).reset_index(drop=True)

    # saving bipartite in community structure format to file
    communitized_df.to_csv('input.csv',header=False,index=False)
    # computing weighted projected graph
    os.system('./pandasgraph/comcore1 1 input.csv output.csv')
    # reading weighted projected graph file
    projected=pd.read_csv('output.csv',header=None,names=['source','target','weight'],
                        sep=' ',dtype={'source':int,'target':int,'weight':int})
    projected['source']=projected['source'].map(pd.Series(index=lut['int_id'].values,data=lut[projection].values))
    projected['target']=projected['target'].map(pd.Series(index=lut['int_id'].values,data=lut[projection].values))


def build_id_column_1(df):

    projection = "A_id"
    lut = pd.DataFrame.from_dict({projection:df[projection].unique(),'int_id':np.arange(1,df[projection].nunique()+1,dtype=int)})
    df['int_id'] = df[projection].map(pd.Series(index=lut[projection].values,data=lut['int_id'].values))
    return df
    

def build_id_column_2(df):

    projection = "A_id"
    lut = {node: i + 1 for i, node in enumerate(df[projection].unique())}
    df['int_id'] = df[projection].map(lut)
    return df
        
def build_id_column_3(df):

    projection = "A_id"
    lut = pd.Series({node: i + 1 for i, node in enumerate(df[projection].unique())})
    df['int_id'] = df[projection].map(lut)
    return df


if __name__ == "__main__":

    SETUP_CODE = '''
from random import randint

import pandas as pd
import numpy as np

from __main__ import build_id_column_2

df = pd.DataFrame([(f"a{randint(0, 10000)}", f"b{randint(0, 100000)}") for x in range(1000000)], columns=["A_id", "B_id"])
    '''

    times = timeit.repeat(setup = SETUP_CODE,
                        stmt = "build_id_column_2(df)",
                        repeat = 2,
                        number = 1000)
    
    print(times)





