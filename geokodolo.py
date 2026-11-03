import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import geopandas as gpd
import time
from shapely import geometry

geocoder = Nominatim(user_agent="virsli")
print(geocoder.geocode('Pázmány Péter sétány 1/a, Budapest'))

df = pd.read_excel('kir_mukodo_intezmenyek_2022_05_30.xlsx')

def geocode(address, attempt=1, max_attempts=5):
    try:
        return geocoder.geocode(address)
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            return geocode(address, attempt=attempt + 1)
        raise

points = []
addresses = []

for i in range(len(df)):
    time.sleep(1.1)
    addr = 'Magyarország, ' + str(df.iloc[i]['Intézmény székhelyének megyéje']) + ' megye, ' + str(df.iloc[i]['Intézmény székhelyének települése']) + ', ' + str(df.iloc[i]['Intézmény székhelyének irányítószáma']) + ', ' + str(df.iloc[i]['Intézmény székhelyének pontos címe'])
    print(addr)
    location = geocode(addr)
    if location != None:
        print(location.latitude, location.longitude)
        point = geometry.Point(location.latitude, location.longitude)
        points.append(point)
        addresses.append(addr)

gdf = gpd.GeoDataFrame({'cim': addresses, 'geometry': points}, crs='EPSG:4326')
print(gdf)
gdf.to_file('eredmenyek.geojson', driver="GeoJSON")