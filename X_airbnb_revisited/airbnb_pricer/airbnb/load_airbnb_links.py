import pandas as pd
from time import sleep

from airbnb_pricer.utils.async_run import async_run
from airbnb_pricer.airbnb.skipped_columns import skipped_columns

def load_airbnb_links(cur_links_table):
    cur_urls = cur_links_table.url.tolist()

    cur_tables = async_run(_load_airbnb_link, cur_urls)

    cur_links_table["table"] = cur_tables

    return cur_links_table

def _load_airbnb_link(cur_url):

    tmp_data = pd.read_csv(cur_url, low_memory=False)

    tmp_data = tmp_data.drop(
        columns=[
            tmp_column for tmp_column in tmp_data.columns if tmp_column in skipped_columns
        ]
    )

    sleep(1/3)

    return tmp_data
