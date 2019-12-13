from glob import glob
from collections import OrderedDict
import re
import pandas as pd

def make_general_packages(verbose=False):

  cur_globs = glob("tmp/general/**/**/Package.toml")

  cur_names = list(sorted(map(lambda cur_glob: cur_glob.split("/")[-2], cur_globs), key=lambda cur_name: cur_name.lower()))

  cur_dict = OrderedDict()

  for cur_name in cur_names:
    for cur_glob in cur_globs:
      if f"/{cur_name}/" not in cur_glob : continue

      cur_url = re.search('repo = \"([^\"]+)\"', open(cur_glob).read()).group(1)

      assert cur_url != None

      assert cur_url.endswith(".git")
      cur_url = cur_url.replace(".git", "")

      if not cur_url.endswith(".jl") :
        if verbose : print(cur_name, cur_url)
        continue

      if "gitlab.com" in cur_url : continue
      assert "github.com" in cur_url

      cur_dict[cur_name] = cur_url
      break

  general_df = pd.DataFrame.from_dict(cur_dict, orient="index").reset_index()

  general_df.columns = ["name", "url"]

  general_df.to_pickle("data/raw_general.pkl")

  return general_df
