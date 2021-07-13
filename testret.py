#import urllib.request

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Artemisia Gentileschi")
location = geolocator.geocode("Museo Soumaya")
print(location.latitude, location.longitude)

print(geolocator.reverse(f"{location.latitude}, {location.longitude}"))
print("===")