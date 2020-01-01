from bs4 import BeautifulSoup
import pandas as pd

import requests
import pickle

class ZipCodeData():
  def __init__(self):
    self.data = _make_zip_data()
    self.save()

  def save(self):
    pickle.dump(self, open( "data/zip_code.pkl", "wb" ) )

  def load():
    return pickle.load(open( "data/zip_code.pkl", "rb" ))

  def boot():
    try:
      return ZipCodeData.load()
    except:
      print("downloading zip...")
      return ZipCodeData()

def _make_zip_data():
  cur_url_list = [
      "http://zipatlas.com/us/ny/new-york/zip-code-comparison/population-density.htm",
      "http://zipatlas.com/us/ny/brooklyn/zip-code-comparison/population-density.htm"
  ]

  cur_table_list = []

  for cur_url in cur_url_list:
      cur_response = requests.get(cur_url)
      cur_soup = BeautifulSoup(cur_response.text, "html.parser")

      cur_html = str(cur_soup.findAll("td", {"class": "report_data"})[0].find_parent("table"))

      cur_table_list.append(
          pd.read_html(cur_html, parse_dates=True, header=0)[0]
      )

  cur_table = pd.concat(cur_table_list)

  cur_table["sq_mile"] = cur_table["Population"] / cur_table["People / Sq. Mile"]

  cur_table = cur_table[ cur_table.sq_mile < 5 ]
  cur_table = cur_table[ cur_table.sq_mile > 0.1 ]

  cur_table = cur_table.drop(columns=["sq_mile"])

  cur_table = cur_table.drop(columns=["#","Location","City", "Population", "National Rank"]).sort_values(by="Zip Code").reset_index(drop=True)

  cur_table.columns = ["zipcode", "density"]

  return cur_table
