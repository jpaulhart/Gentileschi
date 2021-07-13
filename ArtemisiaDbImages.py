import os.path
from os import path
import urllib.request
import time

#--------------------------------------------------------------------
# Download a painting from Wikipedia
#--------------------------------------------------------------------
def downloadPainting(painting, imageDir):

    urlLarge = f"https:{painting.imageLarge}"
    diskImageLarge = f"{imageDir}/{painting.imageFileName}"
    paintingExists = path.exists(diskImageLarge)
    #print(f"{paintingExists} {diskImageLarge}")
    if path.exists(diskImageLarge) == False:
        print(f"Downloading {painting.imageFileName}")

        urlMedium = f"https:{painting.imageMedium}"
        diskImageMedium = f"{imageDir}/{painting.imageFileName}-medium"

        urlSmall = f"https:{painting.imageSmall}"
        diskImageSmall = f"{imageDir}/{painting.imageFileName}-small"

        urllib.request.urlretrieve(urlLarge, diskImageLarge)
        urllib.request.urlretrieve(urlMedium, diskImageMedium)
        urllib.request.urlretrieve(urlSmall, diskImageSmall)

#--------------------------------------------------------------------
# Process each painting
#--------------------------------------------------------------------
def downloadImages(paintings, imageDir):
    print("Start of image download")

    for painting in paintings:

        #print(f"Downloading {painting.imageFileName}")
        downloadPainting(painting, imageDir)
        #print("Sleeping because Wikipedia has a limit of downloads")
        time.sleep(1)

    print("End of image download")
    