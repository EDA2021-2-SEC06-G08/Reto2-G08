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
from DISClib.DataStructures import mapentry as me
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
    print("2- REQ. 1: Listar cronológicamente los artistas ")
    print("3- REQ. 2: Listar cronológicamente las adquisiciones")
    print("4. REQ. 3: Clasificar las obras de un artista por técnica")
    print("5. REQ. 4: Clasificar las obras por la nacionalidad de sus creadores")
    print("6. REQ. 5: Transportar obras de un departamento")  
    print("7. REQ. 6 (BONO): Encontrar los artistas más prolíficos del museo")  
    print("0- Salir")

def initCatalog():
    """
    Incializa el catalogo del museo
    """
    return controller.initCatalog()

def loadData(catalog):
    controller.loadData(catalog)

def sortArtists(catalog):
    controller.sortArtists(catalog)

# Funciones de impresión
def printArtistsCronOrder(data, iyear, fyear):
    print(f"Artistas en orden cronologico desde {iyear} hasta {fyear}")
    print(f"Numero total de artistas en el rango de años: {data['NumTot']}")
    print("\n")
    print("Primeros 3 artistas rango:")
    print("\n")
    for artista in lt.iterator(data["Primeros3"]):
        print(f"- {artista['DisplayName']} is a {artista['Gender']} {artista['Nationality']} artist borned in the year {artista['BeginDate']}", end=" ")
        print(f"and died in {artista['EndDate']}" if artista["EndDate"] != 0 else "and hasn't died.")
    print("-"*100)
    print("Ultimos 3 artistas del rango:")
    print("\n")
    for artista in lt.iterator(data["Ultimos3"]):
        print(f"- {artista['DisplayName']} is a {artista['Gender']} {artista['Nationality']} artist borned in the year {artista['BeginDate']}", end=" ")
        print(f"and died in {artista['EndDate']}" if artista["EndDate"] != 0 else "and hasn't died.")
    print("\n")

def printArtworksCronOrder(data, idate, fdate):
    print(f"Obras adquiridas en orden cronologico desde la fecha {idate} hasta {fdate}")
    print(f"Numero total de obras en el rango de fechas: {data['NumTot']} por {data['NumArtistas']} artistas diferentes")
    print(f"De las cuales se adquirieron {data['Purchase']} por modo de compra (Purchase)")
    print("-"*100)
    print("Primeras 3 obras del rango:")
    print("")
    for obra in lt.iterator(data["Primeros3"]):
        nombres = ", ".join(name for name in lt.iterator(obra['ArtistsNames']))
        print(f"{obra['Title']} por {nombres}, fecha: {obra['Date']}, Medio: {obra['Medium']}, Dimensiones: {obra['Dimensions']}")
        print("")
    print("-"*100)
    print("Ultimas 3 obras del rango")
    print("")
    for obra in lt.iterator(data["Ultimos3"]):
        nombres = ", ".join(name for name in lt.iterator(obra['ArtistsNames']))
        print(f"{obra['Title']} por {nombres}, fecha: {obra['Date']}, Medio: {obra['Medium']}, Dimensiones: {obra['Dimensions']}")
        print("")

def printArtworksByMedium(data, name):
    print(f"{41*'='} Req. No.3 Inputs {41*'='}")
    print(f"Examine the work of the artist named: {name}")
    print(f"{41*'='} Req. No.3 Answer {41*'='}")
    print(f"{name} with MoMA ID {data['constID']} has {data['TotObras']} pieces in his/her name at the museum.")
    print(f"There are {data['TotMedios']} different mediums/techniques in his/her work.\n")
    print(f"His/her most used Medium/Technique is {data['MedMasUsado']} with {lt.size(data['ObrasMedMasUsado'])} pieces.")
    if lt.size(data["ObrasMedMasUsado"]) <3:
        print(f"These pieces are:")
        print(100*"=")
        for artwork in lt.iterator(data["ObrasMedMasUsado"]): 
            print(artwork) 
        print(100*"=")
        print("\n")
    else:
        print(f"The first 3 pieces are:")
        print(100*"=")
        for artwork in lt.iterator(data["3primeras"]): 
            print(artwork) 
        print(100*"=")
        print("\n")
        print(f"The last 3 pieces are:")
        print(100*"=")
        for artwork in lt.iterator(data["3ultimas"]): 
            print(artwork) 
        print(100*"=")
        print("\n")

def printClasificationByNation(data):
    print(f"{'='*16} Req No. 4 Inputs {'='*16}")
    print(f"Ranking countries by their number of artworks in the MoMa. . .")
    print("\n")
    print(f"{'='*16} Req No. 4 Answer {'='*16}")
    print("The TOP 10 Countries in the MoMA are:")
    print("\n")
    print("-"*24)
    print(f" Nationality | Artworks ")
    for i, vals in enumerate(lt.iterator(data[0])):
        if i > 9:
            break
        print("-"*24)
        print(f"{(vals[0].strip() if vals[0] != '' else 'Unknown').center(13,' ')}|{str(vals[1]).center(10, ' ')}")
    print("-"*24)
    print("\n")
    print(f"The TOP nacionality in the museum is: {data[1]['key']} with {lt.size(me.getValue(data[1]))} unique pieces.")
    print("-"*100)
    print("the first and last 3 objects in the american list are:")
    for j in range(1,4):
        i = lt.getElement(me.getValue(data[1]),j)
        print(f" Title: {i['Title']}, Artists: {', '.join(lt.iterator(i['ArtistsNames']))}, Date: {i['Date'] if i['Date'] != 0 else 'Unknown'}, Dimensions: {i['Dimensions'] if i['Dimensions'] != None and i['Dimensions'] != '' else 'Unknown' } ")
    for j in range(lt.size(me.getValue(data[1]))-2, lt.size(me.getValue(data[1]))+1):
        i = lt.getElement(me.getValue(data[1]), j)
        print(f" Title: {i['Title']}, Artists: {', '.join(lt.iterator(i['ArtistsNames']))}, Date: {i['Date'] if i['Date'] != 0 else 'Unknown'}, Dimensions: {i['Dimensions'] if i['Dimensions'] != None and i['Dimensions'] != '' else 'Unknown' } ")
    print("")

def printTransportArtwDepartment(data, department):
    print(f"The MoMA is going to transport {data['Tot']} from {department}")
    print(f"Estimated cargo weight (kg): {data['Weight']}")
    print(f"Estimated cargo cost (USD): {data['Cost']}")
    print("")
    print("The TOP 5 most expensive items to transport are:")
    print("")
    for i in lt.iterator(data["5priciest"]):
        print(f'Title: {i["Title"]}, Artists: {", ".join(i["Artists"])}, Classification: {i["Classification"]}, Date: {i["Date"]}, Medium: {i["Medium"]}, Dimensions: {i["Dimensions"]}, Cost: {i["Cost"]}')
        print("")
    print("The TOP 5 oldests items to transport are:")
    for i in lt.iterator(data["5oldest"]):
        print(f'Title: {i["Title"]}, Artists: {", ".join(i["Artists"])}, Classification: {i["Classification"]}, Date: {i["Date"]}, Medium: {i["Medium"]}, Dimensions: {i["Dimensions"]}, Cost: {i["Cost"]}')
        print("")


def printArtistasProlificos(rta, numArtist, iyear, fyear):
    print(f"{41*'='} Req. No.6 (BONUS) Inputs {41*'='}")
    print(f"Searching artist born between {iyear} to {fyear}")
    print(f"Amount of artist in the Top Ranking: {numArtist}")
    print("")
    print(f"{41*'='} Req. No.6 (BONUS) Answer {41*'='}")
    print(f"The TOP {numArtist} most prolific artist in the period are:")
    print("")
    i = 1
    for artist in lt.iterator(rta["artistas"]):
        print(100*"-")
        print(f"{i}. {artist}")
        i += 1 
    print(100*"-")
    print("")
    print(f"{lt.getElement(rta['artistas'],1)['Nombre']} has {lt.getElement(rta['artistas'],1)['Total Obras']} in his/her name at the museum.")
    print(f"The first {numArtist} pieces of his/her work sorted by acquired date are:")
    print("")
    i = 1
    for obra in lt.iterator(rta['obras']): 
        print(100*"-")
        print(f"{i}. {obra}")
        i += 1
    print(100*"-")
    print("")


# def printnArtworksOldestByMedium(oldestArtworks, n, medium):
#     print('')
#     print(f"{41*'='} Req. Lab No.5 Answer {41*'='}")
#     num = 1
#     if lt.size(oldestArtworks) >= n:
#         print(f"Las {n} obras más antiguas con la técnica {medium} son: ")
#         print("Nota: para ordenar solo se tienen en cuenta las obras con fecha disponible")
#         for i in lt.iterator(oldestArtworks):
#             if i["Date"] == 0:                 
#                 continue
#             else:
#                 print('')
#                 print(f"{num}. {i}")
#                 if num == n:
#                     break
#                 num += 1
#         print('')
#     else:
#         print(f"Solo se encontraron {lt.size(oldestArtworks)} obras con la técnica {medium}, estas son: ")
#         for i in lt.iterator(oldestArtworks):
#             print('')
#             print(f"{num}. {i}")
#             num += 1
#         print('')


# def printnumArtworks (total, nacionalidad):
#     print('')
#     print(f"{41*'='} Req. Lab No.6 Answer {41*'='}")
#     print(f"La nacionalidad '{nacionalidad}' tiene un numero total de obras de: {total}")
#     print("")

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
        print(f"Se cargaron {lt.size(catalog['artists'])} artistas")
        print("")
        print(f"Se cargaron {lt.size(catalog['artworks'])} obras")
        
    elif int(inputs[0]) == 2:
        try:
            iyear = int(input("Ingrese el año inicial: "))
            fyear = int(input("Ingrese el año final: "))
            artis_co = controller.getArtistsCronOrder(catalog, iyear, fyear)
            printArtistsCronOrder(artis_co, iyear, fyear)
        except:
            print("No ingreso años validos")

    elif int(inputs[0]) == 3:
        idate = input("Ingrese la fecha inicial (AAAA-MM-DD): ")
        fdate = input("Ingrese la fecha final (AAAA-MM-DD): ")
        try:
            adquis_co = controller.getArtworksCronOrder(catalog, idate, fdate)
            printArtworksCronOrder(adquis_co, idate, fdate)
        except:
            print("No ingreso fechas validas")

    elif int(inputs[0]) == 4:
        name = input("Ingrese el nombre del artista: ")
        artworks_co = controller.getArtworksByMedium(catalog, name)
        if artworks_co:
            printArtworksByMedium(artworks_co, name)
        else:
            print("El artista especificado no esta en la base de datos")  
            print("\n") 

    elif int(inputs[0]) == 5:
        printClasificationByNation(catalog["Req4"])

    elif int(inputs[0]) == 6:
        department = input("Ingrese el departamento: ")
        transport = controller.transportArtwDepartment(catalog, department)
        if transport:
            printTransportArtwDepartment(transport, department)
        else:
            print("No ingreso un departamento del museo")
        
    elif int(inputs[0]) == 7:
        #try:
        numArtist = int(input("Ingrese el número de artistas que desea en la clasificación: "))
        iyear = int(input("Ingrese el año inicial: "))
        fyear = int(input("Ingrese el año final: "))
        prolificos = controller.artistasProlificos(catalog, numArtist, iyear, fyear)
        printArtistasProlificos(prolificos, numArtist, iyear, fyear)
        #except:
            #print("Ingrese numeros enteros válidos")   

    else:
        sys.exit(0)
sys.exit(0)
