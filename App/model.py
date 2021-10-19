"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from DISClib.Algorithms.Sorting import mergesort as ms
from time import process_time as ptime 
from datetime import date
from math import pi
import re


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Decorador para medir el tiempo
def timer(func):
    def wraper(*args, **kwargs):
        start = ptime()
        result = func(*args,**kwargs)
        stop = ptime()
        print("\n")
        print(f"La función tardo {(stop-start)*1000} ms")
        return result
    return wraper

# Construccion de modelos
def newCatalog():
    catalog = {"artists": None,
               "artworks": None,
               "medium": None,
               "Nationality": None,
               "ConstID": None}

    catalog['artworks'] = lt.newList('ARRAY_LIST')
    catalog['artists'] = lt.newList('ARRAY_LIST')
    
    """
    Este índice crea un map cuya llave es el medio/técnica de la obra, se asume que cada medio tenga unas 4 obras 
    """
    catalog['medium'] = mp.newMap(138112//16,
                                   maptype='PROBING',
                                   loadfactor=0.8)
    
    """
    Este índice crea un map cuya llave es la nacionalidad de la obra, hay 195 paises en el mundo 
    """
    catalog['Nationality'] = mp.newMap(195//4,
                                   maptype='PROBING',
                                   loadfactor=0.8)
    
    """
    Este índice crea un map cuya llave es id del artista, hay 15220 artistas
    """
    catalog['ConstID'] = mp.newMap(15220//4,
                                   maptype='CHAINING',
                                   loadfactor=4.0)
    catalog["Req4"] = None

    return catalog

# Funciones para agregar informacion al catalogo
def addArtist(catalog, artist):
    filtered = {"ConstituentID":int(artist["ConstituentID"]),
    "Gender":artist["Gender"], 
    "DisplayName":artist["DisplayName"], 
    "Nationality":parseNat(artist["Nationality"]), 
    "BeginDate":int(artist["BeginDate"]),
    "EndDate": int(artist["EndDate"]) }

    lt.addLast(catalog["artists"], filtered)

    if mp.contains(catalog['ConstID'], filtered['ConstituentID']):
        pass
    else:
        mp.put(catalog['ConstID'], filtered['ConstituentID'], filtered)

def addArtwork(catalog, artwork):
    filtered = {"Title":artwork["Title"], 
        "ConstituentID":eval(artwork["ConstituentID"]),
        "Date":dateToInt(artwork["Date"]),
        "Medium":artwork["Medium"],
        "Dimensions":artwork["Dimensions"],
        "CreditLine":artwork["CreditLine"],
        "Department":artwork["Department"],
        "Classification":artwork["Classification"],
        "Weight (kg)":toFloat(artwork["Weight (kg)"]),
        "Width (cm)":toFloat(artwork["Width (cm)"]),
        "Length (cm)":toFloat(artwork["Length (cm)"]),
        "Height (cm)":toFloat(artwork["Height (cm)"]),
        "Depth (cm)":toFloat(artwork["Depth (cm)"]),
        "Circumference (cm)":toFloat(artwork["Circumference (cm)"]),
        "Diameter (cm)":toFloat(artwork["Diameter (cm)"]),
        "DateAcquired":toDate(artwork["DateAcquired"]),
        "Seat Height (cm)":toFloat(artwork["Seat Height (cm)"]) }

    lt.addLast(catalog["artworks"], filtered)
    if mp.contains(catalog['medium'], filtered['Medium']):
        pareja = mp.get(catalog['medium'], filtered['Medium'])
        lt.addLast(me.getValue(pareja), filtered)
    else:
        mp.put(catalog['medium'], filtered['Medium'], lt.newList('ARRAY_LIST'))
        pareja = mp.get(catalog['medium'], filtered['Medium'])
        lt.addLast(me.getValue(pareja), filtered)

    for artistID in filtered["ConstituentID"] :
        pareja = mp.get(catalog['ConstID'], artistID)
        artista = me.getValue(pareja) 
        nacionalidad = artista["Nationality"] 
        
        if mp.contains(catalog['Nationality'], nacionalidad):
            pareja = mp.get(catalog['Nationality'], nacionalidad)
            lt.addLast(me.getValue(pareja), filtered)
        else:
            mp.put(catalog['Nationality'], nacionalidad, lt.newList('ARRAY_LIST'))
            pareja = mp.get(catalog['Nationality'], nacionalidad)
            lt.addLast(me.getValue(pareja), filtered)

def loadAnswers(catalog):
    catalog["Req4"] = classifyByNation(catalog)

def parseNat(nationality):
    if nationality == "" or nationality == "Nationality unknown":
        return ""
    else:
        return nationality

def toFloat(string):
    try:
        return float(string)
    except ValueError:
        return None

def toDate(string):
    try:
        return date.fromisoformat(string)
    except ValueError:
        return date(1,1,1)

def dateToInt(string):
    try:
        return int(re.search("\d{4}",string)[0])
    except TypeError:
        return 0

# Funciones de consulta
def nArtworksOldestByMedium(catalog, n, medium):
    if not mp.contains(catalog['medium'], medium):
        return False
    else:
        pareja = mp.get(catalog["medium"], medium)
        lista = me.getValue(pareja)
        ms.sort(lista, cmpArworksByDate)
        return lista


def numArtworks(catalog, nacionalidad):
    if not mp.contains(catalog['Nationality'], nacionalidad):
        return False
    else:
        pareja = mp.get(catalog["Nationality"], nacionalidad)
        lista = me.getValue(pareja)
        total = lt.size(lista)
        return total

    """las n obras más
antiguas para un medio específico"""

def getArtistsCronOrder(catalog, iyear, fyear):
    datos = {"NumTot":0,
            "Primeros3":lt.newList("ARRAY_LIST"),
            "Ultimos3":None}
    artists = catalog["artists"]
    pos = ceilSearch(iyear, artists, "BeginDate")
    if pos[1]:
        for i in range(pos[0]-1, 1, -1):
            if lt.getElement(artists, i)["BeginDate"] < iyear:
                pos = i + 1 
                break
    else:
        pos = pos[0]
    maxi = 0
    for i in range(pos, lt.size(artists)+1):
        elem = lt.getElement(artists,i)
        if iyear <= elem["BeginDate"] <= fyear:
            datos["NumTot"] += 1
            if datos["NumTot"] <= 3:
                lt.addLast(datos["Primeros3"], elem)
            if i > maxi:
                maxi = i
        if elem["BeginDate"] > fyear:
            break
    datos["Ultimos3"] = lt.subList(artists,maxi-2, 3)
    return datos

#Obtenido de https://www.techiedelight.com/find-floor-ceil-number-sorted-array/
def ceilSearch(value, list, key):
    upper = lt.size(list)
    lower = 1
    ceil = -1
    while lower <= upper:
        mid = (upper-lower) // 2 + lower
        elem = lt.getElement(list, mid)[key]

        if elem == value:
            return mid,True
    
        elif value > elem:
            lower = mid + 1
        
        else:
            ceil = mid
            upper = mid - 1 
    return ceil, False


def getArtworksCronOrder(catalog, idate, fdate):
    idate = toDate(idate)
    fdate = toDate(fdate)
    res = {"NumTot":0,
            "Purchase":0,
            "NumArtistas": 0,
            "Primeros3":lt.newList("ARRAY_LIST"),
            "Ultimos3":lt.newList("ARRAY_LIST")}

    pos = ceilSearch(idate, catalog["artworks"], "DateAcquired")
    if pos[1]:
        for i in range(pos[0]-1, 1, -1):
            elem = lt.getElement(catalog["artworks"],i)
            if elem < idate:
                pos = i + 1
                break
    else:
        pos = pos[0]
    maxi = pos
    datos = catalog["artworks"]
    for i in range(pos, lt.size(datos)+1):
        elem = lt.getElement(datos, i)
        if idate <= elem["DateAcquired"] <= fdate:
            res["NumTot"] += 1
            if "purchase" in elem["CreditLine"].lower():
                res["Purchase"] += 1
            for id in elem["ConstituentID"]:
                res["NumArtistas"] += 1
            if res["NumTot"] <= 3:
                filtrado = {"Title": elem["Title"], "ArtistsNames":lt.newList("ARRAY_LIST"), "Medium":elem["Medium"], "Date":elem["Date"], "DateAcquired":elem["DateAcquired"], "Dimensions":elem["Dimensions"]}
                for id in elem["ConstituentID"]:
                    name = mp.get(catalog["ConstID"], id)["value"]["DisplayName"]
                    lt.addLast(filtrado["ArtistsNames"], name)
                lt.addLast(res["Primeros3"], filtrado)
            if i > maxi:
                maxi = i
        if elem["DateAcquired"] > fdate:
            break
    for i in range(maxi-2, maxi+1):
        elem = lt.getElement(datos, i)
        filtrado = {"Title": elem["Title"], "ArtistsNames":lt.newList("ARRAY_LIST"), "Medium":elem["Medium"], "Date":elem["Date"], "DateAcquired":elem["DateAcquired"], "Dimensions":elem["Dimensions"]}
        for id in elem["ConstituentID"]:
            name = mp.get(catalog["ConstID"], id)["value"]["DisplayName"]
            lt.addLast(filtrado["ArtistsNames"], name)
        lt.addLast(res["Ultimos3"], filtrado)


def classifyByNation(catalog):
    UniqueNats = mp.newMap(195, maptype='PROBING',loadfactor=0.5)
    NumANats = mp.newMap(195, maptype='PROBING',loadfactor=0.5)

    for obra in lt.iterator(catalog["artworks"]):
        adjust = {"Title": obra["Title"], "Date": obra["Date"], "Medium": obra["Medium"], "Dimensions" :obra["Dimensions"], "ArtistsNames":lt.newList("ARRAY_LIST")}
        nations = mp.newMap(195,maptype='PROBING',loadfactor=0.5)
        for id in obra["ConstituentID"]:
            try:
                artist = mp.get(catalog["ConstID"], id)["value"]
                name,nationality = artist["DisplayName"], artist["Nationality"]
            except:
                name = nationality = "Unknown"
            
            if nationality == "":
                nationality = "Unknown"
            
            if mp.contains(nations, nationality):
                mp.get(nations, nationality)["value"] += 1
            else:
                mp.put(nations, nationality, 1)
            
            lt.addLast(adjust["ArtistsNames"], name)

        for national in lt.iterator(mp.keySet(nations)):
            if mp.contains(UniqueNats, national):
                lt.addLast(mp.get(UniqueNats, national)["value"], adjust)
            else:
                mp.put(UniqueNats, national, lt.newList("ARRAY_LIST"))
                lt.addLast(mp.get(UniqueNats, national)["value"], adjust)

            if mp.contains(NumANats, national):
                mp.get(NumANats, national)["value"] += mp.get(nations, national)["value"]
            else:
                mp.put(NumANats, national, mp.get(nations, national)["value"])

    size = lt.newList("ARRAY_LIST")
    for key in lt.iterator(mp.keySet(NumANats)):
        val = mp.get(NumANats, key)["value"]
        lt.addLast(size, (key,val))

    ms.sort(size, lambda elem1, elem2 : elem1[1] > elem2[1])

    top10 = lt.subList(size,1,10)

    countryMost = lt.getElement(size, 1)[0]
    country = mp.get(UniqueNats, countryMost)
    res = (top10, country)
    return res




# Funciones utilizadas para comparar elementos dentro de una lista
def cmpArworksByDate(medium1, medium2):
    return medium1["Date"] < medium2["Date"]   

def cmpArtistsbyDate(artist1, artist2):
    return artist1["BeginDate"] < artist2["BeginDate"]

# Funciones de ordenamiento
def sortArtists(catalog):
    ms.sort(catalog["artists"],cmpArtistsbyDate)

def sortArtworks(catalog):
    ms.sort(catalog["artworks"], lambda artwork1, artwork2: artwork1["DateAcquired"] < artwork2["DateAcquired"])

