"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Las n obras más antiguas para un medio específico")
    print("0- Salir")

def initCatalog():
    """
    Incializa el catalogo del museo
    """
    return controller.initCatalog()

def loadData(catalog):
    controller.loadData(catalog)

# Funciones de impresión
def printnArtworksOldestByMedium(oldestArtworks, n, medium):
    print('')
    print(f"{41*'='} Req. Lab No.5 Answer {41*'='}")
    num = 1
    if lt.size(oldestArtworks) >= n:
        print(f"Las {n} obras más antiguas con la técnica {medium} son: ")
        for i in lt.iterator(oldestArtworks):
            print('')
            print(f"{num}. {i}")
            num += 1
        print('')
    else:
        print(f"Solo se encontraron {lt.size(oldestArtworks)} obras con la técnica {medium}, estas son: ")
        for i in lt.iterator(oldestArtworks):
            print('')
            print(f"{num}. {i}")
            num += 1
        print('')


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print('')
        print("Cargando información de los archivos ....")
        print('')
        catalog = initCatalog()
        loadData(catalog)
        
    elif int(inputs[0]) == 2:
        print('')
        try:
            n = int(input("Ingrese el número de obras: "))
        except:
            print("Pruebe con un número entero positivo")
            print('')
            continue
        medium = input("Ingrese el medio: ")
        artworks = controller.nArtworksOldestByMedium(catalog, n, medium)
        if artworks:
            printnArtworksOldestByMedium (artworks, n, medium)
        else:
            print("Pruebe con un número entero positivo y con un medio disponible en el MoMA")
            print('')

    else:
        sys.exit(0)
sys.exit(0)
