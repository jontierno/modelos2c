import csv
import operator
import sys

with open('/home/colopreda/ClionProjects/GranDT/GranDT2015_formatted.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	sortedlist = sorted(reader, key=operator.itemgetter(20), reverse=True)
	sortedlist.sort(key=lambda x: int(x[20]))

	arquero = [k for k in sortedlist if 'ARQ' in k]
	#reversed(arquero)
	defensa = [k for k in sortedlist if 'DEF' in k]
	volante = [k for k in sortedlist if 'VOL' in k]
	delantero = [k for k in sortedlist if 'DEL' in k]

	trescuatrotres = arquero[-1:]
	trescuatrotres.extend(defensa[-3:])
	trescuatrotres.extend(volante[-4:])
	trescuatrotres.extend(delantero[-3:])

	suma343 = sum(int(row[20]) for row in trescuatrotres)

	cuatrocuatrodos = arquero[-1:]
	cuatrocuatrodos.extend(defensa[-4:])
	cuatrocuatrodos.extend(volante[-4:])
	cuatrocuatrodos.extend(delantero[-2:])

	suma442 = sum(int(row[20]) for row in cuatrocuatrodos)

	cuatrotrestres = arquero[-1:]
	cuatrotrestres.extend(defensa[-4:])
	cuatrotrestres.extend(volante[-3:])
	cuatrotrestres.extend(delantero[-3:])

	suma433 = sum(int(row[20]) for row in cuatrotrestres)

	if (suma343 >= suma433 and suma343 >= suma442):
		print("La formacion seleccionada es 1-3-4-3 con los siguientes jugadores:\n")
		for row in trescuatrotres:				
			print(' - '.join(list( row[i] for i in [0, 1, 2, 3, 20] )))
		print("\nEl puntaje obtenido es: ", suma343)

	if (suma433 >= suma343 and suma433 >= suma442):
		print("La formacion seleccionada es 1-4-4-2 con los siguientes jugadores:\n")
		for row in cuatrotrestres:				
			print(' - '.join(list( row[i] for i in [0, 1, 2, 3, 20] )))
		print("\nEl puntaje obtenido es: ", suma433)

	if (suma442 >= suma343 and suma442 >= suma433):
		print("La formacion seleccionada es 1-4-3-3 con los siguientes jugadores:\n")
		for row in cuatrocuatrodos:				
			print(' - '.join(list( row[i] for i in [0, 1, 2, 3, 20] )))
		print("\nEl puntaje obtenido es: ", suma442)