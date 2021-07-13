
import re
import wikipedia

from dataclasses import dataclass

fileName = "/Users/paulhart/Documents/Artists/Gentileschi/GentelesciTable.txt"
outFileName = "/Users/paulhart/Documents/Artists/Gentileschi/GentelesciTable.csv"
outFolder = "/Users/paulhart/Documents/Artists/Gentileschi"

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


#print("----------------------------------------------------------")

file1 = open(fileName, 'r')
table = file1.read()
table = table.replace("\n", " ")

# --------------------------------------------------------------------
# Column Parsers
# --------------------------------------------------------------------

# --------------------------------------------------------------------
# Column 0 - Image
# --------------------------------------------------------------------
def parseCol0(col): # image
    imagePattern = '.*?<a href="(.*?)".*?<img .*?src="(.*?)".*?srcset="(.*?)".*?</a>.*?'
    imageMatch = re.match(imagePattern, col)
    imageLink = ""
    imageSrc = ""
    imageSrcSet = ""
    imageLarge = ""
    imageMedium = ""
    imageSmall = ""
    imageFileName = ""

    if imageMatch != None:
        imageLink = imageMatch.groups(1)
        imageLink = imageLink[1].strip()
        imageSrc = imageMatch.groups(2)
        imageSrc = imageSrc[1].strip()
        imageSrcSet = imageMatch.groups(3)
        imageSrcSet = imageSrcSet[1].strip()
        names = imageSrcSet.split("jpg/")
        names[0] += "jpg"
        imageLarge = names[0].replace("thumb/", "")
        imageSmall = imageSrcSet
        imageMedium = imageSmall.replace("128", "256")
        imageFileName = ""
        index = imageLarge.rfind("/")
        imageFileName = imageLarge[index + 1:]

        #print(names)
    else:
        print("Error with image column")
        raise
    return imageLarge, imageMedium, imageSmall, imageFileName

# --------------------------------------------------------------------
# Column 1 - Name
# --------------------------------------------------------------------
def parseCol1(col): # name
    namePattern1 = ".*?<i>(.*?)</i>.*?"
    namePattern2 = '.*?<a href="(.*?)".*?title=".*?">(.*?)</a>.*?'
    name1Match = re.match(namePattern1, col)
    nameText = name1Match.groups(1)
    nameText = nameText[0].strip()
    nameLink = ""
    if nameText.startswith("<a"):
        name2Match = re.match(namePattern2, nameText)
        nameLink = name2Match.groups(1)
        nameLink = nameLink[0]
        nameText = name2Match.groups(2)
        nameText = nameText[1]
    #print(nameText, nameLink)
    return nameText, nameLink

# --------------------------------------------------------------------
# Column 2 - Year
# --------------------------------------------------------------------
def parseCol2(col): # year
    year = col.replace("<td>", "").replace("</td>", "").strip()
    return year

# --------------------------------------------------------------------
# Column 3 - collection
# --------------------------------------------------------------------
def parseCol3(col): # collection
    collectionPattern1 = ".*?<td>(.*?)</td>.*?" 
    collectionPattern2 = '.*?<a href="(.*?)".*?title=".*?">(.*?)</a>.*?'
    collection1Match = re.match(collectionPattern1, col)
    collectionText = collection1Match.groups(1)
    collectionText = collectionText[0].strip()
    collectionLink = ""
    if collectionText.startswith("<a"):
        collection2Match = re.match(collectionPattern2, collectionText)
        collectionLink = collection2Match.groups(1)
        collectionLink = "//www.wikipedia.org" + collectionLink[0]
        collectionText = collection2Match.groups(2)
        collectionText = collectionText[1]
    #print(collectionText, collectionLink)
    return collectionText, collectionLink

# --------------------------------------------------------------------
# Column 4 - Dimensions
# --------------------------------------------------------------------
def parseCol4(col): # dimensions
    dim = col.replace("<td>", "").replace("</td>", "").strip()
    return dim

# --------------------------------------------------------------------
# Column 5 - Inventory number
# --------------------------------------------------------------------
def parseCol5(col): # inventory nr.
    invNo = col.replace("<td>", "").replace("</td>", "").strip()
    return invNo

# --------------------------------------------------------------------
# Column 6 - Catalog code
# --------------------------------------------------------------------
def parseCol6(col): # catalog code
    catCode = col.replace("<td>", "").replace("</td>", "").strip()
    return catCode


# --------------------------------------------------------------------
# Parse Table
# --------------------------------------------------------------------
def parseTable():

    print("Start of table parse")

    rowPattern = "<tr>.*?</tr>"
    colPattern = "<td>.*?</td>"
    rows = re.findall(rowPattern, table)

    imageLarge = ""
    imageMedium = ""
    imageSmall = ""
    imageFileName = ""
    nameText = ""
    nameLink = ""
    year = ""
    collectionText = ""
    collectionLink = ""
    invNo = ""
    dim = ""
    catCode = ""

    rowNo = 0
    recs = []
    paintings = []
    rec = f'imageLarge,imageMedium,imageSmall,imageFileName,nameText,nameLink,year,collectionText,collectionLink,invNo,dim,catCode'
    recs.append(rec)

    for row in rows:
        if rowNo > 0:
            imageLink = ""
            imageSrc = ""
            imageSrcSet = ""
            imageLarge = ""
            imageMedium = ""
            imageSmall = ""
            imageFileName = ""
            nameText = ""
            nameLink = ""
            year = ""
            collectionText = ""
            collectionLink = ""
            invNo = ""
            dim = ""
            catCode = ""
            cols = re.findall(colPattern, row)
            colNo = 0
            #0 - image, 1 - name, 2 - year, 3 - collection, 4 - dimensions, 5 - inventory nr., 6 - catalogue code
            for col in cols:
                if colNo == 0:   # image
                    imageLarge, imageMedium, imageSmall, imageFileName = parseCol0(col)
                elif colNo == 1: # name
                    nameText, nameLink = parseCol1(col)
                elif colNo == 2: # year
                    year = parseCol2(col)
                elif colNo == 3: # collection
                    collectionText, collectionLink = parseCol3(col)
                elif colNo == 4: # dimensions
                    dim = parseCol4(col)
                elif colNo == 5: # inventory nr.
                    invNo = parseCol5(col)
                elif colNo == 6: # catalog code
                    catCode = parseCol6(col)
                #print(f"colNo: {colNo}, col: {col}")
                colNo += 1
        if rowNo > 0:
            rec = f'"{imageLarge}","{imageMedium}","{imageSmall}","{imageFileName}","{nameText}","{nameLink}","{year}","{collectionText}","{collectionLink}","{invNo}","{dim}","{catCode}"'
            recs.append(rec)
            painting = Painting(imageLarge,imageMedium,imageSmall, imageFileName,
                                nameText,nameLink,
                                year,
                                collectionText,
                                collectionLink,invNo,
                                dim,
                                catCode)
            paintings.append(painting)
        rowNo += 1
    #groups = rows.groups
    with open(outFileName, "w") as outfile:
        outfile.write("\n".join(recs))
    outfile.close()
    print(f"End of table parse.")
    return paintings

if __name__ == "__main__":
    paintings = parseTable()
    print("Done")