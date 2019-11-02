import numpy as np
from booleanize import booleanize, unbooleanize

def remove_columns(tokamak_data):
  unbooleanize(tokamak_data)

  drop_columns = []

  for cur_index, this_col in enumerate(tokamak_data.columns):
    if "_vol_2" in this_col or "_vol_3" in this_col:
      drop_columns.append(this_col)
      continue

    if any(tokamak_data[this_col].isnull()) : continue
    if not tokamak_data[this_col].dtype == float and not tokamak_data[this_col].dtype == int: continue

    this_vec = tokamak_data[this_col]
    this_min = np.min(np.abs(this_vec[this_vec != 0]))
    for that_col in tokamak_data.columns[0:cur_index]:
      if that_col in drop_columns : continue

      if any(tokamak_data[that_col].isnull()) : continue
      if not tokamak_data[that_col].dtype == float and not tokamak_data[that_col].dtype == int: continue

      that_vec = tokamak_data[that_col]
      that_min = np.min(np.abs(that_vec[that_vec != 0]))

      total_min = np.min([this_min, that_min]) / 100
      if np.allclose(this_vec, that_vec, atol=total_min, equal_nan=True):
        if len(this_col) > len(that_col):
          drop_columns.append(this_col)
        else:
          drop_columns.append(that_col)
        break

  booleanize(tokamak_data)

  for cur_index, this_col in enumerate(tokamak_data.columns):
    if any(tokamak_data[this_col].isnull()) : continue
    if not tokamak_data[this_col].dtype == bool : continue

    for that_col in tokamak_data.columns[0:cur_index]:
      if not tokamak_data[that_col].dtype == bool : continue
      if not all(tokamak_data[this_col] == ~tokamak_data[that_col]) : continue

      if len(this_col) > len(that_col):
        drop_columns.append(this_col)
      else:
        drop_columns.append(that_col)
      break

  for col in tokamak_data.columns:
    if len(tokamak_data[col].value_counts()) > 1 : continue
    drop_columns.append(col)

  drop_columns = list(set(drop_columns))
  tokamak_data.drop(columns=drop_columns, inplace=True)
