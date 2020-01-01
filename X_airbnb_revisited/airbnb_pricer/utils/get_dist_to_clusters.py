import numpy as np

from time import sleep
from airbnb_pricer.utils.async_run import async_run

mile_per_degree__latitude = 111.32 * 0.621371
mile_per_degree__longitude = 84.35 * 0.621371

def get_dist_to_clusters(location_data, cluster_data):
    location_data = location_data.copy()
    cluster_data = cluster_data.copy()

    location_data["x"] = location_data["lon"] * mile_per_degree__longitude
    location_data["y"] = location_data["lat"] * mile_per_degree__latitude

    cluster_data["x"] = cluster_data["lon"] * mile_per_degree__longitude
    cluster_data["y"] = cluster_data["lat"] * mile_per_degree__latitude

    def _get_cluster_dists(cur_input):
        cur_x, cur_y, cur_is_bkn = cur_input

        data_dict = {
            "center": cluster_data[cluster_data.is_com],
            "hub": cluster_data[
                ~cluster_data.is_com & (cluster_data.is_bkn == cur_is_bkn)
            ]
        }

        sleep(0.01)

        cur_dists = {}

        for cur_key, sub_data in data_dict.items():
            cur_dist = ( sub_data.x - cur_x ) ** 2
            cur_dist += ( sub_data.y - cur_y ) ** 2
            cur_dist = np.min(np.sqrt(cur_dist))

            cur_dists[cur_key] = cur_dist

        return cur_dists

    cluster_dists_iter = list(
        zip(location_data["x"], location_data["y"], location_data["is_brooklyn"])
    )

    dist_list = async_run(
        _get_cluster_dists, cluster_dists_iter
    )

    return dist_list
