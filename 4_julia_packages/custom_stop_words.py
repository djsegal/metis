from sklearn.feature_extraction import text
from stop_words import get_stop_words
from nltk.corpus import stopwords

stop_list_1 = set(get_stop_words('en'))
stop_list_2 = set(stopwords.words('english'))
stop_list_3 = set(text.ENGLISH_STOP_WORDS.union(["book"]))
stop_list_4 = set([])

custom_stop_words = list(
  stop_list_1 | stop_list_2 | stop_list_3 | stop_list_4
)

custom_stop_words = [
  stop_word.replace("'", "") for stop_word in custom_stop_words
]

custom_stop_words = list(sorted(set(custom_stop_words)))
