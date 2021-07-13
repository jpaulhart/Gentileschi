import ArtemisiaDbModels as am
import ArtemisiaDbParser as ap
import ArtemisiaDbImages as ai
import ArtemisiaDbCollections as ac

fileName = "/Users/paulhart/Documents/Artists/Gentileschi/GentelesciTable.txt"
outFileName = "/Users/paulhart/Documents/Artists/Gentileschi/GentelesciTable.csv"
outFolder = "/Users/paulhart/Documents/Artists/Gentileschi/Images"

#--------------------------------------------------------------------
# Main entry point
#--------------------------------------------------------------------
if __name__ == "__main__":
    print("Build Artemisia Gentelesci paintings started")
    paintings = ap.parseTable()
    collections = ac.downloadCollections(paintings)
    ai.downloadImages(paintings, outFolder)
    print("Build Artemisia Gentelesci paintings complete")
