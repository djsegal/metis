import os
from github import Github
import pandas as pd
import numpy as np
import time

def make_starred_packages(verbose=False):
  cur_api = Github(os.environ['CLIENT_ID'], os.environ['CLIENT_SECRET'])

  cur_list = cur_api.search_repositories(query='.jl language:julia', sort="stars")

  min_stars = 10

  max_stars = cur_list.get_page(0)[0].stargazers_count

  cur_scalar = 10**np.floor(np.log10(max_stars))

  max_stars = int(
    np.ceil( max_stars / cur_scalar ) * cur_scalar
  )

  beg_stars = min_stars
  end_stars = max_stars

  repo_names = []
  repo_urls = []

  while end_stars > beg_stars :
    if verbose : print(".", end="")
    time.sleep(3)

    cur_list = cur_api.search_repositories(query=f".jl language:julia stars:{beg_stars}..{end_stars}")

    if cur_list.totalCount >= 1000 :
      tmp_stars = int(np.round(np.mean([beg_stars, end_stars])))

      assert tmp_stars != beg_stars
      assert tmp_stars != end_stars

      beg_stars = tmp_stars
      continue

    cur_count = 0
    cur_repos = []

    while True:
      if verbose : print(".", end="")
      time.sleep(3)

      tmp_repos = cur_list.get_page(cur_count)

      if len(tmp_repos) == 0 : break

      cur_count += 1
      cur_repos.extend(tmp_repos)

    for cur_repo in cur_repos:
      repo_names.append(cur_repo.name.replace(".jl", ""))
      repo_urls.append(cur_repo.html_url)

    cur_diff = end_stars - beg_stars

    end_stars = beg_stars
    beg_stars = np.max([min_stars, beg_stars - cur_diff])

  starred_packages = pd.DataFrame(index=[repo_names, repo_urls]).reset_index().drop_duplicates()

  starred_packages.columns = ["name", "url"]

  starred_packages["sort_name"] = starred_packages["name"].str.lower()

  starred_packages = starred_packages.set_index("sort_name")

  starred_packages = starred_packages.sort_index()

  starred_packages = starred_packages.reset_index()

  del starred_packages["sort_name"]

  starred_packages.to_pickle("data/raw_starred.pkl")

  return starred_packages
