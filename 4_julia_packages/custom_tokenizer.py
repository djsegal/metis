from nltk.stem.porter import PorterStemmer
import re

from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

porter_stemmer = PorterStemmer()
wnl = WordNetLemmatizer()

from textblob import TextBlob

def custom_tokenizer(str_input):
  tokens = TextBlob(str_input).words

  words = [
      porter_stemmer.stem(
          wnl.lemmatize(
              token.stem()
          )
      )
      for token in tokens
  ]

  return words
