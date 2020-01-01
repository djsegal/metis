import numpy as np
import pandas as pd

import geopandas
import pickle

from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

class ClusterData():
    def __init__(self, cur_data):
        all_data = _make_cluster_data(cur_data, 1, None)
        bkn_data = _make_cluster_data(cur_data, 10, True)
        nyc_data = _make_cluster_data(cur_data, 13, False)

        all_data["is_com"] = True
        bkn_data["is_bkn"] = True

        self_data = pd.concat([all_data, nyc_data, bkn_data], ignore_index=True, sort=False)

        self_data["is_com"] = self_data.is_com.fillna(False)
        self_data["is_bkn"] = self_data.is_bkn.fillna(False)

        self.data = self_data

        self.save()

    def save(self):
        pickle.dump(self, open( "data/clusters.pkl", "wb" ) )

    def load():
        return pickle.load(open( "data/clusters.pkl", "rb" ))

    def boot():
        try:
            return ClusterData.load()
        except:
            print("buidling clusters...")
            return ClusterData()

def _make_cluster_data(cur_data, n_clusters, is_brooklyn):
    cluster_gdf = cur_data[["id","price"]].copy()
    cluster_gdf["price"] = np.log10(cluster_gdf["price"])

    cluster_gdf = cluster_gdf.groupby("id").median()
    cluster_cols = ["price","geometry","is_brooklyn"]

    merge_data = cur_data[["id", *cluster_cols]].drop("price", axis=1)
    cluster_gdf = cluster_gdf.merge(merge_data, on="id", how="left")[cluster_cols]
    cluster_gdf = geopandas.GeoDataFrame(cluster_gdf)

    cluster_gdf["longitude"] = cluster_gdf.geometry.map(lambda cur_geom: cur_geom.x)
    cluster_gdf["latitude"] = cluster_gdf.geometry.map(lambda cur_geom: cur_geom.y)

    if is_brooklyn == True: cluster_gdf = cluster_gdf[cluster_gdf.is_brooklyn]
    if is_brooklyn == False: cluster_gdf = cluster_gdf[~cluster_gdf.is_brooklyn]

    cluster_gdf = cluster_gdf.drop("geometry", axis=1)

    cur_scaler = StandardScaler()

    cur_kmeans = KMeans(
      n_clusters=n_clusters, n_jobs=-1, random_state=42
    )

    cluster_pipeline = Pipeline([
        ("scaler", cur_scaler),
        ("kmeans", cur_kmeans)
    ])

    cluster_fit = cluster_pipeline.fit(cluster_gdf)

    cur_prices = []
    cur_lat_list = []
    cur_long_list = []

    cur_transform = cur_scaler.inverse_transform
    cur_centers = cur_kmeans.cluster_centers_

    for cur_row in cur_transform(cur_centers):
        cur_price = cur_row[0]
        if cur_price < cluster_gdf.price.median() : continue
        cur_prices.append(cur_price)

        cur_long, cur_lat = cur_row[-2:]
        cur_lat_list.append(cur_lat)
        cur_long_list.append(cur_long)

    cluster_gdf = pd.DataFrame.transpose(
      pd.DataFrame(data=[cur_lat_list, cur_long_list, 10 ** np.array(cur_prices)])
    )

    cluster_gdf.columns = ["lat", "lon", "price"]

    cluster_gdf = geopandas.GeoDataFrame(
        cluster_gdf, geometry=geopandas.points_from_xy(cluster_gdf.lon, cluster_gdf.lat)
    )

    return cluster_gdf
