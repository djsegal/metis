import numpy as np
import pandas as pd

from expand_columns import expand_columns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import RidgeCV, LassoCV, ElasticNetCV

import random

from collections import defaultdict

def chunks(l, n):
  num_groups = int(np.ceil(len(l)/n))
  num_per_group = int(np.ceil(len(l)/num_groups))
  n = max(1, n)
  return (l[i*num_per_group:(i+1)*num_per_group] for i in range(num_groups))

def impute_values(tokamak_data):
  impute_simple_values(tokamak_data)
  expand_columns(tokamak_data)

  all_full_columns = list(tokamak_data.dropna(axis=1).columns)

  main_cols = [ tmp_col for tmp_col in all_full_columns if not tmp_col.startswith("_") ]
  side_cols = [ tmp_col for tmp_col in all_full_columns if tmp_col.startswith("_") ]

  cur_col = "prad"
  cur_tok = "D3D"

  main_cols = [ tmp_col for tmp_col in main_cols if tmp_col != cur_col ]
  random.shuffle(side_cols)

  col_list = []

  cur_chunks = [
    main_cols, *chunks(side_cols, len(main_cols)-25)
  ]

  for tmp_list in cur_chunks:
    tmp_list.extend(col_list)

    work_result = _impute_complex_value(
      tokamak_data, tmp_list, cur_col, cur_tok,
      True, False, False, 0.0, True
    )

    print(404, work_result)
    col_list.extend(work_result[1])
    col_list = list(set(col_list))

  print(col_list)

  work_result = _impute_complex_value(
    tokamak_data, col_list, cur_col, cur_tok,
    True, False, True, 0.75, False
  )

  print(work_result)

  return work_result

def impute_simple_values(tokamak_data):
  full_columns = list(tokamak_data.dropna(axis=1).columns)

  partial_columns = [
    work_col for work_col in tokamak_data.columns if work_col not in full_columns
  ]

  for cur_col in partial_columns:
    for cur_tok in set(tokamak_data.tok):
      sub_data = tokamak_data[tokamak_data.tok == cur_tok]
      null_count = np.sum(sub_data[cur_col].isnull())

      if null_count == 0: continue

      if null_count == len(sub_data):

        imputed_label = f"imp_{cur_col}"
        imputed_list = (
          tokamak_data[cur_col].isnull() & ( tokamak_data.tok == cur_tok )
        )

        if imputed_label in tokamak_data.columns:
          imputed_list = list(map(any, zip(
            tokamak_data[imputed_label], imputed_list
          )))

        tokamak_data[imputed_label] = imputed_list

        tokamak_data.loc[
          ( tokamak_data[cur_col].isnull() & ( tokamak_data.tok == cur_tok ) ),
          cur_col
        ] = tokamak_data[cur_col].dropna().median()

        continue

      if null_count / len(sub_data) > 0.7 or len(sub_data) - null_count < 50 :

        imputed_label = f"imp_{cur_col}"
        imputed_list = (
          tokamak_data[cur_col].isnull() & ( tokamak_data.tok == cur_tok )
        )

        if imputed_label in tokamak_data.columns:
          imputed_list = list(map(any, zip(
            tokamak_data[imputed_label], imputed_list
          )))

        tokamak_data[imputed_label] = imputed_list

        tokamak_data.loc[
          ( tokamak_data[cur_col].isnull() & ( tokamak_data.tok == cur_tok ) ),
          cur_col
        ] = sub_data[cur_col].dropna().median()

def impute_complex_values(tokamak_data, col_list, cur_threshold):
  all_full_columns = list(tokamak_data.dropna(axis=1).columns)

  full_columns = [
    work_col for work_col in col_list if work_col in all_full_columns
  ]

  partial_columns = [
    work_col for work_col in col_list if work_col not in full_columns
  ]

  quicken_dict = {}

  for cur_col in partial_columns:
    quicken_dict[cur_col] = {}

    for cur_tok in set(tokamak_data.tok):
      null_data = tokamak_data[tokamak_data[cur_col].isnull() & (tokamak_data.tok == cur_tok)]
      if len(null_data) == 0: continue

      quicken_dict[cur_col][cur_tok] = len(null_data)
    quicken_dict[cur_col]["all"] = np.sum(list(quicken_dict[cur_col].values()))

  run_keys = []
  run_counts = []

  for cur_key, cur_value in quicken_dict.items():
    run_keys.append(cur_key)
    run_counts.append(cur_value["all"])

  run_counts, run_keys = list(zip(*sorted(zip(run_counts, run_keys))))
  print(run_counts)
  print(run_keys)

  work_dict = {}

  for cur_col in run_keys:
    for cur_tok in set(tokamak_data.tok):
      null_data = tokamak_data[tokamak_data[cur_col].isnull() & (tokamak_data.tok == cur_tok)]
      if len(null_data) == 0: continue

      print(cur_col, cur_tok, end="")

      for use_log in [False, True]:
        for use_all in [False, True]:
          work_result = _impute_complex_value(
            tokamak_data, full_columns, cur_col, cur_tok,
            use_log, use_all, False, cur_threshold, True
          )

          if work_result == False: continue
          work_dict[(cur_col, cur_tok, use_log, use_all)] = work_result

      print("")

      best_key = (np.nan, np.nan)
      best_score, best_columns = -np.inf, []

      for cur_key, cur_value in work_dict.items():
        if cur_key[0] != cur_col : continue
        if cur_key[1] != cur_tok : continue

        if cur_value[0] <= best_score: continue

        best_key = cur_key[-2:]
        best_score, best_columns = cur_value

      if best_score <= 0 : continue

      assert len(best_columns) > 0

      print(cur_col, cur_tok, best_score)
      print(best_columns)

      if cur_threshold == 0: continue

      _impute_complex_value(
        tokamak_data, best_columns, cur_col,
        cur_tok, *best_key, True, cur_threshold, True
      )

  return work_dict

def _impute_complex_value(tokamak_data, full_columns, cur_col, cur_tok, use_log, use_all, mutate_data, cur_threshold, do_prune):
  prev_train_scores = []
  prev_test_scores = []

  this_data = tokamak_data[~tokamak_data[cur_col].isnull() & (tokamak_data.tok == cur_tok)]
  that_data = tokamak_data[~tokamak_data[cur_col].isnull() & (tokamak_data.tok != cur_tok)]

  if use_log:
    if len( this_data[ this_data[cur_col] <= 0  ] ) > 0 : return False
    if use_all and len( that_data[ that_data[cur_col] <= 0  ] ) > 0 : return False

  null_data = tokamak_data[tokamak_data[cur_col].isnull() & (tokamak_data.tok == cur_tok)]
  assert len(null_data) > 0

  attempt_count = 0
  skipped_columns = ["tok", cur_col]

  this_y = this_data[cur_col]
  that_y = that_data[cur_col]

  if use_log :
    this_y = np.log(this_y)
    that_y = np.log(that_y)

  max_columns = 200

  skipped_dict = defaultdict(int)

  while do_prune and len(skipped_columns) < len(full_columns):
    print(".", end="", flush=True)

    tmp_columns = [
      work_col for work_col in full_columns if work_col not in skipped_columns
    ]

    if len(tmp_columns) > max_columns:
      tmp_columns = random.sample(tmp_columns, max_columns)

    this_X = this_data[tmp_columns]
    that_X = that_data[tmp_columns]

    X_train, X_test, y_train, y_test = train_test_split(this_X, this_y, test_size=0.2)

    if use_all:
      while len(X_train) < len(that_X):
        X_train = X_train.append(X_train)
        y_train = y_train.append(y_train)

      X_train = X_train.append(that_X)
      y_train = y_train.append(that_y)

    scaler = StandardScaler().fit(X_train)

    X_train = pd.DataFrame(scaler.transform(X_train), columns=this_X.columns)
    X_test = pd.DataFrame(scaler.transform(X_test), columns=this_X.columns)

    cur_cv = LassoCV(cv=3, n_alphas=256, max_iter=100000, tol=1e-6, n_jobs=-1)
    cur_cv.fit(X_train, y_train)

    if cur_cv.dual_gap_ > 1e30:
      return False

    new_skipped = list(X_train.columns[np.abs(cur_cv.coef_) < 1e-8])
    if len(new_skipped) == 0:
      attempt_count += 1
      if attempt_count > 5 : break
    else:
      attempt_count -= 2
      attempt_count = np.max([0, attempt_count])

    for tmp_col in tmp_columns:
      if tmp_col not in new_skipped:
        skipped_dict[tmp_col] = 0
        continue

      skipped_dict[tmp_col] += 1
      if skipped_dict[tmp_col] <= 3 : continue

      assert tmp_col not in skipped_columns
      skipped_columns.append(tmp_col)

    prev_train_scores.append(cur_cv.score(X_train, y_train))
    prev_test_scores.append(cur_cv.score(X_test, y_test))

  if len(skipped_columns) >= len(full_columns): return False

  this_X = this_data[[work_col for work_col in full_columns if work_col not in skipped_columns]]
  that_X = that_data[[work_col for work_col in full_columns if work_col not in skipped_columns]]

  X_train, X_test, y_train, y_test = train_test_split(this_X, this_y, test_size=0.2)
  scaler = StandardScaler().fit(X_train)

  if use_all:
    while len(X_train) < len(that_X):
      X_train = X_train.append(X_train)
      y_train = y_train.append(y_train)

    X_train = X_train.append(that_X)
    y_train = y_train.append(that_y)

  X_train = pd.DataFrame(scaler.transform(X_train), columns=this_X.columns)
  X_test = pd.DataFrame(scaler.transform(X_test), columns=this_X.columns)

  cur_cv = RidgeCV(cv=3, alphas=np.logspace(-4,4,1200))
  cur_cv.fit(X_train, y_train)

  if cur_cv.alpha_ < 1e-5:
    cur_cv = ElasticNetCV(cv=3, n_alphas=256, max_iter=100000, tol=1e-6, n_jobs=-1, random_state=42)
    cur_cv.fit(X_train, y_train)
  else:
    assert cur_cv.alpha_ < 1e+5

  train_score = cur_cv.score(X_train, y_train)
  test_score = cur_cv.score(X_test, y_test)

  if train_score < cur_threshold : return False
  if test_score < cur_threshold : return False

  if np.abs(train_score - test_score) > 0.05:
    print()
    print("************************")
    print(f"overfit ({'log' if use_log else 'lin' } / {'all' if use_all else 'tok' }):", [cur_col, cur_tok, train_score, test_score])
    print("************************")

  if mutate_data:
    in_data = tokamak_data[( tokamak_data.tok == cur_tok ) & tokamak_data[cur_col].isnull() ][this_X.columns]
    in_data = pd.DataFrame(scaler.transform(in_data), columns=this_X.columns)

    imputed_label = f"imp_{cur_col}"
    imputed_list = (
      tokamak_data[cur_col].isnull() & ( tokamak_data.tok == cur_tok )
    )

    if imputed_label in tokamak_data.columns:
      imputed_list = list(map(any, zip(
        tokamak_data[imputed_label], imputed_list
      )))

    tokamak_data[imputed_label] = imputed_list

    predicted_values = cur_cv.predict(in_data)

    if use_log :
      predicted_values = np.exp(predicted_values)

    tokamak_data.loc[
      ( tokamak_data.tok == cur_tok ) & tokamak_data[cur_col].isnull(),
      cur_col
    ] = predicted_values

  # print()
  # print([
  #   cur_col, cur_tok, use_log, use_all,
  #   round(train_score,3), round(test_score,3)
  # ])
  # print(list(map(lambda ts: round(ts,3), prev_train_scores)))
  # print(list(map(lambda ts: round(ts,3), prev_test_scores)))
  # print(this_X.columns.to_list())

  used_columns = [work_col for work_col in full_columns if work_col not in skipped_columns]
  return [test_score, used_columns]
