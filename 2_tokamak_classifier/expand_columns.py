import numpy as np

def expand_columns(tokamak_data):
  init_cols = tokamak_data.columns

  for col in init_cols:
    if any(tokamak_data[col].isnull()) : continue

    if col.startswith("imp_") :
      for other_col in init_cols:
        if not other_col.startswith("tok_") : continue
        tokamak_data[f"_{col}_{other_col}"] = \
          tokamak_data[col] & tokamak_data[other_col]

    if not tokamak_data[col].dtype == float and not tokamak_data[col].dtype == int: continue

    if col.startswith("_") : continue

    if col.lower().startswith("inv_") : continue
    if col.lower().startswith("log_") : continue
    if col.lower().startswith("abs_") : continue

    if col.lower().startswith("zero_") : continue

    if col.lower().startswith("pos_") : continue
    if sorted(np.unique(tokamak_data[col].values)) == [0, 1] : continue

    if len(tokamak_data[tokamak_data[col] == 0]) == 0 :
      tokamak_data[f"inv_{col}"] = 1 / tokamak_data[col]

      if len(tokamak_data[tokamak_data[col] < 0]) > 0 :
        tokamak_data[f"inv_abs_{col}"] = 1 / np.abs(tokamak_data[col])

      if len(tokamak_data[tokamak_data[f"inv_{col}"] <= 0]) == 0 :
        if col != "pgasz" :
          tokamak_data[f"log_inv_{col}"] = np.log10(tokamak_data[f"inv_{col}"])

    if len(tokamak_data[tokamak_data[col] <= 0]) == 0 :
      if col != "pgasz" :
        tokamak_data[f"log_{col}"] = np.log10(tokamak_data[col])

      continue

    if len(tokamak_data[tokamak_data[col] < 0]) == 0 : continue

    tokamak_data[f"abs_{col}"] = np.abs(tokamak_data[col])
    tokamak_data[f"pos_{col}"] = list(tokamak_data[col] == tokamak_data[f"abs_{col}"])

    if len(tokamak_data[tokamak_data[col] == 0]) == 0 :
      tokamak_data[f"log_{col}"] = np.log10(np.abs(tokamak_data[col]))

  for col in tokamak_data.columns:
    if any(tokamak_data[col].isnull()) : continue
    if not tokamak_data[col].dtype == float and not tokamak_data[col].dtype == int: continue

    cur_zero_flags = tokamak_data[col] == 0
    if sum(cur_zero_flags) < 500 : continue

    tokamak_data[f"zero_{col}"] = cur_zero_flags
