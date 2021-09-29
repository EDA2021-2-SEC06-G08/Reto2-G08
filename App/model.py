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

# Construccion de modelos
def newCatalog():
    catalog = {"artists": None,
               "artworks": None,
               "medium": None}

    catalog['artworks'] = lt.newList('ARRAY_LIST')
    
    """
    Este índice crea un map cuya llave es el medio/técnica de la obra, se asume que cada medio tenga unas 4 obras 
    """
    catalog['medium'] = mp.newMap(138112//16,
                                   maptype='CHAINING',
                                   loadfactor=4.0)
    return catalog

# Funciones para agregar informacion al catalogo
""" se comenta porque solo es necesario cargar las obras por el momento y aún no está definido
    como se van a añadir exactemente los artistas

def addArtist(catalog, artist):
    filtered = {"ConstituentID":int(artist["ConstituentID"]),
    "Gender":artist["Gender"], 
    "DisplayName":artist["DisplayName"], 
    "Nationality":parseNat(artist["Nationality"]), 
    "BeginDate":int(artist["BeginDate"]),
    "EndDate": int(artist["EndDate"]) }

    lt.addLast(catalog["artists"], filtered)
"""

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
        if lt.size(lista) >= n:
            oldestArtworks = lt.subList(lista, 1, n) 
            return oldestArtworks
        else: 
            return lista


    """las n obras más
antiguas para un medio específico"""

# Funciones utilizadas para comparar elementos dentro de una lista
def cmpArworksByDate(medium1, medium2):
    return medium1["Date"] < medium2["Date"]   


# Funciones de ordenamiento


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
