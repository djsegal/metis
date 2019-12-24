from bs4 import BeautifulSoup
import pandas as pd

import requests
import datetime

def get_airbnb_links():
    cur_url = "http://insideairbnb.com/get-the-data.html"

    cur_response = requests.get(cur_url)
    cur_soup = BeautifulSoup(cur_response.text, "html.parser")

    for cur_anchor in cur_soup.find_all('a', href=True):
        cur_anchor.replace_with(cur_anchor['href'])

    cur_tables = cur_soup.findAll("table", {"class": "new-york-city"})
    assert len(cur_tables) == 1
    cur_html = str(cur_tables[0])

    cur_table = pd.read_html(cur_html, parse_dates=True)[0]

    assert cur_table["Country/City"].unique().tolist() == ["New York City"]
    cur_table = cur_table[cur_table["File Name"].str.endswith("listings.csv.gz")]

    cur_table.drop(columns=["Country/City","Description"], inplace=True)

    cur_table["url"] = cur_table["File Name"]
    cur_table.drop(columns="File Name", inplace=True)

    cur_dates = cur_table["Date Compiled"].tolist()

    cur_datetimes = []
    cur_months = []
    cur_years = []

    for cur_date in cur_dates:
        assert type(cur_date) == str
        cur_datetime = datetime.datetime.strptime(cur_date, '%d %B, %Y')

        cur_month = cur_datetime.month
        cur_year = cur_datetime.year

        cur_month -= 1

        if cur_month == 0 :
            cur_month = 12
            cur_year -= 1

        cur_datetimes.append(cur_datetime)
        cur_months.append(cur_month)
        cur_years.append(cur_year)

    cur_table["month"] = cur_months
    cur_table["year"] = cur_years
    cur_table["datetime"] = cur_datetimes

    cur_table.drop(columns="Date Compiled", inplace=True)

    cur_table.drop_duplicates(subset=["month","year", "url"], inplace=True)

    cur_table = cur_table[cur_table.year > 2015]
    assert len(cur_table) == len(cur_table.drop_duplicates(subset=["month","year"]))

    return cur_table
