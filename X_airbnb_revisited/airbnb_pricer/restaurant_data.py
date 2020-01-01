from bs4 import BeautifulSoup
import pandas as pd

import datetime
import geopandas
import pickle

class RestaurantData():
  def __init__(self):
    self.data = _make_restaurant_data()
    self.save()

  def save(self):
    pickle.dump(self, open( "data/restaurant.pkl", "wb" ) )

  def load():
    return pickle.load(open( "data/restaurant.pkl", "rb" ))

  def boot():
    try:
      return RestaurantData.load()
    except:
      print("downloading restaurant...")
      return RestaurantData()

def _make_restaurant_data():
  restaurant_data = pd.read_csv(
    "https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv"
  )

  restaurant_data.columns = map(str.lower, restaurant_data.columns)
  restaurant_data.columns = map(lambda data_col: data_col.replace(" ", "_"), restaurant_data.columns)

  if "cuisine_description" in restaurant_data.columns:
    restaurant_data["cuisine"] = restaurant_data["cuisine_description"]
    del restaurant_data["cuisine_description"]

  used_list = [
    'camis', 'dba', 'boro', 'zipcode', 'cuisine',
    'grade', 'grade_date', 'latitude', 'longitude'
  ]

  used_list = [
    used_column for used_column in used_list
    if used_column in restaurant_data.columns
  ]

  restaurant_data = restaurant_data[used_list].copy()

  restaurant_data = restaurant_data[
    ( restaurant_data["boro"] == "Manhattan" ) |
    ( restaurant_data["boro"] == "Brooklyn" )
  ]

  restaurant_data = restaurant_data[
    restaurant_data.grade == "A"
  ].drop("grade", axis=1)

  grade_year = restaurant_data["grade_date"].map(
    lambda cur_date: datetime.datetime.strptime(cur_date, "%m/%d/%Y").year
  )

  restaurant_data = restaurant_data[grade_year > 2016].drop("grade_date", axis=1)

  restaurant_data["dba"] = restaurant_data.dba.str.lower()

  restaurant_data = restaurant_data.dropna(subset=[
    "zipcode", "latitude", "longitude"
  ])

  restaurant_data["zipcode"] = restaurant_data.zipcode.astype(int)

  restaurant_data = restaurant_data.drop_duplicates(subset=["camis"])

  restaurant_data = geopandas.GeoDataFrame(
    restaurant_data,
    geometry=geopandas.points_from_xy(
      restaurant_data.longitude, restaurant_data.latitude
    )
  )

  restaurant_data = restaurant_data.drop(
    columns=["camis", "latitude", "longitude"]
  )

  return restaurant_data
