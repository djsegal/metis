def one_hot(tokamak_data):
  one_hot_auxheat(tokamak_data)
  one_hot_elmtype(tokamak_data)
  one_hot_phase(tokamak_data)
  one_hot_walmat(tokamak_data)
  one_hot_config(tokamak_data)
  one_hot_divmat(tokamak_data)
  one_hot_limmat(tokamak_data)
  one_hot_tok(tokamak_data)

  tokamak_data.columns = tokamak_data.columns.str.lower()
  tokamak_data.columns = tokamak_data.columns.str.replace("-", "_")

def one_hot_auxheat(tokamak_data):
  auxheat_classes = ['EC', 'ECIC', 'IC', 'NB', 'NBIC', 'NONE']

  assert auxheat_classes == sorted(list(tokamak_data.auxheat.value_counts().index))

  auxheat_classes = ["NB", "IC"]

  for work_class in auxheat_classes:
    tokamak_data[f"auxheat_{work_class}"] = \
      tokamak_data.auxheat.str.contains(work_class)

  tokamak_data.drop(columns=["auxheat"], inplace=True)

def one_hot_elmtype(tokamak_data):
  elmtype_classes = ['', 'NONE', 'TYPE-?', 'TYPE-I', 'TYPE-III', 'TYPE-RF', 'UNKNOWN']

  assert elmtype_classes == sorted(list(tokamak_data.elmtype.value_counts().index))

  elmtype_classes = ["NONE", "TYPE-III"]

  tokamak_data["elmtype_TYPE-I"] = \
    tokamak_data.elmtype == "TYPE-I"

  for work_class in elmtype_classes:
    tokamak_data[f"elmtype_{work_class}"] = \
      tokamak_data.elmtype.str.contains(work_class)

  tokamak_data.drop(columns=["elmtype"], inplace=True)

def one_hot_phase(tokamak_data):
  phase_classes = ['H', 'HGELM', 'HSELM', 'HGELMH', 'HSELMH']

  assert phase_classes == list(tokamak_data.phase.value_counts().index)

  phase_classes = ["GELM", "SELM"]

  for work_class in phase_classes:
    tokamak_data[f"phase_{work_class}"] = \
      tokamak_data.phase.str.contains(work_class)

  tokamak_data.drop(columns=["phase"], inplace=True)

def one_hot_walmat(tokamak_data):
  walmat_classes = ['C', 'CSS', 'IN', 'IN/C', 'SS']

  assert walmat_classes == sorted(list(tokamak_data.walmat.value_counts().index))

  walmat_classes = ["C", "SS", "IN"]

  for work_class in walmat_classes:
    tokamak_data[f"walmat_{work_class}"] = \
      tokamak_data.walmat.str.contains(work_class)

  tokamak_data.drop(columns=["walmat"], inplace=True)

def one_hot_config(tokamak_data):
  config_classes = ['BOT', 'DN', 'IW', 'LIM', 'MAR', 'SN', 'SN(L)', 'SN(U)', 'SNL', 'TOP']

  assert config_classes == sorted(list(tokamak_data.config.value_counts().index))

  config_classes = ["SN", "DN"]

  for work_class in config_classes:
    tokamak_data[f"config_{work_class}"] = \
      tokamak_data.config.str.contains(work_class)

  tokamak_data.drop(columns=["config"], inplace=True)

def one_hot_divmat(tokamak_data):
  divmat_classes = ['BE', 'C', 'C/BE', 'CC', 'MO', 'NONE', 'SS', 'TI1', 'TI2', 'W']

  assert divmat_classes == sorted(list(tokamak_data.divmat.value_counts().index))

  divmat_classes = ["C", "W", "TI", "SS", "BE"]

  for work_class in divmat_classes:
    tokamak_data[f"divmat_{work_class}"] = \
      tokamak_data.divmat.str.contains(work_class)

  tokamak_data.drop(columns=["divmat"], inplace=True)

def one_hot_limmat(tokamak_data):
  limmat_classes = ['BE', 'C', 'MO', 'NONE']

  assert limmat_classes == sorted(list(tokamak_data.limmat.value_counts().index))

  limmat_classes = ["C", "BE"]

  for work_class in limmat_classes:
    tokamak_data[f"limmat_{work_class}"] = \
      tokamak_data.limmat.str.contains(work_class)

  tokamak_data.drop(columns=["limmat"], inplace=True)


def one_hot_tok(tokamak_data):
  tok_classes = [
    'ASDEX','AUG','CMOD','D3D','JET','JFT2M',
    'JT60U','NSTX','PBXM','PDX','TCV','TDEV','TFTR'
  ]

  assert tok_classes == sorted(list(tokamak_data.tok.value_counts().index))

  for work_class in tok_classes:
    tokamak_data[f"tok_{work_class}"] = \
      tokamak_data.tok.str.contains(work_class)


