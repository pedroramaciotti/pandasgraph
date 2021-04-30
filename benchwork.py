import pandas as pd
import numpy as np
import os

#############################
# In puts of the function
#############################

projection = 'A_id' # the part of the bipartite whose nodes will be retained in the projection

# Loading a biparte network as a list of edges.
df = pd.read_csv('sample_graphs/sample_bipartite_1.csv')

#############################
# The function
#############################

# Selecting the projection
# Here there are 3 options: either a proper columns has been selected, 
# either an unexisting column has been selected,
# either no column has been.
if projection is None:
    projection=df.columns[0]
elif projection not in df.columns:
    raise ValueError("Selected columns not in graph")

# Lookup table between projected nodes and integer numbering
lut = pd.DataFrame.from_dict({projection:df[projection].unique(),'int_id':np.arange(1,df[projection].nunique()+1,dtype=int)})

# The nodes of part to be projected need integer numbering, starting from 1
df['int_id'] = df[projection].map(pd.Series(index=lut[projection].values,data=lut['int_id'].values))
    
# Writing the bipartite graph in community structure
# Each node of the non-projected side is a "community"
# We write one line per community, each line contains the nodes from the projected side that belong (are connected) 
# to the community
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







