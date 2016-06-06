#!/usr/bin/python3

import csv
import operator
import sys
import functools
from collections import Counter
from operator import itemgetter

# CONSTANTES

JUG_POR_EQUIPO = 3
COTIZACION_MAX = 65000000
FECHAS = 15
COLUMNA_FECHA_1 = 4

def equipoMas3Players(jugadores):

	# Crea una lista solo con los equipos de los jugadores
	equipos = [j[2] for j in jugadores]

	cnt = Counter(equipos)
	# Cuenta las repeticiones de un elemento dentro de la lista para ver si esta mas de 3 veces
	equiposMas3 = [k for k, v in cnt.items() if v > JUG_POR_EQUIPO]
	return equiposMas3

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

def generarEquipo(datos, defensas, volantes, delanteros):
	jugadores = []
	# Genero una lista con los mejores jugadores, segun la formacion
	jugadores += datos["ARQ"][-1:]
	datos["ARQ"] = datos["ARQ"][:-1]
	jugadores += datos["DEF"][-defensas:]
	datos["DEF"] = datos["DEF"][:-defensas]
	jugadores += datos["VOL"][-volantes:]
	datos["VOL"] = datos["VOL"][:-volantes]
	jugadores += datos["DEL"][-delanteros:]
	datos["DEL"] = datos["DEL"][:-delanteros]

	jugadores.sort(key=lambda x: int(x[3]))
	return jugadores

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

def equipoIdeal():
	# Abro el archivo csv
	with open('GranDT2015_formatted_python.csv') as csvfile:
		# Lo parseo
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		# Lo ordeno por puntaje total del torneo
		jugadores = sorted(reader, key=operator.itemgetter(23), reverse=True)
		jugadores.sort(key=lambda y: int(y[23]))

		# Creo mapa con todos los datos
		datos = {
		"ARQ" : [k for k in jugadores if 'ARQ' in k],
		"DEF" : [k for k in jugadores if 'DEF' in k],
		"VOL" : [k for k in jugadores if 'VOL' in k],
		"DEL" : [k for k in jugadores if 'DEL' in k],
		}
		# Creo copia para formacion 343
		datos343 = datos.copy()
		trescuatrotres = generarEquipo(datos343, 3, 4, 3)
		# Puntuacion total de esta formacion
		suma343 = sum(int(row[23]) for row in trescuatrotres)

		# Creo copia para formacion 442
		datos442 = datos.copy()
		cuatrocuatrodos = generarEquipo(datos442, 4, 4, 2)
		# Puntuacion total de esta formacion
		suma442 = sum(int(row[23]) for row in cuatrocuatrodos)

		# Creo copia para formacion 442
		datos433 = datos.copy()
		cuatrotrestres = generarEquipo(datos433, 4, 3, 3)
		# Puntuacion total de esta formacion
		suma433 = sum(int(row[23]) for row in cuatrotrestres)

		# Comparando las diferentes sumas, veo cual es la formacion conveniente
		if (suma343 >= suma433 and suma343 >= suma442):
			formacionSel = trescuatrotres
			datosSel = datos343
		elif (suma433 >= suma343 and suma433 >= suma442):
			formacionSel = cuatrotrestres
			datosSel = datos433
		else:
			formacionSel = cuatrocuatrodos
			datosSel = datos442

		# Veo si se pasa por cotizacion, si se pasa, lo cambio
		cotizacion = sum(int(row[3]) for row in formacionSel)
		while (cotizacion > COTIZACION_MAX):
			reemplazarJugadorMasCaro(datosSel, formacionSel)
			cotizacion = sum(int(row[3]) for row in formacionSel)

		# Veo si el equipo tiene mas de 3 jugadores de un equipo, si es asi, cambio al peor
		equiposMas3 = equipoMas3Players(formacionSel)
		while (equiposMas3):
			cambiarJugador(equiposMas3, formacionSel, datos)
			equiposMas3 = equipoMas3Players(formacionSel)

		formacionSel = sorted(formacionSel, key = sortPorPos)
		# Lista de listas que va a ir teniendo a todos los equipos elegidos en las diferentes 
		# fechas, siendo la posicion 0 el equipo ideal para tener una base
		equiposPorFechas.append(formacionSel)

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


equiposPorFechas = []
equipoIdeal()
puntajeTotal = 0

for x in range(COLUMNA_FECHA_1, COLUMNA_FECHA_1+FECHAS):
	with open('GranDT2015_formatted_python.csv') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		jugadores = sorted(reader, key=operator.itemgetter(x), reverse=True)
		jugadores.sort(key=lambda y: int(y[x]))

		# Creo el mapa de datos para la fecha X
		datos = {
		"ARQ" : [k for k in jugadores if 'ARQ' in k],
		"DEF" : [k for k in jugadores if 'DEF' in k],
		"VOL" : [k for k in jugadores if 'VOL' in k],
		"DEL" : [k for k in jugadores if 'DEL' in k],
		}

		# Uso de base la formacion de la fecha anterior
		formacionActual = equiposPorFechas[x - COLUMNA_FECHA_1]
		# Lista con los jugadores con menos puntaje
		jugadoresMenosPuntaje = jugadoresMenosPuntos(formacionActual, x)

		# Hago las transferencias
		transferencias(formacionActual, jugadoresMenosPuntaje, datos)

		# Chequeo que no se haya excedido de presupuesto
		cotizacion = sum(int(row[3]) for row in formacionActual)
		while (cotizacion > COTIZACION_MAX):
			reemplazarJugadorMasCaro(datosSel, formacionActual)
			cotizacion = sum(int(row[3]) for row in formacionActual)

		# Chequeo que no haya mas de 3 jugadores de un mismo equipo
		equiposMas3 = equipoMas3Players(formacionActual)
		while (equiposMas3):
			cambiarJugador(equiposMas3, formacionActual, datos)
			equiposMas3 = equipoMas3Players(formacionActual)

		# Ordeno para que se impriman bien
		formacionActual = sorted(formacionActual, key = sortPorPos)
		# Lo agrego a la lista de equipos por fecha
		equiposPorFechas.append(formacionActual)

		# Impresion
		print ("{:<25}{:^10}{:<20}{:<15}{:<10}".format("Nombre","Pos","Equipo", "Cotizacion", "Puntaje"))
		print ("{:<25}{:^10}{:<20}{:<15}{:<10}\n".format("-"*6,"-"*3,"-"*6, "-"*10, "-"*7))
		for row in formacionActual:				
			print ("{:<25}{:^10}{:<20}{:<15}{:<10}".format(row[0],row[1],row[2], row[3], row[x]))
		puntaje = sum(int(row[x]) for row in formacionActual)
		puntajeTotal += puntaje
		#puntaje = sum((sum([int(player[i]) for player in formacionSel])) for i in range(4, 19))
		#puntaje += sum((max([int(player[i]) for player in formacionSel])) for i in range(4, 19))
		print "\nEl puntaje obtenido es: ", puntaje

		print "La cotizacion total del equipo es: ", cotizacion

print "\n----------------------------------------\n"
print  "El puntaje total hecho por este equipo es: ", puntajeTotal
print("\n")
