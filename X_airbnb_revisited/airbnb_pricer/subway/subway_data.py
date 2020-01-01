from bs4 import BeautifulSoup
import pandas as pd

import geopandas
import pickle

import numpy as np

from airbnb_pricer.subway.group_subway_lines import subway_lines, group_subway_lines

class SubwayData():
  def __init__(self):
    self.data = _make_subway_data()
    self.save()

  def save(self):
    pickle.dump(self, open( "data/subway.pkl", "wb" ) )

  def load():
    return pickle.load(open( "data/subway.pkl", "rb" ))

  def boot():
    try:
      return SubwayData.load()
    except:
      print("downloading subway...")
      return SubwayData()

def _make_subway_data():

  subway_data = pd.read_csv(
    "https://data.cityofnewyork.us/api/views/kk4q-3rt2/rows.csv"
  )

  subway_data.columns = map(str.lower, subway_data.columns)

  subway_data = subway_data.drop(columns=["url", "objectid", "notes"])

  def _subway_line_split(cur_line):
    split_line = cur_line.split("-")

    split_line = [
      sub_line for sub_line in split_line if len(sub_line) == 1 and sub_line != "H"
    ]

    return split_line

  subway_data["lines"] = subway_data.line.str.upper().map(_subway_line_split)

  subway_data = subway_data[subway_data.lines.map(len) > 0]

  subway_data["groups"] = subway_data.lines.map(group_subway_lines)

  subway_data["the_geom"] = subway_data.the_geom.str.extract(r"POINT \((.*)\)")

  cur_longitude, cur_latitude = list(map(list,zip(*subway_data["the_geom"].str.split().values)))

  cur_longitude = list(map(float, cur_longitude))
  cur_latitude = list(map(float, cur_latitude))

  subway_data = geopandas.GeoDataFrame(
    subway_data, geometry=geopandas.points_from_xy(cur_longitude, cur_latitude)
  )

  subway_data = subway_data.drop(columns=["the_geom","line"])

  return subway_data
