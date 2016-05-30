#!/usr/bin/python3

import csv
import operator
import sys
import functools
from collections import Counter

def equipoMas3Players(jugadores):
	equipos = []
	for row in jugadores:
		equipos.append(row[2]) 
	cnt = Counter(equipos)
	equiposMas3 = ([k for k, v in cnt.items() if v > 3])
	return equiposMas3

def cambiarJugador(equiposMas3, jugadores, datos):
	#jugadoresAfectados = [k for k in jugadores if k in equiposMas3]
	#print(jugadoresAfectados)
	jugadoresAfectados = []
	for s in jugadores:
		for item in equiposMas3:
			if item in s:
				jugadoresAfectados.append(s)

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

with open('GranDT2015_formatted_python.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	jugadores = sorted(reader, key=operator.itemgetter(23), reverse=True)
	jugadores.sort(key=lambda x: int(x[23]))

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
		print("La formacion seleccionada es 1-3-4-3 con los siguientes jugadores:\n")
	elif (suma433 >= suma343 and suma433 >= suma442):
		formacionSel = cuatrotrestres
		datosSel = datos433
		print("La formacion seleccionada es 1-4-3-3 con los siguientes jugadores:\n")
	else:
		formacionSel = cuatrocuatrodos
		datosSel = datos442
		print("La formacion seleccionada es 1-4-4-2 con los siguientes jugadores:\n")

	cotizacion = sum(int(row[3]) for row in formacionSel)
	while (cotizacion > 65000000):
		reemplazarJugadorMasCaro(datosSel, formacionSel)
		cotizacion = sum(int(row[3]) for row in formacionSel)

	equiposMas3 = equipoMas3Players(formacionSel)
	while (equiposMas3):
		cambiarJugador(equiposMas3, formacionSel, datos)
		equiposMas3 = equipoMas3Players(formacionSel)

	formacionSel = sorted(formacionSel, key = sortPorPos)

	print ("{:<20}{:^10}{:<20}{:<15}{:<10}".format("Nombre","Pos","Equipo", "Cotizacion", "Puntaje"))
	print ("{:<20}{:^10}{:<20}{:<15}{:<10}\n".format("-"*6,"-"*3,"-"*6, "-"*10, "-"*7))
	for row in formacionSel:				
		print ("{:<20}{:^10}{:<20}{:<15}{:<10}".format(row[0],row[1],row[2], row[3], row[23]))

	puntaje = sum((sum([int(player[i]) for player in formacionSel])) for i in range(4, 19))
	puntaje += sum((max([int(player[i]) for player in formacionSel])) for i in range(4, 19))
	print("\nEl puntaje obtenido es: ", puntaje)

	print("La cotizacion total del equipo es: ", cotizacion)
