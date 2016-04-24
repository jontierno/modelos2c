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

	for row in trescuatrotres:				
		print(row)

	print(sum(int(row[20]) for row in trescuatrotres))

	cuatrocuatrodos = arquero[-1:]
	cuatrocuatrodos.extend(defensa[-4:])
	cuatrocuatrodos.extend(volante[-4:])
	cuatrocuatrodos.extend(delantero[-2:])

	for row in cuatrocuatrodos:				
		print(row)

	print(sum(int(row[20]) for row in cuatrocuatrodos))

	cuatrotrestres = arquero[-1:]
	cuatrotrestres.extend(defensa[-4:])
	cuatrotrestres.extend(volante[-3:])
	cuatrotrestres.extend(delantero[-3:])

	for row in cuatrotrestres:				
		print(row)

	print(sum(int(row[20]) for row in cuatrotrestres))

	