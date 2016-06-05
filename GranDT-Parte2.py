#!/usr/bin/python3

import csv
import operator
import sys
import functools
from collections import Counter
from operator import itemgetter

JUG_POR_EQUIPO = 3
COTIZACION_MAX = 65000000
FECHAS = 15
COLUMNA_FECHA_1 = 4

def equipoMas3Players(jugadores):
	#equipos = []
	#for row in jugadores:
	#	equipos.append(row[2]) 

	equipos = [j[2] for j in jugadores]

	cnt = Counter(equipos)
	equiposMas3 = [k for k, v in cnt.items() if v > JUG_POR_EQUIPO]
	return equiposMas3

def cambiarJugador(equiposMas3, jugadores, datos):
	#jugadoresAfectados = [] 
	#for s in jugadores:
	#	for item in equiposMas3:
	#		if item in s:
	#			jugadoresAfectados.append(s)

	jugadoresAfectados = [j for j in jugadores if j[2] in equiposMas3]

	if jugadoresAfectados:
		jugadorASacarEnPos = jugadores.index(jugadoresAfectados[0])
		jugadorSuperado = jugadores.pop(jugadorASacarEnPos)
		reemplazo = datos[jugadorSuperado[1]][-1:]
		datos[jugadorSuperado[1]] = datos[jugadorSuperado[1]][:-1]

		jugadores += reemplazo
		jugadores.sort(key=lambda x: int(x[3]))

def generarEquipo(datos, defensas, volantes, delanteros):
	jugadores = []
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
	mascaro = jugadores.pop()
	reemplazo = datos[mascaro[1]][-1:]
	datos[mascaro[1]] = datos[mascaro[1]][:-1]

	jugadores += reemplazo
	jugadores.sort(key=lambda x: int(x[3]))

def sortPorPos(x):
	l = ["ARQ", "DEF", "VOL", "DEL"]
	return l.index(x[1])

def equipoIdeal():
	with open('GranDT2015_formatted_python.csv', newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		jugadores = sorted(reader, key=operator.itemgetter(23), reverse=True)
		jugadores.sort(key=lambda y: int(y[23]))

		datos = {
		"ARQ" : [k for k in jugadores if 'ARQ' in k],
		"DEF" : [k for k in jugadores if 'DEF' in k],
		"VOL" : [k for k in jugadores if 'VOL' in k],
		"DEL" : [k for k in jugadores if 'DEL' in k],
		}
		datos343 = datos.copy()
		trescuatrotres = generarEquipo(datos343, 3, 4, 3)
		suma343 = sum(int(row[23]) for row in trescuatrotres)

		datos442 = datos.copy()
		cuatrocuatrodos = generarEquipo(datos442, 4, 4, 2)
		suma442 = sum(int(row[23]) for row in cuatrocuatrodos)

		datos433 = datos.copy()
		cuatrotrestres = generarEquipo(datos433, 4, 3, 3)
		suma433 = sum(int(row[23]) for row in cuatrotrestres)

		if (suma343 >= suma433 and suma343 >= suma442):
			formacionSel = trescuatrotres
			datosSel = datos343
		elif (suma433 >= suma343 and suma433 >= suma442):
			formacionSel = cuatrotrestres
			datosSel = datos433
		else:
			formacionSel = cuatrocuatrodos
			datosSel = datos442

		cotizacion = sum(int(row[3]) for row in formacionSel)
		while (cotizacion > COTIZACION_MAX):
			reemplazarJugadorMasCaro(datosSel, formacionSel)
			cotizacion = sum(int(row[3]) for row in formacionSel)

		equiposMas3 = equipoMas3Players(formacionSel)
		while (equiposMas3):
			cambiarJugador(equiposMas3, formacionSel, datos)
			equiposMas3 = equipoMas3Players(formacionSel)

		formacionSel = sorted(formacionSel, key = sortPorPos)
		equiposPorFechas.append(formacionSel)

def jugadoresMenosPuntos(formacionActual, fecha):	
	ordenPorFecha = formacionActual
	ordenPorFecha.sort(key=lambda x: int(x[fecha]))
	menosPuntos = ordenPorFecha[:4]
	return menosPuntos

def transferencias(formacionActual, jugadoresMenosPuntaje, datos):

	for x in range(0,4):
		jugadorASacarEnPos = formacionActual.index(jugadoresMenosPuntaje[x])
		jugadorSuperado = formacionActual.pop(jugadorASacarEnPos)
		reemplazo = datos[jugadorSuperado[1]][-1:]
		datos[jugadorSuperado[1]] = datos[jugadorSuperado[1]][:-1]		
		while reemplazo[0] in formacionActual:
			datos[jugadorSuperado[1]] = datos[jugadorSuperado[1]][:-1]			
			reemplazo = datos[jugadorSuperado[1]][-1:]

		formacionActual += reemplazo
		formacionActual.sort(key=lambda x: int(x[3]))


equiposPorFechas = []
equipoIdeal()
puntajeTotal = 0

for x in range(COLUMNA_FECHA_1, COLUMNA_FECHA_1+FECHAS):
	with open('GranDT2015_formatted_python.csv', newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		jugadores = sorted(reader, key=operator.itemgetter(x), reverse=True)
		jugadores.sort(key=lambda y: int(y[x]))

		datos = {
		"ARQ" : [k for k in jugadores if 'ARQ' in k],
		"DEF" : [k for k in jugadores if 'DEF' in k],
		"VOL" : [k for k in jugadores if 'VOL' in k],
		"DEL" : [k for k in jugadores if 'DEL' in k],
		}

		formacionActual = equiposPorFechas[x - COLUMNA_FECHA_1]
		jugadoresMenosPuntaje = jugadoresMenosPuntos(formacionActual, x)

		transferencias(formacionActual, jugadoresMenosPuntaje, datos)

		cotizacion = sum(int(row[3]) for row in formacionActual)
		while (cotizacion > COTIZACION_MAX):
			reemplazarJugadorMasCaro(datosSel, formacionActual)
			cotizacion = sum(int(row[3]) for row in formacionActual)

		equiposMas3 = equipoMas3Players(formacionActual)
		while (equiposMas3):
			cambiarJugador(equiposMas3, formacionActual, datos)
			equiposMas3 = equipoMas3Players(formacionActual)

		formacionActual = sorted(formacionActual, key = sortPorPos)
		equiposPorFechas.append(formacionActual)

		print ("{:<25}{:^10}{:<20}{:<15}{:<10}".format("Nombre","Pos","Equipo", "Cotizacion", "Puntaje"))
		print ("{:<25}{:^10}{:<20}{:<15}{:<10}\n".format("-"*6,"-"*3,"-"*6, "-"*10, "-"*7))
		for row in formacionActual:				
			print ("{:<25}{:^10}{:<20}{:<15}{:<10}".format(row[0],row[1],row[2], row[3], row[x]))
		puntaje = sum(int(row[x]) for row in formacionActual)
		puntajeTotal += puntaje
		#puntaje = sum((sum([int(player[i]) for player in formacionSel])) for i in range(4, 19))
		#puntaje += sum((max([int(player[i]) for player in formacionSel])) for i in range(4, 19))
		print("\nEl puntaje obtenido es: ", puntaje)

		print("La cotizacion total del equipo es: ", cotizacion)

print("\n----------------------------------------\n")
print("El puntaje total hecho por este equipo es: ", puntajeTotal)
print("\n")
