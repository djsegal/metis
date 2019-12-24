import pandas as pd
import geopandas

def compile_airbnb_data(cur_link_table):
    cur_tables = []

    for cur_row in cur_link_table.itertuples():
        tmp_table = cur_row.table.copy()

        tmp_table["month"] = cur_row.month
        tmp_table["year"] = cur_row.year
        tmp_table["datetime"] = cur_row.datetime

        cur_tables.append(tmp_table)

    cur_data = pd.concat(cur_tables)

    cur_data = cur_data.sort_values(by=["id", "datetime"], ascending=False).reset_index(drop=True)

    cur_data = cur_data.drop(columns=["host_id", "first_review", "last_review"])

    print(len(cur_data))

    cur_selector = cur_data.groupby("id")["zipcode"].nunique()
    cur_selector = cur_selector[ cur_selector == 1 ]

    cur_data = cur_data[cur_data.id.isin(cur_selector.index)]

    print(len(cur_data))

    cur_data = cur_data[cur_data.room_type == "Entire home/apt"]
    cur_data = cur_data.drop(columns = ["room_type"])

    print(len(cur_data))

    cur_data = cur_data[cur_data.property_type == "Apartment"]
    cur_data = cur_data.drop(columns = ["property_type"])

    print(len(cur_data))

    cur_data = cur_data[cur_data.bed_type == "Real Bed"]
    cur_data = cur_data.drop(columns = ["bed_type"])

    print(len(cur_data))

    cur_data = cur_data.dropna(subset=["zipcode", "beds", "bedrooms", "bathrooms"])

    print(len(cur_data))

    cur_data["price"] = cur_data.price.str.replace(r"[\$\,]", "").astype(float).round().astype(int)

    cur_data = cur_data[cur_data["price"] < 1250]
    cur_data = cur_data[cur_data["price"] > 25]

    print(len(cur_data))

    cur_selector = cur_data.groupby("id")["id"].count()
    cur_selector = cur_selector[ cur_selector > 3 ]

    cur_data = cur_data[cur_data.id.isin(cur_selector.index)]

    print(len(cur_data))

    replaced_columns = [
        'neighbourhood_group_cleansed', 'latitude', 'longitude',
        'accommodates', 'bathrooms', 'bedrooms', 'beds',
        'number_of_reviews', 'review_scores_rating',
        'reviews_per_month', 'is_location_exact', "datetime"
    ]

    firsts_table = cur_data.groupby("id").first()[replaced_columns]

    cur_data = cur_data.drop(columns=replaced_columns).merge(firsts_table, on="id", how="right")

    cur_data = geopandas.GeoDataFrame(
        cur_data,
        geometry=geopandas.points_from_xy(
            cur_data.longitude, cur_data.latitude
        )
    )

    cur_data = cur_data.drop(columns=["longitude", "latitude"])

    cur_data = cur_data.dropna(subset=["review_scores_rating", "reviews_per_month"])

    print(len(cur_data))

    cur_data = cur_data[cur_data.review_scores_rating > 60]
    cur_data = cur_data.drop(columns=["review_scores_rating"])

    print(len(cur_data))

    cur_data = cur_data[cur_data.is_location_exact == "t"]
    cur_data = cur_data.drop(columns=["is_location_exact"])

    print(len(cur_data))

    cur_data = cur_data[cur_data.neighbourhood_group_cleansed.isin(["Manhattan", "Brooklyn"])]

    cur_data["is_brooklyn"] = cur_data.neighbourhood_group_cleansed == "Brooklyn"
    cur_data = cur_data.drop(columns = ["neighbourhood_group_cleansed"])

    print(len(cur_data))

    cur_data = cur_data[cur_data.accommodates < 9]

    print(len(cur_data))

    cur_data = cur_data[cur_data.bathrooms >= 1]

    print(len(cur_data))

    cur_data = cur_data[ cur_data.bedrooms > 0 ]
    cur_data = cur_data[ cur_data.bedrooms < 5 ]

    print(len(cur_data))

    cur_data = cur_data[ cur_data.beds > 0 ]
    cur_data = cur_data[ cur_data.beds < 7 ]

    print(len(cur_data))

    cur_data = cur_data[ cur_data.number_of_reviews > 5 ]
    cur_data = cur_data.drop(columns=["number_of_reviews"])

    print(len(cur_data))

    cur_data = cur_data[ cur_data.reviews_per_month > 1/8 ]
    cur_data = cur_data.drop(columns=["reviews_per_month"])

    print(len(cur_data))

    cur_data = cur_data.drop(columns=["datetime"])

    cur_data = cur_data.reset_index(drop=True)

    cur_data["zipcode"] = cur_data["zipcode"].str.split("-").map(lambda work_list: work_list[0])

    cur_data["zipcode"] = cur_data["zipcode"].astype("int")

    return cur_data
