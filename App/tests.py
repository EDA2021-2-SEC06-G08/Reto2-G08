import controller as ctl
import model
import csv
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
from time import process_time as ptime
import pickle
assert cf

def loadData(catalog):

    filename = r"C:\Users\camil\OneDrive\Desktop\Los Andes\5to Semestre\EDA\Retos\Reto2-G08\Data/MoMa/Artists-utf8-small.csv"
    input_file = csv.DictReader(open(filename, encoding="utf-8"))
    for artist in input_file:
        model.addArtist(catalog, artist)


    filename= r"C:\Users\camil\OneDrive\Desktop\Los Andes\5to Semestre\EDA\Retos\Reto2-G08\Data/MoMA/Artworks-utf8-small.csv"
    input_file = csv.DictReader(open(filename, encoding="utf-8"))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)

def loadReq(catalog):
    catalog["Req4"] = model.classifyByNation(catalog)
    

calcCost = model.calculateCost

# with open(r"C:\Users\camil\OneDrive\Desktop\Los Andes\5to Semestre\EDA\Retos\Reto2-G08\Data\catalogLarge", "rb") as file:
#     catalog = pickle.load(file)
catalog = ctl.initCatalog()
loadData(catalog)
ctl.sortArtists(catalog)
ctl.sortArtworks(catalog)
loadReq(catalog)





