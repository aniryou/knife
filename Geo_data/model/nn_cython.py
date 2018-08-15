from distance_fast import dist

import pandas as pd
import numpy as np

df = pd.read_hdf("data/Main_final_cleaned_316.hdf")

pt = np.array([[44.7529478,-7.0088461]])
df['distances'] = dist(np.rad2deg(df[['lat','lon']].values), pt)
df[:10]

df[df.distances<200].shape