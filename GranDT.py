#!/usr/bin/python3

import csv
import operator
import sys
import functools


with open('/home/colopreda/ClionProjects/GranDT/GranDT2015_formatted.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	jugadores = sorted(reader, key=operator.itemgetter(23), reverse=True)
	jugadores.sort(key=lambda x: int(x[23]))

	arquero = [k for k in jugadores if 'ARQ' in k]
	defensa = [k for k in jugadores if 'DEF' in k]
	volante = [k for k in jugadores if 'VOL' in k]
	delantero = [k for k in jugadores if 'DEL' in k]

	trescuatrotres = arquero[-1:]
	trescuatrotres.extend(defensa[-3:])
	trescuatrotres.extend(volante[-4:])
	trescuatrotres.extend(delantero[-3:])

	suma343 = sum(int(row[23]) for row in trescuatrotres)

	cuatrocuatrodos = arquero[-1:]
	cuatrocuatrodos.extend(defensa[-4:])
	cuatrocuatrodos.extend(volante[-4:])
	cuatrocuatrodos.extend(delantero[-2:])

	suma442 = sum(int(row[23]) for row in cuatrocuatrodos)

	cuatrotrestres = arquero[-1:]
	cuatrotrestres.extend(defensa[-4:])
	cuatrotrestres.extend(volante[-3:])
	cuatrotrestres.extend(delantero[-3:])

	suma433 = sum(int(row[23]) for row in cuatrotrestres)

	if (suma343 >= suma433 and suma343 >= suma442):
		formacionSel = trescuatrotres
		print("La formacion seleccionada es 1-3-4-3 con los siguientes jugadores:\n")
	elif (suma433 >= suma343 and suma433 >= suma442):
		formacionSel = cuatrotrestres
		print("La formacion seleccionada es 1-4-3-3 con los siguientes jugadores:\n")
	else:
		formacionSel = cuatrocuatrodos
		print("La formacion seleccionada es 1-4-4-2 con los siguientes jugadores:\n")

	for row in formacionSel:				
		print(' - '.join(list( row[i] for i in [0, 1, 2, 3, 23] )))

	puntaje = sum((sum([int(player[i]) for player in formacionSel])) for i in range(4, 19))
	puntaje += sum((max([int(player[i]) for player in formacionSel])) for i in range(4, 19))
	print("\nEl puntaje obtenido es: ", puntaje)
	cotizacion = sum(int(row[3]) for row in formacionSel)
	print("La cotización total del equipo es: ", cotizacion)


	# 	print("La formacion seleccionada es 1-3-4-3 con los siguientes jugadores:\n")
	# 	for row in trescuatrotres:				
	# 		print(' - '.join(list( row[i] for i in [0, 1, 2, 3, 20] )))
	# 	suma343 += sum((max([int(player[i]) for player in trescuatrotres])) for i in range(4, 19))
	# 	print("\nEl puntaje obtenido es: ", suma343)

	# if (suma433 >= suma343 and suma433 >= suma442):
	# 	print("La formacion seleccionada es 1-4-4-2 con los siguientes jugadores:\n")
	# 	for row in cuatrotrestres:				
	# 		print(' - '.join(list( row[i] for i in [0, 1, 2, 3, 20] )))
	# 	suma433 += sum((max([int(player[i]) for player in trescuatrotres])) for i in range(4, 19))
	# 	print("\nEl puntaje obtenido es: ", suma433)

	# if (suma442 >= suma343 and suma442 >= suma433):
	# 	print("La formacion seleccionada es 1-4-3-3 con los siguientes jugadores:\n")
	# 	for row in cuatrocuatrodos:				
	# 		print(' - '.join(list( row[i] for i in [0, 1, 2, 3, 20] )))

	# 	print("\nEl puntaje obtenido es: ", suma442)


	# print("--------------------------------------------------------------")

	# print("<><><><><><><><><><><><>")
	# [print(str(i-3)+":"+str(max([int(player[i]) for player in trescuatrotres]))) for i in range(4, 19)]

	# Puntaje con GLPK = 1676
