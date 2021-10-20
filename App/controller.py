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
 """

import config as cf
import model
import csv
from time import process_time as ptime 

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

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo
def initCatalog():
    return model.newCatalog()

# Funciones para la carga de datos

def loadData(catalog):
    loadArtists(catalog)
    loadArtworks(catalog)
    sortArtists(catalog)
    sortArtworks(catalog)
    model.loadAnswers(catalog)

""" Se suman los dos tiempo del decorador"""

def loadArtists(catalog):
    filename = cf.data_dir + "MoMa/Artists-utf8-small.csv"
    input_file = csv.DictReader(open(filename, encoding="utf-8"))
    for artist in input_file:
        model.addArtist(catalog, artist)


def loadArtworks(catalog):
    filename= cf.data_dir + "MoMA/Artworks-utf8-small.csv"
    input_file = csv.DictReader(open(filename, encoding="utf-8"))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)

# Funciones de ordenamiento
def sortArtworks(catalog):
    model.sortArtworks(catalog)

def sortArtists(catalog):
    model.sortArtists(catalog)

# Funciones de consulta sobre el catálogo
# def  nArtworksOldestByMedium(catalog, n, medium):
#     return model.nArtworksOldestByMedium(catalog, n, medium)

# def numArtworks(catalog, nacionalidad):
#     return model.numArtworks(catalog, nacionalidad)

def getArtistsCronOrder(catalog, iyear, fyear):
    """
    Retorna los datos de los artistas que estan en el rango de años pasados por parametro
    """
    return model.getArtistsCronOrder(catalog, iyear, fyear)

def getArtworksCronOrder(catalog, idate, fdate):

    return model.getArtworksCronOrder(catalog, idate, fdate)

def getArtworksByMedium(catalog, name):
    return model.getArtworksByMedium(catalog, name)

def transportArtwDepartment(catalog, department):
    return model.transportArtwDepartment(catalog, department)

def artistasProlificos(numArtist, iyear, fyear):
    return model.artistasProlificos(numArtist, iyear, fyear)

