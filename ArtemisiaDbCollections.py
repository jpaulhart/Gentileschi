import wikipedia
import html
from geopy.geocoders import Nominatim

import ArtemisiaDbModels as am


# --------------------------------------------------------------------
# Check for an existing collection
# --------------------------------------------------------------------
def findCollection(collections, painting):
    rc = False

    for collection in collections:
        if collection.name == painting.collectionText:
            rc = True
            break
    return rc

# --------------------------------------------------------------------
# Load table from Wikipedia
# --------------------------------------------------------------------
def downloadCollections(paintings):
    print("Start of collection download")

    name = ""
    address = ""
    lat = ""
    long = ""
    url = ""
    summary = ""
    collections = []

    for painting in paintings:
        if painting.collectionLink != "":
            index = painting.collectionLink.rfind("/") + 1
            pageTitle = painting.collectionLink[index:].replace("_", " ")
            if pageTitle.find("%C3%9F") >= 0:
                pageTitle = html.unescape(pageTitle).replace("%C3%9F", "ß")
            if pageTitle.find("%27") >= 0:
                pageTitle = html.unescape(pageTitle).replace("%27", "'")
            wikipage = wikipedia.WikipediaPage(pageTitle)

            name = wikipage.title

            if findCollection(collections, painting) == False:
                # print(f"Painting: {painting.nameText}")
                geolocator = Nominatim(user_agent="Artemisia Gentileschi")
                try:
                    lat, long = wikipage.coordinates
                except:
                    location = geolocator.geocode(name)
                    if location is not None:
                        lat = location.latitude
                        long = location.longitude

                if lat != "":
                    address = geolocator.reverse(f"{lat}, {long}")
                    address = address.address
                url = painting.collectionLink
                summary = wikipage.summary

                collection = am.Collection(
                    name,
                    address,
                    lat,
                    long,
                    url,
                    summary)
                collections.append(collection)

    print("End of collection download")
    return collections