import pandas as pd
import matplotlib.pyplot as plt
from inflection import titleize

def make_barh(cur_input, cur_limit=12):
  tmp_input = pd.Series(cur_input)

  top_value_counts = tmp_input.value_counts().sort_values().nlargest(cur_limit)

  for cur_key in top_value_counts.keys():
    top_value_counts[titleize(cur_key)] = top_value_counts.pop(cur_key)

  cur_plot = top_value_counts.plot(kind = 'barh')

  plt.gca().invert_yaxis()

  return cur_plot

def make_two_barh(cur_dict, cur_limit=8):
  for cur_index, (cur_key, cur_value) in enumerate(cur_dict.items()):
    plt.subplot(1,2,cur_index+1)
    make_barh(cur_value,8)
    plt.title(titleize(cur_key))

  plt.gca().invert_xaxis()
  plt.gca().yaxis.tick_right()
