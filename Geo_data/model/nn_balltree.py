import numpy as np
import pandas as pd
from sklearn.neighbors import BallTree


df = pd.read_hdf("data/Main_final_cleaned_316.hdf")

b = BallTree(np.deg2rad(df[['lat','lon']]))

pt = np.deg2rad(np.array([44.7529478,-7.0088461]))
ind, dist = b.query_radius(pt, 200/6371.0, return_distance=True,sort_results=True)
ind[0].shape
dist*6371.0
