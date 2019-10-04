import pandas as pd

def clean_airbnb_data(work_data):
    drop_columns = [
        "access", "amenities", "availability_30", "availability_365",
        "availability_60", "availability_90", "bed_type",
        "calculated_host_listings_count",
        "calculated_host_listings_count_entire_homes",
        "calculated_host_listings_count_private_rooms",
        "calculated_host_listings_count_shared_rooms",
        "calendar_last_scraped", "calendar_updated",
        "cancellation_policy", "city", "cleaning_fee", "country",
        "country_code", "description", "experiences_offered",
        "extra_people", "first_review", "guests_included",
        "has_availability", "host_about", "host_acceptance_rate",
        "host_has_profile_pic", "host_id", "host_identity_verified",
        "host_is_superhost", "host_listings_count", "host_location",
        "host_name", "host_neighbourhood", "host_picture_url",
        "host_response_rate", "host_response_time", "host_since",
        "host_thumbnail_url", "host_total_listings_count", "host_url",
        "host_verifications", "house_rules", "instant_bookable",
        "interaction", "is_business_travel_ready",
        "is_location_exact", "jurisdiction_names", "last_review",
        "last_scraped", "license", "listing_url", "market",
        "maximum_maximum_nights", "maximum_minimum_nights",
        "maximum_nights", "maximum_nights_avg_ntm", "medium_url",
        "minimum_maximum_nights", "minimum_minimum_nights",
        "minimum_nights", "minimum_nights_avg_ntm", "monthly_price",
        "name", "neighborhood_overview", "neighbourhood", "notes",
        "number_of_reviews_ltm", "picture_url",
        "require_guest_phone_verification",
        "require_guest_profile_picture", "requires_license",
        "review_scores_accuracy", "review_scores_checkin",
        "review_scores_cleanliness", "review_scores_communication",
        "review_scores_location", "review_scores_value",
        "reviews_per_month", "room_type", "scrape_id",
        "security_deposit", "smart_location", "space", "square_feet",
        "state", "street", "summary", "thumbnail_url", "transit",
        "weekly_price", "xl_picture_url", "zipcode"
    ]

    drop_columns = [
        drop_column for drop_column in drop_columns if drop_column in work_data.columns
    ]

    work_data.dropna(
        subset=["bathrooms", "bedrooms", "beds"], inplace=True
    )

    property_types = [ "Apartment", "House", "Loft", "Townhouse", "Condominium" ]

    work_data = work_data[
        work_data.property_type.isin(property_types) &
        (work_data.is_location_exact == "t") &
        (work_data.room_type == "Entire home/apt") &
        (work_data.availability_365 > 50) &
        (work_data.minimum_nights < 5) &
        (work_data.accommodates < 10) &
        (work_data.bathrooms >= 1) &
        (work_data.bathrooms < 5) &
        (work_data.bedrooms >= 1) &
        (work_data.bedrooms < 6) &
        (work_data.beds >= 1) &
        (work_data.beds < 9) &
        (
            ( work_data.neighbourhood_group_cleansed == "Brooklyn" ) |
            ( work_data.neighbourhood_group_cleansed == "Manhattan" )
        )
    ].drop(
        columns = drop_columns
    )

    work_data.price = work_data.price.replace('[\$,]', '', regex=True).astype(float)

    work_data.rename(columns={
        "neighbourhood_cleansed": "neighbourhood",
        "neighbourhood_group_cleansed": "neighbourhood_group"
    }, inplace=True)

    work_data = work_data[(work_data.price >= 30) & (work_data.price <= 600)]

    return work_data
