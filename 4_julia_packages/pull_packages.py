import os
from git import Repo

def pull_packages():
  repo_dict = {
    "decibans": "https://github.com/svaksha/Julia.jl.git",
    "general": "https://github.com/JuliaRegistries/General.git",
    "metadata": "https://github.com/JuliaLang/METADATA.jl.git"
  }

  for cur_key, cur_value in repo_dict.items():
    print(cur_key)
    cur_dir = f"tmp/{cur_key}"

    if not os.path.exists(cur_dir) :
      Repo.clone_from(cur_value, cur_dir)
      continue

    cur_repo = Repo(cur_dir)
    cur_repo.remote().fetch()
    cur_repo.git.reset('--hard','origin/master')
