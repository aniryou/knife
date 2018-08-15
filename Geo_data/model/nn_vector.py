import math

import numpy as np
import pandas as pd


def distance(lat_orig, lon_orig, lat_dest, lon_dest):
    radius = 6371 # km
    dlat = math.radians(lat_dest-lat_orig)
    dlon = math.radians(lon_dest-lon_orig)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat_orig)) \
        * math.cos(math.radians(lat_dest)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d

DISTANCE = np.vectorize(distance, excluded=['lat_dest', 'lon_dest'])

df = pd.read_hdf("data/Main_final_cleaned_316.hdf")


pt = np.array([44.7529478,-7.0088461])
df['distances'] = DISTANCE(df['lat'],df['lon'], pt[0], pt[1])

df[df.distances<200].shape