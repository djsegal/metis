import re
import string

from unidecode import unidecode
from custom_stop_words import custom_stop_words

def clean_text(cur_string):
  cur_string = unidecode(cur_string)

  cur_string = cur_string.lower().strip()

  cur_string = cur_string.replace("'", "")

  cur_string = re.sub(r"\S*@\S*\s?", "", cur_string)

  cur_string = re.sub(r'[\"\:\.\!\?\(\)\-\–\—\d\,]', " ", cur_string)

  for cur_punctuation in string.punctuation:
    cur_string = cur_string.replace(cur_punctuation, " ")

  cur_split = cur_string.split()

  cur_split = [
    cur_term for cur_term in cur_split if len(cur_term) >= 3
  ]

  cur_split = [
    cur_term for cur_term in cur_split if cur_term not in custom_stop_words
  ]

  cur_string = " ".join(cur_split)

  return cur_string
