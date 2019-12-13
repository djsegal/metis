import pandas as pd

def make_decibans():
  decibans_db = pd.read_csv("./tmp/decibans/db.csv", header=None)

  for cur_column in decibans_db.columns:
      decibans_db[cur_column] = decibans_db[cur_column].str.strip()
      decibans_db[cur_column] = decibans_db[cur_column].str.strip("/")

  decibans_db.columns = [
      "category", "sub_category", "name", "url", "description"
  ]

  decibans_db = decibans_db.drop(columns="description")

  decibans_db = decibans_db[decibans_db.name.str.endswith(".jl")]
  decibans_db = decibans_db[decibans_db.url.str.endswith(".jl")]

  decibans_db = decibans_db[decibans_db.url.str.contains("github.com")]

  decibans_db["name"] = decibans_db["name"].str.replace(".jl", "")
  decibans_db["sort_name"] = decibans_db["name"].str.lower()

  decibans_db = decibans_db.set_index("sort_name")
  decibans_db = decibans_db.sort_index()
  decibans_db = decibans_db.reset_index()
  del decibans_db["sort_name"]

  decibans_db["work_sub_category"] = decibans_db["sub_category"].str.extract("\[([^\]]+)\]")
  decibans_db["sub_category"] = decibans_db["work_sub_category"].combine_first(decibans_db["sub_category"])
  del decibans_db["work_sub_category"]

  decibans_db["sub_category"] = decibans_db["sub_category"].fillna("Other")

  decibans_db = decibans_db.reindex(columns=["name", "url", "category", "sub_category"])

  decibans_db.loc[
      decibans_db.sub_category.str.isupper() & (
          decibans_db.category.str.lower() == decibans_db.sub_category.str.lower()
      ),
      "sub_category"
  ] = decibans_db[
      decibans_db.sub_category.str.isupper() & (
          decibans_db.category.str.lower() == decibans_db.sub_category.str.lower()
      )
  ].category

  decibans_db.to_pickle("data/raw_decibans.pkl")

  return decibans_db
