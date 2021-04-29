import pandas as pd
import numpy as np


# # Assigning ids to users in the log
# Log_df['user_node_id'] = Log_df['user_id'].map(pd.Series(index=LogUsers_df['user_id'].values,data=LogUsers_df['user_node_id'].values))
# Log_df['user_node_id'].isna().sum() # -> 0
# # we subtract elements 
# citation_count=Log_df[['user_node_id',top_level_object]].groupby(top_level_object).count()['user_node_id']
# citation_count.size # -> 12.620.446
# (citation_count>1).sum() # -> 1.927.854
# # computing bipartite graph in community structure format
# bipartite_df = Log_df.loc[Log_df[top_level_object].isin(citation_count[citation_count>1].index.values),['user_node_id',top_level_object]]
# bipartite_df.duplicated().sum() # -> 0
# bipartite_df.shape[0] # -> 8.486.251
# bipartite_df.normalized_url.nunique() # -> 1.927.854
# bipartite_df.user_node_id.nunique() # -> 34.872
# bipartite_df.shape[0]/(bipartite_df.normalized_url.nunique()*bipartite_df.user_node_id.nunique())
# # -> density = 0.000126
# bipartite=bipartite_df.groupby(top_level_object)['user_node_id'].apply(lambda n: ' '.join(np.sort(n))).reset_index(drop=True)
# bipartite.shape[0] # -> 1.927.854 AOK
# # Checking that there are no repeated bottom nodes per top nodes
# bipartite.apply(lambda tn: len(tn.split(' '))!=len(set(tn.split(' '))) ).sum() # -> 0, AOK!
# # Deleting URLs cited by the same set of users (in whatever commutation)
# bipartite.duplicated().sum() # -> 340.422 urls/domains are cited by the same set of users
# bipartite=bipartite[~bipartite.duplicated()] # we have to eliminate them
# bipartite.shape[0] # 1.587.432
# # saving to file
# bipartite.to_csv('user_citation_bipartite.csv',header=False,index=False)
# # computing weighted projected graph
# os.system('./comcore1 1 user_citation_bipartite.csv user_citation_projection.csv')
# # reading weighted projected graph file
# projected=pd.read_csv('user_citation_projection.csv',header=None,names=['source','target','weight'],
#                       sep=' ',dtype={'source':str,'target':str,'weight':int})
# pd.concat([projected['source'],projected['target']],axis=0).nunique() # -> 34.872 AOK!
# projected.shape[0] # -> 78.365.661 edges
# projected[['source','target']].duplicated().sum() # -> 0 AOK!
# # Exporting a graph with weight threshold for qualitative inspections
# projected.loc[projected['weight']>=20,['source','target']].to_csv('gephi_user_projected_graph.csv',sep=';',header=False,index=False)