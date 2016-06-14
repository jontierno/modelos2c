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
SUPLENTES_POR_PUESTO=1
def leerJugadores ():
	jugadores = []
	
	with open('GranDT2015_formatted_python.csv') as csvfile:
		id = 0
		rows = csv.reader(csvfile, delimiter=',', quotechar='"')
		for i in rows:
			puntajes = []
			for x in range(COLUMNA_FECHA_1, COLUMNA_FECHA_1+FECHAS):
				puntajes.append(int(i[x]))
			jugadores.append(Jugador(id, i[0], i[1], i[2], int(i[3]), puntajes))
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

def equipoMas3Players(jugadores):
	pass

def cambiarJugador(equiposMas3, jugadores, datos):
	
	# Crea una lista con los jugadores del equipo que tiene mas de 3 jugadores

	jugadoresAfectados = [j for j in jugadores if j[2] in equiposMas3]

	if jugadoresAfectados:
		# Busca el indice
		jugadorASacarEnPos = jugadores.index(jugadoresAfectados[0])
		# Lo saca del equipo
		jugadorSuperado = jugadores.pop(jugadorASacarEnPos)
		# Busca un reemplazo en la misma posicion
		reemplazo = datos[jugadorSuperado[1]][-1:]
		# Saca a ese jugador de la lista de posibles reemplazos
		datos[jugadorSuperado[1]] = datos[jugadorSuperado[1]][:-1]

		# Agrega al reemplazo al equipo
		jugadores += reemplazo
		# Ordena por cotizacion
		jugadores.sort(key=lambda x: int(x[3]))

def generarEquipo(datos, defensas, volantes, delanteros, fecha):
	pass

def reemplazarJugadorMasCaro(datos, jugadores):
	# Al estar siempre ordenado por cotizacion, el pop saca el jugador mas caro
	mascaro = jugadores.pop()
	# Busca el reemplazo que tenga la mayor cantidad de puntos en su posicion
	reemplazo = datos[mascaro[1]][-1:]
	# Lo saca del mapa para que si hay que reemplazar otro no vuelva a aparecer
	datos[mascaro[1]] = datos[mascaro[1]][:-1]

	# Lo agrega al equipo
	jugadores += reemplazo
	# Ordeno por cotizacion
	jugadores.sort(key=lambda x: int(x[3]))

def sortPorPos(x):
	# Funcion que sirve solamente para que se vea linda la salida
	l = ["ARQ", "DEF", "VOL", "DEL"]
	return l.index(x[1])




def jugadoresMenosPuntos(formacionActual, fecha):	
	ordenPorFecha = formacionActual
	# Ordeno por menor cantidad de puntos en la fechas
	ordenPorFecha.sort(key=lambda x: int(x[fecha]))
	# Me quedo con los 4 que menos puntaje hicieron (van a salir del equipo)
	menosPuntos = ordenPorFecha[:4]
	return menosPuntos

def transferencias(formacionActual, jugadoresMenosPuntaje, datos):

	# Elijo 4 jugadores que van a entrar
	for x in range(0,4):
		# Selecciono un jugador de la lista de jugadores que menos puntaje
		# hicieron en esa fecha
		jugadorASacarEnPos = formacionActual.index(jugadoresMenosPuntaje[x])
		# Lo saco del equipo
		jugadorSuperado = formacionActual.pop(jugadorASacarEnPos)
		# Le busco un reemplazo
		reemplazo = datos[jugadorSuperado[1]][-1:]
		# Saco al reemplazo de los posibles reemplazos		
		datos[jugadorSuperado[1]] = datos[jugadorSuperado[1]][:-1]		
		# Me fijo si el reemplazo ya estaba en el equipo, si es asi busco al siguiente
		while reemplazo[0] in formacionActual:
			datos[jugadorSuperado[1]] = datos[jugadorSuperado[1]][:-1]			
			reemplazo = datos[jugadorSuperado[1]][-1:]

		# Agrego al reemplazo al equipo
		formacionActual += reemplazo
		formacionActual.sort(key=lambda x: int(x[3]))

def imprimirEquipo(equipo):
    print(equipo)
    ## busco la siguiente fecha.
    for j in equipo.jugadores:
        print("{}, Titular: {}".format(j["jugador"], j["titular"]))
    print()

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

formacionesPosibles = [Formacion(3, 4, 3, SUPLENTES_POR_PUESTO), Formacion(4, 4, 2, SUPLENTES_POR_PUESTO),Formacion(4, 3, 3, SUPLENTES_POR_PUESTO)]

for x in range(1,FECHAS):
    equiposEnFecha = []
    for f in formacionesPosibles:
        formacion = f.clonar()
        equipo1 = equipos[x-1].clonar()
        equipo1.formacion = formacion
        equipo1.fecha = x
        equipo1.reordenarTitulares()
        completarEquipo(equipo1,jugadores,x)
        equipo1.mejorar(jugadores)
        equiposEnFecha.append(equipo1)

    # tomo el que mas puntos hizo
    equiposEnFecha.sort(key=lambda x: x.puntaje)
    equipos.append(equiposEnFecha.pop())

puntaje = 0

previo = 0
for e in equipos:
    puntaje += e.puntaje
    imprimirEquipo(e)
    #if e != equipos[0]:
    #    transferencias = contarTransferencias(previo,e)
    #    print("Transferencias contadas:", transferencias)
    #previo = e


print ("Puntaje Total:",puntaje)
