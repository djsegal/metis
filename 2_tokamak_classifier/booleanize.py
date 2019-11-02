import numpy as np

def booleanize(tokamak_data):
  for cur_col in tokamak_data.columns:
    sub_data = tokamak_data[cur_col]
    if sorted(np.unique(sub_data)) != [0, 1]: continue

    tokamak_data[cur_col] = list(
      map(bool, sub_data)
    )

def unbooleanize(tokamak_data):
  for cur_col in tokamak_data.columns:
    sub_data = tokamak_data[cur_col]
    if sub_data.dtype != bool : continue

    tokamak_data[cur_col] = list(
      map(int, sub_data)
    )
