import pandas as pd

def merge_packages():

  decibans_df = pd.read_pickle("data/raw_decibans.pkl").drop(columns=["category", "sub_category"])
  general_df = pd.read_pickle("data/raw_general.pkl")
  metadata_df = pd.read_pickle("data/raw_metadata.pkl")
  starred_df = pd.read_pickle("data/raw_starred.pkl")

  decibans_df["type"] = "decibans"
  general_df["type"] = "general"
  metadata_df["type"] = "metadata"
  starred_df["type"] = "starred"

  cur_df = pd.concat([
      decibans_df, general_df, metadata_df, starred_df
  ]).drop_duplicates("name")

  cur_df = cur_df.reset_index(drop=True)

  cur_df["sort_name"] = cur_df["name"].str.lower()

  cur_df = cur_df.set_index("sort_name")

  cur_df = cur_df.sort_index()

  cur_df = cur_df.reset_index()

  del cur_df["sort_name"]

  cur_df.to_pickle("data/raw_merged.pkl")

  return cur_df
