import controller as ctl
import model
import csv
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.Algorithms.Sorting import mergesort as ms
assert cf

def loadData(catalog):

    filename = "../Data/MoMa/Artists-utf8-large.csv"
    input_file = csv.DictReader(open(filename, encoding="utf-8"))
    for artist in input_file:
        model.addArtist(catalog, artist)


    filename= "../Data/MoMA/Artworks-utf8-large.csv"
    input_file = csv.DictReader(open(filename, encoding="utf-8"))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)



catalog = ctl.initCatalog()
loadData(catalog)
ctl.sortArtists(catalog)
ctl.sortArtworks(catalog)

con = set()


for i in lt.iterator(catalog["artworks"]):
    con.add(i["Department"])



