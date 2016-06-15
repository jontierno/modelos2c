#!/usr/bin/python3

import csv
import operator
import sys
import functools
from collections import Counter
from operator import itemgetter
from jugador import Jugador
from equipo import Equipo
from formacion import Formacion
# CONSTANTES

JUG_POR_EQUIPO = 3
COTIZACION_MAX = 65000000
FECHAS = 15
COLUMNA_FECHA_1 = 4
SUPLENTES_POR_PUESTO=0
def leerJugadores ():
	jugadores = []
	
	with open('GranDT2015_formatted_python.csv') as csvfile:
		id = 0
		rows = csv.reader(csvfile, delimiter=',', quotechar='"')
		for i in rows:
			puntajes = []
			for x in range(COLUMNA_FECHA_1, COLUMNA_FECHA_1+FECHAS):
				puntajes.append(float(i[x]))
			jugadores.append(Jugador(id, i[0], i[1], i[2], float(i[3]), puntajes))
			id = id +1
	return jugadores

def equipoIdeal(fecha, jugadores,suplentes):

	#ordeno por el índice de la fecha
	jugadores.sort(key=lambda y: y.sensibilidad[0], reverse=True)

	#Genero un equipo por cada formacion
	tresCuatrores =	Equipo(Formacion(3,4,3,suplentes),COTIZACION_MAX,fecha)
	cuatrocuatrodos = Equipo(Formacion(4,4,2,suplentes),COTIZACION_MAX,fecha)
	cuatrotrestres = Equipo(Formacion(4,3,3,suplentes),COTIZACION_MAX,fecha)
	
	resultados = []
	resultados.append(tresCuatrores)
	resultados.append(cuatrocuatrodos)
	resultados.append(cuatrotrestres)

	#los armo de forma tal que solamente entren como suplentes.
	for j in jugadores:
		tresCuatrores.agregar(j, False)
		cuatrocuatrodos.agregar(j, False)
		cuatrotrestres.agregar(j, False)

	resultados.sort(key=lambda x: x.puntaje)
	return resultados.pop()
	#ordeno las formaciones y me quedo con la que obtuvo mas puntaje

def completarEquipo(equipo, jugadores, fecha):
    jugadores.sort(key=lambda y: y.sensibilidad[fecha], reverse=True)
    for j in jugadores:
        if not equipo.existe(j) and equipo.agregar(j, True):
            equipo.transferencias +=1

def imprimirEquipo(equipo):
    print(equipo)

    #arqueros  titulares
    arqueros = [x for x in equipo.jugadores if x["jugador"].posicion =="ARQ" and x["titular"]]

    defensores = [x for x in equipo.jugadores if x["jugador"].posicion == "DEF" and x["titular"]]

    volantes = [x for x in equipo.jugadores if x["jugador"].posicion == "VOL" and x["titular"]]

    delanteros = [x for x in equipo.jugadores if x["jugador"].posicion == "DEL" and x["titular"]]
    puntajetotal = 0
    print("")
    print("Titulares")
    for j in arqueros: print("{} {} {}".format(j["jugador"],j["jugador"].puntajes[equipo.fecha], ", Capitan" if j["capitan"] else ""))

    for j in defensores: print("{} {} {}".format(j["jugador"],j["jugador"].puntajes[equipo.fecha], ", Capitan" if j["capitan"] else ""))
    for j in volantes: print("{} {} {}".format(j["jugador"],j["jugador"].puntajes[equipo.fecha], ", Capitan" if j["capitan"] else ""))
    for j in delanteros: print("{} {} {}".format(j["jugador"],j["jugador"].puntajes[equipo.fecha], ", Capitan" if j["capitan"] else ""))
    print()
    if(SUPLENTES_POR_PUESTO > 0) :
        print("Suplentes")
        for j in [x for x in equipo.jugadores if x["titular"] == False]: print("{} {} {}".format(j["jugador"], j["jugador"].puntajes[equipo.fecha],", Capitan" if j["capitan"] else ""))
    print("-------------------------------------------------------------------------------------------------------------")

def contarTransferencias ( previo, equipo):
    matches = 0
    for j in previo.jugadores:
        matches += len([x for x in equipo.jugadores if x["jugador"] == j["jugador"]])

    return len(equipo.jugadores) - matches

#equiposPorFechas = []
#equipoIdeal()
#puntajeTotal = 0

equipos = []

jugadores = leerJugadores()
equipo = equipoIdeal(0, jugadores,SUPLENTES_POR_PUESTO)




completarEquipo(equipo, jugadores, equipo.fecha+1)
equipos.append(equipo)
equipo.reordenarTitulares()
equipo.transferencias = 0
formacionesPosibles = [Formacion(3, 4, 3, SUPLENTES_POR_PUESTO), Formacion(4, 4, 2, SUPLENTES_POR_PUESTO),Formacion(4, 3, 3, SUPLENTES_POR_PUESTO)]

for x in range(1,FECHAS):
    equiposEnFecha = []
    for f in formacionesPosibles:
        formacion = f.clonar()
        equipo1 = equipos[x-1].clonar()
        equipo1.formacion = formacion
        equipo1.fecha = x
		#esto saca un titular del equipo, por eso lo hago.
        equipo1.reordenarTitulares()
        #completo el equipo dsps de cambiar la formación ya que alguno quedó afuera sí o sí.
        completarEquipo(equipo1,jugadores,x)


        equipo1.mejorar(jugadores)
        equipo1.reordenarTitulares()
        equiposEnFecha.append(equipo1)

    # tomo el que mas puntos hizo
    equiposEnFecha.sort(key=lambda x: x.puntaje, reverse=False)
    equipos.append(equiposEnFecha.pop())

puntaje = 0

previo = 0
for e in equipos:
    puntaje += e.puntaje
    print()
    imprimirEquipo(e)
 #   if e != equipos[0]:
 #       transferencias = contarTransferencias(previo,e)
 #       print("Transferencias contadas:", transferencias)
 #   previo = e

print()
print ("Puntaje Total:",puntaje)
