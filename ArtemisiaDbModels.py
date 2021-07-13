from dataclasses import dataclass

# --------------------------------------------------------------------
# Painting Dataclass
# --------------------------------------------------------------------
@dataclass
class Painting:
    imageLarge: str
    imageMedium: str
    imageSmall: str
    imageFileName: str
    nameText: str
    nameLink: str
    year: str
    collectionText: str
    collectionLink: str
    invNo: str
    dim: str
    catCode: str

# --------------------------------------------------------------------
# Painting Dataclass
# --------------------------------------------------------------------
@dataclass
class Collection:
    name: str
    address: str
    lat: str
    long: str
    url: str
    summary: str
