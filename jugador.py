
import math
MU =  0.9
class Jugador:

	def __init__(self, id, nombre, posicion, equipo, cotizacion, puntajes):
		self.id = id
		self.nombre = nombre
		self.posicion = posicion
		self.equipo = equipo
		self.cotizacion = cotizacion
		self.puntajes = puntajes
		self.puntajeTotal = sum (puntajes)
		self.sensibilidad = []

		media = sum(puntajes) / len(puntajes)

		for i in puntajes:
			self.sensibilidad.append(self.calcularIndiceSensibilidad(i, media))
			media -= i *MU/ len(puntajes)


	def calcularIndiceSensibilidad (self, puntaje, media ):
		return  puntaje + media
		#return puntaje

	def __str__(self):
		return "{} {} {} {}".format(self.nombre, self.posicion, self.equipo, self.cotizacion)