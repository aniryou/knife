import pandas as pd
import numpy as np
from datetime import datetime

# Serialization format
#%timeit pd.read_hdf("data/Main_final_cleaned_316.hdf")
#%timeit pd.read_table("data/Main_final_cleaned_316.tsv")


df = pd.read_hdf("data/Main_final_cleaned_316.hdf")
df[:10]

# Ranking 1: Find ports with most incoming trips
df_tmp = df.groupby(['port_id_orig'])['trip_id'].size().reset_index()
df_tmp.sort_values(by=0, ascending=False).head(10)

del df_tmp


# Ranking 2: Find terminals with most incoming trips, for each terminal in 316
df_trips = pd.read_hdf("data/HIST_Trips.hdf")
df2 = df.merge(df_trips, on='trip_id', how='inner')

df_tmp = df2.groupby(['berth_in_id_dest','berth_in_id_orig'])['trip_id'].size().reset_index()
df_tmp.sort_values(by=['berth_in_id_dest',0], ascending=[True,False], inplace=True)
df_tmp[:10]

# Rank top 3
df_tmp2 = df_tmp.groupby(['berth_in_id_dest'],sort=False).head(3)
df_tmp2[:10]

# Rank top N percentile
df_tmp3 = df_tmp.copy(deep=True)
df_tmp3['percent_traffic'] = df_tmp.groupby(['berth_in_id_dest'],sort=False)[0].apply(lambda x: x/sum(x))
df_tmp3['percent_traffic_cum'] = df_tmp3.groupby('berth_in_id_dest')['percent_traffic'].cumsum()
df_tmp4 = df_tmp3[df_tmp3['percent_traffic_cum']<=0.2]

del df2
del df_tmp
del df_tmp2
del df_tmp3
del df_tmp4


# Lookup: Port Names
df_ports = pd.read_table("data/ports.tsv")
df3 = df.merge(df_ports[['port_ID','port_name']], left_on='port_id_orig',right_on='port_ID', how='left')
df3 = df3.merge(df_ports[['port_ID','port_name']], left_on='port_id_dest',right_on='port_ID', how='left', suffixes=['_orig','_dest'])


# Summarising data
df = pd.read_hdf("/Users/anil/src/knife/Geo_data/data/Points_In_Polygon.hdf")
df[np.all([df.imo==7905584, pd.notnull(df.Unique_ID)], axis=0)][:10]
df.sort_values(by=['imo','timestamp_position','Unique_ID'],inplace=True)
df = df.drop_duplicates(subset=['imo','timestamp_position'],keep='first')

df_1 = df.shift(1)
df['flag'] = np.any([df.imo!=df_1.imo,df.Unique_ID!=df_1.Unique_ID], axis=0).astype(int)

df.flag = df.flag.cumsum()
df_head = df.groupby('flag').head(1)
df_tail = df.groupby('flag').tail(1)

df_tmp = pd.merge(df_head,df_tail,on=['imo','name','flag','Unique_ID'],suffixes=['_in','_out'])
df_voyages = df_tmp[pd.notnull(df_tmp.Unique_ID)]
df_voyages[:10]

# Summarising data: patching up
df_voyages[np.all([df_voyages.imo==8420907, df_voyages.timestamp_position_in>=datetime(2016,10,1), \
                   df_voyages.timestamp_position_in<=datetime(2016,10,3)], axis=0)]

df_voyages_1 = df_voyages.shift(-1)
df_voyages_1['identical_to_prv'] = np.all([df_voyages.imo==df_voyages_1.imo, df_voyages.Unique_ID==df_voyages_1.Unique_ID, (df_voyages_1['timestamp_position_in'] - df_voyages['timestamp_position_out']).apply(lambda x: x.total_seconds()/60.0/60 <= 3)], axis=0)==True
df_voyages['identical_to_prv'] = df_voyages_1['identical_to_prv'].shift(1)
ix_identical_next = df_voyages_1[df_voyages_1['identical_to_prv']].index
df_voyages.ix[ix_identical_next,['timestamp_position_out']] = df_voyages_1[df_voyages_1['identical_to_prv']]['timestamp_position_out']
df_voyages = df_voyages[~(df_voyages['identical_to_prv']==True)]
