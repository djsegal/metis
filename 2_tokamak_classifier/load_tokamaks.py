import pandas as pd
import numpy as np

from impute_values import impute_values
from booleanize import booleanize
from one_hot import one_hot

skipped_reactors = [
  "COMPASS", "MAST", "START",
  "T10", "TEXTOR", "TUMAN3M"
]

def load_tokamaks():
  tokamak_data = pd.read_csv("./tokamak_shots.csv", low_memory=False)

  tokamak_data.columns = tokamak_data.columns.str.lower()
  tokamak_data.columns = tokamak_data.columns.str.replace("-", "_")

  for cur_key in tokamak_data.columns:
    try:
      tokamak_data[cur_key] = tokamak_data[cur_key].str.strip()
    except:
      continue

  tokamak_data = tokamak_data[tokamak_data.phase.str.startswith("H")]

  tokamak_data = tokamak_data[~tokamak_data.tok.isin(skipped_reactors)]

  tokamak_data.date[tokamak_data.date % 100 == 0] = tokamak_data.date[tokamak_data.date % 100 == 0] + 1

  tokamak_data["seldb3"] = tokamak_data.seldb3.astype(int)
  tokamak_data["is_good"] = list(map(int,( tokamak_data.seldb3 == 1111111111 )))

  drop_columns = [
      "area", "bepdia", "bepmhd", "bgasa2", "bgasz2", "bmhdmdia",
      "bsource", "bsource2", "coctr", "dalfdv", "dalfmp",
      "db2p5", "db2p8", "db3is", "db3v5", "deltal", "deltau",
      "divname", "dwdia", "dwmhd", "echloc", "echmode", "elmdur",
      "elmfreq", "elmint", "elmmax", "enbi", "evap", "hmws2003",
      "iae2000n", "iae2000x", "iaea92", "icanten", "icform",
      "icscheme", "igradb", "iseq", "lcupdate", "lhtime", "ne0",
      "ne0tsc", "nelform", "palpha", "pellet", "pfloss", "pinj2",
      "plth", "premag", "rmag", "seldb1", "seldb2", "seldb2x",
      "seldb3", "seldb3x", "seplim", "shot", "spin", "t1", "t2",
      "taudia", "taumhd", "tauth1", "tauth2", "te0", "ti0",
      "time_id", "tok_id", "torq", "tpi", "vsurf", "vtor0",
      "vtorimp", "vtorv", "wdia", "wekin", "wficform", "wficrh",
      "wficrhp", "wfpar", "wfper", "wikin", "wkin", "xgasa",
      "xgasz", "zeff", "zeffneo",
      "bgasa", "bgasz", "wfform",
      "h89", "hiter96l", "h93", "hiter92y", "hipb98y3",
      "heps97", "hipb98y", "hipb98y1", "hipb98y2", "hipb98y4",
      "indent", "echfreq", "ieml", "pecrh", "picrh",
      "dneldt", "icfreq"
  ]

  tokamak_data.drop(columns=drop_columns, inplace=True)

  tokamak_data.replace([np.inf, -np.inf], np.nan, inplace=True)

  tokamak_data.dropna(axis=1, how="all", inplace=True)

  force_numerics(tokamak_data)
  force_drops(tokamak_data)

  tok_set = set(tokamak_data.tok)

  print(len(tok_set), "Tokamaks")

  for tok in set(tokamak_data.tok):
      dtp = pd.to_datetime(tokamak_data[tokamak_data.tok==tok].date, format='%Y%m%d')
      print([tok,len(dtp),f"{np.min(dtp).year} - {np.max(dtp).year}"])


  tokamak_data.drop(columns=["date"], inplace=True)

  one_hot(tokamak_data)
  booleanize(tokamak_data)

  print_dataframe = pd.DataFrame()

  print_dataframe["good"] = [
      len(tokamak_data[tokamak_data.is_good & (tokamak_data.tok == "JET")]),
      len(tokamak_data[tokamak_data.is_good & (tokamak_data.tok != "JET")]),
      len(tokamak_data[tokamak_data.is_good])
  ]

  print_dataframe["bad"] = [
      len(tokamak_data[~tokamak_data.is_good & (tokamak_data.tok == "JET")]),
      len(tokamak_data[~tokamak_data.is_good & (tokamak_data.tok != "JET")]),
      len(tokamak_data[~tokamak_data.is_good])
  ]

  print_dataframe.index = ["jet", "else", "total"]

  print()
  print(print_dataframe)

  return tokamak_data

def force_numerics(tokamak_data):

  numeric_keys = []

  for cur_key in tokamak_data.columns:
    try:
      tokamak_data[cur_key] = tokamak_data[cur_key].str.strip()
    except:
      numeric_keys.append(cur_key)

  string_keys = [
    work_key for work_key in tokamak_data.columns if work_key not in numeric_keys
  ]

  for cur_key in string_keys:

    tmp_col = tokamak_data[cur_key].copy().dropna()
    cur_output = [
      cur_value for cur_value in set(tmp_col.values)
      if cur_value != ''
    ]

    is_int = False
    is_flt = False

    try:
      cur_output = [int(str(x)) for x in cur_output]
      is_int = True
    except:
      pass

    if not is_int:
      try:
        cur_output = [float(str(x)) for x in cur_output]
        is_flt = True
      except:
        pass

    if not is_int and not is_flt: continue

    tokamak_data.loc[tokamak_data[cur_key] == "", cur_key] = np.nan

    if is_flt:
      tokamak_data[cur_key] = [float(x) for x in tokamak_data[cur_key]]
      continue

    cur_list = []
    for work_value in tokamak_data[cur_key]:
      if pd.isnull(work_value):
        cur_list.append(np.nan)
      else:
        cur_list.append(int(work_value))

    tokamak_data[cur_key] = cur_list

def force_drops(tokamak_data):
  bad_cols = []

  jet_data = tokamak_data[tokamak_data.tok == "JET"]
  cmod_data = tokamak_data[tokamak_data.tok == "CMOD"]

  for col in tokamak_data.columns:
    is_bad = False

    is_bad |= len(tokamak_data[col].unique()) == 1
    is_bad |= len(set(tokamak_data.dropna(subset=[col]).tok)) < 8

    is_bad |= len(jet_data[~jet_data[col].isnull()]) == 0
    is_bad |= len(cmod_data[~cmod_data[col].isnull()]) == 0

    if not is_bad: continue

    bad_cols.append(col)
    tokamak_data.drop(col,inplace=True,axis=1)
