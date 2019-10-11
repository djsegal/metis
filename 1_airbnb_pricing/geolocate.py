import random
from geopy.geocoders import ArcGIS, Bing, Nominatim, OpenCage, GoogleV3, OpenMapQuest
import csv, sys
import time

n_user = 'dansegal2@gmail.com'
bing_api = ''
oc_api = ''
g3_api = ''
omq_api =''

timeout = 10

arcgis = ArcGIS(timeout=timeout)
bing = Bing(api_key=bing_api,timeout=timeout)
nominatim = Nominatim(user_agent=n_user, timeout=timeout)
opencage = OpenCage(api_key=oc_api,timeout=timeout)
googlev3 = GoogleV3(api_key=g3_api, domain='maps.googleapis.com', timeout=timeout)
openmapquest = OpenMapQuest(api_key=omq_api, timeout=timeout)

# choose and order your preference for geocoders here
geocoders = {
    "openmapquest": openmapquest,
    "nominatim": nominatim,
    "bing": bing,
    "arcgis": arcgis,
#     "googlev3": googlev3,
#     "opencage": opencage,
}

geocoder_keys = list(geocoders.keys())
skip_keys = []

def gc(address):
    random.shuffle(geocoder_keys)

    for gcoder_key in geocoder_keys:
        if gcoder_key in skip_keys:
            skip_keys.remove(gcoder_key)
            continue

        gcoder = geocoders[gcoder_key]

        time1 = time.time()
        location = gcoder.geocode(address)
        time2 = time.time()

        if location == None:
            skip_keys.append(gcoder_key)
            continue

        print(f'geocoded: {address} ({gcoder_key} - {round(time2-time1,1)}s)')
        return (location.latitude, location.longitude)

    print(f'failed to geolocate record {address}')
    return
